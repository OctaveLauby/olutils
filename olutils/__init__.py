"""Tools for common operation in a module

- conversions
- file writing / reading
- object storing
- parameter management
- loop monitoring
"""
from .collection import (
    defaultdict,
    deepdefaultdict,
    lazy_content,
    LazyList,
    identity,
    prod,
    Singleton,
)
from .comparison import content_diff
from .conversion import (
    basedict,
    dict2str,
    err2str,
)
from .os import (
    mkdirs,
    rmdirs,
    sopen,
)
from .params import (
    read_params,
    DFT,
)
from .storing import (
    load,
    save,
)
from .sequencing import (
    countiter,
    display,
    wait_until,
)
