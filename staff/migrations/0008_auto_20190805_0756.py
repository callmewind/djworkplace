# Generated by Django 2.2.4 on 2019-08-05 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='name'),
        ),
    ]