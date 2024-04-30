# Generated by Django 5.0.4 on 2024-04-30 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0009_adress_orderstatus_alter_order_status_productrating_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductComment',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='ProductRating',
            new_name='Rating',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='deliveryrecord',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='adress',
            table='adress',
        ),
        migrations.AlterModelTable(
            name='cart',
            table='cart',
        ),
        migrations.AlterModelTable(
            name='cartitem',
            table='cart_item',
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='deliveryrecord',
            table='delivery_record',
        ),
        migrations.AlterModelTable(
            name='driver',
            table='driver',
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
        migrations.AlterModelTable(
            name='orderitem',
            table='order_item',
        ),
        migrations.AlterModelTable(
            name='orderstatus',
            table='order_status',
        ),
        migrations.AlterModelTable(
            name='payment',
            table='payment',
        ),
        migrations.AlterModelTable(
            name='paymenttype',
            table='payment_type',
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
        migrations.AlterModelTable(
            name='rating',
            table='rating',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user_info',
        ),
        migrations.AlterModelTable(
            name='vehicle',
            table='vehicle',
        ),
        migrations.AlterModelTable(
            name='wishlist',
            table='wishlist',
        ),
    ]
