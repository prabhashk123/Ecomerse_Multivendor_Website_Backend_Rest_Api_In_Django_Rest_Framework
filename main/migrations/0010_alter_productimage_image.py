# Generated by Django 5.0 on 2023-12-27 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to='product_imgs/'),
        ),
    ]
