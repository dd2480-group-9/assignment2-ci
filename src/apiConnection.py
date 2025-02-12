import requests
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: to be changed dynamically, based on test function
repo = "assignment2-ci"
repoOwner = "dd2480-group-9"
commitSHA = "a668da4f96de41c8c0225b8ceb14cf4212909923" 
state = 'success'
description = 'The tests passed'

def setCommitStatus(commitSHA, repo, repoOwner, state, description):
    '''
    This function sets the commit status of a specific commit based on the result of tests. 

    Parameters:
        commitSHA (str): The SHA hash of the commit 
        repo (str): The repository which contains the commit
        repoOwner (str): The owner of the repository
        state (str): The state of the commit (success, failure, error, pending) based on the result of the test function
        description (str): Description of the state 

    Returns: 
        None 
    '''
    
    url = f"https://api.github.com/repos/{repoOwner}/{repo}/statuses/{commitSHA}"

    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {os.getenv('TOKEN')}",
    "X-GitHub-Api-Version": "2022-11-28"
    }

    payload = {
        "state": state, 
        "description": description
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)

    if response.status_code == 201:
        print(f"Successfully set the commit status to {state}")
    else:
        print(f"Failed to set commit status: {response.status_code} - {response.text}")


if __name__ == "__main__":
    setCommitStatus(commitSHA, repo, repoOwner, state, description)

