# Generated by Django 4.2.1 on 2023-06-14 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Synchron_api', '0002_remove_memberandremarks_standup_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberandremarks',
            name='standup',
        ),
        migrations.AddField(
            model_name='memberandremarks',
            name='standup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Synchron_api.standupcard'),
            preserve_default=False,
        ),
    ]