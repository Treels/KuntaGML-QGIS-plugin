"""
This class contains fixtures and common helper function to keep the test files shorter
"""

#  Gispo Ltd., hereby disclaims all copyright interest in the program KuntaGML-QGIS-plugin
#  Copyright (C) 2020 Gispo Ltd (https://www.gispo.fi/).
#
#
#  This file is part of KuntaGML-QGIS-plugin.
#
#  KuntaGML-QGIS-plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  KuntaGML-QGIS-plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with KuntaGML-QGIS-plugin.  If not, see <https://www.gnu.org/licenses/>.

import pytest
from qgis.core import QgsProject

from ..qgis_plugin_tools.testing.utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()
QGIS_INSTANCE = QgsProject.instance()


@pytest.fixture(scope='function')
def new_project() -> None:
    """Initializes new iface project"""
    yield IFACE.newProject()
