# Generated by Django 2.2.1 on 2019-06-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20190622_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcopy',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
