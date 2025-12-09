from django.core.management.base import BaseCommand
from main.models import Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Mengisi database dengan data dummy produk olahraga'

    def handle(self, *args, **kwargs):
        # 1. Cari user buat jadi pemilik produk
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('❌ ERROR: Belum ada user! Bikin dulu pake "python manage.py createsuperuser"'))
            return

        self.stdout.write(self.style.SUCCESS(f'✅ Memproses data untuk user: {user.username}'))

        # 2. Data Dummy
        products_data = [
            {
                "name": "Jersey Timnas Indonesia Home",
                "price": 899000,
                "description": "Jersey original Timnas Indonesia merah membara. Bahan nyaman, logo Garuda di dada. Cocok buat nobar!",
                "category": "Jersey",
                "thumbnail": "https://images.tokopedia.net/img/cache/700/VqbcmM/2022/9/22/e0066164-902e-486a-b286-905156a624ce.jpg",
                "is_featured": True
            },
            {
                "name": "Adidas Predator Accuracy",
                "price": 2500000,
                "description": "Sepatu bola legendaris untuk kontrol maksimal. Akurasi tendangan meningkat 100% (kalau jago).",
                "category": "Sepatu",
                "thumbnail": "https://assets.adidas.com/images/w_600,f_auto,q_auto/283626775670499691b0af8800ea07f4_9366/Predator_Accuracy.1_Firm_Ground_Boots_Black_GW4569_22_model.jpg",
                "is_featured": True
            },
            {
                "name": "Nike Mercurial Vapor 15",
                "price": 3200000,
                "description": "Sepatu khusus speedster. Enteng banget, berasa lari tanpa beban. Dipakai Mbappe.",
                "category": "Sepatu",
                "thumbnail": "https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/0a28f44d-1683-4966-932f-7634db844358/zoom-mercurial-vapor-15-academy-mg-multi-ground-soccer-cleats-s1H5M4.png",
                "is_featured": False
            },
            {
                "name": "Bola Al Rihla Pro",
                "price": 1500000,
                "description": "Bola resmi Piala Dunia 2022. Aerodinamis tinggi, flight ball stabil. Standar FIFA Quality Pro.",
                "category": "Equipment",
                "thumbnail": "https://assets.adidas.com/images/w_600,f_auto,q_auto/4e6f9660370d47789437ae2d005f5690_9366/Al_Rihla_Pro_Ball_White_H57783_01_standard.jpg",
                "is_featured": True
            },
            {
                "name": "Jersey Real Madrid 2024",
                "price": 1200000,
                "description": "Jersey putih kebanggaan Los Blancos. Desain elegan dengan aksen emas. Hala Madrid!",
                "category": "Jersey",
                "thumbnail": "https://assets.adidas.com/images/w_600,f_auto,q_auto/b66e3954002641a9807aaf6d010724f7_9366/Real_Madrid_23-24_Home_Jersey_White_HR3796_22_model.jpg",
                "is_featured": False
            },
            {
                "name": "Ortuseight Jogosala",
                "price": 450000,
                "description": "Sepatu futsal lokal pride. Harga pelajar kualitas ngeri. Sol tebal, awet buat main di lapangan semen.",
                "category": "Sepatu",
                "thumbnail": "https://ortuseight.id/cdn/shop/products/JOGOSALA-VENOM-WHITE-ORTRED-01_800x.jpg",
                "is_featured": False
            },
            {
                "name": "Sarung Tangan Kiper Adidas",
                "price": 800000,
                "description": "Predator Pro Goalkeeper Gloves. Grip lengket banget, melindungi jari dari cedera saat menepis bola keras.",
                "category": "Aksesoris",
                "thumbnail": "https://assets.adidas.com/images/w_600,f_auto,q_auto/a4449887103e4075b060af7300e84b7a_9366/Predator_Pro_Goalkeeper_Gloves_Black_HN3345_01_standard.jpg",
                "is_featured": False
            },
            {
                "name": "Kaos Kaki Anti-Slip",
                "price": 50000,
                "description": "Kaos kaki dengan grip karet di telapak. Kaki gak bakal geser di dalam sepatu. Mengurangi risiko lecet.",
                "category": "Aksesoris",
                "thumbnail": "https://down-id.img.susercontent.com/file/id-11134207-7r98v-lsh5d9j5g9t78c",
                "is_featured": False
            },
            {
                "name": "Jersey Manchester City Treble",
                "price": 1100000,
                "description": "Jersey biru langit edisi spesial Treble Winner. Bahan breathable, cocok dipakai casual maupun olahraga.",
                "category": "Jersey",
                "thumbnail": "https://images.footballfanatics.com/manchester-city/manchester-city-home-shirt-2023-24_ss4_p-13369499+u-15x96e00y3g10j4s0z8+v-63456345.jpg",
                "is_featured": True
            },
            {
                "name": "Tas Gym Duffel Bag",
                "price": 350000,
                "description": "Tas besar muat sepatu, baju ganti, dan botol minum. Tahan air dan desain sporty.",
                "category": "Equipment",
                "thumbnail": "https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/9859f772-5a50-4286-8a03-7b61f4350165/brasilia-9-5-training-duffel-bag-medium-60l-XhC7X7.png",
                "is_featured": False
            }
        ]

        # 3. Hapus data lama (Opsional, uncomment kalau mau bersih2 dulu sebelum isi)
        # Product.objects.all().delete()
        # self.stdout.write(self.style.WARNING('⚠️ Data lama dihapus...'))

        # 4. Loop isi data
        count = 0
        for item in products_data:
            # Pake get_or_create biar gak duplikat kalau dijalankan berkali-kali
            obj, created = Product.objects.get_or_create(
                name=item['name'],
                user=user,
                defaults={
                    'price': item['price'],
                    'description': item['description'],
                    'category': item['category'],
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