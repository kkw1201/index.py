import os
import signal
import subprocess
import sys
import time


def execute(*commands):
    process = subprocess.Popen(" ".join(commands), cwd=os.getcwd(), shell=True)

    def sigterm_handler(signo, frame):
        process.terminate()
        process.wait()

    signal.signal(signal.SIGTERM, sigterm_handler)

    while process.poll() is None:
        time.sleep(1)
    return process.poll()


def shell(command: str) -> None:
    exit_code = execute(command)
    if exit_code != 0:
        sys.exit(exit_code)


if __name__ == "__main__":
    shell("flake8 indexpy --ignore W503,E203,E501,E731")
    shell("mypy -p indexpy --ignore-missing-imports")
    shell("pytest --cov indexpy -s -o log_cli=true -o log_cli_level=DEBUG")
