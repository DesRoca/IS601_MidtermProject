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

        print(Fore.CYAN + "Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input(Fore.LIGHTMAGENTA_EX + "\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print(Fore.CYAN + "\nAvailable commands:")
                    print(Fore.CYAN + "  add, subtract, multiply, divide, power, root, modulus, percent, int_divide, abs_diff - Perform calculations")
                    print(Fore.CYAN + "  history - Show calculation history")
                    print(Fore.CYAN + "  last - Show the last calculation performed")
                    print(Fore.CYAN + "  clear - Clear calculation history")
                    print(Fore.CYAN + "  undo - Undo the last calculation")
                    print(Fore.CYAN + "  redo - Redo the last undone calculation")
                    print(Fore.CYAN + "  save - Save calculation history to file")
                    print(Fore.CYAN + "  load - Load calculation history from file")
                    print(Fore.CYAN + "  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully.")
                    except Exception as e:
                        print(Fore.YELLOW + f"Warning: Could not save history: {e}")
                    print(Fore.LIGHTMAGENTA_EX + "Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print(Fore.YELLOW + "No calculations in history")
                    else:
                        print(Fore.LIGHTMAGENTA_EX + "\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(Fore.LIGHTMAGENTA_EX + f"{i}. {entry}")
                    continue

                if command == 'last':
                    # Show the last calculation performed
                    last_calc = calc.last_calculation()
                    if last_calc:
                        print(Fore.LIGHTMAGENTA_EX + f"Last Calculation: {last_calc}")
                    else:
                        print(Fore.YELLOW + "No calculations have been performed yet.")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print(Fore.GREEN + "History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print(Fore.GREEN + "Operation undone")
                    else:
                        print(Fore.YELLOW + "Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print(Fore.GREEN + "Operation redone")
                    else:
                        print(Fore.YELLOW + "Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully")
                    except Exception as e:
                        print(Fore.RED + f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print(Fore.GREEN + "History loaded successfully")
                    except Exception as e:
                        print(Fore.RED + f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'percent', 'int_divide', 'abs_diff']:
                    # Perform the specified arithmetic operation
                    try:
                        print(Fore.LIGHTMAGENTA_EX + "\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(Fore.YELLOW + "Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(Fore.YELLOW + "Operation cancelled")
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = format(result.normalize(), 'f')

                        print(Fore.GREEN + f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(Fore.RED + f"Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(Fore.RED + f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                print(Fore.RED + f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print(Fore.YELLOW + "\nOperation cancelled")
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print(Fore.YELLOW + "\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(Fore.RED + f"Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(Fore.RED + f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
