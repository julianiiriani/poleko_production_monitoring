import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Manajemen", "Laporan gabungan yang masuk, status konfirmasi, dan gambaran 18 tahapan.")

visible = state.reports_visible_to_management()
n_masuk = sum(r["status"] == data.R_MASUK for r in visible)
n_conf = sum(r["status"] in (data.R_KONFIRMASI, data.R_GM) for r in visible)
n_gm = sum(r["status"] == data.R_GM for r in visible)
color = data.STATUS_STYLE

ui.stat_grid(
    [
        ("Laporan masuk", len(visible), color[data.R_MASUK][0], "laporan"),
        ("Menunggu pemeriksaan dan konfirmasi", n_masuk, color[data.R_GENERATED][0], "laporan"),
        ("Terkonfirmasi", n_conf, color[data.R_KONFIRMASI][0], "laporan"),
        ("Diteruskan ke General Manager (DEMO)", n_gm, color[data.R_GM][0], "laporan"),
    ]
)
if not visible:
    st.caption("Belum ada laporan masuk. Laporan muncul setelah SPV memvalidasi TRUE dan meneruskannya ke PPIC.")
else:
    st.page_link("views/mgr_laporan_masuk.py", label="Buka Laporan Masuk", icon=":material/inbox:")

cycle = state.active_cycle()
st.subheader(f"Gambaran 18 tahapan · {cycle}")
ui.stage_grid(cycle)
st.caption(data.REALTIME_NOTE)

st.write("")
st.markdown(
    '<div class="pk-kpi"><div class="pk-kpi-title">KPI Utama Penelitian</div>'
    '<div class="pk-kpi-value">Time Efficiency — Belum Dihitung</div>'
    '<div class="pk-kpi-note">Tidak ada angka karena parameter simulasi ARENA belum dikonfigurasi dan keluaran simulasi yang valid belum tersedia.</div></div>',
    unsafe_allow_html=True,
)
with st.expander("Rumus awal dan status ARENA"):
    st.markdown('<div class="pk-formula">Time Efficiency = (Processing Time / Total Time) × 100%</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        ui.info_card("Processing Time", "Menunggu Data Valid", "Placeholder", pending=True)
    with c2:
        ui.info_card("Total Time", "Menunggu Data Valid", "Placeholder", pending=True)
    with c3:
        ui.info_card("Time Efficiency", "Belum Dihitung", "Placeholder", pending=True)
    st.markdown(
        "- ARENA As-Is: parameter **Belum Dikonfigurasi** · keluaran simulasi **Belum Tersedia**\n"
        "- ARENA To-Be: parameter **Belum Dikonfigurasi** · keluaran simulasi **Belum Tersedia**\n"
        "- Waktu pada formulir input DEMO tidak dipakai untuk menghitung KPI penelitian."
    )
ui.demo_note()
ui.about_prototype()
