# Generated by Django 2.0.6 on 2018-08-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20180810_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]
