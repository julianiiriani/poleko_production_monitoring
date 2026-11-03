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
ROLE_PEKERJA = "Pekerja / Pelaksana Produksi"
ROLE_SPV = "SPV Produksi"
ROLE_MANAJER = "Manajer Produksi / PPIC / QC / QA"
ROLES = [ROLE_PEKERJA, ROLE_SPV, ROLE_MANAJER]
GM = "General Manager"

ROLE_COLOR = {ROLE_PEKERJA: "#0B2545", ROLE_SPV: "#6B3FA0", ROLE_MANAJER: "#D6A62A"}
ROLE_ON_COLOR = {ROLE_PEKERJA: "#FFFFFF", ROLE_SPV: "#FFFFFF", ROLE_MANAJER: "#1B2430"}
ROLE_ROLE_NAME = {ROLE_PEKERJA: "Navy", ROLE_SPV: "Purple", ROLE_MANAJER: "Gold"}

# KONFIGURASI DEMO: profil dan penugasan di bawah ini bukan nama pegawai atau penugasan nyata POLEKO.
# Ganti isi dict ini setelah penugasan resmi dikonfirmasi; seluruh aplikasi membaca dari sini.
DEMO_WORKERS = {
    "PKJ-DEMO-1": {"name": "Pekerja DEMO 1", "stages": [1, 2, 3]},
    "PKJ-DEMO-2": {"name": "Pekerja DEMO 2", "stages": [4, 5, 6]},
    "PKJ-DEMO-3": {"name": "Pekerja DEMO 3", "stages": [7, 8, 9]},
    "PKJ-DEMO-4": {"name": "Pekerja DEMO 4", "stages": [10, 11, 12]},
    "PKJ-DEMO-5": {"name": "Pekerja DEMO 5", "stages": [13, 14, 15]},
    "PKJ-DEMO-6": {"name": "Pekerja DEMO 6", "stages": [16, 17, 18]},
}
DEMO_SPV = "SPV Produksi DEMO"
DEMO_MANAJER = "Manajer/PPIC/QC/QA DEMO"

# ID siklus hanya placeholder demonstrasi.
DEMO_CYCLES = ["DEMO-SIKLUS-001", "DEMO-SIKLUS-002", "DEMO-SIKLUS-003"]

# Status catatan tahapan (Pekerja -> SPV).
S_BELUM = "Belum Dicatat"
S_TERKIRIM = "Menunggu Validasi SPV"
S_KEMBALI = "Perlu Pemeriksaan Kembali"
S_KIRIM_ULANG = "Dikirim Ulang — Menunggu Tinjauan SPV"
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

V_TRUE = "TRUE — Tervalidasi"
V_FALSE = "FALSE — Tidak Tervalidasi"

# Warna semantik status (terpisah dari warna identitas peran).
STATUS_STYLE = {
    S_BELUM: ("#64748B", "#F1F5F9"),
    S_TERKIRIM: ("#B45309", "#FEF3C7"),
    S_KEMBALI: ("#B91C1C", "#FEE2E2"),
    S_KIRIM_ULANG: ("#1D4ED8", "#DBEAFE"),
    S_LAPORAN: ("#15803D", "#DCFCE7"),
    T_OPEN: ("#B91C1C", "#FEE2E2"),
    T_DONE: ("#15803D", "#DCFCE7"),
    R_NONE: ("#64748B", "#F1F5F9"),
    R_GENERATED: ("#B45309", "#FEF3C7"),
    R_MASUK: ("#1D4ED8", "#DBEAFE"),
    R_KONFIRMASI: ("#0F766E", "#CCFBF1"),
    R_GM: ("#15803D", "#DCFCE7"),
    V_TRUE: ("#15803D", "#DCFCE7"),
    V_FALSE: ("#B91C1C", "#FEE2E2"),
}

# Field input mengikuti Formulir Pengumpulan Data Ke-2, bagian B (tabel waktu proses produksi) dan petunjuk pengisian.
KONDISI_OPTIONS = [
    "Normal",
    "Sering mengalami kendala/keterlambatan",
    "Kadang mengalami kendala/keterlambatan",
    "Tidak terjadi / tidak dilakukan",
]
MONITORING_OPTIONS = ["Ada monitoring/pencatatan", "Tidak ada monitoring/pencatatan", "Tidak tahu"]
DURASI_UNITS = ["menit", "jam"]
FIELD_EXAMPLE_PELAKSANA = "Contoh pada formulir: Operator, SPV, Foreman, QC."

PROTOTYPE_BADGE = "Mode Demonstrasi"
DEMO_NOTICE = "Data DEMO — tersimpan sementara di sesi ini, bukan di database"
DEMO_VALIDATION_LABEL = "Validasi Demonstrasi — Bukan Ketentuan Resmi POLEKO"
STORE_LABEL = "Penyimpanan Terpusat — Simulasi Prototype, Database Belum Terhubung"
STORE_NAME = "Data Aktivitas Proses Produksi"

SESSION_NOTE = (
    "Data DEMO hanya disimpan di sesi Streamlit ini, bukan di database permanen. Data tidak dibagikan antar "
    "pengguna atau perangkat dan dapat hilang saat browser di-refresh atau sesi berakhir. Reset DEMO menghapus "
    "data sementara secara eksplisit; Keluar tidak menghapusnya."
)
REALTIME_NOTE = (
    "\"Real-time\" di prototipe ini hanya berarti tampilan ikut berubah dalam sesi demo ini setelah sebuah "
    "catatan atau aksi dikirim. Tidak ada sinkronisasi antar pengguna atau perangkat."
)
