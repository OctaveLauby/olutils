"""olutils provide tools for common operation in a module

- conversions
- file writing / reading
- object storing
- logs
- parameter management
- loop monitoring
- plotting (if matplotlib available)
"""
from .collection import *
from .conversion import *
from .storing import *
from .files import *
from .log import *
from .params import *
from .search import *
from .tools import *

try:
    from .plotting import *
except ModuleNotFoundError:
    pass
