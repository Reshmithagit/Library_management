# Generated by Django 4.2.3 on 2023-08-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0004_remove_category_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='addbook',
            name='language',
            field=models.CharField(default='Malayalam', max_length=20),
        ),
    ]
