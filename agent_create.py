from langchain.agents import AgentExecutor, create_openai_tools_agent
from agent_llm import llm
from agent_prompt import prompt
from agent_tool import command_tool
# Create an agent using the create_openai_tools_agent function
agent = create_openai_tools_agent(llm, [command_tool], prompt)

# Create an AgentExecutor to manage the agent
executor = AgentExecutor(agent=agent, tools=[command_tool])
