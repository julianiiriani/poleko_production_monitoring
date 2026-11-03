import streamlit as st

from core import data, state, ui

ui.page_header(
    "Konfirmasi Laporan",
    "Laporan yang diteruskan ke PPIC diperiksa kembali dan dikonfirmasi.",
    data.PAGE_ACTORS["konfirmasi"],
)

cycle = state.active_cycle()
if not ui.cycle_required(cycle):
    st.stop()

counts = state.status_counts(cycle)
pending = state.records_with(cycle, (data.S_KONFIRMASI,))
done = counts[data.S_SELESAI]
not_forwarded = state.not_yet_forwarded(cycle)

st.subheader(f"Siklus {cycle} · DEMO")
ui.flow(
    [
        ("Validasi laporan", data.ROLE_SPV, False),
        ("Meneruskan ke PPIC", data.ROLE_SPV, False),
        ("Memeriksa kembali dan melakukan konfirmasi laporan", data.ROLE_MANAJER, False),
    ]
)
st.write("")
a, b, c = st.columns(3)
a.metric("Menunggu konfirmasi", len(pending))
b.metric("Sudah dikonfirmasi", f"{done} / 18")
c.metric(
    "Belum diteruskan ke PPIC",
    not_forwarded,
    help=f"Belum Dicatat + {data.QUEUE_LABEL} ({data.QUEUE_DEFINITION}) + Perlu Pemeriksaan Kembali",
)
st.progress(done / 18)

if done == 18:
    st.success("Seluruh 18 tahapan telah dikonfirmasi — laporan siklus ini berstatus Terkonfirmasi (DEMO).")
elif done:
    st.info("Konfirmasi baru sebagian. Laporan siklus lengkap bila seluruh 18 tahapan terkonfirmasi.")

st.subheader("Ringkasan Laporan")
df = state.overview_df(cycle)
st.dataframe(
    df[["No", "Tahapan", "Status", "Hasil (usulan)", "SPV Pencatat", "Diperbarui"]],
    hide_index=True,
    width="stretch",
)

st.subheader("Konfirmasi")
if not pending:
    ui.empty_state("Tidak ada laporan menunggu konfirmasi", "Laporan yang dinyatakan sesuai pada halaman validasi akan muncul di sini.")
else:
    labels = {f"{r['stage_no']:02d}. {data.STAGE_NAMES[r['stage_no']]}": r for r in pending}
    chosen = st.multiselect("Pilih laporan tahapan untuk dikonfirmasi", list(labels), default=list(labels))
    if st.button("Konfirmasi laporan terpilih (DEMO)", type="primary", disabled=not chosen, icon=":material/task_alt:"):
        for name in chosen:
            state.set_status(labels[name], data.S_SELESAI, "Dikonfirmasi (DEMO)")
        st.rerun()
ui.demo_notice()
