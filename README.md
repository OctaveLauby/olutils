olutils
---




# Introduction

## About

The module ***olutils*** provide common tools to simplify daily coding. It includes:

- object management (saving, loading for .txt, .csv, .pickle)
- convenient collection (deep defaultdict, lazy list, identity/prod functions)
- conversion functions (for datetime, dictionaries, errors)
- sequencing helpers (iteration with progress display, wait until predicate)
- parameter management
- and more...



## Installation

One can install olutils using pip install command: `pip install olutils`




# Usage

## Collections

* `deepdefaultdict`

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


* `LazyList`

```python
import olutils

print(olutils.LazyList(range(10000), 10))
```


* functions: `prod` and `identity`

```python
import olutils

# Operations
assert olutils.prod([2, 7]) == 14
assert olutils.identity(1) == 1
```



## Object management

* Storage: `save` and `load`

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



## More

* Explicit iteration

```python
import olutils


print("Iterating on very long iterable:")
for elem in olutils.countiter(range(int(10e6)), v_batch=100, prefix=". "):
    # One-Line display of progress every 100 iteration
    pass
```


* Compare

```python
import olutils

# Comparison
l1 = [1, 2, "hi", "bye"]
l2 = [3, "bye", "bye bye", 2]
assert olutils.diff(l1, l2) == {
    'common': {2, "bye"},
    'minus': {1, "hi"},
    'plus': {3, "bye bye"},
}
```


* Pretty displays

```python
import olutils

assert olutils.err2str(ValueError("Message")) == "ValueError - Message"
l = [1, 2, 3, 4, 5]
imp_l = olutils.lazy_content(l, 4)
assert str(imp_l) == '[1, 2, ..., 5]'
dic = {
    'values': l,
    'info': {
        'name': "Some example",
        'also': "This is awesome (kinda)",
    }
}
print(f"Dictionary used: {dic}")
print(f"Dictionary to pretty string:")
def leafconv(x):
    return (
        str(olutils.implicit_list(x, 5))
        if isinstance(x, list)
        else str(x)
    )
print(olutils.dict2str(dic, leafconv=leafconv))
```
