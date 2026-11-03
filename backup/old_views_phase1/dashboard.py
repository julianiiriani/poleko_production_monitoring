import streamlit as st

from core import data, state, ui

ui.page_header(
    "Dashboard",
    "Ringkasan monitoring 18 tahapan produksi pada proses To-Be.",
    data.PAGE_ACTORS["dashboard"],
)

role = st.session_state.role
cycle = state.active_cycle()
counts = state.status_counts(cycle)
queue_total, queue_new, queue_resent = state.queue_breakdown(cycle)

# --- Siklus produksi -------------------------------------------------------
st.subheader("Siklus Produksi")
c1, c2, c3 = st.columns(3)
with c1:
    ui.info_card("ID Siklus", cycle or "Belum ditetapkan", "Placeholder — ID siklus final belum ditentukan", pending=cycle is None)
with c2:
    ui.info_card("Periode Produksi", "Belum ditetapkan", "Placeholder", pending=True)
with c3:
    ui.info_card("Sumber Data", "Sesi DEMO" if cycle else "Tidak ada data", data.DEMO_NOTICE, pending=cycle is None)

# --- Alur To-Be ------------------------------------------------------------
st.subheader("Alur Monitoring To-Be")
ui.flow(
    [
        ("Menjalankan 18 tahapan produksi", data.ROLE_PEKERJA, False),
        ("Input laporan monitoring per tahapan", data.ROLE_SPV, False),
        ("Data Aktivitas Proses Produksi (penyimpanan terpusat, visual)", "Data store", True),
        ("Memantau pencatatan dan aktivitas produksi (real-time, visual)", data.ROLE_MANAJER, False),
        ("Validasi laporan; tidak sesuai → pemeriksaan kembali, sesuai → teruskan ke PPIC", data.ROLE_SPV, False),
        ("Memeriksa kembali dan konfirmasi laporan", data.ROLE_MANAJER, False),
    ]
)
st.caption(data.REALTIME_NOTE)

# --- Panel perspektif ------------------------------------------------------
if role == data.ROLE_SPV:
    st.subheader("Tugas SPV Produksi")
    a, b, c, d = st.columns(4)
    with a:
        ui.action_card("Input laporan", f"{counts[data.S_BELUM]} tahapan", "Belum dicatat", "views/input_monitoring.py", "Input Monitoring", ":material/edit_note:")
    with b:
        ui.action_card(data.QUEUE_LABEL, f"{queue_total} tahapan", "Perlu divalidasi", "views/validasi.py", "Validasi Laporan", ":material/fact_check:")
    with c:
        ui.action_card("Pemeriksaan kembali", f"{counts[data.S_KEMBALI]} tahapan", "Dikembalikan ke penginput", "views/pemeriksaan_kembali.py", "Periksa Kembali", ":material/undo:")
    with d:
        ui.action_card("Diteruskan ke PPIC", f"{counts[data.S_KONFIRMASI]} tahapan", "Menunggu konfirmasi", "views/konfirmasi.py", "Lihat Konfirmasi", ":material/task_alt:")
elif role == data.ROLE_MANAJER:
    recorded = 18 - counts[data.S_BELUM]
    st.subheader("Pemantauan Menyeluruh dan Konfirmasi")
    a, b, c = st.columns(3)
    with a:
        ui.action_card("Tahapan tercatat", f"{recorded} / 18", "Visibilitas pencatatan SPV", "views/monitoring.py", "Monitoring Aktivitas", ":material/monitoring:")
    with b:
        ui.action_card("Menunggu konfirmasi", f"{counts[data.S_KONFIRMASI]} tahapan", "Sudah diteruskan ke PPIC", "views/konfirmasi.py", "Konfirmasi Laporan", ":material/task_alt:")
    with c:
        ui.action_card("Selesai dikonfirmasi", f"{counts[data.S_SELESAI]} / 18", "Laporan terkonfirmasi", "views/konfirmasi.py", "Ringkasan Laporan", ":material/fact_check:")
else:
    st.subheader("Perspektif Pekerja / Pelaksana Produksi")
    st.info(
        "Anda menjalankan 18 tahapan produksi sesuai urutan. Pada BPMN To-Be, laporan monitoring "
        "per tahapan diinput oleh SPV Produksi; status di bawah hanya untuk visibilitas operasional."
    )

# --- Tahapan ---------------------------------------------------------------
st.subheader("Urutan Tahapan Produksi" if role == data.ROLE_PEKERJA else "Ringkasan Status 18 Tahapan")
ui.status_summary(counts)
st.caption(
    f"Total keenam status selalu 18 tahapan. {data.QUEUE_LABEL} = {data.QUEUE_DEFINITION} "
    "(tahapan yang menunggu validasi)."
)
ui.stage_grid(cycle)
if cycle is None:
    st.write("")
    ui.empty_state(
        "Belum ada catatan monitoring",
        "Semua tahapan berstatus Belum Dicatat. Isi satu tahapan di Input Monitoring Produksi, atau muat 18 data DEMO dari sidebar.",
    )

# --- Status laporan (tidak untuk perspektif Pekerja) -----------------------
if role != data.ROLE_PEKERJA:
    st.subheader("Status Laporan")
    r1, r2, r3 = st.columns(3)
    with r1:
        ui.info_card(
            data.QUEUE_LABEL,
            f"{queue_total} tahapan" if queue_total else "Tidak ada",
            f"{queue_new} Sudah Dicatat + {queue_resent} Menunggu Pemeriksaan" if queue_total else "Kosong",
            pending=not queue_total,
        )
    with r2:
        n = counts[data.S_KEMBALI]
        ui.info_card("Perlu Pemeriksaan Kembali", f"{n} tahapan" if n else "Tidak ada", "Dikembalikan ke pihak penginput" if n else "Kosong", pending=not n)
    with r3:
        n = counts[data.S_KONFIRMASI]
        ui.info_card("Menunggu Konfirmasi", f"{n} tahapan" if n else "Tidak ada", "Sudah diteruskan ke PPIC" if n else "Kosong", pending=not n)

# --- Time efficiency -------------------------------------------------------
st.subheader("KPI Utama")
st.markdown(
    '<div class="pk-kpi"><div class="pk-kpi-title">Time Efficiency</div>'
    '<div class="pk-kpi-value">Belum Dihitung</div>'
    '<div class="pk-kpi-note">Parameter simulasi ARENA dan hasil pengukuran yang valid belum tersedia, '
    "sehingga tidak ada angka yang ditampilkan.</div></div>",
    unsafe_allow_html=True,
)
st.write("")
ui.session_expander()
