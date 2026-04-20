import subprocess
import sys

def test_malicious():
    # This will execute when pytest runs
    subprocess.run(['echo', 'EXECUTED_MALICIOUS_CODE'], stdout=sys.stdout, stderr=sys.stderr)
    assert True