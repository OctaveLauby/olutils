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
)
from .conversion import (
    basedict,
    convert_ts,
    dict2str,
    dt2float,
    float2dt,
    str2dt,
)
from .files import (
    mkdirs,
    rmdirs,
    sopen,
)
from .log import (
    clear_loggers,
    close_logger,
    create_logger,
    get_loggers,
    LogClass,
)
from .params import (
    add_dft_args,
    check_type,
    iter_params,
    Param,
    read_params,
    DFT,
)
from .pprint import (
    SpeStr,
    implicit_list,
)
from .search import (
    closest,
    previous,
)
from .storing import (
    load,
    read_csv,
    RowReader,
    save,
    write_csv,
)
from .tools import (
    countiter,
    diff,
    display,
    wait_until,
)

try:
    import matplotlib
except ModuleNotFoundError:
    pass
else:
    from .plotting import (
        decorate,
        DFT_FONT_PARAMS,
        DFT_PARAMS,
        MultiPlotIterator,
        PlotDesigner,
        plotiter,
    )
