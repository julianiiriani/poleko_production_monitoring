import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Pencatatan", "Laporan yang pernah Anda kirim untuk tahapan Anda.")

ui.session_note("Riwayat sementara untuk sesi demo ini, bukan arsip permanen.")
wid = st.session_state.worker_id
mine = [r for r in st.session_state.records.values() if r["worker_id"] == wid]  # hanya laporan milik pekerja yang login

if not mine:
    ui.empty_state("Belum ada catatan", "Laporan Anda muncul di sini setelah dikirim lewat Input Monitoring Produksi.")
else:
    ui.table(
        pd.DataFrame(
            [
                {
                    "Tanggal dan Waktu": r["submitted_at"],
                    "Nama Tahapan": data.STAGE_NAMES[r["stage_no"]],
                    "Jumlah Produksi": state.kg_text(r["data"]),
                    "Waktu Mulai – Selesai": state.time_text(r["data"]),
                    "Pelaksana/Pemantau": state.val(r["data"].get("pelaksana")),
                    "Kondisi Proses": state.val(r["data"].get("kondisi")),
                    "Status SPV": r["status"],
                    "Versi": len(r["versions"]),
                }
                for r in mine
            ]
        ),
        badge_cols=("Status SPV",),
    )
    st.subheader("Riwayat perubahan")
    for r in mine:
        ui.version_history(r)

st.subheader("Kejadian")
ui.events_list([e for e in st.session_state.events if e["worker_id"] == wid])
