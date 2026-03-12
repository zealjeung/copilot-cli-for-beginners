import sys
from books import BookCollection


# Global collection instance
collection = BookCollection()


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_search():
    """Search books with optional filters provided as argv flags.

    Supported flags:
      --title <substring>
      --author <substring>
      --year <int>
      --read <true|false>

    Example:
      python book_app.py search --author "Tolkien" --read true
    """
    # Simple manual parsing to avoid adding argparse as a dependency in this small sample
    args = sys.argv[2:]
    title = None
    author = None
    year = None
    read = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif arg == "--author" and i + 1 < len(args):
            author = args[i + 1]
            i += 2
        elif arg == "--year" and i + 1 < len(args):
            try:
                year = int(args[i + 1])
            except ValueError:
                print("Invalid year provided; ignoring year filter.")
                year = None
            i += 2
        elif arg == "--read" and i + 1 < len(args):
            val = args[i + 1].lower()
            if val in ("true", "t", "yes", "1"):
                read = True
            elif val in ("false", "f", "no", "0"):
                read = False
            else:
                print("Invalid read value; expected true/false. Ignoring read filter.")
                read = None
            i += 2
        else:
            # Skip unknown tokens
            i += 1

    results = collection.search(title=title, author=author, year=year, read=read)
    show_books(results)


def handle_mark():
    """Mark a book as read.

    If a title is provided as the second CLI argument it will be used; otherwise the
    user is prompted to enter a title interactively.
    """
    print("\nMark a Book as Read\n")

    # Accept title as an argument for non-interactive usage
    if len(sys.argv) >= 3:
        title = " ".join(sys.argv[2:]).strip()
    else:
        title = input("Enter the title of the book to mark as read: ").strip()

    if not title:
        print("No title provided. Aborting.")
        return

    success = collection.mark_as_read(title)
    if success:
        print(f"\nMarked '{title}' as read.\n")
    else:
        print(f"\nBook titled '{title}' not found in collection.\n")


def show_help():
    print("""
Book Collection Helper

Commands:
  list       - Show all books
  add        - Add a new book
  remove     - Remove a book by title
  find       - Find books by author
  mark-read  - Mark a book as read
  help       - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "mark-read":
        handle_mark()
    elif command == "search" or command == "filter":
        handle_search()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
