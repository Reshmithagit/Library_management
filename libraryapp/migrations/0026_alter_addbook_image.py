# Generated by Django 4.2.3 on 2023-08-26 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0025_alter_addbook_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addbook',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]