# Generated by Django 4.2.9 on 2024-01-28 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_remove_notifications_notif_for_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='message',
            field=models.CharField(max_length=200, null=True, verbose_name='message'),
        ),
    ]
