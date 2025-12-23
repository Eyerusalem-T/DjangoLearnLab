
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    form = ExampleForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect("book_list")

    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect("book_list")
