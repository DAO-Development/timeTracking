# Generated by Django 3.1.7 on 2021-11-11 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_remove_news_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientemployees',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='server.client', verbose_name='Фирма'),
        ),
        migrations.AlterField(
            model_name='objectcomments',
            name='object_comments_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='server.objectcomments', verbose_name='Родительский комментарий'),
        ),
        migrations.AlterField(
            model_name='objectcomments',
            name='user_profile_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.userprofile', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='objects',
            name='client_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='objects',
            name='contact_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.clientemployees', verbose_name='Контактное лицо'),
        ),
        migrations.AlterField(
            model_name='objectuser',
            name='objects_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.objects', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='objectuser',
            name='user_profile_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.userprofile', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='timereport',
            name='objects_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.objects', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='timereport',
            name='user_profile_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.userprofile', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='usercontracts',
            name='user_profile_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.userprofile', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='userdocuments',
            name='user_profile_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='server.userprofile', verbose_name='Сотрудник'),
        ),
    ]
