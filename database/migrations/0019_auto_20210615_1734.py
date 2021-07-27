# Generated by Django 3.2.3 on 2021-06-15 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_auto_20210615_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='href',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='node',
            name='work_or_no',
            field=models.CharField(choices=[('0', 'inactive'), ('1', 'active')], max_length=2),
        ),
        migrations.AlterField(
            model_name='pages',
            name='icon',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
