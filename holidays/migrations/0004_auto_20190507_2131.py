# Generated by Django 2.2 on 2019-05-07 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('holidays', '0003_auto_20190507_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(verbose_name='start')),
                ('end', models.DateField(verbose_name='end')),
                ('approval_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vacation_approvals', to=settings.AUTH_USER_MODEL, verbose_name='approved by')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'vacations',
                'verbose_name_plural': 'vacations',
                'ordering': ['-start', '-end'],
            },
        ),
        migrations.DeleteModel(
            name='Holiday',
        ),
    ]
