import datetime
import uuid

from django.contrib.auth.models import User, Permission
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


class LoanedBooksByUserListViewTest(TestCase):

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

        Genre.objects.create(
            name="Fantasy",
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

    def test_only_borrowed_book_in_list(self):
        self.client.login(
            username="testuser1",
            password='1X<ISRUkw+tuK',
        )
        response = self.client.get(reverse('my_borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()

        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)

        for bookinstance in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookinstance.borrower)
            self.assertEqual(bookinstance.status, 'o')

    def test_pages_ordered_by_due_date(self):
        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        self.client.login(
            username="testuser1",
            password='1X<ISRUkw+tuK',
        )
        response = self.client.get(reverse('my_borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['bookinstance_list']), 3)

        last_date = 0
        for bookinstance in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = bookinstance.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back

class RenewBookInstanceViewTest(TestCase):

    def setUp(self):
        test_user_1 = User.objects.create_user(
            username='testuser1', 
            password='1X<ISRUkw+tuK'
        )
        test_user_2 = User.objects.create_user(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        permission = Permission.objects.get(
            name="Indiquer un exemplaire comme rapporté"
        )
        test_user_2.user_permissions.add(permission)

        test_user_1.save()
        test_user_2.save()

        test_author = Author.objects.create(
            first_name="John",
            last_name="Doe",
        )
        Genre.objects.create(
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

        Genre.objects.create(
            name="Fantasy",
        )
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)        
        test_book.save()

        due_back = datetime.date.today() + datetime.timedelta(weeks=1)
        self.test_bookinstance_1 = BookInstance.objects.create(
            book=test_book,
            imprint="SBJD1",
            due_back=due_back,
            borrower=test_user_1,
            status='o',
        )
        self.test_bookinstance_2 = BookInstance.objects.create(
            book=test_book,
            imprint="SBJD2",
            due_back=due_back,
            borrower=test_user_2,
            status='o',
        )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(
            'renew_book_librarian',
            kwargs={'pk': self.test_bookinstance_1.pk},
        ))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_but_without_correct_permission(self):
        self.client.login(
            username='testuser1', 
            password='1X<ISRUkw+tuK'
        )
        response = self.client.get(reverse(
            'renew_book_librarian', kwargs={'pk': self.test_bookinstance_1.pk},
        ))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_permission_for_own_borrowed_book(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        response = self.client.get(reverse(
            'renew_book_librarian', kwargs={'pk': self.test_bookinstance_2.pk},
        ))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_for_another_user_borrowed_book(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        response = self.client.get(reverse(
            'renew_book_librarian', kwargs={'pk': self.test_bookinstance_1.pk},
        ))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged(self):
        test_uuid = uuid.uuid4()

        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        response = self.client.get(reverse(
            'renew_book_librarian', kwargs={'pk': test_uuid}
        ))
        self.assertEqual(response.status_code, 404)

    def test_use_correct_template(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        response = self.client.get(reverse(
            'renew_book_librarian', kwargs={'pk': self.test_bookinstance_1.pk},
        ))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_set_three_weeks_in_future(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        response = self.client.get(reverse(
            'renew_book_librarian', kwargs={'pk': self.test_bookinstance_1.pk},
        ))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today(
            ) + datetime.timedelta(weeks=3)
        self.assertEqual(
            response.context['form'].initial['due_back'],
            date_3_weeks_in_future,
        )

    def test_redirects_to_all_borrowed_books_list_on_success(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        valid_date_in_future = datetime.date.today(
            ) + datetime.timedelta(weeks=2)
        response = self.client.post(
            reverse(
                'renew_book_librarian', 
                kwargs={'pk': self.test_bookinstance_1.pk},
            ),
            {'due_back': valid_date_in_future},
        )
        self.assertRedirects(response, reverse('all_borrowed'))

    def test_form_invalid_renewal_date_past(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        date_in_past = datetime.date.today(
            ) - datetime.timedelta(days=1)
        response = self.client.post(
            reverse(
                'renew_book_librarian', 
                kwargs={'pk': self.test_bookinstance_1.pk},
            ),
            {'due_back': date_in_past},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'due_back',
            "Date invalide - date passée",
        )

    def test_form_invalid_renewal_date_future(self):
        self.client.login(
            username='testuser2', 
            password='2HJ1vRV0Z&3iD'
        )
        date_in_past = datetime.date.today(
            ) + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        response = self.client.post(
            reverse(
                'renew_book_librarian', 
                kwargs={'pk': self.test_bookinstance_1.pk},
            ),
            {'due_back': date_in_past},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'due_back',
            "Date invalide - date dans plus de 4 semaines",
        )
