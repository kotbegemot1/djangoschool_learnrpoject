# Generated by Django 3.2.7 on 2023-04-19 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_rename_fess_in_world_movie_fees_in_world'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='foto_of_reviewer/', verbose_name='Фото'),
        ),
    ]