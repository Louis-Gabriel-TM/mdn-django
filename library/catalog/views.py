import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import RenewBookModelForm
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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all_borrowed'))

    else:  # request.method == 'GET' in general
        proposed_renewal_date = datetime.date.today() 
        proposed_renewal_date += datetime.timedelta(weeks=3)

        form = RenewBookModelForm(
            initial={'due_back': proposed_renewal_date}
        )

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


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


class AuthorCreate(PermissionRequiredMixin, generic.edit.CreateView):

    permission_required = 'catalog.can_mark_returned'
    model = Author

    fields ='__all__'
    initial = {
        'date_of_death': '01/01/2012',
    }


class AuthorUpdate(PermissionRequiredMixin, generic.edit.UpdateView):

    permission_required = 'catalog.can_mark_returned'
    model = Author

    fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death',
    ]


class AuthorDelete(PermissionRequiredMixin, generic.edit.DeleteView):

    permission_required = 'catalog.can_mark_returned'
    model = Author

    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, generic.edit.CreateView):

    permission_required = 'catalog.can_mark_returned'
    model = Book

    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, generic.edit.UpdateView):

    permission_required = 'catalog.can_mark_returned'
    model = Book

    fields = [
        'title',
        'author',
        'summary',
        'genre',
        'language',
    ]


class BookDelete(PermissionRequiredMixin, generic.edit.DeleteView):

    permission_required = 'catalog.can_mark_returned'
    model = Book

    success_url = reverse_lazy('books')