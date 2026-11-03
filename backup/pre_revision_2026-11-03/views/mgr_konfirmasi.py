import streamlit as st

from core import data, state, ui

ui.page_header("Pemeriksaan dan Konfirmasi", "Periksa laporan, lalu konfirmasi.")

cycle = ui.report_picker()
if not cycle:
    ui.empty_state("Belum ada laporan untuk diperiksa", "Konfirmasi baru tersedia setelah SPV meneruskan laporan ke PPIC.")
    st.stop()

rep = state.get_report(cycle)
ui.report_stepper(rep["status"])
with st.expander("Periksa isi laporan (18 tahapan)"):
    ui.report_preview(rep)

st.subheader("Konfirmasi")
actor = state.actor_name()
if rep["status"] == data.R_MASUK:
    st.write(f"Konfirmasi akan dicatat atas nama **{actor}**.")
    checked = st.checkbox("Saya sudah memeriksa laporan gabungan ini.", key=f"cf_check_{cycle}")
    if st.button("Konfirmasi Laporan", type="primary", disabled=not checked, icon=":material/task_alt:"):
        ok, msg = state.confirm_report(cycle, actor)
        st.session_state["_flash"] = ("success" if ok else "error", msg)
        st.rerun()
    if not checked:
        st.caption("Centang pernyataan di atas untuk mengaktifkan tombol.")
else:
    st.success(f"Laporan sudah dikonfirmasi oleh {rep['confirmed_by']} pada {rep['confirmed_at']}.")
    if rep["status"] == data.R_KONFIRMASI:
        ui.go("views/mgr_gm.py", f"Lanjut ke Penerusan ke {data.GM}", ":material/forward_to_inbox:")
