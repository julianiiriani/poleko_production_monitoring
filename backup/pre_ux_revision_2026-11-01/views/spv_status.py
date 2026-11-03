import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Status Pelaporan", "Status catatan tahapan dan status laporan gabungan ditampilkan terpisah.")

cycle = state.active_cycle()
st.markdown("##### Alur laporan siklus terpilih")
ui.report_stepper(state.report_status(cycle))
st.markdown(f"Status laporan {cycle}: {ui.badge(state.report_status(cycle))}", unsafe_allow_html=True)

st.markdown("##### Semua siklus DEMO")
rows = []
for c in data.DEMO_CYCLES:
    cnt = state.status_counts(c)
    rows.append(
        {
            "Siklus": c,
            "Tercatat": 18 - cnt[data.S_BELUM],
            data.S_TERKIRIM: cnt[data.S_TERKIRIM],
            data.S_KEMBALI: cnt[data.S_KEMBALI],
            data.S_KIRIM_ULANG: cnt[data.S_KIRIM_ULANG],
            data.S_LAPORAN: cnt[data.S_LAPORAN],
            "Status laporan gabungan": state.report_status(c),
        }
    )
ui.table(pd.DataFrame(rows), badge_cols=("Status laporan gabungan",))
st.caption("Angka kolom status adalah jumlah tahapan (dari 18) pada status catatan tersebut; status laporan adalah status satu laporan per siklus.")
ui.demo_note()
