# Generated by Django 3.2.3 on 2021-06-01 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20210601_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='remark',
            field=models.CharField(max_length=32, null=True),
        ),
    ]