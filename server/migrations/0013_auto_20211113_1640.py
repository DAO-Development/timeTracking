# Generated by Django 3.1.7 on 2021-11-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_auto_20211111_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='create_date',
            field=models.DateField(null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='news',
            name='create_date',
            field=models.DateField(null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='objects',
            name='create_date',
            field=models.DateField(null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='create_date',
            field=models.DateField(null=True, verbose_name='Дата создания'),
        ),
    ]