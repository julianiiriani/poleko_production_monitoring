"""Konstanta rujukan prototipe: 18 tahapan, tiga peran, akun DEMO, dan status UI (Revisi 03 November 2026)."""

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


# Tiga perspektif aplikasi (bukan hak akses produksi). General Manager hanya penerima laporan.
ROLE_PEKERJA = "Pekerja Produksi"
ROLE_SPV = "SPV Produksi"
ROLE_MANAJER = "Manajemen"
ROLES = [ROLE_PEKERJA, ROLE_SPV, ROLE_MANAJER]
GM = "General Manager"

ROLE_COLOR = {ROLE_PEKERJA: "#0B2545", ROLE_SPV: "#6B3FA0", ROLE_MANAJER: "#D6A62A"}
ROLE_ON_COLOR = {ROLE_PEKERJA: "#FFFFFF", ROLE_SPV: "#FFFFFF", ROLE_MANAJER: "#1B2430"}

# KONFIGURASI DEMO — penanggung jawab tahapan.
# Satu tahapan = satu pekerja (konfirmasi tim peneliti). "Pekerja NN" hanya penanda akun demo, BUKAN nama pegawai POLEKO.
# Seluruh aplikasi membaca dari sini, jadi cukup diganti di satu tempat setelah penugasan resmi dikonfirmasi.
DEMO_WORKERS = {f"PKJ-{no:02d}": {"name": f"Pekerja {no:02d}", "stages": [no]} for no in STAGE_NOS}
DEMO_SPV = "SPV Produksi"
# Identitas dalam perspektif Manajemen; yang dipilih saat login dicatat sebagai pelaksana pemeriksaan, konfirmasi, dan penerusan.
MANAGEMENT_IDENTITIES = ["Manager Produksi", "PPIC", "QC", "QA"]

# Akun login DEMO. Isi password belum ditentukan, jadi kolom password boleh dikosongkan dan tidak diperiksa.
# Ini bukan mekanisme autentikasi produksi.
DEMO_ACCOUNTS = {
    **{wid: {"label": f"{w['name']} — {stage_short(w['stages'][0])}", "role": ROLE_PEKERJA, "worker_id": wid} for wid, w in DEMO_WORKERS.items()},
    "SPV": {"label": DEMO_SPV, "role": ROLE_SPV, "worker_id": None},
    **{f"MGR-{i}": {"label": name, "role": ROLE_MANAJER, "worker_id": None} for i, name in enumerate(MANAGEMENT_IDENTITIES, 1)},
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
S_MENUNGGU = "Menunggu Pemeriksaan SPV"
S_KEMBALI = "Perlu Perbaikan oleh Pekerja"
S_ULANG = "Menunggu Pemeriksaan Ulang SPV"
S_KONFIRMASI = "Dikonfirmasi SPV"
RECORD_STATUS_ORDER = [S_BELUM, S_MENUNGGU, S_KEMBALI, S_ULANG, S_KONFIRMASI]

# ---- Status penginputan (sisi pekerja)
IN_BELUM = S_BELUM
IN_KIRIM = "Sudah Dikirim ke SPV"
IN_DIPERBAIKI = "Sudah Diperbaiki"

# ---- Status tugas pemeriksaan kembali
T_OPEN = "Menunggu Pekerja"
T_RESENT = S_ULANG
T_DONE = "Selesai Ditinjau SPV"

# ---- Status laporan gabungan (per siklus; terpisah dari status laporan tahapan)
R_NONE = "Laporan Belum Dihasilkan"
R_SIAP = "Siap Dibuat Menjadi Laporan Gabungan"
R_GENERATED = "Laporan Gabungan Dihasilkan"
R_MASUK = "Menunggu Pemeriksaan Manajemen"
R_PERBAIKAN = "Perlu Perbaikan oleh SPV"
R_ULANG = "Menunggu Pemeriksaan Ulang Manajemen"
R_KONFIRMASI = "Dikonfirmasi Manajemen"
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

# Field input (Revisi 03 November 2026 §5.3). Durasi tidak diminta dari pekerja (dihitung otomatis dari waktu mulai/selesai).
PELAKSANA_OPTIONS = ["Operator", "SPV", "QC", "Foreman"]
KONDISI_NORMAL = "Normal"
KONDISI_OPTIONS = [KONDISI_NORMAL, "Sering Ada Kendala", "Kadang Ada Kendala"]
OPENING_ARRIVAL_OPTIONS = ["07.00 — Pagi", "18.00 — Sore"]

DEMO_MODE_LABEL = "Mode demonstrasi · data hanya di sesi ini"
DEMO_VALIDATION_LABEL = "Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO"
