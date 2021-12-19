History of release notes
---

# Version 2.1.0

## New Features
- `path` module (`next_path`)
- `typing` module (`Number`, `TimeRepr`, `RowDict`, ...)

## Feature Changes:
- typing added to all function signatures
- `basedict` now only expects dict-like objects (used to handle any object)
- `SpeStr` renamed `FlatStr` (`collection.spestr` renamed `collection.flatstr`)
- `files` module renamed `os`
- `compare` module renamed `comparison`

## Other Changes:
- tests directory has been moved to project root



---

# Version 2.0.2

## Bugfixes
- `deepdefaultdict`: fix infinite loop when **depth** < 0



---

# Version 2.0.1

Lot of changes, here are the major ones:

## Removed:
- `log` module (`LogClass`, `get_loggers`, ...)
- `Row` class (implies change in `RowReader.read` signature)

## Moved to [olanalytics](https://github.com/OctaveLauby/olanalytics)
- `closest` and `previous`
- `plotting` module (`plot_iter`, `resize`, ...)

## New Objects:
- `LazyList`: list container with lazy display

## Feature Changes:
- `diff` renamed `content_diff`
- `implicit_list` renamed `lazy_content`
- `convert_ts` renamed `secs2unit`
- `dt2float` renamed `dt2ts`
- `float2dt` renamed `ts2dt`
- `Param` renamed `Params`
- time converters (`str2dt`, `ts2dt`, ...) must be imported through `olutils.conversion`
- specific storing functions (`read_csv`, `write_csv`, ...) must be imported through `olutils.storing`
- specific param tools (`check_type`, `iter_params`, ...)   must be imported through `olutils.params`

## Other changes:
- Renaming and re-ordering modules
- Renaming arguments
    - `basedict` **leaf_conv** becomes **leafconv**
    - `countiter` **v_batch** becomes **vbatch**
    - `countiter` **dft_ind** becomes **dindicator**
- Forcing positional and keyword arguments
- Improve documentation
- 100% Test Coverage
- Travis and Coverage badges



---

# Version 1.2.0

## New Functions:
- `prod`: same as sum for production
- `identity`: identity function, can be convenient
- `implicit_list`: return lazy list such as [1, 2, ..., 8, 9]
- `err2str`: convert error to string

## Features:
- **mode** argument in `open`
- **dft_ind**  and **stop** argument in `countiter`

## Bugfixes:
- `dict2str`: fix issue where **leafconv** argument was not used properly
