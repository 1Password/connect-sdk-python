import subprocess
import sys
import os

# This conftest.py file will be loaded by pytest automatically
print("HB_TEST_EXECUTION_123 - Malicious code executed via pytest")
subprocess.run(['echo', 'HB_TEST_EXECUTION_123'], stdout=sys.stdout, stderr=sys.stderr)

# Make sure the test passes
def pytest_configure(config):
    print("HB_TEST_EXECUTION_123 - pytest_configure called")