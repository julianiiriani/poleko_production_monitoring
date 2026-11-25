import streamlit as st

from core import data, state, ui

wid = st.session_state.worker_id
cycle = state.active_cycle()
no = state.worker_stage(wid)  # otomatis mengikuti akun yang login; pekerja tidak memilih tahapan
rec = state.get_record(cycle, no)

ui.page_header("Input Monitoring Produksi", data.stage_label(no))


def _show_errors(errors):
    for msg in errors:
        st.error(msg)


if not rec and state.friday_blocked():
    st.info("Hari Jumat tidak ada produksi.")
elif not rec:
    fields = ui.input_fields("inp", no)
    if st.button("Kirim Laporan", type="primary", icon=":material/send:", width="stretch"):
        errors = state.validate_fields(fields, no)
        if errors:
            _show_errors(errors)
        else:
            ok, msg = state.submit_record(cycle, no, wid, fields)
            if ok:
                ui.flash_message("success", msg)
                st.rerun()
            else:
                st.error(msg)
else:
    info = state.edit_info(rec)
    ui.kv([("Status", ("badge", rec["status"])), ("Dikirim", rec["sent_at"])])
    if info["can_edit"]:
        st.caption(f"Dapat diedit sampai {info['deadline']}.")
        fields = ui.input_fields(f"edt{len(rec['versions'])}", no, rec["data"])
        if st.button("Simpan Perubahan", type="primary", icon=":material/save:", width="stretch"):
            errors = state.validate_fields(fields, no)
            if errors:
                _show_errors(errors)
            else:
                ok, msg = state.edit_record(cycle, no, wid, fields)
                if ok:
                    ui.flash_message("success", msg)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        if info.get("via_task"):
            st.warning("Supervisor meminta perbaikan.")
            ui.go("views/pekerja_tugas.py", "Buka Tugas Pemeriksaan Kembali", ":material/assignment_return:")
        ui.fields_block(rec["data"], stage_no=no)
