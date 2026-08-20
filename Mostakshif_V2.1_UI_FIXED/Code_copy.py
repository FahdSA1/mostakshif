# Mostakshif | نسخة عملية + تصميم فاخر + UX محسن
# تشغيل: python -m streamlit run app.py

import base64
import html
import math
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

GREEN = "#11875c"
GREEN_DARK = "#075f43"
BG = "#f4f7f7"
INK = "#15242d"
MUTED = "#738088"
BORDER = "#e2e8e5"

# ============================================================
# CSS — RTL + luxury UI
# ============================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],.block-container,
button,input,textarea,select,.stMarkdown,.stTextInput,.stSelectbox,.stNumberInput{font-family:'Cairo',Tahoma,Arial,sans-serif!important;}
html,body,.stApp{direction:rtl!important;background:#f4f7f7!important;}
.stApp{text-align:right!important;}
[data-testid="stHeader"],[data-testid="stSidebar"]{display:none!important;}
.block-container{max-width:1500px!important;padding:0 .35rem 2rem!important;}
.stButton>button,.stLinkButton>a{border-radius:12px!important;min-height:42px!important;font-weight:700!important;direction:rtl!important;}
.stButton>button p,.stLinkButton>a p{font-family:'Cairo'!important;}
div[data-baseweb="select"]>div,input,textarea{direction:rtl!important;text-align:right!important;border-radius:12px!important;}

/* Header */
.topbar{height:84px;background:#fff;border:1px solid #e6ecea;border-radius:0 0 22px 22px;display:flex;align-items:center;padding:0 18px;box-shadow:0 4px 18px rgba(15,45,36,.06);margin-bottom:0;direction:rtl;}
.brand{display:flex;align-items:center;gap:9px;min-width:245px;}
.brand-logo{width:76px;height:76px;object-fit:contain;border-radius:13px;background:#fff;}
.brand-mark{width:64px;height:64px;border-radius:15px;background:linear-gradient(145deg,#075f43,#1b9b6c);color:#fff;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;}
.brand-title{font-size:28px;font-weight:800;color:#12212a;line-height:1;}
.brand-sub{font-size:10px;color:#7a878d;margin-top:4px;}
.nav{display:flex;justify-content:center;align-items:center;gap:31px;flex:1;height:100%;}
.nav a{font-weight:700;color:#24333c;font-size:14px;padding:23px 0 17px;white-space:nowrap;text-decoration:none;}
.nav a:hover{color:#11875c;}
.nav a.active{color:#11875c;border-bottom:3px solid #11875c;}
.top-actions{display:flex;gap:10px;min-width:270px;justify-content:flex-start;}
.pill{border:1px solid #b9e1d0;border-radius:13px;padding:11px 16px;color:#127a56;background:#fff;font-weight:800;font-size:12px;text-decoration:none;}
.login-pill{background:#132834;color:#fff;border-color:#132834;}

/* Hero — no search field */
.hero{height:180px;border-radius:0 0 24px 24px;overflow:hidden;position:relative;margin:0 0 12px;color:#fff;background-position:center;background-size:cover;background-image:linear-gradient(90deg,rgba(8,30,43,.82),rgba(8,60,54,.28)),linear-gradient(180deg,#9fc4d4 0%,#e8a271 55%,#33484d 100%);box-shadow:0 8px 25px rgba(19,48,48,.10);}
.hero:after{content:"";position:absolute;inset:auto 0 0;height:65px;background:linear-gradient(90deg,transparent 0 5%,#102630 5% 7%,transparent 7% 10%,#122833 10% 14%,transparent 14% 18%,#122833 18% 22%,transparent 22% 26%,#102631 26% 31%,transparent 31% 35%,#122833 35% 39%,transparent 39% 44%,#122833 44% 48%,transparent 48% 53%,#102631 53% 57%,transparent 57% 62%,#122833 62% 67%,transparent 67% 72%,#102631 72% 76%,transparent 76% 81%,#122833 81% 86%,transparent 86% 92%,#102631 92% 96%,transparent 96%);opacity:.9;}
.hero-inner{position:relative;z-index:2;height:100%;display:flex;align-items:center;justify-content:center;gap:34px;padding:0 28px;direction:rtl;text-align:center;}
.hero-location{display:none;width:235px;background:rgba(255,255,255,.95);color:#17302a;border-radius:15px;padding:11px 13px;box-shadow:0 7px 20px rgba(0,0,0,.12);}
.hero-location strong{display:block;font-size:13px;color:#087554;}
.hero-location span{font-size:10px;color:#75817f;}
.hero-copy{flex:0 1 520px;align-self:center;text-align:center;}
.hero-copy h1{font-size:32px;margin:0 0 5px;color:#fff;font-weight:800;text-shadow:0 2px 8px rgba(0,0,0,.25);}
.hero-copy p{margin:0;color:#e7f0ef;font-size:14px;}
.hero-stats{display:flex;background:rgba(10,30,39,.84);border:1px solid rgba(255,255,255,.16);border-radius:15px;overflow:hidden;min-width:420px;direction:rtl;}
.hero-stat{padding:14px 22px;text-align:center;min-width:135px;border-left:1px solid rgba(255,255,255,.14);}
.hero-stat:last-child{border-left:0;}
.hero-stat b{display:block;font-size:20px;color:#fff;}.hero-stat span{font-size:11px;color:#cdd9dc;}

/* Location */
.location-banner{background:linear-gradient(135deg,#ffffff 0%,#f4fbf8 100%);border:1px solid #bfe7d6;border-radius:18px;padding:14px 18px;margin-bottom:10px;color:#49635c;direction:rtl;text-align:right;box-shadow:0 5px 18px rgba(20,40,35,.04);}
.location-banner strong{display:block;color:#075f43;font-size:16px;font-weight:800;margin-bottom:4px;}
.location-banner small{font-size:11px;color:#71817c;line-height:1.8;}
.location-ready{display:inline-block;background:#e7f7ef;color:#087554;border-radius:999px;padding:4px 10px;margin-right:7px;font-size:10px;font-weight:800;}
.location-help{font-size:10px;color:#8a9692;margin-top:4px;}

/* Search / filters */
.searchbar{background:#fff;border:1px solid #e3e9e7;border-radius:15px;padding:4px 10px;margin-bottom:10px;box-shadow:0 2px 12px rgba(20,40,35,.03);}
.filter-box{background:#fff;border:1px solid #e1e8e5;border-radius:18px;padding:13px 14px 10px;box-shadow:0 5px 20px rgba(20,40,35,.03);direction:rtl;text-align:right;}
.filter-heading{font-size:19px;font-weight:800;color:#15242d;margin-bottom:8px;}

/* Results */
.results-heading{display:flex;justify-content:space-between;align-items:end;gap:12px;margin:14px 2px 10px;direction:rtl;}
.results-heading h2{font-size:21px;font-weight:800;color:#16242d;margin:0;}
.results-heading span{color:#13885d;}
.result-note{font-size:10px;color:#899399;}
.property-card{background:#fff;border:1px solid #e4eae8;border-radius:17px;padding:10px;margin-bottom:10px;box-shadow:0 4px 18px rgba(16,40,32,.04);direction:rtl;text-align:center;}
.property-card img{border-radius:12px;object-fit:cover;max-height:165px;}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;background:#e8f6f0;color:#13855d;font-size:10px;font-weight:800;}.badge-rent{background:#e8f0ff;color:#2b71c8;}.badge-sold{background:#f1f2f3;color:#68727a;}.badge-leased{background:#fff0df;color:#a76108;}.badge-soon{background:#fff4d8;color:#9a6800;}
.price{color:#10865b;font-weight:800;font-size:21px;margin-top:3px;text-align:center;}.prop-name{font-size:16px;font-weight:800;color:#1b2932;margin-top:5px;text-align:center;}.meta{font-size:11px;color:#77838a;line-height:1.9;text-align:center;}.views{font-size:11px;color:#859097;text-align:center;}

/* Map / detail */
.map-wrap{background:#fff;border:1px solid #e2e8e6;border-radius:18px;padding:7px;box-shadow:0 5px 20px rgba(20,40,35,.04);}.map-caption{font-size:11px;color:#7a878d;padding:5px 8px 8px;direction:rtl;text-align:right;}
.detail-card{background:#fff;border:1px solid #e1e7e5;border-radius:20px;overflow:hidden;box-shadow:0 8px 28px rgba(17,40,34,.07);position:sticky;top:10px;direction:rtl;text-align:center;}.detail-card>img{width:100%;height:300px;object-fit:cover;display:block;}.detail-body{padding:18px;text-align:center;}.detail-price{font-size:31px;color:#11875c;font-weight:800;text-align:center;}.detail-title{font-size:24px;color:#172630;font-weight:800;text-align:center;}.detail-location{color:#738088;font-size:12px;margin:3px 0 10px;text-align:center;}.stats{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #edf0ef;border-bottom:1px solid #edf0ef;margin:13px 0;}.stat{padding:10px 4px;text-align:center;border-left:1px solid #edf0ef;}.stat:last-child{border-left:0;}.stat b{display:block;font-size:16px;color:#1b2a33;}.stat span{font-size:9px;color:#859097;}

/* About / Contact hero */
.page-hero{height:230px;border-radius:0 0 24px 24px;overflow:hidden;position:relative;margin:0 0 18px;color:#fff;background-position:center;background-size:cover;background-image:linear-gradient(90deg,rgba(8,30,43,.88),rgba(8,60,54,.32)),linear-gradient(180deg,#9fc4d4 0%,#e8a271 55%,#33484d 100%);box-shadow:0 10px 28px rgba(19,48,48,.12);display:flex;align-items:center;justify-content:center;text-align:center;direction:rtl;}
.page-hero:after{content:"";position:absolute;inset:auto 0 0;height:70px;background:linear-gradient(90deg,transparent 0 5%,#102630 5% 8%,transparent 8% 12%,#122833 12% 17%,transparent 17% 22%,#122833 22% 27%,transparent 27% 33%,#102631 33% 39%,transparent 39% 45%,#122833 45% 51%,transparent 51% 58%,#102631 58% 64%,transparent 64% 71%,#122833 71% 77%,transparent 77% 84%,#102631 84% 90%,transparent 90% 96%,#102631 96%);opacity:.9;}
.page-hero-inner{position:relative;z-index:2;max-width:900px;padding:25px;}
.page-hero h1{font-size:48px!important;margin:0 0 12px;color:#fff!important;font-weight:800;text-shadow:0 2px 10px rgba(0,0,0,.3);}
.page-hero p{font-size:18px;color:#f3f8f7;margin:0;line-height:2;}

/* About / Contact */
.info-card{background:#fff;border:1px solid #e1e8e5;border-radius:22px;padding:30px;box-shadow:0 8px 30px rgba(17,40,34,.06);direction:rtl;text-align:right;margin-top:15px;}
.info-card h1{font-size:42px;color:#075f43;margin:0 0 12px;font-weight:800;}.info-card h2{font-size:19px;color:#172630;margin-top:24px;}.info-card p{font-size:19px;color:#65737a;line-height:2.2;margin:7px 0;}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0;}.contact-item{border:1px solid #e5ebe9;border-radius:16px;padding:18px;background:#fbfdfc;}.contact-item b{display:block;color:#075f43;font-size:12px;margin-bottom:5px;}.contact-item a{color:#182a33;text-decoration:none;font-size:14px;font-weight:700;}
.footer{color:#899399;text-align:center;font-size:10px;padding:25px 0 5px;}
@media(max-width:1200px){.nav{gap:15px}.brand,.top-actions{min-width:180px}.hero-stats{min-width:320px}.nav a{font-size:12px;}.hero-copy h1{font-size:26px;}.page-hero h1{font-size:38px!important;}}
@media(max-width:850px){.topbar{height:auto;flex-wrap:wrap;padding:10px}.brand,.top-actions{min-width:100%;justify-content:center}.nav{order:3;overflow:auto;justify-content:flex-start;gap:22px;height:52px}.hero{height:auto;min-height:220px}.hero-inner{flex-direction:column;align-items:stretch;padding:15px}.hero-location,.hero-stats{width:100%;min-width:0}.hero-copy{text-align:center;}.contact-grid{grid-template-columns:1fr;}}
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

# ============================================================
# Assets — robust and deterministic
# ============================================================
BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def all_images():
    if not ASSETS.exists():
        return []
    return sorted(
        [
            p
            for p in ASSETS.rglob("*")
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTS
            and "logo" not in p.name.lower()
            and "hero" not in p.name.lower()
            and "riyadh" not in p.name.lower()
            and "skyline" not in p.name.lower()
        ]
    )


ALL_IMAGES = all_images()


def find_image(prop_id, index=0):
    # 1) Exact property naming
    exact_names = [
        f"{prop_id}_{index+1}",
        f"property_{prop_id}_{index+1}",
        f"property_{prop_id}",
        str(prop_id),
    ]
    for root in [ASSETS, BASE]:
        if not root.exists():
            continue
        for stem in exact_names:
            for ext in IMAGE_EXTS:
                p = root / f"{stem}{ext}"
                if p.exists():
                    return str(p)

    # 2) Demo package images: property 10001 -> property_demo_1.jpg
    demo_num = int(prop_id) - 10000 + index
    demo_candidates = [p for p in ALL_IMAGES if p.stem.lower() == f"property_demo_{demo_num}".lower()]
    if demo_candidates:
        return str(sorted(demo_candidates)[0])

    # 3) Recursive exact-id match
    exact = [p for p in ALL_IMAGES if str(prop_id) in p.stem]
    if exact:
        return str(exact[min(index, len(exact) - 1)])

    # 4) Deterministic distribution: every property gets a real image when any exist.
    if ALL_IMAGES:
        pos = (int(prop_id) - 10001 + index) % len(ALL_IMAGES)
        return str(ALL_IMAGES[pos])
    return None


def svg_placeholder(prop):
    title = html.escape(f"{prop['type']} في حي {prop['district']}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#244e42"/><stop offset="1" stop-color="#b99963"/></linearGradient></defs><rect width="1200" height="700" fill="#eef1ef"/><rect width="1200" height="700" fill="url(#g)" opacity=".18"/><rect x="170" y="300" width="860" height="280" rx="8" fill="#f6f3ec" stroke="#87765c" stroke-width="5"/><polygon points="120,310 600,70 1080,310" fill="#c8aa78" stroke="#766249" stroke-width="5"/><rect x="520" y="405" width="160" height="175" fill="#5c4637"/><rect x="280" y="380" width="150" height="110" fill="#9fc6d5"/><rect x="770" y="380" width="150" height="110" fill="#9fc6d5"/><text x="600" y="640" text-anchor="middle" font-family="Arial" font-size="38" fill="#23352f">{title}</text></svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def img_for(prop, index=0):
    return find_image(int(prop["id"]), index) or svg_placeholder(prop)


# Logo
logo_candidates = [
    ASSETS / "Logo_Mostaksheef.jpeg",
    ASSETS / "Logo_Mostakshif.jpeg",
    ASSETS / "logo_mostaksheef.jpeg",
    ASSETS / "logo.png",
]
logo_path = next((p for p in logo_candidates if p.exists()), None)


def logo_html():
    if logo_path:
        ext = logo_path.suffix.lower().replace(".", "") or "png"
        return f'<img class="brand-logo" src="data:image/{ext};base64,{base64.b64encode(logo_path.read_bytes()).decode()}">'
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
hero_path = hero_candidates[0] if hero_candidates else None
hero_style = ""
if hero_path:
    hero_b64 = base64.b64encode(hero_path.read_bytes()).decode()
    hero_style = f"background-image:linear-gradient(90deg,rgba(8,30,43,.82),rgba(8,60,54,.28)),url(data:image/{hero_path.suffix[1:]};base64,{hero_b64});"

# ============================================================
# State + query params
# ============================================================
for k, v in {
    "selected_id": 10001,
    "favorites": set(),
    "page": 1,
    "user_lat": None,
    "user_lon": None,
    "last_map_click": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

params = st.query_params
view = params.get("view", "home")
if view not in {"home", "map", "search", "favorites", "about", "contact"}:
    view = "home"

try:
    if params.get("user_lat") and params.get("user_lon"):
        st.session_state.user_lat = float(params.get("user_lat"))
        st.session_state.user_lon = float(params.get("user_lon"))
except Exception:
    pass

if params.get("property"):
    try:
        st.session_state.selected_id = int(params.get("property"))
    except Exception:
        pass

active = view
location_qs = ""
if st.session_state.user_lat is not None and st.session_state.user_lon is not None:
    location_qs = f"&user_lat={st.session_state.user_lat:.7f}&user_lon={st.session_state.user_lon:.7f}"

# ============================================================
# Header
# ============================================================
st.markdown(
    f'''<div class="topbar" dir="rtl">
        <div class="brand">{logo_html()}<div><div class="brand-title">مستكشف</div><div class="brand-sub">اكتشف عقارات • بسهولة وذكاء</div></div></div>
        <div class="nav">
            <a class="{'active' if active=='home' else ''}" href="?view=home{location_qs}">الرئيسية</a>
            <a class="{'active' if active=='favorites' else ''}" href="?view=favorites{location_qs}">المفضلة {len(st.session_state.favorites) if st.session_state.favorites else ''}</a>
            <a class="{'active' if active=='about' else ''}" href="?view=about{location_qs}">حول المنصة</a>
            <a class="{'active' if active=='contact' else ''}" href="?view=contact{location_qs}">تواصل معنا</a>
        </div>
        <div class="top-actions">
            <a class="pill" href="?view=contact{location_qs}">＋ أضف عقارك</a>
            <a class="pill login-pill" href="?view=contact{location_qs}">♙ تسجيل الدخول</a>
        </div>
    </div>''',
    unsafe_allow_html=True,
)

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
      <div class="hero-location"><strong>📍 موقعي الحالي</strong><span>{"تم حفظ موقعك وسيتم حساب المسافة تلقائيًا" if st.session_state.user_lat is not None else "اسمح بالموقع مرة واحدة من الخريطة"}</span></div>
      <div class="hero-copy"><h1>اكتشف العقار المناسب لك</h1><p>خريطة عقارية تفاعلية، فلاتر ذكية، ومسافة دقيقة من موقعك.</p></div>
      <div class="hero-stats"><div class="hero-stat"><b>142,890</b><span>عملية هذا الأسبوع</span></div><div class="hero-stat"><b>21,458</b><span>عقار متاح الآن</span></div><div class="hero-stat"><b>542,180</b><span>عدد المشاهدات</span></div></div>
    </div></div>''',
    unsafe_allow_html=True,
)

# ============================================================
# Location notice
# ============================================================
location_status = '<span class="location-ready">✓ تم حفظ موقعك</span>' if st.session_state.user_lat is not None else '<span class="location-ready" style="background:#fff4d8;color:#8b6900">لم يتم تحديد الموقع</span>'
location_text = (
    "الموقع محفوظ في هذه الجلسة، وستظهر المسافة تلقائيًا على بطاقات العقارات وداخل تفاصيل العقار."
    if st.session_state.user_lat is not None
    else
    "حدّد موقعك مرة واحدة من زر 📍 داخل الخريطة. سيطلب المتصفح الإذن، وبعد الموافقة نحفظ الإحداثيات ونحسب المسافة تلقائيًا."
)
st.markdown(
    f'''<div class="location-banner">
        <strong>📍 خدمة الموقع والمسافة {location_status}</strong>
        <small>{location_text}</small>
        <div class="location-help">لا نطلب الموقع مع كل عقار؛ تحديد الموقع مرة واحدة يكفي لحساب المسافات في النتائج.</div>
    </div>''',
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
# Search + Filters — الرئيسية فقط
# ============================================================
search = ""
if active in {"map", "home"}:
    if active == "home":
        search_value = st.query_params.get("q", "")
        st.markdown('<div class="searchbar">', unsafe_allow_html=True)
        search = st.text_input("البحث", value=search_value, placeholder="ابحث بالحي أو اسم الشارع أو معلم قريب", label_visibility="collapsed", key="main_search")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    st.markdown('<div class="filter-heading">الفلاتر <span style="font-size:11px;color:#7d898f">ابحث بدقة عن العقار المناسب</span></div>', unsafe_allow_html=True)
    f1 = st.columns(5)
    with f1[0]: category = st.selectbox("التصنيف", ["الكل", "سكني", "تجاري"], key="category")
    with f1[1]: kind = st.selectbox("نوع العقار", ["الكل", "فيلا", "دور", "شقة", "أرض", "محل", "مكتب", "معرض", "مستودع", "عمارة"], key="kind")
    with f1[2]: deal = st.selectbox("نوع العملية", ["الكل", "للبيع", "للإيجار"], key="deal")
    with f1[3]: district = st.selectbox("الحي", ["الكل"] + list(RIYADH.keys()), key="district")
    with f1[4]: status = st.selectbox("حالة الإعلان", ["الكل", "متاح", "متاح قريبًا", "مؤجر", "تم التأجير", "تم البيع"], key="status")
    f2 = st.columns(5)
    with f2[0]: sort = st.selectbox("ترتيب النتائج", ["الأحدث", "الأقل سعرًا", "الأعلى سعرًا", "الأكثر مشاهدة", "الأقرب إليك"], key="sort")
    with f2[1]: min_price = st.number_input("السعر من (ريال)", min_value=0, max_value=50_000_000, value=0, step=50_000, key="min_price")
    with f2[2]: max_price = st.number_input("السعر إلى (ريال)", min_value=0, max_value=50_000_000, value=50_000_000, step=50_000, key="max_price")
    with f2[3]: beds = st.selectbox("عدد غرف النوم", ["الكل", "1", "2", "3", "4", "5+"], key="beds")
    with f2[4]: baths = st.selectbox("عدد دورات المياه", ["الكل", "1", "2", "3", "4", "5+"], key="baths")
    f3 = st.columns(3)
    with f3[0]:
        max_age = st.selectbox("عمر العقار حتى (سنة)", ["الكل", 1, 3, 5, 10, 20], key="age")
        max_age = 100 if max_age == "الكل" else int(max_age)
    with f3[1]: distance_filter = st.selectbox("المسافة من موقعي", ["الكل", "1 كم", "3 كم", "5 كم", "10 كم", "20 كم"], key="distance")
    with f3[2]:
        st.markdown('<div style="font-size:11px;color:#74817d;padding-top:31px">💡 يمكنك الجمع بين أكثر من فلتر للوصول للنتيجة الأدق.</div>', unsafe_allow_html=True)
    c_apply, c_reset = st.columns([4, 1])
    with c_apply:
        if st.button("تطبيق الفلاتر", use_container_width=True, key="apply_filters"):
            st.session_state.page = 1
            st.rerun()
    with c_reset:
        if st.button("↻ إعادة التعيين", use_container_width=True, key="reset_filters"):
            for k in ["category", "kind", "deal", "district", "status", "sort", "min_price", "max_price", "beds", "baths", "age", "distance", "main_search"]:
                st.session_state.pop(k, None)
            st.session_state.page = 1
            st.session_state.last_map_click = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
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

if not filtered.empty and st.session_state.selected_id not in set(filtered.id):
    st.session_state.selected_id = int(filtered.iloc[0].id)

PAGE_SIZE = 12
pages = max(1, math.ceil(len(filtered) / PAGE_SIZE))
st.session_state.page = min(st.session_state.page, pages)
start = (st.session_state.page - 1) * PAGE_SIZE
page_df = filtered.iloc[start:start + PAGE_SIZE]

# ============================================================
# Helpers
# ============================================================
def badge(p):
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
    return f'<span class="badge {cls}">{html.escape(label)}</span>'


def render_property_card(p):
    pid = int(p["id"])
    img = img_for(p)
    fav = "♥" if pid in st.session_state.favorites else "♡"
    dtext = f' • 📍 {p["distance_km"]:.1f} كم من موقعك' if pd.notna(p.get("distance_km")) else ""
    st.markdown('<div class="property-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1.05, 2.0])
    with c1:
        st.image(img, use_container_width=True)
    with c2:
        st.markdown(badge(p), unsafe_allow_html=True)
        st.markdown(f'<div class="prop-name">{html.escape(p["type"])} — {html.escape(p["district"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price">{p["price"]:,} ريال</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meta">🛏 {p["beds"]} غرف • 🛁 {p["baths"]} دورات مياه • 📐 {p["area"]} م²{dtext}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="views">👁 {p["views"]:,} مشاهدة • إعلان #{pid}</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("عرض العقار", key=f"open_{pid}", use_container_width=True):
            st.session_state.selected_id = pid
            st.query_params["view"] = "map"
            st.query_params["property"] = str(pid)
            st.rerun()
    with b2:
        if st.button(f"{fav} المفضلة", key=f"fav_{pid}", use_container_width=True):
            if pid in st.session_state.favorites:
                st.session_state.favorites.remove(pid)
            else:
                st.session_state.favorites.add(pid)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Results-only pages: search / favorites
# ============================================================
if active in {"search", "favorites"}:
    title = "نتائج البحث" if active == "search" else "المفضلة"
    if active == "favorites" and not st.session_state.favorites:
        st.markdown('<div class="results-heading"><h2>المفضلة</h2></div>', unsafe_allow_html=True)
        st.info("لم تحفظ أي عقار في المفضلة حتى الآن.")
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
# Home / Map: map is the main content, no left results list
# ============================================================
st.markdown(f'<div class="results-heading"><h2>نتائج البحث <span>{len(filtered)} عقار</span></h2><div class="result-note">الخريطة تعرض النتائج المطابقة للفلاتر الحالية</div></div>', unsafe_allow_html=True)

map_col, detail_col = st.columns([2.25, 1.25], gap="medium")


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
                div.style.background='#fff';div.style.padding='8px 11px';div.style.cursor='pointer';div.style.borderRadius='10px';div.style.fontSize='18px';div.title='تحديد موقعي وحفظ الموقع';
                div.innerHTML='📍';
                L.DomEvent.disableClickPropagation(div);
                L.DomEvent.on(div,'click',function(){
                    div.innerHTML='⏳ جاري تحديد الموقع';
                    map.locate({setView:false,enableHighAccuracy:true,maximumAge:600000,timeout:15000});
                });
                return div;
            }; control.addTo(mapObject);
            mapObject.on('locationfound',function(e){
                var d=e.latlng.distanceTo(target);var txt=d>=1000?(d/1000).toFixed(2)+' كم':Math.round(d)+' متر';
                if(window.__msLine)mapObject.removeLayer(window.__msLine);
                window.__msLine=L.polyline([e.latlng,target],{color:'#11875c',weight:4,opacity:.9,dashArray:'8,8'}).addTo(mapObject);
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


with map_col:
    st.markdown('<div class="map-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="map-caption">🗺️ الخريطة التفاعلية — اضغط على أي عقار لتحديث بطاقة العقار مباشرة. استخدم «📍 تحديد موقعي» مرة واحدة للسماح بحساب المسافة.</div>', unsafe_allow_html=True)
    if filtered.empty:
        st.info("لا توجد نتائج مطابقة للفلاتر الحالية.")
    else:
        selected_rows = filtered[filtered.id == int(st.session_state.selected_id)]
        selected_for_map = selected_rows.iloc[0] if not selected_rows.empty else filtered.iloc[0]
        center = [24.744, 46.68]
        if len(filtered) > 1:
            center = [float(filtered.lat.mean()), float(filtered.lon.mean())]
        m = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron", control_scale=True, prefer_canvas=True)
        folium.TileLayer("CartoDB positron", name="الخريطة الفاتحة", overlay=False, control=True).add_to(m)
        Fullscreen(position="topleft").add_to(m)
        DistanceControl(selected_for_map.lat, selected_for_map.lon, int(selected_for_map.id), f"{selected_for_map.type} — {selected_for_map.district}").add_to(m)

        for _, p in filtered.iterrows():
            selected = int(p.id) == int(st.session_state.selected_id)
            popup = f'''<div dir="rtl" style="font-family:Arial;text-align:right;min-width:230px;line-height:1.8">
            <b>{html.escape(p.category)} • {html.escape(p.type)} — {html.escape(p.district)}</b><br>
            <span style="color:#11875c;font-size:18px;font-weight:bold">{p.price:,} ريال</span><br>
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

        map_result = st_folium(m, use_container_width=True, height=620, returned_objects=["last_object_clicked", "last_clicked", "center", "zoom"])
        click = map_result.get("last_object_clicked") if map_result else None
        if click and "lat" in click and "lng" in click:
            key = (round(float(click["lat"]), 6), round(float(click["lng"]), 6))
            if key != st.session_state.last_map_click:
                st.session_state.last_map_click = key
                nearest = filtered.assign(_d=filtered.apply(lambda x: haversine_km(float(click["lat"]), float(click["lng"]), x.lat, x.lon), axis=1)).sort_values("_d").iloc[0]
                if float(nearest["_d"]) < 0.8:
                    st.session_state.selected_id = int(nearest.id)
                    st.query_params["view"] = "map"
                    st.query_params["property"] = str(int(nearest.id))
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Selected property detail — always on the right
# ============================================================
with detail_col:
    rows = df[df.id == int(st.session_state.selected_id)]
    if rows.empty and not filtered.empty:
        rows = filtered.head(1)
    if not rows.empty:
        p = rows.iloc[0].to_dict()
        pid = int(p["id"])
        img = img_for(p)
        st.markdown('<div class="detail-card">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('<div class="detail-body">', unsafe_allow_html=True)
        st.markdown(badge(p), unsafe_allow_html=True)
        st.markdown(f'<div class="detail-title">{html.escape(p["type"])} — {html.escape(p["district"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-price">{p["price"]:,} ريال</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-location">📍 الرياض — حي {html.escape(p["district"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:11px;color:#7b878d">إعلان #{pid} • 👁 {p["views"]:,} مشاهدة</div>', unsafe_allow_html=True)
        st.markdown(f'''<div class="stats"><div class="stat"><b>{p["beds"]}</b><span>غرف نوم</span></div><div class="stat"><b>{p["baths"]}</b><span>دورات مياه</span></div><div class="stat"><b>{p["area"]}</b><span>م²</span></div><div class="stat"><b>{p["age"]}</b><span>سنوات</span></div></div>''', unsafe_allow_html=True)

        if st.session_state.user_lat is not None and st.session_state.user_lon is not None:
            dist = haversine_km(st.session_state.user_lat, st.session_state.user_lon, p["lat"], p["lon"])
            st.markdown(f'<div style="margin:10px 0;padding:10px;border-radius:12px;background:#eef8f4;color:#087554;font-weight:800;text-align:center">📍 يبعد العقار عن موقعك {dist:.2f} كم</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="margin:10px 0;padding:10px;border-radius:12px;background:#fff8e6;color:#8b6900;font-size:11px;text-align:center">📍 حدّد موقعك مرة واحدة من زر «📍 تحديد موقعي» في الخريطة لحساب المسافة تلقائيًا.</div>', unsafe_allow_html=True)

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
                if pid in st.session_state.favorites:
                    st.session_state.favorites.remove(pid)
                else:
                    st.session_state.favorites.add(pid)
                st.rerun()
        with b4:
            st.link_button("🧭 فتح الموقع", f"https://www.google.com/maps/search/?api=1&query={p['lat']},{p['lon']}", use_container_width=True)

        share_url = f"?view=map&property={pid}"
        st.markdown('<div style="height:7px"></div><b>مشاركة العقار</b>', unsafe_allow_html=True)
        components.html(
            f'''<div dir="rtl" style="font-family:Arial;display:flex;gap:7px;margin-top:6px"><input id="share_{pid}" value="{share_url}" style="flex:1;padding:10px;border:1px solid #ddd;border-radius:10px;font-family:Arial" readonly><button onclick="navigator.clipboard.writeText(window.parent.location.origin+'{share_url}');this.innerText='تم النسخ ✓'" style="padding:10px 15px;border:0;border-radius:10px;background:#11875c;color:#fff;font-weight:bold;cursor:pointer">نسخ الرابط</button></div>''',
            height=55,
        )
        st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================
# Footer
# ============================================================
st.markdown('<div class="footer">مستكشف © 2026 — منصة عقارية تجريبية | الصور تُقرأ تلقائيًا من مجلد assets</div>', unsafe_allow_html=True)
