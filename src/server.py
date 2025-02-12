"""
This module provides 2 methods for server handling and HTTP interaction using flask framework
"""

import os
import shutil
from flask import Flask, request, jsonify   # Importing flask 
import json                                 # Importing json
import git # gitpython
from logger import BuildHistoryManager
from test_runner import run_all_tests


app = Flask(__name__)  # Creates one instance of flask

history_manager = BuildHistoryManager()

# Defining the initial route
@app.route('/')
def index():
    
    return 'Hello Group 9' # Output on HTTP page 
   
# Route that reacts when "input" is given such as webhooks or requests
@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    # Extract repository info and commit hash.
    repo_info = data.get('repository')
    if not repo_info:
        return jsonify({'error': 'Repository info not found in payload'}), 400

    repo_url = repo_info.get('clone_url')
    commit_id = data.get('after')  # The commit SHA after the push
    if not repo_url or not commit_id:
        return jsonify({'error': 'Repository URL or commit ID missing'}), 400
        
    temp_dir = os.path.join(os.getcwd(), "tmp")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        print(f"Cloning repository to {temp_dir}")
        repo = git.Repo.clone_from(repo_url, temp_dir)
        repo.git.checkout(commit_id)

        passed,logs= run_all_tests(temp_dir)
        build_logs = logs
        pusher_name = data.get("pusher", {}).get("name")

        
        print(f"Checked out commit {commit_id}")
        print("Tests passed:", passed)
        # Add tests and stuff here
        
        status = 'ok'
        output = f"Checked out commit {commit_id}"

    except Exception as e:
        status = 'error'
        output = str(e)
    finally:
        shutil.rmtree(temp_dir)
        print(f"Removed temporary directory {temp_dir}")

    final_passed = (status == 'ok') and passed
    build_id = history_manager.add_build(
        commit_id=commit_id,
        passed=final_passed,
        logs=build_logs,
        pusher=pusher_name
    )

    build_url = f"{request.host_url}builds/{build_id}"
    return jsonify({
        'status': status,
        'passed': final_passed,
        'commit_id': commit_id,
        'pusher': pusher_name,
        'build_id': build_id,
        'build_url': build_url,
        'logs_snippet': build_logs[-500:]  
    })

    # Return a JSON response with the build status and logs.
    return jsonify({'status': status, 'output': output})

@app.route('/builds', methods=['GET'])
def list_builds():
    """
    Returns JSON array of saved builds.
    """
    all_builds = history_manager.get_all_builds()
    return jsonify(all_builds), 200

@app.route('/builds/<int:build_id>', methods=['GET'])
def get_build_details(build_id):
    """
    Returns JSON details of a single build.
    """
    build = history_manager.get_build_by_id(build_id)
    if not build:
        return jsonify({'error': 'Build not found'}), 404
    return jsonify(build), 200
 

if __name__ == '__main__':
    app.run(debug=True, port = 8009, host='0.0.0.0') 