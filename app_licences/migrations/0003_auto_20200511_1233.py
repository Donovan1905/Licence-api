# Generated by Django 3.0.6 on 2020-05-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_licences', '0002_auto_20200510_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='key',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]