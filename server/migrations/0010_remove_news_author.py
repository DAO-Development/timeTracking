# Generated by Django 3.1.7 on 2021-10-20 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20211017_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='author',
        ),
    ]