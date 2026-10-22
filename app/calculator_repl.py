########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging

from colorama import Fore, init

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

init(autoreset=True)  # Initialize colorama for colored output

# Define colors for REPL messages
INFO_COLOR = Fore.CYAN
PROMPT_COLOR = Fore.LIGHTMAGENTA_EX
SUCCESS_COLOR = Fore.GREEN
WARNING_COLOR = Fore.YELLOW
ERROR_COLOR = Fore.RED


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(INFO_COLOR + "Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input(PROMPT_COLOR + "\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print(INFO_COLOR + "\nAvailable commands:")
                    print(INFO_COLOR + "  add, subtract, multiply, divide, power, root, modulus, percent, int_divide, abs_diff - Perform calculations")
                    print(INFO_COLOR + "  history - Show calculation history")
                    print(INFO_COLOR + "  last - Show the last calculation performed")
                    print(INFO_COLOR + "  clear - Clear calculation history")
                    print(INFO_COLOR + "  undo - Undo the last calculation")
                    print(INFO_COLOR + "  redo - Redo the last undone calculation")
                    print(INFO_COLOR + "  save - Save calculation history to file")
                    print(INFO_COLOR + "  load - Load calculation history from file")
                    print(INFO_COLOR + "  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(SUCCESS_COLOR + "History saved successfully.")
                    except Exception as e:
                        print(WARNING_COLOR + f"Warning: Could not save history: {e}")
                    print(PROMPT_COLOR + "Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print(WARNING_COLOR + "No calculations in history")
                    else:
                        print(PROMPT_COLOR + "\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(PROMPT_COLOR + f"{i}. {entry}")
                    continue

                if command == 'last':
                    # Show the last calculation performed
                    last_calc = calc.last_calculation()
                    if last_calc:
                        print(PROMPT_COLOR + f"Last Calculation: {last_calc}")
                    else:
                        print(WARNING_COLOR + "No calculations have been performed yet.")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print(SUCCESS_COLOR + "History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print(SUCCESS_COLOR + "Operation undone")
                    else:
                        print(WARNING_COLOR + "Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print(SUCCESS_COLOR + "Operation redone")
                    else:
                        print(WARNING_COLOR + "Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print(SUCCESS_COLOR + "History saved successfully")
                    except Exception as e:
                        print(ERROR_COLOR + f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print(SUCCESS_COLOR + "History loaded successfully")
                    except Exception as e:
                        print(ERROR_COLOR + f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'percent', 'int_divide', 'abs_diff']:
                    # Perform the specified arithmetic operation
                    try:
                        print(PROMPT_COLOR + "\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(WARNING_COLOR + "Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(WARNING_COLOR + "Operation cancelled")
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = format(result.normalize(), 'f')

                        print(SUCCESS_COLOR + f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(ERROR_COLOR + f"Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(ERROR_COLOR + f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                print(ERROR_COLOR + f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print(WARNING_COLOR + "\nOperation cancelled")
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print(WARNING_COLOR + "\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(ERROR_COLOR + f"Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(ERROR_COLOR + f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
