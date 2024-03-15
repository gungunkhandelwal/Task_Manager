from flask import Flask,render_template,request,redirect
from flask_graphql import GraphQLView
from schemas import schema
from db import Task as tsk,session
from view import add_todo,update_todo,delete_todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import json

app=Flask(__name__,static_folder='static')
connection_str = "sqlite:///tasks.db"
engine = create_engine(connection_str, echo=True)

Session = sessionmaker(bind=engine)

# Create a scoped session
db_session = scoped_session(Session)

# This Function is used to display task from database
@app.route('/')
def index():
    tasks=tsk.query.all()
    return render_template('task.html',tasks=tasks)


@app.route('/add_task',methods=['GET','POST'])
# This Function is used to add task to datatbase
def addTask():
    if request.method == 'POST':
        title=request.form.get('title')
        description=request.form.get('description')
        userId=request.form.get('userId')
        result=add_todo(title=title,description=description,userId=userId)
        return redirect('/')
    else:
        return render_template('add_task.html')

from datetime import datetime


@app.route('/update_task/<int:myid>',methods=['GET','POST'])
# This Function is used to update task to datatbase by their
def UpdateTask(myid):
        if request.method =='POST':
            new_title=request.form.get('new_title')
            new_description=request.form.get('new_description')
            new_created_at=datetime.utcnow()
            result=update_todo(id=myid,new_title=new_title,new_description=new_description,new_created_at=new_created_at)
            print(result)
            return redirect('/')
        else:
            return render_template('update_task.html',myid=myid)
        
@app.route('/delete_task/<int:myid>',methods=['GET','POST'])
# This Function is used to delete task from datatbase by their id
def deleteTask(myid):
    delete_todo(id=myid)
    return redirect('/')

@app.route('/single_task/<int:myid>')
# This Function is used to display single task by their id
def singleTask(myid):
    tasks=tsk.query.filter_by(id=myid).first()
    return render_template('single_task.html',tasks =tasks)

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