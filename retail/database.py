import os
import sqlite3

DB = "retail.db"

def get_schema():
    with open("./sql/create-tables.sql", "r") as table_schema_file:
        return table_schema_file.read()    

def execute_sql_script(cursor, script_file):

    with open(script_file, 'r') as sql_file:
        sql_script = sql_file.read()
    
    statements = sql_script.split(';')
    for statement in statements:
        if statement.strip():
            cursor.execute(statement)

def create_db():
    
    if os.path.exists(DB):
        return

    print("Creating database....")    
    with sqlite3.connect(DB) as conn:

        cursor = conn.cursor()

        execute_sql_script(cursor, "./sql/create-tables.sql")
        conn.commit()        

        execute_sql_script(cursor, "./sql/data.sql")
        conn.commit()   

def delete_db():

    if os.path.exists(DB):
        try:
            os.remove(DB)
        except Exception as e:
            print(f"Error deleting database '{DB}': {e}")

def run_sql_select_statement(sql_statement):

    with sqlite3.connect(DB) as conn:

        cursor = conn.cursor()    

        """Executes a SQL SELECT statement and returns the results of running the SELECT. Make sure you have a full SQL SELECT query created before calling this function."""
        print(f"Executing SQL statement: {sql_statement}")
        cursor.execute(sql_statement)
        records = cursor.fetchall()

        if not records:
            return "No results found."
        
        column_names = [description[0] for description in cursor.description]
        col_widths = [len(name) for name in column_names]
        for row in records:
            for i, value in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(value)))
        
        result_str = ""
        
        header = " | ".join(name.ljust(width) for name, width in zip(column_names, col_widths))
        result_str += header + "\n"
        result_str += "-" * len(header) + "\n"
        
        for row in records:
            row_str = " | ".join(str(value).ljust(width) for value, width in zip(row, col_widths))
            result_str += row_str + "\n"
        
        return result_str          