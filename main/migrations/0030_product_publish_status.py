# Generated by Django 5.0 on 2024-01-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_vendor_mobile_vendor_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publish_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
