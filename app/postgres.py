import logging

import pyodbc

from app.config import load_config


class PostgresDao:
    def __init__(self, section: str):
        self.mode = section[-3:].upper()
        self.config = load_config(section)
        self.schema = self.config.pop('schema')
        self.conn = None

    def open(self):
        self.conn = pyodbc.connect(**self.config, timeout=30)

    def close(self):
        if self.conn:
            self.conn.close()

    def log(self, query: str):
        logging.debug('PG ' + self.mode + ': ' + query)

    def create_table(self, table_name: str, columns_with_types: list):
        cur = self.conn.cursor()
        query = f'drop table if exists {self.schema}.{table_name}'
        self.log(query)
        cur.execute(query)
        columns_str = ','.join([column['name'] + ' ' + column['type'] for column in columns_with_types])
        query = f'create table if not exists {self.schema}.{table_name} ({columns_str})'
        self.log(query)
        cur.execute(query)
        self.conn.commit()

    def insert_data(self, table_name: str, column_names: list, data: tuple):
        cur = self.conn.cursor()
        columns = ','.join(column_names)
        args_str = '(' + ','.join(['?'] * len(column_names)) + ')'
        query = f'insert into {self.schema}.{table_name} ({columns}) values {args_str}'
        self.log(query)
        cur.executemany(query, data)
        self.conn.commit()
