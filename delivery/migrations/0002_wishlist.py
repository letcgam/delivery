# Generated by Django 5.0.4 on 2024-04-19 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_adicionado', models.DateTimeField(auto_now_add=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.product')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.user')),
            ],
        ),
    ]