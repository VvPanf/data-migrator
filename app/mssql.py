import logging

import pyodbc
from app.config import load_config


class MsSqlDao:
    def __init__(self, section: str):
        self.config = load_config(section)
        self.schema = self.config.pop('schema')
        self.conn = None

    def open(self):
        self.conn = pyodbc.connect(**self.config, timeout=120)

    def close(self):
        if self.conn:
            self.conn.close()

    def log(self, query: str):
        logging.debug('MS: ' + query)

    def check_table_exists(self, table_name: str) -> bool:
        cur = self.conn.cursor()
        # language=sql
        query = 'select table_name from information_schema.tables where table_schema = ? and table_name = ?'
        self.log(query)
        cur.execute(query, self.schema, table_name)
        return len(cur.fetchall()) != 0

    def get_table_columns(self, table_name: str) -> tuple:
        cur = self.conn.cursor()
        # language=sql
        query = """
        WITH q AS (
            SELECT
                c.TABLE_SCHEMA,
                c.TABLE_NAME,
                c.ORDINAL_POSITION,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                CASE
                    WHEN c.DATA_TYPE IN ( N'binary', N'varbinary'                    ) THEN ( CASE c.CHARACTER_OCTET_LENGTH   WHEN -1 THEN N'(max)' ELSE CONCAT( N'(', c.CHARACTER_OCTET_LENGTH  , N')' ) END )
                    WHEN c.DATA_TYPE IN ( N'char', N'varchar', N'nchar', N'nvarchar' ) THEN ( CASE c.CHARACTER_MAXIMUM_LENGTH WHEN -1 THEN N'(max)' ELSE CONCAT( N'(', c.CHARACTER_MAXIMUM_LENGTH, N')' ) END )
                    WHEN c.DATA_TYPE IN ( N'datetime2', N'datetimeoffset'            ) THEN CONCAT( N'(', c.DATETIME_PRECISION, N')' )
                    WHEN c.DATA_TYPE IN ( N'decimal', N'numeric'                     ) THEN CONCAT( N'(', c.NUMERIC_PRECISION , N',', c.NUMERIC_SCALE, N')' )
                END AS DATA_TYPE_PARAMETER,
                CASE c.IS_NULLABLE
                    WHEN N'NO'  THEN N' NOT NULL'
                    WHEN N'YES' THEN     N' NULL'
                END AS IS_NULLABLE2
            FROM
                INFORMATION_SCHEMA.COLUMNS AS c
        )
        SELECT
            q.TABLE_SCHEMA,
            q.TABLE_NAME,
            q.ORDINAL_POSITION,
            q.COLUMN_NAME,
            q.DATA_TYPE,
            CONCAT( q.DATA_TYPE, ISNULL( q.DATA_TYPE_PARAMETER, N'' ), q.IS_NULLABLE2 ) AS FULL_DATA_TYPE
        FROM
            q
        WHERE
            q.TABLE_SCHEMA = ? AND
            q.TABLE_NAME   = ?
        ORDER BY
            q.TABLE_SCHEMA,
            q.TABLE_NAME,
            q.ORDINAL_POSITION;
        """
        self.log('get columns info')
        cur.execute(query, self.schema, table_name)
        return cur.fetchall()

    def select_data(self, table_name: str, column_names: list):
        cur = self.conn.cursor()
        columns_str = ','.join(column_names)
        query = f'select {columns_str} from {self.schema}.{table_name}'
        self.log(query)
        cur.execute(query)
        return cur.fetchall()
