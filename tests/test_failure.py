"""
tests/test_failure.py

This module includes a basic test that always fails to test ./src/test_runner.py
is correct.
"""
def test_always_fails():
    """
    Test that always fails.

    This test is intentionally designed to fail to check pytest is running properly.
    """
    assert False, "This test is designed to fail intentionally."