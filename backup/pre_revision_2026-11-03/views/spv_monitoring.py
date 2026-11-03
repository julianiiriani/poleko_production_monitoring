import streamlit as st

from core import data, state, ui

ui.page_header("Monitoring & Kelengkapan Produksi", "Status pencatatan 18 tahapan dan apa yang masih kurang.", cycle=True)

cycle = state.active_cycle()
gate = state.completeness(cycle)
st.progress(gate["recorded"] / 18, text=f"{gate['recorded']} dari 18 tahapan sudah dicatat")

if state.get_report(cycle):
    st.success("Laporan gabungan siklus ini sudah dihasilkan.")
elif gate["ready"]:
    st.success("Semua 18 tahapan lengkap dan tidak ada pemeriksaan ulang yang tertunda. Siap divalidasi.")
    ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:")
else:
    todo = []
    if gate["missing"]:
        todo.append("Belum dicatat: " + ", ".join(f"{n:02d}" for n in gate["missing"]))
    if gate["rechecking"]:
        todo.append("Menunggu perbaikan Pekerja: " + ", ".join(f"{n:02d}" for n in gate["rechecking"]))
    if gate["awaiting_review"]:
        todo.append("Kiriman ulang menunggu tinjauan Anda: " + ", ".join(f"{n:02d}" for n in gate["awaiting_review"]))
    st.warning("Belum bisa diterima. " + " · ".join(todo))
    if gate["awaiting_review"]:
        ui.go("views/spv_penugasan.py", "Tinjau Kiriman Ulang", ":material/assignment_return:")

counts = state.status_counts(cycle)
selected = st.multiselect(
    "Tampilkan status", data.RECORD_STATUS_ORDER, placeholder="Semua status", format_func=lambda s: f"{s} ({counts[s]})"
)
if state.has_fixture(cycle):
    st.caption("Catatan bertanda “data contoh” berasal dari Muat Data Demo; isian formulirnya sengaja dikosongkan.")
df = state.overview_df(cycle)
view = df[df["Status"].isin(selected)] if selected else df
if view.empty:
    ui.empty_state("Tidak ada tahapan", "Tidak ada tahapan dengan status yang dipilih.")
else:
    ui.overview_table(view)
