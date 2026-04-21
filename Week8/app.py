from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    { "id": 1, "title": "Learn API Testing", "completed": False },
    { "id": 2, "title": "Read JJ Geewax Chapter 6", "completed": False }
]

def get_next_id():
    return max([t["id"] for t in tasks], default=0) + 1

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"message": "Title is required"}), 400
    
    new_task = {
        "id": get_next_id(),
        "title": data['title'],
        "completed": data.get('completed', False)
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"message": "Task not found"}), 404
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"message": "Task not found"}), 404
        
    data = request.get_json() or {}
    if 'title' in data:
        task['title'] = data['title']
    if 'completed' in data:
        task['completed'] = data['completed']
        
    return jsonify(task), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"message": "Task not found"}), 404
        
    tasks = [t for t in tasks if t["id"] != task_id]
    return '', 204

if __name__ == '__main__':
    app.run(port=3000, debug=True)
