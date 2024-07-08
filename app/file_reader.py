import os

folder = './reports'

def get_folder_files() -> list:
  # Возвращает список файлов
  return os.listdir(folder)


def get_tables(filename: str):
  # Возвращает таблицы из файла
  with open(folder + '/' + filename, 'r') as file:
    lines = [line for line in (l.strip() for l in file) if line]
    return lines
