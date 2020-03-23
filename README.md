olutils
---



# Introduction

The module ***olutils*** provide common tools to simplify project creation. It includes:

- class with logger
- parameter management
- object management (copy, saving, loading)
- plotting (if matplotlib available)


## Installation

One can install olutils using pip install command:

    ```bash
    pip install olutils
    ```

## Usage

Use of temporal converters and deep defaultdict:

```python
import olutils

# Building a deep default dict with datetimes as values
flights = olutils.deepdefaultdict(lambda x: None, depth=2)

# Filling it
flights['Paris-NY']['departure'] = olutils.str2dt("2019-01-15 08:00+01:00")
flights['Paris-NY']['arrival'] = olutils.str2dt("2019-01-15 10:30-05:00")
flights['NY-Paris']['departure'] = olutils.str2dt("2019-01-17 23:00-05:00")
flights['NY-Paris']['arrival'] = olutils.str2dt("2019-01-15 11:00+01:00")

flights.pprint()
```

File reading and object storing:

```python
import olutils

my_dict = {'key_1': "value_1", 'key_2': 2}
my_rows = [{'col_1': 11, 'col_2': 21}, {'col_1': 21, 'col_2': 22}]

# Saving objects in output directory (automatically created)
olutils.save(my_dict, "output/my_dict.json")
olutils.save(my_rows, "output/my_rows.csv")
olutils.save(my_rows, "output/my_rows.unknown", mthd="json")

# Loading objects from save outputs
my_loaded_dict = olutils.load("output/my_dict.json")
my_loaded_rows = olutils.load("output/my_rows.csv")
my_loaded_rows_ = olutils.load("output/my_rows.unknown", mthd="json")
```



# For developers


## Download the project

Clone repository:

```bash
git clone https://github.com/OctaveLauby/olutils.git
cd olutils
```

One can make an editable code installation:

```bash
pip install -e .
```


## Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate
python -m pip install -r requirements.txt
...
deactivate
```

> matplotlib does not have to be imported: plotting submodule is not loaded in that case


## Distribution

0. Install distribution libraries

    ```bash
    pip install check-manifest
    pip install twine
    ```

1. Building manifest file:

    ```bash
    check-manifest --create
    ```

2. Building the wheel:

    ```bash
    python setup.py bdist_wheel
    ```

3. Building the source distribution:

    ```bash
    python setup.py sdist
    ```

4. Publishing:

    ```bash
    python setup.py bdist_wheel sdist
    twine upload dist/*
    ```

> For TestPyPi publication:  `twine upload --repository-url https://test.pypi.org/legacy/ dist/* `

> [Not working on Git terminal](https://github.com/pypa/packaging-problems/issues/197) for some reason


## Testing

```bash
python -m pytest olutils -vv
python -m pylint olutils --ignore-patterns=test*
```
