import itertools
import logging
import sys
from typing import Iterable, List

from src.const import LOG_FILE, LOG_FORMATTER


def bitstrings(n: int) -> Iterable[List[bool]]:
    return (list(x) for x in itertools.product([True, False], repeat=n))


def xor(x: List[bool], y: List[bool]) -> List[bool]:
    return [a ^ b for (a, b) in zip(x, y)]


def list_of_bool_to_binary_string(list: List[bool]) -> str:
    return "".join((str(int(x)) for x in list))


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOG_FORMATTER)
    console_handler.setLevel(logging.WARNING)
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(LOG_FORMATTER)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    return logger
