# Generated by Django 3.2.3 on 2021-07-05 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_auto_20210705_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cname',
            name='cname',
            field=models.CharField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='work_or_no',
            field=models.CharField(choices=[('0', 'inactive'), ('1', 'active')], max_length=2),
        ),
    ]
