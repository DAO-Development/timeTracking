# Generated by Django 3.1.7 on 2021-09-21 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20210921_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='objects',
            options={'verbose_name': 'Объект', 'verbose_name_plural': 'Объекты'},
        ),
        migrations.AlterField(
            model_name='client',
            name='logo_path',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Путь к логотипу'),
        ),
    ]
