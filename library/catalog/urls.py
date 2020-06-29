from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('borrowed/', views.LoanedBooksListView.as_view(), name='all_borrowed'),
    path(
        'authors/<int:pk>', views.AuthorDetailView.as_view(), 
        name='author_detail',
    ),
    path(
        'authors/create/', views.AuthorCreate.as_view(),
        name='author_create',
    ),
    path(
        'authors/<int:pk>/update', views.AuthorUpdate.as_view(),
        name='author_update',
    ),
    path(
        'authors/<int:pk>/delete', views.AuthorDelete.as_view(),
        name='author_delete',
    ),
    path(
        'books/<int:pk>', views.BookDetailView.as_view(), 
        name='book_detail'),
    path(
        'books/<uuid:pk>/renew/', views.renew_book_librarian, 
        name='renew_book_librarian',
    ),
    path(
        'mybooks/', views.LoanedBooksByUserListView.as_view(), 
        name='my_borrowed',
    ),
]
