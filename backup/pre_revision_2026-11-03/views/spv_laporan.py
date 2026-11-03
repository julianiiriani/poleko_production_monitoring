import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Laporan Gabungan", "Satu laporan per siklus, berisi 18 tahapan.")

st.subheader("Status per siklus")
ui.table(
    pd.DataFrame(
        [
            {"Siklus": c, "Tahapan tercatat": f"{18 - state.status_counts(c)[data.S_BELUM]} / 18", "Status laporan": state.report_status(c)}
            for c in data.DEMO_CYCLES
        ]
    ),
    badge_cols=("Status laporan",),
)

with_report = [c for c in data.DEMO_CYCLES if state.get_report(c)]
if not with_report:
    ui.empty_state("Belum ada laporan gabungan", "Laporan dibuat otomatis setelah SPV memilih Laporan Diterima di Validasi Laporan.")
    ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:")
    st.stop()

st.subheader("Laporan")
default = with_report.index(state.active_cycle()) if state.active_cycle() in with_report else 0
cycle = st.selectbox("Pilih laporan", with_report, index=default)
rep = state.get_report(cycle)

ui.report_stepper(rep["status"])
if rep["status"] == data.R_GENERATED:
    if st.button("Teruskan ke PPIC", type="primary", icon=":material/forward:"):
        ok, msg = state.handoff_to_ppic(cycle)
        st.session_state["_flash"] = ("success" if ok else "info", msg)
        st.rerun()
    st.caption("Manajemen baru dapat melihat laporan ini setelah diteruskan.")
ui.report_preview(rep)
