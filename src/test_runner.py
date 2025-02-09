
import subprocess

def run_all_tests() -> tuple[bool, str]:
   
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
