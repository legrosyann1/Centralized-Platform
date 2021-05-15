# Generated by Django 3.1.6 on 2021-05-15 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_remove_change_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='old_info',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='futurechange',
            name='state',
            field=models.CharField(blank=True, choices=[('created', 'Created'), ('pending', 'Pending'), ('canceled', 'Canceled'), ('completed', 'Completed'), ('incompleted', 'Incompleted')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='inventory.device')),
            ],
        ),
    ]
