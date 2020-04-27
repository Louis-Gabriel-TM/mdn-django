from django.shortcuts import render

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
