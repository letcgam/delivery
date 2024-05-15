INSERT INTO category (name) VALUES
    ('Electronics'),
    ('Books'),
    ('Movies'),
    ('Music'),
    ('Clothing'),
    ('Shoes'),
    ('Home & Garden'),
    ('Kitchen & Dining'),
    ('Sports & Outdoors'),
    ('Toys & Games'),
    ('Baby & Kids'),
    ('Beauty & Health'),
    ('Pet Supplies'),
    ('Arts & Crafts'),
    ('Tools & Home Improvement'),
    ('Furniture'),
    ('Office Supplies'),
    ('Jewelry & Watches'),
    ('Luggage & Bags'),
    ('Auto Parts & Accessories'),
    ('Food & Beverages'),
    ('Health & Fitness'),
    ('Collectibles & Memorabilia');

INSERT INTO product (name, description, category_id, price, stock, owner_id) VALUES
    ('iPhone 13 Pro Max','The latest flagship smartphone from Apple.',1,1199.00,10,2),
    ('MacBook Air M2','The latest MacBook Air with the new M2 chip.',1,1199.00,15,2),
    ('Harry Potter and the Sorcerers Stone','The first book in the Harry Potter series by J.K. Rowling.',2,14.99,20,2),
    ('The Lord of the Rings: The Fellowship of the Ring','The first book in The Lord of the Rings trilogy by J.R.R. Tolkien.',2,19.99,15,2),
    ('The Shawshank Redemption','A classic drama film directed by Frank Darabont.',3,9.99,50,2),
    ('The Godfather','A classic crime film directed by Francis Ford Coppola.',3,9.99,30,2),
    ('Led Zeppelin IV','A classic rock album by Led Zeppelin.',4,19.99,25,2),
    ('Abbey Road','A classic rock album by The Beatles.',4,19.99,30,2),
    ('Nike Air Force 1','A classic sneaker from Nike.',5,99.99,12,2),
    ('Adidas Stan Smith','A classic sneaker from Adidas.',5,79.99,18,2),
    ('Sofa Bed','A comfortable sofa that converts into a bed.',6,399.99,8,2),
    ('Dining Table','A sturdy dining table for your home.',7,299.99,10,2),
    ('Basketball','A standard basketball for indoor or outdoor use.',8,19.99,20,2),
    ('Soccer Ball','A standard soccer ball for playing soccer.',8,14.99,30,2),
    ('Lego Star Wars Millennium Falcon','A Lego set of the iconic Millennium Falcon spaceship.',9,199.99,15,2),
    ('Barbie Dreamhouse','A classic Barbie dollhouse for children.',9,149.99,20,2),
    ('Diapers','Disposable diapers for babies.',10,19.99,50,2),
    ('Baby Food','Jarred baby food for infants.',10,2.99,30,2),
    ('Paint Set','A set of acrylic paints for artists.',11,19.99,10,2),
    ('Paint Brushes','A set of paint brushes for artists.',11,9.99,15,2),
    ('Hammer','A hammer for general household use.',12,9.99,20,2),
    ('Screwdriver Set','A set of screwdrivers for various screw types.',12,14.99,12,2),
    ('Queen Bed','A comfortable queen-size bed for your bedroom.',13,499.99,5,2),
    ('Office Chair','An ergonomic office chair for comfort and support.',14,199.99,10,2),
    ('Diamond Necklace','A beautiful diamond necklace for special occasions.',15,2999.99,1,2),
    ('Wireless Bluetooth Headphones', 'High-quality headphones for a superior listening experience.', 1, 49.99, 100, 3),
    ('The Great Gatsby by F. Scott Fitzgerald', 'Classic novel depicting the Jazz Age in America.', 2, 12.99, 50, 3),
    ('The Shawshank Redemption DVD', 'Timeless film about hope and friendship.', 3, 9.99, 75, 3),
    ('Vinyl Record: The Dark Side of the Moon by Pink Floyd', 'Iconic album featuring progressive rock classics.', 4, 29.99, 25, 3),
    ('Mens Casual Hoodie', 'Comfortable and stylish hoodie for everyday wear.', 5, 34.99, 150, 3),
    ('Womens Running Shoes', 'Lightweight and breathable shoes for running enthusiasts.', 6, 59.99, 100, 3),
    ('Stainless Steel Mixing Bowls Set', 'Durable and versatile bowls for kitchen use.', 8, 24.99, 80, 3),
    ('Outdoor Camping Tent', 'Spacious tent for outdoor adventures.', 9, 99.99, 30, 3),
    ('LEGO Star Wars Millennium Falcon Set', 'Build and play with the iconic spaceship from Star Wars.', 10, 129.99, 20, 3),
    ('Baby Diaper Bag Backpack', 'Convenient and stylish bag for parents on the go.', 11, 39.99, 60, 3),
    ('Organic Lavender Essential Oil', 'Relaxing essential oil for aromatherapy and skincare.', 12, 19.99, 40, 3),
    ('Premium Cat Tree Tower', 'Multi-level tower for cats to climb and play.', 13, 79.99, 15, 3),
    ('DIY Scrapbooking Kit', 'Creative kit for preserving memories with style.', 14, 29.99, 50, 3),
    ('Cordless Drill Set', 'Powerful drill for various home improvement projects.', 15, 79.99, 25, 3),
    ('Modern Coffee Table', 'Sleek and minimalist design for contemporary living spaces.', 16, 149.99, 10, 3),
    ('Executive Office Chair', 'Comfortable chair with ergonomic features for long hours of work.', 17, 199.99, 20, 3),
    ('Sterling Silver Bracelet', 'Elegant bracelet crafted from sterling silver.', 18, 49.99, 30, 3),
    ('Travel Backpack with USB Charging Port', 'Functional backpack with charging port for travelers.', 19, 39.99, 50, 3),
    ('Car Tire Pressure Gauge', 'Handy tool for monitoring tire pressure and ensuring safety.', 20, 14.99, 100, 3),
    ('Assorted Chocolate Truffles Box', 'Indulgent chocolates for sweet cravings.', 21, 19.99, 50, 3),
    ('Yoga Mat with Carrying Strap', 'Non-slip mat for yoga and fitness routines.', 22, 29.99, 70, 3),
    ('Limited Edition Star Wars Collectible Figure', 'Rare collectible figure for Star Wars fans.', 23, 79.99, 10, 3),
    ('Smartphone Car Mount Holder', 'Convenient holder for safe navigation while driving.', 1, 9.99, 200, 3),
    ('Cookbook: The Joy of Cooking', 'Comprehensive cookbook with a wide range of recipes.', 2, 29.99, 30, 3),
    ('Classic Film Poster Set', 'Set of vintage posters featuring iconic movies.', 3, 19.99, 40, 3),
    ('Acoustic Guitar Starter Kit', 'Beginner-friendly kit for learning to play the guitar.', 4, 129.99, 15, 3),
    ('Womens Floral Print Dress', 'Chic and trendy dress for various occasions.', 5, 44.99, 80, 3),
    ('Mens Running Shoes', 'Durable and supportive shoes for running and fitness activities.', 6, 69.99, 60, 3),
    ('Stainless Steel Cookware Set', 'High-quality cookware set for professional cooking.', 8, 149.99, 25, 3);




APLICAR NA MIGRATIONS ANTES DE EXECUTAR:

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