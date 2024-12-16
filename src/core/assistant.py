from langchain_core.runnables import Runnable, RunnableConfig
from core.state import State

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
                messages = state["messages"] + [("user", "Please provide a meaningful response.")]
                state = {**state, "messages": messages}
            else:
                break
        
        return {"messages": result}