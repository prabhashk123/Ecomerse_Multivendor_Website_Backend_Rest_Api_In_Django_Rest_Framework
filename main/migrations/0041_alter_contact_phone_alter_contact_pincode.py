# Generated by Django 4.2.9 on 2024-01-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.IntegerField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='pincode',
            field=models.IntegerField(max_length=6, null=True),
        ),
    ]
