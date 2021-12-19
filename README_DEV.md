olutils - developer documentation
---

[![travis](https://img.shields.io/travis/com/OctaveLauby/olutils/dev?label=travis)](https://travis-ci.com/OctaveLauby/olutils)
[![codecov](https://codecov.io/gh/OctaveLauby/olutils/branch/dev/graph/badge.svg)](https://codecov.io/gh/OctaveLauby/olutils/branch/dev)
[![PyPI Latest Release](https://img.shields.io/pypi/v/olutils.svg)](https://pypi.org/project/olutils/)


# Basics


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



## Testing

Classic testing

```bash
python -m pytest tests -vv
python -m pylint olutils
```

Testing with coverage

```bash
coverage run -m pytest tests; coverage report
```

Or, if one has pytest-cov installed:

```bash
python -m pytest tests --cov
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



# Release & Distribute

## Release

0. Check current version to know what is the next version

    ```bash
    git tag
    ```

1. Create release branch from branch-to-release (usually dev)

    ```bash
    git checkout -b release/x.x.x
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


## Distribution

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
