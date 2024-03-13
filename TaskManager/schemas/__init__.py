import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from db import(
    User as UserDB,
    Task as TaskDB,
    session
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
    # Allows sorting over multiple columns, by default over the primary key
    all_task = SQLAlchemyConnectionField(TaskSchema.connection)
    # Disable sorting over this field
    all_User = SQLAlchemyConnectionField(UserSchema.connection)


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

    task = graphene.Field(lambda: TaskSchema)

    def mutate(self, info, user_id, title, description):

        users= session.query(UserDB).filter_by(id=user_id).first()

        created_at = datetime.datetime.utcnow()

        new_task = TaskDB(
            title=title,
            description=description,
            user=users,
            created_at=created_at,
        )

        session.add(new_task)
        session.commit()

        return TaskMutation(task=new_task)


class UpdateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    task=graphene.Field(lambda:TaskSchema)

    def mutate(self,info,title,description=None,created_at=None):
        # users= session.query(UserDB).filter_by(id=user_id).first()
        todo = TaskDB.query.filter_by(title=title).first()

        created_at = datetime.datetime.utcnow()

        if not todo:
            raise Exception(f"ToDo item with title '{title}' not found")
    
        
        # Update the fields if provided
        if description is not None:
            todo.description = description
        if created_at is not None:
            todo.created_at = created_at

        session.commit()

        return UpdateTask(task=todo)
    
class DeleteTask(graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)

    # task=graphene.Field(lambda:TaskSchema)
    success = graphene.Boolean()

    def mutate(self,info,title):
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
    mutate_update_task=UpdateTask.Field()
    mutate_delete_task=DeleteTask.Field()



schema = graphene.Schema(query=Query,mutation=Mutation)