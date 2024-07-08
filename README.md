# Сервис по миграции данных


## Библиотеки
- pyodbc
- tkinter


## Конфигурация

Конфигурационный файл - `config.ini` cодержит 3 секции:
- `[datasource.in.mssql]` - исходная база данных MS SQL
- `[datasource.out.postgres.dev]` - результирующая база данных на DEV-стенде
- `[datasource.out.postgres.ift]` - результирующая база данных на IFT-стенде

Для каждой из баз доступны следующие параметры:
- `driver` - название драйвера можно найти в Поиск -> Источники данных ODBC -> Вкладка Драйверы
- `server` - адрес сервера
- `port` - порт
- `database` - название базы данных
- `uid` - имя пользователя
- `pwd` - пароль
- `schema` - схема

Пример заполнения:
```
[datasource.out.postgres.dev]
driver={Devart ODBC Driver for PostgreSQL}
server=localhost
port=5432
database=data-migrator-dev
uid=postgres
pwd=postgres
schema=test-dev-schema
```

В папку `reports` кладутся txt-файлы с названиями отчётов. Внутри файла перечисляются таблицы, которые нужны для отчёта. Пример:

Файл `my_report.txt`. Содержимое:
```
my_table_1
table_2
third_table
```

## Установка

Установка библиотек производится перед первым запуском открытием файла `install.bat`

## Запуск

Запуск производится открытием файла `run.bat`