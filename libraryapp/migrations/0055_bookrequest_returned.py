# Generated by Django 4.2.3 on 2023-09-17 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0054_alter_bookrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrequest',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]