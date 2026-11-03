"""State sesi sementara (in-memory, st.session_state). Tidak ada database pada Fase 1.

Seluruh transisi alur (input Pekerja, tugas pemeriksaan kembali, validasi SPV, laporan gabungan,
penerimaan/konfirmasi/penerusan manajemen) berada di sini sehingga aturan ditegakkan oleh logika,
bukan hanya oleh tampilan.
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime

import pandas as pd
import streamlit as st

from core import data

MISSING_TEXT = "Belum tersedia"


# ---------------------------------------------------------------- dasar sesi
def init():
    ss = st.session_state
    ss.setdefault("logged_in", False)
    ss.setdefault("role", None)
    ss.setdefault("username", "")
    ss.setdefault("worker_id", None)
    ss.setdefault("records", {})  # "<siklus>|<no>" -> catatan tahapan
    ss.setdefault("tasks", [])  # tugas pemeriksaan kembali
    ss.setdefault("reports", {})  # siklus -> laporan gabungan
    ss.setdefault("events", [])  # riwayat sesi sementara
    ss.setdefault("task_seq", 0)
    ss.setdefault("cycle", data.DEMO_CYCLES[0])


def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def active_cycle():
    return st.session_state.get("cycle", data.DEMO_CYCLES[0])


def log(cycle, actor, text, stage=None, worker_id=None, kind="Alur"):
    st.session_state.events.append(
        {"at": now_str(), "cycle": cycle, "actor": actor, "text": text, "stage": stage, "worker_id": worker_id, "kind": kind}
    )


def actor_name():
    """Identitas akun yang sedang login. Untuk Manajemen: identitas yang dipilih saat login (Manager Produksi/PPIC/QC/QA)."""
    ss = st.session_state
    if ss.role == data.ROLE_PEKERJA and ss.worker_id in data.DEMO_WORKERS:
        return data.DEMO_WORKERS[ss.worker_id]["name"]
    if ss.role == data.ROLE_MANAJER and ss.username in data.MANAGEMENT_IDENTITIES:
        return ss.username
    return {data.ROLE_SPV: data.DEMO_SPV}.get(ss.role, "Pengguna DEMO")


def authenticate(account_id, password=None):
    """Login demonstrasi: cukup memilih akun DEMO. Isi password belum ditentukan sehingga tidak diperiksa."""
    return data.DEMO_ACCOUNTS.get(account_id)


def sign_in(account_id):
    ss = st.session_state
    acc = data.DEMO_ACCOUNTS[account_id]
    ss.logged_in = True
    ss.role = acc["role"]
    ss.worker_id = acc["worker_id"]
    ss.username = acc["label"]


# ---------------------------------------------------------------- penugasan pekerja
def assigned_stages(worker_id):
    return list(data.DEMO_WORKERS.get(worker_id, {}).get("stages", []))


def worker_for_stage(stage_no):
    for wid, w in data.DEMO_WORKERS.items():
        if stage_no in w["stages"]:
            return wid
    return None


def worker_name(worker_id):
    return data.DEMO_WORKERS.get(worker_id, {}).get("name", MISSING_TEXT)


# ---------------------------------------------------------------- akses catatan
def _key(cycle, no):
    return f"{cycle}|{no}"


def get_record(cycle, no):
    return st.session_state.records.get(_key(cycle, no))


def stage_status(cycle, no):
    rec = get_record(cycle, no)
    return rec["status"] if rec else data.S_BELUM


def status_counts(cycle):
    """Jumlah tahapan per status catatan; totalnya selalu 18."""
    counts = Counter(stage_status(cycle, no) for no in data.STAGE_NOS)
    result = {s: counts.get(s, 0) for s in data.RECORD_STATUS_ORDER}
    assert sum(result.values()) == len(data.STAGES), "hitungan status tidak sama dengan 18 tahapan"
    return result


def cycle_records(cycle):
    return [get_record(cycle, no) for no in data.STAGE_NOS if get_record(cycle, no)]


def get_report(cycle):
    return st.session_state.reports.get(cycle)


def report_status(cycle):
    rep = get_report(cycle)
    return rep["status"] if rep else data.R_NONE


# ---------------------------------------------------------------- tugas pemeriksaan kembali
def get_task(task_id):
    return next((t for t in st.session_state.tasks if t["id"] == task_id), None)


def tasks_for(cycle=None, worker_id=None, statuses=None):
    out = []
    for t in st.session_state.tasks:
        if cycle and t["cycle"] != cycle:
            continue
        if worker_id and t["worker_id"] != worker_id:
            continue
        if statuses and t["status"] not in statuses:
            continue
        out.append(t)
    return out


def completeness(cycle):
    """Gerbang True: 18 tahapan lengkap, tidak ada tugas pemeriksaan kembali yang belum selesai ditinjau."""
    missing = [no for no in data.STAGE_NOS if not get_record(cycle, no)]
    rechecking = [t["stage_no"] for t in tasks_for(cycle, statuses=[data.T_OPEN])]
    awaiting = [t["stage_no"] for t in tasks_for(cycle, statuses=[data.T_RESENT])]
    return {
        "recorded": 18 - len(missing),
        "missing": missing,
        "rechecking": rechecking,
        "awaiting_review": awaiting,
        "ready": not missing and not rechecking and not awaiting,
    }


# ---------------------------------------------------------------- teks tampilan
def val(x):
    return MISSING_TEXT if x in (None, "") else str(x)


def time_text(f):
    start, end = f.get("start"), f.get("end")
    if not start and not end:
        return "Belum dicatat"
    text = f"{start or 'Belum dicatat'} – {end or 'Belum dicatat'}"
    return text + (" (+1 hari)" if f.get("overnight") else "")


def duration_text(f):
    d = f.get("duration")
    return "Belum dicatat" if d in (None, "") else f"{d:g} {f.get('duration_unit') or ''}".strip()


def kg_text(f):
    kg = f.get("jumlah_kg")
    return "Belum dicatat" if kg in (None, "") else f"{kg:.2f}".rstrip("0").rstrip(".") + " kg"


def overview_df(cycle):
    rows = []
    for no, name in data.STAGES:
        rec = get_record(cycle, no)
        if rec:
            f = rec["data"]
            rows.append(
                {
                    "No": no,
                    "Tahapan": name,
                    "Status": rec["status"],
                    "Pekerja": rec["worker_name"] + (" (data contoh)" if rec.get("fixture") else ""),
                    "Waktu": time_text(f),
                    "Durasi": duration_text(f),
                    "Jumlah (kg)": kg_text(f),
                    "Diperbarui": rec["updated_at"].split(" ")[1],
                }
            )
        else:
            wid = worker_for_stage(no)
            rows.append(
                {
                    "No": no,
                    "Tahapan": name,
                    "Status": data.S_BELUM,
                    "Pekerja": f"{worker_name(wid)} (ditugaskan)",
                    "Waktu": "—",
                    "Durasi": "—",
                    "Jumlah (kg)": "—",
                    "Diperbarui": "—",
                }
            )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- validasi isian (aturan demonstrasi)
def validate_fields(f):
    """Aturan wajib isi ini hanya interaksi prototipe: Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO."""
    errors = []
    if not f.get("start") or not f.get("end"):
        errors.append("Waktu mulai dan waktu selesai wajib diisi.")
    elif f["end"] <= f["start"] and not f.get("overnight"):
        errors.append("Waktu selesai tidak lebih akhir dari waktu mulai. Centang 'melewati pergantian hari' bila memang demikian.")
    kg = f.get("jumlah_kg")
    if kg is None:
        errors.append("Jumlah Produksi (kg) wajib diisi. Isi 0 bila tidak ada produksi.")
    elif kg < 0:
        errors.append("Jumlah Produksi (kg) tidak boleh negatif.")
    if not f.get("pelaksana"):
        errors.append("Pelaksana/Pemantau wajib diisi.")
    if not f.get("kondisi"):
        errors.append("Kondisi proses wajib dipilih.")
    if not f.get("monitoring"):
        errors.append("Monitoring/Pencatatan wajib dipilih.")
    return errors


# ---------------------------------------------------------------- input Pekerja
def _new_record(cycle, no, worker_id, fields, actor, label, demo_fixture=False):
    ts = now_str()
    rec = {
        "cycle": cycle,
        "stage_no": no,
        "worker_id": worker_id,
        "worker_name": worker_name(worker_id),
        "data": deepcopy(fields),
        "status": data.S_TERKIRIM,
        "updated_at": ts,
        "demo": True,
        "fixture": demo_fixture,
        "versions": [{"label": label, "at": ts, "data": deepcopy(fields)}],
    }
    st.session_state.records[_key(cycle, no)] = rec
    log(cycle, actor, f"Tahap {no:02d} dicatat — status {data.S_TERKIRIM}", stage=no, worker_id=worker_id, kind="Pencatatan")
    return rec


def submit_record(cycle, stage_no, worker_id, fields):
    """Input awal Pekerja. Penugasan tahapan ditegakkan di sini, bukan hanya lewat pilihan dropdown."""
    if worker_id not in data.DEMO_WORKERS:
        return False, "Profil pekerja DEMO tidak dikenali; pengiriman ditolak."
    if stage_no not in assigned_stages(worker_id):
        return False, (
            f"Tahap {stage_no:02d} ({data.STAGE_NAMES.get(stage_no, '?')}) tidak ditugaskan kepada "
            f"{worker_name(worker_id)}. Pengiriman diblokir."
        )
    if (fields.get("jumlah_kg") or 0) < 0:
        return False, "Jumlah Produksi (kg) tidak boleh negatif."
    if get_report(cycle):
        return False, f"Siklus {cycle} sudah memiliki laporan gabungan; catatan tidak dapat ditambah."
    if get_record(cycle, stage_no):
        return False, (
            f"Tahap {stage_no:02d} sudah dicatat pada siklus {cycle}. Perubahan hanya melalui tugas "
            "pemeriksaan kembali dari SPV; catatan awal tidak ditimpa."
        )
    _new_record(cycle, stage_no, worker_id, fields, worker_name(worker_id), "Pengiriman awal")
    return True, f"Tahap {stage_no:02d} tercatat pada siklus {cycle}. Status: {data.S_TERKIRIM}."


# ---------------------------------------------------------------- tugas pemeriksaan kembali (SPV -> Pekerja)
def issue_recheck(cycle, stage_nos, note, actor=None):
    """Jalur Perlu Perbaikan: SPV memilih tahapan, wajib memberi catatan, tugas diteruskan ke pekerja penanggung jawab."""
    actor = actor or data.DEMO_SPV
    note = (note or "").strip()
    if get_report(cycle):
        return False, f"Siklus {cycle} sudah memiliki laporan gabungan; keputusan tidak dapat diubah.", []
    if not stage_nos:
        return False, "Pilih minimal satu tahapan yang perlu diperbaiki.", []
    if not note:
        return False, "Catatan perbaikan wajib diisi: jelaskan bagian yang perlu diperbaiki.", []
    for no in stage_nos:
        rec = get_record(cycle, no)
        if not rec:
            return False, f"Tahap {no:02d} belum dicatat sehingga belum bisa dikembalikan.", []
        if any(t["stage_no"] == no for t in tasks_for(cycle, statuses=[data.T_OPEN])):
            return False, f"Tahap {no:02d} masih memiliki tugas pemeriksaan kembali yang aktif.", []
    created = []
    for no in stage_nos:
        rec = get_record(cycle, no)
        for old in tasks_for(cycle, statuses=[data.T_RESENT]):
            if old["stage_no"] == no:  # kiriman ulang ditinjau lalu dikembalikan lagi
                old["status"] = data.T_DONE
                old["reviewed_at"] = now_str()
        st.session_state.task_seq += 1
        task = {
            "id": f"TUGAS-{st.session_state.task_seq:03d}",
            "cycle": cycle,
            "stage_no": no,
            "worker_id": rec["worker_id"],
            "note": note,
            "status": data.T_OPEN,
            "created_at": now_str(),
            "original": deepcopy(rec["data"]),
            "response": None,
            "resubmitted_at": None,
            "reviewed_at": None,
        }
        st.session_state.tasks.append(task)
        rec["status"] = data.S_KEMBALI
        rec["updated_at"] = now_str()
        created.append(task)
        log(cycle, actor, f"Tahap {no:02d} dikembalikan ke {rec['worker_name']} ({task['id']}) — catatan SPV: {note}",
            stage=no, worker_id=rec["worker_id"], kind="Validasi")
    log(cycle, actor, f"Keputusan validasi: {data.V_PERBAIKAN} ({len(created)} tahapan)", kind="Validasi")
    return True, f"{len(created)} tugas pemeriksaan kembali dibuat.", created


def resubmit_task(task_id, worker_id, fields):
    """Pekerja mengirim ulang informasi yang sudah diperiksa. Hanya pemilik tugas yang boleh."""
    task = get_task(task_id)
    if not task:
        return False, "Tugas tidak ditemukan."
    if task["worker_id"] != worker_id:
        return False, f"Tugas {task_id} ditugaskan kepada {worker_name(task['worker_id'])}, bukan {worker_name(worker_id)}. Diblokir."
    if task["status"] != data.T_OPEN:
        return False, f"Tugas {task_id} tidak sedang menunggu pekerja (status: {task['status']})."
    if (fields.get("jumlah_kg") or 0) < 0:
        return False, "Jumlah Produksi (kg) tidak boleh negatif."
    rec = get_record(task["cycle"], task["stage_no"])
    ts = now_str()
    rec["data"] = deepcopy(fields)
    rec["versions"].append({"label": f"Dikirim ulang ({task_id})", "at": ts, "data": deepcopy(fields)})
    rec["status"] = data.S_KIRIM_ULANG
    rec["updated_at"] = ts
    rec["fixture"] = False  # isian terbaru berasal dari pengguna, bukan data contoh
    task["response"] = deepcopy(fields)
    task["resubmitted_at"] = ts
    task["status"] = data.T_RESENT
    log(task["cycle"], worker_name(worker_id), f"Tahap {task['stage_no']:02d} dikirim ulang ({task_id}); catatan SPV sebelumnya: {task['note']}",
        stage=task["stage_no"], worker_id=worker_id, kind="Pengiriman ulang")
    return True, f"Tugas {task_id} dikirim ulang. Status: {data.S_KIRIM_ULANG}."


def accept_resubmission(task_id, actor=None):
    actor = actor or data.DEMO_SPV
    task = get_task(task_id)
    if not task or task["status"] != data.T_RESENT:
        return False, "Tidak ada kiriman ulang yang menunggu tinjauan untuk tugas ini."
    rec = get_record(task["cycle"], task["stage_no"])
    task["status"] = data.T_DONE
    task["reviewed_at"] = now_str()
    rec["status"] = data.S_TERKIRIM
    rec["updated_at"] = now_str()
    log(task["cycle"], actor, f"Kiriman ulang tahap {task['stage_no']:02d} ({task_id}) ditinjau SPV", stage=task["stage_no"],
        worker_id=task["worker_id"], kind="Validasi")
    return True, f"Kiriman ulang {task_id} ditandai sudah ditinjau."


# ---------------------------------------------------------------- jalur Laporan Diterima: laporan gabungan
def accept_report(cycle, actor=None):
    """Satu laporan gabungan per siklus; klik berulang tidak membuat duplikat."""
    actor = actor or data.DEMO_SPV
    if get_report(cycle):
        return False, f"Siklus {cycle} sudah memiliki laporan gabungan; tidak dibuat ulang."
    gate = completeness(cycle)
    if not gate["ready"]:
        parts = []
        if gate["missing"]:
            parts.append(f"{len(gate['missing'])} tahapan belum dicatat")
        if gate["rechecking"]:
            parts.append(f"{len(gate['rechecking'])} tugas menunggu pekerja")
        if gate["awaiting_review"]:
            parts.append(f"{len(gate['awaiting_review'])} kiriman ulang belum ditinjau")
        return False, "Laporan belum dapat diterima: " + "; ".join(parts) + "."
    ts = now_str()
    stages = []
    for no in data.STAGE_NOS:
        rec = get_record(cycle, no)
        stages.append(
            {
                "no": no,
                "name": data.STAGE_NAMES[no],
                "worker_name": rec["worker_name"],
                "submitted_at": rec["versions"][0]["at"],
                "data": deepcopy(rec["data"]),
                "resubmitted": len(rec["versions"]) > 1,
                "fixture": bool(rec.get("fixture")),
            }
        )
        rec["status"] = data.S_LAPORAN
        rec["updated_at"] = ts
    st.session_state.reports[cycle] = {
        "cycle": cycle,
        "status": data.R_GENERATED,
        "generated_at": ts,
        "validated_by": actor,
        "stages": stages,
        "handoff_at": None,
        "confirmed_at": None,
        "confirmed_by": None,
        "forwarded_at": None,
        "forwarded_by": None,
    }
    log(cycle, actor, f"Keputusan validasi: {data.V_DITERIMA}; laporan gabungan 18 tahapan dihasilkan", kind="Validasi")
    return True, f"Laporan gabungan siklus {cycle} dihasilkan (18 tahapan)."


def draft_report(cycle):
    """Draf laporan gabungan dari catatan terkini (belum divalidasi) agar SPV dapat memeriksa 18 tahapan sebelum memutuskan.

    Tidak disimpan dan bukan laporan resmi; tahapan yang belum dicatat tetap muncul dengan isian kosong.
    """
    stages = []
    for no in data.STAGE_NOS:
        rec = get_record(cycle, no)
        stages.append(
            {
                "no": no,
                "name": data.STAGE_NAMES[no],
                "worker_name": rec["worker_name"] if rec else worker_name(worker_for_stage(no)),
                "submitted_at": rec["versions"][0]["at"] if rec else "—",
                "data": deepcopy(rec["data"]) if rec else {},
                "resubmitted": bool(rec) and len(rec["versions"]) > 1,
                "fixture": bool(rec and rec.get("fixture")),
                "status": rec["status"] if rec else data.S_BELUM,
            }
        )
    return {"cycle": cycle, "stages": stages}


def handoff_to_ppic(cycle, actor=None):
    actor = actor or data.DEMO_SPV
    rep = get_report(cycle)
    if not rep or rep["status"] != data.R_GENERATED:
        return False, "Laporan belum dihasilkan atau sudah diteruskan."
    rep["status"] = data.R_MASUK
    rep["handoff_at"] = now_str()
    log(cycle, actor, "Laporan gabungan diteruskan ke PPIC (masuk ke Manajemen)", kind="Laporan")
    return True, f"Laporan siklus {cycle} diteruskan ke PPIC."


def confirm_report(cycle, actor):
    """`actor` wajib identitas Manajemen yang sedang login (tidak ada nilai bawaan agar tidak ditentukan otomatis)."""
    if actor not in data.MANAGEMENT_IDENTITIES:
        return False, "Identitas pelaksana tidak dikenali; konfirmasi diblokir."
    rep = get_report(cycle)
    if not rep or rep["status"] != data.R_MASUK:
        return False, "Konfirmasi diblokir: laporan belum masuk ke Manajemen atau sudah dikonfirmasi."
    rep["status"] = data.R_KONFIRMASI
    rep["confirmed_at"] = now_str()
    rep["confirmed_by"] = actor
    log(cycle, actor, f"Laporan diperiksa dan dikonfirmasi oleh {actor}", kind="Laporan")
    return True, f"Laporan siklus {cycle} dikonfirmasi oleh {actor}."


def forward_to_gm(cycle, actor):
    if actor not in data.MANAGEMENT_IDENTITIES:
        return False, "Identitas pelaksana tidak dikenali; penerusan diblokir."
    rep = get_report(cycle)
    if not rep or rep["status"] != data.R_KONFIRMASI:
        return False, "Penerusan diblokir: laporan harus dikonfirmasi terlebih dahulu."
    rep["status"] = data.R_GM
    rep["forwarded_at"] = now_str()
    rep["forwarded_by"] = actor
    log(cycle, actor, f"Laporan diteruskan ke {data.GM} (DEMO) oleh {actor}", kind="Laporan")
    return True, f"Laporan siklus {cycle} diteruskan ke {data.GM} (DEMO) oleh {actor}."


def has_fixture(cycle):
    return any(r.get("fixture") for r in cycle_records(cycle))


def reports_visible_to_management():
    """Hanya laporan yang sudah diteruskan SPV ke PPIC yang terlihat oleh Manajemen."""
    return [r for r in st.session_state.reports.values() if r["status"] != data.R_GENERATED]


# ---------------------------------------------------------------- DEMO
_DEMO_CYCLE_FOR = {
    data.SC_LENGKAP: data.DEMO_CYCLES[0],
    data.SC_BELUM: data.DEMO_CYCLES[1],
    data.SC_MASUK: data.DEMO_CYCLES[2],
}


def _demo_fields():
    # Hanya placeholder: tidak ada nilai produksi, waktu, atau hasil mutu karangan.
    return {
        "start": None,
        "end": None,
        "overnight": False,
        "duration": None,
        "duration_unit": data.DURASI_UNITS[0],
        "jumlah_kg": None,
        "pelaksana": None,
        "kondisi": None,
        "monitoring": None,
        "catatan": "[contoh DEMO] Isian formulir belum diisi.",
    }


def _ensure_records(cycle, stage_nos):
    added = 0
    for no in stage_nos:
        if get_record(cycle, no):
            continue
        wid = worker_for_stage(no)
        _new_record(cycle, no, wid, _demo_fields(), f"{worker_name(wid)} (data DEMO)", "Pengiriman awal (data DEMO)", demo_fixture=True)
        added += 1
    return added


def load_demo(scenario):
    """Muat fixture DEMO sesuai skenario tanpa menggandakan data bila ditekan berulang.

    Setiap skenario memakai siklusnya sendiri, sehingga "Semua Skenario" tidak mencampur status yang
    bertentangan dalam satu siklus produksi.
    """
    scenarios = [data.SC_LENGKAP, data.SC_BELUM, data.SC_MASUK] if scenario == data.SC_SEMUA else [scenario]
    records_added = reports_added = tasks_added = 0
    spv = f"{data.DEMO_SPV} (data DEMO)"
    for sc in scenarios:
        cycle = _DEMO_CYCLE_FOR[sc]
        if sc == data.SC_BELUM:
            records_added += _ensure_records(cycle, data.STAGE_NOS[:15])
            if not tasks_for(cycle):  # satu tugas pemeriksaan kembali contoh untuk memperagakan jalur Perlu Perbaikan
                ok, _, made = issue_recheck(cycle, [3], "[contoh DEMO] Periksa kembali isian tahapan ini.", spv)
                tasks_added += len(made) if ok else 0
        else:
            records_added += _ensure_records(cycle, data.STAGE_NOS)
        if sc == data.SC_MASUK and not get_report(cycle):
            ok, _ = accept_report(cycle, spv)
            if ok:
                handoff_to_ppic(cycle, spv)
                reports_added += 1
    return {"records": records_added, "tasks": tasks_added, "reports": reports_added, "cycles": [_DEMO_CYCLE_FOR[sc] for sc in scenarios]}


def reset_demo():
    """Satu-satunya cara menghapus data DEMO (Keluar tidak menghapusnya)."""
    ss = st.session_state
    ss.records = {}
    ss.tasks = []
    ss.reports = {}
    ss.events = []
    ss.task_seq = 0
    ss.pop("_mgr_pick", None)
    for k in [k for k in ss if str(k).startswith(("rc_", "inp_", "val_", "pen_", "cf_", "mgr_"))]:
        ss.pop(k, None)
