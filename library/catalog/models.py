from datetime import date
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    
    first_name = models.CharField(
        max_length=100,
        verbose_name="prénom"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="nom",
    )
    date_of_birth = models.DateField(
        null=True, blank=True,
        verbose_name="date de naissance",
    )
    date_of_death = models.DateField(
        null=True, blank=True,
        verbose_name="date de décès",
    )

    class Meta:

        verbose_name = "Auteur"
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
        verbose_name="langue",
    )

    class Meta:

        verbose_name = "Langue"


    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(
        max_length=200,
        verbose_name="titre",
    )
    author = models.ForeignKey(
        'Author', on_delete=models.SET_NULL, null=True,
        verbose_name="auteur",
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Entrez un bref résumé du livre",
        verbose_name="résumé",
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
        verbose_name="langue",
    )

    class Meta:

        verbose_name = "Livre"


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.pk)])

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "genre(s)"


class BookInstance(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text="ID unique de cet exemplaire pour l'ensemble de la bibliothèque",
    )
    book = models.ForeignKey(
        'Book', on_delete=models.SET_NULL, null=True,
        verbose_name="livre",
    )
    imprint = models.CharField(
        max_length=200,
    )
    due_back = models.DateField(
        null=True, blank=True,
        verbose_name="date de retour",
    )
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Emprunteur",
    )

    LOAN_STATUS = (
        ('m', "En maintenance"),
        ('o', "Emprunté"),
        ('a', "Disponible"),
        ('r', "Réservé"),
    )
    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default='m',
        help_text="Disponibilité de l'exemplaire",
        verbose_name="statut",
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True

        return False

    class Meta:

        verbose_name = "Exemplaire"
        ordering = ['due_back']
        permissions = (
            ('can_mark_returned', 'Indiquer un exemplaire comme rapporté'),
        )


    def __str__(self):
        return f"{self.imprint} - {self.book.title}"
