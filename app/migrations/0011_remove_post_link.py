# Generated by Django 3.1.3 on 2022-12-30 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_post_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='link',
        ),
    ]
