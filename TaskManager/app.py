from flask import Flask,render_template,jsonify,request,redirect
from flask_graphql import GraphQLView
from schemas import schema
from graphene import Schema
from schemas import Mutation
from db import Task as tsk,session
from view import add_todo
import json
from sqlalchemy.orm import scoped_session


app=Flask(__name__)
schema=Schema(mutation=Mutation)
scoped_db_session = scoped_session(session)


@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remove the session from the scoped session
    scoped_db_session.remove()

# Display all ToDo List
@app.route('/')
def Task():
    task=tsk.query.all()
    print(task)
    return render_template('task.html',tasks=task)


# Add task 
# @app.route('/add_task',methods=['GET','POST'])
# def addTask():
#     if request.method == 'POST':
#         title = request.form.get('title')
#         description = request.form.get('description')
#         created_at = request.form.get('created_at')

#         result = add_todo(title, description, created_at)
#         # if result:
#         #     display_todo(result)
#         return render_template('task.html', result=result)
#         # else:
#         #     return render_template('add_task.html')
#     else:
#         return jsonify({'error': "Failed to add task"})


# For graphql
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(debug=True)