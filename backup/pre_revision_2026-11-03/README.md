# POLEKO — Production Monitoring System
Aplikasi Streamlit untuk PT Royal Coconut Airmadidi (POLEKO).

## Status: Fase 1 — prototipe UI/UX (tanpa backend)

Prototipe antarmuka proses **To-Be** monitoring aktivitas produksi. Tidak ada database, backend, API, integrasi mesin ARENA,
atau autentikasi produksi. Semua data yang muncul adalah **data demo** yang hanya tersimpan di `st.session_state` sesi
saat ini: tidak dibagi antar pengguna atau perangkat, dan hilang saat browser di-refresh atau sesi berakhir.
Menu **Keluar** tidak menghapus data; **Reset Demo** menghapusnya (dengan konfirmasi). Aplikasi mulai dalam keadaan kosong.

Jalankan:

```
.venv\Scripts\python.exe -m streamlit run app.py
```

## Login (DEMO)

Pilih akun dari dropdown lalu tekan **Login**. Kolom password tersedia, tetapi isinya belum ditentukan sehingga **boleh dikosongkan**
dan tidak diperiksa. Login ini hanya demonstrasi, bukan sistem keamanan produksi.
Daftar akun dikonfigurasi di `core/data.py` (`DEMO_ACCOUNTS`).

| Akun | Perspektif |
|---|---|
| Pekerja DEMO 01 … Pekerja DEMO 18 (satu pekerja untuk satu tahapan; DEMO 04 = tahap 04 Shelling & Paring, dst.) | Pekerja Produksi |
| SPV Produksi DEMO | SPV Produksi |
| Manager Produksi, PPIC, QC, QA | Manajemen |

Keempat identitas Manajemen memakai alur dan menu yang sama. Identitas yang dipakai saat login dicatat sebagai
pelaksana **konfirmasi** dan **penerusan ke General Manager**, dan tampil di Riwayat Laporan.

## Tiga perspektif

| Perspektif | Warna | Menu |
|---|---|---|
| Pekerja Produksi | Navy `#0B2545` | Dashboard Pekerja, Input Monitoring Produksi, Tugas Pemeriksaan Kembali, Riwayat Pencatatan |
| SPV Produksi | Purple `#6B3FA0` | Dashboard Pengawasan, Monitoring & Kelengkapan Produksi, Ringkasan Hasil per Tahapan, Riwayat Hasil Monitoring, Validasi Laporan, Penugasan Pemeriksaan Kembali, Laporan Gabungan |
| Manajemen | Gold `#D6A62A` | Dashboard Manajemen, Monitoring Real-Time, Laporan Masuk, Pemeriksaan dan Konfirmasi, Penerusan ke General Manager, Riwayat Laporan |

General Manager hanya penerima laporan, bukan akun login.

## Alur

Pekerja menginput tahapannya → SPV memantau kelengkapan 18 tahapan dan membuat satu keputusan per siklus:
- **Perlu Perbaikan**: SPV memilih tahapan, wajib menulis catatan, memeriksa ringkasan penugasan, lalu mengirim. Tugas masuk ke
  Pekerja penanggung jawab, yang memeriksa dan mengirim ulang (versi sebelumnya tetap tersimpan). SPV meninjau hasilnya.
- **Laporan Diterima** (hanya jika 18 tahapan lengkap dan tidak ada pemeriksaan ulang yang tertunda): satu laporan gabungan
  dihasilkan → SPV meneruskan ke PPIC → Manajemen memeriksa dan mengonfirmasi → meneruskan ke General Manager (DEMO).

## Kontrol Demo (sidebar)

**Skenario Demo** (dropdown) → **Muat Data Demo** → **Reset Demo** (dengan konfirmasi). Skenario: *Siklus Lengkap — Siap Divalidasi SPV*
(DEMO-SIKLUS-001), *Siklus Belum Lengkap — 15 dari 18 Tahapan* (DEMO-SIKLUS-002), *Laporan Sudah Masuk ke Manajemen*
(DEMO-SIKLUS-003), dan *Semua Skenario* (ketiga siklus, tanpa mencampur status dalam satu siklus). Memuat skenario yang sama
dua kali tidak menggandakan data. Isi data demo sengaja netral (waktu, pelaksana, dan jumlah kg tidak diisi).

## Struktur

| Path | Isi |
|---|---|
| `app.py` | Router `st.navigation` (menu samping dibuat sendiri per perspektif), sidebar, Kontrol Demo, gerbang login demo |
| `views/` | `login.py`, `pekerja_*` (4), `spv_*` (7), `mgr_*` (6). Sengaja bukan `pages/` agar URL langsung tidak melewati `app.py` |
| `core/data.py` | Daftar 18 tahapan (satu sumber), peran + warna, akun DEMO, penanggung jawab tahapan DEMO, status, opsi formulir |
| `core/state.py` | State sesi sementara dan seluruh transisi alur (aturan ditegakkan di logika, bukan hanya tampilan) |
| `core/ui.py` | CSS dan komponen bersama |
| `assets/` | Tempat logo resmi (lihat di bawah) |
| `backup/` | Arsip: `old_views_phase1/` (halaman versi lama) dan `pre_ux_revision_2026-11-01/` (kode sebelum revisi UX) |
| `database.py` | Kosong — dicadangkan untuk fase backend |

## Logo

Letakkan file logo resmi PT Royal Coconut di folder `assets/` dengan nama yang memuat kata `logo` (mis. `assets/logo_royal_coconut.png`;
format png, jpg, jpeg, webp, atau svg). Aplikasi memakainya otomatis di sidebar dan halaman login, memangkas ruang kosong di tepinya
tanpa mengubah bentuk. Selama file belum ada, aplikasi hanya menampilkan judul teks "POLEKO — Production Monitoring System"
(bukan logo tiruan). `assets/wordmark.svg` adalah berkas lama dan tidak dipakai.

## Catatan penelitian dan asumsi

- Field input Pekerja mengacu pada **Formulir Pengumpulan Data Ke-2** (bagian B): waktu mulai, waktu selesai, durasi, pelaksana/pemantau,
  kondisi proses, monitoring/pencatatan, catatan. **Jumlah Produksi (kg)** ditambahkan atas instruksi revisi (tidak ada pada formulir itu);
  nilainya angka ≥ 0 dan disimpan per versi catatan. Formulir tersebut adalah formulir pengumpulan data penelitian (As-Is);
  pemakaiannya sebagai form input Pekerja adalah usulan prototipe. Tidak ada field lain (standar kualitas, target, dst.).
- Aturan wajib isi pada form hanya aturan interaksi prototipe ("Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO").
- **Penanggung jawab tahapan** (`DEMO_WORKERS` di `core/data.py`): satu tahapan = satu pekerja (konfirmasi tim peneliti). Nama "Pekerja DEMO NN"
  hanya placeholder, bukan nama pegawai POLEKO; cukup diganti di satu tempat bila nama atau penugasan resmi sudah ada.
- Tahap 4 ditulis "Shelling & Paring". Diagram BPMN menulis "Pairing"; BPMN tidak diubah.
- Komponen lama Dashboard Manajemen (Gambaran 18 Tahapan, kartu Time Efficiency, dropdown Rumus Awal dan Status ARENA) sudah dihapus
  dan tidak dikembalikan. Penggantinya adalah panel **Perbandingan Hasil Simulasi ARENA (AS-IS vs TO-BE)** di bagian bawah
  Dashboard Manajemen (`core/arena.py`): hasil final run ARENA yang tercantum di master prompt Bagian III, ditampilkan **statis dan
  read-only**. Panel tidak membaca data demo, tidak berubah mengikuti input, tidak terhubung ke ARENA, dan tidak menghitung ulang simulasi.
  Isinya: total AS-IS 6.639,454968 menit dan TO-BE 6.426 menit, selisih 213,454968 menit, penurunan total waktu simulasi 3,21%,
  rincian A1–A18, B1–B18, P19–P22, sumber selisih, dan catatan metodologi (satu replikasi; 2 menit adalah asumsi skenario; P22 tetap jalur
  pengecualian). **3,21% bukan Time Efficiency.** Time Efficiency berbasis formula tetap "Belum Dihitung".
- Mengganti angka panel: ubah konstanta di `core/arena.py` (teks sengaja ditulis persis seperti dokumen penelitian).
- **Validasi Laporan** menampilkan draf laporan gabungan (18 tahapan, semua field) agar SPV dapat memeriksa isinya sebelum memutuskan.
  Draf tidak disimpan dan bukan laporan resmi; laporan resmi baru dibuat saat SPV memilih Laporan Diterima.
- Catatan yang berasal dari **Muat Data Demo** ditandai "data contoh" di tabel monitoring dan laporan. Tanda itu hilang bila Pekerja
  mengirim ulang isiannya (isian terbaru berasal dari pengguna).
- Istilah status: Belum Dicatat → Menunggu Validasi SPV → Perlu Perbaikan → Sudah Diperbaiki — Menunggu SPV → Termasuk Laporan Gabungan.
