# Generated by Django 5.0 on 2024-01-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_file',
            field=models.FileField(blank=True, default='/placeholder.pdf', null=True, upload_to='product_files/'),
        ),
    ]
