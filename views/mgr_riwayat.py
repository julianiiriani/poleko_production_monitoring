import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Riwayat Laporan", "Penerimaan, pemeriksaan, konfirmasi, dan penerusan laporan.")

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
                "Laporan": r["report_id"],
                "Status": r["status"],
                "Diterima dari SPV": f"{r['handoff_by']} · {r['handoff_at']}",
                "Diperiksa dan dikonfirmasi oleh": f"{r['confirmed_by']} · {r['confirmed_at']}" if r["confirmed_by"] else "—",
                f"Diteruskan ke {data.GM} oleh": f"{r['forwarded_by']} · {r['forwarded_at']}" if r["forwarded_by"] else "—",
            }
            for r in visible
        ]
    ),
    badge_cols=("Status",),
)
returns = [(r["report_id"], x) for r in visible for x in r["returns"]]
if returns:
    st.subheader("Catatan perbaikan ke SPV")
    ui.table(
        pd.DataFrame(
            [{"Laporan": rid, "Waktu": x["at"], "Dari": x["by"], "Catatan": x["note"], "Tanggapan SPV": x.get("response") or "Belum ditanggapi"} for rid, x in returns]
        )
    )
st.subheader("Kejadian")
ui.events_list([e for e in st.session_state.events if e["kind"] == "Laporan"], "Belum ada kejadian laporan.")
