import graphene
from graphene import relay
from sqlalchemy.orm import sessionmaker
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from db import (
    User as UserDB,
    Task as TaskDB,
    session,
    engine
)
import datetime

# Show user schema
class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserDB
        interfaces = (relay.Node, )

# Show task schema
class TaskSchema(SQLAlchemyObjectType):
    class Meta:
        model = TaskDB
        interfaces = (relay.Node, )

# Query for schema
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_task = SQLAlchemyConnectionField(TaskSchema)
    all_user = SQLAlchemyConnectionField(UserSchema)

    def resolve_all_tasks(self, info):
        return TaskDB.query.all()

# User mutation
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
    

# Task mutation
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
    

class UpdateTask(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        new_title = graphene.String()
        new_description = graphene.String()
        new_created_at = graphene.DateTime()

    task = graphene.Field(TaskSchema)

    def mutate(self, info, id, new_title=None, new_description=None, new_created_at=None):
        todo = TaskDB.query.filter_by(id=id).first()
        print(todo)

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

    
class DeleteTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, title):
        todo = TaskDB.query.filter_by(title=title).first()

        if not todo:
            raise Exception(f"ToDo item with title '{title}' not found")
        
        session.delete(todo)
        session.commit()

        return DeleteTask(success=True)
    


# Mention User and Task
class Mutation(graphene.ObjectType):
    mutate_user = UserMutation.Field()
    mutate_task = TaskMutation.Field()
    mutate_update_task = UpdateTask.Field()
    # mutate_task = CreateTodo.Field()
    mutate_delete_task = DeleteTask.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)