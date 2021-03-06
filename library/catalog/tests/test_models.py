from django.test import TestCase

from catalog.models import Author


class Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='John', last_name='Doe')

    def test_first_name_label(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'prénom')

    def test_date_of_death(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, "date de décès")

    def test_first_name_length(self):
        author = Author.objects.get(pk=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(pk=1)
        expected_object_name = f"{author.last_name}, {author.first_name}"
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(pk=1)
        self.assertEquals(author.get_absolute_url(), '/catalog/authors/1')
