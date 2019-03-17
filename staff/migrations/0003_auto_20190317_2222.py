# Generated by Django 2.1.7 on 2019-03-17 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_auto_20190316_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='staffprofile',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='staff.Location', verbose_name='location'),
        ),
    ]
