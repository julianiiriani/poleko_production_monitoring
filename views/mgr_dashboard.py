"""Dashboard manajemen yang berbeda untuk setiap tingkatan (Aturan Main bagian 6).

Top    : Production Manager — ringkasan semua shift, data Merah kendala mesin, laporan siap dikonfirmasi/diteruskan.
Middle : PPIC — data Kuning (waktu dan kg), durasi aktual terhadap standar, total kg terhadap 10 ton.
Middle : QA — temuan mutu dari QC yang menunggu keputusan, riwayat keputusan, gambar bukti.
Lower  : QC — status Tahap 8, 12, 18 per shift dan temuan yang perlu dicatat.
"""
import pandas as pd
import streamlit as st

from core import data, state, ui

who = state.identity()
cycle = state.active_cycle()
color = data.STATUS_STYLE
records = state.cycle_records(cycle)
lv = state.level_counts(cycle)


def _fu_rows(items, with_images=False):
    rows = []
    for rec, fu in items:
        rows.append(
            {
                "Tahap": data.stage_label(rec["stage_no"]),
                "Shift": data.shift_name(rec["shift"]),
                "Tingkat Risiko": rec["level"],
                "Keterangan": "; ".join(i["text"] for i in rec.get("issues", [])) or (rec["data"].get("kendala") or "—"),
                "Status": fu["status"],
                "Dicatat oleh": f"{fu['by']} · {fu['done_at']}" if fu["by"] else "—",
                **({"Gambar": len(fu["images"])} if with_images else {}),
            }
        )
    return pd.DataFrame(rows)


def _reports_block():
    visible = sorted(state.reports_visible_to_management(), key=lambda r: r["cycle"])
    st.subheader("Laporan gabungan")
    if not visible:
        ui.empty_state("Belum ada laporan masuk", "Laporan muncul setelah Supervisor meneruskan laporan gabungan ke Manajemen.")
        return visible
    ui.table(
        pd.DataFrame(
            [{"Laporan": r["report_id"], "Status": r["status"], "Diterima dari": f"{r['handoff_by']} · {r['handoff_at']}"} for r in visible]
        ),
        badge_cols=("Status",),
    )
    return visible


if who == data.PM:
    ui.page_header("Dashboard Production Manager", "Semua shift")
    mesin = state.followups_for(data.PM, cycle)
    pending = state.red_pending(cycle)
    ui.stat_grid(
        [
            ("Tahapan tercatat (semua shift)", len(records), data.ROLE_COLOR[data.ROLE_MANAJER], "/ 18"),
            (data.LV_HIJAU, lv[data.LV_HIJAU], color[data.LV_HIJAU][0], ""),
            (data.LV_KUNING, lv[data.LV_KUNING], color[data.LV_KUNING][0], ""),
            (data.LV_MERAH, lv[data.LV_MERAH], color[data.LV_MERAH][0], ""),
            ("Kendala mesin menunggu Anda", sum(fu["status"] == data.F_MENUNGGU for _, fu in mesin), color[data.F_MENUNGGU][0], ""),
        ],
        min_width=180,
    )
    st.subheader("Per shift")
    ui.table(
        pd.DataFrame(
            [
                {
                    "Shift": data.shift_label(n),
                    "Supervisor": data.SHIFTS[n][3],
                    "Tahap tercatat": sum(r["shift"] == n for r in records),
                    "Dikonfirmasi Supervisor": sum(r["shift"] == n and r["status"] == data.S_KONFIRMASI for r in records),
                    "Kuning": state.level_counts(cycle, n)[data.LV_KUNING],
                    "Merah": state.level_counts(cycle, n)[data.LV_MERAH],
                }
                for n in data.SHIFT_NOS
            ]
        )
    )
    st.subheader("Langkah berikutnya")
    if any(fu["status"] == data.F_MENUNGGU for _, fu in mesin):
        st.warning("Ada data kendala mesin yang menunggu tanggapan Anda.")
        ui.go("views/mgr_tindak_lanjut.py", "Buka Kendala Mesin", ":material/assignment_late:")
    if pending:
        st.info("Data Merah yang belum selesai (menahan penerusan ke General Manager): " + "; ".join(pending) + ".")
    visible = _reports_block()
    waiting = [r for r in visible if r["status"] in (data.R_MASUK, data.R_ULANG)]
    confirmed = [r for r in visible if r["status"] == data.R_KONFIRMASI]
    if waiting:
        ui.go("views/mgr_konfirmasi.py", "Periksa dan Konfirmasi Laporan", ":material/task_alt:")
    if confirmed:
        ui.go("views/mgr_gm.py", f"Teruskan ke {data.GM}", ":material/forward_to_inbox:")

    st.subheader("Semua tindak lanjut (PPIC, QC, QA, Production Manager)")
    names = {data.RT_PPIC: "PPIC", data.RT_PM: "Production Manager", data.RT_QC: "QC", data.RT_QA: "QA"}
    rows = []
    for r in records:
        for key, fu in r.get("followups", {}).items():
            rows.append({
                "Tahap": data.stage_label(r["stage_no"]),
                "Shift": data.shift_name(r["shift"]),
                "Tingkat Risiko": r["level"],
                "Pihak": names.get(key, key),
                "Status": fu["status"],
                "Catatan": (fu.get("note") or "—") + (f" ({fu['decision']})" if fu.get("decision") else ""),
                "Gambar": len(fu.get("images") or []),
            })
    if rows:
        ui.table(pd.DataFrame(rows), badge_cols=("Tingkat Risiko", "Status"))
        for r in records:
            for key in (data.RT_QC, data.RT_QA):
                fu = r.get("followups", {}).get(key)
                if fu and fu.get("images"):
                    with st.expander(f"Gambar {names[key]} — {data.stage_label(r['stage_no'])}"):
                        ui.images_block(fu["images"])
    else:
        ui.empty_state("Belum ada tindak lanjut", "Muncul setelah Supervisor mengonfirmasi data Kuning atau Merah.")
    st.subheader("Data 18 tahap")
    ui.overview_table(state.overview_df(cycle, actions=False))

elif who == data.PPIC:
    ui.page_header("Dashboard PPIC", )
    kuning = state.followups_for(data.PPIC, cycle)
    total_kg = sum(r["data"].get("jumlah_kg") or 0 for r in records if r["stage_no"] == data.OPENING_STAGE)
    ui.stat_grid(
        [
            ("Data di luar batas (Kuning)", len(kuning), color[data.LV_KUNING][0], ""),
            ("Menunggu tanggapan Anda", sum(fu["status"] == data.F_MENUNGGU for _, fu in kuning), color[data.F_MENUNGGU][0], ""),
            ("Bahan diterima (Tahap 01)", f"{total_kg:,.0f}".replace(",", "."), data.ROLE_COLOR[data.ROLE_MANAJER], "kg"),
        ],
        min_width=200,
    )
    st.subheader("Durasi aktual terhadap durasi standar")
    rows = []
    for r in records:
        a, b, dur, _ = data.STAGE_STANDARD[r["stage_no"]]
        act = state.duration_minutes(r["data"])
        rows.append(
            {
                "Tahap": data.stage_label(r["stage_no"]),
                "Shift": data.shift_name(r["shift"]),
                "Standar": ui.standard_text(r["stage_no"]),
                "Aktual": state.duration_text(r["data"]),
                "Selisih (menit)": (act - dur) if (act is not None and dur) else 0,
                "Jumlah (kg)": state.kg_text(r["data"]),
                "Tingkat Risiko": r["level"],
            }
        )
    if rows:
        ui.table(pd.DataFrame(rows), badge_cols=("Tingkat Risiko",))
    else:
        ui.empty_state("Belum ada data", "Data muncul setelah pekerja mengirim laporan tahapan.")
    st.subheader("Data di luar batas yang diarahkan ke PPIC")
    if kuning:
        ui.table(_fu_rows(kuning), badge_cols=("Tingkat Risiko", "Status"))
        ui.go("views/mgr_tindak_lanjut.py", "Buka Data di Luar Batas", ":material/assignment_late:")
    else:
        ui.empty_state("Tidak ada data Kuning", "Data muncul setelah Supervisor memeriksa input yang berada di luar batas formulir.")
    _reports_block()

elif who == data.QA:
    ui.page_header("Dashboard QA", )
    qa = state.followups_for(data.QA, cycle)
    qc = state.followups_for(data.QC, cycle)
    ui.stat_grid(
        [
            ("Temuan dari QC", len(qa), data.ROLE_COLOR[data.ROLE_MANAJER], ""),
            ("Menunggu keputusan Anda", sum(fu["status"] == data.F_MENUNGGU for _, fu in qa), color[data.F_MENUNGGU][0], ""),
            ("Sudah diputuskan", sum(fu["status"] == data.F_DIPUTUSKAN for _, fu in qa), color[data.F_DIPUTUSKAN][0], ""),
            ("Masih diperiksa QC", sum(fu["status"] == data.F_MENUNGGU for _, fu in qc), color[data.F_KE_QA][0], ""),
        ],
        min_width=190,
    )
    st.subheader("Temuan mutu")
    if qa:
        ui.table(_fu_rows(qa, with_images=True), badge_cols=("Tingkat Risiko", "Status"))
        for rec, fu in qa:
            qc_fu = rec["followups"].get(data.RT_QC, {})
            if qc_fu.get("images"):
                with st.expander(f"Gambar bukti QC — {data.stage_label(rec['stage_no'])}"):
                    ui.images_block(qc_fu["images"])
    else:
        ui.empty_state("Belum ada temuan", "Temuan muncul setelah QC menyimpan pemeriksaan mutu beserta fotonya.")
    ui.go("views/mgr_tindak_lanjut.py", "Buka Keputusan Mutu (input keputusan dan foto)", ":material/add_a_photo:")
    _reports_block()

elif who == data.QC:
    ui.page_header("Dashboard QC", "Tahap 8, 12, 18")
    qc = state.followups_for(data.QC, cycle)
    rows = []
    for no in data.QUALITY_STAGES:
        r = state.get_record(cycle, no)
        fu = r["followups"].get(data.RT_QC) if r else None
        rows.append(
            {
                "Tahap": data.stage_label(no),
                "Pemantau (formulir)": data.STAGE_STANDARD[no][3],
                "Shift": data.shift_name(r["shift"]) if r else "—",
                "Status Supervisor": r["status"] if r else data.S_BELUM,
                "Tingkat Risiko": r["level"] if r else "—",
                "Pemeriksaan QC": fu["status"] if fu else "Tidak diarahkan",
            }
        )
    ui.stat_grid(
        [
            ("Tahap mutu tercatat", sum(1 for no in data.QUALITY_STAGES if state.get_record(cycle, no)), data.ROLE_COLOR[data.ROLE_MANAJER], "/ 3"),
            ("Menunggu pemeriksaan Anda", sum(fu["status"] == data.F_MENUNGGU for _, fu in qc), color[data.F_MENUNGGU][0], ""),
            ("Sudah diteruskan ke QA", sum(fu["status"] == data.F_KE_QA for _, fu in qc), color[data.F_KE_QA][0], ""),
        ],
        min_width=200,
    )
    ui.table(pd.DataFrame(rows), badge_cols=("Status Supervisor", "Tingkat Risiko", "Pemeriksaan QC"))
    st.caption("Data Merah Tahap 08, 12, atau 18 yang sudah dikonfirmasi Supervisor masuk ke Pemeriksaan Mutu, lalu diteruskan ke QA.")
    ui.go("views/mgr_tindak_lanjut.py", "Buka Pemeriksaan Mutu (input temuan dan foto)", ":material/add_a_photo:")

else:
    ui.page_header("Dashboard Manajemen", "")
    st.error("Identitas manajemen tidak dikenali. Silakan keluar dan login kembali.")
