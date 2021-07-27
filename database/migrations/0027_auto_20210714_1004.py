# Generated by Django 3.2.3 on 2021-07-14 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0026_auto_20210713_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdomain_src',
            name='pre_port',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subdomain_src',
            name='suf_port',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subdomain_src',
            name='pre_proto',
            field=models.CharField(choices=[('1', 'http'), ('2', 'https'), ('4', 'wss'), ('3', 'ws')], max_length=2),
        ),
        migrations.AlterField(
            model_name='subdomain_src',
            name='suf_proto',
            field=models.CharField(choices=[('1', 'http'), ('2', 'https'), ('4', 'wss'), ('3', 'ws')], max_length=2),
        ),
    ]
