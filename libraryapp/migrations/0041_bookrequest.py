# Generated by Django 4.2.3 on 2023-09-07 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libraryapp', '0040_delete_bookrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=20)),
                ('issued', models.BooleanField(default=False)),
                ('penalty', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('issue_type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('reason', models.CharField(blank=True, choices=[('Damaged', 'Damaged'), ('Overdue', 'Overdue'), ('Lost', 'Lost')], max_length=20, null=True)),
                ('rental_period', models.PositiveIntegerField()),
                ('due_date', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.addbook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
