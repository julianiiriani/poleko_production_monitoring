import streamlit as st

from core import data, state, ui

ui.page_header("Input Monitoring Produksi", "Catat hasil tahapan yang menjadi tanggung jawab Anda.")

wid = st.session_state.worker_id
cycle = state.active_cycle()
no = state.worker_stage(wid)  # otomatis mengikuti akun yang login; pekerja tidak memilih tahapan
rec = state.get_record(cycle, no)

st.subheader("Informasi tahapan")
ui.kv(
    [
        ("Nama Tahapan", data.STAGE_NAMES[no]),
        ("Kode Tahapan", data.stage_code(no)),
        ("Pekerja", state.worker_name(wid)),
        ("Waktu input", state.now_str()),
    ]
)


def _show_errors(errors):
    for msg in errors:
        st.error(msg)


if not rec:
    st.subheader("Isi laporan")
    fields = ui.input_fields("inp", no)
    ui.demo_validation_label()
    if st.button("Kirim Laporan ke SPV", type="primary", icon=":material/send:", width="stretch"):
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
    ui.kv([("Status penginputan", ("badge", state.input_status(rec))), ("Status pemeriksaan SPV", ("badge", rec["status"]))])
    if info["can_edit"]:
        st.info(
            f"Laporan sudah dikirim. Anda masih dapat mengedit sampai **{info['deadline']}** "
            f"(aturan akses prototipe {data.EDIT_WINDOW_HOURS} jam sejak pengiriman, bukan kebijakan resmi perusahaan). "
            "Setiap perubahan disimpan sebagai versi baru; versi awal tidak dihapus."
        )
        st.subheader("Edit laporan")
        fields = ui.input_fields(f"edt{len(rec['versions'])}", no, rec["data"])
        ui.demo_validation_label()
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
        st.warning(info["reason"])
        if info.get("via_task"):
            ui.go("views/pekerja_tugas.py", "Buka Tugas Pemeriksaan Kembali", ":material/assignment_return:")
        st.subheader("Isi laporan terkirim")
        ui.fields_block(rec["data"], stage_no=no)
    st.subheader("Riwayat versi laporan")
    ui.version_history(rec)
