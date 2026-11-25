import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Pengawasan", "Kondisi 18 tahapan produksi dan langkah berikutnya.")

cycle = state.active_cycle()
counts = state.status_counts(cycle)
g = state.completeness(cycle)
rep = state.get_report(cycle)
corrected = sum(state.was_corrected(r) for r in state.cycle_records(cycle))
valid_recorded = g["recorded"] - len(g["incomplete"])  # hanya laporan yang benar-benar masuk dan datanya lengkap
color = data.STATUS_STYLE

st.progress(valid_recorded / 18, text=f"Jumlah Tahapan: {valid_recorded}/18")
ui.stat_grid(
    [
        ("Tahapan sudah dicatat", valid_recorded, data.ROLE_COLOR[data.ROLE_SPV], "/ 18"),
        ("Tahapan belum dicatat", counts[data.S_BELUM], color[data.S_BELUM][0], "/ 18"),
        ("Menunggu pemeriksaan SPV", counts[data.S_MENUNGGU], color[data.S_MENUNGGU][0], "/ 18"),
        ("Sudah dikonfirmasi SPV", counts[data.S_KONFIRMASI], color[data.S_KONFIRMASI][0], "/ 18"),
        ("Perlu perbaikan", counts[data.S_KEMBALI], color[data.S_KEMBALI][0], "/ 18"),
        ("Sudah diperbaiki", corrected, color[data.IN_DIPERBAIKI][0], "/ 18", "Pekerja pernah mengirim perbaikan"),
        ("Menunggu pemeriksaan ulang SPV", counts[data.S_ULANG], color[data.S_ULANG][0], "/ 18"),
    ],
    min_width=225,
)
st.markdown(f"**Status Laporan:** {ui.badge(state.spv_cycle_status(cycle))}", unsafe_allow_html=True)

st.subheader("Langkah Berikutnya")
if rep:
    if rep["status"] == data.R_PERBAIKAN:
        ret = rep["returns"][-1]
        st.warning(f"Laporan gabungan dikembalikan oleh {ret['by']} ({ret['at']}). Catatan: {ret['note']}")
    elif rep["status"] == data.R_GENERATED:
        st.success("Laporan gabungan sudah dihasilkan dan menunggu Anda teruskan ke Manajemen.")
    else:
        st.success(f"Laporan gabungan sudah dihasilkan dan diteruskan ke Manajemen. Status: {rep['status']}.")
    ui.go("views/spv_laporan.py", "Buka Laporan Gabungan", ":material/description:")
else:
    if g["missing"]:
        st.info(f"Masih terdapat {len(g['missing'])} tahapan yang belum memiliki laporan. Menunggu penginputan pekerja terkait.")
    if g["waiting"]:
        st.info(f"{len(g['waiting'])} laporan tahapan menunggu pemeriksaan Anda.")
    if g["recheck"]:
        st.info(f"{len(g['recheck'])} hasil perbaikan menunggu pemeriksaan ulang Anda.")
    if g["fix"]:
        st.info(f"{len(g['fix'])} tahapan menunggu perbaikan dari Pekerja.")
    if g["ready"]:
        st.success("Seluruh 18 tahapan telah diperiksa dan dikonfirmasi. Laporan gabungan siap dibuat.")
        ui.go("views/spv_validasi.py", "Buka Validasi Laporan untuk Generate Report", ":material/fact_check:")
    elif g["waiting"] or g["recheck"]:
        ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:")
    else:
        ui.go("views/spv_monitoring.py", "Lihat Monitoring & Kelengkapan", ":material/monitoring:")

st.subheader("Kondisi 18 tahapan")
ui.stage_grid(cycle)
