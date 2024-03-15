from schemas import schema
from graphql import GraphQLError

def display_todo():
    query="""{
    allTask{
    edges{
    nodes{
    title,
    description,
    createdAt,
    userId
    }
    }
    }
    }"""
    result=schema.execute(query)
    print(result)
    if result:
        print("Working")
    else:
        print("It show an error")


def add_todo(title,description,userId):
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
        print(result)
        return result
    except Exception as e:
        return e
    

def update_todo(id, new_title, new_description, new_created_at):
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
        print(result)
        if result.errors:
            raise GraphQLError(str(result.errors[0]))

        return result.data

    except GraphQLError as e:
        return str(e)
