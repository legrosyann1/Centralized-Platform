# Generated by Django 3.1.6 on 2021-05-11 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20210502_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='old_info',
            field=models.JSONField(null=True),
        ),
    ]