import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import (
    Author,
    Book,
    BookInstance,
    Genre,
    Language,
)


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        nb_of_authors = 5

        for author_id in range(nb_of_authors):
            Author.objects.create(
                first_name=f'John {author_id}',
                last_name=f'Doe {author_id}',
            )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_three(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEquals(response.context['is_paginated'], True)
        self.assertEquals(len(response.context['author_list']), 3)

    def test_list_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEquals(response.context['is_paginated'], True)
        self.assertEquals(len(response.context['author_list']), 2)


class LoanedBooksByUserListView(TestCase):

    def setUp(self):
        test_user_1 = User.objects.create_user(
            username='testuser1', 
            password='1X<ISRUkw+tuK'
        )
        test_user_2 = User.objects.create_user(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        test_user_1.save()
        test_user_2.save()

        test_author = Author.objects.create(
            first_name="John",
            last_name="Doe",
        )
        test_genre = Genre.objects.create(
            name="Fantasy",
        )
        test_language = Language.objects.create(
            name="English",
        )
        test_book = Book.objects.create(
            title="Some book of John Doe",
            summary="A story by John Doe",
            isbn="1234567891234",
            author=test_author,
            language=test_language,
        )

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)        
        test_book.save()

        nb_of_book_copies = 30
        for book_copy in range(nb_of_book_copies):
            due_back = timezone.localtime(
                ) + datetime.timedelta(days=book_copy%5)
            borrower = test_user_1 if book_copy % 2 else test_user_2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint=f"SBJD{book_copy}",
                due_back=due_back,
                borrower=borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_borrowed'))
        self.assertRedirects(
            response, 
            '/accounts/login/?next=/catalog/mybooks/'
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')

    def test_logged_in_uses_correct_template(self):
        self.client.login(
            username="testuser1",
            password='1X<ISRUkw+tuK',
        )
        response = self.client.get(reverse('my_borrowed'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), "testuser1")
        self.assertTemplateUsed(
            response, 
            'catalog/bookinstances_list_borrowed_user.html'
        )