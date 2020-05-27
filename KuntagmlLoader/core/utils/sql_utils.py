import sqlite3

from . import logger
from .utils import tr

TABLES_TO_IGNORE = {
    'spatial_ref_sys',
    'spatialite_history',
    'sqlite_sequence',
    'geometry_columns',
    'spatial_ref_sys_aux',
    'views_geometry_columns',
    'virts_geometry_columns',
    'geometry_columns_statistics',
    'views_geometry_columns_statistics',
    'virts_geometry_columns_statistics',
    'geometry_columns_field_infos',
    'views_geometry_columns_field_infos',
    'virts_geometry_columns_field_infos',
    'geometry_columns_time',
    'geometry_columns_auth',
    'views_geometry_columns_auth',
    'virts_geometry_columns_auth',
    'sql_statements_log',
    'SpatialIndex',
    'ElementaryGeometries',
}


class SQLTable:

    def __init__(self, database: str, table: str, geom_col=None, geom_type=None):
        self.database = database
        self.table = table
        self.geom_col = geom_col
        self.geom_type = geom_type

    def has_geom(self):
        return self.geom_col is not None

    @property
    def name(self):
        name = self.table
        name += f' ({self.geom_col})' if self.has_geom() else ''
        return name

    @property
    def type(self) -> str:
        if self.geom_type == 1:
            return 'point'
        elif self.geom_type == 2:
            return 'line'
        elif self.geom_type == 3:
            return 'polygon'
        else:
            return ''

    @property
    def uri(self):
        uri = f'dbname=\'{self.database}\' table="{self.table}"'
        uri += f' ({self.geom_col})' if self.has_geom() else ''
        return uri

    def __str__(self) -> str:
        return self.uri + self.type


def get_non_empty_tables(database: str) -> [SQLTable]:
    """

    :param database:
    :return:
    """
    logger.debug(f'Opening db: {database}')
    con = sqlite3.connect(database)
    tables = []
    try:
        cur = con.cursor()
        cur.execute("""SELECT name FROM sqlite_master WHERE type = 'table'""")
        orig_tables = [row[0] for row in cur.fetchall() if
                       row[0] not in TABLES_TO_IGNORE and not row[0].startswith('idx')]
        cur.execute("""SELECT f_table_name, f_geometry_column, geometry_type FROM geometry_columns""")
        geom_tables = {}
        for row in cur.fetchall():
            geom_tables[row[0]] = geom_tables.get(row[0], [])
            geom_tables[row[0]].append((row[1], row[2]))

        for table in orig_tables:
            cur.execute("""SELECT COUNT(*) FROM %s""" % table)
            if cur.fetchone()[0] > 0:

                geom_defs = geom_tables.get(table, [(None, None)])

                # Some tables might contain several geometry columns
                for geom_def in geom_defs:
                    if geom_def[0] is not None:
                        cur.execute("""SELECT %s FROM %s LIMIT 1""" % (geom_def[0], table))
                        if cur.fetchone()[0] is None:
                            continue
                    tables.append(SQLTable(database, table, geom_def[0], geom_def[1]))


    except Exception as error:
        logger.exception(tr("Error occurred during database parsing"), error)
        tables = []
    finally:
        con.close()
        return tables
