# Generated by Django 5.0.4 on 2024-05-20 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_alter_product_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]