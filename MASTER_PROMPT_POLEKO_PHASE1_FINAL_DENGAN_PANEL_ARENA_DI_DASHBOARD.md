# POLEKO PRODUCTION MONITORING SYSTEM
# PHASE 1 — MAJOR UX, WORKFLOW & DASHBOARD REVISION
## REVISION 03 NOVEMBER 2026
## Berdasarkan Evaluasi Sir Argha, Julia, Tifanie, dan Kebutuhan Proses Bisnis

---

# 1. TUJUAN REVISI

Lakukan revisi menyeluruh terhadap aplikasi Streamlit POLEKO Production Monitoring System berdasarkan evaluasi terbaru dari Sir Argha dan Julia.

Revisi ini bukan sekadar perubahan kosmetik atau penambahan komponen UI. Fokus utama adalah memperbaiki ketepatan workflow, pemisahan tanggung jawab pengguna, validasi data, konsistensi navigasi, dan kejelasan status laporan dari pekerja sampai penerimaan oleh General Manager.

Aplikasi harus mencerminkan proses monitoring produksi yang sistematis, mudah dipahami, dan tidak menimbulkan kesalahan interpretasi terhadap status pekerjaan.

Gunakan perspektif:

- Senior UI/UX Designer.
- UX Researcher.
- Senior Streamlit Developer.
- Business Process Analyst.
- Application Workflow Designer.

Prinsip utama:

**Business Needs + User Needs = User Experience**

Jangan hanya membuat fitur berfungsi secara teknis. Pastikan pengguna memahami apa yang sedang terjadi, tindakan apa yang harus dilakukan, dan siapa yang bertanggung jawab pada setiap tahapan.

# 2. HIERARKI INSTRUKSI DAN KETENTUAN YANG TETAP BERLAKU

Master prompt sebelumnya tetap menjadi sumber utama ketentuan proyek.

Seluruh ketentuan lama yang tidak bertentangan dengan revisi ini harus dipertahankan, termasuk:

1. Tetap terdapat 18 tahapan produksi dengan nama dan urutan resmi sesuai master prompt.
2. Tetap terdapat tiga perspektif utama:
   - Pekerja Produksi.
   - SPV Produksi.
   - Manajemen.
3. Pekerja bertanggung jawab melakukan input monitoring pada tahapan yang menjadi tanggung jawabnya.
4. SPV tidak melakukan input awal data produksi.
5. SPV melakukan monitoring, pemeriksaan, validasi, dan pembuatan laporan gabungan.
6. Manajemen melakukan pemeriksaan, konfirmasi, dan penerusan laporan kepada General Manager.
7. General Manager tetap menjadi penerima laporan, bukan akun login keempat.
8. Laporan gabungan hanya dapat dibuat setelah seluruh 18 tahapan memenuhi persyaratan validasi.
9. Data aplikasi menggunakan session_state.
10. Tidak menambahkan database, backend, API, atau integrasi langsung ke ARENA.
11. Aplikasi tetap merupakan prototype demonstrasi proses To-Be.
12. Tidak mengarang nama pekerja perusahaan, parameter produksi, hasil simulasi, atau data operasional.

Apabila terdapat perbedaan antara instruksi lama dan revisi terbaru ini, gunakan ketentuan revisi terbaru khusus untuk bagian yang mengalami perubahan.

Jangan mengubah BPMN, nama proses produksi, hasil simulasi ARENA, maupun parameter penelitian hanya untuk menyesuaikan tampilan aplikasi.

# 3. LOGIN — REDESIGN DAN PEMISAHAN IDENTITAS PENGGUNA

## 3.1 Masalah yang harus diperbaiki

Halaman login saat ini menampilkan seluruh akun dalam satu dropdown panjang.

Contohnya:

- Pekerja Demo 01 - Tahap 01 - Opening.
- Pekerja Demo 02 - Tahap 02 - Sortiran Awal.
- Dan seterusnya.
- SPV.
- Manager Produksi.
- PPIC.
- QC.
- QA.

Hal tersebut membuat pilihan akun terlihat bercampur, terlalu panjang, dan tidak terorganisasi.

## 3.2 Struktur login baru

Buat pemisahan pilihan berdasarkan kelompok role.

Gunakan susunan:

**A. Pekerja Produksi**

Tampilkan akun pekerja dalam kelompok tersendiri.

Setiap akun tetap terhubung dengan tahapan produksi yang menjadi tanggung jawabnya.

Contoh format identitas:

- Pekerja 01 — Opening.
- Pekerja 02 — Sortiran Awal.
- Pekerja 03 — Bodega.

Gunakan nama dan pemetaan akun yang memang sudah tersedia dalam konfigurasi aplikasi. Jangan membuat identitas pekerja perusahaan yang tidak tersedia.

**B. SPV Produksi**

Tampilkan akun SPV secara terpisah.

**C. Manajemen**

Tampilkan empat identitas:

- Manager Produksi.
- PPIC.
- QC.
- QA.

Keempat identitas tersebut tetap berada dalam satu perspektif Manajemen dengan alur dan kewenangan yang sama.

Jangan membuat empat sistem pelaporan yang terpisah.

## 3.3 Password dan login DEMO

Perbaiki bagian password.

Gunakan placeholder:

"Masukkan password."

Untuk demonstrasi, login dapat dilakukan tanpa harus mengisi password.

Jangan menampilkan pesan "Belum diperlukan pada demo" sebagai disabled text.

Jangan membuat pengguna mengira bahwa aplikasi memerlukan autentikasi produksi yang sebenarnya.

Gunakan tombol:

**Login**

Setelah akun dipilih, pengguna dapat langsung masuk ke dashboard sesuai role.

Pertahankan pemisahan hak akses berdasarkan identitas yang dipilih.

## 3.4 Visual login

Gunakan desain yang lebih terorganisasi:

- Logo POLEKO di kiri atas.
- Identitas aplikasi jelas.
- Dropdown akun yang dikelompokkan.
- Password input.
- Tombol Login.
- Tidak ada penjelasan panjang yang tidak diperlukan.

Pastikan seluruh elemen memiliki alignment, spacing, dan ukuran yang konsisten.

# 4. SIDEBAR DAN NAVIGASI GLOBAL

Berlaku untuk semua perspektif.

## 4.1 Hapus menu yang tidak lagi diperlukan

Hapus seluruh bagian sidebar:

- Siklus Produksi.
- Kontrol Demo.
- Skenario Demo.
- Muat Data Demo.
- Reset Demo.

Hapus bukan hanya dari tampilan CSS, tetapi juga komponen navigasi dan logika antarmuka yang tidak lagi digunakan.

Jangan meninggalkan menu kosong atau menu yang masih bisa diakses melalui navigasi internal.

Catatan penting:

Penghapusan menu Siklus Produksi bukan berarti menghilangkan hubungan data antartahapan.

Identitas siklus tetap dipertahankan secara internal dalam session_state karena diperlukan untuk mengelompokkan 18 laporan, mencegah pencampuran data, dan membentuk laporan gabungan.

Dengan demikian:

- Tidak ada menu Siklus Produksi.
- Tidak ada dropdown pemilihan siklus pada UI.
- Pengelompokan siklus tetap berjalan di balik sistem.

## 4.2 Konsistensi sidebar

Perbaiki:

- Alignment logo.
- Posisi tulisan POLEKO — Production Monitoring System.
- Margin dan padding.
- Jarak antar-menu.
- Ukuran font.
- Indikator menu aktif.
- Konsistensi ikon.
- Responsivitas sidebar.

Logo harus tetap berada di posisi kiri atas dan tidak berubah-ubah ketika pengguna berpindah halaman.

Jangan memenuhi sidebar dengan informasi dekoratif.

# 5. ROLE PEKERJA PRODUKSI

Perspektif pekerja merupakan bagian paling penting dalam proses input.

Setiap pekerja harus memahami bahwa laporan yang mereka buat adalah laporan untuk tahapan yang menjadi tanggung jawabnya sendiri.

## 5.1 Struktur menu pekerja

Pertahankan empat menu:

1. Dashboard Pekerja.
2. Input Monitoring Produksi.
3. Tugas Pemeriksaan Kembali.
4. Riwayat Pencatatan.

Jangan menambahkan menu yang memiliki fungsi serupa.

## 5.2 Dashboard Pekerja

Perbaiki dashboard agar hanya menampilkan informasi yang relevan dengan pekerja yang sedang login.

Tampilkan:

- Nama atau identitas pekerja.
- Nama tahapan yang menjadi tanggung jawabnya.
- Status penginputan tahapan.
- Status pemeriksaan SPV.
- Catatan dari SPV jika ada.
- Status perbaikan jika ada.
- Riwayat laporan yang relevan.

Jangan menampilkan status seluruh 18 tahapan seolah-olah merupakan tanggung jawab satu pekerja.

### Status yang harus dibedakan

Gunakan status berikut:

- Belum Dicatat.
- Sudah Dikirim ke SPV.
- Menunggu Pemeriksaan SPV.
- Dikonfirmasi SPV.
- Perlu Perbaikan.
- Sudah Diperbaiki.
- Menunggu Pemeriksaan Ulang SPV.

Jangan menggunakan status umum seperti "Semua tahapan sudah dikirim" jika pekerja hanya bertanggung jawab terhadap satu tahapan.

Contoh pesan:

"Input tahapan Opening telah dikirim kepada SPV dan sedang menunggu pemeriksaan."

Jika belum ada input:

"Belum ada laporan yang dikirim untuk tahapan Opening."

Jika SPV telah memberikan catatan:

"SPV meminta pemeriksaan ulang pada tahapan Opening. Silakan periksa catatan perbaikan."

Pesan harus mengikuti data aktual pada akun yang sedang login.

## 5.3 Input Monitoring Produksi

Perbaiki halaman input agar sederhana, rapi, dan mudah dipahami.

Setiap pekerja hanya dapat menginput tahapan yang menjadi tanggung jawab akun tersebut.

Jangan menampilkan form 18 tahapan sekaligus kepada satu pekerja.

### A. Informasi tahapan

Tampilkan secara jelas:

- Nama tahapan.
- Kode tahapan.
- Identitas pekerja.
- Waktu input.

Nama tahapan harus otomatis mengikuti akun yang login.

### B. Waktu proses

Pertahankan input:

- Waktu Mulai.
- Waktu Selesai.

Hapus field Durasi dari tampilan input.

Durasi tidak boleh diminta untuk diisi manual.

Apabila diperlukan untuk ringkasan internal, durasi dapat dihitung secara otomatis dari waktu mulai dan waktu selesai. Jangan meminta pekerja menghitungnya sendiri.

### C. Khusus proses Opening

Pada proses Opening atau Penerimaan Bahan Baku, waktu kedatangan bahan baku sudah diketahui terjadi pada dua waktu:

- 07.00.
- 18.00.

Karena itu, jangan lagi menggunakan input jam manual untuk waktu kedatangan Opening.

Gunakan dropdown:

**Waktu Kedatangan Bahan Baku**

Pilihan:

- 07.00 — Pagi.
- 18.00 — Sore.

Pilihan ini hanya berlaku pada tahapan Opening.

Jangan menerapkan dropdown tersebut ke 17 tahapan lainnya.

### D. Jumlah Produksi

Pertahankan field:

**Jumlah Produksi (kg)**

Ketentuan:

- Input numerik.
- Tidak boleh negatif.
- Satuan kg terlihat jelas.
- Nilai tersimpan di session_state.
- Nilai dapat dilihat pada riwayat pencatatan dan laporan.

Jangan mengarang target atau standar produksi.

### E. Pelaksana/Pemantau

Field yang sebelumnya berupa input teks harus diubah menjadi dropdown.

Nama field:

**Pelaksana/Pemantau**

Pilihan:

- Operator.
- SPV.
- QC.
- Foreman.

Pengguna tidak perlu mengetik sendiri nilai tersebut.

### F. Kondisi Proses

Gunakan pilihan:

- Normal.
- Sering Ada Kendala.
- Kadang Ada Kendala.

Hapus pilihan "Tidak Ada Kendala".

Ketentuan:

Jika pengguna memilih Normal:

- Tidak perlu menampilkan field penjelasan.
- Sistem mencatat kondisi sebagai Normal.

Jika pengguna memilih Sering Ada Kendala:

- Tampilkan field tambahan wajib.
- Label: "Jelaskan Kendala yang Terjadi".
- Pengguna harus menjelaskan kondisi yang dialami.

Jika pengguna memilih Kadang Ada Kendala:

- Tampilkan field tambahan wajib.
- Label: "Jelaskan Kendala yang Terjadi".
- Pengguna harus memberikan keterangan.

Jangan menerima pengiriman laporan dengan kondisi kendala tanpa penjelasan.

### G. Monitoring Pencatatan

Hapus field atau section:

"Monitoring Pencatatan".

Field ini tidak lagi digunakan dalam form pekerja.

Jangan menggantinya dengan field baru yang tidak diminta.

### H. Hapus Pratinjau Laporan

Hapus seluruh pilihan:

"Pratinjau Laporan".

Pekerja tidak membutuhkan tombol pratinjau terpisah setelah melakukan input.

Gantikan dengan proses pengiriman laporan yang jelas.

Tombol utama:

**Kirim Laporan ke SPV**

Sebelum pengiriman, validasi seluruh field wajib.

Setelah berhasil:

- Simpan data.
- Catat identitas pekerja.
- Catat waktu pengiriman.
- Ubah status menjadi Menunggu Pemeriksaan SPV.
- Tampilkan notifikasi bahwa laporan telah berhasil dikirim.

Jangan mengirim data ganda apabila tombol ditekan berulang kali.

## 5.4 Input mandiri per pekerja

Ini merupakan perubahan penting.

Setiap pekerja mempunyai input mandiri sesuai tahapan masing-masing.

Contohnya:

Pekerja Opening hanya mengirim laporan Opening.

Pekerja Sortiran Awal hanya mengirim laporan Sortiran Awal.

Pekerja Bodega hanya mengirim laporan Bodega.

Dan seterusnya sampai seluruh 18 tahapan.

Jangan menggabungkan input semua pekerja menjadi satu status yang otomatis dianggap selesai setelah satu pekerja mengirim laporan.

Satu laporan pekerja hanya dapat mengubah status tahapan miliknya sendiri.

## 5.5 Human Error dan pengeditan laporan

Sediakan mekanisme untuk mengatasi kesalahan input.

Tetapkan aturan prototype berikut:

- Pekerja dapat mengedit laporan yang sudah dikirim selama maksimal 6 jam sejak pengiriman.
- Pengeditan hanya dapat dilakukan sebelum SPV mengonfirmasi laporan tersebut.
- Setelah SPV mengonfirmasi, laporan terkunci.
- Jika SPV meminta perbaikan, pekerja mendapatkan kesempatan memperbaiki laporan melalui tugas pemeriksaan kembali.
- Setiap perubahan harus menyimpan riwayat versi.
- Data awal tidak boleh dihapus atau ditimpa secara permanen.

Riwayat harus dapat menunjukkan:

- Versi awal.
- Waktu pengiriman awal.
- Perubahan yang dilakukan.
- Waktu perubahan.
- Identitas pekerja.
- Catatan SPV jika perbaikan berasal dari permintaan SPV.

Setelah enam jam berlalu, tampilkan informasi bahwa periode pengeditan telah berakhir.

Jangan menyatakan enam jam sebagai kebijakan resmi perusahaan. Ini merupakan aturan akses pada prototype demonstrasi.

## 5.6 Tugas Pemeriksaan Kembali

Halaman ini hanya menampilkan tugas yang benar-benar ditujukan kepada pekerja yang sedang login.

Tampilkan:

- Nama tahapan.
- Catatan SPV.
- Waktu permintaan perbaikan.
- Status tugas.
- Tombol untuk membuka dan memperbaiki laporan.

Setelah pekerja mengirimkan hasil perbaikan:

- Simpan versi baru.
- Catat waktu pengiriman.
- Ubah status menjadi Menunggu Pemeriksaan Ulang SPV.
- Berikan notifikasi bahwa laporan telah dikirim kembali.

Jangan menghapus versi awal.

## 5.7 Riwayat Pencatatan

Tampilkan hanya laporan milik pekerja yang login.

Sediakan informasi:

- Tanggal dan waktu.
- Nama tahapan.
- Jumlah produksi.
- Waktu mulai dan selesai.
- Pelaksana/Pemantau.
- Kondisi proses.
- Status SPV.
- Riwayat perubahan.

Jangan menampilkan laporan pekerja lain.

# 6. ROLE SPV PRODUKSI

SPV bertanggung jawab memeriksa seluruh 18 tahapan dan memastikan laporan lengkap serta benar sebelum membuat laporan gabungan.

Perbaiki workflow SPV secara menyeluruh.

## 6.1 Struktur menu SPV

Pertahankan menu yang benar-benar memiliki fungsi berbeda:

1. Dashboard Pengawasan.
2. Monitoring & Kelengkapan Produksi.
3. Validasi Laporan.
4. Laporan Gabungan.

Jangan membuat dua menu yang menampilkan fungsi dan informasi sama.

## 6.2 Dashboard Pengawasan

Dashboard harus memberikan gambaran langsung mengenai kondisi 18 tahapan.

Tampilkan ringkasan:

- Tahapan sudah dicatat.
- Tahapan belum dicatat.
- Menunggu pemeriksaan SPV.
- Sudah dikonfirmasi SPV.
- Perlu perbaikan.
- Sudah diperbaiki.
- Menunggu pemeriksaan ulang SPV.

Tampilkan indikator:

**Jumlah Tahapan: X/18**

Nilai X harus dihitung berdasarkan laporan yang benar-benar masuk dan memenuhi kriteria pencatatan.

Jangan menghitung laporan kosong atau laporan pekerja lain sebagai laporan yang telah dicatat.

Tambahkan:

**Status Laporan**

Contoh:

- Menunggu Input Pekerja.
- Menunggu Pemeriksaan SPV.
- Perlu Perbaikan.
- Proses Pemeriksaan Ulang.
- Siap Dibuat Menjadi Laporan Gabungan.
- Laporan Gabungan Telah Dihasilkan.
- Menunggu Diteruskan ke Manajemen.

Tambahkan:

**Langkah Berikutnya**

Contoh:

"Masih terdapat 3 tahapan yang belum memiliki laporan. Menunggu penginputan pekerja terkait."

Atau:

"Seluruh 18 tahapan telah diperiksa dan dikonfirmasi. Laporan gabungan siap dibuat."

Jika laporan gabungan sudah tersedia:

Tampilkan tombol:

**Buka Laporan Gabungan**

Tombol tersebut mengarahkan pengguna ke menu Laporan Gabungan.

## 6.3 Monitoring & Kelengkapan Produksi

Tampilkan tabel seluruh 18 tahapan.

Kolom yang disarankan:

- No.
- Kode Tahapan.
- Nama Tahapan.
- Pekerja Penanggung Jawab.
- Status Input.
- Status Pemeriksaan SPV.
- Waktu Pengiriman.
- Tindakan.

Tindakan harus mengikuti kondisi setiap tahapan.

Contoh:

Jika belum ada input:

Status: Belum Dicatat.

Tindakan: Hubungi Pekerja.

Jika laporan sudah masuk:

Status: Menunggu Pemeriksaan SPV.

Tindakan: Periksa Laporan.

Jika sudah dikonfirmasi:

Status: Dikonfirmasi.

Tindakan: Lihat Detail.

Jika perlu perbaikan:

Status: Perlu Perbaikan.

Tindakan: Lihat Catatan.

Jangan mengaktifkan tindakan konfirmasi untuk data yang belum tersedia.

## 6.4 Validasi Laporan — Pemeriksaan Per Tahapan

Ini merupakan perubahan utama.

SPV harus mempunyai kemampuan untuk memeriksa masing-masing tahapan secara individual.

Jangan lagi menggunakan satu tombol konfirmasi yang langsung mengesahkan seluruh 18 tahapan.

Untuk setiap tahapan yang memiliki laporan, sediakan:

A. Tombol:

**Konfirmasi Tahapan**

Ketika ditekan:

- Tandai tahapan sebagai Dikonfirmasi SPV.
- Simpan identitas SPV.
- Simpan tanggal dan waktu konfirmasi.
- Kunci laporan pekerja tersebut.
- Berikan notifikasi bahwa laporan telah dikonfirmasi.

Konfirmasi hanya dapat dilakukan jika laporan tersedia dan telah diperiksa.

B. Tombol:

**Hubungi Pekerja**

Ketika ditekan:

Tampilkan field:

"Catatan untuk Pekerja"

Catatan wajib diisi.

SPV harus menjelaskan hal yang perlu diperiksa atau diperbaiki.

Setelah dikirim:

- Simpan catatan.
- Catat identitas SPV.
- Catat waktu pengiriman.
- Buat tugas pemeriksaan kembali.
- Teruskan tugas kepada pekerja yang bertanggung jawab atas tahapan tersebut.
- Ubah status menjadi Perlu Perbaikan.

Pekerja akan melihat catatan tersebut di menu Tugas Pemeriksaan Kembali.

Jangan menghapus data sebelumnya.

## 6.5 Pengiriman ulang hasil perbaikan

Ketika pekerja mengirimkan hasil perbaikan:

- Status berubah menjadi Menunggu Pemeriksaan Ulang SPV.
- SPV dapat membuka versi terbaru.
- SPV dapat memeriksa kembali.
- SPV dapat mengonfirmasi.
- SPV dapat mengirimkan catatan perbaikan berikutnya jika masih diperlukan.

Jangan menganggap hasil perbaikan otomatis valid tanpa pemeriksaan SPV.

## 6.6 Persyaratan Generate Report

Tombol:

**Generate Report**

hanya dapat digunakan apabila seluruh kondisi berikut terpenuhi:

1. Seluruh 18 tahapan sudah memiliki laporan.
2. Seluruh laporan telah diperiksa oleh SPV.
3. Seluruh 18 tahapan telah mendapatkan konfirmasi SPV.
4. Tidak ada tahapan berstatus Perlu Perbaikan.
5. Tidak ada tugas pemeriksaan kembali yang masih terbuka.
6. Tidak ada laporan yang masih menunggu pemeriksaan ulang.
7. Tidak ada data wajib yang belum lengkap.

Jika salah satu persyaratan belum terpenuhi:

- Tombol Generate Report harus nonaktif.
- Tampilkan alasan yang jelas.
- Tampilkan jumlah tahapan yang belum memenuhi persyaratan.

Contoh:

"Generate Report belum dapat dilakukan. Masih terdapat 2 tahapan yang menunggu pemeriksaan SPV."

Jangan hanya menggunakan disabled button tanpa penjelasan.

## 6.7 Laporan Gabungan

Laporan gabungan merupakan hasil penggabungan data dari 18 tahapan yang sudah dikonfirmasi.

Tampilkan:

- Identitas siklus secara internal.
- Tanggal produksi.
- Ringkasan 18 tahapan.
- Jumlah produksi per tahapan.
- Waktu mulai dan selesai.
- Pelaksana/Pemantau.
- Kondisi proses.
- Catatan kendala jika tersedia.
- Status pemeriksaan.
- Identitas SPV yang melakukan konfirmasi.

Jangan membuat laporan gabungan ganda untuk siklus yang sama.

Jika laporan sudah berhasil dibuat, tampilkan hasilnya dan statusnya.

Tombol tindakan utama:

**Teruskan ke Manajemen**

Hanya satu tombol utama untuk proses penerusan.

Hapus tombol lain yang memiliki fungsi penerusan serupa.

Jangan membuat tombol "Teruskan ke PPIC" pada halaman lain yang mengulang tindakan yang sama.

Setelah tombol ditekan:

- Simpan waktu penerusan.
- Simpan identitas SPV.
- Simpan status laporan.
- Kunci tindakan penerusan agar tidak dapat dilakukan dua kali.
- Teruskan laporan ke perspektif Manajemen.

Tampilkan notifikasi berhasil.

## 6.8 Konsistensi navigasi SPV

Alur yang wajib digunakan:

Dashboard Pengawasan
→ Monitoring & Kelengkapan Produksi
→ Validasi Per Tahapan
→ Seluruh 18 Tahapan Dikonfirmasi
→ Generate Report
→ Laporan Gabungan
→ Teruskan ke Manajemen.

Jika laporan gabungan sudah tersedia, Dashboard Pengawasan harus mengarahkan ke Laporan Gabungan, bukan mengulang proses Generate Report.

Jangan membuat dua halaman dengan tombol penerusan yang sama.

# 7. ROLE MANAJEMEN — MANAGER PRODUKSI, PPIC, QC, QA

Keempat identitas ini berada dalam satu perspektif Manajemen.

Mereka mempunyai fungsi operasional yang sama dalam prototype:

- Melihat laporan yang masuk dari SPV.
- Memeriksa laporan gabungan.
- Melakukan validasi.
- Memberikan catatan perbaikan kepada SPV.
- Mengonfirmasi laporan.
- Meneruskan laporan kepada General Manager.

Yang membedakan adalah identitas pengguna yang melakukan tindakan.

## 7.1 Identitas pelaksana

Simpan identitas yang benar-benar login:

- Manager Produksi.
- PPIC.
- QC.
- QA.

Setiap tindakan harus mencatat identitas yang melakukan tindakan tersebut.

Contoh:

"Laporan diperiksa oleh: PPIC."

"Laporan diteruskan oleh: Manager Produksi."

Jangan menetapkan identitas secara otomatis tanpa mengikuti akun yang sedang login.

## 7.2 Dashboard Manajemen

Tampilkan informasi:

- Laporan yang masuk dari SPV.
- Status laporan.
- Waktu penerimaan.
- Identitas SPV pengirim.
- Status pemeriksaan Manajemen.
- Langkah berikutnya.

Contoh:

"1 laporan menunggu pemeriksaan dan konfirmasi."

Sediakan tombol:

**Periksa dan Konfirmasi**

Tombol mengarahkan pengguna ke halaman Laporan Masuk atau Pemeriksaan dan Konfirmasi.

Jangan menampilkan data yang tidak relevan.

## 7.3 Menu Laporan Masuk

Tampilkan laporan gabungan yang telah diteruskan oleh SPV.

Tampilkan:

- Identitas laporan.
- Tanggal produksi.
- Ringkasan 18 tahapan.
- Jumlah produksi.
- Waktu.
- Kondisi proses.
- Catatan kendala.
- Identitas SPV.
- Waktu penerusan.

Tambahkan tombol:

**Lanjut ke Pemeriksaan dan Konfirmasi**

Tombol mengarahkan pengguna ke proses pemeriksaan laporan.

Jangan menampilkan tombol konfirmasi final pada halaman ini jika tindakan konfirmasi sudah disediakan di halaman berikutnya.

## 7.4 Menu Pemeriksaan dan Konfirmasi

Sediakan proses pemeriksaan laporan gabungan oleh Manajemen.

Tampilkan laporan secara lengkap dan dapat dibaca.

Tambahkan checkbox:

"Saya sudah memeriksa laporan gabungan ini."

Tombol Konfirmasi Laporan baru aktif setelah checkbox dipilih dan seluruh pemeriksaan wajib terpenuhi.

Sediakan keputusan:

- Laporan Diterima.
- Perlu Perbaikan.

### Jika Laporan Diterima

Ketika pengguna memilih Laporan Diterima:

- Simpan identitas pengguna.
- Simpan waktu pemeriksaan.
- Aktifkan tombol Konfirmasi Laporan setelah persyaratan terpenuhi.

Setelah dikonfirmasi:

- Ubah status menjadi Diperiksa dan Dikonfirmasi Manajemen.
- Kunci tindakan konfirmasi agar tidak dapat dilakukan berulang.
- Aktifkan langkah berikutnya.

Tampilkan tombol:

**Lanjut ke Penerusan ke General Manager**

### Jika Perlu Perbaikan

Tampilkan field wajib:

"Catatan Perbaikan untuk SPV"

Manajemen wajib memberikan alasan dan penjelasan yang jelas.

Setelah dikirim:

- Simpan identitas Manajemen.
- Simpan catatan.
- Simpan waktu pengiriman.
- Kembalikan laporan kepada SPV untuk pemeriksaan dan perbaikan.
- Ubah status menjadi Perlu Perbaikan oleh Manajemen.

Jangan menghapus laporan gabungan atau data awal.

SPV harus menerima notifikasi dan dapat melakukan pemeriksaan ulang.

Setelah laporan diperbaiki dan dikirim kembali, Manajemen dapat melakukan pemeriksaan ulang.

Jangan melanjutkan ke General Manager sebelum laporan diterima dan dikonfirmasi Manajemen.

## 7.5 Menu Penerusan ke General Manager

Setelah laporan dikonfirmasi, arahkan pengguna ke bagian:

**Penerusan ke General Manager**

Tampilkan ringkasan:

- Laporan yang akan diteruskan.
- Status pemeriksaan.
- Identitas pemeriksa.
- Identitas pengguna yang akan meneruskan.

Sediakan tombol:

**Teruskan ke General Manager**

Tombol hanya dapat digunakan satu kali untuk satu laporan.

Setelah ditekan:

- Simpan identitas Manager Produksi/PPIC/QC/QA yang meneruskan.
- Simpan tanggal dan waktu penerusan.
- Ubah status menjadi Diteruskan ke General Manager.
- Kunci tindakan penerusan.
- Cegah pengguna lain melakukan penerusan ulang.

## 7.6 Notifikasi penerimaan General Manager

Prototype tidak perlu menyediakan akun login atau dashboard General Manager.

Setelah penerusan berhasil, tampilkan notifikasi atau pop-up:

**Laporan Berhasil Diteruskan**

"General Manager telah menerima laporan."

Tambahkan informasi:

- Nama laporan.
- Waktu penerimaan.
- Identitas pengguna yang meneruskan.
- Status: Diterima General Manager (DEMO).

Notifikasi ini merupakan representasi penerimaan akhir dalam alur demonstrasi.

Jangan membuat proses menggantung setelah tombol penerusan ditekan.

Jangan mengklaim bahwa notifikasi tersebut merupakan integrasi pengiriman atau penerimaan secara nyata ke sistem General Manager.

# 8. PENCEGAHAN DUPLIKASI DAN KONSISTENSI DATA

Ini merupakan ketentuan wajib untuk seluruh aplikasi.

Manager Produksi, PPIC, QC, dan QA menggunakan alur Manajemen yang sama.

Karena itu, sistem harus mencegah:

- Dua laporan gabungan untuk siklus yang sama.
- Dua konfirmasi SPV untuk laporan yang sama.
- Dua penerusan laporan dari SPV.
- Dua konfirmasi Manajemen untuk laporan yang sama.
- Dua penerusan ke General Manager.
- Data pekerja yang sama masuk dua kali karena tombol ditekan berulang.

Gunakan identitas internal laporan dan siklus sebagai dasar pemeriksaan duplikasi.

Setiap tindakan final harus memiliki pemeriksaan status sebelum disimpan.

Contoh:

Jika PPIC sudah meneruskan laporan:

- Manager Produksi tidak dapat meneruskan ulang.
- QC tidak dapat meneruskan ulang.
- QA tidak dapat meneruskan ulang.
- Semua pengguna dapat melihat status bahwa laporan telah diteruskan.

Identitas pelaksana pertama harus tetap tercatat.

Jangan menimpa identitas pelaksana dengan pengguna yang membuka laporan setelah tindakan dilakukan.

# 9. STATUS WORKFLOW TERPADU

Gunakan status yang konsisten pada seluruh perspektif.

Urutan utama:

1. Belum Dicatat.
2. Sudah Dikirim ke SPV.
3. Menunggu Pemeriksaan SPV.
4. Perlu Perbaikan oleh Pekerja.
5. Menunggu Pemeriksaan Ulang SPV.
6. Dikonfirmasi SPV.
7. Siap Dibuat Laporan Gabungan.
8. Laporan Gabungan Dihasilkan.
9. Diteruskan ke Manajemen.
10. Menunggu Pemeriksaan Manajemen.
11. Perlu Perbaikan oleh SPV.
12. Menunggu Pemeriksaan Ulang Manajemen.
13. Dikonfirmasi Manajemen.
14. Diteruskan ke General Manager.
15. Diterima General Manager (DEMO).

Status tidak boleh berubah secara otomatis tanpa tindakan yang sesuai.

Jangan menganggap laporan sudah selesai hanya karena data pekerja sudah masuk.

Jangan menganggap seluruh 18 tahapan sudah valid hanya karena satu tahapan telah dikonfirmasi.

# 10. STRUKTUR DATA SESSION_STATE

Pertahankan penggunaan session_state sesuai batasan proyek.

Perbaiki struktur data agar setiap laporan memiliki identitas dan status tersendiri.

Data minimal yang perlu disimpan:

A. Identitas laporan:

- report_id.
- cycle_id internal.
- process_id.
- process_name.
- worker_id.
- worker_name.

B. Data input:

- waktu mulai.
- waktu selesai.
- jumlah produksi (kg).
- waktu kedatangan Opening jika relevan.
- pelaksana/pemantau.
- kondisi proses.
- keterangan kendala jika ada.

C. Status pekerja:

- status pengiriman.
- waktu pengiriman.
- waktu batas pengeditan.
- versi laporan.

D. Status SPV:

- status pemeriksaan.
- identitas SPV.
- waktu konfirmasi.
- catatan perbaikan.
- status tugas pemeriksaan kembali.

E. Status Manajemen:

- identitas pemeriksa.
- keputusan.
- catatan perbaikan.
- waktu konfirmasi.
- identitas penerus.

F. Status General Manager:

- status penerimaan demo.
- waktu penerimaan.
- identitas penerus laporan.

Gunakan struktur yang konsisten dan hindari duplikasi penyimpanan data yang sama.

Setiap tindakan harus memperbarui status laporan yang sama, bukan membuat laporan baru yang terpisah.

# 11. UI/UX GLOBAL — REDESIGN MENYELURUH

Lakukan perbaikan pada seluruh halaman.

## 11.1 Layout

Perbaiki:

- Lebar sidebar.
- Margin mainboard.
- Padding.
- Alignment.
- Hierarki judul.
- Jarak antarkomponen.
- Kerapian tabel.
- Konsistensi card.
- Responsivitas.

Kurangi area kosong yang berlebihan.

Jangan membuat halaman terlalu padat.

## 11.2 Typography

Perhatikan:

- Ukuran judul.
- Ukuran subjudul.
- Ukuran teks form.
- Warna teks.
- Kontras.
- Keterbacaan.
- Konsistensi font.

Jangan menggunakan terlalu banyak ukuran font.

## 11.3 Komponen

Gunakan desain konsisten untuk:

- Dropdown.
- Input numerik.
- Input teks.
- Checkbox.
- Tombol utama.
- Tombol sekunder.
- Status.
- Tabel.
- Notifikasi.
- Dialog konfirmasi.

Tombol utama harus terlihat jelas.

Tombol berbahaya atau final harus memerlukan tindakan yang jelas dan tidak mudah tertekan secara tidak sengaja.

## 11.4 Feedback pengguna

Setiap tindakan harus memberikan feedback:

- Berhasil.
- Gagal.
- Menunggu.
- Belum memenuhi syarat.
- Sudah pernah dilakukan.
- Tidak dapat dilakukan karena status laporan.

Jangan membiarkan pengguna menebak apakah tindakan telah berhasil.

Gunakan bahasa Indonesia yang sederhana dan profesional.

# 12. HASIL SIMULASI ARENA — KETENTUAN BACKEND

Hasil simulasi ARENA AS-IS dan TO-BE merupakan bagian penting dari penelitian.

Jangan menghilangkan data hasil simulasi yang sudah tersedia.

Pertahankan:

- Hasil ARENA AS-IS.
- Hasil ARENA TO-BE.
- Perbandingan AS-IS dan TO-BE.
- Time Efficiency.
- KPI yang digunakan dalam penelitian.
- Rincian komponen waktu.
- Sumber perbedaan hasil.
- Catatan metodologi.

Namun, seluruh komponen tersebut tidak ditampilkan langsung pada Dashboard Manajemen.

Sesuai arahan, informasi perbandingan simulasi merupakan data evaluasi penelitian yang berada di backend aplikasi.

Ketentuan:

1. Jangan menghapus data hasil simulasi.
2. Jangan mengarang nilai hasil simulasi.
3. Jangan menghitung ulang dengan angka yang tidak tersedia.
4. Jangan mencampur hasil simulasi dengan data input operasional pekerja.
5. Jangan menampilkan komponen perbandingan ARENA pada dashboard pengguna.
6. Pertahankan pemisahan data penelitian dan data monitoring operasional.
7. Jika hasil ARENA belum tersedia dalam source proyek, jangan membuat angka pengganti.

Perbandingan tersebut tetap dapat digunakan pada bagian evaluasi atau laporan penelitian yang memang memerlukannya.

# 13. PENGUJIAN WAJIB

Lakukan pengujian menyeluruh setelah implementasi.

## A. Login

- Dropdown akun terpisah berdasarkan role.
- Seluruh akun pekerja dapat dipilih.
- SPV dapat login.
- Manager Produksi dapat login.
- PPIC dapat login.
- QC dapat login.
- QA dapat login.
- Login DEMO dapat dilakukan tanpa password.

## B. Pekerja

- Setiap pekerja hanya dapat menginput tahap tanggung jawabnya.
- Opening hanya memiliki pilihan kedatangan 07.00 dan 18.00.
- Waktu mulai dan selesai berfungsi.
- Field Durasi tidak tersedia.
- Jumlah Produksi (kg) berfungsi.
- Pelaksana/Pemantau menggunakan dropdown.
- Kondisi proses berfungsi.
- Keterangan kendala wajib jika kondisi tidak normal.
- Monitoring Pencatatan dihapus.
- Pratinjau Laporan dihapus.
- Pengiriman laporan berhasil.
- Pengeditan dalam enam jam berfungsi.
- Riwayat versi tersimpan.
- Tugas pemeriksaan kembali hanya muncul pada pekerja terkait.

## C. SPV

- Seluruh 18 tahapan muncul.
- Jumlah input dihitung dengan benar.
- Satu input tidak mengesahkan tahapan lain.
- SPV dapat mengonfirmasi setiap tahapan secara terpisah.
- SPV dapat menghubungi pekerja per tahapan.
- Catatan perbaikan wajib diisi.
- Tugas perbaikan diteruskan ke pekerja yang benar.
- Hasil perbaikan kembali ke SPV.
- Generate Report tidak aktif sebelum 18 tahapan valid.
- Generate Report berhasil setelah seluruh persyaratan terpenuhi.
- Laporan gabungan tidak terduplikasi.
- Penerusan ke Manajemen hanya sekali.

## D. Manajemen

- Keempat identitas memiliki akses workflow yang sama.
- Identitas pelaksana tersimpan dengan benar.
- Laporan SPV masuk ke Manajemen.
- Pemeriksaan laporan berfungsi.
- Checkbox wajib berfungsi.
- Keputusan Laporan Diterima berfungsi.
- Keputusan Perlu Perbaikan berfungsi.
- Catatan perbaikan diteruskan ke SPV.
- Pemeriksaan ulang berfungsi.
- Penerusan ke General Manager hanya dapat dilakukan satu kali.
- Jika salah satu identitas telah meneruskan, identitas lainnya tidak dapat meneruskan ulang.
- Notifikasi penerimaan General Manager muncul.

## E. Konsistensi workflow

Uji skenario berikut:

1. Satu pekerja mengirim laporan sementara 17 tahapan lain belum diinput.
2. SPV mengonfirmasi satu tahapan.
3. SPV meminta perbaikan.
4. Pekerja memperbaiki laporan.
5. SPV memeriksa kembali.
6. Seluruh 18 tahapan selesai dan dikonfirmasi.
7. SPV menghasilkan laporan gabungan.
8. SPV meneruskan laporan kepada Manajemen.
9. PPIC melakukan pemeriksaan dan konfirmasi.
10. PPIC meneruskan laporan kepada General Manager.
11. Manager Produksi, QC, dan QA mencoba membuka tindakan penerusan yang sama.
12. Sistem mencegah penerusan ganda.
13. Status akhir menunjukkan laporan diterima General Manager (DEMO).

Uji juga skenario Manajemen meminta perbaikan kepada SPV.

## F. UI/UX

- Login.
- Sidebar.
- Dashboard Pekerja.
- Input Monitoring Produksi.
- Tugas Pemeriksaan Kembali.
- Riwayat Pencatatan.
- Dashboard Pengawasan.
- Monitoring & Kelengkapan Produksi.
- Validasi Laporan.
- Laporan Gabungan.
- Dashboard Manajemen.
- Laporan Masuk.
- Pemeriksaan dan Konfirmasi.
- Penerusan ke General Manager.

Pastikan tidak ada halaman yang membingungkan, tombol duplikat, status yang saling bertentangan, atau navigasi yang berputar.

# 14. WORKFLOW IMPLEMENTASI

Lakukan pekerjaan dalam urutan:

1. Audit implementasi aplikasi yang sekarang.
2. Periksa struktur data session_state.
3. Identifikasi seluruh menu, halaman, fungsi, dan komponen yang terdampak.
4. Susun pemetaan perubahan berdasarkan role.
5. Implementasikan perubahan workflow.
6. Implementasikan perubahan struktur data.
7. Implementasikan perubahan UI/UX.
8. Integrasikan seluruh status dan navigasi.
9. Lakukan pengujian.
10. Perbaiki error.
11. Lakukan evaluasi akhir.

Jangan menghentikan pekerjaan hanya untuk memberikan daftar rekomendasi.

Lakukan implementasi langsung berdasarkan instruksi yang telah diberikan.

Jangan membuat opsi desain tambahan yang tidak diperlukan.

Jangan mengubah proses bisnis yang sudah disepakati.

Jangan menghapus file backup.

Jangan melakukan Git commit, push, atau operasi destruktif tanpa izin.

# 15. HASIL AKHIR YANG DIHARAPKAN

Aplikasi harus mempunyai alur yang jelas:

**PEKERJA**

Login
→ Input Tahapan Masing-Masing
→ Kirim Laporan ke SPV
→ Menunggu Pemeriksaan
→ Perbaikan jika Diperlukan
→ Laporan Dikonfirmasi SPV.

**SPV**

Dashboard Pengawasan
→ Memeriksa 18 Tahapan Secara Individual
→ Konfirmasi atau Minta Perbaikan
→ Seluruh 18 Tahapan Valid
→ Generate Report
→ Buka Laporan Gabungan
→ Teruskan ke Manajemen.

**MANAJEMEN**

Login sebagai Manager Produksi / PPIC / QC / QA
→ Laporan Masuk
→ Pemeriksaan dan Konfirmasi
→ Diterima atau Dikembalikan kepada SPV
→ Laporan Dikonfirmasi
→ Teruskan ke General Manager
→ Notifikasi General Manager Telah Menerima Laporan.

Seluruh proses harus terhubung secara konsisten.

Satu laporan tidak boleh dikonfirmasi atau diteruskan berulang kali.

Setiap pengguna harus dapat mengetahui status laporan berdasarkan tanggung jawabnya.

# INSTRUKSI PENUTUP

Jangan mengutamakan jumlah fitur.

Utamakan:

- Ketepatan workflow.
- Konsistensi data.
- Kejelasan tanggung jawab.
- Kemudahan penggunaan.
- Pencegahan human error.
- Tidak adanya tindakan duplikat.
- Kualitas visual.
- Kesesuaian dengan kebutuhan prototype penelitian.

Jangan membuat pengguna awam harus berpikir keras untuk memahami tombol yang harus ditekan.

Jangan menyamakan input satu pekerja dengan penyelesaian seluruh 18 tahapan.

Jangan menyamakan laporan yang sudah dikirim dengan laporan yang sudah divalidasi.

Jangan menyamakan laporan yang sudah divalidasi SPV dengan laporan yang sudah diterima Manajemen.

Jangan menghilangkan data penelitian ARENA AS-IS dan TO-BE.

Hasil akhir harus berupa prototype POLEKO Production Monitoring System yang memiliki alur kerja lengkap dari input pekerja hingga penerimaan laporan oleh General Manager dalam demonstrasi.