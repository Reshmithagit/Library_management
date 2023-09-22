# Generated by Django 4.2.3 on 2023-09-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0053_alter_bookrequest_overdue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]