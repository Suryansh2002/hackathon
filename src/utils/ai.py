import json
import os
import openai
from typing import Optional
from datetime import datetime
from utils.database import create_task, remove_task, my_all_tasks
from utils.time_manager import get_datetime, get_current_time
from utils.exceptions import AppointmentConflictError
from openai.types.chat.completion_create_params import Function

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
assert API_KEY, "Please use the API key"

client = openai.OpenAI(api_key=API_KEY)

GPT_MODEL = "gpt-4-1106-preview"
START_MESSAGE = "You are a personal time management assistant. You are resposible for helping me manage my time."


def prompt(messages: list[dict[str, str]]) -> str:
    _messages = [{"role": "system", "content": START_MESSAGE}]
    _messages.extend(messages)
    completion = client.chat.completions.create(
        model=GPT_MODEL,
        messages=_messages,  # pyright:ignore[reportGeneralTypeIssues]
    )
    return str(completion.choices[0].message.content)


def task_complete(
    title: str, description: str, start: Optional[datetime] = None
) -> str:
    """To generate task complete message by ai"""

    content = f"Write a simple sentence to say that the following scheduled event has arrived.\nTitle: {title}\n\ndescription: {description}.."
    if start:
        content += f"\n\nStarting Time: {start.strftime('%Y-%m-%dT%H:%M:%S%z')}"
    messages = [{"role": "user", "content": content}]
    return prompt(messages)


def task_created(title: str, description: str) -> str:
    """To generate task created message by ai"""

    content = f"Write a simple sentence to say Task Created Successfully for {title}!\n\nDescription: {description}.."
    messages = [{"role": "user", "content": content}]
    return prompt(messages)


# Functions are written in json schema for OpenAI
# These functions are called when certain conditions are met, like creating a task or deleting a task

create_function: Function = {
    "name": "create_task",
    "description": "Get the task information from the body of the input text",
    "parameters": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "description": 'Appointment type or reminder type. if the task has ending and starting time ,it is either "appointment" or "reminder"',
            },
            "name": {"type": "string", "description": "Name of the task"},
            "description": {"type": "string", "description": "Description of the task"},
            "start": {
                "type": "string",
                "description": "Starting Time of the task. It should be datetime format of %Y-%m-%dT%H:%M:%S%z by Indian timezone.",
            },
            "end": {
                "type": "string",
                "description": "Ending Time of the task. It should be datetime format of %Y-%m-%dT%H:%M:%S%z by Indian timezone. This field can be null also",
            },
        },
        "required": ["type", "name", "description", "start"],
    },
}

remove_function: Function = {
    "name": "remove_task",
    "description": "This function is called to delete the tasks !",
    "parameters": {
        "type": "object",
        "properties": {
            "start": {
                "type": "string",
                "description": "Starting Time of the task. It should be datetime format by Indian utc.",
            },
        },
        "required": ["start"],
    },
}


def handle_input(address: str, content: str) -> str:
    all_tasks = my_all_tasks(address)
    all_tasks = json.dumps(all_tasks, indent=3)

    completion = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": START_MESSAGE},
            {
                "role": "user",
                "content": f"Current India's Time is {get_current_time()}",
            },
            {
                "role": "user",
                "content": f"Here are your all tasks:\n{all_tasks},\n Start times can be seen from here !",
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        function_call="auto",
        functions=[create_function, remove_function],
    )

    message = json.loads(completion.json())["choices"][0]["message"]
    if function_call := message.get("function_call"):
        if function_call["name"] == "create_task":
            arguments = json.loads(function_call["arguments"])
            arguments["address"] = address
            try:
                arguments["start"] = get_datetime(arguments["start"])
                if arguments.get("end"):
                    arguments["end"] = get_datetime(arguments["end"])
            except ValueError:
                return handle_input(address, content)
            try:
                create_task(**arguments)
            except AppointmentConflictError:
                return prompt(
                    [{"role": "user", "content": "Say that Appointment Conflict !"}]
                )

            return task_created(
                "Task Created", f"Task Created Successfully for {content}!"
            )

        if function_call["name"] == "remove_task":
            arguments = json.loads(function_call["arguments"])
            arguments["address"] = address
            try:
                arguments["start"] = get_datetime(arguments["start"])
            except ValueError:
                return handle_input(address, content)

            if remove_task(**arguments):
                return task_created(
                    "Task Deleted", f"Task Deleted Successfully for {content}!"
                )
            else:
                return prompt(
                    [{"role": "user", "content": "Say that Task was not found !"}]
                )

    return str(message["content"])
