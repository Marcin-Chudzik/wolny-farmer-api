# Generated by Django 4.2.1 on 2023-05-27 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_post_author_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default='27-05-2023'),
        ),
    ]