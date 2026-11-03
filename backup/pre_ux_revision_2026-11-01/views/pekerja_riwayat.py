import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Pencatatan", "Catatan dan kejadian pemeriksaan kembali milik Anda dalam sesi demo ini.")

wid = st.session_state.worker_id
mine = [r for r in st.session_state.records.values() if r["worker_id"] == wid]

if not mine:
    ui.empty_state("Belum ada catatan", "Catatan Anda akan muncul di sini setelah dikirim melalui Input Monitoring Produksi.")
else:
    mine.sort(key=lambda r: (r["cycle"], r["stage_no"]))
    ui.table(
        pd.DataFrame(
            [
                {
                    "Siklus": r["cycle"],
                    "Tahapan": data.stage_label(r["stage_no"]),
                    "Status": r["status"],
                    "Jumlah versi": len(r["versions"]),
                    "Diperbarui": r["updated_at"],
                }
                for r in mine
            ]
        ),
        badge_cols=("Status",),
        max_height=520,
    )
    pick = st.selectbox("Lihat versi catatan", range(len(mine)), format_func=lambda i: f"{mine[i]['cycle']} · {data.stage_label(mine[i]['stage_no'])}")
    ui.version_history(mine[pick])

st.subheader("Kejadian")
ui.events_list([e for e in st.session_state.events if e["worker_id"] == wid])
