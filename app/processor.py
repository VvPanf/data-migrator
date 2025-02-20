import logging

from threading import Thread
from app.mssql import MsSqlDao
from app.postgres import PostgresDao
from app.file_reader import get_tables


def get_start_process_thread(reports: list, dev_mode: bool, ift_mode: bool) -> Thread:
    return Thread(target=start_process, args=(reports, dev_mode, ift_mode))


def start_process(reports: list, dev_mode: bool, ift_mode: bool):
    global ms, pg_dev, pg_ift
    try:
        logging.info("================= START PROCESSING =================")
        # Создание объектов для БД
        ms = MsSqlDao('datasource.in.mssql')
        pg_dev = PostgresDao('datasource.out.postgres.dev')
        pg_ift = PostgresDao('datasource.out.postgres.ift')

        # Подключение к БД
        logging.info('Connecting to MS SQL Server')
        ms.open()
        if dev_mode:
            logging.info('Connection to GP DEV')
            pg_dev.open()
        if ift_mode:
            logging.info('Connection to GP IFT')
            pg_ift.open()

        # Пересылка данных
        for report in reports:
            logging.info(f'========== REPORT {report} ==========')
            report_tables = get_tables(f'{report}.txt')
            for table_str in report_tables:
                ms_table, pg_table = get_table_names(table_str)
                logging.info(f'-> Start process table {ms_table}')
                if not ms.check_table_exists(ms_table):
                    logging.error(f'Table {ms_table} not exists')
                    continue
                # Create table
                columns_result = ms.get_table_columns(ms_table)
                columns_with_types = [{'name': row[3], 'type': map_types(row[4], row[5])} for row in columns_result]
                if dev_mode:
                    pg_dev.create_table(pg_table, columns_with_types)
                if ift_mode:
                    pg_ift.create_table(pg_table, columns_with_types)
                logging.info(f'Table {pg_table} is created')
                # Insert data
                column_names = [col['name'] for col in columns_with_types]
                data = ms.select_data(ms_table, column_names)
                if dev_mode:
                    pg_dev.insert_data(pg_table, column_names, data)
                if ift_mode:
                    pg_ift.create_table(pg_table, columns_with_types)
                logging.info(f'Table {pg_table} is filled')
        logging.info("=== DONE! ===")
    except Exception as err:
        logging.error(err)

    finally:
        ms.close()
        if dev_mode:
            pg_dev.close()
        if ift_mode:
            pg_ift.close()


def get_table_names(table_str: str) -> tuple:
    return (table_str, table_str) if '|' not in table_str else tuple(table_str.split('|'))


def map_types(short_type: str, full_type: str) -> str:
    typedefs = {
        'bit': 'boolean',
        'datetime': 'timestamp',
        'tinyint': 'smallint'
    }
    replacement = typedefs.get(short_type)
    if replacement:
        return full_type.replace(short_type, replacement)
    return full_type
