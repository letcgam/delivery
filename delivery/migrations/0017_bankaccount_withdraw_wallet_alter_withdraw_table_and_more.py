# Generated by Django 5.0.4 on 2024-06-19 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0016_withdraw'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=255)),
                ('agency', models.IntegerField(max_length=4)),
                ('account', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'bank_account',
            },
        ),
        migrations.AddField(
            model_name='withdraw',
            name='wallet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.wallet'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='withdraw',
            table='withdraw',
        ),
        migrations.AddField(
            model_name='withdraw',
            name='bank_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.bankaccount'),
            preserve_default=False,
        ),
    ]