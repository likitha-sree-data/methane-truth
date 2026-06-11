import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="The Methane Truth | Satellite vs Official Reports",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── DESIGN TOKENS ────────────────────────────────────────────────────────────
# Palette: deep space navy + emission amber + clean data white
# Typography: DM Mono for data readouts, Inter for body
# Signature: the 14.1% stat rendered as a radial fill — data as the hero

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp { background-color: #06101a; }

section[data-testid="stSidebar"] {
    background-color: #0b1a28;
    border-right: 1px solid #1a2d40;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #06101a 0%, #0d1f30 60%, #0a1a28 100%);
    border: 1px solid #1a2d40;
    border-radius: 12px;
    padding: 2.75rem 3rem;
    margin-bottom: 1.75rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(255,140,0,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #f59e0b;
    margin-bottom: 0.85rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #f0f4f8;
    margin: 0 0 0.6rem 0;
    letter-spacing: -1px;
    line-height: 1.15;
}
.hero-title span { color: #f59e0b; }
.hero-sub {
    font-size: 0.93rem;
    color: #7a9ab5;
    margin: 0;
    font-weight: 400;
    line-height: 1.7;
    max-width: 680px;
}
.hero-tags {
    margin-top: 1.4rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.tag {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.25);
    color: #f59e0b;
    padding: 0.22rem 0.75rem;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 1.75rem; }
.kpi-card {
    background: #0b1a28;
    border: 1px solid #1a2d40;
    border-radius: 10px;
    padding: 1.3rem 1.4rem 1.1rem;
    border-top: 2px solid #f59e0b;
    position: relative;
}
.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.85rem;
    font-weight: 500;
    color: #f0f4f8;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1;
}
.kpi-value.amber { color: #f59e0b; }
.kpi-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #4a6a85;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0.45rem 0 0.2rem;
}
.kpi-note { font-size: 0.76rem; color: #3d5a70; margin: 0; }

/* ── Finding Cards ── */
.finding-card {
    background: #0b1a28;
    border: 1px solid #1a2d40;
    border-radius: 10px;
    padding: 1.5rem 1.5rem 1.3rem;
    border-left: 3px solid #f59e0b;
    height: 100%;
}
.finding-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #f59e0b;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.finding-region {
    font-size: 1rem;
    font-weight: 600;
    color: #c8daea;
    margin-bottom: 0.2rem;
}
.finding-value {
    font-family: 'DM Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: #f59e0b;
    margin: 0.3rem 0;
    letter-spacing: -0.5px;
}
.finding-detail { font-size: 0.82rem; color: #4a6a85; line-height: 1.6; margin: 0; }

/* ── Section headers ── */
.section-head {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 2.5px;
    color: #f59e0b;
    text-transform: uppercase;
    margin: 2rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1a2d40;
}

/* ── Insight box ── */
.insight-box {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.18);
    border-left: 3px solid #f59e0b;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin: 1.25rem 0;
    font-size: 0.87rem;
    color: #7a9ab5;
    line-height: 1.75;
}
.insight-box strong { color: #c8daea; }

/* ── Warning box ── */
.warn-box {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.2);
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin: 1rem 0;
    font-size: 0.84rem;
    color: #9a6a6a;
    line-height: 1.7;
}
.warn-box strong { color: #f0a0a0; }

/* ── Sidebar ── */
.sb-head {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}
.sb-val { font-size: 0.83rem; color: #7a9ab5; line-height: 1.7; }
.sb-val strong { color: #c8daea; }
.sb-divider { border-top: 1px solid #1a2d40; margin: 1rem 0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0b1a28;
    border: 1px solid #1a2d40;
    border-radius: 8px;
    padding: 0.2rem;
    gap: 0.2rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #4a6a85;
    border-radius: 6px;
    padding: 0.5rem 1.25rem;
    font-weight: 500;
    font-size: 0.875rem;
}
.stTabs [aria-selected="true"] {
    background: #f59e0b !important;
    color: #06101a !important;
}

/* ── Table ── */
.dataframe { background: #0b1a28 !important; color: #c8daea !important; }

/* ── Footer ── */
.footer {
    background: #0b1a28;
    border: 1px solid #1a2d40;
    border-radius: 10px;
    padding: 1.25rem 2rem;
    text-align: center;
    margin-top: 2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #4a6a85;
}
.footer a { color: #f59e0b; text-decoration: none; }

/* ── Radio / select ── */
div[role="radiogroup"] label { color: #7a9ab5 !important; }
.stSelectbox label { color: #7a9ab5 !important; }
</style>
""", unsafe_allow_html=True)


# ─── PLOT THEME ───────────────────────────────────────────────────────────────
DARK_BG   = "#06101a"
CARD_BG   = "#0b1a28"
BORDER    = "#1a2d40"
AMBER     = "#f59e0b"
TEXT_DIM  = "#4a6a85"
TEXT_MID  = "#7a9ab5"
TEXT_HI   = "#c8daea"

PLOT_LAYOUT = dict(
    paper_bgcolor=DARK_BG,
    plot_bgcolor=CARD_BG,
    font=dict(family="Inter", color=TEXT_MID, size=12),
    title=dict(font=dict(color=TEXT_HI, size=13, family="Inter"), x=0),
    xaxis=dict(gridcolor=BORDER, linecolor=BORDER,
               tickfont=dict(color=TEXT_DIM, size=11), zeroline=False),
    yaxis=dict(gridcolor=BORDER, linecolor=BORDER,
               tickfont=dict(color=TEXT_DIM, size=11), zeroline=False),
    legend=dict(bgcolor=CARD_BG, bordercolor=BORDER, borderwidth=1,
                font=dict(color=TEXT_MID, size=11)),
    margin=dict(l=10, r=10, t=44, b=10)
)

AMBER_SCALE = [
    [0.0,  "#0a1520"],
    [0.25, "#1a3040"],
    [0.5,  "#7a4010"],
    [0.75, "#c07010"],
    [1.0,  "#f59e0b"],
]


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    errors = []
    dfs = {}

    files = {
        "winter":    "satellite_usa_winter.csv",
        "summer":    "satellite_usa_summer.csv",
        "hotspot_w": "winter_hotspots.csv",
        "hotspot_s": "summer_hotspots.csv",
        "official":  "unfccc_usa_totals.csv",
    }

    for key, fname in files.items():
        try:
            dfs[key] = pd.read_csv(fname)
        except FileNotFoundError:
            errors.append(fname)
            dfs[key] = None

    return dfs, errors


@st.cache_data
def make_sector_data():
    """
    UNFCCC USA CH4 by sector — approximated from public Climate Watch data.
    Replace with real unfccc_usa_totals.csv sector breakdown when available.
    """
    return pd.DataFrame({
        "sector": [
            "Oil & Gas", "Enteric Fermentation", "Landfills",
            "Coal Mining", "Manure Management", "Wastewater",
            "Agriculture Other", "Other"
        ],
        "mt_ch4_2022": [10.8, 8.4, 6.2, 2.4, 2.1, 1.6, 1.5, 2.5],
        "pct": [30.4, 23.7, 17.5, 6.8, 5.9, 4.5, 4.2, 7.0],
    })


dfs, load_errors = load_data()
winter_df     = dfs["winter"]
summer_df     = dfs["summer"]
winter_hs     = dfs["hotspot_w"]
summer_hs     = dfs["hotspot_s"]
official_data = dfs["official"]

DATA_LOADED = all(v is not None for v in dfs.values())

# Background constants
BG_WINTER = 1919.93   # NOAA GML January 2023
BG_SUMMER = 1914.89   # NOAA GML June–August 2023 average


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:0.25rem 0 1.5rem;">
        <div style="font-family:'DM Mono',monospace; font-size:0.95rem;
        font-weight:500; color:{TEXT_HI}; letter-spacing:-0.3px;">
        The Methane Truth</div>
        <div style="font-family:'DM Mono',monospace; font-size:0.62rem;
        color:{AMBER}; margin-top:0.2rem; text-transform:uppercase;
        letter-spacing:2px;">Open Source · Zero Proprietary Data</div>
    </div>
    <div class="sb-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sb-head">Study Coverage</div>
    <div class="sb-val">
    <strong>304,611</strong> quality-filtered observations<br>
    Winter — January 2023<br>
    Summer — June – August 2023<br>
    Continental USA bounding box
    </div>
    <div class="sb-divider"></div>

    <div class="sb-head">NOAA Verified Background</div>
    <div class="sb-val">
    Jan 2023 &nbsp;→ <strong>1,919.93 ppb</strong><br>
    Jun–Aug 2023 → <strong>1,914.89 ppb</strong><br>
    <span style="font-size:0.75rem; color:{TEXT_DIM};">
    Source: NOAA GML monthly means.<br>
    A fixed 1,870 ppb baseline overestimates<br>
    enhancement by ~50 ppb. This was corrected.
    </span>
    </div>
    <div class="sb-divider"></div>

    <div class="sb-head">Quality Standard</div>
    <div class="sb-val">
    ESA TROPOMI qa_value > 0.5<br>
    Land pixels only · No Mapbox token
    </div>
    <div class="sb-divider"></div>

    <div class="sb-head">Pipeline</div>
    <div class="sb-val">
    Python · xarray · Snowflake<br>
    dbt Core · Streamlit · GitHub Pages
    </div>
    <div class="sb-divider"></div>

    <div class="sb-head">Author</div>
    <div class="sb-val">
    <strong>Likitha Yarabarla</strong><br>
    Climate Data Engineer<br>
    <a href="https://linkedin.com/in/likitha-sree"
    style="color:{AMBER}; text-decoration:none;">LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/likitha-sree-data/methane-truth"
    style="color:{AMBER}; text-decoration:none;">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🛰️ ESA Sentinel-5P TROPOMI · NOAA GML · UNFCCC</div>
    <h1 class="hero-title">The Methane <span>Truth</span></h1>
    <p class="hero-sub">
    304,611 real satellite observations over the continental USA.
    Only <strong style="color:#f59e0b;">14.1%</strong> of pixels detect methane above the verified
    global background — but those pixels cluster with geographic precision
    over three known emission corridors. Here is exactly where.
    </p>
    <div class="hero-tags">
        <span class="tag">304,611 OBSERVATIONS</span>
        <span class="tag">5.5 × 3.5 KM RESOLUTION</span>
        <span class="tag">WINTER + SUMMER 2023</span>
        <span class="tag">FULLY REPRODUCIBLE</span>
        <span class="tag">ZERO PROPRIETARY DATA</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── DATA LOAD WARNINGS ───────────────────────────────────────────────────────
if load_errors:
    st.markdown(f"""
    <div class="warn-box">
    <strong>⚠ Missing data files:</strong> {', '.join(load_errors)}<br>
    Place the CSV files in the same directory as app.py and restart.
    The dashboard will display sample data where files are unavailable.
    </div>
    """, unsafe_allow_html=True)


# ─── KPI STRIP ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-head">Overview Metrics</div>', unsafe_allow_html=True)

n_winter  = len(winter_df)  if winter_df  is not None else 73_486
n_summer  = len(summer_df)  if summer_df  is not None else 211_430
n_hs_w    = len(winter_hs)  if winter_hs  is not None else 15_902
n_hs_s    = len(summer_hs)  if summer_hs  is not None else 24_562
total_hs  = n_hs_w + n_hs_s
total_obs = n_winter + n_summer

col1, col2, col3, col4, col5 = st.columns(5)
kpis = [
    (f"{total_obs:,}",  "Total Observations",        "Quality-filtered · land only",    False),
    (f"{total_hs:,}",   "Hotspot Pixels",             f"Above NOAA verified background",  False),
    ("14.1%",           "Detection Rate",             "Pixels showing elevation",         True),
    ("+75.9 ppb",       "Peak Enhancement",           "Gulf Coast · summer max pixel",    True),
    ("35.5 Mt",         "Official Reported (2022)",   "USA UNFCCC submission · CH₄",      False),
]

for col, (val, label, note, hi) in zip(
    [col1, col2, col3, col4, col5], kpis
):
    with col:
        cls = "amber" if hi else ""
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value {cls}">{val}</p>
            <p class="kpi-label">{label}</p>
            <p class="kpi-note">{note}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── THREE FINDINGS ───────────────────────────────────────────────────────────
st.markdown('<div class="section-head">Primary Findings — Where Methane Is Elevated</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
findings = [
    ("01", "Northern Plains",       "MN–ND Border",
     "+56.3 ppb", "Peak 1,976.2 ppb · Winter 2023",
     "485 hotspot pixels. Agricultural wetlands and oil & gas operations. "
     "The winter signal is consistent with thermogenic methane from O&G "
     "combined with waterlogged soil emissions."),
    ("02", "Gulf Coast",            "TX–LA Offshore Corridor",
     "+75.9 ppb", "Peak 1,990.7 ppb · Summer 2023",
     "1,271 hotspot pixels. Highest single pixel in the dataset. "
     "Offshore petrochemical operations between Houston and New Orleans. "
     "Summer peak consistent with increased production activity and temperature-driven venting."),
    ("03", "California Central Valley", "San Joaquin Valley",
     "+70.3 ppb", "Peak 1,985.2 ppb · Summer 2023",
     "1,221 hotspot pixels. Dairy farming and agricultural methane. "
     "Largest agricultural CH₄ source region in the western USA. "
     "Signal persists across the full summer window."),
]

for col, (num, region, sub, val, peak, detail) in zip([col1, col2, col3], findings):
    with col:
        st.markdown(f"""
        <div class="finding-card">
            <div class="finding-num">FINDING {num}</div>
            <div class="finding-region">{region}</div>
            <div style="font-size:0.75rem; color:{TEXT_DIM}; margin-bottom:0.3rem;">{sub}</div>
            <div class="finding-value">{val}</div>
            <div style="font-family:'DM Mono',monospace; font-size:0.72rem;
            color:{AMBER}; margin-bottom:0.6rem;">{peak}</div>
            <p class="finding-detail">{detail}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── METHODOLOGY NOTE ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="insight-box">
<strong>Why does the satellite mean fall below the NOAA background?</strong>
This is atmospheric physics, not a data error. TROPOMI pixels are 5.5 × 3.5 km.
Emission plumes from individual facilities dilute rapidly into surrounding clean background air
within the column average. The result: 85.9% of pixels measure background air, not plumes.
The 14.1% that do show elevation are geographically meaningful — they cluster precisely over
known source regions, not randomly. Satellite monitoring at national scale is a
<strong>geographic localization tool</strong>, not a national inventory verification tool.
</div>
""", unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️  Satellite Maps",
    "📊  Sector Breakdown",
    "📈  Seasonal Analysis",
    "🔬  Hotspot Detail",
    "⚙️  Methodology",
])


# ══ TAB 1 — MAPS ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-head">Satellite Methane Concentration Maps</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color:{TEXT_MID}; font-size:0.87rem; margin-bottom:1.25rem; max-width:720px;">
    Each point is an ESA Sentinel-5P TROPOMI pixel at 5.5 × 3.5 km resolution.
    The hotspot view shows <em>all</em> 43,086 above-background pixels — no random sampling.
    The full-dataset views sample 5,000 points for rendering speed; the hotspot view is complete.
    Color encodes methane column concentration (ppb) relative to NOAA verified background.
    </p>
    """, unsafe_allow_html=True)

    map_choice = st.radio(
        "Select view",
        [
            "🔴 Hotspots only — all 43,086 above-background pixels (recommended)",
            "❄️  Winter full dataset — January 2023 (5,000 sample)",
            "☀️  Summer full dataset — June–August 2023 (5,000 sample)",
        ],
        horizontal=False,
    )

    if "Hotspot" in map_choice:
        if winter_hs is not None and summer_hs is not None:
            plot_df = pd.concat([winter_hs, summer_hs], ignore_index=True)
        else:
            # Synthetic demo data so the map never breaks
            rng = np.random.default_rng(42)
            demo_lats = np.concatenate([
                rng.normal(47.5, 1.2, 485),   # Northern Plains
                rng.normal(29.0, 0.8, 1271),  # Gulf Coast
                rng.normal(36.5, 1.0, 1221),  # Central Valley
            ])
            demo_lons = np.concatenate([
                rng.normal(-97.5, 1.5, 485),
                rng.normal(-91.5, 1.2, 1271),
                rng.normal(-120.0, 0.8, 1221),
            ])
            demo_ppb = np.concatenate([
                rng.uniform(1920, 1976, 485),
                rng.uniform(1915, 1991, 1271),
                rng.uniform(1915, 1985, 1221),
            ])
            plot_df = pd.DataFrame({
                "latitude": demo_lats,
                "longitude": demo_lons,
                "methane_column_ppb": demo_ppb,
            })
        cmin, cmax = 1915, 1992
        map_title  = "Emission Hotspots — All Pixels Exceeding NOAA Verified Background"
        caption    = f"Combined winter ({BG_WINTER} ppb) and summer ({BG_SUMMER} ppb) above-background pixels. No sampling — every hotspot pixel shown."
        dot_size   = 3

    elif "Winter" in map_choice:
        src = winter_df if winter_df is not None else pd.DataFrame(
            {"latitude": np.random.uniform(30, 49, 5000),
             "longitude": np.random.uniform(-125, -67, 5000),
             "methane_column_ppb": np.random.normal(1904, 12, 5000)})
        plot_df   = src.sample(min(5000, len(src)), random_state=42)
        cmin, cmax = 1875, 1980
        map_title  = "Winter Methane Concentrations — USA, January 2023"
        caption    = f"NOAA verified background: {BG_WINTER} ppb · January 2023"
        dot_size   = 2

    else:
        src = summer_df if summer_df is not None else pd.DataFrame(
            {"latitude": np.random.uniform(30, 49, 5000),
             "longitude": np.random.uniform(-125, -67, 5000),
             "methane_column_ppb": np.random.normal(1895, 15, 5000)})
        plot_df   = src.sample(min(5000, len(src)), random_state=42)
        cmin, cmax = 1870, 1992
        map_title  = "Summer Methane Concentrations — USA, June–August 2023"
        caption    = f"NOAA verified background: {BG_SUMMER} ppb · Summer 2023 avg"
        dot_size   = 2

    # ── Scattergeo — no Mapbox token required ──
    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lat=plot_df["latitude"],
        lon=plot_df["longitude"],
        mode="markers",
        marker=dict(
            color=plot_df["methane_column_ppb"],
            colorscale=AMBER_SCALE,
            cmin=cmin, cmax=cmax,
            size=dot_size,
            opacity=0.85,
            colorbar=dict(
                title=dict(text="CH₄ (ppb)", font=dict(color=TEXT_MID, size=11)),
                tickfont=dict(color=TEXT_DIM, size=10),
                thickness=12, len=0.65,
                bgcolor=CARD_BG,
                bordercolor=BORDER,
                x=1.01,
            ),
        ),
        text=plot_df["methane_column_ppb"].round(1).astype(str) + " ppb",
        hovertemplate="<b>%{text}</b><br>Lat %{lat:.3f} · Lon %{lon:.3f}<extra></extra>",
    ))

    # Annotation pins for the three hotspots
    hotspot_pins = [
        dict(lat=47.5,  lon=-97.5,  label="Northern Plains<br>+56.3 ppb peak"),
        dict(lat=29.0,  lon=-91.5,  label="Gulf Coast<br>+75.9 ppb peak"),
        dict(lat=36.5,  lon=-120.0, label="Central Valley<br>+70.3 ppb peak"),
    ]
    for pin in hotspot_pins:
        fig_map.add_trace(go.Scattergeo(
            lat=[pin["lat"]], lon=[pin["lon"]],
            mode="markers+text",
            marker=dict(size=10, color=AMBER, symbol="circle", line=dict(color="#fff", width=1.5)),
            text=[pin["label"]],
            textfont=dict(color=AMBER, size=9, family="DM Mono"),
            textposition="top right",
            hoverinfo="skip",
            showlegend=False,
        ))

    fig_map.update_layout(
        title=dict(text=map_title, font=dict(color=TEXT_HI, size=13, family="Inter"), x=0),
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            showland=True, landcolor="#0a1520",
            showocean=True, oceancolor="#06101a",
            showlakes=True, lakecolor="#06101a",
            showcoastlines=True, coastlinecolor=BORDER,
            showsubunits=True, subunitcolor="#1a2d40",
            bgcolor=DARK_BG,
        ),
        paper_bgcolor=DARK_BG,
        margin=dict(l=0, r=100, t=44, b=0),
        height=560,
        font=dict(family="Inter", color=TEXT_MID),
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(caption + " · Source: ESA Copernicus Data Space L2 CH₄ · qa_value > 0.5")


# ══ TAB 2 — SECTOR BREAKDOWN ══════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-head">USA Methane by Sector — UNFCCC Official Inventory</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color:{TEXT_MID}; font-size:0.87rem; margin-bottom:1.25rem; max-width:720px;">
    The USA officially reports 35.5 Mt CH₄ for 2022 across multiple sectors.
    The satellite hotspot signals correspond geographically to the two largest sectors:
    oil & gas (Gulf Coast, Northern Plains) and enteric fermentation/agriculture (Central Valley).
    This is the accountability question satellites are uniquely positioned to probe.
    </p>
    """, unsafe_allow_html=True)

    sector_df = make_sector_data()

    col1, col2 = st.columns([3, 2])

    with col1:
        fig_sector = go.Figure(go.Bar(
            x=sector_df["mt_ch4_2022"],
            y=sector_df["sector"],
            orientation="h",
            marker=dict(
                color=sector_df["mt_ch4_2022"],
                colorscale=[[0, "#1a2d40"], [0.5, "#7a4010"], [1, AMBER]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=sector_df["mt_ch4_2022"].apply(lambda x: f"{x:.1f} Mt"),
            textfont=dict(color=TEXT_HI, size=11, family="DM Mono"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x:.1f} Mt CH₄ · %{customdata:.1f}%<extra></extra>",
            customdata=sector_df["pct"],
        ))
        fig_sector.update_layout(
            **PLOT_LAYOUT,
            height=380,
            title="USA CH₄ Emissions by Sector — 2022 UNFCCC Submission",
            xaxis=dict(**PLOT_LAYOUT["xaxis"], title="Mt CH₄ per year",
                       range=[0, 13]),
            yaxis=dict(**PLOT_LAYOUT["yaxis"],
                       categoryorder="total ascending"),
        )
        st.plotly_chart(fig_sector, use_container_width=True)

    with col2:
        fig_pie = go.Figure(go.Pie(
            labels=sector_df["sector"],
            values=sector_df["mt_ch4_2022"],
            hole=0.55,
            marker=dict(
                colors=[AMBER, "#c07010", "#7a4010", "#4a2808",
                        "#1a3040", "#0d1f30", "#152030", "#0a1520"],
                line=dict(color=DARK_BG, width=2),
            ),
            textfont=dict(color=TEXT_HI, size=10),
            hovertemplate="<b>%{label}</b><br>%{value:.1f} Mt · %{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text="35.5 Mt<br>total", x=0.5, y=0.5, showarrow=False,
            font=dict(family="DM Mono", size=13, color=TEXT_HI),
        )
        fig_pie.update_layout(
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            height=380,
            title=dict(text="Sector Share", font=dict(color=TEXT_HI, size=13), x=0),
            legend=dict(bgcolor=CARD_BG, bordercolor=BORDER, borderwidth=1,
                        font=dict(color=TEXT_MID, size=10)),
            margin=dict(l=0, r=0, t=44, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <strong>Satellite × Sector alignment:</strong>
    Oil & gas (30.4% / 10.8 Mt) and enteric fermentation (23.7% / 8.4 Mt) together account for
    54% of official US methane. The Gulf Coast hotspot (+75.9 ppb) geographically maps onto
    offshore O&G operations. The Central Valley hotspot (+70.3 ppb) maps onto
    California's dairy sector — the state with the largest enteric fermentation inventory in the USA.
    The Northern Plains winter signal overlaps both O&G activity (Bakken formation) and
    agricultural wetlands. This geographic alignment is the core validation this project provides.
    </div>
    """, unsafe_allow_html=True)

    # ── Official trend line ──
    st.markdown('<div class="section-head">USA Official Inventory Trend 2015–2022</div>',
                unsafe_allow_html=True)

    if official_data is not None and "year" in official_data.columns:
        trend_df = official_data
    else:
        trend_df = pd.DataFrame({
            "year": list(range(2015, 2023)),
            "reported_Mt_CH4": [36.1, 35.8, 35.5, 35.7, 35.3, 35.0, 35.4, 35.5],
        })

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_df["year"], y=trend_df["reported_Mt_CH4"],
        mode="lines+markers",
        line=dict(color=AMBER, width=2.5),
        marker=dict(size=7, color=AMBER, line=dict(color=DARK_BG, width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(245,158,11,0.07)",
        hovertemplate="<b>%{x}</b> · %{y:.1f} Mt CH₄<extra></extra>",
    ))
    fig_trend.update_layout(
        **PLOT_LAYOUT,
        height=280,
        title="USA Official CH₄ — UNFCCC Annual Submissions",
        xaxis=dict(**PLOT_LAYOUT["xaxis"], title="Year",
                   tickvals=list(range(2015, 2023))),
        yaxis=dict(**PLOT_LAYOUT["yaxis"], title="Mt CH₄", range=[30, 42]),
    )
    st.plotly_chart(fig_trend, use_container_width=True)


# ══ TAB 3 — SEASONAL ANALYSIS ═════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-head">Seasonal Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        dist_data = pd.DataFrame({
            "Season": ["Winter Jan", "Winter Jan", "Summer Jun–Aug", "Summer Jun–Aug"],
            "Category": ["Below Background", "Above Background",
                         "Below Background", "Above Background"],
            "Pct": [78.5, 21.5, 88.3, 11.7],
        })
        fig_dist = px.bar(
            dist_data, x="Season", y="Pct", color="Category",
            color_discrete_map={
                "Below Background": BORDER,
                "Above Background": AMBER,
            },
            title="Pixel Distribution vs NOAA Background",
            labels={"Pct": "% of Observations"},
            text="Pct", height=380, barmode="stack",
        )
        fig_dist.update_traces(
            texttemplate="%{text:.1f}%", textposition="inside",
            textfont=dict(color=DARK_BG, size=12, family="DM Mono"),
        )
        fig_dist.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        # Enhancement comparison across the three hotspots
        enh_df = pd.DataFrame({
            "Region": ["Northern Plains", "Gulf Coast", "Central Valley"],
            "Season": ["Winter", "Summer", "Summer"],
            "Enhancement_ppb": [56.3, 75.9, 70.3],
            "Peak_ppb": [1976.2, 1990.7, 1985.2],
        })
        fig_enh = go.Figure(go.Bar(
            x=enh_df["Region"],
            y=enh_df["Enhancement_ppb"],
            marker=dict(
                color=enh_df["Enhancement_ppb"],
                colorscale=[[0, "#1a3040"], [1, AMBER]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=["+" + str(v) + " ppb" for v in enh_df["Enhancement_ppb"]],
            textfont=dict(color=TEXT_HI, size=11, family="DM Mono"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>+%{y:.1f} ppb above background<br>Peak: %{customdata:.1f} ppb<extra></extra>",
            customdata=enh_df["Peak_ppb"],
        ))
        fig_enh.update_layout(
            **PLOT_LAYOUT,
            title="Peak Enhancement Above NOAA Background by Region",
            yaxis=dict(**PLOT_LAYOUT["yaxis"], title="Enhancement (ppb)", range=[0, 90]),
            height=380,
        )
        st.plotly_chart(fig_enh, use_container_width=True)

    # Summary stats table
    st.markdown('<div class="section-head">Seasonal Summary Statistics</div>',
                unsafe_allow_html=True)

    summary_df = pd.DataFrame({
        "Season": ["Winter — January 2023", "Summer — Jun–Aug 2023", "Combined"],
        "Observations": [f"{n_winter:,}", f"{n_summer:,}", f"{total_obs:,}"],
        "Satellite Mean (ppb)": [1904.7, 1894.9, 1899.8],
        "NOAA Background (ppb)": [BG_WINTER, BG_SUMMER, 1917.41],
        "Hotspot Pixels": [
            f"{n_hs_w:,} (21.5%)", f"{n_hs_s:,} (11.7%)", f"{total_hs:,} (14.1%)"
        ],
        "Peak Enhancement": ["+56.3 ppb", "+75.9 ppb", "+75.9 ppb"],
    })
    st.dataframe(summary_df, hide_index=True, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <strong>Column dilution explained:</strong> The satellite mean (1,904.7 ppb winter)
    falls below the NOAA background (1,919.93 ppb) because TROPOMI measures the full
    atmospheric column average. Emission plumes from surface sources represent a small
    fraction of the column depth and dilute rapidly into background air at the 5.5 km pixel scale.
    This is not a data quality issue — it is the expected physical behavior of passive
    column-integrated remote sensing. The hotspot pixels that <em>do</em> show elevation
    are the scientifically meaningful signal.
    </div>
    """, unsafe_allow_html=True)


# ══ TAB 4 — HOTSPOT DETAIL ════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-head">Emission Hotspot Detail</div>',
                unsafe_allow_html=True)

    hotspot_table = pd.DataFrame({
        "Region": ["Northern Plains MN–ND", "Gulf Coast TX–LA", "CA Central Valley"],
        "Season": ["Winter", "Summer", "Summer"],
        "Hotspot Pixels": [485, 1_271, 1_221],
        "Peak Conc. (ppb)": [1976.2, 1990.7, 1985.2],
        "Peak Enhancement (ppb)": ["+56.3", "+75.9", "+70.3"],
        "Likely Source": [
            "Agricultural wetlands + Bakken O&G",
            "Offshore petrochemical (Gulf basin)",
            "Dairy farming + rice agriculture",
        ],
        "UNFCCC Sector Match": ["Oil & Gas / Agriculture", "Oil & Gas", "Enteric Fermentation"],
    })
    st.dataframe(hotspot_table, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        src_w = winter_hs if winter_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1930, 12, 15902).clip(BG_WINTER, 1985)})
        fig_w = px.histogram(
            src_w, x="methane_column_ppb", nbins=50,
            title=f"Winter Hotspot Distribution — {n_hs_w:,} pixels",
            labels={"methane_column_ppb": "CH₄ Concentration (ppb)", "count": "Pixel Count"},
            color_discrete_sequence=[AMBER], height=360,
        )
        fig_w.add_vline(x=BG_WINTER, line_dash="dash", line_color="#ef4444", line_width=1.5,
                        annotation_text=f"NOAA background {BG_WINTER} ppb",
                        annotation_font_color="#ef4444", annotation_font_size=10)
        fig_w.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_w, use_container_width=True)

    with col2:
        src_s = summer_hs if summer_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1925, 15, 24562).clip(BG_SUMMER, 1992)})
        fig_s = px.histogram(
            src_s, x="methane_column_ppb", nbins=50,
            title=f"Summer Hotspot Distribution — {n_hs_s:,} pixels",
            labels={"methane_column_ppb": "CH₄ Concentration (ppb)", "count": "Pixel Count"},
            color_discrete_sequence=["#c07010"], height=360,
        )
        fig_s.add_vline(x=BG_SUMMER, line_dash="dash", line_color="#ef4444", line_width=1.5,
                        annotation_text=f"NOAA background {BG_SUMMER} ppb",
                        annotation_font_color="#ef4444", annotation_font_size=10)
        fig_s.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_s, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <strong>What next-level analysis looks like:</strong>
    Cross-referencing these hotspot coordinates against the EPA GHGRP facility-level database
    would let you attribute specific pixel clusters to named facilities — refineries, compressor
    stations, dairy CAFOs. That is the jump from geographic localization to facility accountability.
    It is Priority 4 in the roadmap and would meaningfully differentiate this platform from
    existing public tools.
    </div>
    """, unsafe_allow_html=True)


# ══ TAB 5 — METHODOLOGY ═══════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-head">Methodology</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        #### Pipeline Architecture

        **Satellite Ingestion**
        ESA Sentinel-5P TROPOMI L2 methane product downloaded via Copernicus Data Space API.
        Parsed from netCDF4 using xarray. Key variable:
        `methane_mixing_ratio_bias_corrected` in the PRODUCT group.
        Shape: `(time, scanline, ground_pixel)`.

        **Quality Filtering**
        `qa_value > 0.5` per ESA TROPOMI L2 documentation.
        Plausibility filter: 1,600–2,200 ppb.
        Bounding box: lat 24–50°N, lon 66–125°W.
        Land mask removes Gulf of Mexico, Pacific, and Atlantic ocean pixels.

        **Background Selection** *(critical)*
        NOAA GML monthly means used as period-specific background.
        Using a historical fixed value of 1,870 ppb would overestimate
        enhancement by ~50 ppb for 2023 data. Always query NOAA GML for
        the specific study month.

        **Data Warehouse**
        Snowflake (free trial). Four schemas: RAW → STAGING → INTERMEDIATE → MARTS.
        dbt Core transformations. Batched inserts of 10,000 records with
        deduplication on (date, lat, lon).

        **Official Inventory**
        UNFCCC submissions via Climate Watch API (no key required).
        Filtered: gas = CH₄, region = USA, all sectors.
        """)

    with col2:
        st.markdown(f"""
        #### Known Limitations

        **Temporal coverage**
        Four months only (Jan + Jun–Aug). Spring and autumn data would
        complete the seasonal picture and reduce sampling bias.

        **Pixel footprint**
        5.5 × 3.5 km means individual facility plumes are diluted into
        surrounding background air in the column average. This is structural
        to TROPOMI, not a flaw in this analysis.

        **Sampling bias**
        Cloud cover systematically reduces valid observations in certain
        regions and seasons. No orbital sampling correction is applied.

        **No uncertainty quantification**
        Implied emission ranges are not reported as confidence intervals.
        Required before academic publication (Priority 6 in roadmap).

        #### Reproduce This Analysis

        1. Free account: `dataspace.copernicus.eu`
        2. Free Snowflake trial: `snowflake.com`
        3. Notebook: `github.com/likitha-sree-data/methane-truth`
        4. Run in Google Colab following the cell sequence

        Runtime: ~2–3 hours. Zero proprietary data.
        """)

    st.markdown('<div class="section-head">Citations</div>', unsafe_allow_html=True)
    st.markdown("""
    - ESA Sentinel-5P TROPOMI Level 2 Methane Product User Manual — sentinel.esa.int
    - NOAA Global Monitoring Laboratory · gml.noaa.gov/ccgg/trends_ch4
    - Turner et al. 2020 · *A large increase in US methane emissions over the past decade* · Science 369, 1219–1223
    - Alvarez et al. 2018 · *Assessment of methane emissions from the US oil and gas supply chain* · Science 361, 186–188
    - Climate Watch API Documentation · climatewatchdata.org/api
    """)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    Built with real satellite data · Zero proprietary sources · Fully reproducible pipeline<br><br>
    ESA Sentinel-5P TROPOMI &nbsp;·&nbsp; NOAA GML &nbsp;·&nbsp; UNFCCC via Climate Watch
    &nbsp;·&nbsp;
    <a href="https://github.com/likitha-sree-data/methane-truth">GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/likitha-sree">LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="https://medium.com/the-quantastic-journal/the-blue-carbon-market-promised-to-save-the-worlds-coastlines-the-data-tells-a-different-story-6b4f4ec774bd">
    Blue Carbon Analysis</a>
</div>
""", unsafe_allow_html=True)
