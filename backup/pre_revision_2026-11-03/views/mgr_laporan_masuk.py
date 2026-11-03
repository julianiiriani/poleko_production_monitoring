import streamlit as st

from core import data, state, ui

ui.page_header("Laporan Masuk", "Laporan gabungan yang sudah diterima SPV dan diteruskan ke PPIC.")

cycle = ui.report_picker()
if not cycle:
    ui.empty_state("Belum ada laporan masuk", "Laporan muncul setelah SPV menerima laporan dan meneruskannya ke PPIC.")
    st.stop()

rep = state.get_report(cycle)
ui.report_stepper(rep["status"])
st.caption(f"Diterima dari SPV pada {rep['handoff_at']}.")
ui.report_preview(rep)
if rep["status"] == data.R_MASUK:
    ui.go("views/mgr_konfirmasi.py", "Lanjut ke Pemeriksaan dan Konfirmasi", ":material/task_alt:")
