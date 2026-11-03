import streamlit as st

from core import data, state, ui

ss = st.session_state
goto = ss.pop("_goto", None)
if goto:  # setelah Generate Report berhasil, langsung ke Laporan Gabungan (pesan berhasil ikut dibawa)
    ss["_flash"] = goto[1]
    st.switch_page(goto[0])

ui.page_header("Validasi Laporan", "Periksa setiap tahapan secara individual, lalu Generate Report setelah 18 tahapan terkonfirmasi.")

cycle = state.active_cycle()
g = state.completeness(cycle)
rep = state.get_report(cycle)
actor = state.actor_name()

def _open_contact(n):
    ss[f"val_contact_{n}"] = True


st.progress(len(g["confirmed"]) / 18, text=f"{len(g['confirmed'])} dari 18 tahapan sudah dikonfirmasi SPV")

# ------------------------------------------------------------ 1. pemeriksaan per tahapan
st.subheader("1. Pemeriksaan per tahapan")
pick = ss.pop("_val_pick", None)
if pick in data.STAGE_NOS:
    ss["val_stage"] = pick
elif "val_stage" not in ss:
    ss["val_stage"] = next((n for n in data.STAGE_NOS if state.stage_status(cycle, n) in (data.S_MENUNGGU, data.S_ULANG)), 1)
stage_labels = {n: f"{data.stage_label(n)} — {state.stage_status(cycle, n)}" for n in data.STAGE_NOS}
no = st.selectbox("Pilih tahapan", data.STAGE_NOS, key="val_stage", format_func=stage_labels.get)
rec = state.get_record(cycle, no)
wid = state.worker_for_stage(no)

st.markdown(f"#### {data.stage_label(no)} &nbsp; {ui.badge(state.stage_status(cycle, no))}", unsafe_allow_html=True)
ui.kv(
    [
        ("Pekerja Penanggung Jawab", state.worker_name(wid)),
        ("Kode Tahapan", data.stage_code(no)),
        ("Status penginputan", ("badge", state.input_status(rec))),
        ("Waktu pengiriman terakhir", state.sent_text(rec)),
    ]
)

if not rec:
    st.info(f"Belum ada laporan untuk tahapan ini. Menunggu penginputan {state.worker_name(wid)}; hubungi pekerja tersebut agar segera menginput.")
    st.button("Konfirmasi Tahapan", disabled=True, key="val_cf_off")
    st.caption("Konfirmasi dan permintaan perbaikan baru tersedia setelah Pekerja mengirim laporan.")
else:
    ui.fields_block(rec["data"], stage_no=no)
    if len(rec["versions"]) > 1:
        st.markdown(f"**Riwayat versi ({len(rec['versions'])} versi) — buka versi terbaru atau sebelumnya**")
        ui.version_history(rec)

    status = rec["status"]
    editable_cycle = not rep or rep["status"] == data.R_PERBAIKAN  # setelah laporan diteruskan, tahapan terkunci
    can_confirm = status in (data.S_MENUNGGU, data.S_ULANG) and editable_cycle
    can_contact = status in (data.S_MENUNGGU, data.S_ULANG, data.S_KONFIRMASI) and editable_cycle

    if status == data.S_KONFIRMASI:
        st.success(f"Dikonfirmasi oleh {rec['confirmed_by']} pada {rec['confirmed_at']}. Laporan pekerja terkunci.")
        if rep and rep["status"] != data.R_PERBAIKAN:
            st.caption("Laporan gabungan sudah dihasilkan; tahapan ini tidak dapat diubah.")
    elif status == data.S_KEMBALI:
        st.warning(f"Menunggu perbaikan dari {rec['worker_name']}. Catatan SPV: {rec['spv_note']}")
    elif status == data.S_ULANG:
        st.info("Pekerja sudah mengirim perbaikan. Periksa versi terbaru, lalu konfirmasi atau kirim catatan perbaikan berikutnya.")

    if can_confirm or can_contact:
        reviewed = False
        if can_confirm:
            reviewed = st.checkbox("Saya sudah memeriksa laporan tahapan ini.", key=f"val_chk_{no}_{rec['updated_at']}")
        c1, c2 = st.columns(2)
        if can_confirm and c1.button("Konfirmasi Tahapan", type="primary", icon=":material/task_alt:", disabled=not reviewed, key=f"val_cf_{no}", width="stretch"):
            ok, msg = state.confirm_stage(cycle, no, actor, reviewed)
            if ok:
                nxt = next((n for n in data.STAGE_NOS if state.stage_status(cycle, n) in (data.S_MENUNGGU, data.S_ULANG)), None)
                if nxt:
                    ss["_val_pick"] = nxt
            ui.flash_message("success" if ok else "error", msg)
            st.rerun()
        if can_contact:
            c2.button("Hubungi Pekerja", icon=":material/support_agent:", key=f"val_ct_{no}", width="stretch", on_click=_open_contact, args=(no,))
        if can_confirm and not reviewed:
            st.caption("Centang pernyataan di atas untuk mengaktifkan Konfirmasi Tahapan.")
        if ss.get(f"val_contact_{no}") and can_contact:
            note = st.text_area("Catatan untuk Pekerja", key=f"val_note_{no}", placeholder="Jelaskan hal yang perlu diperiksa atau diperbaiki (wajib diisi)")
            if st.button("Kirim Catatan ke Pekerja", type="primary", icon=":material/send:", key=f"val_send_{no}"):
                ok, msg, _task = state.contact_worker(cycle, no, note, actor)
                if ok:
                    ss.pop(f"val_contact_{no}", None)
                    ui.flash_message("success", msg)
                    st.rerun()
                else:
                    st.error(msg)

# ------------------------------------------------------------ 2. Generate Report
st.subheader("2. Generate Report")
if rep:
    st.success(f"Laporan gabungan sudah dihasilkan pada {rep['generated_at']} dan tidak dibuat ganda.")
    st.markdown(f"Status laporan: {ui.badge(rep['status'])}", unsafe_allow_html=True)
    ui.go("views/spv_laporan.py", "Buka Laporan Gabungan", ":material/description:")
else:
    if g["ready"]:
        st.success(state.gate_headline(g))
    else:
        st.warning(state.gate_headline(g))
        for reason in state.gate_reasons(g):
            st.markdown(f"- {reason}")

    def _on_generated(ok, msg):
        if ok:
            ss["_goto"] = ("views/spv_laporan.py", ("success", msg + " Teruskan ke Manajemen dari halaman ini."))
        else:
            ui.flash_message("error", msg)

    ui.confirm_action(
        "Generate Report", "val_generate", "Generate Report",
        "Seluruh 18 tahapan sudah dikonfirmasi. Laporan gabungan akan dibuat satu kali untuk siklus ini dan tahapan terkunci. Lanjutkan?",
        lambda: state.generate_report(cycle, actor), icon=":material/summarize:", disabled=not g["ready"], on_done=_on_generated,
    )
    if not g["ready"]:
        st.caption("Tombol aktif setelah seluruh 18 tahapan dikonfirmasi SPV dan tidak ada tugas perbaikan yang terbuka.")
