olutils
---


# Introduction

The module ***olutils*** provide common tools to simplify project creation. It includes:
- class with logger
- parameter management
- object management (copy, saving, loading)


## Installation

For editable code installation :

```
git clone https://github.com/OctaveLauby/olutils.git
cd olutils
pip install -e .
```

For classic installation (/!\ when library will be published):

```
pip install olutils
```


## Usage


Use of temporal converters and deep defaultdict :

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


File reading and object storing :

```python
import olutils

my_dict = {'key_1': "value_1", 'key_2': 2}
my_rows = [{'col_1': 11, 'col_2': 21}, {'col_1': 21, 'col_2': 22}]
olutils.save(my_dict, "output/my_dict.json")
olutils.save(my_rows, "output/my_rows.csv")
olutils.save(my_rows, "output/my_rows.unknown", mthd="json")

my_loaded_dict = olutils.load("output/my_dict.json")
my_loaded_rows = olutils.load("output/my_rows.csv")
my_loaded_rows_ = olutils.load("output/my_rows.unknown", mthd="json")
```



# For developers

## Virtual Environment

Using classical virtual environment :

```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
...
deactivate
```

Using new pipenv feature (`pip install pipenv`)

```
pipenv install
pipenv shell
...
exit
```


## Testing

```
python -m pytest olutils -vv
pylint olutils --ignore-patterns=test*
```
