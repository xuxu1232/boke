# Generated by Django 2.2.1 on 2019-09-16 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0002_auto_20190912_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='作者性别'),
        ),
    ]
