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
            ("spv_validasi", "Validasi Laporan", ":material/fact_check:"),
            ("spv_laporan", "Laporan Gabungan", ":material/description:"),
        ]
    },
    data.ROLE_MANAJER: {
        "Manajemen": [
            ("mgr_dashboard", "Dashboard Manajemen", ":material/dashboard:"),
            ("mgr_monitoring", "Monitoring Real-Time", ":material/monitoring:"),
            ("mgr_tindak_lanjut", "Tindak Lanjut Data", ":material/assignment_late:"),
            ("mgr_laporan_masuk", "Laporan Masuk", ":material/inbox:"),
            ("mgr_konfirmasi", "Pemeriksaan dan Konfirmasi", ":material/task_alt:"),
            ("mgr_gm", "Penerusan ke General Manager", ":material/forward_to_inbox:"),
            ("mgr_riwayat", "Riwayat Laporan", ":material/history:"),
        ]
    },
}
# Menu manajemen berbeda per tingkatan (Aturan Main bagian 1 dan 6). Judul menu menyesuaikan identitas.
MGR_MENU = {
    data.PM: [("mgr_dashboard", "Dashboard Production Manager"), ("mgr_monitoring", "Monitoring Semua Shift"),
              ("mgr_tindak_lanjut", "Kendala Mesin"), ("mgr_laporan_masuk", "Laporan Masuk"),
              ("mgr_konfirmasi", "Pemeriksaan dan Konfirmasi"), ("mgr_gm", "Penerusan ke General Manager"), ("mgr_riwayat", "Riwayat Laporan")],
    data.PPIC: [("mgr_dashboard", "Dashboard PPIC"), ("mgr_monitoring", "Monitoring Semua Shift"),
                ("mgr_tindak_lanjut", "Data di Luar Batas"), ("mgr_laporan_masuk", "Laporan Masuk"), ("mgr_riwayat", "Riwayat Laporan")],
    data.QA: [("mgr_dashboard", "Dashboard QA"), ("mgr_tindak_lanjut", "Keputusan Mutu"), ("mgr_laporan_masuk", "Laporan Masuk"),
              ("mgr_riwayat", "Riwayat Laporan")],
    data.QC: [("mgr_dashboard", "Dashboard QC"), ("mgr_tindak_lanjut", "Pemeriksaan Mutu"), ("mgr_riwayat", "Riwayat Laporan")],
}
ALL_SPECS = [spec for sections in NAV.values() for pages in sections.values() for spec in pages]

if logged_in:
    sections = NAV[ss.role]
    if ss.role == data.ROLE_MANAJER and ss.get("identity") in MGR_MENU:
        icons = {k: i for k, _, i in NAV[data.ROLE_MANAJER]["Manajemen"]}
        sections = {"Manajemen": [(k, t, icons[k]) for k, t in MGR_MENU[ss.identity]]}
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
        if st.button("Keluar", width="stretch", icon=":material/logout:"):
            for key in ("logged_in", "role", "username", "worker_id", "identity", "shift"):
                ss.pop(key, None)
            st.switch_page(pages["login"])
        st.caption(data.DEMO_MODE_LABEL)

    flash = ss.pop("_flash", None)
    if flash:
        {"success": st.success, "error": st.error}.get(flash[0], st.info)(flash[1])

nav.run()
