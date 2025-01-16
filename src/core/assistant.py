from langchain_core.runnables import Runnable, RunnableConfig
from core.state import State
from pydantic import BaseModel, Field

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        """
        Process the current state and generate a response.
        
        :param state: Current conversation state
        :param config: Runnable configuration
        :return: Updated state with assistant's response
        """
        while True:
            result = self.runnable.invoke(state)
            
            # Handle empty or invalid responses
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        
        return {"messages": result}
    
class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant,
    who can re-route the dialog based on the user's needs."""

    cancel: bool = True
    reason: str

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "cancel": True,
                    "reason": "User changed their mind about the current task.",
                },
                {
                    "cancel": True,
                    "reason": "I have fully completed the task.",
                },
                {
                    "cancel": False,
                    "reason": "I need to search the user's emails or calendar for more information.",
                },
            ]
        }