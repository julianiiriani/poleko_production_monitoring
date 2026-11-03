import streamlit as st

from core import data, state, ui

ui.page_header("Laporan Masuk", "Laporan gabungan yang sudah divalidasi SPV dan diteruskan ke PPIC.")

visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
if not visible:
    ui.empty_state("Belum ada laporan masuk", "Laporan muncul setelah SPV memutuskan TRUE dan meneruskannya ke PPIC.")
    ui.demo_note()
    st.stop()

cycles = [r["cycle"] for r in visible]
cycle = st.selectbox("Pilih laporan", cycles, format_func=lambda c: f"{c} · {state.report_status(c)}")
rep = state.get_report(cycle)
st.markdown(f"Status: {ui.badge(rep['status'])}", unsafe_allow_html=True)
ui.report_stepper(rep["status"])
st.caption(f"Diterima dari SPV pada {rep['handoff_at']} (waktu demo).")
ui.report_preview(rep)
ui.demo_note()
