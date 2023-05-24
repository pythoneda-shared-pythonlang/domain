# log_config.py
import logging
import sys

def next_higher_level(level):
    levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    for i, current_level in enumerate(levels):
        if level == current_level:
            return levels[i - 1] if i > 0 else current_level
    return level

def configure_logging(verbose: bool, trace: bool, quiet: bool):
    level = logging.WARNING
    if (quiet):
        level = logging.ERROR
    elif (trace):
        level = logging.DEBUG
    elif (verbose):
        level = logging.INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    default_logger = logging.getLogger()
    default_logger.setLevel(level)
    default_logger.addHandler(console_handler)

    default_level = default_logger.getEffectiveLevel()

    next_level = next_higher_level(default_level)

    for name in [ "urllib3.connectionpool" ]:
        logger = logging.getLogger(name)
        logger.setLevel(next_level)
