"""Komponen tampilan bersama agar seluruh halaman terasa sebagai satu sistem."""
import html
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from core import data, state

NAVY = "#0B2545"
ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".svg")

CSS = f"""
<style>
html {{ font-size: 16px; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px; }}
[data-testid="stSidebar"] {{ background: #F5F7FA; border-right: 1px solid #DCE3EC; }}
h1, h2, h3, h4, h5 {{ color: {NAVY}; letter-spacing: -0.01em; }}
h3 {{ font-size: 1.15rem; margin-top: .6rem; }}
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {{ min-height: 2.75rem; font-weight: 600; }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {{
  background: var(--accent); border-color: var(--accent); color: var(--on-accent); }}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {{
  filter: brightness(.92); border-color: var(--accent); color: var(--on-accent); }}
.stButton > button[kind="primary"]:disabled {{ background: #CBD5E1; border-color: #CBD5E1; color: #475569; }}
[data-testid="stCaptionContainer"] {{ font-size: .86rem; }}

/* menu samping buatan sendiri */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {{ border-radius: 8px; padding: .5rem .7rem; margin: 1px 0; }}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {{
  background: color-mix(in srgb, var(--accent) 16%, white); border-left: 4px solid var(--accent); font-weight: 700; }}
.pk-navhead {{ font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; color: #64748B; margin: 12px 0 2px 4px; font-weight: 600; }}
.pk-brand {{ padding: 2px 0 6px 0; }}
.pk-brand .n {{ font-size: 1.9rem; font-weight: 800; letter-spacing: .05em; color: {NAVY}; line-height: 1.1; }}
.pk-brand .s {{ font-size: .95rem; font-weight: 600; color: #334155; line-height: 1.25; }}
.pk-who {{ border-left: 5px solid var(--accent); background: #fff; border-radius: 6px; padding: 6px 10px; margin: 6px 0 4px 0; }}
.pk-who b {{ color: {NAVY}; font-size: .95rem; }}
.pk-who span {{ display: block; font-size: .8rem; color: #475569; }}

@media (max-width: 900px) {{ .block-container {{ padding-top: 3.6rem; }} }}
.pk-head {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; flex-wrap: wrap;
  border-left: 6px solid var(--accent, {NAVY}); padding: 2px 0 2px 14px; margin-bottom: 14px; }}
.pk-head h1 {{ color: {NAVY}; font-size: 1.6rem; margin: 0; padding: 0; line-height: 1.2; }}
.pk-head .pk-sub {{ color: #475569; font-size: .95rem; margin-top: 2px; }}
.pk-chip {{ font-size: .78rem; padding: 3px 10px; border-radius: 999px; background: #EEF2F7; color: #334155; border: 1px solid #DCE3EC; white-space: nowrap; }}
.pk-chip.warn {{ background: #FEF3C7; color: #92400E; border-color: #F5D58A; }}

.pk-card {{ background: #fff; border: 1px solid #DCE3EC; border-radius: 10px; padding: 14px 16px; height: 100%; }}
.pk-card .pk-label {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; color: #475569; }}
.pk-card .pk-value {{ font-size: 1.2rem; font-weight: 700; color: {NAVY}; margin-top: 2px; }}
.pk-card .pk-note {{ font-size: .85rem; color: #475569; margin-top: 4px; }}

.pk-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }}
.pk-stage {{ background: #fff; border: 1px solid #DCE3EC; border-left: 5px solid #64748B; border-radius: 8px;
  padding: 10px 12px; display: flex; flex-direction: column; gap: 6px; min-height: 104px; }}
.pk-stage-no {{ font-size: .75rem; font-weight: 700; color: #64748B; letter-spacing: .06em; }}
.pk-stage-name {{ font-size: .92rem; font-weight: 600; color: #1B2430; line-height: 1.25; flex: 1; }}
.pk-badge {{ display: inline-block; align-self: flex-start; font-size: .75rem; font-weight: 600;
  padding: 2px 9px; border-radius: 999px; border: 1px solid; line-height: 1.35; }}

.pk-statgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin-bottom: 10px; }}
.pk-stat {{ background: #fff; border: 1px solid #DCE3EC; border-top: 4px solid #64748B; border-radius: 10px;
  padding: 12px 14px; min-height: 96px; display: flex; flex-direction: column; justify-content: space-between; }}
.pk-stat .pk-label {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .07em; color: #475569; line-height: 1.3; }}
.pk-stat .pk-value {{ font-size: 1.6rem; font-weight: 700; color: {NAVY}; }}
.pk-stat .pk-value small {{ font-size: .85rem; color: #64748B; font-weight: 500; }}
.pk-stat .pk-sn {{ font-size: .82rem; color: #475569; margin-top: 2px; }}

.pk-note-box {{ border: 1px solid #F5D58A; border-left: 5px solid #D6A62A; background: #FFFBEB; border-radius: 8px; padding: 10px 14px;
  margin: 6px 0 10px 0; font-size: .92rem; line-height: 1.55; color: #1B2430; }}

.pk-empty {{ border: 1.5px dashed #C3CEDC; border-radius: 10px; padding: 24px; text-align: center; color: #475569; background: #FAFBFD; }}
.pk-empty b {{ color: {NAVY}; display: block; margin-bottom: 4px; font-size: 1.05rem; }}

.pk-steps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin: 4px 0 10px 0; }}
.pk-st {{ border: 1px solid #DCE3EC; border-top: 4px solid #CBD5E1; border-radius: 8px; padding: 8px 10px; background: #fff;
  font-size: .82rem; color: #475569; line-height: 1.3; }}
.pk-st.done {{ border-top-color: #15803D; color: #166534; background: #F3FBF6; }}
.pk-st.now {{ border-top-color: var(--accent); color: {NAVY}; font-weight: 700; box-shadow: 0 0 0 2px var(--accent); }}

.pk-fields {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 6px 18px; margin: 6px 0; }}
.pk-f .l {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: #475569; }}
.pk-f .v {{ font-size: .93rem; color: #1B2430; overflow-wrap: anywhere; }}
.pk-f .v.na {{ color: #64748B; font-style: italic; }}

.pk-report {{ border: 1px solid #DCE3EC; border-radius: 10px; background: #fff; padding: 14px 16px; }}
.pk-report .head {{ border-bottom: 2px solid var(--accent); padding-bottom: 8px; margin-bottom: 10px; }}
.pk-report .head b {{ color: {NAVY}; font-size: 1.05rem; }}
.pk-report .head span {{ display: block; font-size: .85rem; color: #475569; }}
.pk-rep-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }}
.pk-rep-stage {{ border: 1px solid #E3E8EF; border-radius: 8px; padding: 10px 12px; background: #FBFCFE; }}
.pk-rep-stage .h {{ font-weight: 700; color: {NAVY}; font-size: .92rem; margin-bottom: 4px; }}

.pk-tblwrap {{ border: 1px solid #DCE3EC; border-radius: 10px; background: #fff; overflow: auto; margin: 4px 0 8px 0; }}
.pk-tbl {{ width: 100%; border-collapse: collapse; font-size: .9rem; color: #1B2430; }}
.pk-tbl th {{ position: sticky; top: 0; z-index: 1; background: #F8FAFC; text-align: left; font-size: .72rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .06em; color: #475569; padding: 8px 10px; border-bottom: 1px solid #DCE3EC; }}
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
  .pk-tbl td::before {{ content: attr(data-label); flex: 0 0 34%; font-size: .72rem; text-transform: uppercase; letter-spacing: .05em; color: #475569; padding-top: 2px; }}
}}

.pk-login-brand {{ text-align: center; margin: 0 0 6px 0; }}
.pk-login-brand .n {{ font-size: 2.3rem; font-weight: 800; color: {NAVY}; letter-spacing: .05em; line-height: 1.1; }}
.pk-login-brand .s {{ font-size: 1.05rem; font-weight: 600; color: #334155; }}
</style>
"""

HIDE_SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"], [data-testid="stExpandSidebarButton"] { display: none; }
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


# ---------------------------------------------------------------- identitas aplikasi
def logo_file():
    """Logo resmi PT Royal Coconut bila file-nya ada di assets/ (nama berisi 'logo'). Tidak pernah dibuat ulang."""
    if not ASSETS.is_dir():
        return None
    for f in sorted(ASSETS.iterdir()):
        if f.suffix.lower() in LOGO_SUFFIXES and "logo" in f.stem.lower():
            return f
    return None


@st.cache_resource(show_spinner=False)
def _trimmed_logo(path, mtime):
    """Pangkas ruang kosong (putih atau transparan) di tepi logo tanpa mengubah bentuknya."""
    from PIL import Image, ImageChops

    im = Image.open(path).convert("RGBA")
    flat = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im).convert("RGB")
    diff = ImageChops.difference(flat, Image.new("RGB", im.size, (255, 255, 255))).point(lambda v: 255 if v > 12 else 0)
    box = diff.getbbox()
    if not box:
        return im
    pad = 4
    box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height))
    return im.crop(box)


def brand(sidebar=True, width=210):
    """Logo (jika file tersedia) lalu identitas aplikasi. Tanpa file logo hanya judul teks, bukan logo tiruan."""
    f = logo_file()
    if f:
        if f.suffix.lower() == ".svg":
            st.image(str(f), width=width)
        else:
            st.image(_trimmed_logo(str(f), f.stat().st_mtime), width=width)
    if sidebar:
        st.markdown('<div class="pk-brand"><div class="n">POLEKO</div><div class="s">Production Monitoring System</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pk-login-brand" style="text-align:center;width:100%"><div class="n">POLEKO</div><div class="s">Production Monitoring System</div></div>', unsafe_allow_html=True)




def who_block():
    ss = st.session_state
    stages = ""
    role = ss.get("role")
    if role == data.ROLE_PEKERJA and ss.get("worker_id"):
        no = state.worker_stage(ss.worker_id)
        stages = f"<span>Tahap {no:02d} — {esc(data.stage_short(no))}</span>"
    elif role == data.ROLE_SPV and ss.get("shift"):
        stages = f"<span>{esc(data.shift_name(ss.shift))}</span>"
    st.markdown(f'<div class="pk-who"><b>{esc(state.actor_name())}</b><span>{esc(role)}</span>{stages}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- komponen halaman
def badge(status):
    color, bg = data.STATUS_STYLE.get(status, ("#475569", "#F1F5F9"))
    return f'<span class="pk-badge" style="color:{color};background:{bg};border-color:{color}55">{esc(status)}</span>'


def page_header(title, subtitle=""):
    sub = f'<div class="pk-sub">{esc(subtitle)}</div>' if subtitle else ""
    st.markdown(f'<div class="pk-head"><div><h1>{esc(title)}</h1>{sub}</div></div>', unsafe_allow_html=True)


def go(page, label, icon=None, type="primary"):
    """Tombol aksi menuju halaman lain (lebih jelas bagi pengguna awam daripada tautan teks)."""
    if st.button(label, type=type, icon=icon, key=f"go_{page}_{label}"):
        st.switch_page(page)


def flash_message(kind, text):
    st.session_state["_flash"] = (kind, text)


def empty_state(title, text):
    st.markdown(f'<div class="pk-empty"><b>{esc(title)}</b>{esc(text)}</div>', unsafe_allow_html=True)


def info_card(label, value, note=""):
    st.markdown(
        f'<div class="pk-card"><div class="pk-label">{esc(label)}</div>'
        f'<div class="pk-value">{esc(value)}</div><div class="pk-note">{esc(note)}</div></div>',
        unsafe_allow_html=True,
    )


def stat_grid(items, min_width=170):
    """items: list of (label, value, warna, sufiks[, catatan kecil]). Satu grid agar tinggi kartu seragam."""
    cards = []
    for label, value, color, suffix, *rest in items:
        suf = f" <small>{esc(suffix)}</small>" if suffix else ""
        note = f'<div class="pk-sn">{esc(rest[0])}</div>' if rest else ""
        cards.append(
            f'<div class="pk-stat" style="border-top-color:{color}"><div class="pk-label">{esc(label)}</div>'
            f'<div class="pk-value">{esc(value)}{suf}</div>{note}</div>'
        )
    st.markdown(
        f'<div class="pk-statgrid" style="grid-template-columns:repeat(auto-fit,minmax({min_width}px,1fr))">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


def status_stat_grid(counts):
    stat_grid([(s, counts[s], data.STATUS_STYLE[s][0], "/ 18") for s in data.RECORD_STATUS_ORDER])


def stage_grid(cycle, only=None):
    cards = []
    for no, name in data.STAGES:
        if only is not None and no not in only:
            continue
        status = state.stage_status(cycle, no)
        color, _ = data.STATUS_STYLE[status]
        cards.append(
            f'<div class="pk-stage" style="border-left-color:{color}">'
            f'<div class="pk-stage-no">TAHAP {no:02d}</div>'
            f'<div class="pk-stage-name">{esc(name)}</div>{badge(status)}</div>'
        )
    st.markdown(f'<div class="pk-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def field_rows(f, stage_no=None):
    rows = [("Waktu mulai – selesai", state.time_text(f)), ("Durasi", state.duration_text(f))]
    if stage_no in data.STAGE_STANDARD:
        rows.append(("Batas", standard_text(stage_no)))
    if stage_no == data.OPENING_STAGE or f.get("arrival"):
        rows.append(("Waktu Kedatangan Bahan Baku", state.val(f.get("arrival"))))
    rows += [
        ("Jumlah Produksi (kg)", state.kg_text(f)),
        ("Pelaksana/Pemantau", state.val(f.get("pelaksana"))),
        ("Kondisi proses", state.val(f.get("kondisi"))),
    ]
    if f.get("kendala"):
        rows.append(("Kendala", f["kendala"]))
    if f.get("mesin"):
        rows.append(("Kerusakan mesin", "Ya"))
    if f.get("alasan"):
        rows.append(("Alasan", f["alasan"]))
    return rows


def standard_text(stage_no):
    a, b, dur, _ = data.STAGE_STANDARD[stage_no]
    if a is None:
        lo, hi = data.STORAGE_DAYS
        return f"{lo}–{hi} hari"
    nxt = " (+1 hari)" if stage_no == 3 else ""
    return f"{a.replace(':', '.')}–{b.replace(':', '.')}{nxt} · {dur} menit"


def level_badge(level):
    return badge(level)


def _field_cell(label, value):
    na = " na" if value in (state.MISSING_TEXT, "Belum dicatat") else ""
    return f'<div class="pk-f"><div class="l">{esc(label)}</div><div class="v{na}">{esc(value)}</div></div>'


def fields_block(f, extra=None, stage_no=None):
    cells = "".join(_field_cell(label, value) for label, value in (extra or []) + field_rows(f, stage_no))
    st.markdown(f'<div class="pk-fields">{cells}</div>', unsafe_allow_html=True)


def kv(rows):
    """Blok label/nilai. Nilai berupa teks biasa, atau ("badge", status) untuk lencana status."""
    cells = []
    for label, value in rows:
        if isinstance(value, tuple) and value[0] == "badge":
            cells.append(f'<div class="pk-f"><div class="l">{esc(label)}</div><div class="v">{badge(value[1])}</div></div>')
        else:
            cells.append(_field_cell(label, value))
    st.markdown(f'<div class="pk-fields">{"".join(cells)}</div>', unsafe_allow_html=True)


def version_history(rec):
    """Riwayat versi: versi awal tidak pernah ditimpa; setiap perubahan tersimpan sebagai versi baru."""
    n = len(rec["versions"])
    for i, v in enumerate(rec["versions"], 1):
        tag = " · terbaru" if i == n else ""
        with st.expander(f"Versi {i} — {v['label']} · {v['at']}{tag}", expanded=False):
            extra = [("Dikirim oleh", v.get("by") or "—")]
            if v.get("spv_note"):
                extra.append(("Catatan Supervisor yang mendasari perbaikan", v["spv_note"]))
            fields_block(v["data"], extra, rec["stage_no"])


def report_stepper(status):
    """Posisi laporan pada alur: dihasilkan -> diteruskan ke Manajemen -> dikonfirmasi -> diterima General Manager (DEMO)."""
    labels = ["Laporan gabungan dihasilkan (Supervisor)", "Diteruskan ke Manajemen", "Diperiksa dan dikonfirmasi Production Manager", f"Diterima {data.GM} (DEMO)"]
    current = data.REPORT_STEP.get(status, -1)
    parts = []
    for i, label in enumerate(labels):
        if status == data.R_GM:
            cls = "pk-st done"
        else:
            cls = "pk-st done" if i < current else "pk-st now" if i == current else "pk-st"
        parts.append(f'<div class="{cls}">{i + 1}. {esc(label)}</div>')
    st.markdown(f'<div class="pk-steps">{"".join(parts)}</div>', unsafe_allow_html=True)


def report_preview(rep):
    """Laporan gabungan 18 tahapan (versi terbaru)."""
    blocks = []
    for s in rep["stages"]:
        rows = [
            ("Dicatat oleh", s["worker_name"] + (f" · {s['versions']} versi" if s["versions"] > 1 else "")),
            ("Dikirim", s["submitted_at"]),
            ("Status pemeriksaan", s["status"]),
            ("Dikonfirmasi Supervisor", f"{s['confirmed_by']} · {s['confirmed_at']}" if s["confirmed_by"] else "—"),
            ("Shift", data.shift_name(s.get("shift"))),
            ("Tingkat risiko", s.get("level", data.LV_HIJAU) + (f" → {', '.join(s['routes'])}" if s.get("routes") else "")),
        ]
        cells = "".join(_field_cell(l, v) for l, v in rows + field_rows(s["data"], s["no"]))
        blocks.append(f'<div class="pk-rep-stage"><div class="h">{s["no"]:02d}. {esc(s["name"])}</div><div class="pk-fields">{cells}</div></div>')
    head = (
        f'<b>Laporan Gabungan {esc(rep["report_id"])} — 18 Tahapan</b>'
        f'<span>Identitas siklus (internal): {esc(rep["cycle"])} · Tanggal produksi: {esc(rep["production_date"])}</span>'
        f'<span>Dihasilkan oleh {esc(rep["generated_by"])} · {esc(rep["generated_at"])} · Versi laporan: {len(rep["versions"])}</span>'
        f'<span>Status: {esc(rep["status"])}</span>'
    )
    st.markdown(f'<div class="pk-report"><div class="head">{head}</div><div class="pk-rep-grid">{"".join(blocks)}</div></div>', unsafe_allow_html=True)


def session_note(text="Data hanya tersimpan sementara pada sesi demo ini. Tidak tersinkron antar pengguna atau perangkat."):
    st.caption(text)


def report_picker(label="Pilih laporan"):
    """Pilihan laporan Manajemen. Mengembalikan siklus terpilih atau None bila belum ada laporan (satu laporan: tanpa dropdown)."""
    cycles = sorted(r["cycle"] for r in state.reports_visible_to_management())
    if not cycles:
        return None
    if len(cycles) == 1:
        return cycles[0]
    ss = st.session_state
    if ss.get("mgr_sel") not in cycles:
        ss["mgr_sel"] = ss.get("_mgr_pick") if ss.get("_mgr_pick") in cycles else cycles[0]
    labels = {c: f"{c} · {state.report_status(c)}" for c in cycles}
    cycle = st.selectbox(label, cycles, key="mgr_sel", format_func=labels.get)
    ss["_mgr_pick"] = cycle
    return cycle


def events_list(events, empty="Belum ada kejadian pada sesi ini."):
    if not events:
        empty_state("Belum ada riwayat", empty)
        return
    df = pd.DataFrame([{"Waktu": e["at"], "Pelaku": e["actor"], "Jenis": e["kind"], "Kejadian": e["text"]} for e in reversed(events)])
    table(df, max_height=560)


def demo_validation_label():
    pass


def _to_time(text):
    return datetime.strptime(text, "%H:%M").time() if text else None


def _index(options, value):
    return options.index(value) if value in options else None


def input_fields(prefix, stage_no, d=None, shift=None):
    """Isian Pekerja. Durasi dihitung otomatis; batas tahap diperiksa langsung saat diisi."""
    d = d or {}
    storage = stage_no == data.STORAGE_STAGE
    c1, c2 = st.columns(2)
    start = c1.time_input("Waktu Mulai", value=_to_time(d.get("start")), step=300, key=f"{prefix}_start")
    end, hari = None, None
    if storage:
        lo, hi = data.STORAGE_DAYS
        hari = c2.number_input("Lama Penyimpanan (hari)", min_value=0, max_value=30, value=d.get("hari"), step=1, key=f"{prefix}_hari")
    else:
        end = c2.time_input("Waktu Selesai", value=_to_time(d.get("end")), step=300, key=f"{prefix}_end")
    arrival = None
    if stage_no == data.OPENING_STAGE:
        arrival = st.selectbox("Kedatangan Bahan Baku", data.OPENING_ARRIVAL_OPTIONS, index=_index(data.OPENING_ARRIVAL_OPTIONS, d.get("arrival")),
                               placeholder="Pilih", key=f"{prefix}_arr")
    kg = st.number_input("Jumlah Produksi (kg)", min_value=0.0, value=d.get("jumlah_kg"), step=1.0, format="%.2f", key=f"{prefix}_kg")
    c3, c4 = st.columns(2)
    pelaksana = c3.selectbox("Pelaksana/Pemantau", data.PELAKSANA_OPTIONS, index=_index(data.PELAKSANA_OPTIONS, d.get("pelaksana")),
                             placeholder="Pilih", key=f"{prefix}_pel")
    kondisi = c4.selectbox("Kondisi Proses", data.KONDISI_OPTIONS, index=_index(data.KONDISI_OPTIONS, d.get("kondisi")),
                           placeholder="Pilih", key=f"{prefix}_kon")
    kendala, mesin = "", False
    if kondisi and kondisi != data.KONDISI_NORMAL:
        kendala = st.text_area("Kendala", value=d.get("kendala") or "", key=f"{prefix}_kend")
        mesin = st.checkbox("Kerusakan mesin", value=bool(d.get("mesin")), key=f"{prefix}_mesin")
    f = {
        "start": start.strftime("%H:%M") if start else None,
        "end": end.strftime("%H:%M") if end else None,
        "overnight": False,
        "hari": int(hari) if hari not in (None, "") else None,
        "arrival": arrival,
        "jumlah_kg": kg,
        "pelaksana": pelaksana,
        "kondisi": kondisi,
        "kendala": (kendala or "").strip(),
        "mesin": mesin,
        "alasan": "",
        "lewat_batas": False,
    }
    shift = state.shift_from_start(f["start"]) or 1
    issues = state.check_limits(f, stage_no, shift)
    for i in issues:
        st.warning(i["text"])
    if any(i["hard"] for i in issues):
        f["lewat_batas"] = st.checkbox("Selesai melewati batas", value=bool(d.get("lewat_batas")), key=f"{prefix}_lewat")
    if issues:
        f["alasan"] = st.text_area("Alasan", value=d.get("alasan") or "", key=f"{prefix}_alasan").strip()
    return f


def confirm_action(label, key, title, message, action, *, icon=None, type="primary", disabled=False, confirm_label="Ya, lanjutkan", on_done=None):
    """Tombol tindakan final yang meminta konfirmasi lewat dialog agar tidak tertekan tanpa sengaja.

    `action()` mengembalikan (ok, pesan, ...). Hasil dikirim sebagai pesan umpan balik, kecuali `on_done(ok, pesan)` diberikan.
    """

    @st.dialog(title)
    def _dialog():
        st.write(message)
        yes, no = st.columns(2)
        if yes.button(confirm_label, type="primary", width="stretch", key=f"{key}_yes"):
            result = action()
            if on_done:
                on_done(result[0], result[1])
            else:
                flash_message("success" if result[0] else "error", result[1])
            st.rerun()
        if no.button("Batal", width="stretch", key=f"{key}_no"):
            st.rerun()

    if st.button(label, type=type, icon=icon, disabled=disabled, key=key):
        _dialog()


def overview_table(df):
    table(df, badge_cols=("Status Input", "Status Pemeriksaan Supervisor", "Status", "Tingkat Risiko"), max_height=640)


def images_block(images, width=220):
    if images:
        cols = st.columns(min(len(images), 3))
        for i, (name, blob) in enumerate(images):
            cols[i % len(cols)].image(blob, caption=name, width=width)


def table(df, badge_cols=(), max_height=None):
    """Tabel HTML responsif: teks membungkus (tidak terpotong); di layar sempit tiap baris menjadi kartu bertumpuk."""
    head = "".join(f'<th class="{"num" if _is_num(df[c]) else ""}">{esc(c)}</th>' for c in df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = []
        for c in df.columns:
            v = row[c]
            inner = badge(v) if c in badge_cols and v in data.STATUS_STYLE else esc(v)
            cells.append(f'<td data-label="{html.escape(str(c))}" class="{"num" if _is_num(df[c]) else ""}">{inner}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    style = f' style="max-height:{max_height}px"' if max_height else ""
    st.markdown(
        f'<div class="pk-tblwrap"{style}><table class="pk-tbl"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>',
        unsafe_allow_html=True,
    )


def _is_num(series):
    return str(series.dtype).startswith(("int", "float"))
