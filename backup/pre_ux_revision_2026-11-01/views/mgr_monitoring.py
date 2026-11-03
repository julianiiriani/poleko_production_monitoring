import streamlit as st

from core import data, state, ui

ui.page_header("Monitoring Real-Time", "Informasi 18 tahapan dari Data Aktivitas Proses Produksi (representasi konsep).")

cycle = state.active_cycle()
ui.store_panel(cycle)
st.caption(data.REALTIME_NOTE)

counts = state.status_counts(cycle)
ui.status_stat_grid(counts)
ui.overview_table(state.overview_df(cycle))
st.caption("Manajemen hanya memantau; tidak ada input ulang data produksi pada perspektif ini.")
ui.demo_note()
