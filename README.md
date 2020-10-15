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

Multi-plotting:

```python
import matplotlib.pyplot as plt
import numpy as np

from olutils import plotiter

for i in plotiter(range(5), n_cols=3):
    x = [i + k/10 for k in range(10)]
    y = [np.sin(xk) for xk in x]
    plt.plot(x, y)
```

Others:

```python
import olutils

# Operations
assert olutils.prod([2, 7]) == 14
assert olutils.identity(1) == 1

# Comparison
l1 = [1, 2, "hi", "bye"]
l2 = [3, "bye", "bye bye", 2]
assert olutils.diff(l1, l2) == {
    'common': {2, "bye"},
    'minus': {1, "hi"},
    'plus': {3, "bye bye"},
}

# Pretty display
assert olutils.err2str(ValueError("Message")) == "ValueError - Message"
l = [1, 2, 3, 4, 5]
imp_l = olutils.implicit_list(l, 4)
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


# Iteration
print("Iterating on very long iterable:")
for elem in olutils.countiter(range(int(10e6)), v_batch=100, prefix=". "):
    # One-Line display of progress every 100 iteration
    pass


# And more
# olutils.dict2str

...
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


## Release & Distribute

### Release

0. Check current version to know what is the next version

    ```bash
    git tag
    ```

1. Create release branch from branch-to-release (usually dev)

    ```bash
    git checkout <branch_to_release>
    git checkout release/x.x.x
    ```

2. Add related section in [release notes](RELEASE_NOTES.md), commit and push (even if not completed yet)

    ```
    git commit -m "Adding release note related to current release"
    git push --set-upstream origin release/x.x.x
    ```

3. Create 2 pull requests on github:
    - on from {release_branch} to {dev} (name="Release/x.x.x Dev)
    - on from {release_branch} to {master} (name="Release/x.x.x)

4. Fill up the release note + commit and push
    - Read commits descriptions
    - Go through all the Files Changes

    > Fill free to complete missing documentations and add comments in code

6. Update [setup](setup.py)
    - Update version
    - Ensure install_requires have all [requirements](requirements.txt)

7. Run tests on clean venv

    ```bash
    rm -r venv
    python -m venv venv
    source venv/Scripts/activate
    python m pytest -vv
    ```

    > If any error, fix issues + commit and push

8. Merge dev pull request on github
    - Check the File Changes (one should see the new release note and the possible fixes he made)
    - Merge pull request

    > One can redo tests locally just to be sure

9. Merge master pull request on github + Delete branch

10. Add tag and Push

    - Tag master

    ```bash
    git checkout master
    git pull
    git tag -a vx.x.x -m "Version x.x.x"
    ```

    - Tag dev

    ```bash
    git checkout dev
    git pull
    git tag -a vx.x.x-dev -m "Version x.x.x (dev)"
    ```

    - Push

    ```bash
    git push origin --tags
    ```

11. Update local repo:
    - Remove release branch: `git branch -d release/x.x.x`


### Distribution

First make sure to be on master branch with latest release.

0. Install distribution libraries

    ```bash
    pip install check-manifest
    pip install twine
    pip install wheel
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
