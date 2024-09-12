import argparse
from core import execute_user_query

def main():
    parser = argparse.ArgumentParser(description="Run Codex commands.")
    parser.add_argument('run', help="Run the Codex command", nargs='?')
    args = parser.parse_args()

    if args.run:
        user_query = input("i'm ur codex ai-agent executer how i can help you: ?")
        execute_user_query(user_query)

if __name__ == "__main__":
    main()