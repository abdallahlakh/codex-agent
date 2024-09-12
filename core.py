from agent_action import run_agent
from agent_tool import run_command

def execute_user_query(user_query):
    response = run_agent(user_query)
    final = run_command(response['output'])
    print(final)
    return final