# Generated by Django 3.2.3 on 2021-06-15 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_auto_20210615_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='href',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
    ]
