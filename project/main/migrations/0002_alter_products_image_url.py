# Generated by Django 4.0.2 on 2023-07-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image_url',
            field=models.URLField(max_length=100000),
        ),
    ]
