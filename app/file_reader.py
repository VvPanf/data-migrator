import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
REPORTS_FOLDER = os.path.join(ROOT_DIR, 'reports')


def get_folder_files() -> list:
  # Возвращает список файлов
  return os.listdir(REPORTS_FOLDER)


def get_tables(filename: str):
  # Возвращает таблицы из файла
  with open(os.path.join(REPORTS_FOLDER, filename), 'r') as file:
    lines = [line for line in (l.strip() for l in file) if line]
    return lines
