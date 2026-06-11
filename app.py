import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Methane Truth — Satellite Emissions Analysis",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ─────────────────────────────────────────────────────────────
# Palette: scientific slate — the visual language of NOAA/ESA publications
# with a single infrared teal accent (CH4 false-color imagery standard)
# Type: Space Grotesk (authority) + Inter (clarity) + IBM Plex Mono (data)
# Signature: the 14.1% detection rate rendered as a precision radial gauge
# No gradients on cards. No rounded corners above 6px. No decoration.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background-color: #f2f4f7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1923;
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #8a9ab0 !important;
}

/* ── Header band ── */
.page-header {
    background-color: #0f1923;
    padding: 2.5rem 3rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    border-bottom: 1px solid #1e2d3d;
}
.header-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #2eb8a6;
    margin-bottom: 0.75rem;
}
.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem;
    font-weight: 600;
    color: #e8edf2;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin: 0 0 0.6rem;
}
.header-sub {
    font-size: 0.9rem;
    color: #5a7a94;
    line-height: 1.7;
    max-width: 700px;
    margin: 0;
    font-weight: 300;
}
.header-meta {
    margin-top: 1.25rem;
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}
.meta-item {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #3a5a72;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.meta-item span {
    color: #5a9ab0;
    display: block;
    font-size: 0.65rem;
    margin-top: 0.15rem;
}

/* ── KPI row ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    background: #d4d9e0;
    border: 1px solid #d4d9e0;
    margin-bottom: 2rem;
}
.kpi-cell {
    background: #ffffff;
    padding: 1.4rem 1.5rem 1.2rem;
    border-top: 3px solid transparent;
}
.kpi-cell.accent { border-top-color: #2eb8a6; }
.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.95rem;
    font-weight: 600;
    color: #0f1923;
    letter-spacing: -1px;
    line-height: 1;
    margin: 0;
}
.kpi-value.teal { color: #2eb8a6; }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 400;
    color: #7a8fa0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0.5rem 0 0.2rem;
}
.kpi-note {
    font-size: 0.75rem;
    color: #a0afbe;
    margin: 0;
    line-height: 1.4;
}

/* ── Section label ── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 2px;
    color: #2eb8a6;
    text-transform: uppercase;
    margin: 2rem 0 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #d4d9e0;
}

/* ── Finding cards ── */
.finding-card {
    background: #ffffff;
    border: 1px solid #d4d9e0;
    border-top: 3px solid #2eb8a6;
    padding: 1.5rem;
    height: 100%;
}
.finding-region {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #0f1923;
    margin-bottom: 0.15rem;
}
.finding-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #7a8fa0;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}
.finding-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #2eb8a6;
    letter-spacing: -1px;
    margin: 0 0 0.15rem;
    line-height: 1;
}
.finding-peak {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #5a7a94;
    margin-bottom: 0.8rem;
}
.finding-detail {
    font-size: 0.82rem;
    color: #5a7a94;
    line-height: 1.65;
    margin: 0;
    border-top: 1px solid #eef0f3;
    padding-top: 0.8rem;
}

/* ── Insight / callout ── */
.callout {
    background: #f7fafa;
    border: 1px solid #b8ddd8;
    border-left: 3px solid #2eb8a6;
    padding: 1.1rem 1.4rem;
    margin: 1.25rem 0;
    font-size: 0.86rem;
    color: #3a5a6a;
    line-height: 1.75;
}
.callout strong { color: #0f1923; font-weight: 500; }

.callout-warn {
    background: #fafaf7;
    border: 1px solid #ddd8b8;
    border-left: 3px solid #c8a020;
    padding: 1rem 1.4rem;
    margin: 0.75rem 0;
    font-size: 0.83rem;
    color: #6a5a2a;
    line-height: 1.7;
}
.callout-warn strong { color: #3a2a00; }

/* ── Sidebar internals ── */
.sb-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #2eb8a6 !important;
    margin-bottom: 0.4rem;
    display: block;
}
.sb-text {
    font-size: 0.81rem;
    color: #6a8a9a !important;
    line-height: 1.7;
}
.sb-text strong { color: #a8bfcc !important; }
.sb-divider {
    border: none;
    border-top: 1px solid #1e2d3d;
    margin: 1.1rem 0;
}
.sb-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e8edf2 !important;
    letter-spacing: -0.3px;
}
.sb-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #2eb8a6 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.2rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border: 1px solid #d4d9e0;
    border-radius: 4px;
    padding: 0.2rem;
    gap: 0.15rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7a8fa0;
    border-radius: 3px;
    padding: 0.45rem 1.1rem;
    font-weight: 500;
    font-size: 0.84rem;
    font-family: 'Inter', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: #0f1923 !important;
    color: #e8edf2 !important;
}

/* ── Tables ── */
.dataframe thead tr th {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: #7a8fa0 !important;
    background: #f7f8fa !important;
}
.dataframe tbody tr td {
    font-size: 0.84rem !important;
    color: #2a3a4a !important;
}

/* ── Footer ── */
.page-footer {
    background: #0f1923;
    border-top: 1px solid #1e2d3d;
    padding: 1.25rem 2rem;
    text-align: center;
    margin-top: 3rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #3a5a72;
    letter-spacing: 0.5px;
}
.page-footer a {
    color: #2eb8a6;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ─────────────────────────────────────────────────────────────────
BG_WINTER = 1919.93
BG_SUMMER = 1914.89

TEAL      = "#2eb8a6"
NAVY      = "#0f1923"
SLATE     = "#5a7a94"
BORDER    = "#d4d9e0"
CARD      = "#ffffff"
PAGE_BG   = "#f2f4f7"

PLOT_BASE = dict(
    paper_bgcolor=CARD,
    plot_bgcolor="#f7f8fa",
    font=dict(family="Inter", color=SLATE, size=12),
    title=dict(font=dict(family="Space Grotesk", color=NAVY, size=13), x=0),
    xaxis=dict(gridcolor=BORDER, linecolor=BORDER,
               tickfont=dict(family="IBM Plex Mono", color="#9aaabb", size=10),
               zeroline=False),
    yaxis=dict(gridcolor=BORDER, linecolor=BORDER,
               tickfont=dict(family="IBM Plex Mono", color="#9aaabb", size=10),
               zeroline=False),
    legend=dict(bgcolor=CARD, bordercolor=BORDER, borderwidth=1,
                font=dict(color=SLATE, size=11)),
    margin=dict(l=10, r=10, t=44, b=10),
)

TEAL_SCALE = [
    [0.0,  "#e8f4f2"],
    [0.3,  "#7accc0"],
    [0.6,  "#2eb8a6"],
    [0.85, "#0d6b60"],
    [1.0,  "#062e2a"],
]


# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    files = {
        "winter":    "satellite_usa_winter.csv",
        "summer":    "satellite_usa_summer.csv",
        "hotspot_w": "winter_hotspots.csv",
        "hotspot_s": "summer_hotspots.csv",
        "official":  "unfccc_usa_totals.csv",
    }
    dfs, missing = {}, []
    for key, fname in files.items():
        try:
            dfs[key] = pd.read_csv(fname)
        except FileNotFoundError:
            dfs[key] = None
            missing.append(fname)
    return dfs, missing


@st.cache_data
def sector_data():
    return pd.DataFrame({
        "sector": [
            "Oil & Gas Systems", "Enteric Fermentation", "Municipal Solid Waste",
            "Coal Mining", "Manure Management", "Wastewater Treatment",
            "Agricultural Soils", "Other",
        ],
        "mt_ch4": [10.8, 8.4, 6.2, 2.4, 2.1, 1.6, 1.5, 2.5],
        "pct":    [30.4, 23.7, 17.5, 6.8, 5.9, 4.5, 4.2, 7.0],
    })


dfs, missing_files = load_data()
winter_df = dfs["winter"]
summer_df = dfs["summer"]
winter_hs = dfs["hotspot_w"]
summer_hs = dfs["hotspot_s"]
official  = dfs["official"]

n_winter = len(winter_df) if winter_df is not None else 73_486
n_summer = len(summer_df) if summer_df is not None else 211_430
n_hs_w   = len(winter_hs) if winter_hs is not None else 15_902
n_hs_s   = len(summer_hs) if summer_hs is not None else 24_562
total_hs  = n_hs_w + n_hs_s
total_obs = n_winter + n_summer


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.5rem;">
        <div class="sb-logo">Methane Truth</div>
        <div class="sb-tagline">Satellite Emissions Analysis</div>
    </div>
    <hr class="sb-divider">

    <span class="sb-label">Study Coverage</span>
    <div class="sb-text">
        <strong>304,611</strong> quality-filtered observations<br>
        Winter — January 2023<br>
        Summer — June to August 2023<br>
        Continental USA · Land pixels only
    </div>
    <hr class="sb-divider">

    <span class="sb-label">NOAA Verified Background</span>
    <div class="sb-text">
        January 2023 &nbsp;&nbsp; <strong>1,919.93 ppb</strong><br>
        Jun–Aug 2023 &nbsp;<strong>1,914.89 ppb</strong><br><br>
        <span style="font-size:0.73rem; color:#3a5a72 !important;">
        A fixed 1,870 ppb baseline overestimates<br>
        enhancement by ~50 ppb for 2023 data.
        </span>
    </div>
    <hr class="sb-divider">

    <span class="sb-label">Quality Standard</span>
    <div class="sb-text">
        ESA TROPOMI qa_value &gt; 0.5<br>
        Plausibility filter: 1,600–2,200 ppb<br>
        Land mask applied post-download
    </div>
    <hr class="sb-divider">

    <span class="sb-label">Pipeline</span>
    <div class="sb-text">
        Python · xarray · Snowflake · dbt<br>
        Streamlit · GitHub Pages
    </div>
    <hr class="sb-divider">

    <span class="sb-label">Author</span>
    <div class="sb-text">
        <strong>Likitha Yarabarla</strong><br>
        Climate Data Engineer<br>
        <a href="https://linkedin.com/in/likitha-sree"
        style="color:#2eb8a6 !important; text-decoration:none;">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="https://github.com/likitha-sree-data/methane-truth"
        style="color:#2eb8a6 !important; text-decoration:none;">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="header-eyebrow">ESA Sentinel-5P TROPOMI · NOAA GML · UNFCCC · Open Source</div>
    <h1 class="header-title">Methane Truth</h1>
    <p class="header-sub">
        304,611 satellite observations over the continental United States.
        14.1% of pixels detect methane above the verified global background —
        those pixels cluster with geographic precision over three emission corridors.
    </p>
    <div class="header-meta">
        <div class="meta-item">Study Period<span>Jan + Jun–Aug 2023</span></div>
        <div class="meta-item">Resolution<span>5.5 × 3.5 km per pixel</span></div>
        <div class="meta-item">Instrument<span>TROPOMI / Sentinel-5P</span></div>
        <div class="meta-item">Background Source<span>NOAA GML Monthly Means</span></div>
        <div class="meta-item">Inventory Source<span>UNFCCC via Climate Watch API</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── MISSING FILES WARNING ─────────────────────────────────────────────────────
if missing_files:
    st.markdown(f"""
    <div class="callout-warn">
    <strong>Data files not found:</strong> {', '.join(missing_files)}<br>
    Place the CSV files in the same directory as app.py. 
    Charts will render with illustrative data until real files are present.
    </div>
    """, unsafe_allow_html=True)


# ── KPI ROW ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

kpis = [
    (f"{total_obs:,}",  "Total Observations",    "Quality-filtered, land only",     False),
    (f"{total_hs:,}",   "Hotspot Pixels",         "Exceeding NOAA monthly mean",     False),
    ("14.1%",           "Detection Rate",          "Pixels showing CH4 elevation",    True),
    ("+75.9 ppb",       "Peak Enhancement",        "Gulf Coast · single pixel max",   True),
    ("35.5 Mt CH4",     "Official 2022 Inventory", "USA UNFCCC submission",           False),
]

for col, (val, label, note, hi) in zip([c1, c2, c3, c4, c5], kpis):
    with col:
        vc = "teal" if hi else ""
        ac = "accent" if hi else ""
        st.markdown(f"""
        <div class="kpi-cell {ac}">
            <p class="kpi-value {vc}">{val}</p>
            <p class="kpi-label">{label}</p>
            <p class="kpi-note">{note}</p>
        </div>
        """, unsafe_allow_html=True)


# ── THREE FINDINGS ────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Primary Findings</div>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)
findings = [
    ("Northern Plains",    "Minnesota – North Dakota",
     "+56.3 ppb", "Peak 1,976.2 ppb · Winter 2023 · 485 hotspot pixels",
     "Winter signal at the MN–ND border. Consistent with thermogenic methane "
     "from Bakken formation O&G combined with agricultural wetland emissions. "
     "The seasonal winter peak is characteristic of O&G venting patterns."),
    ("Gulf Coast",         "Texas – Louisiana Offshore",
     "+75.9 ppb", "Peak 1,990.7 ppb · Summer 2023 · 1,271 hotspot pixels",
     "Highest single pixel in the dataset. Offshore petrochemical operations "
     "between Houston and New Orleans. Summer peak consistent with increased "
     "production activity and temperature-driven venting in the Gulf basin."),
    ("Central Valley",     "California Agricultural Core",
     "+70.3 ppb", "Peak 1,985.2 ppb · Summer 2023 · 1,221 hotspot pixels",
     "Dairy farming and rice agriculture. Largest agricultural CH4 source "
     "region in the western USA. Signal persists across the full Jun–Aug window, "
     "consistent with enteric fermentation and flooded paddy field emissions."),
]

for col, (region, sub, val, peak, detail) in zip([fc1, fc2, fc3], findings):
    with col:
        st.markdown(f"""
        <div class="finding-card">
            <div class="finding-region">{region}</div>
            <div class="finding-sub">{sub}</div>
            <div class="finding-value">{val}</div>
            <div class="finding-peak">{peak}</div>
            <p class="finding-detail">{detail}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
<strong>On column dilution:</strong>
The satellite mean concentration falls below the NOAA background for both seasons.
This is not a data error — it is the expected behavior of passive column-integrated remote sensing.
TROPOMI pixels are 5.5 × 3.5 km. Emission plumes from surface sources represent a small
fraction of the column depth and dilute rapidly into background air at this scale.
The 14.1% of pixels that do show elevation are the scientifically meaningful signal,
and they are not randomly distributed. They cluster precisely over known source regions,
confirming that satellite monitoring functions as a <strong>geographic localization tool</strong>
rather than a national inventory verification mechanism.
</div>
""", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Satellite Maps",
    "Sector Attribution",
    "Seasonal Analysis",
    "Hotspot Detail",
    "Methodology",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MAPS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Satellite Methane Concentration Maps</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <p style="color:{SLATE}; font-size:0.87rem; margin-bottom:1.25rem; max-width:740px; line-height:1.7;">
    Each point is an ESA Sentinel-5P TROPOMI pixel. The hotspot view renders all 43,086
    above-background pixels without sampling. Full-dataset views sample 5,000 points for
    rendering performance. Color encodes methane column concentration relative to
    the NOAA verified monthly background.
    </p>
    """, unsafe_allow_html=True)

    map_choice = st.radio(
        "Select view",
        [
            "Hotspots — all 43,086 above-background pixels",
            "Winter full dataset — January 2023 (5,000 sample)",
            "Summer full dataset — June–August 2023 (5,000 sample)",
        ],
    )

    if "Hotspot" in map_choice:
        if winter_hs is not None and summer_hs is not None:
            plot_df = pd.concat([winter_hs, summer_hs], ignore_index=True)
        else:
            rng = np.random.default_rng(42)
            lats = np.concatenate([rng.normal(47.5,1.2,485), rng.normal(29.0,0.8,1271), rng.normal(36.5,1.0,1221)])
            lons = np.concatenate([rng.normal(-97.5,1.5,485), rng.normal(-91.5,1.2,1271), rng.normal(-120.0,0.8,1221)])
            ppbs = np.concatenate([rng.uniform(1920,1976,485), rng.uniform(1915,1991,1271), rng.uniform(1915,1985,1221)])
            plot_df = pd.DataFrame({"latitude":lats,"longitude":lons,"methane_column_ppb":ppbs})
        cmin, cmax = 1915, 1992
        title   = "Emission Hotspots — Pixels Exceeding NOAA Verified Background"
        caption = "All above-background pixels, winter and summer combined. No sampling."
        dot_sz  = 3

    elif "Winter" in map_choice:
        src = winter_df if winter_df is not None else pd.DataFrame({
            "latitude": np.random.uniform(30,49,5000),
            "longitude": np.random.uniform(-125,-67,5000),
            "methane_column_ppb": np.random.normal(1904,12,5000),
        })
        plot_df = src.sample(min(5000,len(src)), random_state=42)
        cmin, cmax = 1875, 1980
        title   = "Winter Methane Concentrations — USA, January 2023"
        caption = f"NOAA verified background: {BG_WINTER} ppb · January 2023"
        dot_sz  = 2

    else:
        src = summer_df if summer_df is not None else pd.DataFrame({
            "latitude": np.random.uniform(30,49,5000),
            "longitude": np.random.uniform(-125,-67,5000),
            "methane_column_ppb": np.random.normal(1895,15,5000),
        })
        plot_df = src.sample(min(5000,len(src)), random_state=42)
        cmin, cmax = 1870, 1992
        title   = "Summer Methane Concentrations — USA, June–August 2023"
        caption = f"NOAA verified background: {BG_SUMMER} ppb · Summer 2023 average"
        dot_sz  = 2

    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lat=plot_df["latitude"],
        lon=plot_df["longitude"],
        mode="markers",
        marker=dict(
            color=plot_df["methane_column_ppb"],
            colorscale=TEAL_SCALE,
            cmin=cmin, cmax=cmax,
            size=dot_sz,
            opacity=0.9,
            colorbar=dict(
                title=dict(text="CH4 (ppb)",
                           font=dict(family="IBM Plex Mono", color=SLATE, size=10)),
                tickfont=dict(family="IBM Plex Mono", color="#9aaabb", size=9),
                thickness=10, len=0.6,
                bgcolor=CARD, bordercolor=BORDER, x=1.01,
            ),
        ),
        hovertemplate="%{customdata:.1f} ppb<br>%{lat:.3f}N %{lon:.3f}W<extra></extra>",
        customdata=plot_df["methane_column_ppb"],
    ))

    for pin in [
        dict(lat=47.5, lon=-97.5, label="Northern Plains"),
        dict(lat=29.0, lon=-91.5, label="Gulf Coast"),
        dict(lat=36.5, lon=-120.2, label="Central Valley"),
    ]:
        fig_map.add_trace(go.Scattergeo(
            lat=[pin["lat"]], lon=[pin["lon"]],
            mode="markers+text",
            marker=dict(size=8, color=TEAL, symbol="circle-open",
                        line=dict(color=TEAL, width=2)),
            text=[pin["label"]],
            textfont=dict(family="IBM Plex Mono", color=TEAL, size=9),
            textposition="top right",
            hoverinfo="skip", showlegend=False,
        ))

    fig_map.update_layout(
        title=dict(text=title,
                   font=dict(family="Space Grotesk", color=NAVY, size=13), x=0),
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,    landcolor="#e8edf2",
            showocean=True,   oceancolor="#d0d8e4",
            showlakes=True,   lakecolor="#d0d8e4",
            showcoastlines=True, coastlinecolor="#b0bece",
            showsubunits=True,   subunitcolor="#c4ceda",
            bgcolor=PAGE_BG,
        ),
        paper_bgcolor=CARD,
        margin=dict(l=0, r=100, t=44, b=0),
        height=540,
        font=dict(family="Inter", color=SLATE),
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(caption + " · Source: ESA Copernicus Data Space L2 CH4 · qa_value > 0.5")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SECTOR ATTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">USA Methane by Sector — UNFCCC 2022 Submission</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <p style="color:{SLATE}; font-size:0.87rem; margin-bottom:1.25rem; max-width:740px; line-height:1.7;">
    The USA officially reports 35.5 Mt CH4 for 2022. Oil & gas systems and enteric fermentation
    together account for 54% of that total. The three satellite hotspots map geographically
    onto precisely these two sectors — the alignment is the core validation this analysis provides.
    </p>
    """, unsafe_allow_html=True)

    sd = sector_data()
    sc1, sc2 = st.columns([3, 2])

    with sc1:
        fig_bar = go.Figure(go.Bar(
            x=sd["mt_ch4"],
            y=sd["sector"],
            orientation="h",
            marker=dict(
                color=sd["mt_ch4"],
                colorscale=[[0,"#d4eae8"],[0.5,"#7accc0"],[1,TEAL]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=[f"{v:.1f} Mt" for v in sd["mt_ch4"]],
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=10),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x:.1f} Mt CH4<br>%{customdata:.1f}%<extra></extra>",
            customdata=sd["pct"],
        ))
        fig_bar.update_layout(
            **PLOT_BASE,
            title="CH4 Emissions by Sector — 2022",
            xaxis=dict(**PLOT_BASE["xaxis"], title="Mt CH4 / year", range=[0,13.5]),
            yaxis=dict(**PLOT_BASE["yaxis"], categoryorder="total ascending"),
            height=380,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with sc2:
        fig_pie = go.Figure(go.Pie(
            labels=sd["sector"],
            values=sd["mt_ch4"],
            hole=0.58,
            marker=dict(
                colors=[TEAL,"#7accc0","#4a9e94","#2a7a70",
                        "#d4eae8","#b0d4d0","#e8f4f2","#f0f8f7"],
                line=dict(color=CARD, width=2),
            ),
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=9),
            hovertemplate="<b>%{label}</b><br>%{value:.1f} Mt · %{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text="35.5 Mt<br>CH4 2022",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="IBM Plex Mono", size=11, color=NAVY),
        )
        fig_pie.update_layout(
            paper_bgcolor=CARD, plot_bgcolor=CARD,
            title=dict(text="Sector Share", font=dict(family="Space Grotesk", color=NAVY, size=13), x=0),
            legend=dict(bgcolor=CARD, bordercolor=BORDER, borderwidth=1,
                        font=dict(family="Inter", color=SLATE, size=10)),
            margin=dict(l=0, r=0, t=44, b=0),
            height=380,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown(f"""
    <div class="callout">
    <strong>Satellite-to-sector alignment:</strong>
    Oil & gas systems (30.4% / 10.8 Mt) and enteric fermentation (23.7% / 8.4 Mt) together
    represent 54% of the official US methane inventory.
    The Gulf Coast hotspot (+75.9 ppb) maps onto offshore O&G infrastructure.
    The Central Valley hotspot (+70.3 ppb) maps onto California's dairy sector —
    the state with the largest enteric fermentation inventory in the USA.
    The Northern Plains winter signal overlaps both Bakken O&G activity and agricultural wetlands.
    The satellite does not verify the totals. It verifies the <strong>geography</strong>.
    </div>
    """, unsafe_allow_html=True)

    # Trend line
    st.markdown('<div class="section-label">Official Inventory Trend 2015–2022</div>',
                unsafe_allow_html=True)

    if official is not None and "year" in official.columns:
        tr = official
    else:
        tr = pd.DataFrame({
            "year": list(range(2015,2023)),
            "reported_Mt_CH4": [36.1,35.8,35.5,35.7,35.3,35.0,35.4,35.5],
        })

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=tr["year"], y=tr["reported_Mt_CH4"],
        mode="lines+markers",
        line=dict(color=TEAL, width=2),
        marker=dict(size=6, color=TEAL, line=dict(color=CARD, width=1.5)),
        fill="tozeroy", fillcolor="rgba(46,184,166,0.06)",
        hovertemplate="<b>%{x}</b> · %{y:.1f} Mt CH4<extra></extra>",
    ))
    fig_trend.update_layout(
        **PLOT_BASE,
        title="USA Official CH4 — UNFCCC Annual Submissions (Mt CH4)",
        xaxis=dict(**PLOT_BASE["xaxis"], tickvals=list(range(2015,2023))),
        yaxis=dict(**PLOT_BASE["yaxis"], range=[30,42]),
        height=260,
    )
    st.plotly_chart(fig_trend, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SEASONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Seasonal Analysis</div>', unsafe_allow_html=True)

    sa1, sa2 = st.columns(2)

    with sa1:
        dist = pd.DataFrame({
            "Season":   ["Winter", "Winter", "Summer", "Summer"],
            "Category": ["Below background","Above background",
                         "Below background","Above background"],
            "Pct":      [78.5, 21.5, 88.3, 11.7],
        })
        fig_dist = px.bar(
            dist, x="Season", y="Pct", color="Category",
            color_discrete_map={"Below background":"#d4dde8","Above background":TEAL},
            title="Pixel Distribution Relative to NOAA Background",
            labels={"Pct":"% of observations"},
            text="Pct", height=360, barmode="stack",
        )
        fig_dist.update_traces(
            texttemplate="%{text:.1f}%", textposition="inside",
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=11),
        )
        fig_dist.update_layout(**PLOT_BASE)
        st.plotly_chart(fig_dist, use_container_width=True)

    with sa2:
        enh = pd.DataFrame({
            "Region":    ["Northern Plains","Gulf Coast","Central Valley"],
            "ppb":       [56.3, 75.9, 70.3],
            "Peak":      [1976.2, 1990.7, 1985.2],
        })
        fig_enh = go.Figure(go.Bar(
            x=enh["Region"], y=enh["ppb"],
            marker=dict(
                color=enh["ppb"],
                colorscale=[[0,"#d4eae8"],[1,TEAL]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=[f"+{v} ppb" for v in enh["ppb"]],
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=10),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>+%{y} ppb above background<br>Peak: %{customdata} ppb<extra></extra>",
            customdata=enh["Peak"],
        ))
        fig_enh.update_layout(
            **PLOT_BASE,
            title="Peak Enhancement Above NOAA Background",
            yaxis=dict(**PLOT_BASE["yaxis"], title="Enhancement (ppb)", range=[0,92]),
            height=360,
        )
        st.plotly_chart(fig_enh, use_container_width=True)

    st.markdown('<div class="section-label">Summary Statistics</div>', unsafe_allow_html=True)
    summ = pd.DataFrame({
        "Season": ["Winter — January 2023","Summer — Jun–Aug 2023","Combined"],
        "Observations": [f"{n_winter:,}",f"{n_summer:,}",f"{total_obs:,}"],
        "Satellite Mean (ppb)": [1904.7, 1894.9, 1899.8],
        "NOAA Background (ppb)": [BG_WINTER, BG_SUMMER, 1917.41],
        "Hotspot Pixels": [
            f"{n_hs_w:,} (21.5%)",
            f"{n_hs_s:,} (11.7%)",
            f"{total_hs:,} (14.1%)",
        ],
        "Peak Enhancement": ["+56.3 ppb","+75.9 ppb","+75.9 ppb"],
    })
    st.dataframe(summ, hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — HOTSPOT DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-label">Emission Hotspot Detail</div>', unsafe_allow_html=True)

    ht = pd.DataFrame({
        "Region":               ["Northern Plains MN–ND","Gulf Coast TX–LA","CA Central Valley"],
        "Season":               ["Winter","Summer","Summer"],
        "Hotspot Pixels":       [485, 1271, 1221],
        "Peak Conc. (ppb)":     [1976.2, 1990.7, 1985.2],
        "Peak Enhancement":     ["+56.3 ppb","+75.9 ppb","+70.3 ppb"],
        "Likely Source":        [
            "Agricultural wetlands + Bakken O&G",
            "Offshore petrochemical (Gulf basin)",
            "Dairy + rice agriculture",
        ],
        "UNFCCC Sector":        ["Oil & Gas / Agriculture","Oil & Gas","Enteric Fermentation"],
    })
    st.dataframe(ht, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hc1, hc2 = st.columns(2)

    with hc1:
        src_w = winter_hs if winter_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1930,12,n_hs_w).clip(BG_WINTER, 1985)})
        fig_wh = px.histogram(
            src_w, x="methane_column_ppb", nbins=50,
            title=f"Winter Hotspot Distribution — {n_hs_w:,} pixels",
            labels={"methane_column_ppb":"CH4 (ppb)","count":"Pixels"},
            color_discrete_sequence=[TEAL], height=340,
        )
        fig_wh.add_vline(x=BG_WINTER, line_dash="dot", line_color="#c8381a", line_width=1.5,
                         annotation_text=f"Background {BG_WINTER} ppb",
                         annotation_font_color="#c8381a", annotation_font_size=9)
        fig_wh.update_layout(**PLOT_BASE)
        st.plotly_chart(fig_wh, use_container_width=True)

    with hc2:
        src_s = summer_hs if summer_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1925,15,n_hs_s).clip(BG_SUMMER, 1992)})
        fig_sh = px.histogram(
            src_s, x="methane_column_ppb", nbins=50,
            title=f"Summer Hotspot Distribution — {n_hs_s:,} pixels",
            labels={"methane_column_ppb":"CH4 (ppb)","count":"Pixels"},
            color_discrete_sequence=["#0d6b60"], height=340,
        )
        fig_sh.add_vline(x=BG_SUMMER, line_dash="dot", line_color="#c8381a", line_width=1.5,
                         annotation_text=f"Background {BG_SUMMER} ppb",
                         annotation_font_color="#c8381a", annotation_font_size=9)
        fig_sh.update_layout(**PLOT_BASE)
        st.plotly_chart(fig_sh, use_container_width=True)

    st.markdown("""
    <div class="callout">
    <strong>Next step — facility attribution:</strong>
    Cross-referencing these hotspot coordinates against the EPA GHGRP facility-level database
    would attribute specific pixel clusters to named facilities — refineries, compressor stations,
    dairy CAFOs. That is the jump from geographic localization to facility-level accountability,
    and it is what separates a portfolio project from a publishable analysis.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-label">Methodology</div>', unsafe_allow_html=True)

    mc1, mc2 = st.columns(2)

    with mc1:
        st.markdown(f"""
        #### Pipeline

        **Satellite ingestion**
        ESA Sentinel-5P TROPOMI L2 methane product. Downloaded via Copernicus Data Space API.
        Parsed from netCDF4 with xarray. Key variable:
        `methane_mixing_ratio_bias_corrected` · shape `(time, scanline, ground_pixel)`.

        **Quality filtering**
        `qa_value > 0.5` per ESA TROPOMI L2 documentation.
        Plausibility bounds: 1,600–2,200 ppb.
        Bounding box: lat 24–50°N · lon 66–125°W.
        Custom land mask removes Gulf of Mexico, Pacific, and Atlantic ocean pixels
        (3,648 winter + 16,047 summer pixels removed).

        **Background values**
        NOAA GML monthly means queried for each study period.
        A historical fixed value of 1,870 ppb overestimates enhancement by ~50 ppb for 2023 data.
        Always use period-specific NOAA GML values.

        **Data warehouse**
        Snowflake (free trial). Four schemas: RAW → STAGING → INTERMEDIATE → MARTS.
        dbt Core transformations. Batched inserts, 10,000 records,
        deduplicated on (date, latitude, longitude).

        **Official inventory**
        UNFCCC submissions via Climate Watch API (no API key required).
        Filter: gas = CH4, region = USA, all sectors combined.
        """)

    with mc2:
        st.markdown(f"""
        #### Limitations

        **Temporal coverage**
        Four months only (January + June–August). Spring and autumn data would
        complete the seasonal picture and reduce sampling bias in sector attribution.

        **Pixel footprint**
        5.5 × 3.5 km means facility-level plumes are diluted into surrounding background
        air within the column average. This is structural to TROPOMI, not an artifact of
        this analysis. It explains why the national mean falls below background.

        **Orbital sampling bias**
        Cloud cover systematically reduces valid observations in certain regions and seasons.
        No sampling correction is applied. Results should be interpreted with this in mind.

        **No uncertainty quantification**
        Implied emission ranges are not reported as confidence intervals.
        Required before academic submission.

        #### Reproduce This Analysis

        All data sources are free and publicly accessible.

        1. Account: `dataspace.copernicus.eu`
        2. Account: `snowflake.com` (free trial)
        3. Notebook: `github.com/likitha-sree-data/methane-truth`
        4. Run in Google Colab, following the cell sequence

        Runtime: approximately 2–3 hours (mostly download time).
        """)

    st.markdown('<div class="section-label">Citations</div>', unsafe_allow_html=True)
    st.markdown("""
    - ESA Sentinel-5P TROPOMI Level 2 Methane Product User Manual — sentinel.esa.int
    - NOAA Global Monitoring Laboratory — gml.noaa.gov/ccgg/trends_ch4
    - Turner et al. 2020 · *A large increase in US methane emissions over the past decade* · Science 369, 1219–1223
    - Alvarez et al. 2018 · *Assessment of methane emissions from the US oil and gas supply chain* · Science 361, 186–188
    - Climate Watch API Documentation — climatewatchdata.org/api
    """)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
    ESA Sentinel-5P TROPOMI &nbsp;·&nbsp; NOAA GML &nbsp;·&nbsp; UNFCCC via Climate Watch
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Zero proprietary data &nbsp;·&nbsp; Fully reproducible pipeline
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://github.com/likitha-sree-data/methane-truth">GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/likitha-sree">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
