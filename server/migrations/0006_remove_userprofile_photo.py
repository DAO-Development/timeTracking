# Generated by Django 3.1.7 on 2021-09-22 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_userprofile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='photo',
        ),
    ]