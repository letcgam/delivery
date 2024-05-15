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

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_order_statuses),
    ]
    dependencies = [
        ('delivery', '0001_initial'),
    ]