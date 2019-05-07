# Generated by Django 2.2 on 2019-05-07 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20190507_2135'),
        ('holidays', '0004_auto_20190507_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicHoliday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('yearly', models.BooleanField(verbose_name='yearly')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.Location', verbose_name='location')),
            ],
            options={
                'verbose_name': 'public holiday',
                'verbose_name_plural': 'public holidays',
                'ordering': ['yearly', '-date'],
            },
        ),
    ]
