# IS601 Midterm Project: Enhanced Calculator Command-Line Application

## Objective

This assignment focuses on building an advanced calculator application with various arithmetic operations, a command-line interface (REPL), and robust error handling. You'll use several design patterns (Factory, Memento, Observer) and implement features like undo/redo, logging, history management, and CI/CD pipelines. Additionally, you'll enhance the application with optional advanced features.

## Features

- **Arithmetic operations:** Addition, subtraction, multiplication, and division.
- **Additional operations:** Power, root, modulus, integer division, percentage calculation, and absolute difference.
- **Command-line interface:** Interactive REPL (Read-Eval-Print Loop) with color-coded output using Colorama.
- **Input validation and error handling:** Validates numerical inputs and handles invalid operations, division by zero, and other errors.
- **Calculation history:** Stores calculation results and timestamps and supports saving and loading history using CSV files.
- **Undo and redo:** Allows users to undo previous calculations and restore undone calculations.
- **Logging:** Records application events and calculation activity in a log file.
- **Automatic saving:** Supports automatically saving calculation history when new calculations are performed.
- **Configuration management:** Uses environment variables and a `.env` file to configure application settings.
- **Unit testing:** Uses pytest and pytest-cov to test functionality and measure code coverage.
- **Continuous integration:** Uses GitHub Actions to run automated tests and enforce a minimum coverage requirement.

## Technologies Used

- Python
- pytest and pytest-cov
- pandas
- Colorama
- python-dotenv
- Git and GitHub Actions

## Installation Instructions

### 1. Clone the repository

Clone the repository and navigate to the project directory:

```bash
git clone git@github.com:DesRoca/IS601_MidtermProject.git
cd IS601_MidtermProject
```

### 2. Create a virtual environment

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment on macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

Upgrade pip and install the project dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure the virtual environment is activated before installing dependencies or running the application.

## Configuration Setup

The application uses a `.env` file to manage configuration settings. This allows users to customize application behavior without modifying the source code.

### 1. Create the `.env` file

Create a file named `.env` in the project root directory, alongside `main.py`.

```bash
touch .env
```

### 2. Configure environment variables

The following variables are used for configuring the application. The application can use default values when optional settings are not provided.

```dotenv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```
These variables control the calculator's configuration:

CALCULATOR_MAX_HISTORY_SIZE: Sets the maximum number of calculations retained in history.
CALCULATOR_AUTO_SAVE: Enables or disables automatic saving of calculation history.
CALCULATOR_DEFAULT_ENCODING: Specifies the default character encoding used for file operations.

You can adjust these values to suit your needs. Make sure the values follow the expected formats for each setting.

### 3. Protect the `.env` file

The `.env` file contains local configuration and should not be committed to version control.

Add the following entries to `.gitignore` if they are not already present:

```gitignore
.env
venv/
__pycache__/
.pytest_cache/
.coverage
htmlcov/
logs/
```

The application can create the log and history directories automatically when needed.

## Usage Guide

### Starting the application

Run the calculator from the project root directory:

```bash
python3 main.py
```

The calculator starts an interactive command-line interface. Enter a supported command to perform an operation or manage calculation history.

### Calculation commands

The calculator supports the following operations:

| Command | Description | Example |
|---|---|---|
| `add` | Adds two numbers | `add 5 3` |
| `subtract` | Subtracts the second number from the first | `subtract 5 3` |
| `multiply` | Multiplies two numbers | `multiply 5 3` |
| `divide` | Divides the first number by the second | `divide 6 2` |
| `power` | Raises the first number to the power of the second | `power 2 3` |
| `root` | Calculates the nth root of the first number, using the second as the root degree | `root 27 3` |
| `modulus` | Calculates the remainder | `modulus 10 3` |
| `int_divide` | Performs integer division | `int_divide 10 3` |
| `percent` | Calculates what percentage the first number is of the second | `percent 25 100` |
| `abs_diff` | Calculates the absolute difference between two numbers | `abs_diff 3 10` |

### History and application commands

| Command | Description |
|---|---|
| `help` | Displays available commands and usage instructions. |
| `history` | Displays the calculation history. |
| `last` | Displays the most recent calculation. |
| `clear` | Clears the calculation history. |
| `undo` | Reverts the most recent calculation. |
| `redo` | Restores a previously undone calculation. |
| `save` | Manually saves calculation history to a CSV file. |
| `load` | Loads calculation history from the saved CSV file. |
| `exit` | Saves history as configured and exits the application. |

The interface uses color-coded messages to make prompts, successful calculations, warnings, and errors easier to distinguish.

### Error handling

The calculator validates user input and displays appropriate error messages when an operation cannot be completed.

## Logging

The application uses Python's built-in `logging` module to record important application events and errors.

### Log file location

By default, log output is stored in:

```text
logs/calculator.log
```

The log directory and file location can be configured through the application's configuration settings and supported environment variables.

### Log contents

The log records events such as:

- Calculator initialization.
- Logging initialization.
- Operation selection and calculation activity.
- History management and saving.
- Warnings and errors encountered during execution.

Log entries use timestamps, severity levels, and descriptive messages to help with troubleshooting.

The application configures logging at the INFO level. The log directory is created automatically when necessary.

## Testing Instructions

The project uses pytest for unit testing and pytest-cov for measuring test coverage.

### Run the full test suite

With the virtual environment activated, run:

```bash
pytest
```

This executes the project's unit tests and reports any failures.

### Run tests with coverage

To measure coverage for the application code, run:

```bash
pytest --cov=app --cov-report=term-missing
``