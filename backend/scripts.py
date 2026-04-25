import subprocess
import sys

PACKAGE_NAME = "vector_os"
PYTHON = sys.executable


def load_data():
    subprocess.run([PYTHON, "-m", f"{PACKAGE_NAME}.db.load"], check=True)


def start_app():
    subprocess.run([PYTHON, "-m", f"{PACKAGE_NAME}.db.load"], check=True)
    subprocess.run([PYTHON, "-m", f"{PACKAGE_NAME}.main"], check=True)


def format():
    subprocess.run(["isort", f"./{PACKAGE_NAME}", "./tests/", "--profile", "black"], check=True)
    subprocess.run(["black", f"./{PACKAGE_NAME}"], check=True)


def check_format():
    subprocess.run(["black", "--check", f"./{PACKAGE_NAME}"], check=True)


def sort_imports():
    subprocess.run(["isort", f"./{PACKAGE_NAME}", "./tests/", "--profile", "black"], check=True)


def check_sort_imports():
    subprocess.run(["isort", f"./{PACKAGE_NAME}", "--check-only", "--profile", "black"], check=True)


def check_lint():
    subprocess.run(["pylint", "--rcfile=.pylintrc", f"./{PACKAGE_NAME}"], check=True)


def mypy():
    subprocess.run([PYTHON, "-m", "mypy", f"./{PACKAGE_NAME}"], check=True)


def test():
    subprocess.run([PYTHON, "-m", "pytest", PACKAGE_NAME, "--log-level=CRITICAL"], check=True)


def test_cov():
    subprocess.run(
        [
            PYTHON,
            "-m",
            "pytest",
            "-vv",
            f"--cov=./{PACKAGE_NAME}",
            "--cov-report=xml",
            "--log-level=CRITICAL",
        ],
        check=True,
    )


def cov():
    subprocess.run(["coverage", "html"], check=True)
    print("If data was present, coverage report is in ./htmlcov/index.html")
