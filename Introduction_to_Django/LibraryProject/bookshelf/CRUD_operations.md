from bookshelf.models import Book
book = Book.objects.create(title = "1984",author="George orwell", publication_year=1949)
books = Book.objects.all()
print (books)

book.title = "Nineteeen Eighty-Four"
book.save()
book.delete()
