from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Language


admin.AdminSite.site_title = "MDN Library"
admin.AdminSite.site_header = "Back Office de MDN Library"


class BookInstanceInline(admin.TabularInline):

    model = BookInstance
    extra = 0


class BookInline(admin.StackedInline):

    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = (
        'last_name', 'first_name', 'date_of_birth', 'date_of_death',
    )
    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death'),
    ]
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'author', 'display_genre',
    )
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = (
        'book', 'imprint', 'status', 'due_back',
    )
    list_filter = (
        'status', 'due_back',
    )
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'uuid',),
        }),
        ("Disponibilité", {
            'fields': ('status', 'due_back',),
        }),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):

    pass