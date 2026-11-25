import streamlit as st

from core import data, state, ui

ui.page_header("Monitoring & Kelengkapan Produksi", "Status 18 tahapan, pekerja penanggung jawab, dan tindakan yang sesuai.")

cycle = state.active_cycle()
g = state.completeness(cycle)
st.progress(g["recorded"] / 18, text=f"Jumlah Tahapan: {g['recorded']}/18 sudah memiliki laporan")

counts = state.status_counts(cycle)
selected = st.multiselect(
    "Tampilkan status", data.RECORD_STATUS_ORDER, placeholder="Semua status", format_func=lambda s: f"{s} ({counts[s]})"
)
df = state.overview_df(cycle)
view = df[df["No"].map(lambda n: state.stage_status(cycle, n)).isin(selected)] if selected else df
if view.empty:
    ui.empty_state("Tidak ada tahapan", "Tidak ada tahapan dengan status yang dipilih.")
else:
    ui.overview_table(view)

st.subheader("Tindak lanjuti tahapan")
stage_labels = {n: f"{data.stage_label(n)} — {state.stage_status(cycle, n)}" for n in data.STAGE_NOS}
no = st.selectbox("Pilih tahapan", data.STAGE_NOS, format_func=stage_labels.get, key="mon_stage")
label = state.action_label(state.get_record(cycle, no))
if st.button(label, type="primary", icon=":material/arrow_forward:", key="mon_action"):
    st.session_state["_val_pick"] = no
    st.switch_page("views/spv_validasi.py")
st.caption("Tombol membuka tahapan terpilih pada Validasi Laporan. Tahapan yang belum dicatat hanya menampilkan pekerja yang perlu dihubungi.")
