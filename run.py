import questionary
from retail.database import create_db, delete_db
from retail.agents import router_agent
from swarm.repl import run_demo_loop
from dotenv import load_dotenv

load_dotenv()

def run():

    create_db()
    run_demo_loop(router_agent)

def main():

    options = {
        "Run": run,
        "Delete Database": delete_db,
        "Exit": exit
    }

    choice = questionary.select(
        "Choose an Option",
        choices=list(options.keys())
    ).ask()

    if choice:
        options[choice]()

if __name__ == "__main__":
    main()
