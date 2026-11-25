import streamlit as st

from core import data, state, ui

cycle = state.active_cycle()
shift = st.session_state.shift
ui.page_header("Dashboard Pengawasan", data.shift_name(shift))
mine = [r for r in state.cycle_records(cycle) if r["shift"] == shift]
lv = state.level_counts(cycle, shift)
ui.stat_grid(
    [
        ("Data shift Anda", len(mine), data.ROLE_COLOR[data.ROLE_SPV], "tahap"),
        ("Menunggu pemeriksaan Anda", sum(r["status"] in (data.S_MENUNGGU, data.S_ULANG) for r in mine), data.STATUS_STYLE[data.S_MENUNGGU][0], ""),
        (data.LV_HIJAU, lv[data.LV_HIJAU], data.STATUS_STYLE[data.LV_HIJAU][0], ""),
        (data.LV_KUNING, lv[data.LV_KUNING], data.STATUS_STYLE[data.LV_KUNING][0], ""),
        (data.LV_MERAH, lv[data.LV_MERAH], data.STATUS_STYLE[data.LV_MERAH][0], ""),
    ],
    min_width=190,
)
st.subheader("Kelengkapan 18 tahapan (semua shift)")
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
        ("Menunggu pemeriksaan Supervisor", counts[data.S_MENUNGGU], color[data.S_MENUNGGU][0], "/ 18"),
        ("Sudah dikonfirmasi Supervisor", counts[data.S_KONFIRMASI], color[data.S_KONFIRMASI][0], "/ 18"),
        ("Perlu perbaikan", counts[data.S_KEMBALI], color[data.S_KEMBALI][0], "/ 18"),
        ("Sudah diperbaiki", corrected, color[data.IN_DIPERBAIKI][0], "/ 18"),
        ("Menunggu pemeriksaan ulang Supervisor", counts[data.S_ULANG], color[data.S_ULANG][0], "/ 18"),
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
