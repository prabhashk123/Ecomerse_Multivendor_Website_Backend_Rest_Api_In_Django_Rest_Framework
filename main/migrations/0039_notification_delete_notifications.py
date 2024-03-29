# Generated by Django 4.2.9 on 2024-01-28 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_alter_notifications_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, null=True, verbose_name='message')),
                ('notif_created_time', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.owner')),
            ],
            options={
                'verbose_name_plural': '5. Notifications',
            },
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
    ]
