from __future__ import annotations
import os
import time
from enum import StrEnum
from typing import Optional
from utils.exceptions import AppointmentConflictError
from utils.time_manager import get_current_time, get_datetime_string
from datetime import datetime, timedelta

from odmantic import Model
from pymongo import MongoClient
from odmantic.engine import SyncEngine
from odmantic import Field

from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
assert MONGODB_URL, "Please set the MONGODB_URL environment variable"

client = MongoClient(MONGODB_URL)
engine = SyncEngine(client, database="tasks")


class TaskType(StrEnum):
    appointment = "appointment"
    reminder = "reminder"


class Task(Model):
    address: str = Field(index=True)
    name: str
    type: TaskType
    description: str
    start: datetime
    end: Optional[datetime] = None

    def save(self):
        engine.save(self)

    def delete(self):
        engine.delete(self)

    @property
    def length(self) -> Optional[timedelta]:
        if self.end:
            return self.end - self.start


tasks: list[Task] = []


def my_all_tasks(address: str):
    # All tasks for a particular address
    return [
        {
            "name": task.name,
            "description": task.description,
            "start": get_datetime_string(task.start),
        }
        for task in engine.find(Task, Task.address == address)
    ]


def delete_dead_task():
    for task in engine.find(Task):
        if task.end:
            if task.end < get_current_time():
                task.delete()


def get_upcoming_task() -> Optional[Task]:
    # Latest task is the task that needs to be proessed first
    return engine.find_one(
        Task, Task.start < get_current_time(), sort=Task.start.asc() # pyright:ignore[reportGeneralTypeIssues]
    )  


def create_task(
    address: str,
    type: TaskType,
    name: str,
    description: str,
    start: datetime,
    end: Optional[datetime] = None,
):
    # Removing tzinfo because odmantic ODM doesn't support timezone aware datetime
    start = start.replace(tzinfo=None)
    if end:
        end = end.replace(tzinfo=None)
    if end:
        for t in tasks:
            if t.type == TaskType.appointment and t.end:
                if (
                    (t.start < end and t.end > end)
                    or (t.start < start and t.end > start)
                    or (t.start > start and t.end < end)
                ):
                    raise AppointmentConflictError("Appointment conflict !")

    task = Task(
        address=address,
        name=name,
        type=type,
        description=description,
        start=start,
        end=end,
    )

    task.save()


def remove_task(address: str, start: datetime):
    for task in engine.find(Task, Task.address == address):
        if task.start.strftime("%Y-%m-%dT%H:%M:%S") == start.strftime(
            "%Y-%m-%dT%H:%M:%S"
        ):
            task.delete()
            return True
    return False
