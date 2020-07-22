import os

from ..core.utils.sql_utils import SQLTable, get_non_empty_tables


def test_getting_tables(new_project) -> None:
    db = os.path.join(os.path.dirname(__file__), "testdata", "test.sqlite")
    tables = get_non_empty_tables(db)
    assert len(tables) == 5


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
