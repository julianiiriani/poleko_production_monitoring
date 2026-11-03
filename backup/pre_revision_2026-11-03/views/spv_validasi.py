import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Validasi Laporan", "Satu keputusan untuk seluruh laporan siklus ini (18 tahapan).", cycle=True)

# Bersihkan isian setelah catatan perbaikan terkirim (harus sebelum widget dibuat).
if st.session_state.pop("_clear_val", False):
    for k in ("val_stages", "val_note", "val_decision"):
        st.session_state.pop(k, None)

cycle = state.active_cycle()
gate = state.completeness(cycle)
rep = state.get_report(cycle)

st.subheader("1. Periksa kelengkapan")
if rep:
    st.success(f"Keputusan {data.V_DITERIMA} sudah dibuat untuk siklus {cycle}. Laporan gabungan tidak dibuat ulang.")
elif gate["ready"]:
    st.success("Semua 18 tahapan sudah dicatat dan tidak ada pemeriksaan ulang yang tertunda.")
else:
    reasons = []
    if gate["missing"]:
        reasons.append("Belum dicatat: " + ", ".join(f"{n:02d} {data.STAGE_NAMES[n]}" for n in gate["missing"]))
    if gate["rechecking"]:
        reasons.append("Masih menunggu perbaikan Pekerja: " + ", ".join(f"{n:02d}" for n in gate["rechecking"]))
    if gate["awaiting_review"]:
        reasons.append("Kiriman ulang menunggu tinjauan Anda: " + ", ".join(f"{n:02d}" for n in gate["awaiting_review"]))
    st.warning("**Laporan belum bisa diterima.**\n\n" + "\n\n".join(f"- {r}" for r in reasons))
    if gate["awaiting_review"]:
        ui.go("views/spv_penugasan.py", "Tinjau Kiriman Ulang", ":material/assignment_return:")
with st.expander("Periksa isi 18 tahapan sebelum memutuskan" if not rep else "Isi 18 tahapan"):
    ui.report_preview(state.draft_report(cycle), draft=True)

st.subheader("2. Keputusan")
if rep:
    st.markdown(f"Status laporan: {ui.badge(rep['status'])}", unsafe_allow_html=True)
    ui.report_stepper(rep["status"])
    if rep["status"] == data.R_GENERATED:
        if st.button("Teruskan ke PPIC", type="primary", icon=":material/forward:"):
            ok, msg = state.handoff_to_ppic(cycle)
            st.session_state["_flash"] = ("success" if ok else "info", msg)
            st.rerun()
    ui.go("views/spv_laporan.py", "Buka Laporan Gabungan", ":material/description:")
    st.stop()

decision = st.radio(
    "Keputusan SPV",
    [data.V_DITERIMA, data.V_PERBAIKAN],
    index=None,
    key="val_decision",
    captions=["Semua tahapan sudah benar. Buat laporan gabungan.", "Ada tahapan yang harus diperiksa ulang oleh Pekerja."],
)

if decision == data.V_DITERIMA:
    if st.button("Selesaikan Validasi dan Buat Laporan Gabungan", type="primary", disabled=not gate["ready"], icon=":material/check_circle:"):
        ok, msg = state.accept_report(cycle)
        if ok:
            st.session_state["_flash"] = ("success", msg + " Teruskan ke PPIC agar Manajemen dapat memeriksanya.")
            st.rerun()
        st.error(msg)
    if not gate["ready"]:
        st.caption("Tombol aktif setelah semua tahapan lengkap dan pemeriksaan ulang selesai.")

elif decision == data.V_PERBAIKAN:
    candidates = [n for n in data.STAGE_NOS if state.get_record(cycle, n) and n not in gate["rechecking"]]
    if not candidates:
        ui.empty_state("Belum ada tahapan yang bisa diperbaiki", "Tahapan harus sudah dicatat dan belum memiliki tugas yang menunggu Pekerja.")
        st.stop()
    chosen = st.multiselect("Tahapan yang Perlu Diperbaiki", candidates, format_func=data.stage_label, key="val_stages", placeholder="Pilih satu atau beberapa tahapan")
    note = st.text_area("Jelaskan bagian yang perlu diperbaiki", key="val_note", placeholder="Contoh: Mohon periksa kembali waktu mulai dan waktu selesai.")
    if chosen:
        with st.container(border=True):
            st.markdown("**Ringkasan penugasan** — periksa sebelum dikirim")
            ui.table(
                pd.DataFrame(
                    [{"Tahapan": data.stage_label(n), "Pekerja yang ditugaskan": state.get_record(cycle, n)["worker_name"]} for n in chosen]
                )
            )
            st.markdown(f"**Catatan:** {note.strip() or '(belum diisi)'}")
    ui.demo_validation_label()
    if st.button("Kirim Catatan Perbaikan", type="primary", icon=":material/assignment_return:"):
        ok, msg, made = state.issue_recheck(cycle, chosen, note)
        if ok:
            names = ", ".join(sorted({state.worker_name(t["worker_id"]) for t in made}))
            st.session_state["_clear_val"] = True
            st.session_state["_flash"] = ("success", f"Catatan perbaikan terkirim kepada {names}. {msg}")
            st.rerun()
        else:
            st.error(msg)
