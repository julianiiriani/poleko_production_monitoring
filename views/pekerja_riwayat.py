import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Pencatatan")

wid = st.session_state.worker_id
mine = [r for r in st.session_state.records.values() if r["worker_id"] == wid]  # hanya laporan milik pekerja yang login

if not mine:
    ui.empty_state("Belum ada catatan", "Laporan muncul di sini setelah dikirim.")
else:
    ui.table(
        pd.DataFrame(
            [
                {
                    "Dikirim": r["submitted_at"],
                    "Waktu": state.time_text(r["data"]),
                    "Jumlah": state.kg_text(r["data"]),
                    "Kondisi": state.val(r["data"].get("kondisi")),
                    "Status": r["status"],
                    "Versi": len(r["versions"]),
                }
                for r in mine
            ]
        ),
        badge_cols=("Status",),
    )
    for r in mine:
        ui.version_history(r)
