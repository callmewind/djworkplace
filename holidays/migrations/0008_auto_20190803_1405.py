# Generated by Django 2.2.1 on 2019-08-03 14:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('holidays', '0007_auto_20190707_2032'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vacation',
            new_name='Leave',
        ),
    ]
