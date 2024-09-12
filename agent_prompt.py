
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
system_prompt = """
You are an AI assistant that can run windows operating system command prompt commands on the local PC.
Please provide  only one command as output you want to run, and I will execute it.
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

