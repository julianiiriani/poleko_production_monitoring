import streamlit as st

from core import data, state, ui

_, center, _ = st.columns([1, 1.4, 1])

HOME = {
    data.ROLE_PEKERJA: "views/pekerja_dashboard.py",
    data.ROLE_SPV: "views/spv_dashboard.py",
    data.ROLE_MANAJER: "views/mgr_dashboard.py",
}
BLURB = {
    data.ROLE_PEKERJA: "Input awal monitoring untuk tahapan yang ditugaskan; memeriksa kembali bila diminta SPV.",
    data.ROLE_SPV: "Memantau kelengkapan 18 tahapan, memvalidasi laporan gabungan (TRUE/FALSE), menugaskan pemeriksaan kembali.",
    data.ROLE_MANAJER: "Menerima laporan gabungan, memantau, memeriksa, mengonfirmasi, dan meneruskan ke General Manager.",
}

with center:
    st.markdown(
        '<div class="pk-login"><div class="pk-brand">POLEKO</div>'
        '<div class="pk-brand-sub">Production Monitoring System · PT Royal Coconut — Airmadidi</div></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        role = st.radio("Masuk sebagai (perspektif demonstrasi)", data.ROLES, index=1)
        st.markdown(
            f'<div class="pk-rolecard" style="--c:{data.ROLE_COLOR[role]}"><b>{ui.esc(role)} · {data.ROLE_ROLE_NAME[role]}</b>'
            f"<span>{ui.esc(BLURB[role])}</span></div>",
            unsafe_allow_html=True,
        )
        worker_id = None
        if role == data.ROLE_PEKERJA:
            worker_id = st.selectbox(
                "Profil pekerja DEMO",
                list(data.DEMO_WORKERS),
                format_func=lambda w: f"{data.DEMO_WORKERS[w]['name']} — tahap " + ", ".join(f"{n:02d}" for n in data.DEMO_WORKERS[w]["stages"]),
                help="Profil dan penugasan tahapan ini konfigurasi DEMO, bukan pegawai atau penugasan nyata POLEKO.",
            )
        if st.button("Masuk", type="primary", width="stretch"):
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.worker_id = worker_id
            st.session_state.username = data.DEMO_WORKERS[worker_id]["name"] if worker_id else state.actor_name()
            st.switch_page(HOME[role])
        st.caption(
            "Autentikasi demonstrasi: tidak ada kata sandi atau kredensial nyata dan tidak ada akun yang disimpan. "
            "Menu hanya menampilkan fungsi sesuai perspektif, bukan keamanan akses produksi."
        )
        st.caption(f"⚠ {data.PROTOTYPE_BADGE}. {data.SESSION_NOTE}")
