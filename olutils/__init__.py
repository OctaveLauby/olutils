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
    identity,
    prod,
)
from .conversion import (
    basedict,
    convert_ts,
    dict2str,
    dt2float,
    err2str,
    float2dt,
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
