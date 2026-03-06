"""A smoke test so the package, test runner, and CI are wired up before v1 lands."""

import monkway


def test_package_imports():
    assert monkway.__version__ == "0.0.1"
