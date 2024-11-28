#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from cli_tool.log.config import LoggingConfig


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    status: str = "в наличии"

    def __str__(self) -> str:
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"


class Library:
    def __init__(self, storage_file: str = "data.json"):
        self.storage_file = storage_file
        self.books: List[Book] = self._load_books()

    def _load_books(self) -> List[Book]:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_books(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump(
                [asdict(book) for book in self.books],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_book(self, title: str, author: str, year: int) -> str:
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self._save_books()
        return f"Книга '{title}' добавлена с ID {book_id}."

    def remove_book(self, book_id: int) -> str:
        book = self._find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self._save_books()
            return f"Книга с ID {book_id} удалена."
        raise ValueError(f"Книга с ID {book_id} не найдена.")

    def search_books(self, criteria: List[str]) -> List[Book]:
        results = self.books
        for criterion in criteria:
            field, value = criterion.split("=", 1)
            value = value.strip('"')
            results = [
                book
                for book in results
                if str(getattr(book, field)).lower() == value.lower()
            ]
        return results

    def display_books(self) -> List[str]:
        if not self.books:
            return ["Библиотека пуста."]
        return [str(book) for book in self.books]

    def update_status(self, book_id: int, status: str) -> str:
        book = self._find_book_by_id(book_id)
        if book:
            book.status = status
            self._save_books()
            return f"Статус книги с ID {book_id} обновлён на '{status}'."
        return f"Книга с ID {book_id} не найдена."

    def _find_book_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)


import logging
from cli_tool.log import configure_logging

logger = logging.getLogger(__name__)


def main():
    BASE_DIR = Path(__file__).parent.resolve()
    storage_file = os.path.join(BASE_DIR, "data.json")

    config = LoggingConfig()
    configure_logging(config)

    logger.info("Launch app", extra={"config": config})

    parser = argparse.ArgumentParser(
        description="Консольное приложение для управления библиотекой."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда add
    add_parser = subparsers.add_parser("add", help="Добавить книгу")
    add_parser.add_argument("--title", type=str, required=True, help="Название книги")
    add_parser.add_argument("--author", type=str, required=True, help="Автор книги")
    add_parser.add_argument("--year", type=int, required=True, help="Год издания книги")

    # Команда remove
    remove_parser = subparsers.add_parser("remove", help="Удалить книгу")
    remove_parser.add_argument("id", type=int, help="ID книги для удаления")

    # Команда search
    search_parser = subparsers.add_parser("search", help="Поиск книги")
    search_parser.add_argument(
        "criteria",
        nargs="+",
        type=str,
        help="Пара 'поле=значение' для поиска, например: title='Война и мир' author='Толстой'",
    )

    # Команда list
    subparsers.add_parser("list", help="Показать все книги")

    # Команда update
    update_parser = subparsers.add_parser("update", help="Обновить статус книги")
    update_parser.add_argument("id", type=int, help="ID книги")
    update_parser.add_argument("status", type=str, help="Новый статус книги")

    args = parser.parse_args()
    library = Library(storage_file)

    if args.command == "add":
        logger.info(
            library.add_book(title=args.title, author=args.author, year=args.year)
        )
    elif args.command == "remove":
        try:
            logger.info(library.remove_book(args.id))
        except ValueError as e:
            logger.warning(str(e))
        except Exception as e:
            logger.error(f"Неизвестная ошибка при удалении книги: {str(e)}")
    elif args.command == "search":
        results = library.search_books(args.criteria)
        if results:
            logger.info("\n".join(map(str, results)))
        else:
            logger.info("Книги не найдены.")
    elif args.command == "list":
        books = library.display_books()
        if books:
            logger.info("\n".join(books))
        else:
            logger.info("Библиотека пуста.")
    elif args.command == "update":
        logger.info(library.update_status(args.id, args.status))


if __name__ == "__main__":
    main()
