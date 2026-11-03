import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Kelengkapan Pencatatan", "Syarat TRUE: 18 tahapan tercatat dan tidak ada tugas pemeriksaan kembali yang belum selesai ditinjau.")

cycle = state.active_cycle()
gate = state.completeness(cycle)
st.progress(gate["recorded"] / 18, text=f"{gate['recorded']} dari 18 tahapan tercatat")

if gate["ready"]:
    st.success("Syarat kelengkapan terpenuhi untuk siklus ini.")
else:
    st.warning("Syarat kelengkapan belum terpenuhi, sehingga keputusan TRUE diblokir.")

left, right = st.columns(2)
with left:
    st.subheader(f"Belum dicatat ({len(gate['missing'])})")
    if gate["missing"]:
        ui.table(
            pd.DataFrame(
                [{"Tahapan": data.stage_label(n), "Pekerja ditugaskan (DEMO)": state.worker_name(state.worker_for_stage(n))} for n in gate["missing"]]
            )
        )
    else:
        st.caption("Semua tahapan sudah tercatat.")
with right:
    st.subheader(f"Dalam pemeriksaan kembali ({len(gate['rechecking']) + len(gate['awaiting_review'])})")
    tasks = state.tasks_for(cycle, statuses=[data.T_OPEN, data.T_RESENT])
    if tasks:
        ui.table(
            pd.DataFrame(
                [{"Tahapan": data.stage_label(t["stage_no"]), "Pekerja": state.worker_name(t["worker_id"]), "Status": t["status"]} for t in tasks]
            ),
            badge_cols=("Status",),
        )
        if gate["awaiting_review"]:
            st.page_link("views/spv_penugasan.py", label="Tinjau kiriman ulang", icon=":material/assignment_return:")
    else:
        st.caption("Tidak ada tugas pemeriksaan kembali yang belum selesai.")

st.subheader("Peta 18 tahapan")
ui.stage_grid(cycle)
ui.demo_note()
