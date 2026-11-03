import streamlit as st

from core import data, state, ui

ui.page_header("Ringkasan Hasil per Tahapan", "Periksa isi catatan satu tahapan seperti yang dikirim Pekerja.")

cycle = state.active_cycle()
no = st.selectbox("Tahapan", data.STAGE_NOS, format_func=data.stage_label)
rec = state.get_record(cycle, no)

if not rec:
    wid = state.worker_for_stage(no)
    ui.empty_state("Belum Dicatat", f"{state.worker_name(wid)} (penugasan DEMO) belum mengirim catatan untuk tahapan ini pada {cycle}.")
else:
    st.markdown(f"**{data.stage_label(no)}** &nbsp; {ui.badge(rec['status'])}", unsafe_allow_html=True)
    ui.fields_block(rec["data"], extra=[("Dicatat oleh", rec["worker_name"]), ("Diperbarui", rec["updated_at"])])
    if rec["status"] == data.S_KEMBALI:
        task = next((t for t in state.tasks_for(cycle, statuses=[data.T_OPEN]) if t["stage_no"] == no), None)
        if task:
            st.warning(f"Catatan SPV aktif ({task['id']}): {task['note']}")
    st.markdown("##### Riwayat versi")
    ui.version_history(rec)
ui.demo_note()
