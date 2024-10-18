from swarm import Agent
from retail.database import get_schema, run_sql_select_statement
import sys

def get_sql_agent_instructions():
    return f"""
        You are a SQL expert who takes in a request from a user for information
        they want to retrieve from the DB, creates a SELECT statement to retrieve the
        necessary information, and then invoke the function to run the query and
        get the results back to then report to the user the information they wanted to know.
        
        Here are the table schemas for the DB you can query:
        
        {get_schema()}

        Write all of your SQL SELECT statements to work 100% with these schemas and nothing else.
        You are always willing to create and execute the SQL statements to answer the user's question.
    """

router_agent = Agent(
    name = "Router Agent",
    instructions = """
        You are an orchestrator of different agents and it is your job to
        determine which of the agent is best suited to handle the user's request, 
        and transfer the conversation to that agent.
    """
)

orders_agent = Agent(
    name = "Order Agent",
    instructions = get_sql_agent_instructions() + "\n\nHelp the user with data related to orders",
    functions = [run_sql_select_statement]
)

items_agent = Agent(
    name = "Item Agent",
    instructions = get_sql_agent_instructions() + "\n\nHelp the user with data related to items",
    functions = [run_sql_select_statement]
)

def run_exit():
    sys.exit(1)

exit_agent = Agent(
    name = "Exit Agent",
    instructions = "If the user says anything about exiting then run this agent. Users could say 'exit', 'bye' or similar keywords",
    functions = [run_exit]
)

def transfer_back_to_router_agent():
    return router_agent

def transfer_to_orders_agent():
    return orders_agent

def transfer_to_items_agent():
    return items_agent

def transfer_to_exit_agent():
    return exit_agent

router_agent.functions = [transfer_to_items_agent, transfer_to_orders_agent, transfer_to_exit_agent]
orders_agent.functions.append(transfer_back_to_router_agent)
items_agent.functions.append(transfer_back_to_router_agent)
exit_agent.functions.append(transfer_to_exit_agent)