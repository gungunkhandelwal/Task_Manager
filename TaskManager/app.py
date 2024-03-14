from flask import Flask,render_template,request,redirect
from flask_graphql import GraphQLView
from schemas import schema
from graphene import Schema
from schemas import Mutation
from db import Task as tsk,session
from view import display_todo,add_todo,update_todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import json

app=Flask(__name__,static_folder='static')
# schema=Schema(mutation=Mutation)
connection_str = "sqlite:///tasks.db"
engine = create_engine(connection_str, echo=True)

Session = sessionmaker(bind=engine)

# Create a scoped session
db_session = scoped_session(Session)

# Display all task
@app.route('/')
def index():
    tasks=tsk.query.all()
    return render_template('task.html',tasks=tasks)


# Add Task to DataBase
@app.route('/add_task',methods=['GET','POST'])
def addTask():
    if request.method == 'POST':
        title=request.form.get('title')
        description=request.form.get('description')
        userId=request.form.get('userId')
        result=add_todo(title=title,description=description,userId=userId)
        return redirect('/')
    else:
        return render_template('add_task.html')

@app.route('/update_task')
def UpdateTask():
    return render_template('update_task.html')

@app.route('/delete_task/<int:id>')
def deleteTask():
    return render_template('delete_task.html')



# For graphql
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remove the session from the scoped session
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)