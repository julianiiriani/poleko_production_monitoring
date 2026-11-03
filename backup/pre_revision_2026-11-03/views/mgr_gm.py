import streamlit as st

from core import data, state, ui

ui.page_header("Penerusan ke General Manager", "Teruskan laporan yang sudah dikonfirmasi.")

cycle = ui.report_picker()
if not cycle:
    ui.empty_state("Belum ada laporan", "Laporan harus masuk dan dikonfirmasi sebelum dapat diteruskan.")
    st.stop()

rep = state.get_report(cycle)
ui.report_stepper(rep["status"])
st.markdown(f"Tujuan: **{data.GM}** (penerima laporan)")

actor = state.actor_name()
if rep["status"] == data.R_KONFIRMASI:
    st.write(f"Penerusan akan dicatat atas nama **{actor}**.")
    if st.button(f"Teruskan ke {data.GM}", type="primary", icon=":material/forward_to_inbox:"):
        ok, msg = state.forward_to_gm(cycle, actor)
        st.session_state["_flash"] = ("success" if ok else "error", msg)
        st.rerun()
elif rep["status"] == data.R_GM:
    st.success(f"Laporan diteruskan oleh {rep['forwarded_by']} pada {rep['forwarded_at']}.")
else:
    st.button(f"Teruskan ke {data.GM}", disabled=True, icon=":material/forward_to_inbox:")
    st.warning("Laporan harus dikonfirmasi lebih dulu sebelum dapat diteruskan.")
    ui.go("views/mgr_konfirmasi.py", "Buka Pemeriksaan dan Konfirmasi", ":material/task_alt:")
