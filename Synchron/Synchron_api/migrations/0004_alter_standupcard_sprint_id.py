# Generated by Django 4.2.1 on 2023-06-14 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Synchron_api', '0003_remove_memberandremarks_standup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standupcard',
            name='sprint_id',
            field=models.IntegerField(unique=True),
        ),
    ]
