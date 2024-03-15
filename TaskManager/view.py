from schemas import schema
from graphql import GraphQLError

def add_todo(title,description,userId):
    # This Function is used to executes Task Mutation from schema.py
    try:
        result=schema.execute(f"""
                mutation{{
                   mutateTask(title:"{title}",description:"{description}",userId:{userId}){{
                    task{{
                        id title description  createdAt  userId
                    }}
                }}
           }}
        """)
        return result
    except Exception as e:
        return e
    

def update_todo(id, new_title, new_description, new_created_at):
    # This Function is used to executes Update Task Mutation from schema.py
    try:
        mutation_str = """
            mutation ($id: Int!, $newTitle: String!, $newDescription: String!, $newCreatedAt: DateTime!) {
                mutateUpdateTask(
                    id: $id,
                    newTitle: $newTitle,
                    newDescription: $newDescription,
                    newCreatedAt: $newCreatedAt
                ) {
                    task {
                        id
                        title
                        description
                        createdAt
                        userId
                    }
                }
            }
        """
        variables = {
            "id": id,
            "newTitle": new_title,
            "newDescription": new_description,
            "newCreatedAt": new_created_at
        }

        result = schema.execute(mutation_str, variables=variables)
        if result.errors:
            raise GraphQLError(str(result.errors[0]))

        return result.data

    except GraphQLError as e:
        return str(e)

def delete_todo(id):
    # This Function is used to executes deleter task mutation from schema.py
    try:
        mutation_str = """
            mutation ($id: Int!) {
                mutateDeleteTask(
                    id: $id,
                ) {
                   success
                }
            }
        """
        variables = {
            "id": id,
        }

        result = schema.execute(mutation_str, variables=variables)
        if result.errors:
            raise GraphQLError(str(result.errors[0]))

        return result.data

    except GraphQLError as e:
        return str(e)
