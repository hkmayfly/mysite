# Generated by Django 2.2.1 on 2019-06-07 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_reader_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='reader_num',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
