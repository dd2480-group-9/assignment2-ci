"""
This module provides 2 methods for server handling and HTTP interaction using flask framework
"""

import os
import shutil
from flask import Flask, request, jsonify   # Importing flask 
import git # gitpython
from src.logger import BuildHistoryManager
from src.test_runner import run_all_tests
from src.apiConnection import setCommitStatus   # Importing own module for Git connection


app = Flask(__name__)                       # Creates one intance of flask
history_manager = BuildHistoryManager()


@app.route('/')
def index():
    """
    Default route that returns a greeting message.

    This function serves as a simple test endpoint to verify that the server is running.

    Returns:
        str: A welcome message.

    """
    return 'Hello Group 9' # Output on HTTP page 

@app.route('/webhook', methods=['POST'])
def post_webhook():
    """
    
      Processes incoming webhook requests from GitHub.

      Extracts repository details, clones the repository, runs tests and API Connection for return messages 

    
        Returns : 
            flask.Response: A JSON respons with operation status
    
    """
    data = request.get_json()  
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    # Gets repository details 
    repo_info = data.get('repository')
    if not repo_info:
        return jsonify({'error': 'Repository info not found in payload'}), 400
    
    repo_url = repo_info.get('clone_url')
    if not repo_url or not commit_id:
        return jsonify({'error': 'Repository URL or commit ID missing'}), 400
    
    commit_id = data.get('after')  # The commit SHA after the push
    repo_owner = repo_info.get('owner',{}).get('login')
    repo_name = repo_info.get('name')
    pusher_name = data.get("pusher", {}).get("name")     
    
    # Setting up a temporary directory
    temp_dir = os.path.join(os.getcwd(), "tmp")

    # Remove temporary directory if it exists, then recreates it
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Clone repository and check out the specified commit 
        print(f"Cloning repository to {temp_dir}")
        repo = git.Repo.clone_from(repo_url, temp_dir)
        repo.git.checkout(commit_id)
        print(f"Checked out commit {commit_id}")
        
        passed,logs = run_all_tests(temp_dir)
        build_logs = logs        
        print("Tests result:", passed)
        
        if passed == True: 
            description = 'All tests passed'
            state = 'success'
        elif passed == False: 
            state = 'failure'
            description = 'One or more tests has failed' 

        setCommitStatus(commit_id, repo_name , repo_owner, state, description)
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