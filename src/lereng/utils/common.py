import logging
import sys

import colorlog

loggers = {}


def logger_object(module_name: str):
    """Logger Obejct

    Args:
        name (string): Name of the module
    """
    if loggers.get(module_name):

        return loggers.get(module_name)

    logger = logging.getLogger(module_name)
    # Set the threshold logging level of the logger to INFO
    logger.setLevel(logging.INFO)
    # Create a stream-based handler that writes the log entries
    # into the standard output stream
    handler = logging.StreamHandler(sys.stdout)
    # Create a formatter for the logs
    formatter = colorlog.ColoredFormatter(
        f"%(log_color)s%(levelname)-2s%(reset)s\t: %(asctime)s - {module_name}\t- %(message)s",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        secondary_log_colors={
            "message": {
                "DEBUG": "white",
                "INFO": "white",
                "WARNING": "white",
                "ERROR": "white",
                "CRITICAL": "white",
            }
        },
        style="%",
    )
    # Set the created formatter as the formatter of the handler
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    loggers.update({module_name: logger})
    return logger
