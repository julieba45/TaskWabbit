from flask import Blueprint, jsonify, session, request
from app.models import Task, User
from app.models import User, db
from app.forms import CreateTaskForm
from datetime import datetime, timedelta
from sqlalchemy import and_
from .auth_routes import validation_errors_to_error_messages
from flask_login import login_required, current_user

task_routes = Blueprint('tasks', __name__)

@task_routes.route('/', methods=['POST'])
@login_required                       #for testing purposes
def create_task():
    form = CreateTaskForm()
    # print('DATA', form.data)
    form['csrf_token'].data = request.cookies['csrf_token']


    if form.validate_on_submit():
        task_date = form.data['task_date']

        tasker_id = form.data['tasker_id']
        # count tasks assigned to a specific tasker on a specific date
        tasks = Task.query.filter(
            and_(
                Task.tasker_id == tasker_id
            )
        ).count()
        print('TASKS', tasks)

        #check validations: removing validation to later be implemented
        # if tasks >= 8:
        #     return {'errors': 'Tasker has reached maximum limit of tasks for the day'}, 400

        #make sure timezone aligns
        time_diff_minutes = int(request.json.get('timeDiff', 0))
        adjusted_current_date = datetime.now() - timedelta(minutes=time_diff_minutes)
        adjusted_current_date = adjusted_current_date.date()


        if task_date < adjusted_current_date:
            return {'errors': ['Cannot schedule task in the past']}, 400

        # Create the task
        task = Task(
            taskTypeId=form.data['taskTypeId'],
            title=form.data['title'],
            description=form.data['description'],
            totalPrice=form.data['totalPrice'],
            location=form.data['location'],
            task_date=task_date,
            user_id=current_user.id,
            tasker_id=tasker_id,
        )
        print(current_user.id)
        db.session.add(task)
        db.session.commit()
        return task.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@task_routes.route('/<int:taskId>', methods=['PUT'])
@login_required
def update_task(taskId):
    form = CreateTaskForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    task = Task.query.get(taskId)
    # print('HEY TASK', vars(task))

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    if form.validate_on_submit():
        task_date = form.data['task_date']
        tasker_id = form.data['tasker_id']

        # count tasks assigned to a specific tasker on a specific date
        tasks = Task.query.filter(
            and_(
                Task.tasker_id == tasker_id,
                # Task.task_date == task_date.date()
            )
        ).count()

        # check validations
        # if tasks >= 8:
        #     return {'errors': 'Tasker has reached maximum limit of tasks for the day'}, 400
        if task_date < datetime.now().date():
            return {'errors': ['Cannot schedule task in the past']}, 400

        # Update the task
        if 'taskTypeId' in form.data:
            task.taskTypeId = form.data['taskTypeId']
        if 'title' in form.data:
            task.title = form.data['title']
        if 'description' in form.data:
            task.description = form.data['description']
        if 'totalPrice' in form.data:
            task.totalPrice = form.data['totalPrice']
        if 'location' in form.data:
            task.location = form.data['location']
        if 'task_date' in form.data:
            task.task_date = task_date
        if 'tasker_id' in form.data:
            task.tasker_id = tasker_id
        db.session.commit()

        return task.to_dict()

    return {'errors': validation_errors_to_error_messages(form.errors)}, 400

@task_routes.route('/current', methods=['GET'])
@login_required
def get_current_task():
    '''
    Query for all tasks of current user and return them in a list of dictionaries
    '''
    current_user_id = current_user.get_id()
    # print('CURRENT USERID', current_user_id)
    user = User.query.get(current_user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify(user.to_dict_with_tasks())


@task_routes.route('/<int:taskId>', methods=['GET'])
@login_required
def get_task(taskId):
    '''
    Query for a specific task and return is as a dictionary
    '''

    task = Task.query.get(taskId)
    if task is None:
        return jsonify({'error: Task not found'}), 404
    else:
        return jsonify(task.to_dict())


@task_routes.route('/<int:taskId>', methods=['DELETE'])
@login_required
def delete_task(taskId):
    '''
    Deletes a specific task
    '''
    task = Task.query.get(taskId)
    if task is None:
        return jsonify({'error':'Task not found'}), 404
    #check if the current user is the owner of the task
    if task.user_id != current_user.id:
        return jsonify({'error':'Unauthorized'}), 404
    db.session.delete(task)
    db.session.commit()

    return jsonify({'messahe': 'Task successfully deleted'})
