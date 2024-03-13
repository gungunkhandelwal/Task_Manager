from flask import Flask,render_template,request,redirect
from flask_graphql import GraphQLView
from schemas import schema
from graphene import Schema
from schemas import Mutation
from db import Task as tsk,session
from view import add_todo,display_todo
# import json
from sqlalchemy.orm import scoped_session


app=Flask(__name__)
schema=Schema(mutation=Mutation)
scoped_db_session = scoped_session(session)

# Display all ToDo List
@app.route('/')
def Task():
    task=tsk.query.all()
    return render_template('task.html',tasks=task)

@app.route('/listOne',methods=['GET','POST'])
def listOne():
    if request.method == 'POST':
        data=display_todo(request.form.get('title'))
        if data == 'None':
            return render_template('listOne.html',data=None)
        return render_template('listOne.html',data=data)
    return render_template('listOne.html',data=None)


# Add Task
@app.route('/add_task', methods=['GET', 'POST'])
def addTask():
    if request.method == 'POST':
        print(100*'-')
        title = request.form.get('title')
        description = request.form.get('description')
        userId = request.form.get('userId')

        # # Add validation to ensure title is a string
        # if not isinstance(title, str):
        #     return "Error: Title must be a string"

        result = add_todo(title=title, description=description, userId=userId)
        if result:
            print("Result",result)
            data = display_todo(title)
            print("Data",data)
            return render_template('listOne.html', data=data)
        else:
            return render_template('add_task.html')
    else:
        return render_template('add_task.html')



# Update Task
# @app.route('/update_task')
# def updateTask():
#     data=display_todo(title="Eat")
#     return render_template('listOne.html',data=data)

# Delete Task
@app.route('/delete_task')
def deleteTask():
    return render_template('deleteTask.html')



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
    scoped_db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)