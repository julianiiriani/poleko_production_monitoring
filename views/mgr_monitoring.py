import streamlit as st

from core import data, state, ui

ui.page_header("Monitoring Real-Time", "Status pencatatan 18 tahapan produksi.")

cycle = state.active_cycle()
ui.session_note("Menampilkan data pada sesi demo ini. Pembaruan tidak tersinkron antar pengguna atau perangkat.")
ui.status_stat_grid(state.status_counts(cycle))
ui.overview_table(state.overview_df(cycle, actions=False))
