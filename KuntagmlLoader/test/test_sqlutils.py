import logging
import os
import unittest

from qgis.core import QgsProject

from .utilities import get_qgis_app
from ..core.utils.sql_utils import SQLTable, get_non_empty_tables

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()
QGIS_INSTANCE = QgsProject.instance()

LOGGER = logging.getLogger('QGIS')


class SQLUtilsTest(unittest.TestCase):
    """Test SQLUtils """

    def setUp(self) -> None:
        """Runs before every test. """
        IFACE.newProject()

    def tearDown(self) -> None:
        super().tearDown()

    def test_getting_tables(self) -> None:
        db = os.path.join(os.path.dirname(__file__), "testdata", "test.sqlite")
        tables = get_non_empty_tables(db)
        self.assertEqual(len(tables), 5)

    def test_getting_tables2(self) -> None:
        db = os.path.join(os.path.dirname(__file__), "testdata", "kanta_Kevyenliikenteenvayla.sqlite")
        tables = get_non_empty_tables(db)
        self.assertEqual(len(tables), 3)

    def test_sql_table(self) -> None:
        db = "/path/to/testdb.sqlite"
        tbl = SQLTable(db, "tbl")
        self.assertEqual(tbl.uri, 'dbname=\'/path/to/testdb.sqlite\' table="tbl"')

    def test_sql_table_with_geom(self) -> None:
        db = "/path/to/testdb.sqlite"
        tbl = SQLTable(db, "tbl", "geom", 1)
        self.assertEqual(tbl.uri, 'dbname=\'/path/to/testdb.sqlite\' table="tbl" (geom)')
        self.assertEqual(tbl.type, "point")
