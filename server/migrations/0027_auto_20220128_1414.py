# Generated by Django 3.1.7 on 2022-01-28 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0026_calendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='color',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='end',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата и время конца'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='start',
            field=models.DateTimeField(verbose_name='Дата и время начала'),
        ),
    ]
