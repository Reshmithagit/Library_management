# Generated by Django 4.2.3 on 2023-09-14 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0050_remove_bookrequest_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrequest',
            name='additional_charges',
        ),
        migrations.RemoveField(
            model_name='bookrequest',
            name='reason',
        ),
    ]
