# Generated by Django 4.2.9 on 2024-01-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_alter_contact_phone_alter_contact_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='pincode',
            field=models.IntegerField(max_length=10, null=True),
        ),
    ]