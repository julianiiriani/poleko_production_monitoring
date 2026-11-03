import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Hasil Monitoring", "Pencatatan Pekerja, catatan SPV, pemeriksaan kembali, kiriman ulang, dan validasi dalam sesi demo ini.")

choice = st.selectbox("Siklus", ["Semua siklus"] + data.DEMO_CYCLES)
events = st.session_state.events
if choice != "Semua siklus":
    events = [e for e in events if e["cycle"] == choice]
ui.events_list(events)
ui.demo_note()
