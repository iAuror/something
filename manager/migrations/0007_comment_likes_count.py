# Generated by Django 3.1.3 on 2020-12-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_remove_commentlikes_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]