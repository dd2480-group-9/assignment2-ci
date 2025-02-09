"""
test_runner.py

This module provides a function, `run_all_tests()`, that executes all tests
under the './tests' folder using pytest. 

Usage:
    To run tests, execute this file:
        $ python test_runner.py
"""
import subprocess

def run_all_tests() -> tuple[bool, str]:
    """
    Runs all tests in the ./tests folder using pytest.

    Returns:
        A tuple (passed, logs):
          - passed (bool): True if all tests passed, False otherwise.
          - logs (str): Stores the logs when tests are executed.
    """
   
    # Defines the command to run on ./tests folder.
    cmd = ["pytest", "./tests"] 

    # Executes the command, captures the output and keeps it as string/
    process = subprocess.run(cmd, capture_output=True, text=True)

    # Checks if all the tests are passed or not.
    passed = (process.returncode == 0)
    
    # Stores the logs
    logs = process.stdout + "\n" + process.stderr

    return passed, logs

if __name__ == '__main__':
    # If this module is executed directly, run all tests.
    passed, logs = run_all_tests()
    print("Tests passed:", passed)
    print("Logs:")
    print(logs)
