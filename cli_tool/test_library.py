import pytest
from cli_tool.main import Library


@pytest.fixture
def temp_library(tmp_path):
    """Создаёт временную библиотеку с использованием временного файла."""
    temp_file = tmp_path / "temp_data.json"
    return Library(storage_file=str(temp_file))


def test_add_book(temp_library):
    """Тестирование добавления книги."""
    result = temp_library.add_book("Война и мир", "Толстой", 1869)
    assert "Книга 'Война и мир' добавлена с ID 1." in result
    assert len(temp_library.books) == 1
    assert temp_library.books[0].title == "Война и мир"


def test_remove_book(temp_library):
    """Тестирование удаления существующей книги."""
    temp_library.add_book("Гарри Поттер", "Дж.К. Роулинг", 1997)
    result = temp_library.remove_book(1)
    assert "Книга с ID 1 удалена." in result
    assert len(temp_library.books) == 0


def test_remove_nonexistent_book(temp_library):
    """Тестирование удаления несуществующей книги."""
    with pytest.raises(ValueError, match="Книга с ID 999 не найдена."):
        temp_library.remove_book(999)


def test_update_status(temp_library):
    """Тестирование обновления статуса книги."""
    temp_library.add_book("1984", "Джордж Оруэлл", 1949)
    result = temp_library.update_status(1, "в аренде")
    assert "Статус книги с ID 1 обновлён на 'в аренде'." in result
    assert temp_library.books[0].status == "в аренде"


def test_update_status_nonexistent_book(temp_library):
    """Тестирование обновления статуса несуществующей книги."""
    result = temp_library.update_status(999, "в аренде")
    assert "Книга с ID 999 не найдена." in result


def test_search_books(temp_library):
    """Тестирование поиска книг по критериям."""
    temp_library.add_book("Война и мир", "Толстой", 1869)
    temp_library.add_book("Анна Каренина", "Толстой", 1877)
    results = temp_library.search_books(["author=Толстой"])
    assert len(results) == 2
    assert all(book.author == "Толстой" for book in results)


def test_search_books_no_results(temp_library):
    """Тестирование поиска книг, которые не соответствуют критериям."""
    temp_library.add_book("Война и мир", "Толстой", 1869)
    results = temp_library.search_books(["author=Достоевский"])
    assert len(results) == 0


def test_display_books(temp_library):
    """Тестирование отображения списка книг."""
    temp_library.add_book("Гарри Поттер", "Дж.К. Роулинг", 1997)
    books = temp_library.display_books()
    assert len(books) == 1
    assert "Гарри Поттер" in books[0]


def test_display_books_empty_library(temp_library):
    """Тестирование отображения пустой библиотеки."""
    books = temp_library.display_books()
    assert len(books) == 1
    assert books[0] == "Библиотека пуста."
