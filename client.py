from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from enum import Enum
from uagents import Model


class UAgentResponseType(Enum):
    ERROR = "error"
    MESSAGE = "message"


class UAgentMessage(Model):
    type: UAgentResponseType
    message: str


main_agent = Agent(
    name="main_agent", port=8001, endpoint="http://localhost:8001/submit"
)

print(main_agent.address)
fund_agent_if_low(str(main_agent.wallet.address()))


@main_agent.on_message(model=UAgentMessage)
async def receive_update(ctx: Context, sender: str, message: UAgentMessage):
    if message.type == UAgentResponseType.MESSAGE:
        ctx.logger.info(f"{sender}: {message.message}")
    elif message.type == UAgentResponseType.ERROR:
        ctx.logger.error(f"{sender}: {message.message}")


@main_agent.on_event("startup")
async def start(ctx: Context):
    await ctx.send(
        "agent1qtr39jhpalmft4f0x5aye65ddsg6lwazygkesy00hr8jcty8ydh3khmyxvk",
        message=UAgentMessage(
            type=UAgentResponseType.MESSAGE, message="Say hi in 2 seconds !"
        ),
    )


if __name__ == "__main__":
    main_agent.run()
