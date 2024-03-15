from flask import Flask,render_template,request,redirect,url_for
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID
from flask_wtf.csrf import CSRFProtect
from flask_graphql import GraphQLView
from schemas import schema
from db import Task as tsk
from view import add_todo,update_todo,delete_todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import logging

app=Flask(__name__,static_folder='static')
connection_str = "sqlite:///tasks.db"
engine = create_engine(connection_str, echo=True)

logging.basicConfig(level=logging.DEBUG)

# Configuring the app with keycloak credentials
app.config.update({
	'SECRET_KEY': 'Ok7uZIKeAPSSUd3pPfRy98bYYkKNccF5', 
	'TESTING': True,
	'DEBUG': True,
	'OIDC_CLIENT_SECRETS': 'clients_secrets.json',
	'OIDC_ID_TOKEN_COOKIE_SECURE': False,
	'OIDC_USER_INFO_ENABLED': True,
	'OIDC_OPENID_REALM': 'task',
	'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

# Connect app from OpenIdConnet
oidc = OpenIDConnect(app)
# Csrf token
csrf = CSRFProtect(app) 

# Define Keycloak
keycloak_openid = KeycloakOpenID(server_url="http://127.0.0.1:8080/", client_id="task",
                                 realm_name="Task_Manager", client_secret_key='Ok7uZIKeAPSSUd3pPfRy98bYYkKNccF5') 

Session = sessionmaker(bind=engine)

# Create a scoped session
db_session = scoped_session(Session)

# This Function is used to display task from database
@app.route('/')
def index():
    tasks=tsk.query.all()
    return render_template('task.html',tasks=tasks)


@app.route('/single_task/<int:myid>')
# This Function is used to display single task by their id
def singleTask(myid):
    tasks=tsk.query.filter_by(id=myid).first()
    return render_template('single_task.html',tasks =tasks)

@app.route('/add_task',methods=['GET','POST'])
# This Function is used to add task to datatbase
def addTask():
    if oidc.user_loggedin == 'True':
        if request.method == 'POST':
            title=request.form.get('title')
            description=request.form.get('description')
            userId=request.form.get('userId')
            add_todo(title=title,description=description,userId=userId)
            return redirect('/')
    else:
         return render_template('add_task.html')


from datetime import datetime


@app.route('/update_task/<int:myid>',methods=['GET','POST'])
# This Function is used to update task to datatbase by their
def UpdateTask(myid):
    if oidc.user_loggedin == 'True':
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

@app.route('/login')
@oidc.require_login
# Login using keycloak
def login():
    result=oidc.redirect_to_auth_server()
    return redirect(url_for('task'))


@app.route('/logout')
# Logout function
def logout():
	oidc.logout()
	return redirect('/')


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