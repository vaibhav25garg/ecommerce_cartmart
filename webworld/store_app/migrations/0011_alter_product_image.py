# Generated by Django 5.0.1 on 2024-02-07 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0010_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='store.Product_images.img'),
        ),
    ]
