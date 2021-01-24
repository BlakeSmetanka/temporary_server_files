from flask import Flask, request, redirect, render_template, url_for, jsonify
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_sqlalchemy import SQLAlchemy
from Logic import pageLoader
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://flaskr/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Added to suppress a warning
app.config['FLASK_DEBUG'] = 1
app.config['JSON_ADD_STATUS'] = False # Without this I kept getting KeyErrors
db = SQLAlchemy(app)

VALID_CAMPUSES = ["Daytona Beach", "Cocoa", "Sanford-Lake Mary", "Lake Nona", "Downtown", "Rosen"]

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id # Will return the word Task followed by the ID

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/tasks')
        except:
            return "There was an issue adding a task to the database."

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks)

# Returns JSON data of a task object.
@app.route('/tasksjson/<search>', methods=['GET'])
def taskJSON(search):
    try:
        task = Todo.query.filter(Todo.content.contains(search, autoescape=True)).first()
        return json_response(id=task.id, content = task.content, date_created=task.date_created)
    except:
        return "There was an error retrieving the search result."
    # task = Todo.query.filter(Todo.content.like('%'+search+'%')).first()
    # task = Todo.query.filter(Todo.content.endswith(search, autoescape=True)).first()

@app.route('/deleteTask/<int:id>')
def deleteTask(id):

    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/tasks')
    except:
        return 'There was a problem deleting that task.'

@app.route('/updateTask/<int:id>', methods=['GET','POST'])
def updateTask(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/tasks')
        except:
            return 'There was an issue updating your task.'

    else:
        return render_template('update.html', task=task)

# Dynamic URL example
# Note that a varible defaults to string. Can be cast with syntax <int:varName>
@app.route('/example/<URLPassedToFunction>')
def dynamicURLExample(URLPassedToFunction):
    return "Your URL ends with /" + URLPassedToFunction

# POST example with headers.
# Will display username and password sent in headers.
@app.route('/sneakybackchannel', methods=['POST'])
def postExample():
    return "I know this defeats the purpose, but here is your username and password: \n" + request.headers['username'] + "\n" + request.headers['password']

@app.route('/m/landing')
def landing():
    landing_page_final = pageLoader.landing_page
    campus_names = landing_page_final["content"][1]["content"][1]["items"][0]
    campus_names["optionLabels"] = VALID_CAMPUSES
    campus_names["optionValues"] = list(map(str, list(range(1, len(VALID_CAMPUSES) + 1))))
    print("landing")
    return landing_page_final

@app.route('/m/contact')
def contact():
    contact_page_final = pageLoader.contact_page

    campus_name = contact_page_final["content"][1]
    campus_name["title"] = "Downtown Campus"

    contact_items = contact_page_final["content"][2]["items"]
    contact_items[0]["title"] = "(123)-456-7890"
    contact_items[1]["title"] = "111 ThePantry St."

    map_points = contact_page_final["content"][3]["content"][0]["staticPlacemarks"][0]["point"]
    map_points["latitude"] = 28.547870
    map_points["longitude"] = -81.388070

    return contact_page_final

@app.route('/m/about')
def about():
    about_page_final = pageLoader.about_page

    about_text = about_page_final["content"][2]["items"][0]
    about_text["title"] = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "\
                    "Aenean commodo ligula eget dolor. Aenean massa. Cum sociis "\
                    "natoque penatibus et magnis dis parturient montes, nascetur "\
                    "ridiculus mus. Donec quam felis, ultricies nec, pellentesque "\
                    "eu, pretium quis, sem. Nulla consequat massa quis enim."

    campus_names = about_page_final["content"][3]["items"][0]
    campus_names["optionLabels"] = VALID_CAMPUSES
    campus_names["optionValues"] = list(map(str, list(range(1, len(VALID_CAMPUSES) + 1))))

    return about_page_final

@app.route('/m/reservations', methods=['POST', 'GET'])
def reservations():
    reserve_page_final = pageLoader.reservation_page

    #about_text = about_page_final["content"][2]["items"][0]
    #about_text["title"] = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "\
    #                "Aenean commodo ligula eget dolor. Aenean massa. Cum sociis "\
    #                "natoque penatibus et magnis dis parturient montes, nascetur "\
    #                "ridiculus mus. Donec quam felis, ultricies nec, pellentesque "\
    #                "eu, pretium quis, sem. Nulla consequat massa quis enim."

    #campus_names = about_page_final["content"][3]["items"][0]
    #campus_names["optionLabels"] = VALID_CAMPUSES
    #campus_names["optionValues"] = list(map(str, list(range(1, len(VALID_CAMPUSES) + 1))))
    if request.method == 'POST':
        print("HIT POST")
        print(request.form.to_dict())

        return reserve_page_final

        '''
        payload = {
            "metadata": {
                "version": "1",
                "redirectLink": {
                    "relativePath": "./m/reservations"
                }
            }
        }

        return json.dumps(payload)
        '''
    else:
        print("HIT GET")
        print(request.__dict__.items())
        return reserve_page_final

# GET query example. Make a request to the homepage followed by ?name=yourname
#@app.route('/')
#def index():
#    name = request.args.get('name', '')
#    return 'Hello, ' + name + "!" # http://127.0.0.1:5000/?name=blake

# This makes it so when you do python app.py, it runs in debug mode.
# Code changes will automatically restart the server in debug mode.
# A nice error page will display in web browser with this active.
# THIS HAS TO BE LAST IN THE DOCUMENT
if __name__ == "__main__":
    app.run(debug=True)
