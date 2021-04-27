import subprocess
from typing import Optional


def git(cmd) -> Optional[str]:
    complete = subprocess.run(cmd, shell=True, capture_output=True)
    if complete.returncode == 0:
        return complete.stdout.decode('utf-8').rstrip()
    return None
