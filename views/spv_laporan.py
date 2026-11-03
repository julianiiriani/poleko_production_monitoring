import pandas as pd
import streamlit as st

from core import data, state, ui

ui.page_header("Laporan Gabungan", "Laporan hasil penggabungan 18 tahapan yang sudah dikonfirmasi SPV.")

cycle = state.active_cycle()
rep = state.get_report(cycle)
actor = state.actor_name()

if not rep:
    g = state.completeness(cycle)
    ui.empty_state("Belum ada laporan gabungan", "Laporan dibuat lewat Generate Report di Validasi Laporan setelah 18 tahapan terkonfirmasi.")
    st.info(state.gate_headline(g))
    ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:")
    st.stop()

ui.kv(
    [
        ("ID Laporan", rep["report_id"]),
        ("Identitas siklus (internal)", rep["cycle"]),
        ("Tanggal produksi", rep["production_date"]),
        ("Status", ("badge", rep["status"])),
    ]
)
ui.report_stepper(rep["status"])

st.subheader("Tindakan")
if rep["status"] == data.R_GENERATED:
    st.info("Laporan gabungan sudah dihasilkan. Teruskan ke Manajemen agar dapat diperiksa dan dikonfirmasi.")
    ui.confirm_action(
        "Teruskan ke Manajemen", "lap_forward", "Teruskan ke Manajemen",
        "Laporan gabungan akan diteruskan ke Manajemen. Tindakan ini hanya dapat dilakukan satu kali. Lanjutkan?",
        lambda: state.handoff_to_management(cycle, actor), icon=":material/forward:",
    )
elif rep["status"] == data.R_PERBAIKAN:
    ret = rep["returns"][-1]
    st.warning(f"Laporan dikembalikan oleh **{ret['by']}** pada {ret['at']}.\n\nCatatan perbaikan: {ret['note']}")
    g = state.completeness(cycle)
    if not g["ready"]:
        st.info(state.gate_headline(g))
        for reason in state.gate_reasons(g):
            st.markdown(f"- {reason}")
        ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:")
    else:
        st.write("Tahapan yang perlu diperbaiki dapat dibuka kembali lewat Validasi Laporan (Hubungi Pekerja). Bila sudah selesai, kirim laporan kembali.")
        response = st.text_area("Tanggapan SPV", key=f"lap_resp_{len(rep['versions'])}", placeholder="Jelaskan perbaikan atau pemeriksaan ulang yang Anda lakukan (wajib diisi)")
        ui.confirm_action(
            "Kirim Ulang ke Manajemen", "lap_resend", "Kirim Ulang ke Manajemen",
            "Laporan gabungan versi terbaru akan dikirim kembali ke Manajemen untuk diperiksa ulang. Versi sebelumnya tetap tersimpan. Lanjutkan?",
            lambda: state.resend_report(cycle, response, actor), icon=":material/forward:", disabled=not response.strip(),
        )
        ui.go("views/spv_validasi.py", "Buka Validasi Laporan", ":material/fact_check:", type="secondary")
else:
    st.success(
        f"Laporan sudah diteruskan ke Manajemen pada {rep['handoff_at']} oleh {rep['handoff_by']}. "
        f"Status saat ini: {rep['status']}. Tindakan penerusan tidak dapat dilakukan ulang."
    )

ui.report_preview(rep)

st.subheader("Riwayat versi laporan")
ui.table(
    pd.DataFrame(
        [{"Versi": v["no"], "Jenis": v["kind"], "Waktu": v["at"], "Oleh": v["by"], "Tanggapan SPV": v["note"] or "—"} for v in rep["versions"]]
    )
)
if rep["returns"]:
    st.subheader("Catatan dari Manajemen")
    ui.table(
        pd.DataFrame(
            [
                {"Waktu": r["at"], "Dari": r["by"], "Catatan": r["note"], "Tanggapan SPV": r.get("response") or "Belum ditanggapi"}
                for r in rep["returns"]
            ]
        )
    )
