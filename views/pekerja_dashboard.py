import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Pekerja", "Status laporan untuk tahapan yang menjadi tanggung jawab Anda.")

wid = st.session_state.worker_id
cycle = state.active_cycle()
no = state.worker_stage(wid)
short = data.stage_short(no)
rec = state.get_record(cycle, no)
open_task = next(iter(state.tasks_for(cycle, wid, [data.T_OPEN])), None)
all_tasks = state.tasks_for(cycle, wid)

task_state = "Tidak ada permintaan perbaikan"
if open_task:
    task_state = "Menunggu perbaikan dari Anda"
elif all_tasks and all_tasks[-1]["status"] == data.T_RESENT:
    task_state = "Perbaikan sudah dikirim, menunggu pemeriksaan ulang SPV"
elif all_tasks:
    task_state = "Perbaikan sudah ditinjau SPV"

ui.kv(
    [
        ("Pekerja", state.worker_name(wid)),
        ("Tahapan Anda", data.stage_label(no)),
        ("Status penginputan", ("badge", state.input_status(rec))),
        ("Status pemeriksaan SPV", ("badge", rec["status"] if rec else "—")),
        ("Status perbaikan", task_state),
    ]
)

st.subheader("Yang perlu Anda lakukan")
if not rec:
    st.info(f"Belum ada laporan yang dikirim untuk tahapan {short}.")
    ui.go("views/pekerja_input.py", "Buka Input Monitoring Produksi", ":material/edit_note:")
elif rec["status"] == data.S_KEMBALI:
    st.warning(f"SPV meminta pemeriksaan ulang pada tahapan {short}. Silakan periksa catatan perbaikan.")
    ui.go("views/pekerja_tugas.py", "Buka Tugas Pemeriksaan Kembali", ":material/assignment_return:")
elif rec["status"] == data.S_MENUNGGU:
    st.info(f"Input tahapan {short} telah dikirim kepada SPV dan sedang menunggu pemeriksaan.")
elif rec["status"] == data.S_ULANG:
    st.info(f"Perbaikan tahapan {short} telah dikirim kembali dan sedang menunggu pemeriksaan ulang SPV.")
else:
    st.success(f"Laporan tahapan {short} sudah dikonfirmasi SPV dan terkunci. Tidak ada tindakan lain.")

if rec:
    info = state.edit_info(rec)
    if info["can_edit"]:
        st.caption(f"Anda masih dapat mengedit laporan ini sampai {info['deadline']} (aturan prototipe {data.EDIT_WINDOW_HOURS} jam, selama belum dikonfirmasi SPV).")
        ui.go("views/pekerja_input.py", "Edit Laporan", ":material/edit:", type="secondary")
    elif not info.get("via_task"):
        st.caption(info["reason"])

if rec and rec.get("spv_note"):
    st.subheader("Catatan dari SPV")
    if rec["status"] == data.S_KEMBALI:
        st.warning(rec["spv_note"])
    else:
        st.caption("Catatan sebelumnya (sudah ditindaklanjuti):")
        st.write(rec["spv_note"])

st.subheader("Riwayat laporan Anda")
if not rec:
    ui.empty_state("Belum ada riwayat", "Riwayat muncul setelah Anda mengirim laporan tahapan.")
else:
    ui.table(
        pd.DataFrame([{"Versi": i, "Waktu": v["at"], "Keterangan": v["label"]} for i, v in enumerate(rec["versions"], 1)]),
    )
    ui.go("views/pekerja_riwayat.py", "Buka Riwayat Pencatatan", ":material/history:", type="secondary")
