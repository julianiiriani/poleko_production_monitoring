import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Pengawasan", "Ringkasan kelengkapan dan status laporan gabungan untuk siklus terpilih.")

cycle = state.active_cycle()
counts = state.status_counts(cycle)
gate = state.completeness(cycle)
rep_status = state.report_status(cycle)

ui.stat_grid(
    [
        ("Catatan diterima dari Pekerja", f"{gate['recorded']}", data.ROLE_COLOR[data.ROLE_SPV], "/ 18"),
        (data.S_TERKIRIM, counts[data.S_TERKIRIM], data.STATUS_STYLE[data.S_TERKIRIM][0], "/ 18"),
        ("Tugas pemeriksaan kembali aktif", len(gate["rechecking"]), data.STATUS_STYLE[data.S_KEMBALI][0], "tahapan"),
        ("Dikirim ulang, menunggu tinjauan", len(gate["awaiting_review"]), data.STATUS_STYLE[data.S_KIRIM_ULANG][0], "tahapan"),
        ("Laporan gabungan siklus ini", "Ada" if state.get_report(cycle) else "Belum", data.STATUS_STYLE[rep_status][0], ""),
    ]
)
st.progress(gate["recorded"] / 18, text=f"Kelengkapan pencatatan: {gate['recorded']} dari 18 tahapan")
st.markdown(f"Status laporan: {ui.badge(rep_status)}", unsafe_allow_html=True)

if state.get_report(cycle):
    st.success("Siklus ini sudah divalidasi TRUE dan laporan gabungannya dihasilkan.")
    st.page_link("views/spv_laporan.py", label="Buka Laporan Gabungan", icon=":material/description:")
elif gate["ready"]:
    st.success("18 tahapan lengkap dan tidak ada tugas yang belum selesai. Siklus siap diputuskan di Validasi Laporan.")
    st.page_link("views/spv_validasi.py", label="Validasi Laporan", icon=":material/fact_check:")
else:
    st.warning("TRUE belum dapat diputuskan. Lihat Kelengkapan Pencatatan untuk tahapan yang kurang atau masih dalam pemeriksaan kembali.")
    st.page_link("views/spv_kelengkapan.py", label="Kelengkapan Pencatatan", icon=":material/checklist:")

st.subheader(f"18 tahapan · {cycle}")
ui.stage_grid(cycle)
st.write("")
ui.store_panel(cycle)
ui.demo_note()
ui.about_prototype()
