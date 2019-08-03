# Generated by Django 2.2.1 on 2019-08-03 14:36

from django.db import migrations

leave_types = [
    { 'name':'Vacaciones', 'icon':'☀️',},
    { 'name':'Permiso retribuido', 'icon':'⌛',},
]

def create_leave_types(apps, schema_editor):
    LeaveType = apps.get_model('holidays', 'LeaveType')
    for leave_type in leave_types:
        LeaveType.objects.create(**leave_type)

def remove_leave_types(apps, schema_editor):
    LeaveType = apps.get_model('holidays', 'LeaveType')
    for leave_type in leave_types:
        LeaveType.objects.filter(name=leave_type['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0010_auto_20190803_1435'),
    ]

    operations = [
        migrations.RunPython(create_leave_types, remove_leave_types),
    ]
