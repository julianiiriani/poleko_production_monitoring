"""Konstanta rujukan prototipe: 18 tahapan, peran per tingkatan, akun DEMO, batas tiap tahap, dan status UI.

Revisi pasca sidang (26 November 2026): mengikuti Aturan Main Sistem yang disetujui (Formulir Pengumpulan Data dan
Struktur Organisasi Bagian Produksi yang baru).
"""

# CONFIRMED (master prompt §3 dan Formulir Pengumpulan Data Ke-2, tabel B baris 4: "Shelling & Paring").
# Label BPMN menulis "Pairing"; selisih ini dilaporkan, bukan diubah di BPMN.
STAGES = [
    (1, "Opening (Penerimaan & Penimbangan)"),
    (2, "Sortiran Awal (Busuk & Layak)"),
    (3, "Bodega (Penyimpanan)"),
    (4, "Shelling & Paring"),
    (5, "Pencucian & Sortir Kedua"),
    (6, "Penyiraman & Penampungan"),
    (7, "Grinding"),
    (8, "Sterilisasi"),
    (9, "Drying"),
    (10, "Grading"),
    (11, "Picking"),
    (12, "Sampling & Quality Control"),
    (13, "Packing"),
    (14, "Weighting / Timbang"),
    (15, "Sealing & Sewing"),
    (16, "Bag Flattener"),
    (17, "Metal Detector"),
    (18, "Penyimpanan Produk Sebelum Pengiriman"),
]
STAGE_NAMES = dict(STAGES)
STAGE_NOS = [no for no, _ in STAGES]
OPENING_STAGE = 1  # satu-satunya tahapan dengan pilihan Waktu Kedatangan Bahan Baku


def stage_label(no):
    return f"{no:02d}. {STAGE_NAMES[no]}"


def stage_short(no):
    """Nama tahapan tanpa keterangan dalam kurung, mis. "Opening", "Sortiran Awal"."""
    return STAGE_NAMES[no].split(" (")[0]


def stage_code(no):
    return f"T{no:02d}"


# Tiga perspektif aplikasi. General Manager hanya penerima laporan.
ROLE_PEKERJA = "Pekerja Produksi"
ROLE_SPV = "Supervisor Produksi"
ROLE_MANAJER = "Manajemen"
ROLES = [ROLE_PEKERJA, ROLE_SPV, ROLE_MANAJER]
GM = "General Manager"

ROLE_COLOR = {ROLE_PEKERJA: "#0B2545", ROLE_SPV: "#6B3FA0", ROLE_MANAJER: "#D6A62A"}
ROLE_ON_COLOR = {ROLE_PEKERJA: "#FFFFFF", ROLE_SPV: "#FFFFFF", ROLE_MANAJER: "#1B2430"}

# ---- Shift (Formulir Pengumpulan Data bagian C1 dan C3: SPV tiap shift)
# nomor -> (nama shift, jam mulai, jam selesai, Supervisor). Shift III berjalan dari 23.00 sampai selesai (lewat tengah malam).
SHIFTS = {
    1: ("Shift I", "07:00", "15:00", "Supervisor I"),
    2: ("Shift II", "15:00", "23:00", "Supervisor II"),
    3: ("Shift III", "23:00", "07:00", "Supervisor III"),
}
SHIFT_NOS = list(SHIFTS)


def shift_name(n):
    return SHIFTS[n][0] if n in SHIFTS else "—"


def shift_label(n):
    return shift_name(n)


SPV_IDENTITIES = [SHIFTS[n][3] for n in SHIFT_NOS]
SPV_SHIFT = {SHIFTS[n][3]: n for n in SHIFT_NOS}

# ---- Manajemen per tingkatan (Struktur Organisasi baru, urutan kotak dari atas ke bawah)
PM = "Production Manager"
PPIC = "PPIC"
QA = "QA"
QC = "QC"
MANAGEMENT_IDENTITIES = [PM, PPIC, QA, QC]
MGMT_FULL = {
    PM: "Production Manager",
    PPIC: "Production Planning and Inventory Control (PPIC)",
    QA: "Quality Assurance (QA)",
    QC: "Quality Control (QC)",
}
LEVEL = {PM: "Top", PPIC: "Middle", QA: "Middle", QC: "Lower", **{s: "Lower" for s in SPV_IDENTITIES}}

# KONFIGURASI DEMO — penanggung jawab tahapan. Satu tahapan = satu akun pekerja (level Workers, termasuk Foreman).
# "Pekerja NN" hanya penanda akun demo, BUKAN nama pegawai POLEKO.
DEMO_WORKERS = {f"PKJ-{no:02d}": {"name": f"Pekerja {no:02d}", "stages": [no]} for no in STAGE_NOS}

# Akun login DEMO. Kolom password tidak diperiksa (bukan mekanisme autentikasi produksi).
DEMO_ACCOUNTS = {
    **{wid: {"label": f"{w['name']} — {stage_short(w['stages'][0])}", "role": ROLE_PEKERJA, "worker_id": wid} for wid, w in DEMO_WORKERS.items()},
    **{f"SPV-{n}": {"label": SHIFTS[n][3], "role": ROLE_SPV, "worker_id": None, "identity": SHIFTS[n][3], "shift": n} for n in SHIFT_NOS},
    **{f"MGR-{i}": {"label": name, "role": ROLE_MANAJER, "worker_id": None, "identity": name} for i, name in enumerate(MANAGEMENT_IDENTITIES, 1)},
}
# Kelompok pada halaman login (urutan tampil).
LOGIN_GROUPS = {role: [aid for aid, a in DEMO_ACCOUNTS.items() if a["role"] == role] for role in ROLES}

# Identitas siklus hanya dipakai internal (pengelompokan 18 laporan, pencegahan campur data, laporan gabungan); tidak ada menu atau
# dropdown siklus pada UI.
INTERNAL_CYCLE = "SIKLUS-001"

# Aturan akses prototipe (BUKAN kebijakan resmi perusahaan): pekerja boleh mengedit laporan yang dikirim maksimal 6 jam.
EDIT_WINDOW_HOURS = 6

# ---- Status pemeriksaan laporan tahapan (Pekerja <-> SPV)
S_BELUM = "Belum Dicatat"
S_MENUNGGU = "Menunggu Pemeriksaan Supervisor"
S_KEMBALI = "Perlu Perbaikan oleh Pekerja"
S_ULANG = "Menunggu Pemeriksaan Ulang Supervisor"
S_KONFIRMASI = "Dikonfirmasi Supervisor"
RECORD_STATUS_ORDER = [S_BELUM, S_MENUNGGU, S_KEMBALI, S_ULANG, S_KONFIRMASI]

# ---- Status penginputan (sisi pekerja)
IN_BELUM = S_BELUM
IN_KIRIM = "Sudah Dikirim ke Supervisor"
IN_DIPERBAIKI = "Sudah Diperbaiki"

# ---- Status tugas pemeriksaan kembali
T_OPEN = "Menunggu Pekerja"
T_RESENT = S_ULANG
T_DONE = "Selesai Ditinjau Supervisor"

# ---- Status laporan gabungan (per siklus; terpisah dari status laporan tahapan)
R_NONE = "Laporan Belum Dihasilkan"
R_SIAP = "Siap Dibuat Menjadi Laporan Gabungan"
R_GENERATED = "Laporan Gabungan Dihasilkan"
R_MASUK = "Menunggu Pemeriksaan Manajemen"
R_PERBAIKAN = "Perlu Perbaikan oleh Supervisor"
R_ULANG = "Menunggu Pemeriksaan Ulang Manajemen"
R_KONFIRMASI = "Dikonfirmasi Production Manager"
R_GM = "Diterima General Manager (DEMO)"
REPORT_STATUS_ORDER = [R_GENERATED, R_MASUK, R_PERBAIKAN, R_ULANG, R_KONFIRMASI, R_GM]
# Posisi pada alur: dihasilkan(0) -> diteruskan ke Manajemen(1) -> dikonfirmasi(2) -> diterima GM DEMO(3)
REPORT_STEP = {R_GENERATED: 0, R_MASUK: 1, R_PERBAIKAN: 1, R_ULANG: 1, R_KONFIRMASI: 2, R_GM: 3}

# ---- Status ringkas siklus (dihitung, bukan disimpan) untuk Dashboard SPV
C_MENUNGGU_INPUT = "Menunggu Input Pekerja"
C_MENUNGGU_SPV = S_MENUNGGU
C_PERBAIKAN = "Perlu Perbaikan"
C_ULANG = "Proses Pemeriksaan Ulang"

# Keputusan Manajemen
D_DITERIMA = "Laporan Diterima"
D_PERBAIKAN = "Perlu Perbaikan"

# Warna semantik status (terpisah dari warna identitas peran). Status selalu disertai label teks.
_GREY, _AMBER, _RED, _BLUE, _GREEN, _TEAL = (
    ("#475569", "#F1F5F9"), ("#B45309", "#FEF3C7"), ("#B91C1C", "#FEE2E2"),
    ("#1D4ED8", "#DBEAFE"), ("#15803D", "#DCFCE7"), ("#0F766E", "#CCFBF1"),
)
STATUS_STYLE = {
    S_BELUM: _GREY,
    S_MENUNGGU: _AMBER,
    S_KEMBALI: _RED,
    S_ULANG: _BLUE,
    S_KONFIRMASI: _GREEN,
    IN_KIRIM: _AMBER,
    IN_DIPERBAIKI: _BLUE,
    T_OPEN: _RED,
    T_DONE: _GREEN,
    R_NONE: _GREY,
    R_SIAP: _TEAL,
    R_GENERATED: _AMBER,
    R_MASUK: _BLUE,
    R_PERBAIKAN: _RED,
    R_ULANG: _BLUE,
    R_KONFIRMASI: _TEAL,
    R_GM: _GREEN,
    C_MENUNGGU_INPUT: _GREY,
    C_PERBAIKAN: _RED,
    C_ULANG: _BLUE,
    D_DITERIMA: _GREEN,
}


# ---- Field input. Durasi tidak diminta dari pekerja (dihitung otomatis dari waktu mulai/selesai).
PELAKSANA_OPTIONS = ["Operator", "SPV", "QC", "Foreman"]  # Foreman berada pada level Workers
KONDISI_NORMAL = "Normal"
KONDISI_SERING = "Sering Ada Kendala"
KONDISI_TIDAK = "Tidak Dilakukan"
KONDISI_OPTIONS = [KONDISI_NORMAL, "Kadang Ada Kendala", KONDISI_SERING, KONDISI_TIDAK]  # empat pilihan petunjuk formulir
ARRIVAL_PAGI = "07.00–08.00 — Pagi"
OPENING_ARRIVAL_OPTIONS = [ARRIVAL_PAGI]  # kedatangan kelapa hanya pagi (Formulir bagian B tahap 1)

# ---- Batas setiap tahap (Formulir Pengumpulan Data bagian B, basis 10 ton).
# no -> (jam mulai, jam selesai/batas, durasi standar dalam menit, pemantau). Jam berlaku untuk Shift I (shift pagi yang diisi narasumber);
# Shift II dan III hanya diperiksa durasinya. Tahap 3 berlangsung 24 jam (selesai pukul 08.00 hari berikutnya).
STAGE_STANDARD = {
    1: ("07:00", "08:00", 60, "Timbangan"),
    2: ("07:15", "07:45", 30, "Bodega SPV"),
    3: ("08:00", "08:00", 1440, "SPV bodega"),
    4: ("07:00", "08:00", 60, "SPV dan Foreman"),
    5: ("08:00", "08:15", 15, "Picker Washing"),
    6: ("08:15", "08:25", 10, "Operator Winder"),
    7: ("08:25", "09:25", 60, "SPV dan Foreman tiap shift"),
    8: ("09:25", "09:35", 10, "Senior LAB"),
    9: ("09:35", "10:30", 55, "Operator dryer"),
    10: ("10:30", "10:40", 10, "Pikers Dryer"),
    11: ("10:40", "11:00", 20, "Personil warehouse"),
    12: ("11:00", "11:10", 10, "Senior Lab dan Sampler"),
    13: ("11:10", "11:20", 10, "Packing"),
    14: ("11:20", "11:30", 10, "(tidak diisi pada formulir)"),
    15: ("11:30", "11:40", 10, "Packing"),
    16: ("11:40", "11:50", 10, "Packing"),
    17: ("11:50", "12:00", 10, "Checker"),
    18: (None, None, None, "SPV Warehouse"),
}
STORAGE_STAGE = 18
STORAGE_DAYS = (1, 5)  # tahap 18: 1–5 hari
QUALITY_STAGES = (8, 12, 18)  # tahap yang melibatkan lab (Senior Lab, Sampler, hasil lab/inkubasi)
KG_MAX = 10000.0  # basis 10 ton pada Formulir bagian B
TOLERANCE_MIN = 0  # toleransi Under/Over: 0 (harus sama dengan batas formulir)

# ---- Tingkat risiko dan pengarahan (Aturan Main bagian 5)
LV_HIJAU = "Hijau — Sesuai Batas"
LV_KUNING = "Kuning — Di Luar Batas"
LV_MERAH = "Merah — Risiko Tinggi"
LEVEL_ORDER = [LV_HIJAU, LV_KUNING, LV_MERAH]
RT_PPIC = "PPIC"  # waktu/durasi/kg di luar batas
RT_PM = "Production Manager"  # kendala atau kerusakan mesin
RT_QC = "QC"  # mutu: tahap 8, 12, 18 (lalu QA)
RT_QA = "QA"
F_MENUNGGU = "Menunggu Tanggapan"
F_DITANGGAPI = "Sudah Ditanggapi"
F_KE_QA = "Diteruskan QC ke QA"
F_DIPUTUSKAN = "Diputuskan QA"
QA_DECISIONS = ["Mutu Diterima", "Perlu Tindakan Produksi"]

DEMO_MODE_LABEL = "Mode demonstrasi · data hanya di sesi ini"
DEMO_VALIDATION_LABEL = "Validasi mengikuti batas Formulir Pengumpulan Data (Aturan Main Sistem)"

STATUS_STYLE.update({
    LV_HIJAU: _GREEN, LV_KUNING: _AMBER, LV_MERAH: _RED,
    F_MENUNGGU: _AMBER, F_DITANGGAPI: _GREEN, F_KE_QA: _BLUE, F_DIPUTUSKAN: _GREEN,
})
