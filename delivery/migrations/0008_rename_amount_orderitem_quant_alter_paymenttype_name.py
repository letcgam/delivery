# Generated by Django 5.0.4 on 2024-04-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_alter_user_adress_alter_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='amount',
            new_name='quant',
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]