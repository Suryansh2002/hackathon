import asyncio
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from utils.database import get_upcoming_task
from utils.ai import task_complete, handle_input
from messages import UAgentMessage, UAgentResponseType

assistant = Agent(name="scheduler", seed="scheduler-agent")

fund_agent_if_low(str(assistant.wallet.address()))


@assistant.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("AI Assistant agent started")


@assistant.on_interval(1)
async def check_tasks(ctx: Context):
    task = get_upcoming_task()
    if task is None:
        return

    content = await asyncio.to_thread(
        task_complete,
        task.name,
        task.description,
    )

    await ctx.send(
        task.address, UAgentMessage(type=UAgentResponseType.MESSAGE, message=content)
    )

    task.delete()


@assistant.on_message(model=UAgentMessage)
async def receive_request(ctx: Context, sender: str, message: UAgentMessage):
    # Agent can create reminders, appointments, show all tasks and even respond intelligently to user queries
    ctx.logger.info(f"Received request from {sender}: {message.message}")
    content = await asyncio.to_thread(handle_input, sender, message.message)
    await ctx.send(
        sender, UAgentMessage(type=UAgentResponseType.MESSAGE, message=content)
    )
