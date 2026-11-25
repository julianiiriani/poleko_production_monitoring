# POLEKO — Production Monitoring System
Aplikasi Streamlit untuk PT Royal Coconut Airmadidi (POLEKO).

## Status: Fase 1 — prototipe UI/UX (tanpa backend) · Revisi 03 November 2026

Prototipe antarmuka proses **To-Be** monitoring aktivitas produksi. Tidak ada database, backend, API, integrasi mesin ARENA,
atau autentikasi produksi. Semua data yang muncul hanya tersimpan di `st.session_state` sesi saat ini: tidak dibagi antar
pengguna atau perangkat, dan hilang saat browser di-refresh atau sesi berakhir. Menu **Keluar** tidak menghapus data. Aplikasi
mulai dalam keadaan kosong dan tidak ada lagi Kontrol Demo (Muat Data Demo / Reset Demo) maupun pilihan Siklus Produksi:
seluruh data dibuat dengan menjalankan alurnya sendiri (login sebagai tiap pekerja, SPV, lalu Manajemen).

Jalankan:

```
.venv\Scripts\python.exe -m streamlit run app.py
```

## Login (DEMO)

Pilih kelompok (**Pekerja Produksi**, **SPV Produksi**, **Manajemen**), pilih akun pada dropdown kelompok itu, lalu tekan **Login**.
Kolom password tersedia (placeholder "Masukkan password.") tetapi boleh dikosongkan dan tidak diperiksa. Login ini hanya
demonstrasi, bukan sistem keamanan produksi. Daftar akun ada di `core/data.py` (`DEMO_ACCOUNTS`).

| Kelompok | Akun |
|---|---|
| Pekerja Produksi | Pekerja 01 — Opening … Pekerja 18 — Penyimpanan Produk Sebelum Pengiriman (satu pekerja = satu tahapan) |
| SPV Produksi | SPV Produksi |
| Manajemen | Manager Produksi, PPIC, QC, QA (satu perspektif, alur dan kewenangan sama) |

Identitas Manajemen yang dipakai saat login dicatat sebagai pelaksana pemeriksaan, konfirmasi, dan penerusan ke General Manager.
General Manager hanya penerima laporan, bukan akun login.

## Alur

1. **Pekerja** menginput tahapannya sendiri (Waktu Mulai/Selesai; Waktu Kedatangan Bahan Baku 07.00/18.00 khusus Opening; Jumlah
   Produksi kg; Pelaksana/Pemantau; Kondisi Proses; penjelasan kendala wajib bila kondisi bukan Normal). Durasi dihitung otomatis.
   Tombol **Kirim Laporan ke SPV**. Pekerja boleh mengedit sampai 6 jam sejak pengiriman selama SPV belum mengonfirmasi (aturan
   akses prototipe, bukan kebijakan perusahaan); tiap perubahan menjadi versi baru dan versi awal tidak ditimpa.
2. **SPV** memeriksa tiap tahapan secara individual di **Validasi Laporan**: *Konfirmasi Tahapan* (mengunci laporan pekerja) atau
   *Hubungi Pekerja* (catatan wajib; membuat tugas pemeriksaan kembali untuk pekerja penanggung jawab). Hasil perbaikan kembali ke
   SPV sebagai "Menunggu Pemeriksaan Ulang SPV" dan tidak otomatis valid.
3. **Generate Report** (Validasi Laporan) aktif hanya bila 18 tahapan sudah dikonfirmasi, tanpa Perlu Perbaikan, tanpa tugas terbuka,
   tanpa pemeriksaan ulang tertunda, dan data wajib lengkap. Bila belum, alasan dan jumlah tahapan yang belum memenuhi syarat ditampilkan.
   Satu laporan gabungan per siklus. SPV lalu menekan satu-satunya tombol **Teruskan ke Manajemen** di Laporan Gabungan.
4. **Manajemen** memeriksa laporan (Laporan Masuk → Pemeriksaan dan Konfirmasi): centang pernyataan sudah diperiksa, lalu
   *Laporan Diterima* (Konfirmasi Laporan) atau *Perlu Perbaikan* (Catatan Perbaikan untuk SPV wajib; laporan kembali ke SPV, yang dapat
   membuka kembali tahapan, memperbaiki, dan mengirim ulang dengan tanggapan). Setelah dikonfirmasi: **Teruskan ke General Manager**
   (satu kali; pelaksana pertama tidak ditimpa) dan muncul notifikasi "Laporan Berhasil Diteruskan" dengan status
   *Diterima General Manager (DEMO)*. Notifikasi ini representasi demonstrasi, bukan integrasi nyata.

Tindakan final (Generate Report, penerusan, konfirmasi, penerusan ke GM) meminta konfirmasi lewat dialog. Setiap tindakan final memeriksa
status lebih dulu sehingga klik berulang atau identitas lain tidak dapat menggandakannya.

## Menu

| Perspektif | Menu |
|---|---|
| Pekerja Produksi | Dashboard Pekerja, Input Monitoring Produksi, Tugas Pemeriksaan Kembali, Riwayat Pencatatan |
| SPV Produksi | Dashboard Pengawasan, Monitoring & Kelengkapan Produksi, Validasi Laporan, Laporan Gabungan |
| Manajemen | Dashboard Manajemen, Monitoring Real-Time, Laporan Masuk, Pemeriksaan dan Konfirmasi, Penerusan ke General Manager, Riwayat Laporan |

Warna perspektif: Pekerja navy `#0B2545`, SPV purple `#6B3FA0`, Manajemen gold `#D6A62A`.

## Struktur

| Path | Isi |
|---|---|
| `app.py` | Router `st.navigation` (menu samping dibuat sendiri per perspektif), sidebar, gerbang login demo |
| `views/` | `login.py`, `pekerja_*` (4), `spv_*` (4), `mgr_*` (6). Sengaja bukan `pages/` agar URL langsung tidak melewati `app.py` |
| `core/data.py` | Daftar 18 tahapan (satu sumber), peran + warna, akun DEMO, penanggung jawab tahapan, status, opsi formulir |
| `core/state.py` | State sesi sementara dan seluruh transisi alur (aturan ditegakkan di logika, bukan hanya tampilan) |
| `core/ui.py` | CSS dan komponen bersama |
| `core/arena.py` | Data hasil simulasi ARENA AS-IS vs TO-BE (data penelitian, backend; tidak ditampilkan di UI) |
| `assets/` | Tempat logo resmi (lihat di bawah) |
| `backup/` | Arsip: `old_views_phase1/`, `pre_ux_revision_2026-11-01/`, `pre_revision_2026-11-03/` (kode sebelum revisi ini), `obsolete_views_2026-11-03/` (halaman SPV yang digabung) |
| `database.py` | Kosong — dicadangkan untuk fase backend |

## Logo

Letakkan file logo resmi PT Royal Coconut di folder `assets/` dengan nama yang memuat kata `logo` (mis. `assets/logo_royal_coconut.png`;
format png, jpg, jpeg, webp, atau svg). Aplikasi memakainya otomatis di sidebar dan halaman login (kiri atas), memangkas ruang kosong di
tepinya tanpa mengubah bentuk. Selama file belum ada, aplikasi hanya menampilkan judul teks "POLEKO — Production Monitoring System"
(bukan logo tiruan). `assets/wordmark.svg` adalah berkas lama dan tidak dipakai.

## Catatan penelitian dan asumsi

- Field input Pekerja mengacu pada **Formulir Pengumpulan Data Ke-2** (bagian B) dan Revisi 03 November 2026. **Jumlah Produksi (kg)**
  adalah tambahan dari instruksi revisi; nilainya angka ≥ 0 dan disimpan per versi. Tidak ada field lain (standar kualitas, target, dst.).
- Aturan wajib isi pada form hanya aturan interaksi prototipe ("Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO").
- **Penanggung jawab tahapan** (`DEMO_WORKERS` di `core/data.py`): satu tahapan = satu pekerja. "Pekerja NN" hanya penanda akun demo, bukan
  nama pegawai POLEKO; cukup diganti di satu tempat bila nama resmi sudah ada. Kode Tahapan ditampilkan sebagai `T` + nomor tahap (format tampilan).
- **Tanggal produksi** pada laporan gabungan diambil dari tanggal pencatatan pertama pada siklus (aplikasi tidak memiliki field tanggal terpisah).
- Identitas siklus (`SIKLUS-001`) hanya dipakai internal untuk mengelompokkan 18 laporan dan mencegah pencampuran/duplikasi; tidak ada menu
  atau dropdown siklus. Karena itu satu sesi memproses satu siklus; untuk mengulang demonstrasi, segarkan (refresh) browser.
- Tahap 4 ditulis "Shelling & Paring". Diagram BPMN menulis "Pairing"; BPMN tidak diubah.
- **Hasil simulasi ARENA** (AS-IS 6.639,454968 menit; TO-BE 6.426 menit; selisih 213,454968 menit; penurunan total waktu simulasi 3,21%, rincian
  A1–A18, B1–B18, P19–P22, catatan metodologi) tetap disimpan di `core/arena.py` sebagai data penelitian, tetapi **tidak ditampilkan pada
  dashboard pengguna mana pun** (Revisi 03 November 2026, bagian 12). Panel ARENA yang sebelumnya ada di Dashboard Manajemen sudah dilepas dari
  UI. Angka 3,21% bukan Time Efficiency berbasis formula; Time Efficiency tetap "Belum Dihitung".
- Istilah status tahapan: Belum Dicatat → Menunggu Pemeriksaan SPV → Perlu Perbaikan oleh Pekerja → Menunggu Pemeriksaan Ulang SPV → Dikonfirmasi SPV.
  Status laporan gabungan: Laporan Gabungan Dihasilkan → Menunggu Pemeriksaan Manajemen → (Perlu Perbaikan oleh SPV → Menunggu Pemeriksaan Ulang
  Manajemen) → Dikonfirmasi Manajemen → Diterima General Manager (DEMO).
