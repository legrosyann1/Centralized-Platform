# Generated by Django 3.1.6 on 2021-05-02 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210502_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='futurechange',
            old_name='executor',
            new_name='implementer',
        ),
        migrations.RenameField(
            model_name='futurechange',
            old_name='requestor',
            new_name='requester',
        ),
    ]
