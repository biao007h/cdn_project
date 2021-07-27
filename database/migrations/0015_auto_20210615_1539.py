# Generated by Django 3.2.3 on 2021-06-15 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_auto_20210608_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='icon',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pages',
            name='target',
            field=models.CharField(default='_self', max_length=32),
        ),
        migrations.AlterField(
            model_name='node',
            name='work_or_no',
            field=models.CharField(choices=[('1', 'active'), ('0', 'inactive')], max_length=2),
        ),
    ]