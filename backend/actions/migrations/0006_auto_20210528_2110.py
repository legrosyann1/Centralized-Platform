# Generated by Django 3.1.6 on 2021-05-28 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0005_auto_20210525_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='template',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='scheduledtask',
            name='title',
            field=models.CharField(choices=[('helloWorld', 'Hello World'), ('getWeeklyChanges', 'Weekly changes in all devices')], max_length=70),
        ),
    ]
