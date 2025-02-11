"""
This module provides 2 methods for server handling and HTTP interaction using flask framework
"""

import os
import shutil
from flask import Flask, request, jsonify   # Importing flask 
import json                                 # Importing json
import git # gitpython

app = Flask(__name__)  # Creates one instance of flask


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
    repo_url = repo_info.get('clone_url')
    commit_id = data.get('after')  # The commit SHA after the push


    if not repo_info:
        return jsonify({'error': 'Repository info not found in payload'}), 400

  
    if not repo_url or not commit_id:
        return jsonify({'error': 'Repository URL or commit ID missing'}), 400
        
    
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
        
        # Add tests and stuff here
        
        status = 'ok'
        output = f"Checked out commit {commit_id}"

    except Exception as e:
        status = 'error'
        output = str(e)
    finally:
        shutil.rmtree(temp_dir)
        print(f"Removed temporary directory {temp_dir}")

    # Return a JSON response with the build status and logs.
    return jsonify({'status': status, 'output': output})

if __name__ == '__main__':
    app.run(debug=True, port = 8009, host='0.0.0.0') 
