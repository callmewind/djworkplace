# Generated by Django 2.2.4 on 2019-12-10 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_auto_20190805_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='staff', to='staff.Department', verbose_name='department'),
        ),
    ]