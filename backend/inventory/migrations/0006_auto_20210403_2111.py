# Generated by Django 3.1.6 on 2021-04-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210403_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logicpartition',
            name='name',
            field=models.CharField(blank=True, default=[], max_length=100),
            preserve_default=False,
        ),
    ]
