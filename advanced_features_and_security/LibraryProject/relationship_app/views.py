from django.shortcuts import render, redirect,  get_object_or_404

# Create your views here.
from .models import Book, Library
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

def list_bookd(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model= Library
    template_name= "library_detail.html"
    context_object_name = "library"



# -------- Role check functions --------

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# -------- Views --------

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')


# ---------- Login View ----------
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# ---------- Logout View ----------
class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

# ---------- Registration View ----------
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'relationship_app/register.html', {'form': form})

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        year = request.POST.get('publication_year')

        Book.objects.create(
            title=title,
            author_id=author_id,
            publication_year=year
        )
        return redirect('list_books')

    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get('title')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('list_books')

    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect('list_books')

    return render(request, 'relationship_app/delete_book.html', {'book': book})
