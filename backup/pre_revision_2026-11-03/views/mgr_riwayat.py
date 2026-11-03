import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Laporan", "Penerimaan, konfirmasi, dan penerusan laporan.")

ui.session_note("Riwayat sementara untuk sesi demo ini, bukan arsip permanen.")
visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
if not visible:
    ui.empty_state("Belum ada riwayat", "Riwayat muncul setelah ada laporan yang diterima Manajemen.")
    st.stop()

st.subheader("Status laporan")
ui.table(
    pd.DataFrame(
        [
            {
                "Siklus": r["cycle"],
                "Status": r["status"],
                "Diterima": r["handoff_at"] or "—",
                "Dikonfirmasi oleh": f"{r['confirmed_by']} · {r['confirmed_at']}" if r["confirmed_by"] else "—",
                f"Diteruskan ke {data.GM} oleh": f"{r['forwarded_by']} · {r['forwarded_at']}" if r["forwarded_by"] else "—",
            }
            for r in visible
        ]
    ),
    badge_cols=("Status",),
)
st.subheader("Kejadian")
ui.events_list([e for e in st.session_state.events if e["kind"] == "Laporan"], "Belum ada kejadian laporan.")
