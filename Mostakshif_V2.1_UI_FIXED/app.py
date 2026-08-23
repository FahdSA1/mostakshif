# Mostakshif | نسخة عملية + تصميم فاخر + UX محسن (Hackathon Edition)
# تشغيل: python -m streamlit run app.py

import base64
import html
import math
import random
from pathlib import Path
from urllib.parse import quote

import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from branca.element import MacroElement, Template
from folium.plugins import Fullscreen
from streamlit_folium import st_folium

st.set_page_config(
    page_title="مستكشف | عقارات الرياض",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# Design tokens — Color Palette (derived from brand reference colors)
#   #08635a  -> Primary (deep teal-green)
#   #00ae84  -> Primary Light / accents
#   #00deba  -> Secondary (mint accent)
#   #5c707d  -> Muted text / secondary text
#   #f7a20b  -> Warning / highlight accent
#   #eeeeee  -> Neutral surfaces
# ============================================================
PRIMARY = "#08635a"
PRIMARY_LIGHT = "#0f9a7f"
PRIMARY_DARK = "#054a43"
SECONDARY = "#00deba"
ACCENT_GOLD = "#c9973e"
BG = "#f5f8f7"
SURFACE = "#ffffff"
INK = "#12241f"
MUTED = "#5c707d"
MUTED_LIGHT = "#8a9793"
BORDER = "#e4ece9"
SUCCESS = "#0f9a6b"
WARNING = "#f7a20b"
ERROR = "#d64545"
INFO = "#2b71c8"
SELECTED = "#1678d3"
HOVER = "#0c7768"

# Max interior photos per residential property
MAX_INTERIOR = 3

# ============================================================
# CSS — RTL + premium commercial UI
# ============================================================
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');

:root {{
  --primary: {PRIMARY};
  --primary-light: {PRIMARY_LIGHT};
  --primary-dark: {PRIMARY_DARK};
  --secondary: {SECONDARY};
  --gold: {ACCENT_GOLD};
  --bg: {BG};
  --surface: {SURFACE};
  --ink: {INK};
  --muted: {MUTED};
  --muted-light: {MUTED_LIGHT};
  --border: {BORDER};
  --success: {SUCCESS};
  --warning: {WARNING};
  --error: {ERROR};
  --info: {INFO};
  --selected: {SELECTED};
  --radius-sm: 10px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 26px;
  --shadow-sm: 0 2px 10px rgba(8,40,34,.05);
  --shadow-md: 0 6px 22px rgba(8,40,34,.07);
  --shadow-lg: 0 14px 38px rgba(8,40,34,.12);
}}

html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],.block-container,
button,input,textarea,select,.stMarkdown,.stTextInput,.stSelectbox,.stNumberInput{{font-family:'Cairo',Tahoma,Arial,sans-serif!important;}}
html,body,.stApp{{direction:rtl!important;background:var(--bg)!important;color:var(--ink);}}
.stApp{{text-align:right!important;}}
[data-testid="stHeader"],[data-testid="stSidebar"]{{display:none!important;}}
.block-container{{max-width:100%!important;width:100%!important;padding:.6rem 1.4rem 2.5rem!important;margin:0 auto!important;}}
[data-testid="stAppViewBlockContainer"]{{padding-top:.6rem!important;}}
[data-testid="stMainBlockContainer"]{{padding-top:.6rem!important;}}
* {{ box-sizing: border-box; }}

/* Buttons — unified system */
.stButton>button,.stLinkButton>a{{
  border-radius:var(--radius-sm)!important;min-height:44px!important;font-weight:700!important;
  direction:rtl!important;border:1px solid transparent!important;
  transition:transform .15s ease, box-shadow .15s ease, filter .15s ease!important;
  box-shadow:var(--shadow-sm)!important;
}}
.stButton>button p,.stLinkButton>a p{{font-family:'Cairo'!important;font-size:13.5px!important;}}
.stButton>button:hover,.stLinkButton>a:hover{{transform:translateY(-1px);filter:brightness(1.05);box-shadow:var(--shadow-md)!important;}}
.stButton>button:active{{transform:translateY(0px) scale(.98);}}

/* Primary CTA gets brand color via kind="primary" */
div[data-testid="stButton"] button[kind="primary"]{{background:var(--primary)!important;color:#fff!important;border-color:var(--primary)!important;}}

div[data-baseweb="select"]>div,input,textarea{{direction:rtl!important;text-align:right!important;border-radius:var(--radius-sm)!important;border-color:var(--border)!important;transition:border-color .15s ease, box-shadow .15s ease;}}
div[data-baseweb="select"]>div:hover,input:hover,textarea:hover{{border-color:var(--primary-light)!important;}}
div[data-baseweb="select"]>div:focus-within,input:focus,textarea:focus{{border-color:var(--primary)!important;box-shadow:0 0 0 3px rgba(8,99,90,.12)!important;}}
label{{font-weight:700!important;color:var(--ink)!important;font-size:12.5px!important;}}

/* ---------------- Header ---------------- */
.topbar{{min-height:128px;background:var(--surface);border:1px solid var(--border);border-radius:0 0 24px 24px;display:flex;align-items:center;padding:0 24px;box-shadow:var(--shadow-md);margin-bottom:14px;direction:rtl;}}
.brand{{display:flex;align-items:center;gap:16px;min-width:300px;}}
.brand-logo{{width:132px;height:132px;object-fit:contain;border-radius:18px;background:#fff;}}
.brand-mark{{width:100px;height:100px;border-radius:20px;background:linear-gradient(145deg,var(--primary-dark),var(--primary-light));color:#fff;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:800;box-shadow:var(--shadow-sm);}}
.brand-title{{font-size:32px;font-weight:900;color:var(--ink);line-height:1;letter-spacing:.2px;}}
.brand-sub{{font-size:10.5px;color:var(--muted);margin-top:5px;font-weight:600;}}
.nav{{display:flex;justify-content:center;align-items:center;gap:33px;flex:1;height:100%;}}
.nav a{{font-weight:700;color:#2b3a41;font-size:14.5px;padding:24px 2px 18px;white-space:nowrap;text-decoration:none;border-bottom:3px solid transparent;transition:color .15s ease,border-color .15s ease;}}
.nav a:hover{{color:var(--primary);}}
.nav a.active{{color:var(--primary);border-bottom:3px solid var(--primary);}}
.top-actions{{display:flex;gap:10px;min-width:275px;justify-content:flex-start;}}
.pill{{border:1.5px solid var(--primary);border-radius:var(--radius-sm);padding:11px 18px;color:var(--primary);background:#fff;font-weight:800;font-size:12.5px;text-decoration:none;transition:all .15s ease;display:inline-flex;align-items:center;gap:6px;}}
.pill:hover{{background:var(--primary);color:#fff;}}
.login-pill{{background:var(--primary-dark);color:#fff;border-color:var(--primary-dark);}}
.login-pill:hover{{background:var(--primary);border-color:var(--primary);}}

/* Nav rendered as real Streamlit buttons (in-app navigation, no page reload) */
div[class*="st-key-topbar_wrap"]{{background:var(--surface);border:1px solid var(--border);border-radius:0 0 24px 24px;box-shadow:var(--shadow-md);margin-bottom:14px;padding:10px 18px;}}
div[class*="st-key-nav_"] .stButton>button{{background:transparent!important;box-shadow:none!important;border:none!important;color:#2b3a41!important;font-weight:700!important;border-bottom:3px solid transparent!important;border-radius:0!important;min-height:38px!important;}}
div[class*="st-key-nav_"] .stButton>button:hover{{color:var(--primary)!important;transform:none;}}
div[class*="st-key-navactive_"] .stButton>button{{color:var(--primary)!important;border-bottom:3px solid var(--primary)!important;}}
div[class*="st-key-navcta_"] .stButton>button{{border:1.5px solid var(--primary)!important;color:var(--primary)!important;background:#fff!important;}}
div[class*="st-key-navlogin_"] .stButton>button{{background:var(--primary-dark)!important;color:#fff!important;border:1.5px solid var(--primary-dark)!important;}}

/* ---------------- Hero ---------------- */
.hero{{height:190px;border-radius:var(--radius-xl);overflow:hidden;position:relative;margin:0 0 14px;color:#fff;background-position:center;background-size:cover;
  background-image:linear-gradient(100deg,rgba(5,25,22,.90) 5%,rgba(8,99,90,.55) 60%,rgba(0,222,186,.28) 100%),linear-gradient(180deg,#9fc4d4 0%,#e8a271 55%,#33484d 100%);
  box-shadow:var(--shadow-lg);}}
.hero:after{{content:"";position:absolute;inset:auto 0 0;height:60px;background:linear-gradient(90deg,transparent 0 5%,#0c2420 5% 7%,transparent 7% 10%,#0e2622 10% 14%,transparent 14% 18%,#0e2622 18% 22%,transparent 22% 26%,#0c2420 26% 31%,transparent 31% 35%,#0e2622 35% 39%,transparent 39% 44%,#0e2622 44% 48%,transparent 48% 53%,#0c2420 53% 57%,transparent 57% 62%,#0e2622 62% 67%,transparent 67% 72%,#0c2420 72% 76%,transparent 76% 81%,#0e2622 81% 86%,transparent 86% 92%,#0c2420 92% 96%,transparent 96%);opacity:.85;}}
.hero-inner{{position:relative;z-index:2;height:100%;display:flex;align-items:center;justify-content:center;gap:36px;padding:0 30px;direction:rtl;text-align:center;}}
.hero-copy{{flex:0 1 540px;align-self:center;text-align:center;}}
.hero-copy h1{{font-size:33px;margin:0 0 6px;color:#fff;font-weight:900;text-shadow:0 2px 10px rgba(0,0,0,.3);letter-spacing:.2px;}}
.hero-copy p{{margin:0;color:#e7f4f1;font-size:14.5px;font-weight:500;}}
.hero-stats{{display:flex;background:rgba(6,22,20,.55);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.18);border-radius:var(--radius-md);overflow:hidden;min-width:430px;direction:rtl;}}
.hero-stat{{padding:15px 24px;text-align:center;min-width:138px;border-left:1px solid rgba(255,255,255,.16);}}
.hero-stat:last-child{{border-left:0;}}
.hero-stat b{{display:block;font-size:21px;color:#fff;font-weight:800;}}
.hero-stat span{{font-size:11px;color:#d7e8e4;}}

/* ---------------- Search / filters ---------------- */
.searchbar{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);padding:5px 12px;margin-bottom:12px;box-shadow:var(--shadow-sm);}}
.filter-box{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:18px 20px 14px;box-shadow:var(--shadow-md);direction:rtl;text-align:right;margin-bottom:14px;animation:fadeSlide .25s ease;}}
@keyframes fadeSlide{{from{{opacity:0;transform:translateY(-6px);}}to{{opacity:1;transform:translateY(0);}}}}
.filter-heading{{font-size:20px;font-weight:900;color:var(--ink);margin-bottom:4px;display:flex;align-items:center;gap:10px;}}
.filter-heading span{{font-size:11.5px;color:var(--muted);font-weight:600;}}
.filter-sep{{height:1px;background:var(--border);margin:10px 0 14px;}}
.filter-tip{{font-size:11px;color:var(--muted-light);padding-top:31px;font-weight:600;}}
.filter-toggle-row{{display:flex;justify-content:flex-end;margin-bottom:8px;}}

/* ---------------- Results ---------------- */
.results-heading{{display:flex;justify-content:space-between;align-items:end;gap:12px;margin:6px 4px 12px;direction:rtl;}}
.results-heading h2{{font-size:22px;font-weight:900;color:var(--ink);margin:0;}}
.results-heading span{{color:var(--primary);}}
.result-note{{font-size:10.5px;color:var(--muted-light);font-weight:600;}}

.property-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:12px;margin-bottom:12px;
  box-shadow:var(--shadow-sm);direction:rtl;text-align:center;transition:box-shadow .18s ease, transform .18s ease, border-color .18s ease;}}
.property-card:hover{{box-shadow:var(--shadow-lg);transform:translateY(-2px);border-color:#cfe9e0;}}
.property-card.is-selected{{border-color:var(--primary);box-shadow:0 0 0 2px rgba(8,99,90,.18),var(--shadow-md);}}
.property-card img{{border-radius:var(--radius-md);object-fit:cover;max-height:170px;}}

.photo-count{{position:relative;display:inline-block;background:rgba(8,36,31,.72);color:#fff;font-size:10px;font-weight:800;
  border-radius:999px;padding:3px 9px;margin-top:-30px;z-index:5;backdrop-filter:blur(2px);}}

.badge{{display:inline-block;padding:5px 12px;border-radius:999px;background:#e3f6ee;color:var(--primary-dark);font-size:10.5px;font-weight:800;letter-spacing:.2px;}}
.badge-rent{{background:#e8f0ff;color:var(--info);}}
.badge-sold{{background:#f1f2f3;color:#68727a;}}
.badge-leased{{background:#fff0df;color:#a76108;}}
.badge-soon{{background:#fff4d8;color:#9a6800;}}
.badge-selected{{background:var(--primary);color:#fff;}}

.price{{color:var(--primary);font-weight:900;font-size:22px;margin-top:4px;text-align:center;letter-spacing:.1px;}}
.prop-name{{font-size:16.5px;font-weight:800;color:var(--ink);margin-top:6px;text-align:center;}}
.meta{{font-size:11.5px;color:var(--muted);line-height:2;text-align:center;font-weight:600;}}
.views{{font-size:10.5px;color:var(--muted-light);text-align:center;font-weight:600;}}
.reminder-tag{{display:inline-block;margin-top:6px;background:#fff4d8;color:#9a6800;border-radius:999px;padding:4px 10px;font-size:10px;font-weight:800;}}

/* ---------------- Split layout: list + sticky map ---------------- */
[data-testid="stVerticalBlockBorderWrapper"] {{border-radius:var(--radius-lg)!important;}}

/* ---------------- Map / detail ---------------- */
.map-wrap{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:8px;box-shadow:var(--shadow-md);}}
.map-caption{{font-size:11.5px;color:var(--muted);padding:6px 10px 10px;direction:rtl;text-align:right;font-weight:600;}}

.detail-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-lg);direction:rtl;text-align:center;margin-top:12px;}}
.detail-body{{padding:20px;text-align:center;}}
.detail-price{{font-size:32px;color:var(--primary);font-weight:900;text-align:center;letter-spacing:.1px;}}
.detail-title{{font-size:24px;color:var(--ink);font-weight:900;text-align:center;}}
.detail-location{{color:var(--muted);font-size:12.5px;margin:4px 0 12px;text-align:center;font-weight:600;}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--border);border-bottom:1px solid var(--border);margin:14px 0;}}
.stat{{padding:11px 4px;text-align:center;border-left:1px solid var(--border);}}
.stat:last-child{{border-left:0;}}
.stat b{{display:block;font-size:17px;color:var(--ink);font-weight:800;}}
.stat span{{font-size:9.5px;color:var(--muted-light);font-weight:700;}}
.detail-extra{{background:#f6faf9;border:1px solid var(--border);border-radius:var(--radius-md);padding:10px 12px;margin:8px 0;font-size:11.5px;color:var(--muted);text-align:right;font-weight:600;}}

/* ---------------- Gallery ---------------- */
.gallery-wrap{{padding:10px 10px 0;}}
.gallery-main{{position:relative;border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-md);border:1px solid var(--border);aspect-ratio:16/10;background:#eef1ef;}}
.gallery-main img{{width:100%;height:100%;object-fit:cover;object-position:center;display:block;}}
.gallery-counter{{position:absolute;bottom:10px;left:10px;background:rgba(6,22,20,.72);color:#fff;font-size:11px;font-weight:800;padding:5px 12px;border-radius:999px;backdrop-filter:blur(3px);}}
.gallery-badge{{position:absolute;top:10px;right:10px;}}
.thumb{{border-radius:var(--radius-sm);overflow:hidden;border:2px solid var(--border);cursor:pointer;flex:0 0 132px;width:132px;height:98px;box-shadow:var(--shadow-sm);transition:border-color .15s ease, box-shadow .15s ease;}}
.thumb img{{width:100%;height:100%;object-fit:cover;object-position:center;display:block;}}
.thumb.active{{border-color:var(--primary);box-shadow:0 0 0 2px rgba(8,99,90,.15);}}

/* ---------------- About / Contact hero ---------------- */
.page-hero{{height:230px;border-radius:var(--radius-xl);overflow:hidden;position:relative;margin:0 0 20px;color:#fff;background-position:center;background-size:cover;
  background-image:linear-gradient(100deg,rgba(5,25,22,.92) 5%,rgba(8,99,90,.55) 60%,rgba(0,222,186,.30) 100%),linear-gradient(180deg,#9fc4d4 0%,#e8a271 55%,#33484d 100%);
  box-shadow:var(--shadow-lg);display:flex;align-items:center;justify-content:center;text-align:center;direction:rtl;}}
.page-hero-inner{{position:relative;z-index:2;max-width:900px;padding:25px;}}
.page-hero h1{{font-size:46px!important;margin:0 0 12px;color:#fff!important;font-weight:900;text-shadow:0 2px 12px rgba(0,0,0,.35);}}
.page-hero p{{font-size:17px;color:#f0f9f7;margin:0;line-height:2;font-weight:500;}}

/* ---------------- About / Contact ---------------- */
.info-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-xl);padding:32px;box-shadow:var(--shadow-md);direction:rtl;text-align:right;margin-top:16px;}}
.info-card h1{{font-size:38px;color:var(--primary-dark);margin:0 0 12px;font-weight:900;}}
.info-card h2{{font-size:19px;color:var(--ink);margin-top:26px;font-weight:800;}}
.info-card p{{font-size:16.5px;color:var(--muted);line-height:2.1;margin:8px 0;font-weight:500;}}
.contact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:20px 0;}}
.contact-item{{border:1px solid var(--border);border-radius:var(--radius-md);padding:19px;background:#fbfdfc;transition:border-color .15s ease;}}
.contact-item:hover{{border-color:var(--primary-light);}}
.contact-item b{{display:block;color:var(--primary-dark);font-size:12px;margin-bottom:6px;}}
.contact-item a{{color:var(--ink);text-decoration:none;font-size:14.5px;font-weight:700;}}
.footer{{color:var(--muted-light);text-align:center;font-size:10.5px;padding:26px 0 6px;font-weight:600;}}

/* ---------------- Empty state ---------------- */
.empty-state{{background:var(--surface);border:1.5px dashed var(--border);border-radius:var(--radius-lg);padding:40px 20px;text-align:center;color:var(--muted);font-weight:600;}}
.empty-state .icon{{font-size:34px;margin-bottom:8px;}}

@media(max-width:1200px){{.hero-copy h1{{font-size:27px;}}.page-hero h1{{font-size:38px!important;}}}}

/* ---------------- Mobile (phones/small tablets) ---------------- */
@media(max-width:850px){{
  .block-container{{padding:.5rem .6rem 2rem!important;}}
  .hero{{height:auto;min-height:190px}}
  .hero-inner{{flex-direction:column;align-items:stretch;padding:14px;gap:14px;}}
  .hero-copy h1{{font-size:22px;}}
  .hero-copy p{{font-size:12.5px;}}
  .hero-stats{{width:100%;min-width:0;}}
  .hero-stat{{padding:10px 8px;min-width:0;}}
  .hero-stat b{{font-size:16px;}}
  .contact-grid{{grid-template-columns:1fr;}}
  .stats{{grid-template-columns:repeat(2,1fr);}}
  .page-hero{{height:auto;min-height:170px;padding:10px;}}
  .page-hero h1{{font-size:26px!important;}}
  .page-hero p{{font-size:13px!important;}}
  .info-card{{padding:18px;}}
  .info-card h1{{font-size:24px;}}

  /* Top nav: keep it one compact scrollable row instead of Streamlit's
     default stacking (which would turn 8 columns into 8 tall full-width
     buttons). */
  div[class*="st-key-topbar_wrap"]{{padding:8px 10px;}}
  div[class*="st-key-topbar_wrap"] [data-testid="stHorizontalBlock"]{{flex-wrap:nowrap!important;overflow-x:auto;gap:6px!important;-webkit-overflow-scrolling:touch;}}
  div[class*="st-key-topbar_wrap"] [data-testid="column"]{{min-width:max-content!important;width:auto!important;flex:0 0 auto!important;}}
  .brand-logo{{width:52px!important;height:52px!important;border-radius:12px!important;}}
  .brand-mark{{width:44px!important;height:44px!important;font-size:20px!important;}}
  .brand-title{{font-size:18px!important;}}
  .brand-sub{{display:none;}}
  div[class*="st-key-nav_"] .stButton>button,div[class*="st-key-navactive_"] .stButton>button{{font-size:12px!important;padding:0 9px!important;min-height:34px!important;white-space:nowrap;}}
  div[class*="st-key-navcta_"] .stButton>button,div[class*="st-key-navlogin_"] .stButton>button{{font-size:11px!important;padding:0 10px!important;min-height:34px!important;white-space:nowrap;}}
}}
@media(max-width:480px){{
  .brand-title{{font-size:16px!important;}}
  .price{{font-size:18px;}}
  .detail-price{{font-size:26px;}}
  .detail-title{{font-size:19px;}}
  .thumb{{flex:0 0 100px;width:100px;height:74px;}}
}}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# Data
# ============================================================
RIYADH = {
    "الملقا": (24.8184, 46.6122),
    "النفل": (24.7767, 46.6617),
    "الروضة": (24.7276, 46.7675),
    "السويدي": (24.5755, 46.6767),
    "الشفا": (24.5487, 46.6960),
    "المصيف": (24.7440, 46.6780),
    "القدس": (24.7615, 46.7830),
}

# id, category, type, district, deal, status, price, area, beds, baths, age, lat, lon, views
DEMO = [
    [10001,"سكني","فيلا","المصيف","للبيع","متاح",1850000,488,5,3,8,24.7440,46.6780,1248],
    [10002,"سكني","دور","النفل","للبيع","متاح قريبًا",1250000,310,4,3,6,24.7767,46.6617,893],
    [10003,"سكني","فيلا","الملقا","للبيع","تم البيع",2650000,520,4,5,10,24.8184,46.6122,1734],
    [10004,"سكني","شقة","السويدي","للإيجار","متاح",42000,142,2,3,1,24.5755,46.6767,612],
    [10005,"سكني","فيلا","الشفا","للبيع","متاح",1480000,410,3,5,7,24.5487,46.6960,982],
    [10006,"سكني","دور","الروضة","للبيع","متاح",1320000,335,3,4,6,24.7276,46.7675,1204],
    [10007,"سكني","شقة","القدس","للإيجار","تم التأجير",55000,165,2,3,2,24.7615,46.7830,721],
    [10008,"سكني","فيلا","الملقا","للبيع","متاح",3150000,610,5,7,11,24.8200,46.6160,2281],
    [10009,"سكني","شقة","المصيف","للبيع","متاح",890000,118,2,2,2,24.7480,46.6810,534],
    [10010,"سكني","دور","الروضة","للبيع","متاح",1590000,390,3,4,7,24.7310,46.7710,1057],
    [10011,"سكني","فيلا","النفل","للبيع","متاح",2290000,460,4,5,8,24.7790,46.6650,1450],
    [10012,"سكني","شقة","الشفا","للإيجار","مؤجر",36000,128,2,2,2,24.5520,46.7000,449],
    [10013,"تجاري","محل","الملقا","للإيجار","متاح",95000,86,0,1,3,24.8175,46.6108,638],
    [10014,"تجاري","مكتب","الروضة","للإيجار","متاح قريبًا",72000,120,0,2,4,24.7290,46.7688,421],
    [10015,"تجاري","معرض","النفل","للبيع","متاح",1850000,310,0,2,6,24.7758,46.6609,887],
    [10016,"تجاري","مستودع","الشفا","للإيجار","مؤجر",140000,540,0,2,8,24.5512,46.6981,304],
]
df = pd.DataFrame(DEMO, columns=["id","category","type","district","deal","status","price","area","beds","baths","age","lat","lon","views"])

# Optional extra info (contract / availability) — used only when present, does not affect existing schema
EXTRA_INFO = {
    10007: {"contract_remaining": "6 أشهر متبقية على العقد"},
    10012: {"contract_remaining": "10 أشهر متبقية على العقد"},
    10016: {"contract_remaining": "3 أشهر متبقية على العقد"},
    10002: {"available_from": "متاح للبيع خلال 30 يومًا"},
    10014: {"available_from": "متاح للإيجار خلال أسبوعين"},
}

# ============================================================
# Assets — deterministic numbered-image system
#   1-9   -> صور خارجية للبيوت السكنية (فيلا/دور/شقة)
#   10-14 -> صور داخلية للبيوت السكنية
#   15-16 -> صور مستودعات
#   17    -> صورة محل
#   18    -> صورة عمارة
# ============================================================
BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
RESIDENTIAL_TYPES = {"فيلا", "دور", "شقة"}
EXTERIOR_RANGE = list(range(1, 10))     # 1-9
INTERIOR_RANGE = list(range(10, 15))    # 10-14
WAREHOUSE_RANGE = [15, 16]
SHOP_NUM = 17
BUILDING_NUM = 18


def _is_excluded(name: str) -> bool:
    n = name.lower()
    return any(x in n for x in ("logo", "hero", "riyadh", "skyline"))


@st.cache_data(show_spinner=False)
def _numbered_image_map():
    """Scan assets/ once and map: number -> list[Path] whose filename contains that number
    (e.g. '3.jpg', 'image_3.jpg', 'property_3.png' all map to number 3).
    Cached so this full-folder scan runs once per session instead of on every rerun
    (every button click / filter change triggers a Streamlit rerun)."""
    mapping = {}
    if not ASSETS.exists():
        return mapping
    for p in ASSETS.rglob("*"):
        if not (p.is_file() and p.suffix.lower() in IMAGE_EXTS):
            continue
        if _is_excluded(p.name):
            continue
        digits = "".join(ch for ch in p.stem if ch.isdigit())
        if not digits:
            continue
        try:
            n = int(digits)
        except ValueError:
            continue
        mapping.setdefault(n, []).append(p)
    return mapping


NUMBERED_IMAGES = _numbered_image_map()


def svg_placeholder(prop, index=0):
    """Professional placeholder illustration used only when a required numbered
    image is missing from assets/, so the gallery never looks empty."""
    title = html.escape(f"{prop['type']} في حي {prop['district']}")
    palettes = [
        ("#244e42", "#b99963"),
        ("#08635a", "#00deba"),
        ("#0f2f2a", "#c9973e"),
        ("#054a43", "#8fd6c4"),
    ]
    c1, c2 = palettes[index % len(palettes)]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700"><defs><linearGradient id="g{index}" x1="0" x2="1"><stop stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="1200" height="700" fill="#eef1ef"/><rect width="1200" height="700" fill="url(#g{index})" opacity=".20"/><rect x="170" y="300" width="860" height="280" rx="8" fill="#f6f3ec" stroke="#87765c" stroke-width="5"/><polygon points="120,310 600,70 1080,310" fill="#c8aa78" stroke="#766249" stroke-width="5"/><rect x="520" y="405" width="160" height="175" fill="#5c4637"/><rect x="280" y="380" width="150" height="110" fill="#9fc6d5"/><rect x="770" y="380" width="150" height="110" fill="#9fc6d5"/><text x="600" y="640" text-anchor="middle" font-family="Arial" font-size="38" fill="#23352f">{title}</text></svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


@st.cache_data(show_spinner=False)
def _read_and_encode_image(path_str: str, mtime: float) -> str:
    """يقرأ الصورة ويحوّلها base64 مرة واحدة فقط، ثم يخزّن الناتج مؤقتًا (cache).
    بدون هذا الـ cache كانت كل صورة (رئيسية + كل صورة مصغّرة) تُقرأ من القرص
    وتُحوَّل base64 من جديد مع كل rerun — أي مع كل ضغطة زر بالتطبيق — وهذا
    كان سبب البطء الملحوظ عند فتح بطاقة تفاصيل العقار. مُعامل mtime يجعل
    الكاش يتحدّث تلقائيًا لو تغيّر ملف الصورة على القرص."""
    p = Path(path_str)
    ext = p.suffix.lower().replace(".", "") or "jpeg"
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64," + base64.b64encode(p.read_bytes()).decode()


def img_src(path_or_uri):
    """Convert a local file path to a base64 data URI (needed for raw HTML rendering).
    Data URIs / already-encoded strings pass through unchanged."""
    if path_or_uri.startswith("data:"):
        return path_or_uri
    p = Path(path_or_uri)
    try:
        return _read_and_encode_image(str(p), p.stat().st_mtime)
    except Exception:
        return path_or_uri


def images_for_property(prop):
    """Deterministic (seeded by property id, so it never changes between reruns)
    image selection that follows the asset numbering rules:
      - فيلا/دور/شقة : 1 exterior image (1-9) + 3 distinct interior images (10-14)
      - مستودع        : warehouse images (15-16) only
      - محل           : shop image (17) only
      - عمارة         : building image (18) only
      - other (مكتب/معرض/أرض) : a single generic exterior-style image (1-9)
    Falls back to a themed placeholder for any slot with no matching asset,
    so the gallery is always complete and never mixes categories."""
    pid = int(prop["id"])
    ptype = prop["type"]
    rng = random.Random(pid)
    picks = []  # list of Path or None

    def pick_one(number):
        pool = NUMBERED_IMAGES.get(number)
        return rng.choice(pool) if pool else None

    if ptype == "مستودع":
        for n in WAREHOUSE_RANGE:
            picks.append(pick_one(n))
    elif ptype == "محل":
        picks.append(pick_one(SHOP_NUM))
    elif ptype == "عمارة":
        picks.append(pick_one(BUILDING_NUM))
    elif ptype in RESIDENTIAL_TYPES:
        ext_candidates = [n for n in EXTERIOR_RANGE if NUMBERED_IMAGES.get(n)]
        picks.append(pick_one(rng.choice(ext_candidates)) if ext_candidates else None)
        int_candidates = [n for n in INTERIOR_RANGE if NUMBERED_IMAGES.get(n)]
        rng.shuffle(int_candidates)
        chosen = int_candidates[:MAX_INTERIOR]
        for n in chosen:
            picks.append(pick_one(n))
        while len(picks) < 1 + MAX_INTERIOR:
            picks.append(None)
    else:
        # مكتب / معرض / أرض / غير مصنف: صورة تمثيلية واحدة فقط
        ext_candidates = [n for n in EXTERIOR_RANGE if NUMBERED_IMAGES.get(n)]
        picks.append(pick_one(rng.choice(ext_candidates)) if ext_candidates else None)

    images = []
    for i, p in enumerate(picks):
        images.append(str(p) if p else svg_placeholder(prop, i))
    if not images:
        images.append(svg_placeholder(prop, 0))
    return images


def img_for(prop, index=0):
    imgs = images_for_property(prop)
    return imgs[index % len(imgs)]


# Logo — logo.png (the current design) takes priority; legacy filenames from
# earlier project versions are only used as a fallback if logo.png is absent.
logo_candidates = [
    ASSETS / "logo.png",
    ASSETS / "Logo_Mostaksheef.jpeg",
    ASSETS / "Logo_Mostakshif.jpeg",
    ASSETS / "logo_mostaksheef.jpeg",
]
logo_path = next((p for p in logo_candidates if p.exists()), None)


@st.cache_data(show_spinner=False)
def _encode_logo(path_str: str) -> str:
    p = Path(path_str)
    ext = p.suffix.lower().replace(".", "") or "png"
    return f'data:image/{ext};base64,{base64.b64encode(p.read_bytes()).decode()}'


def logo_html():
    if logo_path:
        return f'<img class="brand-logo" src="{_encode_logo(str(logo_path))}">'
    return '<div class="brand-mark">⌂</div>'


# Hero image search, recursively
hero_candidates = []
if ASSETS.exists():
    hero_candidates = [
        p for p in ASSETS.rglob("*")
        if p.is_file()
        and p.suffix.lower() in IMAGE_EXTS
        and any(x in p.name.lower() for x in ["hero", "riyadh", "skyline"])
    ]
    # If multiple matches exist (e.g. a leftover file from an earlier version),
    # the most recently modified one wins instead of an arbitrary filesystem order.
    hero_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
hero_path = hero_candidates[0] if hero_candidates else None


@st.cache_data(show_spinner=False)
def _encode_hero(path_str: str) -> str:
    return base64.b64encode(Path(path_str).read_bytes()).decode()


hero_style = ""
if hero_path:
    hero_b64 = _encode_hero(str(hero_path))
    hero_style = f"background-image:linear-gradient(100deg,rgba(5,25,22,.90) 5%,rgba(8,99,90,.55) 60%,rgba(0,222,186,.28) 100%),url(data:image/{hero_path.suffix[1:]};base64,{hero_b64});"

# ============================================================
# State + query params
# ============================================================
DEFAULT_STATE = {
    "selected_id": None,  # لا يوجد عقار محدد افتراضيًا — المستخدم هو من يختار
    "favorites": set(),
    "reminders": set(),
    "page": 1,
    "user_lat": None,
    "user_lon": None,
    "last_map_click": None,
    "gallery_index": 0,
    "gallery_property": None,
    "show_filters": True,
    "keep_selection_once": False,
}
for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

FILTER_DEFAULTS = {
    "category": "الكل",
    "kind": "الكل",
    "deal": "الكل",
    "district": "الكل",
    "status": "الكل",
    "sort": "الأحدث",
    "min_price": 0,
    "max_price": 50_000_000,
    "beds": "الكل",
    "baths": "الكل",
    "age": "الكل",
    "distance": "الكل",
    "main_search": "",
}

# --- Reset-filters must run BEFORE any widget bound to these keys is created,
#     otherwise Streamlit raises "session_state cannot be modified after the
#     widget is instantiated" and the whole page crashes. A one-shot flag set
#     by the reset button (see below) is consumed here, at the very top. ---
if st.session_state.get("_do_reset_filters"):
    for key_name, default_val in FILTER_DEFAULTS.items():
        st.session_state[key_name] = default_val
    st.session_state.page = 1
    st.session_state.last_map_click = None
    st.session_state["_do_reset_filters"] = False

st.session_state.setdefault("view", "home")

params = st.query_params
view = params.get("view") or st.session_state.view
if view not in {"home", "map", "search", "favorites", "about", "contact"}:
    view = "home"
st.session_state.view = view

try:
    if params.get("user_lat") and params.get("user_lon"):
        st.session_state.user_lat = float(params.get("user_lat"))
        st.session_state.user_lon = float(params.get("user_lon"))
except Exception:
    pass

if params.get("property"):
    try:
        new_pid = int(params.get("property"))
        if new_pid != st.session_state.selected_id:
            st.session_state.gallery_index = 0
        st.session_state.selected_id = new_pid
    except Exception:
        pass


def toggle_favorite(pid: int):
    """Single source of truth for favorite state — avoids duplicates and keeps
    the favorites page, nav counter and card hearts perfectly in sync."""
    pid = int(pid)
    favs = st.session_state.favorites
    if not isinstance(favs, set):
        favs = set(favs)
    if pid in favs:
        favs.discard(pid)
    else:
        favs.add(pid)
    st.session_state.favorites = favs


def toggle_reminder(pid: int):
    pid = int(pid)
    rem = st.session_state.reminders
    if not isinstance(rem, set):
        rem = set(rem)
    if pid in rem:
        rem.discard(pid)
    else:
        rem.add(pid)
    st.session_state.reminders = rem


active = view
location_qs = ""
if st.session_state.user_lat is not None and st.session_state.user_lon is not None:
    location_qs = f"&user_lat={st.session_state.user_lat:.7f}&user_lon={st.session_state.user_lon:.7f}"

# ============================================================
# Header — real Streamlit buttons switch the view in-place (no browser
# navigation, no full page reload, session state such as Favorites is
# never lost). Visual styling comes from the CSS rules on st-key-nav_* above.
# ============================================================
def go_to(new_view: str):
    st.session_state.view = new_view
    st.query_params["view"] = new_view
    st.rerun()


try:
    _topbar_ctx = st.container(key="topbar_wrap")
except TypeError:
    # Older Streamlit versions (<1.32) don't support container(key=...).
    _topbar_ctx = st.container()

with _topbar_ctx:
    b_col, n1, n2, n3, n4, spacer, a1, a2 = st.columns([2.9, 0.85, 1.05, 1.05, 1.05, 1.1, 1.15, 1.25])
    with b_col:
        st.markdown(f'<div class="brand">{logo_html()}<div><div class="brand-title">مستكشف</div><div class="brand-sub">اكتشف عقارات • بسهولة وذكاء</div></div></div>', unsafe_allow_html=True)
    nav_items = [
        (n1, "home", "الرئيسية"),
        (n2, "favorites", f"المفضلة {len(st.session_state.favorites) if st.session_state.favorites else ''}".strip()),
        (n3, "about", "حول المنصة"),
        (n4, "contact", "تواصل معنا"),
    ]
    for col, target, label in nav_items:
        with col:
            key_prefix = "navactive_" if active == target else "nav_"
            if st.button(label, key=f"{key_prefix}{target}", use_container_width=True):
                go_to(target)
    with a1:
        if st.button("＋ أضف عقارك", key="navcta_add", use_container_width=True):
            go_to("contact")
    with a2:
        if st.button("👤 تسجيل الدخول", key="navlogin_in", use_container_width=True):
            go_to("contact")

# ============================================================
# About / Contact pages — no map
# ============================================================
if active == "about":
    st.markdown('''<div class="page-hero"><div class="page-hero-inner"><h1>عن مستكشف</h1><p>منصة عقارية ذكية تجمع البحث، المقارنة، الخريطة، والمسافة في تجربة واحدة تساعدك على الوصول للعقار المناسب بثقة ووضوح.</p></div></div>''', unsafe_allow_html=True)
    st.markdown('''<div class="info-card">
        <h1>مستكشف — نقرّب لك العقار المناسب</h1>
        <p><b>مستكشف</b> منصة عقارية صُممت لتجعل رحلة البحث عن العقار أبسط وأسرع وأكثر ذكاءً.</p>
        <p>بدل التنقل بين الإعلانات، تستطيع استكشاف العقارات، معرفة الأسعار والمواصفات، مشاهدة عدد مرات مشاهدة الإعلان، وحساب المسافة من موقعك المحفوظ تلقائيًا.</p>
        <p>هدفنا أن تتحول بيانات العقار من معلومات متفرقة إلى قرار واضح يساعد الباحث والمستثمر والمالك.</p>
        <h2>ابحث بذكاء… قارن بسهولة… واتخذ قرارك بثقة.</h2>
        </div>''', unsafe_allow_html=True)
    st.markdown('<div class="footer">مستكشف © 2026 — منصة عقارية تجريبية</div>', unsafe_allow_html=True)
    st.stop()

if active == "contact":
    st.markdown('''<div class="page-hero"><div class="page-hero-inner"><h1>تواصل معنا</h1><p>نرحب باستفساراتك ومقترحاتك وإضافاتك العقارية، ويسعدنا أن نسمع منك.</p></div></div>''', unsafe_allow_html=True)
    st.markdown('''<div class="info-card">
        <h1>تواصل معنا</h1>
        <p>هل لديك استفسار، اقتراح، أو ترغب في إضافة عقارك إلى مستكشف؟ تواصل معنا مباشرة.</p>
        <div class="contact-grid">
          <div class="contact-item"><b>📞 الهاتف</b><a href="tel:+966501740434">+966 50 174 0434</a></div>
          <div class="contact-item"><b>✉️ البريد الإلكتروني</b><a href="mailto:Fahd.s.alaskar@gmail.com">Fahd.s.alaskar@gmail.com</a></div>
        </div>
        <h2>لتواصل معي</h2>
        </div>''', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("💬 واتساب", "https://wa.me/966501740434", use_container_width=True)
    with c2:
        st.link_button("📧 إرسال بريد إلكتروني", "mailto:Fahd.s.alaskar@gmail.com", use_container_width=True)
    st.markdown('<div class="footer">نسعد بملاحظاتكم ومقترحاتكم لتطوير مستكشف.</div>', unsafe_allow_html=True)
    st.stop()

# ============================================================
# Hero — visual only, search removed
# ============================================================
st.markdown(
    f'''<div class="hero" style="{hero_style}" dir="rtl"><div class="hero-inner">
      <div class="hero-copy"><h1>اكتشف العقار المناسب لك</h1><p>خريطة عقارية تفاعلية، فلاتر ذكية، ومسافة دقيقة من موقعك.</p></div>
      <div class="hero-stats"><div class="hero-stat"><b>142,890</b><span>عملية هذا الأسبوع</span></div><div class="hero-stat"><b>21,458</b><span>عقار متاح الآن</span></div><div class="hero-stat"><b>542,180</b><span>عدد المشاهدات</span></div></div>
    </div></div>''',
    unsafe_allow_html=True,
)


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))

# ============================================================
# Search + Filters — الرئيسية / الخريطة فقط
# ============================================================
search = ""
if active in {"map", "home"}:
    if active == "home":
        search_value = st.query_params.get("q", "")
        st.markdown('<div class="searchbar">', unsafe_allow_html=True)
        search = st.text_input(
            "البحث",
            value=search_value,
            placeholder="🔍 ابحث بالحي، نوع العقار، أو رقم الإعلان — مثال: فيلا في الملقا",
            label_visibility="collapsed",
            key="main_search",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    tcol1, tcol2 = st.columns([5, 1.3])
    with tcol2:
        toggle_label = "🙈 إخفاء الفلاتر" if st.session_state.show_filters else "👁 إظهار الفلاتر"
        if st.button(toggle_label, key="toggle_filters", use_container_width=True):
            st.session_state.show_filters = not st.session_state.show_filters
            st.rerun()

    if st.session_state.show_filters:
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        st.markdown('<div class="filter-heading">🎛️ الفلاتر <span>ابحث بدقة عن العقار المناسب لك</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-sep"></div>', unsafe_allow_html=True)
        f1 = st.columns(5)
        with f1[0]: category = st.selectbox("التصنيف", ["الكل", "سكني", "تجاري"], key="category")
        with f1[1]: kind = st.selectbox("نوع العقار", ["الكل", "فيلا", "دور", "شقة", "أرض", "محل", "مكتب", "معرض", "مستودع", "عمارة"], key="kind")
        with f1[2]: deal = st.selectbox("نوع العملية", ["الكل", "للبيع", "للإيجار"], key="deal")
        with f1[3]: district = st.selectbox("الحي", ["الكل"] + list(RIYADH.keys()), key="district")
        with f1[4]: status = st.selectbox("حالة الإعلان", ["الكل", "متاح", "متاح قريبًا", "مؤجر", "تم التأجير", "تم البيع"], key="status")
        f2 = st.columns(5)
        with f2[0]: sort = st.selectbox("ترتيب النتائج", ["الأحدث", "الأقل سعرًا", "الأعلى سعرًا", "الأكثر مشاهدة", "الأقرب إليك"], key="sort")
        with f2[1]: min_price = st.number_input("السعر من (ريال)", min_value=0, max_value=50_000_000, value=st.session_state.get("min_price", 0), step=50_000, key="min_price")
        with f2[2]: max_price = st.number_input("السعر إلى (ريال)", min_value=0, max_value=50_000_000, value=st.session_state.get("max_price", 50_000_000), step=50_000, key="max_price")
        with f2[3]: beds = st.selectbox("عدد غرف النوم", ["الكل", "1", "2", "3", "4", "5+"], key="beds")
        with f2[4]: baths = st.selectbox("عدد دورات المياه", ["الكل", "1", "2", "3", "4", "5+"], key="baths")
        f3 = st.columns(3)
        with f3[0]:
            max_age = st.selectbox("عمر العقار حتى (سنة)", ["الكل", 1, 3, 5, 10, 20], key="age")
            max_age = 100 if max_age == "الكل" else int(max_age)
        with f3[1]: distance_filter = st.selectbox("المسافة من موقعي", ["الكل", "1 كم", "3 كم", "5 كم", "10 كم", "20 كم"], key="distance")
        with f3[2]:
            st.markdown('<div class="filter-tip">💡 يمكنك الجمع بين أكثر من فلتر للوصول للنتيجة الأدق.</div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-sep"></div>', unsafe_allow_html=True)
        c_apply, c_reset = st.columns([4, 1.3])
        with c_apply:
            if st.button("🔎  تطبيق الفلاتر", use_container_width=True, key="apply_filters", type="primary"):
                st.session_state.page = 1
                st.rerun()
        with c_reset:
            if st.button("↻ إعادة تعيين الفلاتر", use_container_width=True, key="reset_filters"):
                st.session_state["_do_reset_filters"] = True
                try:
                    if "q" in st.query_params:
                        del st.query_params["q"]
                except Exception:
                    pass
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        category = st.session_state.get("category", "الكل")
        kind = st.session_state.get("kind", "الكل")
        deal = st.session_state.get("deal", "الكل")
        district = st.session_state.get("district", "الكل")
        status = st.session_state.get("status", "الكل")
        sort = st.session_state.get("sort", "الأحدث")
        min_price = st.session_state.get("min_price", 0)
        max_price = st.session_state.get("max_price", 50_000_000)
        beds = st.session_state.get("beds", "الكل")
        baths = st.session_state.get("baths", "الكل")
        max_age_raw = st.session_state.get("age", "الكل")
        max_age = 100 if max_age_raw == "الكل" else int(max_age_raw)
        distance_filter = st.session_state.get("distance", "الكل")
else:
    category, kind, deal, district, status, sort = "الكل", "الكل", "الكل", "الكل", "الكل", "الأحدث"
    min_price, max_price, beds, baths, max_age, distance_filter = 0, 50_000_000, "الكل", "الكل", 100, "الكل"

# ============================================================
# Filtering
# ============================================================
filtered = df.copy()
q = (search or "").strip()
if q:
    filtered = filtered[
        filtered["district"].str.contains(q, case=False, na=False)
        | filtered["type"].str.contains(q, case=False, na=False)
        | filtered["id"].astype(str).str.contains(q, na=False)
    ]
if category != "الكل":
    filtered = filtered[filtered.category == category]
if kind != "الكل":
    filtered = filtered[filtered.type == kind]
if deal != "الكل":
    filtered = filtered[filtered.deal == deal]
if district != "الكل":
    filtered = filtered[filtered.district == district]
if status != "الكل":
    filtered = filtered[filtered.status == status]
if beds != "الكل":
    filtered = filtered[filtered.beds >= 5 if beds == "5+" else filtered.beds == int(beds)]
if baths != "الكل":
    filtered = filtered[filtered.baths >= 5 if baths == "5+" else filtered.baths == int(baths)]
filtered = filtered[(filtered.price >= min_price) & (filtered.price <= max_price) & (filtered.age <= max_age)].copy()

if st.session_state.user_lat is not None and st.session_state.user_lon is not None:
    filtered["distance_km"] = filtered.apply(lambda x: haversine_km(st.session_state.user_lat, st.session_state.user_lon, x.lat, x.lon), axis=1)
else:
    filtered["distance_km"] = float("nan")

if distance_filter != "الكل" and filtered.distance_km.notna().any():
    filtered = filtered[filtered.distance_km <= int(distance_filter.split()[0])]

if sort == "الأقل سعرًا":
    filtered = filtered.sort_values("price")
elif sort == "الأعلى سعرًا":
    filtered = filtered.sort_values("price", ascending=False)
elif sort == "الأكثر مشاهدة":
    filtered = filtered.sort_values("views", ascending=False)
elif sort == "الأقرب إليك" and filtered.distance_km.notna().any():
    filtered = filtered.sort_values("distance_km")
else:
    filtered = filtered.sort_values("id", ascending=False)

if active == "favorites":
    filtered = filtered[filtered.id.isin(st.session_state.favorites)]

# لا نختار عقارًا تلقائيًا بعد الفلترة — فقط نلغي التحديد الحالي إذا لم يعد
# ضمن النتائج المفلترة (حتى لا تبقى بطاقة تفاصيل لعقار غير ظاهر بالقائمة).
keep_once = st.session_state.pop("keep_selection_once", False)
if not keep_once and st.session_state.selected_id is not None and st.session_state.selected_id not in set(filtered.id):
    st.session_state.selected_id = None
    st.session_state.gallery_index = 0

PAGE_SIZE = 12
pages = max(1, math.ceil(len(filtered) / PAGE_SIZE))
st.session_state.page = min(st.session_state.page, pages)
start = (st.session_state.page - 1) * PAGE_SIZE
page_df = filtered.iloc[start:start + PAGE_SIZE]

# ============================================================
# Helpers
# ============================================================
def badge(p, extra_class=""):
    status = p["status"]
    if status == "تم البيع":
        cls = "badge-sold"
    elif status in ["مؤجر", "تم التأجير"]:
        cls = "badge-leased"
    elif status == "متاح قريبًا":
        cls = "badge-soon"
    elif p["deal"] == "للإيجار":
        cls = "badge-rent"
    else:
        cls = ""
    label = status if status != "متاح" else p["deal"]
    return f'<span class="badge {cls} {extra_class}">{html.escape(label)}</span>'


def render_property_card(p, compact=False):
    pid = int(p["id"])
    img = img_for(p, 0)
    photo_count = len(images_for_property(p))
    fav = "♥" if pid in st.session_state.favorites else "♡"
    is_selected = st.session_state.selected_id is not None and pid == int(st.session_state.selected_id)
    dtext = f' • 📍 {p["distance_km"]:.1f} كم من موقعك' if pd.notna(p.get("distance_km")) else ""
    card_cls = "property-card is-selected" if (compact and is_selected) else "property-card"
    st.markdown(f'<div class="{card_cls}">', unsafe_allow_html=True)
    c1, c2 = st.columns([1.05, 2.0])
    with c1:
        st.image(img, use_container_width=True)
        st.markdown(f'<div style="text-align:center"><span class="photo-count">📷 {photo_count} صور</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(badge(p, "badge-selected" if (compact and is_selected) else ""), unsafe_allow_html=True)
        st.markdown(f'<div class="prop-name">{html.escape(p["type"])} — {html.escape(p["district"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price">{p["price"]:,} ريال</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meta">🛏 {p["beds"]} غرف • 🛁 {p["baths"]} دورات مياه • 📐 {p["area"]} م²{dtext}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="views">👁 {p["views"]:,} مشاهدة • إعلان #{pid}</div>', unsafe_allow_html=True)
        if p["status"] == "متاح قريبًا":
            is_on = pid in st.session_state.reminders
            if is_on:
                st.markdown('<div class="reminder-tag">🔔 تم تفعيل التذكير</div>', unsafe_allow_html=True)

    if compact:
        b1, b2, b3 = st.columns([2, 1.1, 1.1])
        with b1:
            btn_label = "★ محدد على الخريطة" if is_selected else "عرض على الخريطة"
            if st.button(btn_label, key=f"open_{pid}", use_container_width=True, disabled=is_selected):
                st.session_state.selected_id = pid
                st.session_state.gallery_index = 0
                st.session_state.keep_selection_once = True
                st.rerun()
        with b2:
            if st.button(fav, key=f"fav_{pid}", use_container_width=True, help="أضف/أزل من المفضلة"):
                toggle_favorite(pid)
                st.rerun(scope="app")
        with b3:
            if p["status"] == "متاح قريبًا":
                if st.button("🔔", key=f"rem_{pid}", use_container_width=True, help="ذكرني عند التوفر"):
                    toggle_reminder(pid)
                    st.rerun()
    else:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("عرض العقار", key=f"viewprop_{pid}", use_container_width=True):
                st.session_state.selected_id = pid
                st.session_state.gallery_index = 0
                st.session_state.keep_selection_once = True
                go_to("map")
        with b2:
            if st.button(f"{fav} المفضلة", key=f"fav_{pid}", use_container_width=True):
                toggle_favorite(pid)
                st.rerun(scope="app")
        if p["status"] == "متاح قريبًا":
            is_on = pid in st.session_state.reminders
            rlabel = "🔕 إلغاء التذكير" if is_on else "🔔 ذكرني عند التوفر"
            if st.button(rlabel, key=f"remb_{pid}", use_container_width=True):
                toggle_reminder(pid)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Results-only pages: search / favorites
# ============================================================
if active in {"search", "favorites"}:
    title = "نتائج البحث" if active == "search" else "المفضلة"
    if active == "favorites" and not st.session_state.favorites:
        st.markdown('<div class="results-heading"><h2>المفضلة</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="empty-state"><div class="icon">🤍</div>لم تحفظ أي عقار في المفضلة حتى الآن.<br>تصفح العقارات واضغط «♡ المفضلة» لحفظها هنا.</div>', unsafe_allow_html=True)
    elif filtered.empty:
        st.markdown(f'<div class="results-heading"><h2>{title} <span>0 عقار</span></h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="empty-state"><div class="icon">🔍</div>لا توجد نتائج مطابقة لبحثك أو فلاترك الحالية.<br>جرّب تعديل الفلاتر أو الضغط على «↻ إعادة تعيين الفلاتر».</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="results-heading"><h2>{title} <span>{len(filtered)} عقار</span></h2><div class="result-note">عرض {start+1 if len(filtered) else 0}–{min(start+PAGE_SIZE,len(filtered))} من {len(filtered)}</div></div>', unsafe_allow_html=True)
        for _, row in page_df.iterrows():
            render_property_card(row.to_dict())
        if pages > 1:
            pc1, pc2, pc3 = st.columns([1, 2, 1])
            with pc1:
                if st.button("التالي →", disabled=st.session_state.page >= pages, key="next_results", use_container_width=True):
                    st.session_state.page += 1
                    st.rerun()
            with pc2:
                st.markdown(f'<div style="text-align:center;padding:10px;font-size:11px;color:#66757b">صفحة {st.session_state.page} من {pages}</div>', unsafe_allow_html=True)
            with pc3:
                if st.button("← السابق", disabled=st.session_state.page <= 1, key="prev_results", use_container_width=True):
                    st.session_state.page -= 1
                    st.rerun()
    st.markdown('<div class="footer">مستكشف © 2026 — منصة عقارية تجريبية</div>', unsafe_allow_html=True)
    st.stop()

# ============================================================
# Home / Map: list (scrollable) + sticky map & details
# ============================================================
if filtered.empty:
    st.markdown('<div class="results-heading"><h2>نتائج البحث <span>0 عقار</span></h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="empty-state"><div class="icon">🔍</div>لا توجد عقارات مطابقة للفلاتر الحالية.<br>جرّب توسيع نطاق البحث أو اضغط «↻ إعادة تعيين الفلاتر» أعلاه.</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">مستكشف © 2026 — منصة عقارية تجريبية</div>', unsafe_allow_html=True)
    st.stop()

@st.fragment
def render_home_map_section():
    """
    كل القائمة + الخريطة + بطاقة التفاصيل محصورة هنا كـ Streamlit fragment.
    هذا يمنع أي تفاعل داخلها (اختيار عقار، تصفح المعرض، الصفحات، إلخ)
    من إعادة تشغيل الصفحة كاملة (CSS + الهيدر + الفلاتر) — بس هالقسم يعاد
    بناؤه، وهذا يخلي التفاعل أسرع بشكل ملموس مقارنة بإعادة تشغيل الصفحة كلها.
    """
    st.markdown(f'<div class="results-heading"><h2>نتائج البحث <span>{len(filtered)} عقار</span></h2><div class="result-note">القائمة قابلة للتمرير — الخريطة تبقى ثابتة أثناء التصفح</div></div>', unsafe_allow_html=True)

    list_col, map_col = st.columns([1.05, 1.75], gap="medium")

    # ---- Left: scrollable property list ----
    with list_col:
        with st.container(height=760, border=False):
            for _, row in page_df.iterrows():
                render_property_card(row.to_dict(), compact=True)
            if pages > 1:
                pc1, pc2, pc3 = st.columns([1, 2, 1])
                with pc1:
                    if st.button("التالي →", disabled=st.session_state.page >= pages, key="next_list", use_container_width=True):
                        st.session_state.page += 1
                        st.rerun()
                with pc2:
                    st.markdown(f'<div style="text-align:center;padding:10px;font-size:11px;color:#66757b">صفحة {st.session_state.page} من {pages}</div>', unsafe_allow_html=True)
                with pc3:
                    if st.button("← السابق", disabled=st.session_state.page <= 1, key="prev_list", use_container_width=True):
                        st.session_state.page -= 1
                        st.rerun()


    class DistanceControl(MacroElement):
        """One-time browser geolocation control. Coordinates are persisted in URL query params."""
        def __init__(self, target_lat, target_lon, property_id, property_label):
            super().__init__()
            self._name = "DistanceControl"
            self.target_lat = float(target_lat)
            self.target_lon = float(target_lon)
            self.property_id = int(property_id)
            self.property_label = str(property_label)
            self._template = Template(
                """
                {% macro script(this, kwargs) %}
                var mapObject={{this._parent.get_name()}};
                var target=L.latLng({{this.target_lat}},{{this.target_lon}});
                var control=L.control({position:'topleft'});
                control.onAdd=function(map){
                    var div=L.DomUtil.create('div','leaflet-bar leaflet-control');
                    div.style.background='#fff';div.style.padding='8px 11px';div.style.cursor='pointer';div.style.borderRadius='10px';div.style.fontSize='18px';div.title='تحديد موقعي وحساب المسافة';
                    div.innerHTML='📍';
                    L.DomEvent.disableClickPropagation(div);
                    L.DomEvent.on(div,'click',function(){
                        div.innerHTML='⏳';
                        map.locate({setView:false,enableHighAccuracy:true,maximumAge:600000,timeout:15000});
                    });
                    return div;
                }; control.addTo(mapObject);
                mapObject.on('locationfound',function(e){
                    var d=e.latlng.distanceTo(target);var txt=d>=1000?(d/1000).toFixed(2)+' كم':Math.round(d)+' متر';
                    if(window.__msLine)mapObject.removeLayer(window.__msLine);
                    window.__msLine=L.polyline([e.latlng,target],{color:'#08635a',weight:4,opacity:.9,dashArray:'8,8'}).addTo(mapObject);
                    window.__msLine.bindTooltip('المسافة الجوية: '+txt,{permanent:true,direction:'center',className:'distance-label'}).openTooltip();
                    if(window.__userMarker)mapObject.removeLayer(window.__userMarker);
                    window.__userMarker=L.circleMarker(e.latlng,{radius:8,color:'#1678d3',weight:3,fillColor:'#1678d3',fillOpacity:.85}).addTo(mapObject);
                    try{
                        var base=window.parent.location.pathname;
                        var qs=new URLSearchParams(window.parent.location.search);
                        qs.set('view','map');
                        qs.set('user_lat',e.latlng.lat.toFixed(7));
                        qs.set('user_lon',e.latlng.lng.toFixed(7));
                        qs.set('property','{{this.property_id}}');
                        window.parent.location.href=base+'?'+qs.toString();
                    }catch(err){}
                });
                mapObject.on('locationerror',function(){alert('تعذر تحديد موقعك. اسمح للموقع من إعدادات المتصفح ثم حاول مرة أخرى.');});
                {% endmacro %}
                """
            )


    # ---- Right: sticky map + selected-property detail ----
    with map_col:
        st.markdown('<div class="map-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="map-caption">🗺️ اضغط على أي عقار على الخريطة لتحديد بطاقته. استخدم «📍» لتحديد موقعك مرة واحدة وحساب المسافة تلقائيًا.</div>', unsafe_allow_html=True)

        if st.session_state.selected_id is not None:
            selected_rows = filtered[filtered.id == int(st.session_state.selected_id)]
        else:
            selected_rows = pd.DataFrame()
        selected_for_map = selected_rows.iloc[0] if not selected_rows.empty else filtered.iloc[0]
        center = [24.744, 46.68]
        if len(filtered) > 1:
            center = [float(filtered.lat.mean()), float(filtered.lon.mean())]

        # خريطة بطبقة واحدة فقط (OpenStreetMap — أوضح بأسماء الشوارع) بدون
        # LayerControl أو طبقة ثانية، لتخفيف الحمل على كل rerun (كل ضغطة زر
        # بالتطبيق تعيد بناء الخريطة بالكامل من الصفر).
        m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap", control_scale=True, prefer_canvas=True)
        Fullscreen(position="topleft").add_to(m)
        DistanceControl(selected_for_map.lat, selected_for_map.lon, int(selected_for_map.id), f"{selected_for_map.type} — {selected_for_map.district}").add_to(m)

        for _, p in filtered.iterrows():
            selected = st.session_state.selected_id is not None and int(p.id) == int(st.session_state.selected_id)
            popup = f'''<div dir="rtl" style="font-family:Arial;text-align:right;min-width:230px;line-height:1.8">
            <b>{html.escape(p.category)} • {html.escape(p.type)} — {html.escape(p.district)}</b><br>
            <span style="color:#08635a;font-size:18px;font-weight:bold">{p.price:,} ريال</span><br>
            📐 {p.area} م² • 🛏 {p.beds} غرف<br>
            👁 {p.views:,} مشاهدة<br><b>{html.escape(p.status)}</b>
            </div>'''
            folium.Marker(
                [p.lat, p.lon],
                tooltip=f"{'★ ' if selected else ''}{p.type} — {p.district} | {p.price:,} ريال",
                popup=folium.Popup(popup, max_width=300),
                icon=folium.Icon(color="green" if selected else "blue", icon="home", prefix="fa"),
            ).add_to(m)

        # Do not zoom out to a whole region. Keep Riyadh scale.
        if len(filtered) > 1:
            lat_span = float(filtered.lat.max() - filtered.lat.min())
            lon_span = float(filtered.lon.max() - filtered.lon.min())
            if lat_span < 0.8 and lon_span < 0.8:
                m.fit_bounds([[filtered.lat.min(), filtered.lon.min()], [filtered.lat.max(), filtered.lon.max()]], padding=(25, 25))

        map_result = st_folium(m, use_container_width=True, height=430, key="property_map", returned_objects=["last_object_clicked", "last_clicked", "center", "zoom"])
        click = map_result.get("last_object_clicked") if map_result else None
        if click and "lat" in click and "lng" in click and not filtered.empty:
            key = (round(float(click["lat"]), 6), round(float(click["lng"]), 6))
            if key != st.session_state.last_map_click:
                st.session_state.last_map_click = key
                nearest = filtered.assign(_d=filtered.apply(lambda x: haversine_km(float(click["lat"]), float(click["lng"]), x.lat, x.lon), axis=1)).sort_values("_d").iloc[0]
                # last_object_clicked only fires when an actual marker is clicked, so the
                # nearest match is always the marker itself — no distance gate needed here.
                st.session_state.selected_id = int(nearest.id)
                st.session_state.gallery_index = 0
                st.session_state.keep_selection_once = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # ---- Selected property detail, right under the map ----
        if st.session_state.selected_id is None:
            st.markdown(
                '<div class="empty-state"><div class="icon">🏠</div>'
                'اختر عقارًا من القائمة أو اضغط على أي علامة بالخريطة لعرض تفاصيله هنا.'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            rows = df[df.id == int(st.session_state.selected_id)]
            if not rows.empty:
                p = rows.iloc[0].to_dict()
                pid = int(p["id"])

                if st.session_state.gallery_property != pid:
                    st.session_state.gallery_property = pid
                    st.session_state.gallery_index = 0

                images = images_for_property(p)
                gidx = st.session_state.gallery_index % len(images)

                st.markdown('<div class="detail-card">', unsafe_allow_html=True)
                st.markdown('<div class="gallery-wrap">', unsafe_allow_html=True)
                main_src = img_src(images[gidx])
                st.markdown(
                    f'''<div class="gallery-main">
                        <img src="{main_src}">
                        <div class="gallery-badge">{badge(p)}</div>
                        <div class="gallery-counter">📷 {gidx+1} / {len(images)}</div>
                    </div>''',
                    unsafe_allow_html=True,
                )
                if len(images) > 1:
                    nav_prev, nav_label, nav_next = st.columns([1, 2, 1])
                    with nav_prev:
                        if st.button("‹ السابق", key=f"gal_prev_{pid}", use_container_width=True):
                            st.session_state.gallery_index = (gidx - 1) % len(images)
                            st.rerun()
                    with nav_label:
                        st.markdown(f'<div style="text-align:center;padding-top:9px;font-size:11px;color:var(--muted);font-weight:700">معرض الصور • صورة {gidx+1} من {len(images)}</div>', unsafe_allow_html=True)
                    with nav_next:
                        if st.button("التالي ›", key=f"gal_next_{pid}", use_container_width=True):
                            st.session_state.gallery_index = (gidx + 1) % len(images)
                            st.rerun()

                    thumbs_html = '<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:2px 0 6px">'
                    for i, im in enumerate(images):
                        active_cls = " active" if i == gidx else ""
                        thumbs_html += f'<div class="thumb{active_cls}"><img src="{img_src(im)}" loading="lazy"></div>'
                    thumbs_html += '</div>'
                    st.markdown(thumbs_html, unsafe_allow_html=True)

                    thumb_cols = st.columns(len(images))
                    for i, tcol in enumerate(thumb_cols):
                        with tcol:
                            if st.button(f"صورة {i+1}", key=f"thumb_{pid}_{i}", use_container_width=True, type=("primary" if i == gidx else "secondary")):
                                st.session_state.gallery_index = i
                                st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="detail-body">', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-title">{html.escape(p["type"])} — {html.escape(p["district"])}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-price">{p["price"]:,} ريال</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail-location">📍 الرياض — حي {html.escape(p["district"])}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:11px;color:#7b878d">إعلان #{pid} • 👁 {p["views"]:,} مشاهدة</div>', unsafe_allow_html=True)
                st.markdown(f'''<div class="stats"><div class="stat"><b>{p["beds"]}</b><span>غرف نوم</span></div><div class="stat"><b>{p["baths"]}</b><span>دورات مياه</span></div><div class="stat"><b>{p["area"]}</b><span>م²</span></div><div class="stat"><b>{p["age"]}</b><span>سنوات</span></div></div>''', unsafe_allow_html=True)

                extra = EXTRA_INFO.get(pid)
                if extra:
                    if "contract_remaining" in extra:
                        st.markdown(f'<div class="detail-extra">📄 {html.escape(extra["contract_remaining"])}</div>', unsafe_allow_html=True)
                    if "available_from" in extra:
                        st.markdown(f'<div class="detail-extra">🗓️ {html.escape(extra["available_from"])}</div>', unsafe_allow_html=True)

                if st.session_state.user_lat is not None and st.session_state.user_lon is not None:
                    dist = haversine_km(st.session_state.user_lat, st.session_state.user_lon, p["lat"], p["lon"])
                    st.markdown(f'<div style="margin:10px 0;padding:10px;border-radius:12px;background:#eaf7f1;color:var(--primary-dark);font-weight:800;text-align:center">📍 يبعد العقار عن موقعك {dist:.2f} كم</div>', unsafe_allow_html=True)

                if p["status"] == "متاح قريبًا":
                    is_on = pid in st.session_state.reminders
                    rlabel = "🔕 إلغاء التذكير" if is_on else "🔔 ذكرني عند التوفر"
                    if st.button(rlabel, key=f"detail_rem_{pid}", use_container_width=True):
                        toggle_reminder(pid)
                        st.rerun()
                    if is_on:
                        st.markdown('<div class="reminder-tag">✓ سنقوم بتنبيهك فور توفر هذا العقار</div>', unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1:
                    st.link_button("☎️ اتصال بالمالك", "tel:0551234567", use_container_width=True)
                with b2:
                    msg = quote(f"السلام عليكم، أرغب بالاستفسار عن العقار {p['type']} في حي {p['district']} بسعر {p['price']:,} ريال — رقم الإعلان #{pid}")
                    st.link_button("💬 واتساب", f"https://wa.me/966551234567?text={msg}", use_container_width=True)

                b3, b4 = st.columns(2)
                with b3:
                    fav_text = "♥ إزالة من المفضلة" if pid in st.session_state.favorites else "♡ حفظ العقار"
                    if st.button(fav_text, key="detail_fav", use_container_width=True):
                        toggle_favorite(pid)
                        st.rerun(scope="app")
                with b4:
                    st.link_button("🧭 فتح الموقع", f"https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lon']}", use_container_width=True)

                share_url = f"?view=map&property={pid}"
                st.markdown('<div style="height:7px"></div><b>مشاركة العقار</b>', unsafe_allow_html=True)
                components.html(
                    f'''<div dir="rtl" style="font-family:Arial;display:flex;gap:7px;margin-top:6px"><input id="share_{pid}" value="{share_url}" style="flex:1;padding:10px;border:1px solid #ddd;border-radius:10px;font-family:Arial" readonly><button onclick="navigator.clipboard.writeText(window.parent.location.origin+'{share_url}');this.innerText='تم النسخ ✓'" style="padding:10px 15px;border:0;border-radius:10px;background:#08635a;color:#fff;font-weight:bold;cursor:pointer">نسخ الرابط</button></div>''',
                    height=55,
                )
                st.markdown('</div></div>', unsafe_allow_html=True)

render_home_map_section()


# ============================================================
# Footer
# ============================================================
st.markdown('<div class="footer">مستكشف © 2026 — منصة عقارية تجريبية | الصور تُقرأ تلقائيًا من مجلد assets</div>', unsafe_allow_html=True)
