import streamlit as st

from core import data, state, ui

ui.page_header("Laporan Masuk", "Laporan gabungan yang sudah diteruskan SPV ke Manajemen.")

cycle = ui.report_picker()
if not cycle:
    ui.empty_state("Belum ada laporan masuk", "Laporan muncul setelah SPV meneruskan laporan gabungan ke Manajemen.")
    st.stop()

rep = state.get_report(cycle)
ui.report_stepper(rep["status"])
ui.kv(
    [
        ("Identitas SPV pengirim", rep["handoff_by"]),
        ("Waktu penerusan dari SPV", rep["handoff_at"]),
        ("Status", ("badge", rep["status"])),
    ]
)
if rep["status"] in (data.R_MASUK, data.R_ULANG):
    ui.go("views/mgr_konfirmasi.py", "Lanjut ke Pemeriksaan dan Konfirmasi", ":material/task_alt:")
elif rep["status"] == data.R_PERBAIKAN:
    ret = rep["returns"][-1]
    st.info(f"Laporan dikembalikan ke SPV oleh {ret['by']} pada {ret['at']}. Menunggu SPV mengirim kembali.")
ui.report_preview(rep)
