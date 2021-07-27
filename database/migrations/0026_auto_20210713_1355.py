# Generated by Django 3.2.3 on 2021-07-13 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0025_subdomain_src_protocol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subdomain_src',
            name='protocol',
        ),
        migrations.AddField(
            model_name='subdomain_src',
            name='pre_proto',
            field=models.CharField(choices=[('1', 'http'), ('4', 'wss'), ('2', 'https'), ('3', 'ws')], default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subdomain_src',
            name='suf_proto',
            field=models.CharField(choices=[('1', 'http'), ('4', 'wss'), ('2', 'https'), ('3', 'ws')], default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='node',
            name='work_or_no',
            field=models.CharField(choices=[('0', 'inactive'), ('1', 'active')], max_length=2),
        ),
    ]