# Generated by Django 4.2.9 on 2024-01-28 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_notifications_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='notif_for',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='notif_query',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='notif_subj',
        ),
    ]