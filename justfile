# Justfile

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

dependency:
  python3 src/.dependency_graphs.py

clean-build:
  \rm -rf build/
  \rm -rf dist/
  \rm -rf *.egg-info
  python3 setup.py sdist bdist_wheel

# These are tester tasks, I used them to test the code, do not use them

# demo:
#   python3 src/templating_logic.py
# deploy:
#   python3 src/deployer_template.py
# run:
#     python3 src/agg.py
