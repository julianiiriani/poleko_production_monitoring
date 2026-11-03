import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Pekerja", "Tahapan Anda dan tugas dari SPV.", cycle=True)

wid = st.session_state.worker_id
cycle = state.active_cycle()
stages = state.assigned_stages(wid)
sent = [n for n in stages if state.get_record(cycle, n)]
todo = [n for n in stages if not state.get_record(cycle, n)]
open_tasks = state.tasks_for(cycle, wid, [data.T_OPEN])

st.subheader("Yang perlu Anda lakukan")
if open_tasks:
    for t in open_tasks:
        with st.container(border=True):
            st.markdown(f"**{data.stage_label(t['stage_no'])}** · {t['id']}")
            st.warning(f"Catatan SPV: {t['note']}")
    ui.go("views/pekerja_tugas.py", "Periksa dan kirim ulang", ":material/assignment_return:")
if todo and state.get_report(cycle):
    st.info("Siklus ini sudah memiliki laporan gabungan, sehingga catatan baru tidak dapat ditambahkan.")
elif todo:
    st.info(f"{len(todo)} tahapan Anda belum dicatat: " + ", ".join(f"{n:02d}" for n in todo) + ".")
    ui.go("views/pekerja_input.py", "Buka Input Monitoring Produksi", ":material/edit_note:")
elif not open_tasks:
    st.success("Semua tahapan Anda pada siklus ini sudah dikirim ke SPV. Tidak ada tugas lain.")

if len(stages) > 1:  # satu tahapan: status sudah terlihat pada kartu tahapan di bawah, ringkasan hitungan tidak diperlukan
    ui.stat_grid(
        [
            ("Tahapan Anda", len(stages), data.ROLE_COLOR[data.ROLE_PEKERJA], ""),
            ("Sudah dikirim ke SPV", len(sent), data.STATUS_STYLE[data.S_TERKIRIM][0], f"/ {len(stages)}"),
            ("Belum dicatat", len(todo), data.STATUS_STYLE[data.S_BELUM][0], f"/ {len(stages)}"),
            ("Perlu perbaikan", len(open_tasks), data.STATUS_STYLE[data.S_KEMBALI][0], ""),
        ]
    )

st.subheader("Status tahapan Anda")
ui.stage_grid(cycle, only=set(stages))
