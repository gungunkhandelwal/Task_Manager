from schemas import schema
from db import Task,session

def add_todo(title,description,created_at):
    mutation_str=f"""
       mutation{{
       mutateTask(
       title:"{{title}}",
       descrption:"{{description}}",
       created:"{{created_at}}"
       )
       }}
    """

    try:
        schema.execute(mutation_str)
        return True

    except Exception as e:
        return e
    