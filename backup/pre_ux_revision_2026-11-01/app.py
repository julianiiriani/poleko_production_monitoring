import streamlit as st

from core import data, state, ui

st.set_page_config(
    page_title="POLEKO Production Monitoring System",
    page_icon=":material/factory:",
    layout="wide",
)

state.init()
ss = st.session_state
logged_in = ss.logged_in
ui.inject_css(logged_in)

# Daftar halaman per perspektif: (nama file di views/, judul, ikon). Menu hanya menampilkan halaman peran aktif;
# halaman lain tetap terdaftar (tersembunyi) agar URL langsung tidak memicu dialog "Page not found".
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
            ("spv_monitoring", "Monitoring Aktivitas Produksi", ":material/monitoring:"),
            ("spv_kelengkapan", "Kelengkapan Pencatatan", ":material/checklist:"),
            ("spv_ringkasan", "Ringkasan Hasil per Tahapan", ":material/table_view:"),
            ("spv_status", "Status Pelaporan", ":material/flag:"),
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


def make_page(spec, default=False, hidden=False):
    key, title, icon = spec
    return st.Page(f"views/{key}.py", title=title, icon=icon, url_path=key, default=default, visibility="hidden" if hidden else "visible")


login_page = st.Page("views/login.py", title="Login", url_path="login", visibility="hidden")
all_specs = [spec for sections in NAV.values() for pages in sections.values() for spec in pages]

if logged_in and ss.role in NAV:
    sections = NAV[ss.role]
    first = next(iter(sections.values()))[0]
    own_keys = {spec[0] for pages in sections.values() for spec in pages}
    structure = {name: [make_page(s, default=(s is first)) for s in pages] for name, pages in sections.items()}
    structure["_"] = [make_page(s, hidden=True) for s in all_specs if s[0] not in own_keys] + [login_page]
    nav = st.navigation(structure)
    home = f"views/{first[0]}.py"
    if nav.url_path not in own_keys | {""}:  # halaman milik perspektif lain atau /login
        st.switch_page(home)
else:
    nav = st.navigation([st.Page("views/login.py", title="Login", url_path="login", default=True)] +
                        [make_page(s, hidden=True) for s in all_specs], position="hidden")
    if nav.url_path not in ("login", ""):  # "" = halaman default (login)
        st.switch_page("views/login.py")

if logged_in and ss.role in NAV:
    st.logo("assets/wordmark.svg", size="large")
    with st.sidebar:
        st.markdown(
            f'<div style="border-left:5px solid {ui.accent()};padding:2px 10px;margin:4px 0 8px 0">'
            f'<div style="font-size:.7rem;letter-spacing:.08em;color:#64748B">PERSPEKTIF DEMO</div>'
            f'<b style="color:{ui.NAVY}">{ui.esc(state.actor_name())}</b><br>'
            f'<span style="font-size:.8rem;color:#475569">{ui.esc(ss.role)}</span></div>',
            unsafe_allow_html=True,
        )
        if ss.role == data.ROLE_PEKERJA:
            nos = state.assigned_stages(ss.worker_id)
            st.caption("Tahapan ditugaskan (DEMO): " + ", ".join(f"{n:02d}" for n in nos))
        st.selectbox("Siklus produksi (DEMO)", data.DEMO_CYCLES, key="cycle")

        with st.expander("Kontrol demo (prototipe)"):
            scenario = st.selectbox("Skenario DEMO", list(state.DEMO_SCENARIOS), key="demo_scenario")
            if st.button("Muat Data DEMO", width="stretch", icon=":material/dataset:"):
                res = state.load_demo(scenario)
                if res["records"] or res["reports"] or res["tasks"]:
                    ss["_flash"] = ("success", f"Data DEMO dimuat: {res['records']} catatan tahapan, {res['tasks']} tugas pemeriksaan kembali, dan {res['reports']} laporan baru ({', '.join(res['cycles'])}).")
                else:
                    ss["_flash"] = ("info", "Skenario ini sudah dimuat; tidak ada data baru ditambahkan.")
                st.rerun()
            if st.button("Reset DEMO", width="stretch", icon=":material/restart_alt:", help="Menghapus seluruh catatan, tugas, laporan, dan riwayat sementara."):
                state.reset_demo()
                ss["_flash"] = ("success", "Reset DEMO selesai: seluruh data sementara dihapus.")
                st.rerun()
            st.caption(data.SESSION_NOTE)
        if st.button("Keluar", width="stretch", icon=":material/logout:", help="Keluar tidak menghapus data DEMO sesi ini."):
            for key in ("logged_in", "role", "username", "worker_id"):
                ss.pop(key, None)
            st.switch_page("views/login.py")
        st.caption(f"⚠ {data.PROTOTYPE_BADGE} · data tidak permanen")

if logged_in and ss.role in NAV:
    flash = ss.pop("_flash", None)
    if flash:
        (st.success if flash[0] == "success" else st.info)(flash[1])

nav.run()
