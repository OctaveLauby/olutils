olutils
---


# Introduction

The module ***olutils*** provide common tools to simplify project creation. It includes:
- class with logger
- parameter management
- object management (copy, saving, loading)


# Installation

Manual installation :

```
git clone https://github.com/OctaveLauby/olutils.git
cd olutils
pip install -e .
```

# Testing

```
pytest olutils -vv
pylint olutils --ignore-patterns=test*
```
