# Rotanika
A bring-your-own-key AI-powered "[Akinator](https://en.akinator.com/)" clone

# Development
All instructions are intended to be used in a linux environment (specifically WSL/Ubuntu)

## Run With Docker
Run the game from source using docker
```sh
docker-compose run --rm rotanika
# - or -
poe run:docker # Running in an established environment
```

## Set Up Environment
Run these commands to establish the virtual environment and enable poe commands:
```sh
python3.12 -m venv --prompt rotanika .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Example Commands
Run all tests
```sh
poe test
```

Build the game
```sh
poe build
```
