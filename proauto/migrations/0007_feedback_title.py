# Generated by Django 3.1.6 on 2021-03-29 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proauto', '0006_auto_20210329_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='title',
            field=models.CharField(default=1, max_length=50, verbose_name='Тема обрщения'),
            preserve_default=False,
        ),
    ]
