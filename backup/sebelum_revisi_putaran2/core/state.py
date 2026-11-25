"""State sesi sementara (in-memory, st.session_state). Tidak ada database pada Fase 1.

Seluruh transisi alur berada di sini sehingga aturan ditegakkan oleh logika, bukan hanya oleh tampilan:
input per pekerja -> konfirmasi/permintaan perbaikan per tahapan oleh SPV -> Generate Report (18 tahapan terkonfirmasi) ->
penerusan ke Manajemen -> pemeriksaan/konfirmasi atau pengembalian ke SPV -> penerusan ke General Manager (DEMO).
Setiap tindakan final memeriksa status lebih dulu, sehingga klik berulang atau identitas lain tidak dapat menggandakannya.
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from core import data

MISSING_TEXT = "Belum tersedia"
TS_FORMAT = "%d/%m/%Y %H:%M:%S"
EDIT_WINDOW = timedelta(hours=data.EDIT_WINDOW_HOURS)


# ---------------------------------------------------------------- dasar sesi
def init():
    ss = st.session_state
    ss.setdefault("logged_in", False)
    ss.setdefault("role", None)
    ss.setdefault("username", "")
    ss.setdefault("worker_id", None)
    ss.setdefault("records", {})  # "<siklus>|<no>" -> laporan tahapan
    ss.setdefault("tasks", [])  # tugas pemeriksaan kembali
    ss.setdefault("reports", {})  # siklus -> laporan gabungan
    ss.setdefault("events", [])  # riwayat sesi sementara
    ss.setdefault("task_seq", 0)
    ss.setdefault("cycle", data.INTERNAL_CYCLE)  # internal: tidak ada pilihan siklus pada UI


def now():
    return datetime.now()


def stamp(dt=None):
    return (dt or now()).strftime(TS_FORMAT)


def now_str():
    return stamp()


def active_cycle():
    return st.session_state.get("cycle", data.INTERNAL_CYCLE)


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


def worker_stage(worker_id):
    """Tahapan tunggal milik pekerja (satu pekerja = satu tahapan)."""
    stages = assigned_stages(worker_id)
    return stages[0] if stages else None


# ---------------------------------------------------------------- akses laporan tahapan
def _key(cycle, no):
    return f"{cycle}|{no}"


def get_record(cycle, no):
    return st.session_state.records.get(_key(cycle, no))


def stage_status(cycle, no):
    rec = get_record(cycle, no)
    return rec["status"] if rec else data.S_BELUM


def input_status(rec):
    """Status penginputan (sisi pekerja), terpisah dari status pemeriksaan SPV."""
    if not rec:
        return data.IN_BELUM
    return data.IN_DIPERBAIKI if rec["versions"][-1]["kind"] == "perbaikan" else data.IN_KIRIM


def was_corrected(rec):
    return bool(rec) and any(v["kind"] == "perbaikan" for v in rec["versions"])


def status_counts(cycle):
    """Jumlah tahapan per status pemeriksaan; totalnya selalu 18."""
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


def tasks_for(cycle=None, worker_id=None, statuses=None, stage_no=None):
    out = []
    for t in st.session_state.tasks:
        if cycle and t["cycle"] != cycle:
            continue
        if worker_id and t["worker_id"] != worker_id:
            continue
        if statuses and t["status"] not in statuses:
            continue
        if stage_no and t["stage_no"] != stage_no:
            continue
        out.append(t)
    return out


# ---------------------------------------------------------------- teks tampilan
def val(x):
    return MISSING_TEXT if x in (None, "") else str(x)


def time_text(f):
    start, end = f.get("start"), f.get("end")
    if not start and not end:
        return "Belum dicatat"
    text = f"{start or 'Belum dicatat'} – {end or 'Belum dicatat'}"
    return text + (" (+1 hari)" if f.get("overnight") else "")


def duration_minutes(f):
    """Durasi dihitung otomatis dari waktu mulai dan selesai (pekerja tidak mengisinya)."""
    try:
        s = datetime.strptime(f["start"], "%H:%M")
        e = datetime.strptime(f["end"], "%H:%M")
    except (KeyError, TypeError, ValueError):
        return None
    delta = (e - s).total_seconds() / 60
    if f.get("overnight"):
        delta += 24 * 60
    return int(delta) if delta >= 0 else None


def duration_text(f):
    m = duration_minutes(f)
    if m is None:
        return "Belum dicatat"
    h, mm = divmod(m, 60)
    return " ".join(p for p in (f"{h} jam" if h else "", f"{mm} menit" if mm or not h else "") if p)


def kg_text(f):
    kg = f.get("jumlah_kg")
    return "Belum dicatat" if kg in (None, "") else f"{kg:.2f}".rstrip("0").rstrip(".") + " kg"


def sent_text(rec):
    return rec["sent_at"] if rec else "—"


def edit_info(rec, at=None):
    """Apakah pekerja masih boleh mengedit laporan tahapan ini (aturan prototipe 6 jam, sebelum konfirmasi SPV)."""
    at = at or now()
    if not rec:
        return {"can_edit": False, "reason": "Belum ada laporan.", "deadline": None}
    deadline = rec["edit_deadline_dt"]
    base = {"deadline": stamp(deadline)}
    if rec["locked"] or rec["status"] == data.S_KONFIRMASI:
        return {**base, "can_edit": False, "reason": "Laporan sudah dikonfirmasi SPV dan terkunci."}
    if rec["status"] == data.S_KEMBALI:
        return {**base, "can_edit": False, "reason": "SPV meminta perbaikan. Gunakan menu Tugas Pemeriksaan Kembali untuk memperbaiki laporan.", "via_task": True}
    if at > deadline:
        return {**base, "can_edit": False, "reason": f"Periode pengeditan ({data.EDIT_WINDOW_HOURS} jam sejak pengiriman) telah berakhir pada {stamp(deadline)}."}
    return {**base, "can_edit": True, "reason": ""}


# ---------------------------------------------------------------- validasi isian (aturan demonstrasi)
def validate_fields(f, stage_no):
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
    if f.get("pelaksana") not in data.PELAKSANA_OPTIONS:
        errors.append("Pelaksana/Pemantau wajib dipilih.")
    if f.get("kondisi") not in data.KONDISI_OPTIONS:
        errors.append("Kondisi proses wajib dipilih.")
    elif f["kondisi"] != data.KONDISI_NORMAL and not (f.get("kendala") or "").strip():
        errors.append("Jelaskan Kendala yang Terjadi wajib diisi karena kondisi proses bukan Normal.")
    if stage_no == data.OPENING_STAGE and f.get("arrival") not in data.OPENING_ARRIVAL_OPTIONS:
        errors.append("Waktu Kedatangan Bahan Baku wajib dipilih.")
    return errors


def _normalize(fields, stage_no):
    f = deepcopy(fields)
    if f.get("kondisi") == data.KONDISI_NORMAL:
        f["kendala"] = ""  # kondisi Normal dicatat tanpa penjelasan
    else:
        f["kendala"] = (f.get("kendala") or "").strip()
    if stage_no != data.OPENING_STAGE:
        f["arrival"] = None  # pilihan kedatangan hanya untuk Opening
    f.pop("duration", None)
    f.pop("monitoring", None)
    return f


# ---------------------------------------------------------------- input Pekerja
def _new_record(cycle, no, worker_id, fields):
    ts = now()
    deadline = ts + EDIT_WINDOW
    rec = {
        "report_id": f"{cycle}-{data.stage_code(no)}",
        "cycle": cycle,
        "stage_no": no,
        "process_id": data.stage_code(no),
        "process_name": data.STAGE_NAMES[no],
        "worker_id": worker_id,
        "worker_name": worker_name(worker_id),
        "data": deepcopy(fields),
        "status": data.S_MENUNGGU,
        "submitted_at": stamp(ts),
        "sent_at": stamp(ts),
        "edit_deadline_dt": deadline,
        "updated_at": stamp(ts),
        "locked": False,
        "confirmed_by": None,
        "confirmed_at": None,
        "confirm_history": [],
        "spv_note": None,
        "versions": [{"label": "Versi awal (pengiriman pertama)", "kind": "awal", "at": stamp(ts), "by": worker_name(worker_id), "data": deepcopy(fields), "spv_note": None}],
    }
    st.session_state.records[_key(cycle, no)] = rec
    log(cycle, rec["worker_name"], f"Tahap {no:02d} dikirim ke SPV — status {data.S_MENUNGGU}", stage=no, worker_id=worker_id, kind="Pencatatan")
    return rec


def submit_record(cycle, stage_no, worker_id, fields):
    """Input awal Pekerja. Penugasan tahapan ditegakkan di sini, bukan hanya lewat tampilan."""
    if worker_id not in data.DEMO_WORKERS:
        return False, "Akun pekerja tidak dikenali; pengiriman ditolak."
    if stage_no not in assigned_stages(worker_id):
        return False, (
            f"Tahap {stage_no:02d} ({data.STAGE_NAMES.get(stage_no, '?')}) tidak ditugaskan kepada "
            f"{worker_name(worker_id)}. Pengiriman diblokir."
        )
    fields = _normalize(fields, stage_no)
    errors = validate_fields(fields, stage_no)
    if errors:
        return False, " ".join(errors)
    if get_record(cycle, stage_no):
        return False, f"Laporan tahap {stage_no:02d} sudah pernah dikirim; tidak dikirim ganda. Perubahan lewat menu Input (maks. {data.EDIT_WINDOW_HOURS} jam) atau Tugas Pemeriksaan Kembali."
    _new_record(cycle, stage_no, worker_id, fields)
    return True, f"Laporan tahap {stage_no:02d} berhasil dikirim ke SPV. Status: {data.S_MENUNGGU}."


def edit_record(cycle, stage_no, worker_id, fields):
    """Pengeditan oleh Pekerja dalam batas waktu 6 jam dan sebelum dikonfirmasi SPV. Versi awal tidak ditimpa."""
    rec = get_record(cycle, stage_no)
    if not rec:
        return False, "Belum ada laporan untuk diedit."
    if rec["worker_id"] != worker_id:
        return False, f"Laporan ini milik {rec['worker_name']}; pengeditan diblokir."
    info = edit_info(rec)
    if not info["can_edit"]:
        return False, info["reason"]
    fields = _normalize(fields, stage_no)
    errors = validate_fields(fields, stage_no)
    if errors:
        return False, " ".join(errors)
    if fields == rec["data"]:
        return False, "Tidak ada perubahan yang perlu disimpan."
    ts = stamp()
    rec["data"] = deepcopy(fields)
    rec["versions"].append({"label": "Diedit Pekerja (dalam batas waktu)", "kind": "edit", "at": ts, "by": rec["worker_name"], "data": deepcopy(fields), "spv_note": None})
    rec["updated_at"] = ts
    log(cycle, rec["worker_name"], f"Tahap {stage_no:02d} diedit Pekerja — versi {len(rec['versions'])}", stage=stage_no, worker_id=worker_id, kind="Pencatatan")
    return True, f"Perubahan tersimpan sebagai versi {len(rec['versions'])}. Versi sebelumnya tetap tersimpan."


# ---------------------------------------------------------------- SPV: konfirmasi / hubungi pekerja per tahapan
def _close_resent(cycle, no):
    for t in tasks_for(cycle, statuses=[data.T_RESENT], stage_no=no):
        t["status"] = data.T_DONE
        t["reviewed_at"] = now_str()


def confirm_stage(cycle, stage_no, actor=None, reviewed=False):
    """Konfirmasi Tahapan: hanya satu tahapan; mengunci laporan pekerja. `reviewed` = SPV menyatakan sudah memeriksa."""
    actor = actor or data.DEMO_SPV
    rec = get_record(cycle, stage_no)
    if not rec:
        return False, f"Tahap {stage_no:02d} belum memiliki laporan; konfirmasi tidak tersedia."
    if rec["status"] == data.S_KONFIRMASI:
        return False, f"Tahap {stage_no:02d} sudah dikonfirmasi oleh {rec['confirmed_by']}; tidak dikonfirmasi ganda."
    if rec["status"] == data.S_KEMBALI:
        return False, f"Tahap {stage_no:02d} sedang menunggu perbaikan Pekerja; belum dapat dikonfirmasi."
    rep = get_report(cycle)
    if rep and rep["status"] != data.R_PERBAIKAN:  # laporan yang dikembalikan Manajemen boleh dikonfirmasi ulang per tahapan
        return False, "Laporan gabungan sudah dihasilkan; konfirmasi tahapan tidak dapat diubah."
    if not reviewed:
        return False, "Centang pernyataan bahwa laporan tahapan sudah diperiksa sebelum mengonfirmasi."
    ts = stamp()
    _close_resent(cycle, stage_no)
    rec["status"] = data.S_KONFIRMASI
    rec["confirmed_by"] = actor
    rec["confirmed_at"] = ts
    rec["locked"] = True
    rec["updated_at"] = ts
    log(cycle, actor, f"Tahap {stage_no:02d} dikonfirmasi SPV dan dikunci", stage=stage_no, worker_id=rec["worker_id"], kind="Validasi")
    return True, f"Tahap {stage_no:02d} dikonfirmasi dan dikunci."


def contact_worker(cycle, stage_no, note, actor=None):
    """Hubungi Pekerja: catatan wajib, membuat tugas pemeriksaan kembali untuk pekerja penanggung jawab."""
    actor = actor or data.DEMO_SPV
    note = (note or "").strip()
    rec = get_record(cycle, stage_no)
    if not rec:
        return False, f"Tahap {stage_no:02d} belum memiliki laporan; tidak ada yang dapat dikembalikan.", None
    if rec["status"] == data.S_KEMBALI:
        return False, f"Tahap {stage_no:02d} sudah memiliki tugas perbaikan yang menunggu Pekerja.", None
    rep = get_report(cycle)
    if rep and rep["status"] != data.R_PERBAIKAN:
        return False, "Laporan gabungan sudah dihasilkan dan sedang diproses; tahapan terkunci.", None
    if not note:
        return False, "Catatan untuk Pekerja wajib diisi: jelaskan hal yang perlu diperiksa atau diperbaiki.", None
    ts = stamp()
    _close_resent(cycle, stage_no)
    if rec["status"] == data.S_KONFIRMASI:
        rec["confirm_history"].append({"by": rec["confirmed_by"], "at": rec["confirmed_at"], "reopened_at": ts})
        rec["confirmed_by"] = rec["confirmed_at"] = None
        rec["locked"] = False
    st.session_state.task_seq += 1
    task = {
        "id": f"TUGAS-{st.session_state.task_seq:03d}",
        "cycle": cycle,
        "stage_no": stage_no,
        "worker_id": rec["worker_id"],
        "note": note,
        "status": data.T_OPEN,
        "created_at": ts,
        "created_by": actor,
        "original": deepcopy(rec["data"]),
        "resubmitted_at": None,
        "reviewed_at": None,
    }
    st.session_state.tasks.append(task)
    rec["status"] = data.S_KEMBALI
    rec["spv_note"] = note
    rec["updated_at"] = ts
    log(cycle, actor, f"Tahap {stage_no:02d} dikembalikan ke {rec['worker_name']} ({task['id']}) — catatan SPV: {note}",
        stage=stage_no, worker_id=rec["worker_id"], kind="Validasi")
    return True, f"Catatan dikirim kepada {rec['worker_name']}. Tugas {task['id']} dibuat.", task


def resubmit_task(task_id, worker_id, fields):
    """Pekerja mengirim hasil perbaikan. Hanya pemilik tugas yang boleh; versi sebelumnya tetap tersimpan."""
    task = get_task(task_id)
    if not task:
        return False, "Tugas tidak ditemukan."
    if task["worker_id"] != worker_id:
        return False, f"Tugas {task_id} ditugaskan kepada {worker_name(task['worker_id'])}, bukan {worker_name(worker_id)}. Diblokir."
    if task["status"] != data.T_OPEN:
        return False, f"Tugas {task_id} tidak sedang menunggu pekerja (status: {task['status']}); tidak dikirim ganda."
    no = task["stage_no"]
    fields = _normalize(fields, no)
    errors = validate_fields(fields, no)
    if errors:
        return False, " ".join(errors)
    rec = get_record(task["cycle"], no)
    ts_dt = now()
    ts = stamp(ts_dt)
    rec["data"] = deepcopy(fields)
    rec["versions"].append({"label": f"Perbaikan dikirim ({task_id})", "kind": "perbaikan", "at": ts, "by": rec["worker_name"],
                            "data": deepcopy(fields), "spv_note": task["note"]})
    rec["status"] = data.S_ULANG
    rec["sent_at"] = ts
    rec["edit_deadline_dt"] = ts_dt + EDIT_WINDOW
    rec["updated_at"] = ts
    task["resubmitted_at"] = ts
    task["status"] = data.T_RESENT
    log(task["cycle"], rec["worker_name"], f"Tahap {no:02d} perbaikan dikirim ulang ({task_id}); catatan SPV: {task['note']}",
        stage=no, worker_id=worker_id, kind="Pengiriman ulang")
    return True, f"Perbaikan dikirim ke SPV. Status: {data.S_ULANG}."


# ---------------------------------------------------------------- gerbang Generate Report
def completeness(cycle):
    """Syarat Generate Report (§6.6): 18 tahapan punya laporan, terperiksa, terkonfirmasi, tanpa tugas terbuka, data lengkap."""
    recs = {no: get_record(cycle, no) for no in data.STAGE_NOS}
    missing = [no for no, r in recs.items() if not r]
    by = lambda s: [no for no, r in recs.items() if r and r["status"] == s]
    waiting, fix, recheck, confirmed = by(data.S_MENUNGGU), by(data.S_KEMBALI), by(data.S_ULANG), by(data.S_KONFIRMASI)
    open_tasks = [t["stage_no"] for t in tasks_for(cycle, statuses=[data.T_OPEN])]
    incomplete = [no for no, r in recs.items() if r and validate_fields(r["data"], no)]
    return {
        "recorded": 18 - len(missing),
        "missing": missing,
        "waiting": waiting,
        "fix": fix,
        "recheck": recheck,
        "confirmed": confirmed,
        "open_tasks": open_tasks,
        "incomplete": incomplete,
        "unmet": 18 - len(confirmed),
        "ready": len(confirmed) == 18 and not open_tasks and not incomplete,
    }


def gate_reasons(gate):
    """Alasan yang jelas mengapa Generate Report belum dapat dilakukan (kosong bila sudah siap)."""
    nums = lambda l: ", ".join(f"{n:02d}" for n in l)
    out = []
    if gate["missing"]:
        out.append(f"{len(gate['missing'])} tahapan belum memiliki laporan ({nums(gate['missing'])}).")
    if gate["waiting"]:
        out.append(f"{len(gate['waiting'])} tahapan yang menunggu pemeriksaan SPV ({nums(gate['waiting'])}).")
    if gate["fix"]:
        out.append(f"{len(gate['fix'])} tahapan berstatus Perlu Perbaikan ({nums(gate['fix'])}).")
    if gate["recheck"]:
        out.append(f"{len(gate['recheck'])} tahapan yang menunggu pemeriksaan ulang SPV ({nums(gate['recheck'])}).")
    if gate["incomplete"]:
        out.append(f"{len(gate['incomplete'])} tahapan dengan data wajib yang belum lengkap ({nums(gate['incomplete'])}).")
    extra_tasks = [n for n in gate["open_tasks"] if n not in gate["fix"]]
    if extra_tasks:
        out.append(f"{len(extra_tasks)} tugas pemeriksaan kembali masih terbuka ({nums(extra_tasks)}).")
    return out


def gate_headline(gate):
    if gate["ready"]:
        return "Seluruh 18 tahapan telah dikonfirmasi SPV. Generate Report dapat dilakukan."
    return f"Generate Report belum dapat dilakukan. Masih terdapat {gate['unmet']} tahapan yang belum memenuhi persyaratan."


def spv_cycle_status(cycle):
    """Satu label status siklus untuk Dashboard SPV (Status Laporan)."""
    rep = get_report(cycle)
    if rep:
        return rep["status"]
    g = completeness(cycle)
    if g["fix"] or g["open_tasks"]:
        return data.C_PERBAIKAN
    if g["recheck"]:
        return data.C_ULANG
    if g["waiting"]:
        return data.C_MENUNGGU_SPV
    if g["missing"]:
        return data.C_MENUNGGU_INPUT
    return data.R_SIAP if g["ready"] else data.C_MENUNGGU_SPV


# ---------------------------------------------------------------- laporan gabungan
def _snapshot(cycle):
    stages = []
    for no in data.STAGE_NOS:
        rec = get_record(cycle, no)
        stages.append(
            {
                "no": no,
                "name": data.STAGE_NAMES[no],
                "worker_name": rec["worker_name"],
                "submitted_at": rec["submitted_at"],
                "data": deepcopy(rec["data"]),
                "versions": len(rec["versions"]),
                "status": rec["status"],
                "confirmed_by": rec["confirmed_by"],
                "confirmed_at": rec["confirmed_at"],
            }
        )
    return stages


def production_date(cycle):
    """Tanggal produksi laporan = tanggal pencatatan pertama pada siklus (aplikasi tidak meminta tanggal terpisah)."""
    first = min((r["submitted_at"] for r in cycle_records(cycle)), default=None, key=lambda t: datetime.strptime(t, TS_FORMAT))
    return first.split(" ")[0] if first else "—"


def generate_report(cycle, actor=None):
    """Generate Report: hanya setelah seluruh syarat terpenuhi; satu laporan gabungan per siklus (tidak ganda)."""
    actor = actor or data.DEMO_SPV
    if get_report(cycle):
        return False, "Laporan gabungan untuk siklus ini sudah pernah dihasilkan; tidak dibuat ganda."
    gate = completeness(cycle)
    if not gate["ready"]:
        return False, gate_headline(gate)
    ts = stamp()
    stages = _snapshot(cycle)
    st.session_state.reports[cycle] = {
        "report_id": f"LG-{cycle}",
        "cycle": cycle,
        "status": data.R_GENERATED,
        "production_date": production_date(cycle),
        "generated_at": ts,
        "generated_by": actor,
        "stages": stages,
        "versions": [{"no": 1, "kind": "Dihasilkan", "at": ts, "by": actor, "note": None}],
        "handoff_at": None,
        "handoff_by": None,
        "returns": [],  # pengembalian oleh Manajemen
        "checked_by": None,
        "checked_at": None,
        "confirmed_at": None,
        "confirmed_by": None,
        "forwarded_at": None,
        "forwarded_by": None,
        "gm_received_at": None,
    }
    log(cycle, actor, "Generate Report: laporan gabungan 18 tahapan dihasilkan", kind="Laporan")
    return True, "Laporan gabungan berhasil dihasilkan (18 tahapan)."


def handoff_to_management(cycle, actor=None):
    actor = actor or data.DEMO_SPV
    rep = get_report(cycle)
    if not rep:
        return False, "Laporan gabungan belum dihasilkan."
    if rep["status"] != data.R_GENERATED:
        return False, f"Laporan sudah diteruskan ke Manajemen ({rep['handoff_at']} oleh {rep['handoff_by']}); tidak dapat diteruskan ulang."
    rep["status"] = data.R_MASUK
    rep["handoff_at"] = now_str()
    rep["handoff_by"] = actor
    log(cycle, actor, "Laporan gabungan diteruskan ke Manajemen", kind="Laporan")
    return True, "Laporan gabungan berhasil diteruskan ke Manajemen."


def resend_report(cycle, note, actor=None):
    """SPV mengirim kembali laporan yang dikembalikan Manajemen. Laporan lama tetap tersimpan sebagai versi sebelumnya."""
    actor = actor or data.DEMO_SPV
    note = (note or "").strip()
    rep = get_report(cycle)
    if not rep or rep["status"] != data.R_PERBAIKAN:
        return False, "Tidak ada laporan yang sedang menunggu perbaikan SPV."
    gate = completeness(cycle)
    if not gate["ready"]:
        return False, gate_headline(gate)
    if not note:
        return False, "Tanggapan SPV wajib diisi: jelaskan perbaikan yang dilakukan."
    ts = stamp()
    rep["stages"] = _snapshot(cycle)
    rep["versions"].append({"no": len(rep["versions"]) + 1, "kind": "Dikirim ulang", "at": ts, "by": actor, "note": note})
    rep["status"] = data.R_ULANG
    rep["returns"][-1]["response"] = note
    rep["returns"][-1]["responded_at"] = ts
    rep["returns"][-1]["responded_by"] = actor
    log(cycle, actor, f"Laporan gabungan diperbaiki dan dikirim kembali ke Manajemen — tanggapan SPV: {note}", kind="Laporan")
    return True, "Laporan berhasil dikirim kembali ke Manajemen."


def _need_identity(actor):
    return actor in data.MANAGEMENT_IDENTITIES


def confirm_report(cycle, actor, checked=False):
    """`actor` wajib identitas Manajemen yang sedang login (tidak ada nilai bawaan agar tidak ditentukan otomatis)."""
    if not _need_identity(actor):
        return False, "Identitas pelaksana tidak dikenali; konfirmasi diblokir."
    rep = get_report(cycle)
    if not rep or rep["status"] not in (data.R_MASUK, data.R_ULANG):
        if rep and rep["status"] in (data.R_KONFIRMASI, data.R_GM):
            return False, f"Laporan sudah dikonfirmasi oleh {rep['confirmed_by']} pada {rep['confirmed_at']}; tidak dikonfirmasi ganda."
        return False, "Konfirmasi diblokir: laporan belum berada pada tahap pemeriksaan Manajemen."
    if not checked:
        return False, "Centang pernyataan bahwa laporan gabungan sudah diperiksa sebelum mengonfirmasi."
    ts = now_str()
    rep["status"] = data.R_KONFIRMASI
    rep["checked_by"] = rep["confirmed_by"] = actor
    rep["checked_at"] = rep["confirmed_at"] = ts
    log(cycle, actor, f"Laporan diperiksa dan dikonfirmasi oleh {actor}", kind="Laporan")
    return True, f"Laporan dikonfirmasi oleh {actor}."


def return_report(cycle, actor, note):
    """Keputusan Perlu Perbaikan oleh Manajemen: catatan wajib, laporan kembali ke SPV; laporan dan data awal tidak dihapus."""
    if not _need_identity(actor):
        return False, "Identitas pelaksana tidak dikenali; pengembalian diblokir."
    note = (note or "").strip()
    rep = get_report(cycle)
    if not rep or rep["status"] not in (data.R_MASUK, data.R_ULANG):
        return False, "Pengembalian diblokir: laporan tidak sedang menunggu pemeriksaan Manajemen."
    if not note:
        return False, "Catatan Perbaikan untuk SPV wajib diisi."
    rep["status"] = data.R_PERBAIKAN
    rep["returns"].append({"by": actor, "at": now_str(), "note": note, "version": len(rep["versions"]), "response": None})
    log(cycle, actor, f"Laporan dikembalikan ke SPV oleh {actor} — catatan: {note}", kind="Laporan")
    return True, f"Laporan dikembalikan kepada SPV oleh {actor}."


def forward_to_gm(cycle, actor):
    """Satu kali per laporan. Identitas pelaksana pertama tidak pernah ditimpa."""
    if not _need_identity(actor):
        return False, "Identitas pelaksana tidak dikenali; penerusan diblokir."
    rep = get_report(cycle)
    if not rep:
        return False, "Laporan belum tersedia."
    if rep["status"] == data.R_GM:
        return False, f"Laporan sudah diteruskan ke {data.GM} oleh {rep['forwarded_by']} pada {rep['forwarded_at']}; tidak dapat diteruskan ulang."
    if rep["status"] != data.R_KONFIRMASI:
        return False, "Penerusan diblokir: laporan harus diperiksa dan dikonfirmasi Manajemen terlebih dahulu."
    ts = now_str()
    rep["status"] = data.R_GM
    rep["forwarded_at"] = rep["gm_received_at"] = ts
    rep["forwarded_by"] = actor
    log(cycle, actor, f"Laporan diteruskan ke {data.GM} oleh {actor}", kind="Laporan")
    log(cycle, f"{data.GM} (DEMO)", "Laporan diterima General Manager (DEMO) — representasi penerimaan akhir pada demonstrasi", kind="Laporan")
    return True, f"Laporan diteruskan ke {data.GM} oleh {actor}."


def reports_visible_to_management():
    """Hanya laporan yang sudah diteruskan SPV ke Manajemen yang terlihat oleh Manajemen."""
    return [r for r in st.session_state.reports.values() if r["status"] != data.R_GENERATED]


# ---------------------------------------------------------------- tabel ringkasan
def action_label(rec):
    """Tindakan yang sesuai kondisi tahapan (Monitoring SPV §6.3)."""
    if not rec:
        return "Hubungi Pekerja"
    return {
        data.S_MENUNGGU: "Periksa Laporan",
        data.S_ULANG: "Periksa Laporan",
        data.S_KONFIRMASI: "Lihat Detail",
        data.S_KEMBALI: "Lihat Catatan",
    }[rec["status"]]


def overview_df(cycle, actions=True):
    rows = []
    for no, name in data.STAGES:
        rec = get_record(cycle, no)
        wid = worker_for_stage(no)
        row = {
            "No": no,
            "Kode Tahapan": data.stage_code(no),
            "Nama Tahapan": name,
            "Pekerja Penanggung Jawab": worker_name(wid),
            "Status Input": input_status(rec),
            "Status Pemeriksaan SPV": rec["status"] if rec else "—",
            "Waktu Pengiriman": sent_text(rec),
        }
        if actions:
            row["Tindakan"] = action_label(rec)
        rows.append(row)
    return pd.DataFrame(rows)
