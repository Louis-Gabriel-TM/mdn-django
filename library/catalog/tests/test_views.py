from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


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
