from datetime import date

import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header(
    "Input Monitoring Produksi",
    "Pencatatan hasil monitoring per tahapan oleh SPV Produksi.",
    data.PAGE_ACTORS["input"],
)
if st.session_state.role == data.ROLE_PEKERJA:
    st.info("Pada BPMN To-Be, pencatatan laporan dilakukan SPV Produksi; Pekerja / Pelaksana menjalankan tahapan produksi.")

default_cycle = state.active_cycle() or ""

stage_label = st.selectbox("Tahapan produksi", data.STAGE_LABELS, help="18 tahapan sesuai BPMN, urutan tetap.")
stage_no = state.stage_no_from_label(stage_label)
stage_name = data.STAGE_NAMES[stage_no]

st.markdown(
    f'<div class="pk-step store" style="margin-bottom:10px"><div class="t">Tahap {stage_no:02d} dari 18 — {ui.esc(stage_name)}</div>'
    '<div class="a">Hasil dicatat setelah tahapan selesai, lalu masuk ke Data Aktivitas Proses Produksi (visual).</div></div>',
    unsafe_allow_html=True,
)

with st.form("input_form"):
    ui.demo_validation_label()
    st.caption(
        "Kolom wajib, urutan waktu, daftar satuan, dan pilihan hasil di bawah hanyalah aturan interaksi prototipe. "
        "Semuanya belum dikonfirmasi sebagai ketentuan perusahaan."
    )
    st.markdown("##### Identitas pencatatan")
    a, b = st.columns(2)
    cycle = a.text_input("ID Siklus Produksi", value=default_cycle, placeholder="mis. DEMO-001 (placeholder)")
    spv = b.text_input("Petugas pencatat (SPV Produksi)", value=st.session_state.username or "", placeholder="Nama SPV demo")
    c, d = st.columns(2)
    section = c.text_input("Bagian / unit SPV", placeholder="Placeholder — opsional")
    rec_date = d.date_input("Tanggal pencatatan", value=date.today(), format="DD/MM/YYYY")

    st.markdown("##### Waktu aktivitas")
    e, f, g = st.columns([1, 1, 1.2])
    start = e.time_input("Waktu mulai", value=None, step=300)
    end = f.time_input("Waktu selesai", value=None, step=300)
    overnight = g.checkbox(
        "Melewati pergantian hari (aturan demonstrasi)",
        help="Centang bila aktivitas selesai setelah tengah malam. Opsi ini hanya untuk interaksi prototipe.",
    )

    st.markdown("##### Data Monitoring Tahapan — Menunggu Verifikasi Formulir Resmi")
    st.caption("Kolom di bawah adalah placeholder usulan. Parameter, satuan, dan toleransi final menunggu formulir resmi POLEKO.")
    h, i = st.columns([2, 1])
    qty = h.text_input("Nilai / kuantitas (placeholder)", placeholder="Isi sesuai formulir resmi nanti")
    unit = i.selectbox("Satuan (placeholder)", data.UNIT_OPTIONS, help="Daftar satuan hanya contoh antarmuka, bukan standar perusahaan.")
    result = st.radio(
        "Hasil monitoring (usulan)",
        data.HASIL_OPTIONS,
        horizontal=True,
        help="Pilihan hasil adalah usulan antarmuka; kategori resmi menunggu formulir POLEKO.",
    )
    notes = st.text_area("Catatan / klarifikasi", placeholder="Keterangan tambahan bila diperlukan")

    p, s = st.columns(2)
    preview = p.form_submit_button("Pratinjau", width="stretch")
    submit = s.form_submit_button("Kirim Laporan Monitoring (DEMO)", type="primary", width="stretch")

fields = {
    "spv": spv.strip(),
    "section": section.strip(),
    "date": rec_date.strftime("%d/%m/%Y") if rec_date else "",
    "start": start.strftime("%H:%M") if start else None,
    "end": end.strftime("%H:%M") if end else None,
    "overnight": overnight,
    "qty": qty.strip(),
    "unit": unit,
    "result": result,
    "notes": notes.strip(),
}


def validate():
    errors = []
    if not cycle.strip():
        errors.append("ID Siklus Produksi wajib diisi.")
    if not fields["spv"]:
        errors.append("Petugas pencatat wajib diisi.")
    if start is None or end is None:
        errors.append("Waktu mulai dan waktu selesai wajib diisi.")
    elif end <= start and not overnight:
        errors.append("Waktu selesai tidak lebih akhir dari waktu mulai. Centang 'Melewati pergantian hari' bila memang demikian.")
    if not fields["qty"]:
        errors.append("Nilai / kuantitas (placeholder) wajib diisi.")
    if fields["result"] != "Sesuai" and not fields["notes"]:
        errors.append("Catatan wajib diisi bila hasil monitoring bukan 'Sesuai'.")
    return errors


if preview or submit:
    errors = validate()
    existing = state.get_record(cycle.strip(), stage_no) if cycle.strip() else None
    if existing:
        errors.append(
            f"Tahapan ini sudah dicatat pada siklus {cycle.strip()} (status: {existing['status']}). "
            "Perubahan hanya melalui alur Pemeriksaan Kembali."
        )
    if errors:
        st.caption(f"{data.DEMO_VALIDATION_LABEL}")
    for msg in errors:
        st.error(msg)

    if not errors:
        st.markdown("##### Pratinjau data yang akan dikirim")
        st.dataframe(
            pd.DataFrame(
                [
                    ("Siklus", cycle.strip()),
                    ("Tahapan", f"{stage_no:02d}. {stage_name}"),
                    ("Petugas", fields["spv"]),
                    ("Tanggal", fields["date"]),
                    ("Waktu aktivitas", state.time_text(fields)),
                    ("Nilai (placeholder)", state.value_text(fields)),
                    ("Hasil (usulan)", fields["result"]),
                    ("Catatan", fields["notes"] or "—"),
                ],
                columns=["Kolom", "Isi"],
            ),
            hide_index=True,
            width="stretch",
        )
        if submit:
            state.add_record(cycle.strip(), stage_no, fields)
            st.success(f"Tahap {stage_no:02d} tercatat pada siklus {cycle.strip()}. Status: {data.S_SUDAH}.")
            st.page_link("views/monitoring.py", label="Lihat di Monitoring Aktivitas Produksi", icon=":material/monitoring:")
        else:
            st.info("Ini hanya pratinjau. Tekan 'Kirim Laporan Monitoring (DEMO)' untuk mencatat sementara.")

ui.demo_notice()
