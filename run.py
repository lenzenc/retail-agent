import questionary
from retail.database import create_db, delete_db
from retail.collection import ingest_data, delete_collection
from retail.agents import router_agent
from swarm.repl import run_demo_loop
from dotenv import load_dotenv

load_dotenv()

def run():

    create_db()
    ingest_data()
    run_demo_loop(router_agent, debug=False)

def main():

    options = {
        "Run": run,
        "Delete Database": delete_db,
        "Delete Vector Collection": delete_collection,
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
