import streamlit as st

from core import data, state, ui

HOME = {
    data.ROLE_PEKERJA: "views/pekerja_dashboard.py",
    data.ROLE_SPV: "views/spv_dashboard.py",
    data.ROLE_MANAJER: "views/mgr_dashboard.py",
}
GROUP_TITLE = {
    data.ROLE_PEKERJA: "Pekerja Produksi",
    data.ROLE_SPV: "SPV Produksi",
    data.ROLE_MANAJER: "Manajemen",
}

ui.brand(sidebar=False, width=210)
_, center, _ = st.columns([1, 1.6, 1])
with center:
    with st.container(border=True):
        st.markdown("#### Login")
        role = st.radio("Masuk sebagai", data.ROLES, format_func=GROUP_TITLE.get, horizontal=True, key="login_role")
        ids = data.LOGIN_GROUPS[role]
        account = st.selectbox(
            "Akun",
            ids,
            index=0 if len(ids) == 1 else None,  # satu-satunya akun (SPV) langsung terpilih
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
    st.caption("Prototype demonstrasi: login ini bukan sistem keamanan produksi.")
