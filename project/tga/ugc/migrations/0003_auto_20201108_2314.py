# Generated by Django 3.1.3 on 2020-11-08 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0002_auto_20201108_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='ID пользователя'),
        ),
    ]
