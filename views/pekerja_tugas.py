import streamlit as st

from core import data, state, ui

ui.page_header("Tugas Pemeriksaan Kembali")

wid = st.session_state.worker_id
cycle = state.active_cycle()
tasks = sorted(state.tasks_for(worker_id=wid), key=lambda t: (t["status"] != data.T_OPEN, t["id"]))

if not tasks:
    ui.empty_state("Belum ada tugas", "Tugas muncul di sini jika Supervisor meminta perbaikan pada tahapan Anda.")
    st.stop()


for task in tasks:
    tid = task["id"]
    rec = state.get_record(task["cycle"], task["stage_no"])
    is_open = task["status"] == data.T_OPEN
    with st.container(border=True):
        st.markdown(f"**{data.stage_label(task['stage_no'])}** &nbsp; {ui.badge(task['status'])}", unsafe_allow_html=True)
        st.caption(f"{task['created_by']} · {task['created_at']}")
        if is_open:
            st.warning(task["note"])
            fields = ui.input_fields(f"rc_{tid}", task["stage_no"], rec["data"])
            if st.button("Kirim Perbaikan", type="primary", icon=":material/send:", key=f"fix_send_{tid}", width="stretch"):
                errors = state.validate_fields(fields, task["stage_no"])
                if errors:
                    for msg in errors:
                        st.error(msg)
                else:
                    ok, msg = state.resubmit_task(tid, wid, fields)
                    ui.flash_message("success" if ok else "error", msg)
                    st.rerun()
        else:
            st.write(task["note"])
