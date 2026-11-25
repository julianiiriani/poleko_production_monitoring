import streamlit as st

from core import data, state, ui

HOME = {
    data.ROLE_PEKERJA: "views/pekerja_dashboard.py",
    data.ROLE_SPV: "views/spv_dashboard.py",
    data.ROLE_MANAJER: "views/mgr_dashboard.py",
}
GROUP_TITLE = {
    data.ROLE_PEKERJA: "Pekerja Produksi",
    data.ROLE_SPV: "Supervisor",
    data.ROLE_MANAJER: "Manajemen",
}

_, center, _ = st.columns([1, 1.6, 1])
with center:
    ui.brand(sidebar=False, width=210)
    with st.container(border=True):
        st.markdown(
            """<style>
            .st-key-login_role { width: 100%; margin-bottom: -0.6rem; }
            .st-key-login_role [data-testid="stRadio"], .st-key-login_role > div { gap: 0.25rem; padding-bottom: 0; }
            .st-key-login_title { margin-bottom: 0.5rem; }
            .st-key-login_title p { margin: 0; }
            .st-key-login_role [data-testid="stWidgetLabel"] { width: 100%; justify-content: center; margin-bottom: 0.5rem; }
            .st-key-login_role [data-testid="stWidgetLabel"] * { text-align: center; }
            .st-key-login_role [role="radiogroup"] {
                width: 100%; justify-content: center; align-items: center;
                column-gap: 1.25rem; row-gap: 0.25rem; flex-wrap: wrap;
            }
            .st-key-login_role [role="radiogroup"] > label { margin: 0; }
            </style>""",
            unsafe_allow_html=True,
        )
        with st.container(key="login_title"):
            st.markdown(
                "<div style='width:100%;text-align:center;font-size:1.5rem;font-weight:700;line-height:1.3'>Login</div>",
                unsafe_allow_html=True,
            )
        role = st.radio("Masuk sebagai", data.ROLES, format_func=GROUP_TITLE.get, horizontal=True, key="login_role")
        ids = data.LOGIN_GROUPS[role]
        account = st.selectbox(
            "Akun",
            ids,
            index=None,
            placeholder="Pilih akun",
            format_func=lambda i: data.DEMO_ACCOUNTS[i]["label"],
            key=f"login_acc_{role}",
        )
        with st.form("login_form", border=False):
            password = st.text_input("Password", type="password", placeholder="Masukkan password.")
            submit = st.form_submit_button("Login", type="primary", width="stretch")
        if submit:
            acc = state.authenticate(account, password) if account else None
            if acc is None:
                st.error("Pilih akun terlebih dahulu.")
            else:
                state.sign_in(account)
                st.switch_page(HOME[acc["role"]])
