# Generated by Django 3.1.3 on 2020-12-22 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_auto_20201222_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmpbooks',
            name='published',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации'),
        ),
    ]