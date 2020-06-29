from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('borrowed/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
    path(
        'authors/<int:pk>', views.AuthorDetailView.as_view(), 
        name='author-detail',
    ),
    path(
        'books/<int:pk>', views.BookDetailView.as_view(), 
        name='book-detail'),
    path(
        'books/<uuid:pk>/renew/', views.renew_book_librarian, 
        name='renew-book-librarian',
    ),
    path(
        'mybooks/', views.LoanedBooksByUserListView.as_view(), 
        name='my-borrowed',
    ),
]
