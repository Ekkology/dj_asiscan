# Generated by Django 5.1 on 2024-11-18 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_usuarios', '0004_usergroupmembership'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserGroupMembership',
        ),
    ]
