# Generated by Django 5.1 on 2024-11-03 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='user_form',
            new_name='user_from',
        ),
    ]
