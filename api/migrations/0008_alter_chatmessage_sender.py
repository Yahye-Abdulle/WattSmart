# Generated by Django 5.0.2 on 2024-03-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='sender',
            field=models.CharField(max_length=100),
        ),
    ]
