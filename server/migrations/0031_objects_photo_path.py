# Generated by Django 3.1.7 on 2022-02-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0030_auto_20220221_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='objects',
            name='photo_path',
            field=models.CharField(default='/objects/preview.jpg', max_length=250, verbose_name='Фото'),
        ),
    ]