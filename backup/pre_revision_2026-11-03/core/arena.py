"""Panel read-only "Perbandingan Hasil Simulasi ARENA (AS-IS vs TO-BE)" untuk Dashboard Manajemen.

Seluruh angka adalah hasil run final ARENA yang tercantum di master prompt (Bagian III, R2-R5), disimpan sebagai teks
persis seperti dokumen (format Indonesia). Modul ini TIDAK membaca st.session_state/data demo, TIDAK menghitung ulang
simulasi, dan TIDAK terhubung ke ARENA. Nilai hanya ditampilkan; kecocokan antar-angka diperiksa di pengujian, bukan saat tampil.

Pembedaan wajib: 3,21% adalah penurunan total waktu simulasi TO-BE terhadap AS-IS. Itu BUKAN Time Efficiency
berbasis formula, yang tetap "Belum Dihitung".
"""
import pandas as pd
import streamlit as st

from core import data, ui

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


def _summary_df():
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


SCALE = 6639.454968  # hanya skala gambar batang (= total AS-IS); bukan perhitungan hasil


def _bar(label, parts, total_label):
    """Batang bertumpuk sederhana; lebar relatif terhadap total AS-IS agar kedua batang sebanding. Angka ada di legenda dan tabel."""
    segs = "".join(
        f'<div class="seg" style="width:{w / SCALE * 100:.3f}%;background:{color}" title="{ui.esc(name)}: {ui.esc(val)} menit"></div>'
        for name, val, w, color in parts
    )
    return f'<div class="row"><div class="lab">{ui.esc(label)}</div><div class="bar">{segs}</div><div class="tot">{ui.esc(total_label)}</div></div>'


def render():
    st.subheader(TITLE)
    st.markdown(
        '<span class="pk-chip">Hasil penelitian · statis</span> <span class="pk-chip warn">Bukan data produksi aktual · bukan KPI real-time</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="pk-te"><b>Time Efficiency (KPI berbasis formula)</b><span class="pk-badge" style="color:#475569;background:#F1F5F9;border-color:#47556955">'
        "Belum Dihitung</span>"
        f"<span class=\"x\">Angka {TURUN_PCT_BULAT}% di bawah adalah penurunan total waktu simulasi, bukan Time Efficiency.</span></div>",
        unsafe_allow_html=True,
    )

    ui.stat_grid(
        [
            ("Total waktu AS-IS", ASIS_MENIT, "#64748B", "menit", f"{ASIS_JAM} jam · sekitar {ASIS_HARI} hari"),
            ("Total waktu TO-BE", TOBE_MENIT, data.ROLE_COLOR[data.ROLE_PEKERJA], "menit", f"{TOBE_JAM} jam · {TOBE_HARI} hari"),
            ("Selisih total waktu", SELISIH_MENIT, "#0F766E", "menit", f"sekitar {SELISIH_JAM} jam"),
            ("Penurunan total waktu simulasi", f"{TURUN_PCT_BULAT}%", "#0F766E", "", f"{TURUN_PCT}% terhadap AS-IS"),
        ],
        min_width=220,
    )

    # Komposisi total waktu: A (tahapan) | B (pencatatan) | P20 | P22. Warna dilengkapi legenda berlabel angka.
    asis_parts = [("A1–A18", A_TOTAL, 6150, "#94A3B8"), ("B1–B18", B_ASIS_TOTAL, 129.5, "#D6A62A"), ("P20", "240", 240, "#475569"), ("P22", "120", 120, "#B91C1C")]
    tobe_parts = [("A1–A18", A_TOTAL, 6150, "#94A3B8"), ("B1–B18", B_TOBE_TOTAL, 36, "#D6A62A"), ("P20", "240", 240, "#475569")]
    st.markdown(
        '<div class="pk-arenabar"><div class="cap">Komposisi total waktu (skala sama untuk kedua model)</div>'
        + _bar("AS-IS", asis_parts, f"{ASIS_MENIT} menit")
        + _bar("TO-BE", tobe_parts, f"{TOBE_MENIT} menit")
        + '<div class="leg"><span><i style="background:#94A3B8"></i>A1–A18 (6.150)</span><span><i style="background:#D6A62A"></i>B1–B18 '
        f'(AS-IS {B_ASIS_TOTAL} · TO-BE {B_TOBE_TOTAL})</span><span><i style="background:#475569"></i>P20 (240)</span>'
        '<span><i style="background:#B91C1C"></i>P22 (120, hanya AS-IS)</span></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("##### Rincian komponen (menit)")
    ui.table(_summary_df())

    st.markdown(
        '<div class="pk-note-box"><b>Sumber selisih</b><br>'
        f"1. Perbedaan waktu B1–B18: {B_ASIS_TOTAL} − {B_TOBE_TOTAL} = <b>{SELISIH_B} menit</b>.<br>"
        f"2. Perbedaan jalur P22: dijalankan {SELISIH_P22} menit pada AS-IS, tidak dijalankan pada jalur utama TO-BE = <b>{SELISIH_P22} menit</b>.<br>"
        f"Total {SELISIH_B} + {SELISIH_P22} = <b>{SELISIH_MENIT} menit</b>. "
        f"Karena itu penurunan {TURUN_PCT_BULAT}% tidak seluruhnya berasal dari digitalisasi input: hanya sekitar {SELISIH_B} menit yang berkaitan "
        "dengan perubahan B1–B18, sisanya dari P22.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("##### Catatan metodologi")
    st.markdown("\n".join(f"- {c}" for c in CAVEATS))

    with st.expander("Rincian A1–A18 (sama pada kedua model)"):
        ui.table(pd.DataFrame([{"Kode": c, "Tahapan": n, "Durasi (menit)": d} for c, n, d in A_ITEMS] + [{"Kode": "Jumlah", "Tahapan": "A1–A18", "Durasi (menit)": A_TOTAL}]))
    with st.expander("Rincian B1–B18 (monitoring manual AS-IS vs input digital TO-BE)"):
        ui.table(
            pd.DataFrame(
                [{"Kode": c, "Tahapan": n, "AS-IS (menit)": v, "TO-BE (menit)": B_TOBE_EACH} for c, n, v in B_ASIS]
                + [{"Kode": "Jumlah", "Tahapan": "B1–B18", "AS-IS (menit)": B_ASIS_TOTAL, "TO-BE (menit)": B_TOBE_TOTAL}]
            )
        )
    with st.expander("Rincian P19–P22"):
        ui.table(
            pd.DataFrame(
                [{"Kode": c, "Aktivitas AS-IS": a, "AS-IS (menit)": am, "Aktivitas TO-BE": t, "TO-BE (menit)": tm, "Catatan": note} for c, a, am, t, tm, note in P_ITEMS]
            )
        )
