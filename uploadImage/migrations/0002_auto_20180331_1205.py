# Generated by Django 2.0.2 on 2018-03-31 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadImage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='numberOfDownload',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='numberOfView',
            field=models.IntegerField(default=0),
        ),
    ]
