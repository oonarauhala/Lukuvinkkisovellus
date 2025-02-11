from sqlalchemy import exc


class BookRepository:
    def __init__(self, db):
        self._db = db

    def add_book(self, book, user_id):
        """
        Adds Book-object to database and links it to current user with id.

        Args:
            book (Book): Book-object to be added
            user_id (Integer): Id of the user adding the book.

        Returns:
            Boolen: True if successful.
        """
        try:
            author = book.get_author()
            title = book.get_title()
            isbn = book.get_isbn()
            description = book.get_description()
            sql = "INSERT INTO books (author, title, description, type, isbn, user_id) \
                    VALUES (:author, :title, :description, 'Book', :isbn, :user_id)"
            self._db.session.execute(
                sql, {"author": author, "title": title, "description": description, "isbn": isbn, "user_id": user_id})
            self._db.session.commit()
            return True
        except:
            return False

    def mark_finished(self, book_id):
        """
        Adds timestamp to the marked_read field on the row of this book-id.

        Args:
            book_id (Integer): Id of the book to be marked finished.

        Returns:
            Boolean: True, if marking was successful.
        """
        try:
            sql = "UPDATE books SET marked_read=NOW() WHERE id=:book_id"
            self._db.session.execute(sql, {"id": book_id})
            self._db.session.commit()
            return True
        except:
            return False

    def is_owner(self, user_id, book_id):
        """
        Checks if the user-id and the book-id are in the same row in the database.

        Args:
            user_id (Integer): User-id of the currently logged in user.
            book_id (Integer): Book-id of the book to be checked.

        Returns:
            Boolean: True if logged user and book-id matches.
        """
        try:
            sql = "SELECT * FROM books WHERE user_id=:user_id AND id=:book_id"
            result = self._db.session.execute(sql, {"user_id": user_id, "book_id": book_id})
            if result.fetchone() is not None:
                return True
            else:
                return False
        except:
            return False

    def get_book(self, book_id):
        try:
            sql = "SELECT * FROM books WHERE id=:book_id"
            result = self._db.session.execute(sql, {"book_id": book_id})
            return result.fetchone()
        except:
            return None

    def update_book(self, author, title, description, isbn, book_id):
        try:
            sql = "UPDATE books SET author=:author, title=:title, description=:description, isbn=:isbn WHERE id=:book_id"
            self._db.session.execute(sql, {"author": author, "title": title, "description": description, "isbn": isbn, "book_id": book_id})
            self._db.session.commit()
            return True
        except:
            return False

    def get_users_books(self, user_id):
        """
        Gets all added books by the given user-id.

        Args:
            user_id (Integer): Id of the user whose books will be retrieved.

        Returns:
            List(Tuple): List of books found. If no books were found, return None.
        """
        try:
            sql = "SELECT * FROM books WHERE user_id=:user_id"
            result = self._db.session.execute(sql, {"user_id": user_id})
            return result.fetchall()
        except:
            return None

    def mark_finished(self, book_id):
        try:
            sql = "UPDATE books SET marked_read=NOW() WHERE id=:book_id"
            self._db.session.execute(sql, {"book_id": book_id})
            self._db.session.commit()
            return True
        except:
            return False

