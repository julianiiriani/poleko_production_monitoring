import streamlit as st

from core import data, state, ui

ui.page_header("Penerusan ke General Manager", "General Manager adalah penerima laporan, bukan peran login pada prototipe ini.")

visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
if not visible:
    ui.empty_state("Belum ada laporan", "Laporan harus masuk dan dikonfirmasi sebelum dapat diteruskan.")
    ui.demo_note()
    st.stop()

cycle = st.selectbox("Pilih laporan", [r["cycle"] for r in visible], format_func=lambda c: f"{c} · {state.report_status(c)}")
rep = state.get_report(cycle)
st.markdown(f"Status: {ui.badge(rep['status'])}", unsafe_allow_html=True)
ui.report_stepper(rep["status"])
ui.info_card("Tujuan penerusan", data.GM, "Penerima laporan (DEMO) — bukan login atau dashboard terpisah")

st.write("")
if rep["status"] == data.R_KONFIRMASI:
    if st.button(f"Teruskan ke {data.GM} (DEMO)", type="primary", icon=":material/forward_to_inbox:"):
        ok, msg = state.forward_to_gm(cycle)
        st.session_state["_flash"] = ("success" if ok else "info", msg)
        st.rerun()
elif rep["status"] == data.R_GM:
    st.success(f"{data.R_GM} pada {rep['forwarded_at']}.")
else:
    st.button(f"Teruskan ke {data.GM} (DEMO)", disabled=True, icon=":material/forward_to_inbox:")
    st.error("Penerusan diblokir: laporan harus dikonfirmasi terlebih dahulu.")
    st.page_link("views/mgr_konfirmasi.py", label="Pemeriksaan dan Konfirmasi", icon=":material/task_alt:")
ui.demo_note()
