# Generated by Django 3.2.22 on 2023-10-14 08:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
