# Justfile

# Define the default task
default: run

demo:
  python3 src/templating_logic.py
deploy:
  python3 src/deployer_template.py
# Define the run task
run:
    python3 src/agg.py
