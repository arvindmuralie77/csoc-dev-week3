# Generated by Django 2.2.1 on 2019-06-18 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_ratings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ratings',
        ),
        migrations.AddField(
            model_name='book',
            name='number',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='book',
            name='totalRating',
            field=models.FloatField(default=0.0),
        ),
    ]
