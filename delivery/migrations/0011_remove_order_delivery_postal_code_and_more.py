# Generated by Django 5.0.4 on 2024-04-30 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_rename_productcomment_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_postal_code',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_adress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.adress'),
        ),
        migrations.CreateModel(
            name='BillingAdress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.adress')),
            ],
        ),
    ]