import logging
from typing import List, Optional, Union

Literal = Union[int, bool]
Clause = List[Literal]
TotalAssignment = List[bool]
PartialAssignment = List[Optional[bool]]

# The ith variable is in index i-1
Assignment = Union[TotalAssignment, PartialAssignment]

# maps index i+1 to variable number i+1
Permutation = List[int]

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)
LOG_FILE = "sat.log"
