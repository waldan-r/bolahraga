Penjelasan Tugas 2 Bolahraga
Repo: https://github.com/waldan-r/bolahraga
Web: http://waldan-rafid-bolahraga.pbp.cs.ui.ac.id

1. Checklist diimplementasikan dengan panduan pada tutorial, dan catatan yang saya buat saat mengerjakan tutorial sehingga sebenarnya polanya akan sama dengan tutorial. Dimulai dari menginisiasikan proyek django baru, saya melakukan konfigurasi pada proyek yang berisikan package-package. Setelah itu, MVT diimplementasikan dengan membuat sebuah aplikasi "Main" kemudian melakukan pemodelan untuk class Product. Setelah itu, fungsi pada views dibuat untuk nantinya menjawab request dan melakukan sesuatu ke html (template). Ini di-routing dengan urls yang ada di level proyek (walaupun nanti akan bekerja sebaliknya)

2. Request Client 
    \-> [urls.py] level proyek akan mengecek URL untuk menentukan view yang diambil (memanggil fungsi dari view), kalau tidak ada berarti notFound
    \-> [views.py] melakukan fungsi yang dipanggil, misal pada tugas ini adalah untuk menampilkan main (show_main() dan dihubungkan dengan template)
    \-> [template html] memuat konten yang akan ditampilkan menjadi page di web
    \-> [views.py] balik dari pemanggilan template dan memberikan respon
    \-> [Client] respon diberikan

    pada tugas ini, model.py sebenarnya telah dibangun untuk menyiapkan Product yang nanti akan digunakan tetapi karena belum ada kebutuhan untuk meminta atau memuat data pada model.py, maka pola respon hanya seperti itu. model.py mungkin nanti dipakai sebagai jembatan dengan database.

3. settings.py berfungsi mengatur apa saja yang dibutuhkan pada proyek dan memuat konfigurasi tertentu. dalam kata lain, settings.py seperti pedoman untuk proyek ini melakukan sesuatu atau menggunakan tools tertentu untuk jalannya proyek.

4. Pada soal no. 2, models.py akan berguna ketika ada permintaan tertentu terhadap database. migrasi pada awal pemodelan dan juga setiap kali pengubahan pada model.py dilakukan untuk membuat penerapan skema model yang dibuat sebelumnya (pada models.py) ke dalam database lokal.

5. Dari yang saya perhatikan, framework django memberikan kemudahan dalam proses software development karena tiap elemen cukup self-explanatory sehingga cukup mudah bahkan untuk pemula dalam mempelajari cara kerja dan alur pengembangan perangkat lunak ini. Django sebagai framework python juga memiliki virtual environment yang berisi konfigurasi proyek untuk membuat workspace agar tiap proyek dapat berjalan masing-masing.

6. Menurut saya asdos sudah cukup baik dalam memberikan kesempatan eksplorasi melalui tutorial yang ada. Alur pada tutorial sudah sangat jelas dan sejauh ini terjamin program akan berjalan jika diikuti. Setiap potongan materi juga biasanya disertakan referensi atau dokumentasi sehingga saya bisa dengan mudah mengulik lebih lanjut untuk materi tersebut.
