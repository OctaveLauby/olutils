"""olutils provide tools for common operation in a module

- conversions
- file writing / reading
- object storing
- logs
- parameter management
- loop monitoring
- plotting (if matplotlib available)
"""
from .collection import (
    deepdefaultdict,
    defaultdict,
    lazy_content,
    LazyList,
    identity,
    prod,
)
from .compare import content_diff
from .conversion import (
    basedict,
    convert_seconds,
    dict2str,
    dt2ts,
    err2str,
    ts2dt,
    str2dt,
)
from .files import (
    mkdirs,
    rmdirs,
    sopen,
)
from .params import (
    add_dft_args,
    check_type,
    iter_params,
    Param,
    read_params,
    DFT,
)
from .storing import (
    load,
    read_csv,
    RowReader,
    save,
    write_csv,
)
from .sequencing import (
    countiter,
    display,
    wait_until,
)
