import pandas as pd
import streamlit as st

from core import data, state, ui

wid = st.session_state.worker_id
cycle = state.active_cycle()
no = state.worker_stage(wid)
rec = state.get_record(cycle, no)
open_task = next(iter(state.tasks_for(cycle, wid, [data.T_OPEN])), None)

ui.page_header("Dashboard Pekerja", data.stage_label(no))
ui.kv([("Status", ("badge", rec["status"] if rec else data.S_BELUM)), ("Dikirim", rec["sent_at"] if rec else "—")])

reminder = st.session_state.get("reminders", {}).get(no)
if not rec:
    if reminder:
        st.warning(f"{reminder['by']} meminta Anda segera mengisi laporan.")
    ui.go("views/pekerja_input.py", "Isi Laporan", ":material/edit_note:")
elif open_task or rec["status"] == data.S_KEMBALI:
    st.warning(f"Perlu perbaikan: {rec['spv_note']}")
    ui.go("views/pekerja_tugas.py", "Perbaiki Laporan", ":material/assignment_return:")
elif rec["status"] == data.S_KONFIRMASI:
    st.success("Laporan sudah dikonfirmasi Supervisor.")
elif state.edit_info(rec)["can_edit"]:
    ui.go("views/pekerja_input.py", "Edit Laporan", ":material/edit:", type="secondary")

if rec:
    st.subheader("Riwayat")
    ui.table(pd.DataFrame([{"Versi": i, "Waktu": v["at"], "Keterangan": v["label"]} for i, v in enumerate(rec["versions"], 1)]))
