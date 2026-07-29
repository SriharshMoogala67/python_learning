class Book: 
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.status = "available" 

    def issue(self) -> bool: 
        if self.status == "Unavailable":
            print(f"{self.title} is already issued")
            return False 

        if self.status == "Missing":
            print(f"{self.title} is marked as missing")
            return False     
            
        self.status = "Unavailable"
        print(f"{self.title} issued successfully.")
        return True

    def return_book(self) -> bool:
        if self.status == "Available":
            print(f"{self.title} is already available.")
            return False

        if self.status == "Missing":
            print(f"{self.title} cannot be returned because it is marked missing.")
            return False

        self.status = "Available"
        print(f"{self.title} returned successfully.")
        return True


class Library: 
        def __init__(self, name: str): 
            self.name = name 
            self.books = []

        def add_book(self, book: Book) -> None:
            self.books.append(book)
            print(f"book {book.title} added to the library")
            
        def find_book(self, title: str) -> Book | None: 
            for book in self.books: 
                if book.title.lower == title.lower: 
                    return book

            return None

        def issue_book(self, title: str) -> bool:
            book = self.find_book(title)

            if book is None:
                print("Book not found.")
                return False

            return book.issue()

        def return_book(self, title: str) -> bool:
            book = self.find_book(title)

            if book is None:
                print("Book not found.")
                return False

            return book.return_book()

        def show_books(self) -> None:
            for index, book in enumerate(self.books, start=1):
                print(
                    index,
                    book.title,
                    "-",
                    book.author,
                    "-",
                    book.status,
                )
    

library = Library("City Library")

book1 = Book("Atomic Habits", "James Clear")
book2 = Book("The Alchemist", "Paulo Coelho")

library.add_book(book1)
library.add_book(book2)

library.show_books()

library.issue_book("Atomic Habits")
library.issue_book("Atomic Habits")

library.return_book("Atomic Habits")

library.show_books()