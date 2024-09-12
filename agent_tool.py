import subprocess
from langchain_core.tools import Tool

def run_command(command: str) -> str:
    """Run a command on the local PC and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print("result",result)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# Define the custom tool
command_tool = Tool(
    name="RunCommand",
    description="Run a command on the local PC",
    func=run_command
)