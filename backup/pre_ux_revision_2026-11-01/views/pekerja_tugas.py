import streamlit as st

from core import data, state, ui

ui.page_header("Tugas Pemeriksaan Kembali", "Periksa informasi yang diminta SPV, koreksi atau klarifikasi, lalu kirim ulang.")

wid = st.session_state.worker_id
tasks = sorted(state.tasks_for(worker_id=wid), key=lambda t: (t["status"] != data.T_OPEN, t["id"]))

if not tasks:
    ui.empty_state("Belum ada tugas pemeriksaan kembali", "Tugas muncul di sini bila SPV memutuskan FALSE dan memilih tahapan Anda.")
    ui.demo_note()
    st.stop()

by_id = {t["id"]: t for t in tasks}
task_id = st.selectbox(
    "Pilih tugas",
    list(by_id),
    format_func=lambda i: f"{i} · {by_id[i]['cycle']} · Tahap {by_id[i]['stage_no']:02d} · {by_id[i]['status']}",
)
task = by_id[task_id]
rec = state.get_record(task["cycle"], task["stage_no"])

st.markdown(
    f"**{data.stage_label(task['stage_no'])}** · Siklus {task['cycle']} &nbsp; {ui.badge(task['status'])}",
    unsafe_allow_html=True,
)
if task["status"] == data.T_OPEN:
    st.warning(f"Catatan SPV (aktif): {task['note']}")
else:
    st.caption(f"Catatan SPV sebelumnya (riwayat, bukan tugas aktif): {task['note']}")

st.markdown("##### Informasi yang dikirim sebelumnya")
ui.fields_block(task["original"])

if task["status"] == data.T_OPEN:
    st.markdown("##### Koreksi atau klarifikasi")
    with st.form(f"rc_form_{task_id}"):
        ui.demo_validation_label()
        fields = ui.input_fields(f"rc_{task_id}", rec["data"])
        send = st.form_submit_button("Kirim ulang ke SPV", type="primary", width="stretch")
    if send:
        errors = state.validate_fields(fields)
        if errors:
            for msg in errors:
                st.error(msg)
        else:
            ok, msg = state.resubmit_task(task_id, wid, fields)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()
else:
    st.markdown("##### Informasi yang Anda kirim ulang")
    if task["response"]:
        ui.fields_block(task["response"])
    if task["status"] == data.T_RESENT:
        st.info("Menunggu tinjauan SPV. Tugas ini tidak lagi menunggu koreksi dari Anda.")
    else:
        st.success("SPV sudah meninjau kiriman ulang ini.")

with st.expander("Riwayat versi catatan tahapan ini"):
    ui.version_history(rec)
ui.demo_note()
