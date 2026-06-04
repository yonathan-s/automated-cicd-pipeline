# This file defines the API that the pipeline deploys 
# It exposes a health endpoint used by ECS and Github actions 
# And it exposes CRUD endpoints for managing tasks


from flask import Flask, request, jsonify, render_template
# request reads incoming user data
# jsonify converts python objects into JSON
# render_template loads HTML page
from flask_cors import CORS
# CORS allows frontend apps to communicate with API across domains
# CORS controls which domains can access the API from browsers
from datetime import datetime
import uuid
# uuid creates unique task IDs
import logging
# logging records activity
import os
# os reads environment variables
from config import config
# imports settings from config.py

app = Flask(__name__) # Creates flask object


env = os.getenv('FLASK_ENV', 'development') 
# Looks for production environment confirmation, if not it will default to devlopment environment
app.config.from_object(config[env])
# Sets the configurations based on the environment

CORS(app, origins=app.config['CORS_ORIGINS']) #allows browser requests only from approved origins (in this case all origins)


# congigures timestamp, module, level and message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# These logs are collected by Cloudwatch through ECS log configuration


tasks = [] # In-memory storage, stores tasks temporarily


# Helper function to find tasks by ID
def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)
    # next searches through tasks and finds the first one that matches the given ID, otherwise returns None
    # task at the beginning of the for loop search says to return the whole task instead of just a specified part


def validate_task_data(data): 
    errors = []
    
    if not data: # Checks if data is empty
        errors.append('Request body is required')
        return errors

    if 'title' in data and not data['title'].strip(): # Checks if title was just spaces
        errors.append('Title cannot be empty') 
    
    if 'title' in data and len(data['title']) > 200:
        errors.append('Title must be less than 200 characters')

    if 'description' in data and len(data['description']) > 1000:
        errors.append('Description must be less than 1000 characters')
    
    return errors
# Validation protects the API from invalid input


@app.route('/') # This register URL
def home():
    logger.info('Home page accessed')
    return render_template('index.html')
# This means "GET /" calls home()


@app.route('/health')
def health_check():
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': app.config['APP_NAME'],
        'version': app.config['APP_VERSION'],
        'environment': os.getenv('FLASK_ENV', 'development'),
        'tasks_count': len(tasks)
    }
    logger.info('Health check performed')
    return jsonify(health_status), 200
# This is for the purpose of health validations by the pipeline and ALB and ECS monitoring



@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    logger.info('Fetching all tasks')
    
    completed = request.args.get('completed')
    #checks URL to see if user added a specific filter
    
    filtered_tasks = tasks
    if completed is not None:
        is_completed = completed.lower() == 'true'
        filtered_tasks = [t for t in tasks if t['completed'] == is_completed]
    # creates a list of the filtered tasks
    return jsonify({
        'tasks': filtered_tasks,
        'count': len(filtered_tasks),
        'total': len(tasks)
    }), 200



@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id): # Returns a specific task

    logger.info(f'Fetching task: {task_id}')
    
    task = find_task(task_id)
    if task:
        return jsonify(task), 200
    
    logger.warning(f'Task not found: {task_id}')
    return jsonify({'error': 'Task not found'}), 404



@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() # Takes JSON data and makes it a python object
    
    #Validate input
    if not data or 'title' not in data:
        logger.error('Task creation failed: Title is required')
        return jsonify({'error': 'Title is required'}), 400
    
    errors = validate_task_data(data)
    if errors:
        logger.error(f'Task creation failed: {errors}')
        return jsonify({'errors': errors}), 400
    

    new_task = {
        'id': str(uuid.uuid4()), # generates a unique ID, completely random
        'title': data['title'].strip(), # cleans any trailing spaces
        'description': data.get('description', '').strip(),
        'completed': False,
        'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    logger.info(f'Task created: {new_task["id"]} - {new_task["title"]}')
    
    return jsonify(new_task), 201 
# 201 success code means request was successful AND a brand new resource was created



@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    logger.info(f'Updating task: {task_id}')
    
    task = find_task(task_id)
    if not task:
        logger.warning(f'Update failed: Task not found: {task_id}')
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    errors = validate_task_data(data)
    if errors:
        logger.error(f'Task update failed: {errors}')
        return jsonify({'errors': errors}), 400
    

    if 'title' in data:
        task['title'] = data['title'].strip()
    if 'description' in data:
        task['description'] = data['description'].strip()
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    logger.info(f'Task updated: {task_id}')
    return jsonify(task), 200




@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    logger.info(f'Deleting task: {task_id}')
    
    task = find_task(task_id)
    if not task:
        logger.warning(f'Delete failed: Task not found: {task_id}')
        return jsonify({'error': 'Task not found'}), 404
    
    tasks.remove(task)
    logger.info(f'Task deleted: {task_id}')
    
    return jsonify({
        'message': 'Task deleted successfully',
        'id': task_id
    }), 200




@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = len(tasks)
    completed = sum(1 for task in tasks if task['completed']) # produces a 1 value for every task thats completed and is summed
    pending = total - completed
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': round((completed / total * 100) if total > 0 else 0, 2) # Round to 2 decimal places
    }), 200 



# The following error handlers were added by claude AI
@app.errorhandler(404)
def not_found(error):
    logger.error(f'404 error: {request.url}')
    return jsonify({
        'error': 'Endpoint not found',
        'path': request.path
    }), 404
# Runs when users try a path that doesn't exist, prints the error message to the backend server log

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 error: {str(error)}')
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500
# Runs if something breaks inside the code, it prints the error to the backend server logs (not to user)


@app.errorhandler(400)
def bad_request(error):
    logger.error(f'400 error: {str(error)}')
    return jsonify({
        'error': 'Bad request',
        'message': str(error)
    }), 400
#If a user sends an incorrect request, it returns the error back to the user so they can fix it

# End of AI added error handlers

if __name__ == '__main__':
    logger.info(f'Starting {app.config["APP_NAME"]} v{app.config["APP_VERSION"]}')
    logger.info(f'Environment: {os.getenv("FLASK_ENV", "development")}')
    logger.info(f'Debug mode: {app.config["DEBUG"]}')
    # Startup is logged

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
#test
    