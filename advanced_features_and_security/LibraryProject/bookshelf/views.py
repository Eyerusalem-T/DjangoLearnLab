from django.shortcuts import render
from .forms import ExampleForm


def form_example(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})
