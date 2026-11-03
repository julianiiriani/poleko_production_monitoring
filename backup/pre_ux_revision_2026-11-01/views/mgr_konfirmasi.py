import streamlit as st

from core import data, state, ui

ui.page_header("Pemeriksaan dan Konfirmasi", "Periksa laporan gabungan yang masuk, lalu konfirmasi. Tidak ada input ulang data produksi.")

visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
if not visible:
    ui.empty_state("Belum ada laporan untuk diperiksa", "Konfirmasi diblokir sebelum laporan diteruskan SPV ke PPIC.")
    ui.demo_note()
    st.stop()

cycle = st.selectbox("Pilih laporan", [r["cycle"] for r in visible], format_func=lambda c: f"{c} · {state.report_status(c)}")
rep = state.get_report(cycle)
st.markdown(f"Status: {ui.badge(rep['status'])}", unsafe_allow_html=True)
ui.report_stepper(rep["status"])
ui.report_preview(rep)

st.subheader("Konfirmasi")
if rep["status"] == data.R_MASUK:
    checked = st.checkbox("Saya telah memeriksa laporan gabungan 18 tahapan ini (aksi demonstrasi).", key="cf_check")
    if st.button("Konfirmasi laporan", type="primary", disabled=not checked, icon=":material/task_alt:"):
        ok, msg = state.confirm_report(cycle)
        st.session_state["_flash"] = ("success" if ok else "info", msg)
        st.rerun()
else:
    st.success(f"Laporan sudah dikonfirmasi pada {rep['confirmed_at']}.")
    st.page_link("views/mgr_gm.py", label="Penerusan ke General Manager", icon=":material/forward_to_inbox:")
ui.demo_note()
