# Generated by Django 2.0.6 on 2018-06-27 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumptious', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]