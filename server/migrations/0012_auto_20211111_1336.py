# Generated by Django 3.1.7 on 2021-11-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_auto_20211111_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AddField(
            model_name='clientemployees',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
