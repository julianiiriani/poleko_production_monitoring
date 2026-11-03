import pandas as pd
import streamlit as st

from core import arena, data, state, ui

ui.page_header("Dashboard Manajemen", "Laporan gabungan yang masuk dan statusnya.")

visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
n_masuk = sum(r["status"] == data.R_MASUK for r in visible)
n_konfirmasi = sum(r["status"] == data.R_KONFIRMASI for r in visible)
n_gm = sum(r["status"] == data.R_GM for r in visible)
color = data.STATUS_STYLE

ui.stat_grid(
    [
        ("Laporan masuk", len(visible), color[data.R_MASUK][0], ""),
        ("Menunggu pemeriksaan dan konfirmasi", n_masuk, color[data.R_GENERATED][0], ""),
        ("Terkonfirmasi, belum diteruskan", n_konfirmasi, color[data.R_KONFIRMASI][0], ""),
        ("Diteruskan ke General Manager", n_gm, color[data.R_GM][0], ""),
    ]
)

if not visible:
    ui.empty_state("Belum ada laporan masuk", "Laporan muncul setelah SPV menerima laporan dan meneruskannya ke PPIC.")
else:
    st.subheader("Langkah berikutnya")
    if n_masuk:
        st.info(f"{n_masuk} laporan menunggu Anda periksa dan konfirmasi.")
        ui.go("views/mgr_konfirmasi.py", "Periksa dan Konfirmasi", ":material/task_alt:")
    if n_konfirmasi:
        st.info(f"{n_konfirmasi} laporan sudah dikonfirmasi dan siap diteruskan ke {data.GM}.")
        ui.go("views/mgr_gm.py", f"Teruskan ke {data.GM}", ":material/forward_to_inbox:")
    if not (n_masuk or n_konfirmasi):
        st.success(f"Semua laporan yang masuk sudah diteruskan ke {data.GM}.")

    st.subheader("Daftar laporan")
    ui.table(
        pd.DataFrame([{"Siklus": r["cycle"], "Status": r["status"], "Diterima dari SPV": r["handoff_at"] or "—"} for r in visible]),
        badge_cols=("Status",),
    )

# Hasil penelitian statis: tidak membaca data demo/session_state dan tidak terpengaruh state laporan di atas.
st.divider()
arena.render()
