from typing import List, Tuple, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from books import Book


def print_menu() -> None:
    """Display the main menu to the user."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> int:
    """Prompt the user for a menu choice (1-5). Re-prompts until a valid integer in range is provided.

    Returns:
        int: The chosen menu option as an integer between 1 and 5 inclusive.
    """
    while True:
        choice_str: str = input("Choose an option (1-5): ").strip()
        if not choice_str:
            print("No input provided. Please enter a number between 1 and 5.")
            continue
        if not choice_str.isdigit():
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        choice = int(choice_str)
        if 1 <= choice <= 5:
            return choice
        print("Choice out of range. Please enter a number between 1 and 5.")


def get_book_details() -> Tuple[str, str, Optional[int]]:
    """Prompt the user for book details and return (title, author, year).

    Title and author are required and will re-prompt until non-empty. Year is optional; the user
    may leave it blank to indicate unknown publication year. Non-numeric years will re-prompt.
    """
    while True:
        title: str = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a valid title.")

    while True:
        author: str = input("Enter author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please enter a valid author name.")

    while True:
        year_input: str = input("Enter publication year (leave blank if unknown): ").strip()
        if not year_input:
            year: Optional[int] = None
            break
        try:
            year = int(year_input)
            break
        except ValueError:
            print("Invalid year. Please enter a numeric year (e.g. 1999) or leave blank.")

    return title, author, year


def print_books(books: List['Book']) -> None:
    """Print a numbered list of books."""
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status: str = "✅ Read" if getattr(book, 'read', False) else "📖 Unread"
        year_display = getattr(book, 'year', 'Unknown') if getattr(book, 'year', None) is not None else 'Unknown'
        print(f"{index}. {book.title} by {book.author} ({year_display}) - {status}")
