import streamlit as st

from core import data, state, ui

ui.page_header("Penerusan ke General Manager", "Hanya Production Manager (Top) yang meneruskan laporan yang sudah dikonfirmasi.")


@st.dialog("Laporan Berhasil Diteruskan")
def _notice(n):
    st.success(f"{data.GM} telah menerima laporan.")
    ui.kv(
        [
            ("Nama laporan", n["report_id"]),
            ("Waktu penerimaan", n["at"]),
            ("Diteruskan oleh", n["by"]),
            ("Status", n["status"]),
        ]
    )
    st.caption("Notifikasi ini merupakan representasi penerimaan akhir pada demonstrasi, bukan integrasi pengiriman nyata ke sistem General Manager.")
    if st.button("Tutup", type="primary", width="stretch"):
        st.rerun()


notice = st.session_state.pop("_gm_notice", None)
if notice:
    _notice(notice)

cycle = ui.report_picker()
if not cycle:
    ui.empty_state("Belum ada laporan", "Laporan harus masuk ke Manajemen dan dikonfirmasi sebelum dapat diteruskan.")
    st.stop()

rep = state.get_report(cycle)
actor = state.actor_name()
ui.report_stepper(rep["status"])
ui.kv(
    [
        ("Laporan yang akan diteruskan", rep["report_id"]),
        ("Status pemeriksaan", ("badge", rep["status"])),
        ("Pemeriksa", rep["confirmed_by"] or "Belum diperiksa"),
        ("Tujuan", f"{data.GM} (penerima laporan)"),
    ]
)


def _after(ok, msg):
    if ok:
        r = state.get_report(cycle)
        st.session_state["_gm_notice"] = {"report_id": r["report_id"], "at": r["gm_received_at"], "by": r["forwarded_by"], "status": r["status"]}
    else:
        ui.flash_message("error", msg)


pending = state.red_pending(cycle)
if rep["status"] == data.R_KONFIRMASI and pending:
    st.button("Teruskan ke General Manager", disabled=True, icon=":material/forward_to_inbox:")
    st.warning("Data risiko tinggi (Merah) belum selesai ditanggapi: " + "; ".join(pending) + ".")
    ui.go("views/mgr_tindak_lanjut.py", "Buka Kendala Mesin", ":material/assignment_late:", type="secondary")
elif rep["status"] == data.R_KONFIRMASI:
    st.write(f"Penerusan akan dicatat atas nama **{actor}**. Tombol hanya dapat digunakan satu kali untuk satu laporan.")
    ui.confirm_action(
        "Teruskan ke General Manager", "gm_forward", "Teruskan ke General Manager",
        f"Laporan akan diteruskan ke {data.GM} atas nama {actor}. Tindakan ini hanya dapat dilakukan satu kali. Lanjutkan?",
        lambda: state.forward_to_gm(cycle, actor), icon=":material/forward_to_inbox:", on_done=_after,
    )
elif rep["status"] == data.R_GM:
    st.success(
        f"Laporan sudah diteruskan ke {data.GM} oleh {rep['forwarded_by']} pada {rep['forwarded_at']}. "
        f"Status: {rep['status']}. Penerusan tidak dapat dilakukan ulang oleh identitas mana pun."
    )
else:
    st.button("Teruskan ke General Manager", disabled=True, icon=":material/forward_to_inbox:")
    st.warning("Laporan harus diperiksa dan dikonfirmasi Production Manager lebih dulu sebelum dapat diteruskan.")
    ui.go("views/mgr_konfirmasi.py", "Buka Pemeriksaan dan Konfirmasi", ":material/task_alt:")
