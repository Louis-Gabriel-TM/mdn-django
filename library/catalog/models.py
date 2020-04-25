import uuid

from django.db import models
from django.urls import reverse


class Author(models.Model):
    
    first_name = models.CharField(
        max_length=100,
    )
    last_name = models.CharField(
        max_length=100,
    )
    date_of_birth = models.DateField(
        null=True, blank=True,
    )
    date_of_death = models.DateField(
        "Died", null=True, blank=True,
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.pk)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Genre(models.Model):

    name = models.CharField(
        max_length=200,
        help_text="Entrez un genre litteréiare (e.g. Science-Fiction)",
    )

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(
        max_length=100, default="français",
        help_text="Entrez la langue dans laquelle est écrit le livre",
    )

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(
        max_length=200,
    )
    author = models.ForeignKey(
        'Author', on_delete=models.SET_NULL, null=True,
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Entrez un bref résumé du livre",
    )
    isbn = models.CharField(
        "ISBN", max_length=13,
        help_text="Entrez le No. ISBN (13 caractères)",
    )
    genre = models.ManyToManyField(
        Genre,
        help_text="Sélecionnez un genre littéraire",
    )
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.pk)])


class BookInstance(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text="ID unique de cet exemplaire pour l'ensemble de la bibliothèque",
    )
    book = models.ForeignKey(
        'Book', on_delete=models.SET_NULL, null=True,
    )
    imprint = models.CharField(
        max_length=200,
    )
    due_back = models.DateField(
        null=True, blank=True,
    )

    LOAN_STATUS = (
        ('m', "Maintenace"),
        ('o', "On loan"),
        ('a', "Available"),
        ('r', "Reserved"),
    )
    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default='m',
        help_text="Disponibilité de l'exemplaire",
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.uuid} - {self.book.title}"
