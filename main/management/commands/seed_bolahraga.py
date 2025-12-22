from django.core.management.base import BaseCommand
from main.models import Product  # Pastikan 'main' diganti dengan nama app kamu
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Mengisi database dengan 15+ data dummy produk sesuai kategori model'

    def handle(self, *args, **kwargs):
        # 1. Cari user buat jadi pemilik produk
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('❌ ERROR: Belum ada user! Bikin dulu pake "python manage.py createsuperuser"'))
            return

        self.stdout.write(self.style.SUCCESS(f'✅ Memproses data untuk user: {user.username}'))

        # 2. Data Dummy (17 Items)
        # Kategori disesuaikan dengan models.py: 
        # field_setup, training_equipment, match_equipment, safety_recovery, event_accessories, player_gear
        
        products_data = [
            # --- Field Setup ---
            {
                "name": "Portable Goal Post (Set of 2)",
                "price": 2500000,
                "description": "Gawang portable yang mudah dibongkar pasang. Cocok untuk latihan small sided game di lapangan rumput maupun sintetis.",
                "category": "field_setup",
                "stock": 10,
                "thumbnail": "https://placehold.co/600x400?text=Portable+Goal",
                "is_featured": True
            },
            {
                "name": "Corner Flags Pro Set",
                "price": 450000,
                "description": "Set bendera sudut lapangan dengan tiang fleksibel. Anti patah jika tertabrak pemain.",
                "category": "field_setup",
                "stock": 25,
                "thumbnail": "https://placehold.co/600x400?text=Corner+Flags",
                "is_featured": False
            },
            {
                "name": "Field Spray Marker (White)",
                "price": 85000,
                "description": "Cat semprot khusus lapangan rumput. Aman untuk tanaman dan tidak beracun. Warna putih terang.",
                "category": "field_setup",
                "stock": 100,
                "thumbnail": "https://placehold.co/600x400?text=Field+Spray",
                "is_featured": False
            },

            # --- Training Equipment ---
            {
                "name": "Agility Ladder 6m",
                "price": 120000,
                "description": "Tangga ketangkasan untuk melatih footwork dan koordinasi pemain. Wajib untuk sesi pemanasan.",
                "category": "training_equipment",
                "stock": 50,
                "thumbnail": "https://placehold.co/600x400?text=Agility+Ladder",
                "is_featured": True
            },
            {
                "name": "Marker Cones (Isi 50)",
                "price": 95000,
                "description": "Cone mangkok warna-warni fleksibel. Tahan injak dan tidak mudah pecah.",
                "category": "training_equipment",
                "stock": 200,
                "thumbnail": "https://placehold.co/600x400?text=Marker+Cones",
                "is_featured": False
            },
            {
                "name": "Resistance Parachute",
                "price": 150000,
                "description": "Parasut lari untuk melatih kekuatan sprint dan eksplosivitas otot kaki.",
                "category": "training_equipment",
                "stock": 30,
                "thumbnail": "https://placehold.co/600x400?text=Speed+Parachute",
                "is_featured": False
            },
            {
                "name": "Training Bibs (Rompi) Neon",
                "price": 35000,
                "description": "Rompi latihan bahan mesh ringan. Tersedia warna neon hijau dan oranye untuk membedakan tim.",
                "category": "training_equipment",
                "stock": 500,
                "thumbnail": "https://placehold.co/600x400?text=Training+Bibs",
                "is_featured": False
            },

            # --- Match Equipment ---
            {
                "name": "FIFA Quality Pro Match Ball",
                "price": 1200000,
                "description": "Bola standar pertandingan resmi. Aerodinamika presisi dan grip permukaan bertekstur.",
                "category": "match_equipment",
                "stock": 45,
                "thumbnail": "https://placehold.co/600x400?text=Match+Ball",
                "is_featured": True
            },
            {
                "name": "Referee Whistle Classic",
                "price": 180000,
                "description": "Peluit wasit dengan suara nyaring 115dB. Tanpa bola di dalam (pealess), anti macet saat hujan.",
                "category": "match_equipment",
                "stock": 60,
                "thumbnail": "https://placehold.co/600x400?text=Whistle",
                "is_featured": False
            },
            {
                "name": "Referee Card Set",
                "price": 50000,
                "description": "Set kartu kuning dan merah, lengkap dengan dompet catatan skor dan pensil.",
                "category": "match_equipment",
                "stock": 80,
                "thumbnail": "https://placehold.co/600x400?text=Ref+Cards",
                "is_featured": False
            },

            # --- Safety & Recovery ---
            {
                "name": "Team First Aid Kit",
                "price": 550000,
                "description": "Tas P3K lengkap standar medis olahraga. Berisi perban, antiseptik, gunting, dan plester.",
                "category": "safety_recovery",
                "stock": 15,
                "thumbnail": "https://placehold.co/600x400?text=First+Aid+Kit",
                "is_featured": True
            },
            {
                "name": "Instant Ice Spray 400ml",
                "price": 75000,
                "description": "Semprotan pendingin instan untuk meredakan nyeri benturan atau kram otot di lapangan.",
                "category": "safety_recovery",
                "stock": 120,
                "thumbnail": "https://placehold.co/600x400?text=Ice+Spray",
                "is_featured": False
            },
            {
                "name": "Kinesiology Tape (Kio Tape)",
                "price": 65000,
                "description": "Plester elastis untuk support otot dan sendi tanpa membatasi gerak.",
                "category": "safety_recovery",
                "stock": 150,
                "thumbnail": "https://placehold.co/600x400?text=Kinesio+Tape",
                "is_featured": False
            },

            # --- Event Accessories ---
            {
                "name": "Digital Substitution Board",
                "price": 3500000,
                "description": "Papan pergantian pemain digital LED. Terlihat jelas di siang maupun malam hari.",
                "category": "event_accessories",
                "stock": 5,
                "thumbnail": "https://placehold.co/600x400?text=Sub+Board",
                "is_featured": True
            },
            {
                "name": "Water Bottle Carrier (8 Slot)",
                "price": 125000,
                "description": "Keranjang botol minum lipat. Memuat 8 botol, memudahkan hidrasi tim saat break.",
                "category": "event_accessories",
                "stock": 40,
                "thumbnail": "https://placehold.co/600x400?text=Bottle+Carrier",
                "is_featured": False
            },

            # --- Player Gear ---
            {
                "name": "Carbon Flex Shin Guards",
                "price": 280000,
                "description": "Dekker pelindung tulang kering ringan dengan lapisan karbon. Kuat menahan benturan.",
                "category": "player_gear",
                "stock": 70,
                "thumbnail": "https://placehold.co/600x400?text=Shin+Guards",
                "is_featured": False
            },
            {
                "name": "Pro Grip Goalkeeper Gloves",
                "price": 650000,
                "description": "Sarung tangan kiper dengan lateks Jerman 4mm. Grip lengket di kondisi kering maupun basah.",
                "category": "player_gear",
                "stock": 25,
                "thumbnail": "https://placehold.co/600x400?text=GK+Gloves",
                "is_featured": True
            }
        ]

        # 3. Hapus data lama (Opsional)
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING('⚠️ Data lama dihapus...'))

        # 4. Loop isi data
        count = 0
        for item in products_data:
            obj, created = Product.objects.get_or_create(
                name=item['name'],
                user=user,
                defaults={
                    'price': item['price'],
                    'description': item['description'],
                    'category': item['category'],
                    'stock': item['stock'],  # Ditambahkan sesuai models.py
                    'thumbnail': item['thumbnail'],
                    'is_featured': item['is_featured']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'➕ Berhasil nambah: {item["name"]}'))
                count += 1
            else:
                self.stdout.write(f'⚠️ Udah ada (skip): {item["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Selesai! Berhasil menambahkan {count} produk baru.'))