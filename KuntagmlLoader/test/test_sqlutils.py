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

import os

import pytest

from ..core.utils.sql_utils import SQLTable, get_non_empty_tables
from ..qgis_plugin_tools.testing.utilities import is_running_inside_ci


# TODO: create proper test files
@pytest.mark.skipif(is_running_inside_ci(), reason="CI")
def test_getting_tables(new_project) -> None:
    db = os.path.join(os.path.dirname(__file__), "testdata", "test.sqlite")
    tables = get_non_empty_tables(db)
    assert len(tables) == 5


# TODO: create proper test files
@pytest.mark.skipif(is_running_inside_ci(), reason="CI")
def test_getting_tables2() -> None:
    db = os.path.join(os.path.dirname(__file__), "testdata", "kanta_Kevyenliikenteenvayla.sqlite")
    tables = get_non_empty_tables(db)
    assert len(tables) == 3


def test_sql_table() -> None:
    db = "/path/to/testdb.sqlite"
    tbl = SQLTable(db, "tbl")
    assert tbl.uri == 'dbname=\'/path/to/testdb.sqlite\' table="tbl"'


def test_sql_table_with_geom() -> None:
    db = "/path/to/testdb.sqlite"
    tbl = SQLTable(db, "tbl", "geom", 1)
    assert tbl.uri == 'dbname=\'/path/to/testdb.sqlite\' table="tbl" (geom)'
    assert tbl.type == "point"
