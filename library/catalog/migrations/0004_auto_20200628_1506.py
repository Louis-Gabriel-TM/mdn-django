# Generated by Django 3.0.5 on 2020-06-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200531_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Exemplaire ramené'),), 'verbose_name': 'Exemplaire'},
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'En maintenance'), ('o', 'Emprunté'), ('a', 'Disponible'), ('r', 'Réservé')], default='m', help_text="Disponibilité de l'exemplaire", max_length=1, verbose_name='statut'),
        ),
    ]
