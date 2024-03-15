import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from db import (
    User as UserDB,
    Task as TaskDB,
    session,
)
import datetime

# Show user schema from user table in database
class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserDB
        interfaces = (relay.Node, )

# Show task schema from tasks table in database
class TaskSchema(SQLAlchemyObjectType):
    class Meta:
        model = TaskDB
        interfaces = (relay.Node, )

# Query for schema user and task
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_task = SQLAlchemyConnectionField(TaskSchema)
    all_user = SQLAlchemyConnectionField(UserSchema)



# This class is used to add user details in database
class UserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info, username, email):
        user = UserDB(
            username=username,
            email=email
        )

        session.add(user)
        session.commit()

        return UserMutation(user=user)
    

# This class is used to add task details in database
class TaskMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    success=graphene.Boolean()
    task = graphene.Field(TaskSchema)

    def mutate(self, info, user_id, title, description):
        user = UserDB.query.get(user_id)

        created_at = datetime.datetime.utcnow()

        new_task = TaskDB(
            title=title,
            description=description,
            user=user,
            created_at=created_at,
        )

        session.add(new_task)
        session.commit()

        return TaskMutation(success=True,task=new_task)
    

# This class is used to update task from given task detail
class UpdateTask(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        new_title = graphene.String()
        new_description = graphene.String()
        new_created_at = graphene.DateTime()

    task = graphene.Field(TaskSchema)

    def mutate(self, info, id, new_title=None, new_description=None, new_created_at=None):
        todo = TaskDB.query.filter_by(id=id).first()

        if not todo:
            raise Exception(f"ToDo item with title '{id}' not found")
        
        if new_title is not None:
            todo.title = new_title
        if new_description is not None:
            todo.description = new_description
        if new_created_at is not None:
            todo.created_at = new_created_at

        session.commit()

        return UpdateTask(task=todo)

    
# This class is used to delete task from given task by its id
class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        todo = TaskDB.query.filter_by(id=id).first()

        if not todo:
            raise Exception(f"ToDo item with title '{id}' not found")
        
        session.delete(todo)
        session.commit()

        return DeleteTask(success=True)
    


# This class describe all classes above 
class Mutation(graphene.ObjectType):
    mutate_user = UserMutation.Field()
    mutate_task = TaskMutation.Field()
    mutate_update_task = UpdateTask.Field()
    mutate_delete_task = DeleteTask.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)