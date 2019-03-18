import pytest

try:
    import matplotlib
except ModuleNotFoundError:
    pytest.skip("Skipping plotting tests as matplotlib is not available", allow_module_level=True)
