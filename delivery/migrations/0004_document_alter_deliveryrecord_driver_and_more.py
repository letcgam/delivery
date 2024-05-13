# Generated by Django 5.0.4 on 2024-05-13 20:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_remove_user_adress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('SSN', 'Social Security Number'), ('EIN', 'Employer Identification Number')], max_length=30)),
                ('number', models.CharField(max_length=50, unique=True)),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField()),
            ],
            options={
                'db_table': 'document',
            },
        ),
        migrations.AlterField(
            model_name='deliveryrecord',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='delivery.driver'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='delivery.orderstatus'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='delivery.card'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=24, on_delete=django.db.models.deletion.SET_DEFAULT, to='delivery.category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('client', 'Client'), ('seller', 'Seller'), ('deliveryman applicant', 'Deliveryman applicant'), ('deliveryman', 'Deliveryman')], max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='delivery.document'),
        ),
    ]
