import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Manajemen", "Laporan gabungan yang masuk dari SPV dan statusnya.")

visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
waiting = [r for r in visible if r["status"] in (data.R_MASUK, data.R_ULANG)]
returned = [r for r in visible if r["status"] == data.R_PERBAIKAN]
confirmed = [r for r in visible if r["status"] == data.R_KONFIRMASI]
done = [r for r in visible if r["status"] == data.R_GM]
color = data.STATUS_STYLE

ui.stat_grid(
    [
        ("Laporan masuk dari SPV", len(visible), data.ROLE_COLOR[data.ROLE_MANAJER], ""),
        ("Menunggu pemeriksaan dan konfirmasi", len(waiting), color[data.R_MASUK][0], ""),
        ("Dikembalikan ke SPV", len(returned), color[data.R_PERBAIKAN][0], ""),
        ("Dikonfirmasi, belum diteruskan", len(confirmed), color[data.R_KONFIRMASI][0], ""),
        ("Diterima General Manager (DEMO)", len(done), color[data.R_GM][0], ""),
    ],
    min_width=160,
)


def _mgr_status(r):
    if r["status"] in (data.R_KONFIRMASI, data.R_GM):
        return f"Diperiksa dan dikonfirmasi oleh {r['confirmed_by']}"
    if r["status"] == data.R_PERBAIKAN:
        return f"Dikembalikan ke SPV oleh {r['returns'][-1]['by']}"
    return "Belum diperiksa" if r["status"] == data.R_MASUK else "Menunggu pemeriksaan ulang"


if not visible:
    ui.empty_state("Belum ada laporan masuk", "Laporan muncul setelah SPV meneruskan laporan gabungan ke Manajemen.")
else:
    st.subheader("Langkah berikutnya")
    if waiting:
        st.info(f"{len(waiting)} laporan menunggu pemeriksaan dan konfirmasi.")
        ui.go("views/mgr_konfirmasi.py", "Periksa dan Konfirmasi", ":material/task_alt:")
    if confirmed:
        st.info(f"{len(confirmed)} laporan sudah dikonfirmasi dan siap diteruskan ke {data.GM}.")
        ui.go("views/mgr_gm.py", f"Teruskan ke {data.GM}", ":material/forward_to_inbox:")
    if returned:
        st.info(f"{len(returned)} laporan sedang diperbaiki SPV setelah Anda kembalikan.")
    if not (waiting or confirmed or returned):
        st.success(f"Semua laporan yang masuk sudah diteruskan ke {data.GM}.")

    st.subheader("Daftar laporan")
    ui.table(
        pd.DataFrame(
            [
                {
                    "Laporan": r["report_id"],
                    "Status": r["status"],
                    "Waktu penerimaan": r["handoff_at"] or "—",
                    "Identitas SPV pengirim": r["handoff_by"] or "—",
                    "Status pemeriksaan Manajemen": _mgr_status(r),
                }
                for r in visible
            ]
        ),
        badge_cols=("Status",),
    )
