import streamlit as st

from core import data, state, ui

HOME = {
    data.ROLE_PEKERJA: "views/pekerja_dashboard.py",
    data.ROLE_SPV: "views/spv_dashboard.py",
    data.ROLE_MANAJER: "views/mgr_dashboard.py",
}

def _account_label(account_id):
    acc = data.DEMO_ACCOUNTS[account_id]
    if acc["worker_id"]:
        no = data.DEMO_WORKERS[acc["worker_id"]]["stages"][0]
        return f"{acc['label']} · Tahap {no:02d} — {data.STAGE_NAMES[no]}"
    return f"{acc['label']} · {acc['role']}"


_, center, _ = st.columns([1, 1.5, 1])
with center:
    ui.brand(sidebar=False, width=260)
    with st.form("login_form"):
        st.markdown("#### Login")
        account = st.selectbox(
            "Akun",
            list(data.DEMO_ACCOUNTS),
            index=None,
            placeholder="Pilih akun",
            format_func=_account_label,
        )
        password = st.text_input("Password", type="password", placeholder="Belum diperlukan pada demo")
        submit = st.form_submit_button("Login", type="primary", width="stretch")
    if submit:
        acc = state.authenticate(account, password)
        if acc is None:
            st.error("Pilih akun terlebih dahulu.")
        else:
            state.sign_in(account)
            st.switch_page(HOME[acc["role"]])
    st.caption("Prototype demonstrasi: login ini bukan sistem keamanan produksi.")
