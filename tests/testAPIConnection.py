import requests
import unittest
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv
import sys 

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from apiConnection import setCommitStatus

# to run: python -m unittest tests.testAPIConnection

class testSetCommitStatus(unittest.TestCase):

    @patch('requests.post')
    def test_success(self, mock_post):
        mock_response = MagicMock() 
        mock_response.status_code = 201
        mock_response.text = 'Created'
        mock_post.return_value = mock_response

        # Test data
        commitSHA = "a668da4f96de41c8c0225b8ceb14cf4212909923"
        repo = "assignment2-ci"
        repoOwner = "dd2480-group-9"
        state = 'success'
        description = 'The tests passed'

        setCommitStatus(commitSHA, repo, repoOwner, state, description)

        # Checking if requests.post was called with the correct url and headers
        mock_post.assert_called_once_with(
            
            f"https://api.github.com/repos/{repoOwner}/{repo}/statuses/{commitSHA}",
            json={"state": state, "description": description},
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {os.getenv('TOKEN')}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
        # Checking the status code and text of the mock response
        self.assertEqual(mock_response.status_code, 201)
        self.assertEqual(mock_response.text, 'Created')

if __name__ == '__main__':
    unittest.main()