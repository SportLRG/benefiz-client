# Project Setup Instructions

## Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/docs/#installation) - Dependency Management and Packaging tool

## Environment Variables

Ensure the following environment variables are set:

- `SSS_API_ACCOUNT_NAME`
- `SSS_API_KEY`

additionally environment variables can be set :
- `DAYS_FUTURE` number of future days where appoints will be considered
- `DAYS_PAST` number of past days where appoints will be considered

e.g.:
``` sh
SSS_API_KEY=
SSS_API_ACCOUNT_NAME=Test_Lingen
DAYS_PAST=120
DAYS_FUTURE=7
BOAT_SCHEDULE_NAME="Test Winter"
TRAINING_SCHEDULE_NAME="Benefiz Plan"
TRAINER_SCHEDULE_NAME="Personen"

```


## Prepare environment on windows
1. **Install Scoop:**

    Open PowerShell as Administrator and run:

    ```sh
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    ```

2. **Install Git, Python, Poetry:**

    ```sh
    scoop install git python poetry
    ```

## Setup Instructions

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Install dependencies using Poetry:**

    ```sh
    poetry install
    ```

3. **Run the application:**

    ```sh
    poetry run main.py
    ```

## refer to
https://www.supersaas.com/info/dev/appointment_api
