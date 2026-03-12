import sys
import os
import importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test and point the books module to it."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_mark_read_cli(monkeypatch):
    # Ensure book_app is (re)loaded after DATA_FILE is set so its collection uses the temp file
    if "book_app" in sys.modules:
        importlib.reload(sys.modules["book_app"])
        import book_app
    else:
        import book_app

    # Add a book via the app's collection instance
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)

    # Invoke the CLI command with the title as an argument
    monkeypatch.setattr(sys, "argv", ["book_app.py", "mark-read", "Dune"])
    book_app.main()

    book = book_app.collection.find_book_by_title("Dune")
    assert book is not None
    assert book.read is True
