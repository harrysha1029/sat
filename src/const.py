import logging
from typing import List, Optional, Union

Literal = Union[int, bool]
Clause = List[Literal]
TotalAssignment = List[bool]
PartialAssignment = List[Optional[bool]]
Assignment = Union[TotalAssignment, PartialAssignment]

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)
LOG_FILE = "concordance.log"
