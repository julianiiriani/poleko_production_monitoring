import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Pengawasan", "Ringkasan siklus produksi yang sedang dipantau.", cycle=True)

cycle = state.active_cycle()
counts = state.status_counts(cycle)
gate = state.completeness(cycle)
rep_status = state.report_status(cycle)

ui.stat_grid(
    [
        ("Tahapan sudah dicatat", gate["recorded"], data.ROLE_COLOR[data.ROLE_SPV], "/ 18"),
        (data.S_TERKIRIM, counts[data.S_TERKIRIM], data.STATUS_STYLE[data.S_TERKIRIM][0], "/ 18"),
        (data.S_KEMBALI, len(gate["rechecking"]), data.STATUS_STYLE[data.S_KEMBALI][0], "tahapan"),
        ("Sudah diperbaiki, perlu ditinjau",len(gate["awaiting_review"]), data.STATUS_STYLE[data.S_KIRIM_ULANG][0], "tahapan"),
    ]
)
st.progress(gate["recorded"] / 18, text=f"{gate['recorded']} dari 18 tahapan sudah dicatat")
st.markdown(f"Status laporan gabungan: {ui.badge(rep_status)}", unsafe_allow_html=True)

st.subheader("Langkah berikutnya")
if state.get_report(cycle):
    st.success("Laporan Diterima. Laporan gabungan siklus ini sudah dihasilkan.")
    ui.go("views/spv_laporan.py", "Buka Laporan Gabungan", ":material/description:")
elif gate["awaiting_review"]:
    st.info(f"{len(gate['awaiting_review'])} kiriman ulang dari Pekerja menunggu tinjauan Anda.")
    ui.go("views/spv_penugasan.py", "Tinjau Kiriman Ulang", ":material/assignment_return:")
elif gate["ready"]:
    st.success("Semua 18 tahapan lengkap. Siklus ini siap divalidasi.")
    ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:")
else:
    st.info("Laporan belum bisa diterima karena masih ada tahapan yang belum dicatat atau belum selesai diperbaiki.")
    ui.go("views/spv_monitoring.py", "Lihat Monitoring & Kelengkapan", ":material/monitoring:")
