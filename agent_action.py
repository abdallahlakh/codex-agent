from agent_create import executor
from langchain_core.messages import HumanMessage
def run_agent(input_text):
    response = executor.invoke({"messages": [HumanMessage(content=input_text)]})
    return response
