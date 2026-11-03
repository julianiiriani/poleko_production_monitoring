import streamlit as st

from core import data, state, ui

ui.page_header(
    "Pemeriksaan dan Validasi Laporan",
    "Memeriksa laporan tahapan; bila sesuai diteruskan ke PPIC, bila tidak sesuai dikembalikan ke pihak yang menginput.",
    data.PAGE_ACTORS["validasi"],
)

cycle = state.active_cycle()
if not ui.cycle_required(cycle):
    st.stop()

df = state.overview_df(cycle)
recorded = int((df["Status"] != data.S_BELUM).sum())
queue = state.review_queue(cycle)
queue_total, queue_new, queue_resent = state.queue_breakdown(cycle)
returned = len(state.records_with(cycle, (data.S_KEMBALI,)))

st.subheader(f"Siklus {cycle} · DEMO")
a, b, c = st.columns(3)
a.metric("Kelengkapan laporan", f"{recorded} / 18 tahapan")
b.metric(data.QUEUE_LABEL, queue_total, help=f"{queue_new} Sudah Dicatat + {queue_resent} Menunggu Pemeriksaan (dikirim ulang)")
c.metric("Perlu pemeriksaan kembali", returned)
st.progress(recorded / 18)

with st.expander("Konsolidasi catatan 18 tahapan", expanded=False):
    st.dataframe(
        df[["No", "Tahapan", "Status", "SPV Pencatat", "Hasil (usulan)", "Diperbarui"]],
        hide_index=True,
        width="stretch",
    )

st.subheader(data.QUEUE_LABEL)
if not queue:
    ui.empty_state(
        "Tidak ada laporan dalam antrean pemeriksaan",
        "Laporan tahapan yang baru dicatat atau dikirim ulang akan muncul di sini.",
    )
    ui.demo_notice()
    st.stop()

options = {f"{r['stage_no']:02d}. {data.STAGE_NAMES[r['stage_no']]} — {r['status']}": r for r in queue}
rec = options[st.selectbox("Pilih laporan tahapan", list(options))]
no = rec["stage_no"]

with st.container(border=True):
    st.markdown(f"**{no:02d}. {data.STAGE_NAMES[no]}** &nbsp; {ui.badge(rec['status'])}", unsafe_allow_html=True)
    ui.record_details(rec)
    if rec["reason_history"]:
        st.caption(f"Dikirim ulang setelah alasan sebelumnya: {rec['reason_history'][-1]}")

reason = st.text_area(
    "Alasan ketidaksesuaian (wajib bila dikembalikan)",
    key=f"val_reason_{cycle}_{no}_{len(rec['events'])}",
    placeholder="Jelaskan data yang perlu diperiksa kembali oleh pihak yang menginput",
)
st.caption(f"{data.DEMO_VALIDATION_LABEL}: kewajiban mengisi alasan hanya aturan interaksi prototipe.")
ok_col, back_col = st.columns(2)
if ok_col.button("Laporan sesuai — teruskan ke PPIC", type="primary", width="stretch", icon=":material/forward:"):
    state.set_status(rec, data.S_KONFIRMASI, "Dinyatakan sesuai dan diteruskan ke PPIC (DEMO)")
    st.rerun()
if back_col.button("Tidak sesuai — kembalikan ke pihak yang menginput", width="stretch", icon=":material/undo:"):
    if not reason.strip():
        st.error("Alasan wajib diisi untuk mengembalikan laporan.")
    else:
        state.return_for_recheck(rec, reason.strip())
        st.rerun()
ui.demo_notice()
