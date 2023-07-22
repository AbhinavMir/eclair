# Justfile

# Define the default task
default: run

# Build and Test
build:
  python setup.py sdist bdist_wheel

# live install project
install:
  pip install -e .

requirements:
  pip install -r requirements.txt

env:
  python3 -m venv env

activate:
  source env/bin/activate

# These are tester tasks, I used them to test the code, do not use them
demo:
  python3 src/templating_logic.py
deploy:
  python3 src/deployer_template.py
# Define the run task
run:
    python3 src/agg.py
