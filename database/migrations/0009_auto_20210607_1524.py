# Generated by Django 3.2.3 on 2021-06-07 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20210607_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='work_or_no',
            field=models.CharField(choices=[('0', 'inactive'), ('1', 'active')], max_length=2),
        ),
        migrations.AlterField(
            model_name='user2role',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user', to_field='user_name'),
        ),
    ]