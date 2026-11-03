import streamlit as st

from core import data, state, ui

ui.page_header("Laporan Gabungan", "Satu laporan per siklus, berisi 18 tahapan, dihasilkan otomatis setelah keputusan TRUE.")

with_report = [c for c in data.DEMO_CYCLES if state.get_report(c)]
if not with_report:
    ui.empty_state("Belum ada laporan gabungan", "Laporan dihasilkan otomatis setelah SPV memutuskan TRUE pada Validasi Laporan.")
    st.page_link("views/spv_validasi.py", label="Validasi Laporan", icon=":material/fact_check:")
    ui.demo_note()
    st.stop()

default = with_report.index(state.active_cycle()) if state.active_cycle() in with_report else 0
cycle = st.selectbox("Laporan siklus", with_report, index=default)
rep = state.get_report(cycle)

st.markdown(f"Status: {ui.badge(rep['status'])}", unsafe_allow_html=True)
ui.report_stepper(rep["status"])
if rep["status"] == data.R_GENERATED:
    if st.button("Teruskan ke PPIC", type="primary", icon=":material/forward:"):
        ok, msg = state.handoff_to_ppic(cycle)
        st.session_state["_flash"] = ("success" if ok else "info", msg)
        st.rerun()
    st.caption("Laporan baru terlihat oleh Manajer/PPIC/QC/QA setelah diteruskan.")

ui.report_preview(rep)
ui.demo_note()
