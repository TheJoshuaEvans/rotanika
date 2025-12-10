# General Instructions
From the project root directory, activate the virtual environment:
```sh
source .venv/bin/activate
```

Use this command to run unit tests (replace PATH/TO/FILE.py with the actual path to the test file, relative to the src directory):
```sh
python -m unittest src/PATH/TO/FILE.py -v
```

The application must be run from the project root directory - it is NOT globally installed.

# Running on TheJoshuaEvans' Local Environment
Project root directory for TheJoshuaEvans' local machine:
```
/root/dev/tje/interactive-engine
```

Test command on TheJoshuaEvans' local environment:
```sh
cd /root/dev/tje/interactive-engine && poe test
```
