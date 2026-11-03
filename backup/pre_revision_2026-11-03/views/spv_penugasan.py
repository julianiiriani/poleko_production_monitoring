import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Penugasan Pemeriksaan Kembali", "Tugas perbaikan untuk Pekerja dan tanggapan mereka.", cycle=True)

cycle = state.active_cycle()
tasks = state.tasks_for(cycle)

if not tasks:
    ui.empty_state("Belum ada tugas", "Tugas dibuat dari Validasi Laporan saat SPV memilih Perlu Perbaikan.")
    ui.go("views/spv_validasi.py", "Validasi Laporan", ":material/fact_check:")
    st.stop()

ui.table(
    pd.DataFrame(
        [
            {
                "ID": t["id"],
                "Tahapan": data.stage_label(t["stage_no"]),
                "Pekerja": state.worker_name(t["worker_id"]),
                "Status": t["status"],
                "Catatan perbaikan": t["note"],
                "Dibuat": t["created_at"],
                "Dikirim ulang": t["resubmitted_at"] or "Belum",
            }
            for t in tasks
        ]
    ),
    badge_cols=("Status",),
    max_height=480,
)

by_id = {t["id"]: t for t in tasks}
task_id = st.selectbox("Tinjau tugas", list(by_id), format_func=lambda i: f"{i} · Tahap {by_id[i]['stage_no']:02d} · {by_id[i]['status']}")
task = by_id[task_id]
st.markdown(f"**{data.stage_label(task['stage_no'])}** · {state.worker_name(task['worker_id'])} &nbsp; {ui.badge(task['status'])}", unsafe_allow_html=True)

if task["status"] == data.T_OPEN:
    st.info("Menunggu Pekerja memeriksa dan mengirim ulang. Catatan perbaikan Anda:")
    st.warning(task["note"])
else:
    st.caption(f"Catatan perbaikan: {task['note']}")
    a, b = st.columns(2)
    with a:
        st.markdown("**Versi sebelumnya**")
        ui.fields_block(task["original"])
    with b:
        st.markdown("**Tanggapan Pekerja**")
        ui.fields_block(task["response"])
    if task["status"] == data.T_RESENT:
        if st.button("Terima Hasil Perbaikan", type="primary", icon=":material/done_all:"):
            ok, msg = state.accept_resubmission(task_id)
            st.session_state["_flash"] = ("success" if ok else "info", msg)
            st.rerun()
        st.caption("Bila masih belum sesuai, pilih Perlu Perbaikan lagi di Validasi Laporan.")
    else:
        st.success(f"Ditinjau pada {task['reviewed_at']}.")
