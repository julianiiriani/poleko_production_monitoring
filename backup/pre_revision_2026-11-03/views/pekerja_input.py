import streamlit as st

from core import data, state, ui

ui.page_header("Input Monitoring Produksi", "Catat hasil tahapan yang menjadi tanggung jawab Anda.", cycle=True)

wid = st.session_state.worker_id
cycle = state.active_cycle()
assigned = state.assigned_stages(wid)


def option_label(n):
    return data.stage_label(n) + (" · sudah dikirim" if state.get_record(cycle, n) else "")


if len(assigned) == 1:  # satu pekerja = satu tahapan: tidak perlu memilih
    no = assigned[0]
    st.markdown(f"**Tahapan Anda:** {data.stage_label(no)}")
else:
    no = st.selectbox("Tahapan Anda", assigned, format_func=option_label)
existing = state.get_record(cycle, no)

if state.get_report(cycle):
    st.info(f"Siklus {cycle} sudah memiliki laporan gabungan, sehingga catatan baru tidak dapat ditambahkan.")
elif existing:
    st.info(f"Tahap {no:02d} sudah dikirim ke SPV ({existing['status']}). Perubahan hanya bisa dilakukan jika SPV mengirim tugas pemeriksaan kembali.")
    ui.go("views/pekerja_tugas.py", "Buka Tugas Pemeriksaan Kembali", ":material/assignment_return:")
else:
    st.caption(f"Pencatat: {state.worker_name(wid)}")
    with st.form("inp_form"):
        fields = ui.input_fields("inp")
        ui.demo_validation_label()
        a, b = st.columns(2)
        preview = a.form_submit_button("Pratinjau", width="stretch")
        send = b.form_submit_button("Kirim ke SPV", type="primary", width="stretch")

    if preview or send:
        errors = state.validate_fields(fields)
        if errors:
            for msg in errors:
                st.error(msg)
        elif preview:
            st.markdown(f"##### Pratinjau · {data.stage_label(no)}")
            ui.fields_block(fields)
            st.info("Ini baru pratinjau. Tekan Kirim ke SPV untuk mengirim catatan.")
        else:
            ok, msg = state.submit_record(cycle, no, wid, fields)
            if ok:
                st.session_state["_flash"] = ("success", f"Catatan terkirim ke SPV. {msg}")
                st.rerun()
            else:
                st.error(msg)
