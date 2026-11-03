import streamlit as st

from core import data, state, ui

st.set_page_config(
    page_title="POLEKO Production Monitoring System",
    page_icon=":material/factory:",
    layout="wide",
)

state.init()
ss = st.session_state
logged_in = ss.logged_in and ss.role in data.ROLES
ui.inject_css(logged_in)

# Menu per perspektif: bagian -> [(nama file di views/, judul, ikon)]. Semua halaman terdaftar agar URL langsung
# tidak memicu "Page not found"; halaman milik perspektif lain dialihkan di bawah. Menu samping dibuat dari daftar ini.
NAV = {
    data.ROLE_PEKERJA: {
        "Pekerja": [
            ("pekerja_dashboard", "Dashboard Pekerja", ":material/dashboard:"),
            ("pekerja_input", "Input Monitoring Produksi", ":material/edit_note:"),
            ("pekerja_tugas", "Tugas Pemeriksaan Kembali", ":material/assignment_return:"),
            ("pekerja_riwayat", "Riwayat Pencatatan", ":material/history:"),
        ]
    },
    data.ROLE_SPV: {
        "Pengawasan": [
            ("spv_dashboard", "Dashboard Pengawasan", ":material/dashboard:"),
            ("spv_monitoring", "Monitoring & Kelengkapan Produksi", ":material/monitoring:"),
            ("spv_ringkasan", "Ringkasan Hasil per Tahapan", ":material/table_view:"),
            ("spv_riwayat", "Riwayat Hasil Monitoring", ":material/history:"),
        ],
        "Validasi dan Pelaporan": [
            ("spv_validasi", "Validasi Laporan", ":material/fact_check:"),
            ("spv_penugasan", "Penugasan Pemeriksaan Kembali", ":material/assignment_return:"),
            ("spv_laporan", "Laporan Gabungan", ":material/description:"),
        ],
    },
    data.ROLE_MANAJER: {
        "Manajemen": [
            ("mgr_dashboard", "Dashboard Manajemen", ":material/dashboard:"),
            ("mgr_monitoring", "Monitoring Real-Time", ":material/monitoring:"),
            ("mgr_laporan_masuk", "Laporan Masuk", ":material/inbox:"),
            ("mgr_konfirmasi", "Pemeriksaan dan Konfirmasi", ":material/task_alt:"),
            ("mgr_gm", "Penerusan ke General Manager", ":material/forward_to_inbox:"),
            ("mgr_riwayat", "Riwayat Laporan", ":material/history:"),
        ]
    },
}
ALL_SPECS = [spec for sections in NAV.values() for pages in sections.values() for spec in pages]

if logged_in:
    sections = NAV[ss.role]
    own_keys = {spec[0] for pages in sections.values() for spec in pages}
    home_key = next(iter(sections.values()))[0][0]
else:
    sections, own_keys, home_key = {}, set(), "login"

pages = {
    key: st.Page(f"views/{key}.py", title=title, icon=icon, url_path=key, default=(key == home_key))
    for key, title, icon in ALL_SPECS
}
pages["login"] = st.Page("views/login.py", title="Login", url_path="login", default=not logged_in)
nav = st.navigation(list(pages.values()), position="hidden")

# Alihkan URL langsung ke halaman yang bukan milik perspektif aktif ("" = halaman default).
allowed = (own_keys | {""}) if logged_in else {"login", ""}
if nav.url_path not in allowed:
    st.switch_page(pages[home_key])


def _load_demo():
    scenario = ss.demo_scenario
    res = state.load_demo(scenario)
    if len(res["cycles"]) == 1:
        ss["cycle"] = res["cycles"][0]  # tampilkan siklus skenario yang baru dimuat
    if res["records"] or res["reports"] or res["tasks"]:
        parts = [f"{res['records']} catatan tahapan"]
        if res["tasks"]:
            parts.append(f"{res['tasks']} tugas pemeriksaan kembali")
        if res["reports"]:
            parts.append(f"{res['reports']} laporan")
        ss["_flash"] = ("success", "Data demo dimuat: " + ", ".join(parts) + ".")
    else:
        ss["_flash"] = ("info", "Skenario ini sudah dimuat. Tidak ada data baru ditambahkan.")


@st.dialog("Reset Demo")
def _confirm_reset():
    st.write("Semua data demo pada sesi ini akan dihapus: catatan, tugas, laporan, dan riwayat. Lanjutkan?")
    yes, no = st.columns(2)
    if yes.button("Ya, Reset", type="primary", width="stretch"):
        state.reset_demo()
        ss["_flash"] = ("success", "Reset demo selesai. Data demo sudah dikosongkan.")
        st.rerun()
    if no.button("Batal", width="stretch"):
        st.rerun()


if logged_in:
    with st.sidebar:
        ui.brand()
        ui.who_block()
        for name, specs in sections.items():
            if len(sections) > 1:
                st.markdown(f'<div class="pk-navhead">{name}</div>', unsafe_allow_html=True)
            for key, title, icon in specs:
                st.page_link(pages[key], label=title, icon=icon)
        st.divider()
        st.selectbox("Siklus Produksi", data.DEMO_CYCLES, key="cycle")
        with st.expander("Kontrol Demo"):
            st.selectbox("Skenario Demo", data.DEMO_SCENARIOS, key="demo_scenario")
            st.button("Muat Data Demo", width="stretch", icon=":material/dataset:", on_click=_load_demo)
            if st.button("Reset Demo", width="stretch", icon=":material/restart_alt:"):
                _confirm_reset()
        if st.button("Keluar", width="stretch", icon=":material/logout:"):
            for key in ("logged_in", "role", "username", "worker_id"):
                ss.pop(key, None)
            st.switch_page(pages["login"])
        st.caption(data.DEMO_MODE_LABEL)

    flash = ss.pop("_flash", None)
    if flash:
        {"success": st.success, "error": st.error}.get(flash[0], st.info)(flash[1])

nav.run()
