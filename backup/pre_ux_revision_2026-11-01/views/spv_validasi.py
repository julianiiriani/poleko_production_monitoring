import streamlit as st

from core import data, state, ui

ui.page_header("Validasi Laporan", "Satu keputusan TRUE/FALSE untuk laporan gabungan siklus terpilih (18 tahapan).")

# Bersihkan isian FALSE setelah tugas dibuat (harus sebelum widget dibuat).
if st.session_state.pop("_clear_val", False):
    for k in ("val_stages", "val_note", "val_decision"):
        st.session_state.pop(k, None)

cycle = state.active_cycle()
gate = state.completeness(cycle)
rep = state.get_report(cycle)

ui.stat_grid(
    [
        ("Tahapan tercatat", gate["recorded"], data.ROLE_COLOR[data.ROLE_SPV], "/ 18"),
        ("Belum dicatat", len(gate["missing"]), data.STATUS_STYLE[data.S_BELUM][0], "tahapan"),
        ("Menunggu pekerja", len(gate["rechecking"]), data.STATUS_STYLE[data.S_KEMBALI][0], "tahapan"),
        ("Kiriman ulang belum ditinjau", len(gate["awaiting_review"]), data.STATUS_STYLE[data.S_KIRIM_ULANG][0], "tahapan"),
    ]
)

if not gate["ready"] and not rep:
    reasons = []
    if gate["missing"]:
        reasons.append("Belum dicatat: " + ", ".join(f"{n:02d} {data.STAGE_NAMES[n]}" for n in gate["missing"]))
    if gate["rechecking"]:
        reasons.append("Masih diperiksa kembali oleh pekerja: " + ", ".join(f"{n:02d}" for n in gate["rechecking"]))
    if gate["awaiting_review"]:
        reasons.append("Kiriman ulang menunggu tinjauan SPV: " + ", ".join(f"{n:02d}" for n in gate["awaiting_review"]))
    st.warning("**TRUE diblokir** sampai syarat berikut terpenuhi.\n\n" + "\n\n".join(f"- {r}" for r in reasons))

st.subheader("Konteks tinjauan: 18 tahapan")
ui.overview_table(state.overview_df(cycle))

st.subheader("Keputusan validasi")
if rep:
    st.success(f"Keputusan {data.V_TRUE} sudah dibuat untuk {cycle}. Laporan gabungan tidak dibuat ulang.")
    st.markdown(f"Status laporan: {ui.badge(rep['status'])}", unsafe_allow_html=True)
    ui.report_stepper(rep["status"])
    if rep["status"] == data.R_GENERATED:
        if st.button("Teruskan ke PPIC", type="primary", icon=":material/forward:"):
            ok, msg = state.handoff_to_ppic(cycle)
            st.session_state["_flash"] = ("success" if ok else "info", msg)
            st.rerun()
    st.page_link("views/spv_laporan.py", label="Buka pratinjau Laporan Gabungan", icon=":material/description:")
    ui.demo_note()
    st.stop()

decision = st.radio("Keputusan SPV", [data.V_TRUE, data.V_FALSE], index=None, horizontal=True, key="val_decision")

if decision == data.V_TRUE:
    st.caption("TRUE menghasilkan satu laporan gabungan otomatis berisi 18 tahapan dari catatan Pekerja; SPV tidak menyusunnya manual.")
    if st.button("Validasi dan hasilkan laporan gabungan", type="primary", disabled=not gate["ready"], icon=":material/check_circle:"):
        ok, msg = state.validate_true(cycle)
        (st.success if ok else st.error)(msg)
        if ok:
            st.rerun()
    if not gate["ready"]:
        st.error("TRUE tidak dapat dipilih sebelum syarat kelengkapan terpenuhi (lihat peringatan di atas).")

elif decision == data.V_FALSE:
    st.caption("FALSE membuat tugas pemeriksaan kembali untuk Pekerja yang menginput tahapan terpilih. Laporan tidak dihasilkan.")
    candidates = [n for n in data.STAGE_NOS if state.get_record(cycle, n) and n not in gate["rechecking"]]
    if not candidates:
        ui.empty_state("Belum ada tahapan yang dapat dikembalikan", "Tahapan harus sudah dicatat dan belum memiliki tugas aktif.")
    else:
        chosen = st.multiselect("Tahapan yang perlu diperiksa kembali", candidates, format_func=data.stage_label, key="val_stages", placeholder="Pilih tahapan")
        if chosen:
            st.markdown("**Pekerja penanggung jawab (dari penugasan DEMO):**")
            for n in chosen:
                st.markdown(f"- {data.stage_label(n)} → {state.get_record(cycle, n)['worker_name']}")
        note = st.text_area("Catatan SPV (wajib)", key="val_note", placeholder="Jelaskan apa yang perlu diperiksa atau dikoreksi.")
        st.caption(data.DEMO_VALIDATION_LABEL + " — catatan wajib diisi hanya aturan interaksi prototipe.")
        if st.button("Tugaskan pemeriksaan kembali", type="primary", icon=":material/assignment_return:"):
            ok, msg, _ = state.issue_recheck(cycle, chosen, note)
            if ok:
                st.session_state["_clear_val"] = True
                st.session_state["_flash"] = ("success", msg + " Terlihat pada dashboard Pekerja terkait.")
                st.rerun()
            else:
                st.error(msg)
ui.demo_note()
