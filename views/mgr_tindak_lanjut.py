"""Tindak lanjut data yang diarahkan kepada manajemen (Aturan Main bagian 5).

PPIC              : data Kuning (waktu, durasi, kg di luar batas) — tanggapan.
Production Manager: data Merah kendala/kerusakan mesin — tanggapan wajib sebelum laporan diteruskan ke General Manager.
QC                : data Merah mutu (Tahap 8, 12, 18) — temuan + unggah gambar wajib, lalu diteruskan ke QA.
QA                : keputusan mutu akhir (di atas QC) + gambar opsional — wajib sebelum laporan diteruskan ke General Manager.
"""
import streamlit as st

from core import data, state, ui

who = state.identity()
cycle = state.active_cycle()
TITLE = {data.PM: "Kendala Mesin", data.PPIC: "Data di Luar Batas", data.QC: "Pemeriksaan Mutu", data.QA: "Keputusan Mutu"}
ui.page_header(TITLE.get(who, "Tindak Lanjut Data"))

items = state.followups_for(who, cycle)
if not items:
    ui.empty_state("Belum ada data", "Data muncul setelah Supervisor memeriksa input yang diarahkan kepada Anda.")
    st.stop()

items = sorted(items, key=lambda x: (x[1]["status"] != data.F_MENUNGGU, x[0]["stage_no"]))
for rec, fu in items:
    no = rec["stage_no"]
    with st.container(border=True):
        st.markdown(f"**{data.stage_label(no)}** &nbsp; {ui.badge(rec['level'])} &nbsp; {ui.badge(fu['status'])}", unsafe_allow_html=True)
        ui.kv(
            [
                ("Shift", data.shift_label(rec["shift"])),
                ("Diperiksa Supervisor", f"{rec['confirmed_by']} · {rec['confirmed_at']}" if rec["confirmed_by"] else "—"),
                ("Diarahkan pada", fu["at"]),
                ("Pekerja", rec["worker_name"]),
            ]
        )
        for i in rec.get("issues", []):
            st.warning(f"{i['kind']}: {i['text']}")
        with st.expander("Isi data tahapan"):
            ui.fields_block(rec["data"], stage_no=no)
        if who == data.QA:
            qc_fu = rec["followups"].get(data.RT_QC, {})
            st.markdown(f"**Temuan QC** ({qc_fu.get('by')} · {qc_fu.get('done_at')}): {qc_fu.get('note')}")
            ui.images_block(qc_fu.get("images"))

        if fu["status"] != data.F_MENUNGGU:
            st.success(f"{fu['status']} oleh {fu['by']} pada {fu['done_at']}." + (f" Keputusan: {fu['decision']}." if fu.get("decision") else ""))
            st.write(f"Catatan: {fu['note']}")
            ui.images_block(fu.get("images"))
            continue

        key = f"fu_{who}_{no}"
        decision = None
        if who == data.QA:
            decision = st.radio("Keputusan mutu", data.QA_DECISIONS, index=None, horizontal=True, key=f"{key}_dec")
        label = {data.QC: "Temuan pemeriksaan mutu", data.QA: "Catatan keputusan"}.get(who, "Tanggapan")
        note = st.text_area(label, key=f"{key}_note", placeholder="Wajib diisi")
        images = []
        if who in (data.QC, data.QA):  # fitur unggah gambar hanya untuk QC dan QA
            files = st.file_uploader(
                "Unggah gambar bukti (JPG/PNG)" + (" — wajib" if who == data.QC else " — opsional"),
                type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"{key}_img",
            )
            images = [(f.name, f.getvalue()) for f in (files or [])]
        btn = {data.QC: "Simpan Temuan dan Teruskan ke QA", data.QA: "Simpan Keputusan Mutu"}.get(who, "Simpan Tanggapan")
        if st.button(btn, type="primary", icon=":material/send:", key=f"{key}_go"):
            ok, msg = state.respond_followup(cycle, no, who, note, images, decision)
            ui.flash_message("success" if ok else "error", msg)
            st.rerun()
