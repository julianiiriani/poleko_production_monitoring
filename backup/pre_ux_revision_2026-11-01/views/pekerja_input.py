import streamlit as st

from core import data, state, ui

ui.page_header("Input Monitoring Produksi", "Pencatatan awal per tahapan yang ditugaskan kepada Anda. SPV tidak menggantikan input ini.")

wid = st.session_state.worker_id
cycle = state.active_cycle()
assigned = state.assigned_stages(wid)
ui.cycle_caption()


def option_label(n):
    suffix = " · sudah dikirim" if state.get_record(cycle, n) else ""
    return data.stage_label(n) + suffix


no = st.selectbox("Tahapan (hanya yang ditugaskan kepada Anda)", assigned, format_func=option_label)
existing = state.get_record(cycle, no)
if state.get_report(cycle):
    st.info(f"Siklus {cycle} sudah memiliki laporan gabungan; catatan baru tidak dapat ditambahkan.")
elif existing:
    st.info(
        f"Tahap {no:02d} sudah dicatat pada siklus {cycle} (status: {existing['status']}). Catatan awal tidak ditimpa; "
        "perubahan hanya melalui Tugas Pemeriksaan Kembali dari SPV."
    )
    st.page_link("views/pekerja_tugas.py", label="Tugas Pemeriksaan Kembali", icon=":material/assignment_return:")

with st.form("inp_form"):
    ui.demo_validation_label()
    st.caption(
        "Field mengikuti Formulir Pengumpulan Data Ke-2 (bagian B). Aturan wajib isi di bawah hanya interaksi prototipe."
    )
    st.text_input("Pencatat", value=f"{state.worker_name(wid)} (profil DEMO)", disabled=True)
    fields = ui.input_fields("inp")
    a, b = st.columns(2)
    preview = a.form_submit_button("Pratinjau", width="stretch")
    send = b.form_submit_button("Kirim ke SPV (DEMO)", type="primary", width="stretch")

if preview or send:
    errors = state.validate_fields(fields)
    if errors:
        ui.demo_validation_label()
        for msg in errors:
            st.error(msg)
    elif preview:
        st.markdown(f"##### Pratinjau · {data.stage_label(no)}")
        ui.fields_block(fields)
        st.info("Ini hanya pratinjau. Tekan 'Kirim ke SPV (DEMO)' untuk mencatat sementara.")
    else:
        ok, msg = state.submit_record(cycle, no, wid, fields)
        (st.success if ok else st.error)(msg)
        if ok:
            st.markdown(ui.badge(data.S_TERKIRIM), unsafe_allow_html=True)
            st.page_link("views/pekerja_riwayat.py", label="Lihat Riwayat Pencatatan", icon=":material/history:")

ui.demo_note()
