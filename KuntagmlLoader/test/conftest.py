"""
This class contains fixtures and common helper function to keep the test files shorter
"""

import pytest
from qgis.core import QgsProject

from ..qgis_plugin_tools.testing.utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()
QGIS_INSTANCE = QgsProject.instance()


@pytest.fixture(scope='function')
def new_project() -> None:
    """Initializes new iface project"""
    yield IFACE.newProject()
