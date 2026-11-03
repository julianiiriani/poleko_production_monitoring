# POLEKO Production Monitoring System
Streamlit-based production monitoring system for PT Royal Coconut Airmadidi (POLEKO).

## Status: Fase 1 — Prototipe UI/UX (tanpa backend)

Prototipe antarmuka proses **To-Be** hasil perancangan ulang monitoring aktivitas produksi.
Tidak ada database, autentikasi nyata, atau data operasional. Semua data yang muncul adalah
**DEMO** yang hanya tersimpan di `st.session_state` sesi saat ini: tidak dibagi antar pengguna atau perangkat,
dapat hilang saat browser di-refresh atau sesi berakhir, dan dihapus eksplisit lewat **Reset DEMO**
(tombol Keluar tidak menghapusnya). "Real-time" hanya berarti tampilan ikut berubah dalam sesi demo.

Jalankan:

```
.venv\Scripts\python.exe -m streamlit run app.py
```

## Tiga perspektif (Navy / Purple / Gold)

| Perspektif | Warna | Fungsi |
|---|---|---|
| Pekerja / Pelaksana Produksi | Navy `#0B2545` | Satu-satunya pihak yang melakukan input awal, hanya untuk tahapan yang ditugaskan; mengerjakan tugas pemeriksaan kembali |
| SPV Produksi | Purple `#6B3FA0` | Tidak menginput. Memantau kelengkapan 18 tahapan, satu keputusan TRUE/FALSE per siklus, penugasan pemeriksaan kembali, laporan gabungan, meneruskan ke PPIC |
| Manajer Produksi / PPIC / QC / QA | Gold `#D6A62A` | Menerima laporan, memantau, memeriksa, mengonfirmasi, meneruskan ke General Manager (penerima, bukan peran login) |

Menu setiap perspektif berbeda. Ini navigasi demonstrasi, bukan keamanan akses produksi.

## Alur

Pekerja input per tahapan → SPV memantau kelengkapan 18 tahapan →
- **FALSE**: SPV memilih tahapan + catatan wajib → tugas ke Pekerja yang menginput tahapan itu → Pekerja kirim ulang → SPV meninjau.
- **TRUE** (hanya bila 18 tahapan lengkap dan tidak ada tugas yang belum selesai): satu laporan gabungan dihasilkan → SPV meneruskan ke PPIC → Manajemen memeriksa dan mengonfirmasi → meneruskan ke General Manager (DEMO).

Status catatan tahapan dan status laporan gabungan dipisahkan (`core/data.py`).

## Struktur

| Path | Isi |
|---|---|
| `app.py` | Router `st.navigation` per perspektif, sidebar, kontrol DEMO, gerbang login demo |
| `views/` | `login.py`, `pekerja_*` (4), `spv_*` (9), `mgr_*` (6). Sengaja bukan `pages/`: folder itu ditemukan otomatis oleh Streamlit sehingga URL langsung menjalankan skrip tanpa melewati `app.py` |
| `core/data.py` | Daftar 18 tahapan (satu sumber), peran + warna, profil pekerja DEMO dan penugasannya (`DEMO_WORKERS`, mudah diganti), status, opsi formulir |
| `core/state.py` | State sesi sementara dan seluruh transisi alur (penugasan ditegakkan di `submit_record`/`resubmit_task`) |
| `core/ui.py` | CSS dan komponen bersama |
| `assets/wordmark.svg` | Identitas teks (bukan logo resmi) |
| `database.py` | Kosong — dicadangkan untuk fase backend |

## Catatan penelitian

- Time Efficiency = *Belum Dihitung*; tidak ada angka karena parameter ARENA belum dikonfigurasi.
- Field input Pekerja mengacu pada **Formulir Pengumpulan Data Ke-2** (bagian B): waktu mulai, waktu selesai, durasi,
  pelaksana/pemantau, kondisi proses, monitoring/pencatatan, catatan. Formulir itu formulir pengumpulan data penelitian (As-Is),
  bukan formulir operasional; pemakaiannya sebagai form input Pekerja adalah usulan prototipe. Tidak ada kuantitas, satuan, atau hasil mutu karangan.
- Tahap 4 ditulis "Shelling & Paring" (formulir resmi dan master prompt). Diagram BPMN menulis "Pairing"; selisih ini dilaporkan, BPMN tidak diubah.
- Profil pekerja, penugasan tahapan, dan ID siklus adalah **DEMO**, bukan pegawai atau data resmi POLEKO.
- Aturan wajib isi pada form hanya aturan interaksi prototipe ("Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO").
