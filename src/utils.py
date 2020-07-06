import itertools
import logging
import sys
from typing import Iterable, List

from src.const import LOG_FILE, LOG_FORMATTER, PartialAssignment, TotalAssignment


def bitstrings(n: int) -> Iterable[TotalAssignment]:
    return set_exponent([True, False], n)


def all_partial_assignments(n: int, m: int) -> Iterable[PartialAssignment]:
    def all_partial_assignments_helper(n, m, running):
        if n == 0:
            yield running
        at = running.copy() + [True]
        af = running.copy() + [False]
        if m > 0:
            an = running.copy() + [None]
            x= all_partial_assignments_helper(n - 1, m, at)
            # return all_partial_assignments_helper(n - 1, m, af)
            # return all_partial_assignments_helper(n - 1, m - 1, an)
        else:
            all_partial_assignments_helper(n - 1, m, at
            )
            all_partial_assignments_helper(n - 1, m, af)

    return all_partial_assignments_helper(n, m, [])


def set_exponent(s: Iterable, n: int) -> Iterable[TotalAssignment]:
    return (list(x) for x in itertools.product(s, repeat=n))


def xor(x: TotalAssignment, y: TotalAssignment) -> TotalAssignment:
    return [a ^ b for (a, b) in zip(x, y)]


def list_of_bool_to_binary_string(list: TotalAssignment) -> str:
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
