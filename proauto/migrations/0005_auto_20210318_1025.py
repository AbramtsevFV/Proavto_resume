# Generated by Django 3.1.6 on 2021-03-18 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proauto', '0004_auto_20210310_1548'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auto',
            options={'verbose_name': 'Модели автомобилей', 'verbose_name_plural': 'Модели автомобилей'},
        ),
        migrations.AlterModelOptions(
            name='brend',
            options={'verbose_name': 'Производители автомобилей', 'verbose_name_plural': 'Производители автомобилей'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'Главное мню', 'verbose_name_plural': 'Главное мню'},
        ),
        migrations.AddField(
            model_name='auto',
            name='production_date',
            field=models.IntegerField(default=1960, verbose_name='Год начала производства'),
            preserve_default=False,
        ),
    ]