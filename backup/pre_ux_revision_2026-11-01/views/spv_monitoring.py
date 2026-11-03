import streamlit as st

from core import data, state, ui

ui.page_header("Monitoring Aktivitas Produksi", "Catatan yang dikirim Pekerja untuk 18 tahapan, dalam urutan tetap.")

cycle = state.active_cycle()
ui.store_panel(cycle)
st.write("")

df = state.overview_df(cycle)
recorded = int((df["Status"] != data.S_BELUM).sum())
m1, m2 = st.columns(2)
m1.metric("Tahapan tercatat", f"{recorded} / 18")
m2.metric("Belum dicatat", f"{18 - recorded} / 18")

selected = st.multiselect("Filter status", data.RECORD_STATUS_ORDER, placeholder="Semua status")
view = df[df["Status"].isin(selected)] if selected else df
if view.empty:
    ui.empty_state("Tidak ada tahapan", "Tidak ada tahapan dengan status yang dipilih pada siklus ini.")
else:
    ui.overview_table(view)
st.caption("Pekerja yang tertera di baris 'Belum Dicatat' adalah penugasan DEMO. " + data.REALTIME_NOTE)
ui.demo_note()
