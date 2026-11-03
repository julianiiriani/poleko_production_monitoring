"""Komponen tampilan bersama agar seluruh halaman terasa sebagai satu sistem."""
import html

import streamlit as st

from core import data, state

NAVY = "#0B2545"

CSS = f"""
<style>
.block-container {{ padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1280px; }}
[data-testid="stSidebar"] {{ background: #F5F7FA; border-right: 1px solid #DCE3EC; }}
h1, h2, h3, h4, h5 {{ color: {NAVY}; letter-spacing: -0.01em; }}
[data-testid="stSidebarNavLink"][aria-current="page"] {{
  background: color-mix(in srgb, var(--accent) 14%, white); border-left: 4px solid var(--accent); font-weight: 600; }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {{
  background: var(--accent); border-color: var(--accent); color: var(--on-accent); }}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {{
  filter: brightness(.92); border-color: var(--accent); color: var(--on-accent); }}
.stButton > button[kind="primary"]:disabled {{ background: #CBD5E1; border-color: #CBD5E1; color: #64748B; }}

@media (max-width: 900px) {{ .block-container {{ padding-top: 3.6rem; }} }}
.pk-hero {{ background: #fff; border: 1px solid #DCE3EC; border-left: 7px solid var(--accent, {NAVY});
  border-radius: 10px; padding: 14px 22px; margin-bottom: 14px; }}
.pk-hero .pk-eyebrow {{ font-size: .7rem; letter-spacing: .12em; text-transform: uppercase; color: #64748B; }}
.pk-hero h1 {{ color: {NAVY}; font-size: 1.5rem; margin: 2px 0 2px 0; padding: 0; }}
.pk-hero .pk-sub {{ color: #475569; font-size: .9rem; }}
.pk-chips {{ margin-top: 8px; display: flex; flex-wrap: wrap; gap: 6px; }}
.pk-chip {{ font-size: .72rem; padding: 3px 10px; border-radius: 999px; background: #EEF2F7; color: #334155; border: 1px solid #DCE3EC; }}
.pk-chip.warn {{ background: #FEF3C7; color: #92400E; border-color: #F5D58A; }}
.pk-chip.role {{ background: var(--accent); color: var(--on-accent); border-color: transparent; font-weight: 600; }}

.pk-card {{ background: #fff; border: 1px solid #DCE3EC; border-radius: 10px; padding: 14px 16px; height: 100%; }}
.pk-card .pk-label {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: #64748B; }}
.pk-card .pk-value {{ font-size: 1.2rem; font-weight: 700; color: {NAVY}; margin-top: 2px; }}
.pk-card .pk-note {{ font-size: .8rem; color: #64748B; margin-top: 4px; }}
.pk-card.pending {{ border-style: dashed; background: #FAFBFD; }}
.pk-card.accent {{ border-top: 4px solid var(--accent, {NAVY}); }}

.pk-kpi {{ border: 1px solid #DCE3EC; border-left: 6px solid #94A3B8; border-radius: 10px; padding: 14px 20px; background: #FAFBFD; }}
.pk-kpi .pk-kpi-title {{ font-size: .74rem; letter-spacing: .12em; color: #64748B; text-transform: uppercase; }}
.pk-kpi .pk-kpi-value {{ font-size: 1.5rem; font-weight: 800; color: {NAVY}; }}
.pk-kpi .pk-kpi-note {{ color: #475569; font-size: .84rem; }}
.pk-formula {{ border: 1px solid #DCE3EC; background: #F8FAFC; border-radius: 10px; padding: 14px 20px; text-align: center;
  font-size: 1.1rem; font-weight: 600; color: {NAVY}; line-height: 1.6; overflow-wrap: anywhere; }}

.pk-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 10px; }}
.pk-stage {{ background: #fff; border: 1px solid #DCE3EC; border-left: 5px solid #64748B; border-radius: 8px;
  padding: 10px 12px; display: flex; flex-direction: column; gap: 6px; min-height: 104px; }}
.pk-stage-no {{ font-size: .7rem; font-weight: 700; color: #94A3B8; letter-spacing: .06em; }}
.pk-stage-name {{ font-size: .86rem; font-weight: 600; color: #1B2430; line-height: 1.25; flex: 1; }}
.pk-stage-sub {{ font-size: .7rem; color: #64748B; }}
.pk-badge {{ display: inline-block; align-self: flex-start; font-size: .68rem; font-weight: 600;
  padding: 2px 8px; border-radius: 999px; border: 1px solid; line-height: 1.35; }}

.pk-statgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin-bottom: 8px; }}
.pk-stat {{ background: #fff; border: 1px solid #DCE3EC; border-top: 4px solid #64748B; border-radius: 10px;
  padding: 12px 14px; min-height: 104px; display: flex; flex-direction: column; justify-content: space-between; }}
.pk-stat .pk-label {{ font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; color: #64748B; line-height: 1.3; }}
.pk-stat .pk-value {{ font-size: 1.5rem; font-weight: 700; color: {NAVY}; }}
.pk-stat .pk-value small {{ font-size: .8rem; color: #94A3B8; font-weight: 500; }}

.pk-empty {{ border: 1.5px dashed #C3CEDC; border-radius: 10px; padding: 24px; text-align: center; color: #64748B; background: #FAFBFD; }}
.pk-empty b {{ color: {NAVY}; display: block; margin-bottom: 4px; font-size: 1rem; }}

.pk-store {{ border: 1px solid #DCE3EC; border-left: 5px solid #94A3B8; border-radius: 10px; background: #F8FAFC; padding: 10px 16px; }}
.pk-store .t {{ font-weight: 700; color: {NAVY}; font-size: .86rem; }}
.pk-store .s {{ font-size: .8rem; color: #475569; }}

.pk-steps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin: 4px 0 10px 0; }}
.pk-st {{ border: 1px solid #DCE3EC; border-top: 4px solid #CBD5E1; border-radius: 8px; padding: 8px 10px; background: #fff;
  font-size: .76rem; color: #64748B; line-height: 1.3; }}
.pk-st.done {{ border-top-color: #15803D; color: #166534; background: #F3FBF6; }}
.pk-st.now {{ border-top-color: var(--accent); color: {NAVY}; font-weight: 700; box-shadow: 0 0 0 2px var(--accent); }}

.pk-fields {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 6px 18px; margin: 6px 0; }}
.pk-f .l {{ font-size: .68rem; text-transform: uppercase; letter-spacing: .06em; color: #64748B; }}
.pk-f .v {{ font-size: .88rem; color: #1B2430; overflow-wrap: anywhere; }}
.pk-f .v.na {{ color: #94A3B8; font-style: italic; }}

.pk-report {{ border: 1px solid #DCE3EC; border-radius: 10px; background: #fff; padding: 14px 16px; }}
.pk-report .head {{ border-bottom: 2px solid var(--accent); padding-bottom: 8px; margin-bottom: 10px; }}
.pk-report .head b {{ color: {NAVY}; font-size: 1rem; }}
.pk-report .head span {{ display: block; font-size: .78rem; color: #475569; }}
.pk-rep-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }}
.pk-rep-stage {{ border: 1px solid #E3E8EF; border-radius: 8px; padding: 10px 12px; background: #FBFCFE; }}
.pk-rep-stage .h {{ font-weight: 700; color: {NAVY}; font-size: .86rem; margin-bottom: 4px; }}

.pk-tblwrap {{ border: 1px solid #DCE3EC; border-radius: 10px; background: #fff; overflow: auto; margin: 4px 0 8px 0; }}
.pk-tbl {{ width: 100%; border-collapse: collapse; font-size: .86rem; color: #1B2430; }}
.pk-tbl th {{ position: sticky; top: 0; z-index: 1; background: #F8FAFC; text-align: left; font-size: .7rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .06em; color: #64748B; padding: 8px 10px; border-bottom: 1px solid #DCE3EC; }}
.pk-tbl td {{ padding: 8px 10px; border-bottom: 1px solid #EEF2F7; vertical-align: top; overflow-wrap: break-word; }}
.pk-tbl tr:last-child td {{ border-bottom: 0; }}
.pk-tbl td.num, .pk-tbl th.num {{ text-align: right; }}
.pk-tbl td.num {{ white-space: nowrap; }}
@media (max-width: 640px) {{
  .pk-tbl thead {{ display: none; }}
  .pk-tbl, .pk-tbl tbody, .pk-tbl tr {{ display: block; width: 100%; }}
  .pk-tbl tr {{ padding: 6px 0; border-bottom: 2px solid #DCE3EC; }}
  .pk-tbl tr:last-child {{ border-bottom: 0; }}
  .pk-tbl td {{ display: flex; gap: 10px; border: 0; padding: 2px 12px; }}
  .pk-tbl td.num {{ text-align: left; white-space: normal; }}
  .pk-tbl td::before {{ content: attr(data-label); flex: 0 0 34%; font-size: .68rem; text-transform: uppercase; letter-spacing: .05em; color: #64748B; padding-top: 2px; }}
}}

.pk-login {{ background: #fff; border: 1px solid #DCE3EC; border-top: 5px solid {NAVY}; border-radius: 12px;
  padding: 24px 28px 8px 28px; margin-top: 5vh; }}
.pk-login .pk-brand {{ font-size: 1.7rem; font-weight: 800; color: {NAVY}; letter-spacing: .04em; }}
.pk-login .pk-brand-sub {{ color: #475569; font-size: .9rem; margin-bottom: 4px; }}
.pk-roles {{ display: grid; gap: 8px; margin: 8px 0 4px 0; }}
.pk-rolecard {{ border: 1px solid #DCE3EC; border-left: 6px solid var(--c); border-radius: 8px; padding: 8px 12px; background: #fff; }}
.pk-rolecard b {{ color: {NAVY}; font-size: .86rem; }}
.pk-rolecard span {{ display: block; font-size: .76rem; color: #64748B; }}
</style>
"""

HIDE_SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] { display: none; }
</style>
"""


def accent():
    return data.ROLE_COLOR.get(st.session_state.get("role"), NAVY)


def inject_css(logged_in: bool):
    role = st.session_state.get("role")
    root = f"<style>:root{{--accent:{accent()};--on-accent:{data.ROLE_ON_COLOR.get(role, '#FFFFFF')};}}</style>"
    st.markdown(root + CSS, unsafe_allow_html=True)
    if not logged_in:
        st.markdown(HIDE_SIDEBAR_CSS, unsafe_allow_html=True)


def esc(value):
    return html.escape(str(value)) if value not in (None, "") else "—"


def badge(status):
    color, bg = data.STATUS_STYLE.get(status, ("#475569", "#F1F5F9"))
    return f'<span class="pk-badge" style="color:{color};background:{bg};border-color:{color}55">{esc(status)}</span>'


def page_header(title, subtitle):
    role = st.session_state.get("role") or "-"
    chips = [
        f'<span class="pk-chip role">{esc(role)}</span>',
        f'<span class="pk-chip">{esc(state.actor_name())}</span>',
        f'<span class="pk-chip">Siklus: {esc(state.active_cycle())}</span>',
        f'<span class="pk-chip warn">{data.PROTOTYPE_BADGE}</span>',
    ]
    st.markdown(
        '<div class="pk-hero">'
        '<div class="pk-eyebrow">POLEKO Production Monitoring System · PT Royal Coconut — Airmadidi</div>'
        f"<h1>{esc(title)}</h1><div class=\"pk-sub\">{esc(subtitle)}</div>"
        f'<div class="pk-chips">{"".join(chips)}</div></div>',
        unsafe_allow_html=True,
    )


def empty_state(title, text):
    st.markdown(f'<div class="pk-empty"><b>{esc(title)}</b>{esc(text)}</div>', unsafe_allow_html=True)


def info_card(label, value, note="", pending=False):
    cls = "pk-card pending" if pending else "pk-card"
    st.markdown(
        f'<div class="{cls}"><div class="pk-label">{esc(label)}</div>'
        f'<div class="pk-value">{esc(value)}</div><div class="pk-note">{esc(note)}</div></div>',
        unsafe_allow_html=True,
    )


def stat_grid(items):
    """items: list of (label, value, warna, sufiks). Satu grid agar tinggi kartu seragam."""
    cards = []
    for label, value, color, suffix in items:
        suf = f" <small>{esc(suffix)}</small>" if suffix else ""
        cards.append(
            f'<div class="pk-stat" style="border-top-color:{color}"><div class="pk-label">{esc(label)}</div>'
            f'<div class="pk-value">{esc(value)}{suf}</div></div>'
        )
    st.markdown(f'<div class="pk-statgrid">{"".join(cards)}</div>', unsafe_allow_html=True)


def status_stat_grid(counts):
    stat_grid([(s, counts[s], data.STATUS_STYLE[s][0], "/ 18") for s in data.RECORD_STATUS_ORDER])


def stage_grid(cycle, only=None):
    cards = []
    for no, name in data.STAGES:
        if only is not None and no not in only:
            continue
        status = state.stage_status(cycle, no)
        color, _ = data.STATUS_STYLE[status]
        rec = state.get_record(cycle, no)
        who = rec["worker_name"] if rec else f"Ditugaskan: {state.worker_name(state.worker_for_stage(no))}"
        cards.append(
            f'<div class="pk-stage" style="border-left-color:{color}">'
            f'<div class="pk-stage-no">TAHAP {no:02d}</div>'
            f'<div class="pk-stage-name">{esc(name)}</div>'
            f'<div class="pk-stage-sub">{esc(who)}</div>{badge(status)}</div>'
        )
    st.markdown(f'<div class="pk-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def field_rows(f):
    return [
        ("Waktu mulai – selesai", state.time_text(f)),
        ("Durasi", state.duration_text(f)),
        ("Pelaksana/Pemantau", state.val(f.get("pelaksana"))),
        ("Kondisi proses", state.val(f.get("kondisi"))),
        ("Monitoring/Pencatatan", state.val(f.get("monitoring"))),
        ("Keterangan/Catatan", state.val(f.get("catatan"))),
    ]


def fields_block(f, extra=None):
    rows = (extra or []) + field_rows(f)
    cells = []
    for label, value in rows:
        na = " na" if value in (state.MISSING_TEXT, "Belum dicatat") else ""
        cells.append(f'<div class="pk-f"><div class="l">{esc(label)}</div><div class="v{na}">{esc(value)}</div></div>')
    st.markdown(f'<div class="pk-fields">{"".join(cells)}</div>', unsafe_allow_html=True)


def version_history(rec):
    for i, v in enumerate(rec["versions"], 1):
        with st.expander(f"Versi {i} — {v['label']} · {v['at']}", expanded=False):
            fields_block(v["data"])


def report_stepper(status):
    """Posisi laporan pada alur: dihasilkan → masuk Manajemen → dikonfirmasi → diteruskan ke GM."""
    labels = ["Laporan gabungan dihasilkan (SPV)", "Masuk ke PPIC / Manajemen", "Diperiksa dan dikonfirmasi", f"Diteruskan ke {data.GM} (DEMO)"]
    current = data.REPORT_RANK.get(status, -1)
    parts = []
    for i, label in enumerate(labels):
        cls = "pk-st done" if i < current else "pk-st now" if i == current else "pk-st"
        parts.append(f'<div class="{cls}">{i + 1}. {esc(label)}</div>')
    st.markdown(f'<div class="pk-steps">{"".join(parts)}</div>', unsafe_allow_html=True)


def report_preview(rep):
    blocks = []
    for s in rep["stages"]:
        rows = [("Dicatat oleh", s["worker_name"] + (" · dikirim ulang" if s["resubmitted"] else "")), ("Dikirim", s["submitted_at"])]
        cells = "".join(
            f'<div class="pk-f"><div class="l">{esc(l)}</div><div class="v{" na" if v in (state.MISSING_TEXT, "Belum dicatat") else ""}">{esc(v)}</div></div>'
            for l, v in rows + field_rows(s["data"])
        )
        blocks.append(f'<div class="pk-rep-stage"><div class="h">{s["no"]:02d}. {esc(s["name"])}</div><div class="pk-fields">{cells}</div></div>')
    st.markdown(
        '<div class="pk-report"><div class="head"><b>Laporan Gabungan Siklus '
        f'{esc(rep["cycle"])} — 18 Tahapan</b>'
        f'<span>DEMO / pratinjau sementara · Divalidasi oleh {esc(rep["validated_by"])} (TRUE) · '
        f'Waktu validasi (demo): {esc(rep["generated_at"])}</span>'
        f'<span>Status: {esc(rep["status"])}</span></div>'
        f'<div class="pk-rep-grid">{"".join(blocks)}</div></div>',
        unsafe_allow_html=True,
    )


def events_list(events, empty="Belum ada kejadian pada sesi ini."):
    if not events:
        empty_state("Belum ada riwayat", empty)
        return
    import pandas as pd

    df = pd.DataFrame(
        [{"Waktu": e["at"], "Siklus": e["cycle"], "Pelaku": e["actor"], "Jenis": e["kind"], "Kejadian": e["text"]} for e in reversed(events)]
    )
    table(df, max_height=560)
    st.caption("Riwayat sesi sementara; bukan log audit permanen dan hilang saat sesi berakhir.")


def store_panel(cycle=None):
    cycle = cycle or state.active_cycle()
    n = len(state.cycle_records(cycle))
    st.markdown(
        f'<div class="pk-store"><div class="t">{data.STORE_NAME}</div>'
        f'<div class="s">{data.STORE_LABEL} · Siklus {esc(cycle)}: {n} dari 18 tahapan tercatat di sesi ini.</div></div>',
        unsafe_allow_html=True,
    )


def demo_validation_label():
    st.markdown(f'<span class="pk-chip warn">{data.DEMO_VALIDATION_LABEL}</span>', unsafe_allow_html=True)


def demo_note():
    st.caption(f"⚠ {data.DEMO_NOTICE}.")


def about_prototype():
    with st.expander("Tentang prototipe"):
        st.markdown(
            f"- Mode Demonstrasi: aplikasi memperagakan alur To-Be, bukan sistem operasional perusahaan.\n"
            f"- {data.SESSION_NOTE}\n- {data.REALTIME_NOTE}\n"
            "- Peran dan penugasan tahapan adalah profil DEMO untuk memperagakan alur, bukan keamanan akses produksi "
            "maupun penugasan resmi POLEKO.\n"
            "- Field input mengacu pada Formulir Pengumpulan Data Ke-2; aturan wajib isi di formulir adalah Validasi "
            "Demonstrasi — Bukan Ketentuan Resmi POLEKO."
        )


def cycle_caption():
    st.caption(f"Siklus produksi aktif: **{state.active_cycle()}** (placeholder DEMO). Ganti pada sidebar.")


def _to_time(text):
    from datetime import datetime

    return datetime.strptime(text, "%H:%M").time() if text else None


def input_fields(prefix, d=None):
    """Field mengikuti Formulir Pengumpulan Data Ke-2 (bagian B). Panggil di dalam st.form."""
    d = d or {}
    c1, c2, c3 = st.columns([1, 1, 1.3])
    start = c1.time_input("Waktu mulai", value=_to_time(d.get("start")), step=300, key=f"{prefix}_start")
    end = c2.time_input("Waktu selesai", value=_to_time(d.get("end")), step=300, key=f"{prefix}_end")
    overnight = c3.checkbox(
        "Melewati pergantian hari (aturan demonstrasi)",
        value=bool(d.get("overnight")),
        key=f"{prefix}_night",
        help="Centang bila selesai setelah tengah malam. Hanya aturan interaksi prototipe.",
    )
    c4, c5 = st.columns(2)
    duration = c4.number_input("Durasi", min_value=0.0, value=d.get("duration"), step=5.0, key=f"{prefix}_dur", help="Opsional; formulir meminta lama proses dalam menit/jam.")
    unit_idx = data.DURASI_UNITS.index(d["duration_unit"]) if d.get("duration_unit") in data.DURASI_UNITS else 0
    unit = c5.selectbox("Satuan durasi", data.DURASI_UNITS, index=unit_idx, key=f"{prefix}_unit")
    pelaksana = st.text_input(
        "Pelaksana/Pemantau", value=d.get("pelaksana") or "", key=f"{prefix}_pel",
        help="Jabatan atau bagian yang menjalankan atau memantau proses. " + data.FIELD_EXAMPLE_PELAKSANA,
        placeholder="Jabatan/bagian (mis. Operator, SPV, Foreman, QC)",
    )
    c6, c7 = st.columns(2)
    kondisi = c6.selectbox(
        "Kondisi proses", data.KONDISI_OPTIONS, key=f"{prefix}_kon", index=data.KONDISI_OPTIONS.index(d["kondisi"]) if d.get("kondisi") in data.KONDISI_OPTIONS else None,
        placeholder="Pilih satu",
    )
    monitoring = c7.selectbox(
        "Monitoring/Pencatatan", data.MONITORING_OPTIONS, key=f"{prefix}_mon", index=data.MONITORING_OPTIONS.index(d["monitoring"]) if d.get("monitoring") in data.MONITORING_OPTIONS else None,
        placeholder="Pilih satu",
    )
    catatan = st.text_area(
        "Keterangan/Catatan", value=d.get("catatan") or "", key=f"{prefix}_cat",
        help="Formulir: isi hanya jika ada informasi penting, mis. menunggu, kendala, keterlambatan, atau pihak lain yang terlibat.",
    )
    return {
        "start": start.strftime("%H:%M") if start else None,
        "end": end.strftime("%H:%M") if end else None,
        "overnight": overnight,
        "duration": duration,
        "duration_unit": unit,
        "pelaksana": pelaksana.strip(),
        "kondisi": kondisi,
        "monitoring": monitoring,
        "catatan": catatan.strip(),
    }


def overview_table(df):
    table(df, badge_cols=("Status",), max_height=640)


def table(df, badge_cols=(), max_height=None):
    """Tabel HTML responsif: teks membungkus (tidak terpotong); di layar sempit tiap baris menjadi kartu bertumpuk."""
    head = "".join(f'<th class="{"num" if _is_num(df[c]) else ""}">{esc(c)}</th>' for c in df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = []
        for c in df.columns:
            v = row[c]
            inner = badge(v) if c in badge_cols else esc(v)
            cells.append(f'<td data-label="{html.escape(str(c))}" class="{"num" if _is_num(df[c]) else ""}">{inner}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    style = f' style="max-height:{max_height}px"' if max_height else ""
    st.markdown(
        f'<div class="pk-tblwrap"{style}><table class="pk-tbl"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>',
        unsafe_allow_html=True,
    )


def _is_num(series):
    return str(series.dtype).startswith(("int", "float"))
