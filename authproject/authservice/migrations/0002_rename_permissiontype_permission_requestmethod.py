# Generated by Django 3.2.9 on 2021-11-28 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authservice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='permissionType',
            new_name='requestMethod',
        ),
    ]
