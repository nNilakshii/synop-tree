from importlib.metadata import version

import synop_tree


def test_version_matches_installed_metadata() -> None:
    assert synop_tree.__version__ == version("synop-tree")
