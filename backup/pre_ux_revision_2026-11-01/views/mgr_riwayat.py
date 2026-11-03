import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Laporan", "Penerimaan, konfirmasi, dan penerusan laporan dalam sesi demo ini.")

visible = state.reports_visible_to_management()
if visible:
    ui.table(
        pd.DataFrame(
            [
                {
                    "Siklus": r["cycle"],
                    "Status": r["status"],
                    "Diterima": r["handoff_at"] or "—",
                    "Dikonfirmasi": r["confirmed_at"] or "—",
                    f"Diteruskan ke {data.GM}": r["forwarded_at"] or "—",
                }
                for r in visible
            ]
        ),
        badge_cols=("Status",),
    )
st.subheader("Kejadian")
ui.events_list([e for e in st.session_state.events if e["kind"] == "Laporan"], "Belum ada laporan yang diterima.")
ui.demo_note()
