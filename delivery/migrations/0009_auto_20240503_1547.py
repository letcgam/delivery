from django.db import migrations

def create_order_statuses(apps, schema_editor):
    OrderStatus = apps.get_model("delivery", "OrderStatus")

    statuses = [
        ("PROCESSING", "Processing"),
        ("IN PREPARATION", "In preparation"),
        ("AWAITING WITHDRAW", "Awaiting withdrawal"),
        ("EN ROUTE", "En route"),
        ("DELIVER", "Deliver"),
    ]

    for status_code, description in statuses:
        OrderStatus.objects.get_or_create(description=status_code)


def create_payment_types(apps, schema_editor):
    PaymentType = apps.get_model("delivery", "PaymentType")
    PaymentType.objects.get_or_create(name="CREDIT")
    PaymentType.objects.get_or_create(name="DEBIT")


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_order_statuses),
        migrations.RunPython(create_payment_types),
    ]