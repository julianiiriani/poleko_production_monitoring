import streamlit as st

from core import data, state, ui

ui.page_header("Monitoring & Kelengkapan Produksi")

ss = st.session_state
cycle = state.active_cycle()
shift = ss.shift
actor = state.actor_name()
g = state.completeness(cycle)
st.progress(g["recorded"] / 18, text=f"{g['recorded']}/18 tahap sudah dicatat")

counts = state.status_counts(cycle)
selected = st.multiselect("Tampilkan status", data.RECORD_STATUS_ORDER, placeholder="Semua status", format_func=lambda s: f"{s} ({counts[s]})")

WIDTHS = [0.5, 2.2, 1.4, 0.9, 2.2, 1.6, 1.7]
head = st.columns(WIDTHS)
for c, h in zip(head, ["No", "Tahapan", "Pekerja", "Shift", "Status", "Risiko", "Tindakan"]):
    c.markdown(f"**{h}**")


def _open(no):
    ss["_val_pick"] = no
    st.switch_page("views/spv_validasi.py")


for no, name in data.STAGES:
    rec = state.get_record(cycle, no)
    status = rec["status"] if rec else data.S_BELUM
    if selected and status not in selected:
        continue
    other = rec is not None and rec["shift"] != shift
    c = st.columns(WIDTHS, vertical_alignment="center")
    c[0].write(f"{no:02d}")
    c[1].write(name)
    c[2].write(state.worker_name(state.worker_for_stage(no)))
    c[3].write(data.shift_name(rec["shift"]) if rec else "—")
    c[4].markdown(ui.badge("Shift lain" if other else status), unsafe_allow_html=True)
    c[5].markdown(ui.badge(rec["level"]) if rec and not other else "—", unsafe_allow_html=True)
    if other:
        c[6].button("Shift lain", key=f"mon_{no}", disabled=True, width="stretch")
    elif not rec:
        reminded = no in ss.get("reminders", {})
        if c[6].button("Sudah dihubungi" if reminded else "Hubungi Pekerja", key=f"mon_{no}", disabled=reminded,
                       type="primary", width="stretch"):
            ok, msg = state.remind_worker(cycle, no, actor)
            ui.flash_message("success" if ok else "error", msg)
            st.rerun()
    else:
        label = state.action_label(rec)
        if c[6].button(label, key=f"mon_{no}", width="stretch",
                       type="primary" if rec["status"] in (data.S_MENUNGGU, data.S_ULANG) else "secondary"):
            _open(no)
