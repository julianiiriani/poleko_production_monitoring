import pandas as pd
import streamlit as st

from core import data, ui

ui.page_header(
    "Evaluasi Time Efficiency",
    "Tempat hasil evaluasi KPI utama. Belum ada angka karena data valid belum tersedia.",
    data.PAGE_ACTORS["efisiensi"],
)

st.markdown(
    '<div class="pk-kpi"><div class="pk-kpi-title">KPI Utama</div>'
    '<div class="pk-kpi-value">Time Efficiency — Belum Dihitung</div>'
    '<div class="pk-kpi-note">Parameter simulasi ARENA belum dikonfigurasi dan output simulasi yang valid belum tersedia. '
    "Halaman ini tidak menyatakan adanya peningkatan efisiensi pada proses To-Be.</div></div>",
    unsafe_allow_html=True,
)

st.write("")
st.markdown("##### Rumus awal (preliminary)")
st.markdown(
    '<div class="pk-formula">Time Efficiency = (Processing Time / Total Time) × 100%</div>',
    unsafe_allow_html=True,
)
st.caption("Definisi pengukuran dan sumber data valid belum final; rumus tidak dipakai untuk menghasilkan angka.")

c1, c2, c3 = st.columns(3)
with c1:
    ui.info_card("Processing Time", "Menunggu Data Valid", "Placeholder", pending=True)
with c2:
    ui.info_card("Total Time", "Menunggu Data Valid", "Placeholder", pending=True)
with c3:
    ui.info_card("Time Efficiency", "Belum Dihitung", "Placeholder", pending=True)

st.write("")
st.subheader("Status Model ARENA")
st.dataframe(
    pd.DataFrame(
        [
            ["As-Is", "Struktur disiapkan", "Belum Dikonfigurasi", "Belum Tersedia", "Belum Dihitung"],
            ["To-Be", "Struktur disiapkan", "Belum Dikonfigurasi", "Belum Tersedia", "Belum Dihitung"],
        ],
        columns=["Model", "Struktur modul", "Parameter simulasi", "Output simulasi", "Time Efficiency"],
    ),
    hide_index=True,
    width="stretch",
)

st.subheader("Perbedaan Struktur pada Diagram BPMN")
st.caption(
    "Hanya memuat hal yang tertera pada diagram BPMN As-Is dan To-Be yang disediakan (label diagram dikutip). "
    "Ini bukan evaluasi dan bukan bukti peningkatan efisiensi."
)
st.table(
    pd.DataFrame(
        [
            ["Jumlah swimlane", "4", "3"],
            ["Tahapan produksi", "18 tahapan", "18 tahapan (sama)"],
            ["Swimlane Staff/Admin Produksi", "Ada — aktivitas \"Rekapitulasi Data\"", "Tidak ada"],
            ["Aktivitas SPV Produksi per tahapan", "\"Mencatat Hasil Proses ...\"", "\"Input Laporan ...\""],
            ["Penyimpanan data", "Tidak ada data store pada diagram", "\"Data Aktivitas Proses Produksi\""],
            ["Aktivitas laporan di swimlane SPV Produksi", "\"Menyusun Laporan Produksi / Lockbox Per-Shift\"", "\"Validasi Laporan\""],
            ["Data tidak sesuai", "\"Koreksi / Rekonsiliasi Data\"", "\"Memeriksa Kembali ke Pihak Yang Menginput Aktivitas Produksi\""],
            ["Penerusan laporan", "\"Meneruskan Laporan ke General Manager\"", "\"Meneruskan ke PPIC\""],
            [
                "Swimlane Manajer Produksi / PPIC / QC / QA",
                "\"Memeriksa dan Memvalidasi Laporan\"; \"Koreksi / Rekonsiliasi Data\"; \"Meneruskan Laporan ke General Manager\"",
                "\"Memantau Pencatatan dan Aktivitas Produksi Secara Real-Time\"; \"Memeriksa Kembali dan Melakukan Konfirmasi Laporan\"",
            ],
        ],
        columns=["Aspek", "As-Is", "To-Be"],
    ).set_index("Aspek"),
)
