# Generated by Django 2.2.1 on 2019-09-29 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0009_auto_20190929_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=32, verbose_name='作者邮箱'),
        ),
    ]