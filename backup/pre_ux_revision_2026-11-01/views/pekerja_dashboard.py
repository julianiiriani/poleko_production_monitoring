import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Dashboard Pekerja", "Tahapan yang ditugaskan, status catatan Anda, dan tugas pemeriksaan kembali dari SPV.")

wid = st.session_state.worker_id
cycle = state.active_cycle()
stages = state.assigned_stages(wid)
sent = [n for n in stages if state.get_record(cycle, n)]
open_tasks = state.tasks_for(cycle, wid, [data.T_OPEN])

ui.stat_grid(
    [
        ("Tahapan ditugaskan (DEMO)", len(stages), data.ROLE_COLOR[data.ROLE_PEKERJA], ""),
        ("Sudah dikirim ke SPV", len(sent), data.STATUS_STYLE[data.S_TERKIRIM][0], f"/ {len(stages)}"),
        ("Belum dikirim", len(stages) - len(sent), data.STATUS_STYLE[data.S_BELUM][0], f"/ {len(stages)}"),
        ("Tugas pemeriksaan kembali", len(open_tasks), data.STATUS_STYLE[data.S_KEMBALI][0], "aktif"),
    ]
)
st.caption(f"Profil DEMO: {state.worker_name(wid)} · penugasan tahapan adalah konfigurasi demonstrasi, bukan penugasan resmi POLEKO.")

st.subheader(f"Tahapan Anda · {cycle}")
ui.stage_grid(cycle, only=set(stages))

if open_tasks:
    st.subheader("Perlu diperiksa kembali")
    for t in open_tasks:
        with st.container(border=True):
            st.markdown(f"**{data.stage_label(t['stage_no'])}** · {t['id']} · dibuat {t['created_at']}")
            st.warning(f"Catatan SPV: {t['note']}")
    st.page_link("views/pekerja_tugas.py", label="Buka Tugas Pemeriksaan Kembali", icon=":material/assignment_return:")

todo = [n for n in stages if not state.get_record(cycle, n)]
if todo and not state.get_report(cycle):
    st.page_link("views/pekerja_input.py", label=f"Input monitoring ({len(todo)} tahapan belum dikirim)", icon=":material/edit_note:")
elif not todo and not open_tasks:
    st.success("Seluruh tahapan Anda pada siklus ini sudah dikirim ke SPV.")

ui.demo_note()
ui.about_prototype()
