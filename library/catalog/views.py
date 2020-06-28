from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre, Language



def index(request):

    authors_count = Author.objects.all().count()
    books_count = Book.objects.all().count()
    instances_count = BookInstance.objects.all().count()

    available_instances_count = BookInstance.objects.filter(status__exact='a').count()

    visits_count = request.session.get('visits_count', 0)
    request.session['visits_count'] = visits_count + 1

    context = {
        'authors_count': authors_count,
        'books_count': books_count,
        'instances_count': instances_count,
        'available_instances_count': available_instances_count,
        'visits_count': visits_count,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):

    model = Book
    paginate_by = 3

    def get_queryset(self):

        return Book.objects.all()[:5]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # context['additional_data'] = "Une donnée supplémentaire"

        return context


class BookDetailView(generic.DetailView):

    model = Book


class AuthorListView(generic.ListView):

    model = Author
    paginate_by = 3

    def query_set(self):
        return Author.objects.all()[:5]


class AuthorDetailView(generic.DetailView):

    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = 'catalog/bookinstances_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books actually on loean (for librarians)."""

    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/borrowed_list.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')