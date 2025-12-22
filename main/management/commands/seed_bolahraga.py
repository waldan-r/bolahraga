import os
import django
import random

# --- KONFIGURASI ---
# Ganti 'nama_project_kamu' dengan nama folder project kamu (folder yang ada settings.py nya)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nama_project_kamu.settings')

# Setup Django agar bisa akses model
django.setup()

# Ganti 'nama_app_kamu' dengan nama aplikasi dimana models.py berada
from main.models import Product

def run():
    print("🚀 Memulai proses seeding data...")

    # Opsi: Hapus data lama agar bersih (uncomment jika perlu)
    Product.objects.all().delete()
    print("🗑️  Data lama dihapus.")

    # Data Dummy yang realistis
    dummy_products = [
        # Field Setup
        {"name": "Portable Goal Post", "cat": "field_setup", "price": 1500000},
        {"name": "Corner Flags Set", "cat": "field_setup", "price": 350000},
        {"name": "Field Marker Cones (50pcs)", "cat": "field_setup", "price": 120000},
        
        # Training Equipment
        {"name": "Agility Ladder", "cat": "training_equipment", "price": 180000},
        {"name": "Training Bibs (Neon)", "cat": "training_equipment", "price": 45000},
        {"name": "Resistance Parachute", "cat": "training_equipment", "price": 95000},

        # Match Equipment
        {"name": "Official Match Ball", "cat": "match_equipment", "price": 850000},
        {"name": "Referee Whistle Pro", "cat": "match_equipment", "price": 150000},
        {"name": "Linesman Flags", "cat": "match_equipment", "price": 200000},

        # Safety & Recovery
        {"name": "First Aid Kit (Sports)", "cat": "safety_recovery", "price": 450000},
        {"name": "Ice Spray 500ml", "cat": "safety_recovery", "price": 85000},
        {"name": "Kinesiology Tape", "cat": "safety_recovery", "price": 60000},

        # Event Accessories
        {"name": "Digital Scoreboard", "cat": "event_accessories", "price": 2500000},
        {"name": "Team Water Bottle Carrier", "cat": "event_accessories", "price": 120000},

        # Player Gear
        {"name": "Pro Shin Guards", "cat": "player_gear", "price": 250000},
        {"name": "Goalkeeper Gloves", "cat": "player_gear", "price": 550000},
    ]

    count = 0
    for item in dummy_products:
        # Generate data random tambahan
        random_stock = random.randint(5, 100)
        is_featured = random.choice([True, False])
        
        # Placeholder image service (biar UI gak kosong)
        dummy_img = f"https://placehold.co/600x400?text={item['name'].replace(' ', '+')}"

        product = Product(
            name=item['name'],
            price=item['price'],
            description=f"Deskripsi lengkap untuk {item['name']}. Kualitas terbaik untuk kebutuhan olahraga Anda.",
            category=item['cat'],
            stock=random_stock,
            thumbnail=dummy_img,
            is_featured=is_featured,
            user=None # User dibiarkan null sesuai model, atau bisa diisi user pertama: User.objects.first()
        )
        product.save()
        count += 1
        print(f"✅ Created: {item['name']}")

    print(f"\n✨ Selesai! Berhasil menambahkan {count} produk dummy.")

if __name__ == '__main__':
    run()