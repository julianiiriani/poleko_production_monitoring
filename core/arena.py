"""Data hasil simulasi ARENA AS-IS vs TO-BE (data penelitian, bukan data monitoring operasional).

Sesuai Revisi 03 November 2026 (bagian 12), hasil ini DIPERTAHANKAN di backend aplikasi tetapi TIDAK ditampilkan pada dashboard
pengguna mana pun. Tidak ada halaman yang memanggil modul ini; ia disimpan untuk bagian evaluasi/laporan penelitian.

Seluruh angka adalah hasil run final ARENA yang tercantum di master prompt (Bagian III, R2-R5), disimpan sebagai teks
persis seperti dokumen (format Indonesia). Modul ini TIDAK membaca st.session_state/data demo, TIDAK menghitung ulang
simulasi, dan TIDAK terhubung ke ARENA. Nilai tidak boleh dicampur dengan data input operasional pekerja.

Pembedaan wajib: 3,21% adalah penurunan total waktu simulasi TO-BE terhadap AS-IS. Itu BUKAN Time Efficiency
berbasis formula, yang tetap "Belum Dihitung".
"""
import pandas as pd

TITLE = "Perbandingan Hasil Simulasi ARENA (AS-IS vs TO-BE)"

# R5 — perbandingan final (menit, jam, hari = 24 jam).
ASIS_MENIT, ASIS_JAM, ASIS_HARI = "6.639,454968", "110,657583", "4,610733"
TOBE_MENIT, TOBE_JAM, TOBE_HARI = "6.426", "107,1", "4,4625"
SELISIH_MENIT, SELISIH_JAM = "213,454968", "3,557583"
TURUN_PCT, TURUN_PCT_BULAT = "3,2149", "3,21"
SELISIH_B, SELISIH_P22 = "93,454968", "120"  # sumber selisih (R5)

# R2 — durasi A1-A18 (menit), sama pada kedua model.
A_ITEMS = [
    ("A1", "Opening", "60"), ("A2", "Sortiran Awal", "30"), ("A3", "Bodega", "1.440"), ("A4", "Shelling & Paring", "60"),
    ("A5", "Pencucian & Sortir Kedua", "15"), ("A6", "Penyiraman & Penampungan", "10"), ("A7", "Grinding", "60"),
    ("A8", "Sterilisasi", "10"), ("A9", "Drying", "55"), ("A10", "Grading", "10"), ("A11", "Picking", "20"),
    ("A12", "Sampling & QC", "10"), ("A13", "Packing", "10"), ("A14", "Weighting", "10"), ("A15", "Sealing & Sewing", "10"),
    ("A16", "Bag Flattener", "10"), ("A17", "Metal Detector", "10"), ("A18", "Penyimpanan Produk Sebelum Pengiriman", "4.320"),
]
A_TOTAL = "6.150"

# R3 — B1-B18 AS-IS (monitoring manual, Uniform 5-10 menit; nilai hasil run). R4 — TO-BE: Constant 2 menit per input digital.
B_ASIS = [
    ("B1", "Opening", "6,462976179"), ("B2", "Sortiran Awal", "6,796586886"), ("B3", "Bodega", "6,184005062"),
    ("B4", "Shelling & Paring", "5,291984137"), ("B5", "Pencucian & Sortir Kedua", "5,656151490"),
    ("B6", "Penyiraman & Penampungan", "5,587040957"), ("B7", "Grinding", "9,712319272"), ("B8", "Sterilisasi", "7,734798649"),
    ("B9", "Drying", "9,266621767"), ("B10", "Grading", "9,208052736"), ("B11", "Picking", "5,657981650"),
    ("B12", "Sampling & QC", "9,101745266"), ("B13", "Packing", "9,775365472"), ("B14", "Weighting", "5,570221685"),
    ("B15", "Sealing & Sewing", "7,339535794"), ("B16", "Bag Flattener", "7,683257330"), ("B17", "Metal Detector", "6,484334127"),
    ("B18", "Penyimpanan Produk Sebelum Pengiriman", "5,941989923"),
]
B_ASIS_TOTAL, B_TOBE_EACH, B_TOBE_TOTAL = "129,454968", "2", "36"

# R3/R4 — P19-P22: (kode, aktivitas AS-IS, menit AS-IS, aktivitas TO-BE, menit TO-BE, catatan)
P_ITEMS = [
    ("P19", "Penyerahan Laporan", "0", "Menyusun Laporan Otomatis", "0", "Placeholder 0 menit pada kedua run."),
    ("P20", "Pengumpulan Laporan", "240", "Validasi Laporan", "240", "240 menit pada kedua model; tidak ada perbaikan waktu pada P20."),
    ("P21", "Rekapitulasi Data", "0", "Periksa/Konfirmasi Laporan", "0", "Placeholder 0 menit pada kedua run."),
    ("P22", "Rekonsiliasi Data", "120", "Pemeriksaan Kembali/Koreksi", "120 (tidak dijalankan)",
     "Dijalankan satu kali pada AS-IS. Pada TO-BE tetap tersedia sebagai jalur pengecualian, tetapi tidak dijalankan pada jalur utama."),
]

CAVEATS = [
    "Masing-masing model dijalankan dengan satu replikasi. Angka ini hasil run skenario, bukan rata-rata replikasi berulang. "
    "Confidence level 95% yang disetel tidak membuat satu replikasi cukup untuk menyimpulkan signifikansi statistik.",
    "Total waktu adalah hasil model berdasarkan alur dan parameter yang digunakan, bukan pengukuran aktual di lapangan atau setelah aplikasi diterapkan.",
    "Constant 2 menit per input digital pada TO-BE adalah asumsi skenario, bukan hasil pengukuran. "
    "Jangan dibaca sebagai batas atau target waktu pengisian pekerja.",
    "P22 (pemeriksaan kembali/koreksi) tetap ada sebagai jalur pengecualian TO-BE. Tidak dijalankannya P22 pada jalur utama tidak berarti "
    "mekanisme koreksi dihapus; fitur Perlu Perbaikan di aplikasi tetap tersedia.",
    "P19 dan P21 bernilai 0 menit sebagai placeholder, bukan bukti bahwa kegiatannya tidak memerlukan waktu.",
    "Satu entity mewakili satu batch produksi 10 ton dan satu siklus produksi. Panel ini tidak berubah mengikuti data demo dan bukan data produksi aktual.",
]


def summary_df():
    return pd.DataFrame(
        [
            {"Komponen": "A1–A18", "AS-IS (menit)": A_TOTAL, "TO-BE (menit)": A_TOTAL, "Selisih (menit)": "0",
             "Keterangan": "Durasi tahapan produksi, sama pada kedua model."},
            {"Komponen": "B1–B18", "AS-IS (menit)": B_ASIS_TOTAL, "TO-BE (menit)": B_TOBE_TOTAL, "Selisih (menit)": SELISIH_B,
             "Keterangan": "AS-IS: monitoring manual, Uniform 5–10 menit. TO-BE: input digital, Constant 2 menit × 18 (asumsi skenario)."},
            *[
                {"Komponen": code, "AS-IS (menit)": asis_min, "TO-BE (menit)": "0 (tidak dijalankan)" if code == "P22" else tobe_min,
                 "Selisih (menit)": SELISIH_P22 if code == "P22" else "0", "Keterangan": note}
                for code, _, asis_min, _, tobe_min, note in P_ITEMS
            ],
            {"Komponen": "Total waktu entity", "AS-IS (menit)": ASIS_MENIT, "TO-BE (menit)": TOBE_MENIT, "Selisih (menit)": SELISIH_MENIT,
             "Keterangan": "1 entity = 1 batch produksi 10 ton."},
        ]
    )
