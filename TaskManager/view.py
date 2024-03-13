from schemas import schema
from db import Task,session

# def add_todo(title,description,userId):
#     mutation_str= f"""
#        mutation {{
#            mutateTask(
#                title: "{title}",
#                description: "{description}",
#                userId:{userId}
#            ) {{
#                task {{
#                    title
#                    description
#                    user{{
#                      id
#                      username
#                    }}
#                    createdAt
#                }}
#            }}
#        }}
#     """

#     try:

#         schema.execute(mutation_str)
#         return True
        

#     except Exception as e:
#         return e

def add_todo(title, description, userId):
    variables = {
        "title": title,
        "description": description,
        "userId": userId
    }

    try:
        schema.execute("mutation{" +
	               f'mutateTask(title: "{title}", description: "{description}", userId: "{userId}")' +
		           "{task{title description user{ id username } createdAt}}}", variables=variables)
        return True
    except Exception as e:
        return e

# def add_todo(title,description,userId):
#     try:
#         schema.execute("mutation {"+
#                        f'createTodo(title:"{title}",description:"{description}",userId:{userId})' +
#                        "task{title description userId  createdAt }}}")
#         return True
#     except Exception as e:
#         return e
    

def display_todo(title):
    mutation_str=f""" 
       query{{
       todo(title:"{title}"){{
             title,
             description,
             createdAt
       }}
       }}
    """
    try:
        result=schema.execute(mutation_str)

        task_data=result.data.get('todo')
        print("task_data---", task_data)
        if task_data:
            return {
                'title': task_data.get('title'),
                'description': task_data.get('description'),
                'createdAt': task_data.get('createdAt')
            }
        else:
            return 'error'
    
    except Exception as e:
        return e
    