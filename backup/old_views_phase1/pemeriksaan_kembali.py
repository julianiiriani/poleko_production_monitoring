import streamlit as st

from core import data, state, ui

ui.page_header(
    "Pemeriksaan Kembali",
    "Laporan yang tidak sesuai dikembalikan kepada pihak yang menginput aktivitas produksi untuk diperiksa ulang.",
    data.PAGE_ACTORS["kembali"],
)

cycle = state.active_cycle()
if not ui.cycle_required(cycle):
    st.stop()

returned = state.records_with(cycle, (data.S_KEMBALI,))
if not returned:
    ui.empty_state(
        "Tidak ada laporan yang dikembalikan",
        "Laporan akan muncul di sini setelah dikembalikan dari halaman Pemeriksaan dan Validasi Laporan.",
    )
    ui.demo_notice()
    st.stop()

options = {f"{r['stage_no']:02d}. {data.STAGE_NAMES[r['stage_no']]}": r for r in returned}
rec = options[st.selectbox("Laporan yang perlu diperiksa kembali", list(options))]
no = rec["stage_no"]
orig = rec["original"]
ver = len(rec["events"])

st.markdown(
    f"**Dikembalikan kepada:** {ui.esc(rec['spv'])} (pihak yang menginput) &nbsp; {ui.badge(rec['status'])}",
    unsafe_allow_html=True,
)
st.error(f"Alasan pemeriksaan kembali: {rec['return_reason']}")

left, right = st.columns(2)
with left:
    st.markdown("##### Informasi awal yang dikirim")
    with st.container(border=True):
        st.write(f"Nilai (placeholder): {ui.esc(state.value_text(orig))}")
        st.write(f"Hasil monitoring (usulan): **{orig['result']}**")
        st.write(f"Waktu aktivitas: {state.time_text(orig)}")
        st.write(f"Catatan: {ui.esc(orig['notes'])}")
with right:
    st.markdown("##### Informasi yang diperbarui")
    qty = st.text_input("Nilai / kuantitas (placeholder)", value=rec["qty"], key=f"rk_qty_{cycle}_{no}_{ver}")
    result = st.radio(
        "Hasil monitoring (usulan)",
        data.HASIL_OPTIONS,
        index=data.HASIL_OPTIONS.index(rec["result"]),
        horizontal=True,
        key=f"rk_res_{cycle}_{no}_{ver}",
    )
    notes = st.text_area("Catatan / klarifikasi", value=rec["notes"], key=f"rk_note_{cycle}_{no}_{ver}")

st.caption(f"{data.DEMO_VALIDATION_LABEL}: kolom wajib di bawah hanya aturan interaksi prototipe.")
if st.button("Kirim ulang untuk pemeriksaan", type="primary", icon=":material/send:"):
    if not qty.strip():
        st.error("Nilai / kuantitas wajib diisi.")
    elif result != "Sesuai" and not notes.strip():
        st.error("Catatan wajib diisi bila hasil monitoring bukan 'Sesuai'.")
    else:
        state.resubmit(rec, qty=qty.strip(), result=result, notes=notes.strip())
        st.rerun()
st.caption("Tidak ada jejak audit permanen atau pembaruan database pada Fase 1; riwayat hanya di sesi ini.")
ui.demo_notice()
