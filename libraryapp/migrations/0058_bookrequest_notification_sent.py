# Generated by Django 4.2.3 on 2023-09-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0057_bookrequest_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrequest',
            name='notification_sent',
            field=models.BooleanField(default=False),
        ),
    ]
