from enum import Enum

from uagents import Model


class UAgentResponseType(Enum):
    ERROR = "error"
    MESSAGE = "message"


class UAgentMessage(Model):
    type: UAgentResponseType
    message: str
