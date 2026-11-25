import streamlit as st

from core import data, state, ui

ui.page_header("Pemeriksaan dan Konfirmasi", "Periksa laporan gabungan, lalu terima atau kembalikan ke Supervisor.")

cycle = ui.report_picker()
if not cycle:
    ui.empty_state("Belum ada laporan untuk diperiksa", "Pemeriksaan tersedia setelah Supervisor meneruskan laporan gabungan ke Manajemen.")
    st.stop()

rep = state.get_report(cycle)
actor = state.actor_name()
ui.report_stepper(rep["status"])
ui.report_preview(rep)

st.subheader("Pemeriksaan dan keputusan")
if rep["status"] in (data.R_MASUK, data.R_ULANG):
    if rep["status"] == data.R_ULANG and rep["returns"]:
        last = rep["returns"][-1]
        st.info(f"Laporan dikirim kembali oleh Supervisor. Catatan Anda ({last['by']}): {last['note']}\n\nTanggapan Supervisor: {last.get('response') or '—'}")
    st.write(f"Pemeriksaan dicatat atas nama **{actor}**.")
    ver = len(rep["versions"])
    checked = st.checkbox("Saya sudah memeriksa laporan gabungan ini.", key=f"cf_check_{cycle}_{ver}")
    decision = st.radio(
        "Keputusan",
        [data.D_DITERIMA, data.D_PERBAIKAN],
        index=None,
        key=f"cf_dec_{cycle}_{ver}",
        captions=["Laporan benar dan lengkap. Konfirmasi laporan.", "Kembalikan ke Supervisor beserta catatan perbaikan."],
    )
    if decision == data.D_DITERIMA:
        ui.confirm_action(
            "Konfirmasi Laporan", "cf_confirm", "Konfirmasi Laporan",
            f"Laporan akan dikonfirmasi atas nama {actor}. Tindakan ini hanya dapat dilakukan satu kali. Lanjutkan?",
            lambda: state.confirm_report(cycle, actor, checked), icon=":material/task_alt:", disabled=not checked,
        )
        if not checked:
            st.caption("Centang pernyataan di atas untuk mengaktifkan tombol Konfirmasi Laporan.")
    elif decision == data.D_PERBAIKAN:
        note = st.text_area("Catatan Perbaikan untuk Supervisor", key=f"cf_note_{cycle}_{ver}", placeholder="Jelaskan alasan dan bagian yang perlu diperbaiki (wajib diisi)")
        ui.confirm_action(
            "Kirim Catatan Perbaikan ke Supervisor", "cf_return", "Kembalikan ke Supervisor",
            f"Laporan akan dikembalikan kepada Supervisor atas nama {actor} beserta catatan perbaikan. Laporan dan data awal tidak dihapus. Lanjutkan?",
            lambda: state.return_report(cycle, actor, note), icon=":material/undo:", disabled=not (checked and note.strip()),
        )
        if not checked:
            st.caption("Centang pernyataan pemeriksaan di atas agar tombol aktif.")
elif rep["status"] == data.R_PERBAIKAN:
    ret = rep["returns"][-1]
    st.warning(f"Laporan dikembalikan ke Supervisor oleh {ret['by']} pada {ret['at']}. Catatan: {ret['note']}. Menunggu Supervisor mengirim kembali.")
else:
    st.success(f"Laporan diperiksa dan dikonfirmasi oleh {rep['confirmed_by']} pada {rep['confirmed_at']}. Tindakan konfirmasi sudah terkunci.")
    if rep["status"] == data.R_KONFIRMASI:
        ui.go("views/mgr_gm.py", f"Lanjut ke Penerusan ke {data.GM}", ":material/forward_to_inbox:")
