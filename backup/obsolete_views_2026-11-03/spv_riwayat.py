import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Hasil Monitoring", "Pencatatan, catatan SPV, kiriman ulang, dan keputusan validasi.")

ui.session_note("Riwayat sementara untuk sesi demo ini, bukan arsip permanen.")
choice = st.selectbox("Siklus", ["Semua siklus"] + data.DEMO_CYCLES)
events = st.session_state.events
if choice != "Semua siklus":
    events = [e for e in events if e["cycle"] == choice]
ui.events_list(events)
