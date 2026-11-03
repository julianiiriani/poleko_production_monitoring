import streamlit as st

from core import data, state, ui

ui.page_header(
    "Monitoring Aktivitas Produksi",
    "Tampilan informasi dari Data Aktivitas Proses Produksi untuk pemantauan (representasi konsep real-time).",
    data.PAGE_ACTORS["monitoring"],
)

ui.flow(
    [
        ("Input laporan monitoring per tahapan", data.ROLE_SPV, False),
        ("Data Aktivitas Proses Produksi (visual, belum terhubung)", "Data store", True),
        ("Memantau pencatatan dan aktivitas produksi", data.ROLE_MANAJER, False),
    ]
)
st.caption(
    "Konsep: laporan tahapan disimpan terpusat, dapat diambil kembali oleh pihak berwenang, dan mendukung pemeriksaan laporan. "
    + data.REALTIME_NOTE
)

cycle = state.active_cycle()
if not ui.cycle_required(cycle):
    st.write("")
    ui.stage_grid(None)
    ui.demo_notice()
    st.stop()

st.subheader(f"Siklus {cycle} · DEMO")
df = state.overview_df(cycle)
recorded = int((df["Status"] != data.S_BELUM).sum())
m1, m2 = st.columns(2)
m1.metric("Tahapan tercatat", f"{recorded} / 18")
m2.metric("Kelengkapan pencatatan", f"{recorded / 18:.0%}")
st.progress(recorded / 18)

selected = st.multiselect("Filter status", data.STATUS_ORDER, placeholder="Semua status")
view = df[df["Status"].isin(selected)] if selected else df
st.dataframe(
    view,
    hide_index=True,
    width="stretch",
    height=min(740, 38 + 35 * len(view)),
    column_config={
        "No": st.column_config.NumberColumn("No", width=40),
        "Tahapan": st.column_config.TextColumn("Tahapan", width=285),
        "Status": st.column_config.TextColumn("Status", width=160),
        "SPV Pencatat": st.column_config.TextColumn("SPV Pencatat", width=95),
        "Waktu Aktivitas": st.column_config.TextColumn("Waktu Aktivitas", width=115),
        "Hasil (usulan)": st.column_config.TextColumn("Hasil (usulan)", width=150),
        "Diperbarui": st.column_config.TextColumn("Diperbarui", width=85),
    },
)
st.caption("Seluruh baris pada tabel ini adalah data DEMO. Rincian lengkap setiap tahapan ada di bagian Detail Tahapan.")

st.subheader("Detail Tahapan")
label = st.selectbox("Pilih tahapan", data.STAGE_LABELS, key="mon_stage")
no = state.stage_no_from_label(label)
rec = state.get_record(cycle, no)
if not rec:
    ui.empty_state("Belum Dicatat", "SPV Produksi belum mengirim laporan untuk tahapan ini pada siklus terpilih.")
else:
    left, right = st.columns([2, 1])
    with left:
        st.markdown(
            f"**{no:02d}. {data.STAGE_NAMES[no]}** &nbsp; {ui.badge(rec['status'])} &nbsp; *DEMO*",
            unsafe_allow_html=True,
        )
        ui.record_details(rec)
        # Alasan aktif hanya ada saat status benar-benar Perlu Pemeriksaan Kembali.
        if rec["status"] == data.S_KEMBALI and rec["return_reason"]:
            st.warning(f"Alasan pemeriksaan kembali: {rec['return_reason']}")
    with right:
        st.caption("Riwayat sesi (DEMO)")
        for event in rec["events"]:
            st.caption(f"• {event}")
ui.demo_notice()
