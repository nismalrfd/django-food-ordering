# Generated by Django 4.1.3 on 2023-02-10 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='instamojo_id',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
