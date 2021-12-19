from datetime import datetime, timedelta
from typing import Any, Callable, Dict, TypeVar, Union

import numpy as np

RowDict = Dict[str, Any]
Factory = Callable[[], Any]  # Used by defaultdict
Number = Union[int, float, np.number]
T = TypeVar("T")  # Generic type
TimeRepr = Union[Number, datetime, timedelta]
