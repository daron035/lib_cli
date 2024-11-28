# Library Management System

Консольное приложение для управления библиотекой книг.

## Функционал

- **Добавление книги**: ввод title, author, year.
- **Удаление книги**: ввод ID.
- **Поиск книги**: поиск по title, author, year.
- **Вывод всех книг**.
- **Изменение статуса**: изменение на "в наличии" или "выдана".

## Установка

```bash
git clone https://github.com/daron035/lib_cli.git
cd lib_cli
pip install dist/cli_tool-0.1.0-py3-none-any.whl
```

## Примеры использования

```bash
mycli add --title "Война и мир" --author "Лев Толстой" --year 1869
mycli search title="война и мир"
mycli update 1 "выдана"
mycli list
mycli remove <id>

# тесты
pytest cli_tool/test_library.py
```
