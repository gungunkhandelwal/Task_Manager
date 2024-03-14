# app.py
# from view import add_todo,display_todo,update_todo
# import json

# Display all ToDo List
# @app.route('/')
# def Task():
#     task=tsk.query.all()
#     return render_template('task.html',tasks=task)

# @app.route('/listOne',methods=['GET','POST'])
# def listOne():
#     if request.method == 'POST':
#         data=display_todo(request.form.get('title'))
#         if data == 'None':
#             return render_template('listOne.html',data=None)
#         return render_template('listOne.html',data=data)
#     return render_template('listOne.html',data=None)


# Add Task
# @app.route('/add_task', methods=['GET', 'POST'])
# def addTask():
#     if request.method == 'POST':
#         print(100*'-')
#         title = request.form.get('title')
#         description = request.form.get('description')
#         userId = request.form.get('userId')

#         # # Add validation to ensure title is a string
#         # if not isinstance(title, str):
#         #     return "Error: Title must be a string"

#         result = add_todo(title=title, description=description, userId=userId)
#         if result:
#             print("Result",result)
#             data = display_todo(title)
#             print("Data",data)
#             return render_template('listOne.html', data=data)
#         else:
#             return render_template('add_task.html')
#     else:
#         return render_template('add_task.html')



# # Update Task
# @app.route('/update_task')
# def updateTask():
#     # data=display_todo(title="Eat")
#     return render_template('listOne.html')

# # Delete Task
# @app.route('/delete_task')
# def deleteTask():
#     return render_template('deleteTask.html')


# View.py

# from schemas import schema
# from db import Task,session

# # def add_todo(title, description, userId):
# #     variables = {
# #         "title": title,
# #         "description": description,
# #         "userId": userId
# #     }

# #     try:
# #         schema.execute("mutation{" +
# # 	               f'mutateTask(title: "{title}", description: "{description}", userId: "{userId}")' +
# # 		           "{task{title description user{ id username } createdAt}}}", variables=variables)
# #         return True
# #     except Exception as e:
# #         return e

# # def add_todo(title,description,userId):
# #     try:
# #         schema.execute("mutation {"+
# #                        f'createTodo(title:"{title}",description:"{description}",userId:{userId})' +
# #                        "task{title description userId  createdAt }}}")
# #         return True
# #     except Exception as e:
# #         return e
    
# def add_todo(title, description, userId):
#     mutation_str = f"""
#        mutation createTask($taskData: TaskInput!) {{
#            createTodo(taskData: $taskData) {{
#                todo {{
#                    title
#                    description
#                    user {{
#                      id
#                      username
#                    }}
#                    createdAt
#                }}
#            }}
#        }}
#     """

#     try:
#         schema.execute(
#             mutation_str,
#             variable_values={"taskData": {"title": title, "description": description, "userId": userId}}
#         )
#         return True
#     except Exception as e:
#         return e


# def display_todo(title):
#     mutation_str=f""" 
#        query{{
#        todo(title:"{title}"){{
#              title,
#              description,
#              createdAt
#        }}
#        }}
#     """
#     try:
#         result=schema.execute(mutation_str)

#         task_data=result.data.get('todo')
#         print("task_data---", task_data)
#         if task_data:
#             return {
#                 'title': task_data.get('title'),
#                 'description': task_data.get('description'),
#                 'createdAt': task_data.get('createdAt')
#             }
#         else:
#             return 'error'
    
#     except Exception as e:
#         return e
    

# def update_todo(title,description):
#     mutation_str=f"""
#       mutation{{
#       mutateUpdateTask(title:"{title}",description:"{description}"){{
#       task{{
#       title
#       description
#       createdAt
#     }}
    
#   }}
# }}
#     """
#     try:
#         schema.execute(mutation_str)
#         return True
#     except Exception as e:
#         return e


# from schemas import schema

# def show_todo():
#     try:
#         # Perform a GraphQL query to fetch all tasks
#         result = schema.execute('''
#             query {
#                 allTask {
#                     id
#                     title
#                     description
#                     createdAt
#                 }
#             }
#         ''')

#         # Check if the query was successful
#         if result.errors:
#             # Handle errors if any
#             return None
#         else:
#             # Return the fetched data
#             return result.data

#     except Exception as e:
#         # Handle exceptions
#         return None


# schema.py

# import graphene
# from graphene import relay
# from sqlalchemy.orm import sessionmaker
# from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
# from db import (
#     User as UserDB,
#     Task as TaskDB,
#     session,
#     engine
# )
# import datetime

# # Show user schema
# class UserSchema(SQLAlchemyObjectType):
#     class Meta:
#         model = UserDB
#         interfaces = (relay.Node, )

# # Show task schema
# class TaskSchema(SQLAlchemyObjectType):
#     class Meta:
#         model = TaskDB
#         interfaces = (relay.Node, )

# # Query for schema
# class Query(graphene.ObjectType):
#     node = relay.Node.Field()
#     all_task = SQLAlchemyConnectionField(TaskSchema)
#     all_user = SQLAlchemyConnectionField(UserSchema)
#     todo = graphene.Field(TaskSchema, title=graphene.String())

#     def resolve_all_tasks(parent, info):
#         tasks = TaskDB.query.all()
#         return tasks

#     def resolve_todo(self, info, title):
#         todo = TaskDB.query.filter_by(title=title).first()
#         return todo
    
#     todos = graphene.List(TaskSchema)

#     def resolve_todos(self, info):
#         todos = TaskDB.query.filter_by(user_id=info.context.get('user_id')).all()
#         return todos

# # User mutation
# class UserMutation(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         email = graphene.String(required=True)

#     user = graphene.Field(lambda: UserSchema)

#     def mutate(self, info, username, email):
#         user = UserDB(
#             username=username,
#             email=email
#         )

#         session.add(user)
#         session.commit()

#         return UserMutation(user=user)
    

# # Task mutation
# class TaskMutation(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.Int()
#         title = graphene.String(required=True)
#         description = graphene.String(required=True)

#     task = graphene.Field(lambda: TaskSchema)

#     def mutate(self, info, user_id, title, description):
#         user = UserDB.query.get(user_id)

#         created_at = datetime.datetime.utcnow()

#         new_task = TaskDB(
#             title=title,
#             description=description,
#             user=user,
#             created_at=created_at,
#         )

#         session.add(new_task)
#         session.commit()

#         return TaskMutation(task=new_task)
    
# class TaskInput(graphene.InputObjectType):
#     title = graphene.String(required=True)
#     description = graphene.String(required=True)
#     user_id = graphene.Int(required=True)

# class CreateTodo(graphene.Mutation):
#     class Arguments:
#         task_data = TaskInput(required=True)

#     todo = graphene.Field(TaskSchema)

#     def mutate(self, info, task_data=None):
#         title = task_data.title
#         description = task_data.description
#         user_id = task_data.user_id
        
#         new_task = TaskDB(
#             title=title,
#             description=description,
#             user_id=user_id
#         )
#         session.add(new_task)
#         session.commit()
        
#         return CreateTodo(todo=new_task)

    

# class UpdateTask(graphene.Mutation):
#     class Arguments:
#         title = graphene.String(required=True)
#         description = graphene.String(required=True)

#     task = graphene.Field(lambda: TaskSchema)

#     def mutate(self, info, title, description=None, created_at=None):
#         todo = TaskDB.query.filter_by(title=title).first()

#         if not todo:
#             raise Exception(f"ToDo item with title '{title}' not found")
    
#         if description is not None:
#             todo.description = description
#         if created_at is not None:
#             todo.created_at = created_at

#         session.commit()

#         return UpdateTask(task=todo)
    
# class DeleteTask(graphene.Mutation):
#     class Arguments:
#         title = graphene.String(required=True)

#     success = graphene.Boolean()

#     def mutate(self, info, title):
#         todo = TaskDB.query.filter_by(title=title).first()

#         if not todo:
#             raise Exception(f"ToDo item with title '{title}' not found")
        
#         session.delete(todo)
#         session.commit()

#         return DeleteTask(success=True)
    


# # Mention User and Task
# class Mutation(graphene.ObjectType):
#     mutate_user = UserMutation.Field()
#     # mutate_task = TaskMutation.Field()
#     mutate_update_task = UpdateTask.Field()
#     # mutate_task = CreateTodo.Field()
#     mutate_delete_task = DeleteTask.Field()

# schema = graphene.Schema(query=Query, mutation=Mutation)


# '''
# mutation{
#   mutateUpdateTask(title:"Dancing",description:"Zumba Practice"){
#     task{
#       title
#       description
#       createdAt
#     }
    
#   }
# }  
# '''

# '''
# mutation{
#   mutateDeleteTask(title:""){
#     success
#   }
# }
# '''