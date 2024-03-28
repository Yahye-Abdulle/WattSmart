# Generated by Django 5.0.2 on 2024-03-28 02:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_chatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', models.ManyToManyField(related_name='conversation', to='api.chatmessage')),
                ('participants', models.ManyToManyField(related_name='conversations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
