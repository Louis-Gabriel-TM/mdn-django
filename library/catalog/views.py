from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre, Language



def index(request):

    authors_count = Author.objects.all().count()
    books_count = Book.objects.all().count()
    instances_count = BookInstance.objects.all().count()

    available_instances_count = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'authors_count': authors_count,
        'books_count': books_count,
        'instances_count': instances_count,
        'available_instances_count': available_instances_count,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):

    model = Book
    paginate_by = 3

    def get_queryset(self):

        return Book.objects.all()[:5]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['additional_data'] = "Une donnée supplémentaire"

        return context


class BookDetailView(generic.DetailView):

    model = Book
