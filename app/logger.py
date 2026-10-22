########################
# Logger Configuration #
########################

import logging
import os
from pathlib import Path

def setup_logger(log_file: Path) -> None:
    """
    Set up the logging configuration.

    This function configures the logging system to write logs to a specified file.
    It ensures that the log directory exists and sets the logging level and format.     

    Args:
        log_file (Path): The path to the log file where logs will be written.
    """
    try:
        # Ensure the log directory exists
        os.makedirs(log_file.parent, exist_ok=True)

        # Configure the basic logging settings
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True  # Overwrite any existing logging configuration
        )
        logging.info(f"Logging initialized at: {log_file}")
    except Exception as e:
        # Print an error message and re-raise the exception if logging setup fails
        print(f"Error setting up logging: {e}")
        raise
