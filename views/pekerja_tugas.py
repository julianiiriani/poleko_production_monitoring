import streamlit as st

from core import data, state, ui

ui.page_header("Tugas Pemeriksaan Kembali", "Periksa catatan SPV, perbaiki laporan, lalu kirim kembali.")

wid = st.session_state.worker_id
cycle = state.active_cycle()
tasks = sorted(state.tasks_for(worker_id=wid), key=lambda t: (t["status"] != data.T_OPEN, t["id"]))

if not tasks:
    ui.empty_state("Belum ada tugas", "Tugas muncul di sini jika SPV meminta perbaikan pada tahapan Anda.")
    st.stop()


def _open_fix(task_id):
    st.session_state[f"fix_open_{task_id}"] = True


for task in tasks:
    tid = task["id"]
    rec = state.get_record(task["cycle"], task["stage_no"])
    is_open = task["status"] == data.T_OPEN
    with st.container(border=True):
        st.markdown(f"**{data.stage_label(task['stage_no'])}** · {tid} &nbsp; {ui.badge(task['status'])}", unsafe_allow_html=True)
        ui.kv(
            [
                ("Nama Tahapan", data.STAGE_NAMES[task["stage_no"]]),
                ("Waktu permintaan perbaikan", task["created_at"]),
                ("Diminta oleh", task["created_by"]),
                ("Status tugas", ("badge", task["status"])),
            ]
        )
        if is_open:
            st.warning(f"Catatan SPV: {task['note']}")
        else:
            st.caption(f"Catatan SPV (riwayat, bukan tugas aktif): {task['note']}")
            if task["resubmitted_at"]:
                st.caption(f"Perbaikan dikirim pada {task['resubmitted_at']}.")

        if is_open:
            st.markdown("**Isian sebelum diperbaiki**")
            ui.fields_block(task["original"], stage_no=task["stage_no"])
            if not st.session_state.get(f"fix_open_{tid}"):
                st.button("Buka dan Perbaiki Laporan", type="primary", icon=":material/edit:", key=f"fix_btn_{tid}", on_click=_open_fix, args=(tid,))
            else:
                st.markdown("**Perbaiki laporan**")
                fields = ui.input_fields(f"rc_{tid}", task["stage_no"], rec["data"])
                ui.demo_validation_label()
                if st.button("Kirim Perbaikan ke SPV", type="primary", icon=":material/send:", key=f"fix_send_{tid}", width="stretch"):
                    errors = state.validate_fields(fields, task["stage_no"])
                    if errors:
                        for msg in errors:
                            st.error(msg)
                    else:
                        ok, msg = state.resubmit_task(tid, wid, fields)
                        if ok:
                            st.session_state.pop(f"fix_open_{tid}", None)
                            ui.flash_message("success", f"Laporan perbaikan telah dikirim kembali ke SPV. {msg}")
                            st.rerun()
                        else:
                            st.error(msg)
        elif task["status"] == data.T_RESENT:
            st.info("Perbaikan sudah dikirim. Menunggu pemeriksaan ulang SPV; tugas ini tidak lagi menunggu Anda.")
        else:
            st.success("SPV sudah meninjau perbaikan ini.")

rec = state.get_record(cycle, state.worker_stage(wid))
if rec:
    st.subheader("Riwayat versi laporan tahapan ini")
    ui.version_history(rec)
