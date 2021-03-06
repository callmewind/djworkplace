# Generated by Django 2.2.1 on 2019-08-03 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0011_auto_20190803_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leavetype',
            options={'ordering': ['name'], 'verbose_name': 'leave type', 'verbose_name_plural': 'leave types'},
        ),
        migrations.AddField(
            model_name='leave',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='leaves', to='holidays.LeaveType', verbose_name='type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
