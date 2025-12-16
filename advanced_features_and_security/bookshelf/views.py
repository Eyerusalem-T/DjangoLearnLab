
from django.shortcuts import render
from .models import Book
from .forms import BookForm



def book_list(request):
    books = Book.objects.all()  # ORM prevents SQL injection
    return render(request, 'bookshelf/book_list.html', {'books': books})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():   # input validation
            form.save()
    else:
        form = BookForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})

