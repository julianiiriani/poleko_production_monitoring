"""Konstanta rujukan prototipe: 18 tahapan, tiga peran, profil pekerja DEMO, dan status UI."""

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


def stage_label(no):
    return f"{no:02d}. {STAGE_NAMES[no]}"


# Tiga perspektif aplikasi (bukan hak akses produksi). General Manager hanya penerima laporan.
ROLE_PEKERJA = "Pekerja Produksi"
ROLE_SPV = "SPV Produksi"
ROLE_MANAJER = "Manajemen"
ROLES = [ROLE_PEKERJA, ROLE_SPV, ROLE_MANAJER]
GM = "General Manager"

ROLE_COLOR = {ROLE_PEKERJA: "#0B2545", ROLE_SPV: "#6B3FA0", ROLE_MANAJER: "#D6A62A"}
ROLE_ON_COLOR = {ROLE_PEKERJA: "#FFFFFF", ROLE_SPV: "#FFFFFF", ROLE_MANAJER: "#1B2430"}

# KONFIGURASI DEMO — penanggung jawab tahapan.
# Satu tahapan = satu pekerja (konfirmasi tim peneliti). Nama "Pekerja DEMO NN" hanya placeholder, BUKAN nama pegawai
# POLEKO. Seluruh aplikasi membaca dari sini, jadi cukup diganti di satu tempat setelah penugasan resmi dikonfirmasi.
# Mengubahnya tidak mengubah daftar 18 tahapan.
DEMO_WORKERS = {f"PKJ-DEMO-{no:02d}": {"name": f"Pekerja DEMO {no:02d}", "stages": [no]} for no in STAGE_NOS}
DEMO_SPV = "SPV Produksi DEMO"
# Identitas dalam perspektif Manajemen; yang dipilih saat login dicatat sebagai pelaksana konfirmasi dan penerusan.
MANAGEMENT_IDENTITIES = ["Manager Produksi", "PPIC", "QC", "QA"]

# Akun login DEMO. Isi password belum ditentukan, jadi kolom password boleh dikosongkan dan tidak diperiksa.
# Ini bukan mekanisme autentikasi produksi.
DEMO_ACCOUNTS = {
    **{wid: {"label": w["name"], "role": ROLE_PEKERJA, "worker_id": wid} for wid, w in DEMO_WORKERS.items()},
    "SPV": {"label": DEMO_SPV, "role": ROLE_SPV, "worker_id": None},
    **{f"MGR-{i}": {"label": name, "role": ROLE_MANAJER, "worker_id": None} for i, name in enumerate(MANAGEMENT_IDENTITIES, 1)},
}

# ID siklus hanya placeholder demonstrasi.
DEMO_CYCLES = ["DEMO-SIKLUS-001", "DEMO-SIKLUS-002", "DEMO-SIKLUS-003"]

# Status catatan tahapan (Pekerja -> SPV).
S_BELUM = "Belum Dicatat"
S_TERKIRIM = "Menunggu Validasi SPV"
S_KEMBALI = "Perlu Perbaikan"
S_KIRIM_ULANG = "Sudah Diperbaiki — Menunggu SPV"
S_LAPORAN = "Termasuk Laporan Gabungan"
RECORD_STATUS_ORDER = [S_BELUM, S_TERKIRIM, S_KEMBALI, S_KIRIM_ULANG, S_LAPORAN]

# Status tugas pemeriksaan kembali.
T_OPEN = "Menunggu Pekerja"
T_RESENT = S_KIRIM_ULANG
T_DONE = "Selesai Ditinjau SPV"

# Status laporan gabungan per siklus (terpisah dari status catatan tahapan).
R_NONE = "Laporan Belum Dihasilkan"
R_GENERATED = "Laporan Gabungan Dihasilkan — Menunggu Diteruskan ke PPIC"
R_MASUK = "Laporan Masuk — Menunggu Pemeriksaan dan Konfirmasi"
R_KONFIRMASI = "Terkonfirmasi — Menunggu Diteruskan ke General Manager"
R_GM = "Diteruskan ke General Manager (DEMO)"
REPORT_STATUS_ORDER = [R_GENERATED, R_MASUK, R_KONFIRMASI, R_GM]
REPORT_RANK = {s: i for i, s in enumerate(REPORT_STATUS_ORDER)}

# Keputusan validasi SPV (satu keputusan per siklus produksi).
V_DITERIMA = "Laporan Diterima"
V_PERBAIKAN = "Perlu Perbaikan"

# Warna semantik status (terpisah dari warna identitas peran). Status selalu disertai label teks.
STATUS_STYLE = {
    S_BELUM: ("#475569", "#F1F5F9"),
    S_TERKIRIM: ("#B45309", "#FEF3C7"),
    S_KEMBALI: ("#B91C1C", "#FEE2E2"),
    S_KIRIM_ULANG: ("#1D4ED8", "#DBEAFE"),
    S_LAPORAN: ("#15803D", "#DCFCE7"),
    T_OPEN: ("#B91C1C", "#FEE2E2"),
    T_DONE: ("#15803D", "#DCFCE7"),
    R_NONE: ("#475569", "#F1F5F9"),
    R_GENERATED: ("#B45309", "#FEF3C7"),
    R_MASUK: ("#1D4ED8", "#DBEAFE"),
    R_KONFIRMASI: ("#0F766E", "#CCFBF1"),
    R_GM: ("#15803D", "#DCFCE7"),
    V_DITERIMA: ("#15803D", "#DCFCE7"),
}  # V_PERBAIKAN sama dengan S_KEMBALI ("Perlu Perbaikan"), jadi gayanya otomatis sama.

# Field input mengikuti Formulir Pengumpulan Data Ke-2, bagian B (tabel waktu proses produksi) dan petunjuk pengisian.
# Pengecualian: "Jumlah Produksi (kg)" ditambahkan atas instruksi revisi master prompt (tidak ada di formulir tersebut).
KONDISI_OPTIONS = [
    "Normal",
    "Sering mengalami kendala/keterlambatan",
    "Kadang mengalami kendala/keterlambatan",
    "Tidak terjadi / tidak dilakukan",
]
MONITORING_OPTIONS = ["Ada monitoring/pencatatan", "Tidak ada monitoring/pencatatan", "Tidak tahu"]
DURASI_UNITS = ["menit", "jam"]

DEMO_MODE_LABEL = "Mode demonstrasi · data hanya di sesi ini"
DEMO_VALIDATION_LABEL = "Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO"

# Skenario Kontrol Demo (label sesuai master prompt).
SC_LENGKAP = "Siklus Lengkap — Siap Divalidasi SPV"
SC_BELUM = "Siklus Belum Lengkap — 15 dari 18 Tahapan"
SC_MASUK = "Laporan Sudah Masuk ke Manajemen"
SC_SEMUA = "Semua Skenario"
DEMO_SCENARIOS = [SC_LENGKAP, SC_BELUM, SC_MASUK, SC_SEMUA]
