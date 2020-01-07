from flask import Flask,jsonify,abort,make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)
auth = HTTPBasicAuth()

tasks = [
    {
        'id': 1,
        'title': u'buy groceries',
        'description': u'Milk, Sugar, Malt, Fruits, Pizza',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn DialogFlow',
        'description': u'Need to Download a good dialogflow tutorial on the Web',
        'done': False
    }

]

#gets the list of tasks
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    x = list(map(make_public_task, tasks))
    #return jsonify( { 'tasks': map(make_public_task, tasks) } )
    return jsonify( {'tasks': x})
    

#gets a  singular task resource
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = next(filter(lambda t: t['id'] == task_id, tasks), None)
    return jsonify( { 'task': task } ), 200 if task else 404



#a func to crate a new task
@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    r = request.get_json()
    task = {
        "id": r['id'],
        'title': r['title'],
        'description': r.get('description'),
        'done': False
    }
    tasks.append(task)
    return jsonify( {'task': task }), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    r = request.get_json()
    task = next(filter(lambda t: t['id'] == task_id, tasks), None)

    if task is None:

        task = {
            "id": r['id'],
            'title': r['title'],
            'description': r.get('description'),
            'done': False
        }
        tasks.append(task)

    else:
        task.update(r)

    return jsonify(task)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = list(filter(lambda x: x['id'] != task_id, tasks))
    return {"message": "item Deleted"}



def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)

        else:
            new_task[field] = task[field]
    return new_task




@auth.get_password
def get_password(username):
    if username == "mike":
        return "python"
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access' }), 403)


if __name__ ==  '__main__':
    app.run(debug = True)

