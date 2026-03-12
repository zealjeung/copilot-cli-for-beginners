import sys
import os
import importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_search_by_title():
    import book_app
    book_app.collection.add_book("The Lord of the Rings", "J.R.R. Tolkien", 1954)
    book_app.collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    results = book_app.collection.search(title="lord")
    assert len(results) == 1
    assert results[0].title == "The Lord of the Rings"


def test_search_by_author_and_read():
    import book_app
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    book_app.collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    book_app.collection.mark_as_read("Dune")

    results = book_app.collection.search(author="frank", read=True)
    assert len(results) == 1
    assert results[0].title == "Dune"


def test_cli_search_filters(monkeypatch):
    # Reload to ensure collection uses temp DATA_FILE
    importlib.reload(sys.modules.get("book_app", importlib.import_module("book_app")))
    import book_app

    book_app.collection.add_book("1984", "George Orwell", 1949)
    book_app.collection.add_book("Animal Farm", "George Orwell", 1945)

    monkeypatch.setattr(sys, "argv", ["book_app.py", "search", "--author", "Orwell", "--year", "1949"])
    book_app.main()

    results = book_app.collection.search(author="Orwell", year=1949)
    assert len(results) == 1
    assert results[0].title == "1984"
