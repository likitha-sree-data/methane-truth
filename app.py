import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Methane Truth | Satellite Emissions Analysis",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Design direction: Berkeley Earth / Nature Climate Change publication standard
# White page, hairline rules, Playfair Display for one headline only,
# IBM Plex Sans for all UI, IBM Plex Mono for all data readouts.
# Single accent: #0a7c6e (deep scientific teal from NOAA false-color CH4 imagery).
# No gradients. No shadows. No rounded corners above 2px. No decoration.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    box-sizing: border-box;
}
.stApp { background-color: #ffffff; }

section[data-testid="stSidebar"] {
    background-color: #0d1b24;
    border-right: 1px solid #1a2d3a;
}

/* Page header */
.pub-header {
    border-bottom: 2px solid #0a1014;
    padding: 2rem 0 1.5rem;
    margin-bottom: 2rem;
}
.pub-journal {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #0a7c6e;
    margin-bottom: 0.9rem;
}
.pub-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #0a1014;
    line-height: 1.15;
    margin: 0 0 0.8rem;
    letter-spacing: -0.5px;
}
.pub-abstract {
    font-size: 0.92rem;
    color: #3a4a54;
    line-height: 1.75;
    max-width: 720px;
    font-weight: 300;
    margin: 0 0 1.4rem;
}
.pub-meta {
    display: flex;
    gap: 0;
    border-top: 1px solid #d0d8de;
    border-bottom: 1px solid #d0d8de;
    padding: 0.7rem 0;
}
.pub-meta-item {
    padding: 0 2rem 0 0;
    margin-right: 2rem;
    border-right: 1px solid #d0d8de;
}
.pub-meta-item:last-child {
    border-right: none;
}
.pub-meta-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #7a9aaa;
    display: block;
    margin-bottom: 0.2rem;
}
.pub-meta-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #0a1014;
    font-weight: 500;
}

/* KPI strip */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    border: 1px solid #d0d8de;
    border-right: none;
    margin-bottom: 2.5rem;
}
.kpi-cell {
    padding: 1.3rem 1.4rem 1.1rem;
    border-right: 1px solid #d0d8de;
    border-top: 2px solid transparent;
    background: #ffffff;
}
.kpi-cell.hi { border-top-color: #0a7c6e; }
.kpi-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem;
    font-weight: 500;
    color: #0a1014;
    letter-spacing: -1px;
    line-height: 1;
    margin: 0;
}
.kpi-num.teal { color: #0a7c6e; }
.kpi-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #7a9aaa;
    margin: 0.5rem 0 0.2rem;
}
.kpi-note {
    font-size: 0.74rem;
    color: #9ab0bc;
    margin: 0;
    line-height: 1.4;
}

/* Section label */
.sec-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #0a7c6e;
    margin: 2.5rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #d0d8de;
}

/* Finding cards */
.find-card {
    background: #f8fafa;
    border: 1px solid #d0d8de;
    border-top: 2px solid #0a7c6e;
    padding: 1.5rem;
    height: 100%;
}
.find-region {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #0a1014;
    margin: 0 0 0.15rem;
}
.find-geo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #7a9aaa;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.9rem;
}
.find-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: #0a7c6e;
    letter-spacing: -1px;
    margin: 0 0 0.1rem;
    line-height: 1;
}
.find-peak {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #5a7a8a;
    margin-bottom: 0.9rem;
}
.find-detail {
    font-size: 0.81rem;
    color: #4a6070;
    line-height: 1.7;
    margin: 0;
    border-top: 1px solid #d0d8de;
    padding-top: 0.85rem;
    font-weight: 300;
}

/* Callouts */
.callout {
    background: #f4f8f7;
    border-left: 3px solid #0a7c6e;
    padding: 1rem 1.4rem;
    margin: 1.25rem 0;
    font-size: 0.85rem;
    color: #2a4a54;
    line-height: 1.8;
    font-weight: 300;
}
.callout strong { color: #0a1014; font-weight: 500; }

.callout-warn {
    background: #fdfaf4;
    border-left: 3px solid #b07020;
    padding: 0.9rem 1.4rem;
    margin: 0.75rem 0;
    font-size: 0.83rem;
    color: #5a4010;
    line-height: 1.75;
    font-weight: 300;
}
.callout-warn strong { color: #2a1a00; font-weight: 500; }

/* Sidebar */
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8edf2 !important;
    letter-spacing: -0.3px;
}
.sb-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    color: #0a7c6e !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.2rem;
}
.sb-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0a7c6e !important;
    margin-bottom: 0.4rem;
    display: block;
}
.sb-body {
    font-size: 0.8rem;
    color: #6a8a9a !important;
    line-height: 1.75;
    font-weight: 300;
}
.sb-body strong { color: #a8bfcc !important; font-weight: 500; }
.sb-hr { border: none; border-top: 1px solid #1a2d3a; margin: 1rem 0; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #f8f9fa;
    border: 1px solid #d0d8de;
    border-radius: 2px;
    padding: 0.15rem;
    gap: 0.1rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7a9aaa;
    border-radius: 1px;
    padding: 0.45rem 1.1rem;
    font-weight: 400;
    font-size: 0.83rem;
    font-family: 'IBM Plex Sans', sans-serif;
    letter-spacing: 0.2px;
}
.stTabs [aria-selected="true"] {
    background: #0a1014 !important;
    color: #ffffff !important;
}

/* Footer */
.pub-footer {
    border-top: 2px solid #0a1014;
    padding: 1.2rem 0;
    margin-top: 3rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #7a9aaa;
    letter-spacing: 0.3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.pub-footer a { color: #0a7c6e; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ─────────────────────────────────────────────────────────────────
BG_WINTER = 1919.93
BG_SUMMER = 1914.89
TEAL      = "#0a7c6e"
NAVY      = "#0a1014"
SLATE     = "#4a6070"
BORDER    = "#d0d8de"
PAGE      = "#ffffff"
CARD      = "#f8fafa"

TEAL_SCALE = [
    [0.00, "#e4f0ee"],
    [0.30, "#6abdb0"],
    [0.60, "#0a7c6e"],
    [0.85, "#065048"],
    [1.00, "#021a18"],
]

def base_layout(title="", height=380):
    return dict(
        paper_bgcolor=PAGE,
        plot_bgcolor=CARD,
        font=dict(family="IBM Plex Sans", color=SLATE, size=12),
        title=dict(
            text=title,
            font=dict(family="IBM Plex Sans", color=NAVY, size=13, weight=600),
            x=0,
        ),
        xaxis=dict(
            gridcolor=BORDER, linecolor=BORDER,
            tickfont=dict(family="IBM Plex Mono", color="#9ab0bc", size=10),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=BORDER, linecolor=BORDER,
            tickfont=dict(family="IBM Plex Mono", color="#9ab0bc", size=10),
            zeroline=False,
        ),
        legend=dict(
            bgcolor=PAGE, bordercolor=BORDER, borderwidth=1,
            font=dict(family="IBM Plex Sans", color=SLATE, size=11),
        ),
        margin=dict(l=10, r=10, t=44, b=10),
        height=height,
    )


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
            "Oil and Gas Systems", "Enteric Fermentation", "Municipal Solid Waste",
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

n_winter  = len(winter_df) if winter_df is not None else 73_486
n_summer  = len(summer_df) if summer_df is not None else 211_430
n_hs_w    = len(winter_hs) if winter_hs is not None else 15_902
n_hs_s    = len(summer_hs) if summer_hs is not None else 24_562
total_hs  = n_hs_w + n_hs_s
total_obs = n_winter + n_summer


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.4rem;">
        <div class="sb-logo">Methane Truth</div>
        <div class="sb-tagline">Satellite Emissions Analysis</div>
    </div>
    <hr class="sb-hr">
    <span class="sb-lbl">Study Coverage</span>
    <div class="sb-body">
        <strong>304,611</strong> quality-filtered observations<br>
        Winter: January 2023<br>
        Summer: June to August 2023<br>
        Continental USA, land pixels only
    </div>
    <hr class="sb-hr">
    <span class="sb-lbl">NOAA Verified Background</span>
    <div class="sb-body">
        January 2023 &nbsp;&nbsp;<strong>1,919.93 ppb</strong><br>
        Jun-Aug 2023 &nbsp;<strong>1,914.89 ppb</strong><br><br>
        <span style="font-size:0.72rem; color:#3a5a6a !important;">
        A fixed 1,870 ppb baseline overestimates<br>
        enhancement by approx. 50 ppb for 2023 data.
        </span>
    </div>
    <hr class="sb-hr">
    <span class="sb-lbl">Quality Standard</span>
    <div class="sb-body">
        ESA TROPOMI qa_value greater than 0.5<br>
        Plausibility filter: 1,600 to 2,200 ppb<br>
        Land mask applied post-download
    </div>
    <hr class="sb-hr">
    <span class="sb-lbl">Pipeline</span>
    <div class="sb-body">
        Python, xarray, Snowflake, dbt<br>
        Streamlit, GitHub Pages
    </div>
    <hr class="sb-hr">
    <span class="sb-lbl">Author</span>
    <div class="sb-body">
        <strong>Likitha Yarabarla</strong><br>
        Climate Data Engineer<br>
        <a href="https://linkedin.com/in/likitha-sree"
        style="color:#0a7c6e !important; text-decoration:none;">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="https://github.com/likitha-sree-data/methane-truth"
        style="color:#0a7c6e !important; text-decoration:none;">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pub-header">
    <div class="pub-journal">Satellite Emissions Analysis &nbsp;·&nbsp; ESA Sentinel-5P TROPOMI &nbsp;·&nbsp; NOAA GML &nbsp;·&nbsp; UNFCCC</div>
    <h1 class="pub-title">Methane Truth</h1>
    <p class="pub-abstract">
        304,611 quality-filtered satellite observations over the continental United States,
        January and June through August 2023. Only 14.1 percent of pixels detect methane
        above the verified global background. Those pixels cluster with geographic precision
        over three emission corridors, confirming satellite data as a geographic localization
        instrument rather than a national inventory verification tool.
    </p>
    <div class="pub-meta">
        <div class="pub-meta-item">
            <span class="pub-meta-label">Study Period</span>
            <span class="pub-meta-val">Jan + Jun-Aug 2023</span>
        </div>
        <div class="pub-meta-item">
            <span class="pub-meta-label">Instrument</span>
            <span class="pub-meta-val">TROPOMI / Sentinel-5P</span>
        </div>
        <div class="pub-meta-item">
            <span class="pub-meta-label">Resolution</span>
            <span class="pub-meta-val">5.5 x 3.5 km per pixel</span>
        </div>
        <div class="pub-meta-item">
            <span class="pub-meta-label">Background Source</span>
            <span class="pub-meta-val">NOAA GML Monthly Means</span>
        </div>
        <div class="pub-meta-item">
            <span class="pub-meta-label">Inventory Source</span>
            <span class="pub-meta-val">UNFCCC via Climate Watch API</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── WARNINGS ──────────────────────────────────────────────────────────────────
if missing_files:
    st.markdown(f"""
    <div class="callout-warn">
    <strong>Data files not found:</strong> {', '.join(missing_files)}<br>
    Place CSV files in the same directory as app.py.
    Charts render with illustrative data until real files are present.
    </div>
    """, unsafe_allow_html=True)


# ── KPI STRIP ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (f"{total_obs:,}", "Total Observations",     "Quality-filtered, land only",          False),
    (f"{total_hs:,}", "Hotspot Pixels",           "Exceeding NOAA monthly mean",          False),
    ("14.1%",          "Detection Rate",           "Pixels showing CH4 elevation",         True),
    ("+75.9 ppb",      "Peak Enhancement",         "Gulf Coast, single pixel maximum",     True),
    ("35.5 Mt CH4",    "Official 2022 Inventory",  "USA UNFCCC submission",                False),
]
for col, (val, label, note, hi) in zip([c1,c2,c3,c4,c5], kpis):
    with col:
        nc = "teal" if hi else ""
        hc = "hi"   if hi else ""
        st.markdown(f"""
        <div class="kpi-cell {hc}">
            <p class="kpi-num {nc}">{val}</p>
            <p class="kpi-lbl">{label}</p>
            <p class="kpi-note">{note}</p>
        </div>
        """, unsafe_allow_html=True)


# ── THREE FINDINGS ────────────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Primary Findings</div>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)
findings = [
    ("Northern Plains",      "Minnesota / North Dakota Border",
     "+56.3 ppb", "Peak 1,976.2 ppb · Winter 2023 · 485 hotspot pixels",
     "Winter signal at the MN-ND border. Consistent with thermogenic methane from "
     "Bakken formation oil and gas operations combined with agricultural wetland "
     "emissions. The seasonal winter peak is characteristic of O and G venting patterns."),
    ("Gulf Coast",           "Texas / Louisiana Offshore Corridor",
     "+75.9 ppb", "Peak 1,990.7 ppb · Summer 2023 · 1,271 hotspot pixels",
     "Highest single pixel in the dataset. Offshore petrochemical operations "
     "between Houston and New Orleans. Summer peak consistent with increased "
     "production activity and temperature-driven venting in the Gulf basin."),
    ("California Central Valley", "San Joaquin Agricultural Core",
     "+70.3 ppb", "Peak 1,985.2 ppb · Summer 2023 · 1,221 hotspot pixels",
     "Dairy farming and rice agriculture. Largest agricultural CH4 source region "
     "in the western United States. Signal persists across the full June-August "
     "window, consistent with enteric fermentation and flooded paddy field emissions."),
]
for col, (region, geo, val, peak, detail) in zip([fc1,fc2,fc3], findings):
    with col:
        st.markdown(f"""
        <div class="find-card">
            <div class="find-region">{region}</div>
            <div class="find-geo">{geo}</div>
            <div class="find-val">{val}</div>
            <div class="find-peak">{peak}</div>
            <p class="find-detail">{detail}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="callout">
<strong>On column dilution:</strong>
The satellite mean concentration falls below the NOAA background for both seasons.
This is not a data error. It is the expected behavior of passive column-integrated remote sensing.
TROPOMI pixels are 5.5 x 3.5 km. Emission plumes dilute rapidly into background air at this scale.
The 14.1 percent of pixels that show elevation are not randomly distributed.
They cluster precisely over known source regions, confirming that satellite monitoring functions
as a <strong>geographic localization instrument</strong>, not a national inventory verification tool.
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
# TAB 1: MAPS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-label">Satellite Methane Concentration Maps</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <p style="color:{SLATE}; font-size:0.86rem; margin-bottom:1.25rem;
    max-width:740px; line-height:1.75; font-weight:300;">
    Each point represents an ESA Sentinel-5P TROPOMI pixel at 5.5 x 3.5 km resolution.
    The hotspot view renders all 43,086 above-background pixels without sampling.
    Full-dataset views sample 5,000 points for rendering performance.
    Color encodes methane column concentration relative to the NOAA verified monthly background.
    </p>
    """, unsafe_allow_html=True)

    map_choice = st.radio(
        "Select view",
        [
            "Hotspots: all 43,086 above-background pixels",
            "Winter full dataset: January 2023 (5,000 sample)",
            "Summer full dataset: June to August 2023 (5,000 sample)",
        ],
    )

    if "Hotspot" in map_choice:
        if winter_hs is not None and summer_hs is not None:
            plot_df = pd.concat([winter_hs, summer_hs], ignore_index=True)
        else:
            rng  = np.random.default_rng(42)
            lats = np.concatenate([rng.normal(47.5,1.2,485), rng.normal(29.0,0.8,1271), rng.normal(36.5,1.0,1221)])
            lons = np.concatenate([rng.normal(-97.5,1.5,485), rng.normal(-91.5,1.2,1271), rng.normal(-120.0,0.8,1221)])
            ppbs = np.concatenate([rng.uniform(1920,1976,485), rng.uniform(1915,1991,1271), rng.uniform(1915,1985,1221)])
            plot_df = pd.DataFrame({"latitude": lats, "longitude": lons, "methane_column_ppb": ppbs})
        cmin, cmax = 1915, 1992
        map_title  = "Emission Hotspots: Pixels Exceeding NOAA Verified Background"
        caption    = "All above-background pixels, winter and summer combined. No sampling applied."
        dot_sz     = 3

    elif "Winter" in map_choice:
        src = winter_df if winter_df is not None else pd.DataFrame({
            "latitude":  np.random.uniform(30, 49, 5000),
            "longitude": np.random.uniform(-125, -67, 5000),
            "methane_column_ppb": np.random.normal(1904, 12, 5000),
        })
        plot_df   = src.sample(min(5000, len(src)), random_state=42)
        cmin, cmax = 1875, 1980
        map_title  = "Winter Methane Concentrations: USA, January 2023"
        caption    = f"NOAA verified background: {BG_WINTER} ppb, January 2023"
        dot_sz     = 2

    else:
        src = summer_df if summer_df is not None else pd.DataFrame({
            "latitude":  np.random.uniform(30, 49, 5000),
            "longitude": np.random.uniform(-125, -67, 5000),
            "methane_column_ppb": np.random.normal(1895, 15, 5000),
        })
        plot_df   = src.sample(min(5000, len(src)), random_state=42)
        cmin, cmax = 1870, 1992
        map_title  = "Summer Methane Concentrations: USA, June to August 2023"
        caption    = f"NOAA verified background: {BG_SUMMER} ppb, summer 2023 average"
        dot_sz     = 2

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
                tickfont=dict(family="IBM Plex Mono", color="#9ab0bc", size=9),
                thickness=10, len=0.6,
                bgcolor=PAGE, bordercolor=BORDER, x=1.01,
            ),
        ),
        hovertemplate="%{customdata:.1f} ppb<br>%{lat:.3f}N %{lon:.3f}W<extra></extra>",
        customdata=plot_df["methane_column_ppb"],
    ))

    pins = [
        dict(lat=47.5,  lon=-97.5,  label="Northern Plains"),
        dict(lat=29.0,  lon=-91.5,  label="Gulf Coast"),
        dict(lat=36.5,  lon=-120.2, label="Central Valley"),
    ]
    for pin in pins:
        fig_map.add_trace(go.Scattergeo(
            lat=[pin["lat"]], lon=[pin["lon"]],
            mode="markers+text",
            marker=dict(size=9, color=TEAL, symbol="circle-open",
                        line=dict(color=TEAL, width=2)),
            text=[pin["label"]],
            textfont=dict(family="IBM Plex Mono", color=TEAL, size=9),
            textposition="top right",
            hoverinfo="skip", showlegend=False,
        ))

    fig_map.update_layout(
        title=dict(text=map_title,
                   font=dict(family="IBM Plex Sans", color=NAVY, size=13, weight=600), x=0),
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,       landcolor="#edf1f4",
            showocean=True,      oceancolor="#dce4ea",
            showlakes=True,      lakecolor="#dce4ea",
            showcoastlines=True, coastlinecolor="#b0bece",
            showsubunits=True,   subunitcolor="#c4ceda",
            bgcolor=PAGE,
        ),
        paper_bgcolor=PAGE,
        margin=dict(l=0, r=100, t=44, b=0),
        height=540,
        font=dict(family="IBM Plex Sans", color=SLATE),
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(caption + " · Source: ESA Copernicus Data Space L2 CH4 · qa_value greater than 0.5")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: SECTOR ATTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-label">USA Methane by Sector: UNFCCC 2022 Submission</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <p style="color:{SLATE}; font-size:0.86rem; margin-bottom:1.25rem;
    max-width:740px; line-height:1.75; font-weight:300;">
    The USA officially reports 35.5 Mt CH4 for 2022. Oil and gas systems and enteric
    fermentation together account for 54 percent of that total. The three satellite hotspots
    map geographically onto precisely these two sectors. That alignment is the core
    validation this analysis provides.
    </p>
    """, unsafe_allow_html=True)

    sd   = sector_data()
    sc1, sc2 = st.columns([3, 2])

    with sc1:
        fig_bar = go.Figure(go.Bar(
            x=sd["mt_ch4"],
            y=sd["sector"],
            orientation="h",
            marker=dict(
                color=sd["mt_ch4"],
                colorscale=[[0,"#d0e8e4"],[0.5,"#5ab0a4"],[1,TEAL]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=[f"{v:.1f} Mt" for v in sd["mt_ch4"]],
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=10),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x:.1f} Mt CH4<br>%{customdata:.1f}%<extra></extra>",
            customdata=sd["pct"],
        ))
        layout_bar = base_layout("CH4 Emissions by Sector, 2022", height=380)
        layout_bar["xaxis"]["title"] = "Mt CH4 per year"
        layout_bar["xaxis"]["range"] = [0, 13.5]
        layout_bar["yaxis"]["categoryorder"] = "total ascending"
        fig_bar.update_layout(**layout_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    with sc2:
        fig_pie = go.Figure(go.Pie(
            labels=sd["sector"],
            values=sd["mt_ch4"],
            hole=0.58,
            marker=dict(
                colors=[TEAL,"#5ab0a4","#3a9088","#2a7068",
                        "#d0e8e4","#b0d4d0","#e4f0ee","#f0f8f7"],
                line=dict(color=PAGE, width=2),
            ),
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=9),
            hovertemplate="<b>%{label}</b><br>%{value:.1f} Mt · %{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text="35.5 Mt<br>CH4 2022",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="IBM Plex Mono", size=11, color=NAVY),
        )
        layout_pie = base_layout("Sector Share", height=380)
        layout_pie["paper_bgcolor"] = PAGE
        layout_pie["plot_bgcolor"]  = PAGE
        layout_pie["margin"] = dict(l=0, r=0, t=44, b=0)
        fig_pie.update_layout(**layout_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    <div class="callout">
    <strong>Satellite-to-sector alignment:</strong>
    Oil and gas systems (30.4 percent, 10.8 Mt) and enteric fermentation (23.7 percent, 8.4 Mt)
    together represent 54 percent of the official US methane inventory.
    The Gulf Coast hotspot (+75.9 ppb) maps onto offshore oil and gas infrastructure.
    The Central Valley hotspot (+70.3 ppb) maps onto California's dairy sector.
    The Northern Plains winter signal overlaps both Bakken formation O and G activity
    and agricultural wetlands. The satellite does not verify the totals.
    It verifies the <strong>geography</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Official Inventory Trend 2015 to 2022</div>',
                unsafe_allow_html=True)

    if official is not None and "year" in official.columns:
        tr = official
    else:
        tr = pd.DataFrame({
            "year":             list(range(2015, 2023)),
            "reported_Mt_CH4": [36.1, 35.8, 35.5, 35.7, 35.3, 35.0, 35.4, 35.5],
        })

    fig_tr = go.Figure()
    fig_tr.add_trace(go.Scatter(
        x=tr["year"], y=tr["reported_Mt_CH4"],
        mode="lines+markers",
        line=dict(color=TEAL, width=2),
        marker=dict(size=6, color=TEAL, line=dict(color=PAGE, width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(10,124,110,0.06)",
        hovertemplate="<b>%{x}</b> · %{y:.1f} Mt CH4<extra></extra>",
    ))
    layout_tr = base_layout("USA Official CH4: UNFCCC Annual Submissions (Mt CH4)", height=260)
    layout_tr["xaxis"]["tickvals"] = list(range(2015, 2023))
    layout_tr["yaxis"]["range"]    = [30, 42]
    fig_tr.update_layout(**layout_tr)
    st.plotly_chart(fig_tr, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: SEASONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-label">Seasonal Analysis</div>', unsafe_allow_html=True)

    sa1, sa2 = st.columns(2)

    with sa1:
        dist = pd.DataFrame({
            "Season":   ["Winter","Winter","Summer","Summer"],
            "Category": ["Below background","Above background",
                         "Below background","Above background"],
            "Pct":      [78.5, 21.5, 88.3, 11.7],
        })
        fig_dist = px.bar(
            dist, x="Season", y="Pct", color="Category",
            color_discrete_map={"Below background":"#d8e4ea","Above background":TEAL},
            title="Pixel Distribution Relative to NOAA Background",
            labels={"Pct":"Percent of observations"},
            text="Pct", height=360, barmode="stack",
        )
        fig_dist.update_traces(
            texttemplate="%{text:.1f}%", textposition="inside",
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=11),
        )
        layout_d = base_layout("", height=360)
        layout_d["title"]["text"] = "Pixel Distribution Relative to NOAA Background"
        fig_dist.update_layout(**layout_d)
        st.plotly_chart(fig_dist, use_container_width=True)

    with sa2:
        enh = pd.DataFrame({
            "Region": ["Northern Plains","Gulf Coast","Central Valley"],
            "ppb":    [56.3, 75.9, 70.3],
            "Peak":   [1976.2, 1990.7, 1985.2],
        })
        fig_enh = go.Figure(go.Bar(
            x=enh["Region"], y=enh["ppb"],
            marker=dict(
                color=enh["ppb"],
                colorscale=[[0,"#d0e8e4"],[1,TEAL]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=[f"+{v} ppb" for v in enh["ppb"]],
            textfont=dict(family="IBM Plex Mono", color=NAVY, size=10),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>+%{y} ppb<br>Peak: %{customdata} ppb<extra></extra>",
            customdata=enh["Peak"],
        ))
        layout_enh = base_layout("Peak Enhancement Above NOAA Background", height=360)
        layout_enh["yaxis"]["title"] = "Enhancement (ppb)"
        layout_enh["yaxis"]["range"] = [0, 92]
        fig_enh.update_layout(**layout_enh)
        st.plotly_chart(fig_enh, use_container_width=True)

    st.markdown('<div class="sec-label">Summary Statistics</div>', unsafe_allow_html=True)
    summ = pd.DataFrame({
        "Season": ["Winter: January 2023","Summer: Jun-Aug 2023","Combined"],
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
# TAB 4: HOTSPOT DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-label">Emission Hotspot Detail</div>', unsafe_allow_html=True)

    ht = pd.DataFrame({
        "Region":             ["Northern Plains MN-ND","Gulf Coast TX-LA","CA Central Valley"],
        "Season":             ["Winter","Summer","Summer"],
        "Hotspot Pixels":     [485, 1271, 1221],
        "Peak Conc. (ppb)":   [1976.2, 1990.7, 1985.2],
        "Peak Enhancement":   ["+56.3 ppb","+75.9 ppb","+70.3 ppb"],
        "Likely Source":      [
            "Agricultural wetlands + Bakken O and G",
            "Offshore petrochemical, Gulf basin",
            "Dairy and rice agriculture",
        ],
        "UNFCCC Sector":      ["Oil and Gas / Agriculture","Oil and Gas","Enteric Fermentation"],
    })
    st.dataframe(ht, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hc1, hc2 = st.columns(2)

    with hc1:
        src_w = winter_hs if winter_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1930,12,n_hs_w).clip(BG_WINTER, 1985)})
        fig_wh = px.histogram(
            src_w, x="methane_column_ppb", nbins=50,
            title=f"Winter Hotspot Distribution: {n_hs_w:,} pixels",
            labels={"methane_column_ppb":"CH4 (ppb)","count":"Pixels"},
            color_discrete_sequence=[TEAL], height=340,
        )
        fig_wh.add_vline(
            x=BG_WINTER, line_dash="dot", line_color="#b06020", line_width=1.5,
            annotation_text=f"Background {BG_WINTER} ppb",
            annotation_font_color="#b06020", annotation_font_size=9,
        )
        layout_wh = base_layout("", height=340)
        layout_wh["title"]["text"] = f"Winter Hotspot Distribution: {n_hs_w:,} pixels"
        fig_wh.update_layout(**layout_wh)
        st.plotly_chart(fig_wh, use_container_width=True)

    with hc2:
        src_s = summer_hs if summer_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1925,15,n_hs_s).clip(BG_SUMMER, 1992)})
        fig_sh = px.histogram(
            src_s, x="methane_column_ppb", nbins=50,
            title=f"Summer Hotspot Distribution: {n_hs_s:,} pixels",
            labels={"methane_column_ppb":"CH4 (ppb)","count":"Pixels"},
            color_discrete_sequence=["#065048"], height=340,
        )
        fig_sh.add_vline(
            x=BG_SUMMER, line_dash="dot", line_color="#b06020", line_width=1.5,
            annotation_text=f"Background {BG_SUMMER} ppb",
            annotation_font_color="#b06020", annotation_font_size=9,
        )
        layout_sh = base_layout("", height=340)
        layout_sh["title"]["text"] = f"Summer Hotspot Distribution: {n_hs_s:,} pixels"
        fig_sh.update_layout(**layout_sh)
        st.plotly_chart(fig_sh, use_container_width=True)

    st.markdown("""
    <div class="callout">
    <strong>Facility attribution as next step:</strong>
    Cross-referencing these hotspot coordinates against the EPA GHGRP facility-level database
    would attribute specific pixel clusters to named facilities: refineries, compressor stations,
    dairy CAFOs. That is the transition from geographic localization to facility-level
    accountability, and it is what separates a portfolio project from a publishable analysis.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-label">Methodology</div>', unsafe_allow_html=True)

    mc1, mc2 = st.columns(2)

    with mc1:
        st.markdown("""
        #### Pipeline

        **Satellite ingestion**
        ESA Sentinel-5P TROPOMI L2 methane product. Downloaded via Copernicus Data Space API.
        Parsed from netCDF4 with xarray. Key variable:
        `methane_mixing_ratio_bias_corrected`, shape `(time, scanline, ground_pixel)`.

        **Quality filtering**
        `qa_value > 0.5` per ESA TROPOMI L2 documentation.
        Plausibility bounds: 1,600 to 2,200 ppb.
        Bounding box: lat 24 to 50 N, lon 66 to 125 W.
        Custom land mask removes ocean pixels (3,648 winter + 16,047 summer removed).

        **Background values**
        NOAA GML monthly means queried for each study period.
        A historical fixed value of 1,870 ppb overestimates enhancement
        by approximately 50 ppb for 2023 data. Period-specific values are required.

        **Data warehouse**
        Snowflake (free trial). Four schemas: RAW, STAGING, INTERMEDIATE, MARTS.
        dbt Core transformations. Batched inserts of 10,000 records,
        deduplicated on (date, latitude, longitude).

        **Official inventory**
        UNFCCC submissions via Climate Watch API, no API key required.
        Filter: gas = CH4, region = USA, all sectors combined.
        """)

    with mc2:
        st.markdown("""
        #### Limitations

        **Temporal coverage**
        Four months only. Spring and autumn data would complete the seasonal picture
        and reduce sampling bias in sector attribution.

        **Pixel footprint**
        5.5 x 3.5 km means facility-level plumes are diluted into surrounding background
        air within the column average. This is structural to TROPOMI, not an artifact
        of this analysis.

        **Orbital sampling bias**
        Cloud cover systematically reduces valid observations in certain regions and seasons.
        No sampling correction is applied.

        **No uncertainty quantification**
        Implied emission ranges are not reported as confidence intervals.
        Required before academic submission.

        #### Reproduce This Analysis

        1. Register at `dataspace.copernicus.eu`
        2. Register at `snowflake.com` (free trial)
        3. Open notebook at `github.com/likitha-sree-data/methane-truth`
        4. Run in Google Colab following the cell sequence

        Runtime: approximately 2 to 3 hours, mostly download time.
        Zero proprietary data used.
        """)

    st.markdown('<div class="sec-label">Citations</div>', unsafe_allow_html=True)
    st.markdown("""
    - ESA Sentinel-5P TROPOMI Level 2 Methane Product User Manual. sentinel.esa.int
    - NOAA Global Monitoring Laboratory. gml.noaa.gov/ccgg/trends_ch4
    - Turner et al. 2020. A large increase in US methane emissions over the past decade. Science 369, 1219-1223
    - Alvarez et al. 2018. Assessment of methane emissions from the US oil and gas supply chain. Science 361, 186-188
    - Climate Watch API Documentation. climatewatchdata.org/api
    """)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pub-footer">
    <span>ESA Sentinel-5P TROPOMI &nbsp;·&nbsp; NOAA GML &nbsp;·&nbsp; UNFCCC via Climate Watch &nbsp;·&nbsp; Zero proprietary data &nbsp;·&nbsp; Fully reproducible</span>
    <span>
        <a href="https://github.com/likitha-sree-data/methane-truth">GitHub</a>
        &nbsp;·&nbsp;
        <a href="https://linkedin.com/in/likitha-sree">LinkedIn</a>
    </span>
</div>
""", unsafe_allow_html=True)
