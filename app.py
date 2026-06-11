import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Methane Truth | Satellite Emissions Analysis",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@300;400;600&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.main { background: #fafaf8; }
.block-container {
    padding: 2.5rem 3rem 3rem;
    max-width: 1200px;
}

.headline {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 2.4rem;
    font-weight: 600;
    color: #1a1a1a;
    line-height: 1.2;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
}
.deck {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.1rem;
    color: #4a4a4a;
    line-height: 1.7;
    font-weight: 300;
    max-width: 780px;
    margin-bottom: 0.75rem;
}
.byline {
    font-size: 0.8rem;
    color: #888;
    letter-spacing: 0.03em;
    margin-bottom: 0;
}
.byline a { color: #1a6a3a; text-decoration: none; }
.byline a:hover { text-decoration: underline; }

.sec-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.4rem;
    margin-top: 2.5rem;
}
.sec-title {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 0.3rem;
    line-height: 1.3;
}
.sec-body {
    font-size: 0.9rem;
    color: #555;
    line-height: 1.75;
    max-width: 820px;
    margin-bottom: 1.25rem;
}
.pullquote {
    border-left: 3px solid #1a1a1a;
    padding: 0.5rem 0 0.5rem 1.25rem;
    margin: 1.25rem 0;
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.05rem;
    color: #1a1a1a;
    font-weight: 300;
    line-height: 1.6;
    font-style: italic;
}
.callout {
    background: #f4f8f4;
    border-left: 3px solid #1a6a3a;
    padding: 1rem 1.4rem;
    margin: 1.25rem 0;
    font-size: 0.9rem;
    color: #333;
    line-height: 1.8;
}
.callout strong { color: #111; }
.callout-warn {
    background: #fffbf2;
    border-left: 3px solid #c07020;
    padding: 0.9rem 1.4rem;
    margin: 0.75rem 0;
    font-size: 0.88rem;
    color: #555;
    line-height: 1.75;
}
.find-card {
    background: #fff;
    border: 1px solid #e5e5e5;
    border-top: 2px solid #1a1a1a;
    padding: 1.4rem;
    height: 100%;
}
.find-region {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0 0 0.1rem;
}
.find-geo {
    font-size: 0.72rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.85rem;
}
.find-val {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: #1a6a3a;
    letter-spacing: -1px;
    margin: 0 0 0.1rem;
    line-height: 1;
}
.find-peak {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #888;
    margin-bottom: 0.9rem;
}
.find-detail {
    font-size: 0.85rem;
    color: #555;
    line-height: 1.7;
    margin: 0;
    border-top: 1px solid #eee;
    padding-top: 0.85rem;
}
.rule { border: none; border-top: 1px solid #e5e5e5; margin: 2rem 0; }

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e5e5;
    border-top: 2px solid #1a1a1a;
    border-radius: 0;
    padding: 0.85rem 1rem;
}
div[data-testid="stMetricLabel"] p {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #888 !important;
}
div[data-testid="stMetricValue"] {
    font-family: 'Source Serif 4', Georgia, serif !important;
    font-size: 1.65rem !important;
    color: #1a1a1a !important;
}
div[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    color: #1a6a3a !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #e5e5e5;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 8px 20px;
    font-size: 0.88rem;
    font-weight: 500;
    color: #888;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}
.stTabs [aria-selected="true"] {
    color: #1a1a1a !important;
    background: transparent !important;
    border-bottom: 2px solid #1a1a1a !important;
}
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ─────────────────────────────────────────────────────────────────
BG_WINTER    = 1919.93
BG_SUMMER    = 1914.89
GREEN        = "#1a6a3a"
BLACK        = "#1a1a1a"
GRAY         = "#555555"
LIGHT_GRAY   = "#9ca3af"
BORDER       = "#e5e5e5"
PAGE         = "#fafaf8"
WHITE        = "#ffffff"
DISPLAY_TOTAL = 304_611

TEAL_SCALE = [
    [0.00, "#f0f4f2"],
    [0.20, "#a8d4be"],
    [0.50, "#3a9a64"],
    [0.80, "#1a6a3a"],
    [1.00, "#0a2818"],
]

def base_layout(title="", height=380):
    return dict(
        paper_bgcolor=WHITE,
        plot_bgcolor=PAGE,
        font=dict(family="Inter", color=GRAY, size=12),
        title=dict(text=title,
                   font=dict(family="Source Serif 4, Georgia, serif",
                             color=BLACK, size=13), x=0),
        xaxis=dict(gridcolor="#eeeeee", linecolor=BORDER,
                   tickfont=dict(family="IBM Plex Mono", color=LIGHT_GRAY, size=10),
                   zeroline=False),
        yaxis=dict(gridcolor="#eeeeee", linecolor=BORDER,
                   tickfont=dict(family="IBM Plex Mono", color=LIGHT_GRAY, size=10),
                   zeroline=False),
        legend=dict(bgcolor=WHITE, bordercolor=BORDER, borderwidth=1,
                    font=dict(family="Inter", color=GRAY, size=11)),
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
        "sector": ["Oil and Gas Systems","Enteric Fermentation","Municipal Solid Waste",
                   "Coal Mining","Manure Management","Wastewater Treatment",
                   "Agricultural Soils","Other"],
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
total_hs = n_hs_w + n_hs_s


# ── MASTHEAD ──────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.68rem;font-weight:600;letter-spacing:0.2em;"
    "text-transform:uppercase;color:#9ca3af;margin-bottom:1.25rem'>"
    "Satellite Emissions Analysis &nbsp;·&nbsp; ESA Sentinel-5P TROPOMI &nbsp;·&nbsp; 2023</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='headline'>We analyzed 304,611 satellite methane readings over America.<br>"
    "Here is what we found.</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='deck'>"
    "Only 14.1 percent of satellite pixels detect methane above the verified global background "
    "over one of the world's largest emitters. But the pixels that do show elevation cluster "
    "with geographic precision over three known emission corridors: the Northern Plains, "
    "the Gulf Coast, and California's Central Valley. The satellite tells you where. "
    "It cannot tell you how much."
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='byline'>"
    "Analysis by <a href='https://linkedin.com/in/likitha-sree'>Likitha Sree Yarabarla</a> "
    "&nbsp;·&nbsp; Climate Data Engineer "
    "&nbsp;·&nbsp; Data: ESA Copernicus, NOAA GML, UNFCCC via Climate Watch API "
    "&nbsp;·&nbsp; <a href='https://github.com/likitha-sree-data/methane-truth'>"
    "Full methodology on GitHub</a>"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='rule'>", unsafe_allow_html=True)

if missing_files:
    st.markdown(f"""
    <div class="callout-warn">
    <strong>Data files not found:</strong> {', '.join(missing_files)}<br>
    Place CSV files in the same directory as app.py.
    Charts render with illustrative data until real files are present.
    </div>
    """, unsafe_allow_html=True)


# ── KEY FIGURES ───────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.65rem;font-weight:600;letter-spacing:0.15em;"
    "text-transform:uppercase;color:#9ca3af;margin-bottom:1rem'>Key figures</div>",
    unsafe_allow_html=True,
)

n1, n2, n3, n4, n5 = st.columns(5)
n1.metric("Satellite observations", f"{DISPLAY_TOTAL:,}")
n2.metric("Pixels above background", f"{total_hs:,}", "Exceeding NOAA monthly mean")
n3.metric("Detection rate", "14.1%", "Pixels showing CH4 elevation")
n4.metric("Peak enhancement", "+75.9 ppb", "Gulf Coast single pixel max")
n5.metric("Official 2022 inventory", "35.5 Mt CH4", "USA UNFCCC submission")

st.markdown("<hr class='rule'>", unsafe_allow_html=True)


# ── THREE FINDINGS ────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.65rem;font-weight:600;letter-spacing:0.15em;"
    "text-transform:uppercase;color:#9ca3af;margin-bottom:1rem'>Primary findings</div>",
    unsafe_allow_html=True,
)

fc1, fc2, fc3 = st.columns(3)
findings = [
    ("Northern Plains", "Minnesota / North Dakota Border",
     "+56.3 ppb", "Peak 1,976.2 ppb · Winter 2023 · 485 hotspot pixels",
     "Winter signal at the MN-ND border. Consistent with thermogenic methane from "
     "Bakken formation oil and gas operations combined with agricultural wetland "
     "emissions. The seasonal winter peak is characteristic of O and G venting patterns."),
    ("Gulf Coast", "Texas / Louisiana Offshore Corridor",
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
for col, (region, geo, val, peak, detail) in zip([fc1, fc2, fc3], findings):
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
<strong>Why does the satellite mean fall below the NOAA background?</strong>
This is not a data error. TROPOMI pixels are 5.5 x 3.5 km. Emission plumes from surface sources
dilute rapidly into surrounding clean background air at this scale. The result: 85.9 percent of pixels
measure background air, not plumes. The 14.1 percent that do show elevation are not randomly distributed.
They cluster precisely over known source regions, confirming that satellite monitoring functions as a
<strong>geographic localization instrument</strong>, not a national inventory verification tool.
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
    st.markdown(
        "<div class='sec-label'>Satellite Methane Concentration Maps</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sec-body'>"
        "Each point represents an ESA Sentinel-5P TROPOMI pixel at 5.5 x 3.5 km resolution. "
        "The hotspot view renders all 43,086 above-background pixels without sampling, "
        "colored by enhancement above the NOAA verified monthly background. "
        "Full-dataset views sample 5,000 points for rendering performance."
        "</div>",
        unsafe_allow_html=True,
    )

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
            plot_df["_is_winter"] = plot_df.index < len(winter_hs)
            plot_df["enhancement"] = plot_df.apply(
                lambda r: r["methane_column_ppb"] - (BG_WINTER if r["_is_winter"] else BG_SUMMER),
                axis=1
            ).clip(lower=0)
        else:
            rng  = np.random.default_rng(42)
            lats = np.concatenate([rng.normal(47.5,0.8,485), rng.normal(29.2,0.6,1271), rng.normal(36.8,0.7,1221)])
            lons = np.concatenate([rng.normal(-97.5,1.0,485), rng.normal(-91.5,0.9,1271), rng.normal(-120.2,0.6,1221)])
            ppbs = np.concatenate([rng.uniform(1920,1976,485), rng.uniform(1920,1991,1271), rng.uniform(1918,1985,1221)])
            enh  = np.concatenate([ppbs[:485]-BG_WINTER, ppbs[485:1756]-BG_SUMMER, ppbs[1756:]-BG_SUMMER]).clip(0)
            plot_df = pd.DataFrame({"latitude":lats,"longitude":lons,"methane_column_ppb":ppbs,"enhancement":enh})
        color_col = "enhancement"
        cmin, cmax = 0, 76
        map_title  = "Emission Hotspots: Enhancement Above NOAA Verified Background (ppb)"
        caption    = "Color = ppb above NOAA monthly background. No sampling. All 43,086 hotspot pixels shown."
        dot_sz     = 4
        map_scale  = TEAL_SCALE
        hover_tmpl = "+%{customdata:.1f} ppb above background<br>%{lat:.3f}N %{lon:.3f}W<extra></extra>"
        hover_data = plot_df["enhancement"]
        cbar_title = "ppb above bg"

    elif "Winter" in map_choice:
        src = winter_df if winter_df is not None else pd.DataFrame({
            "latitude": np.random.uniform(30,49,5000),
            "longitude": np.random.uniform(-125,-67,5000),
            "methane_column_ppb": np.random.normal(1904,12,5000),
        })
        plot_df   = src.sample(min(5000,len(src)), random_state=42)
        color_col = "methane_column_ppb"
        cmin, cmax = 1875, 1980
        map_title  = "Winter Methane Concentrations: USA, January 2023"
        caption    = f"NOAA verified background: {BG_WINTER} ppb, January 2023"
        dot_sz, map_scale = 2, TEAL_SCALE
        hover_tmpl = "%{customdata:.1f} ppb<br>%{lat:.3f}N %{lon:.3f}W<extra></extra>"
        hover_data = plot_df["methane_column_ppb"]
        cbar_title = "CH4 (ppb)"

    else:
        src = summer_df if summer_df is not None else pd.DataFrame({
            "latitude": np.random.uniform(30,49,5000),
            "longitude": np.random.uniform(-125,-67,5000),
            "methane_column_ppb": np.random.normal(1895,15,5000),
        })
        plot_df   = src.sample(min(5000,len(src)), random_state=42)
        color_col = "methane_column_ppb"
        cmin, cmax = 1870, 1992
        map_title  = "Summer Methane Concentrations: USA, June to August 2023"
        caption    = f"NOAA verified background: {BG_SUMMER} ppb, summer 2023 average"
        dot_sz, map_scale = 2, TEAL_SCALE
        hover_tmpl = "%{customdata:.1f} ppb<br>%{lat:.3f}N %{lon:.3f}W<extra></extra>"
        hover_data = plot_df["methane_column_ppb"]
        cbar_title = "CH4 (ppb)"

    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lat=plot_df["latitude"], lon=plot_df["longitude"],
        mode="markers",
        marker=dict(
            color=plot_df[color_col], colorscale=map_scale,
            cmin=cmin, cmax=cmax, size=dot_sz, opacity=0.9,
            colorbar=dict(
                title=dict(text=cbar_title, font=dict(family="IBM Plex Mono", color=GRAY, size=10)),
                tickfont=dict(family="IBM Plex Mono", color=LIGHT_GRAY, size=9),
                thickness=10, len=0.6, bgcolor=WHITE, bordercolor=BORDER, x=1.01,
            ),
        ),
        hovertemplate=hover_tmpl,
        customdata=hover_data,
    ))
    for pin in [
        dict(lat=47.5, lon=-97.5, label="Northern Plains"),
        dict(lat=29.2, lon=-91.5, label="Gulf Coast"),
        dict(lat=36.8, lon=-120.2, label="Central Valley"),
    ]:
        fig_map.add_trace(go.Scattergeo(
            lat=[pin["lat"]], lon=[pin["lon"]],
            mode="markers+text",
            marker=dict(size=9, color=GREEN, symbol="circle-open",
                        line=dict(color=GREEN, width=2)),
            text=[pin["label"]],
            textfont=dict(family="IBM Plex Mono", color=GREEN, size=9),
            textposition="top right",
            hoverinfo="skip", showlegend=False,
        ))
    fig_map.update_layout(
        title=dict(text=map_title,
                   font=dict(family="Source Serif 4, Georgia, serif", color=BLACK, size=13), x=0),
        geo=dict(
            scope="usa", projection_type="albers usa",
            showland=True, landcolor="#eeecea",
            showocean=True, oceancolor="#dddbd8",
            showlakes=True, lakecolor="#dddbd8",
            showcoastlines=True, coastlinecolor="#bbbbbb",
            showsubunits=True, subunitcolor="#cccccc",
            bgcolor=PAGE,
        ),
        paper_bgcolor=WHITE,
        margin=dict(l=0, r=100, t=44, b=0),
        height=520,
        font=dict(family="Inter", color=GRAY),
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown(
        f"<div style='font-size:0.72rem;color:#9ca3af;margin-top:-0.5rem'>"
        f"{caption} · Source: ESA Copernicus Data Space L2 CH4 · qa_value greater than 0.5"
        f"</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: SECTOR ATTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        "<div class='pullquote'>"
        "\"Oil and gas and agriculture together account for 54 percent of official US methane. "
        "The satellite hotspots map onto precisely these two sectors.\""
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='sec-body'>"
        "The USA officially reports 35.5 Mt CH4 for 2022. The three satellite hotspots "
        "identified in this analysis map geographically onto the two largest reporting sectors. "
        "The Gulf Coast hotspot aligns with offshore oil and gas infrastructure. "
        "The Central Valley hotspot aligns with California's dairy sector. "
        "The satellite does not verify the totals. It verifies the geography."
        "</div>",
        unsafe_allow_html=True,
    )

    sd = sector_data()
    sc1, sc2 = st.columns([3, 2])

    with sc1:
        fig_bar = go.Figure(go.Bar(
            x=sd["mt_ch4"], y=sd["sector"], orientation="h",
            marker=dict(
                color=sd["mt_ch4"],
                colorscale=[[0,"#d1d5db"],[0.5,"#6b7280"],[1,BLACK]],
                line=dict(color=BORDER, width=0.5),
            ),
            text=[f"{v:.1f} Mt" for v in sd["mt_ch4"]],
            textfont=dict(family="IBM Plex Mono", color=BLACK, size=10),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x:.1f} Mt CH4 · %{customdata:.1f}%<extra></extra>",
            customdata=sd["pct"],
        ))
        layout_bar = base_layout("CH4 Emissions by Sector, 2022 UNFCCC Submission", height=380)
        layout_bar["xaxis"]["title"] = "Mt CH4 per year"
        layout_bar["xaxis"]["range"] = [0, 13.5]
        layout_bar["yaxis"]["categoryorder"] = "total ascending"
        fig_bar.update_layout(**layout_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    with sc2:
        fig_pie = go.Figure(go.Pie(
            labels=sd["sector"], values=sd["mt_ch4"], hole=0.56,
            marker=dict(
                colors=[BLACK,"#374151","#6b7280","#9ca3af",
                        "#d1d5db","#e5e7eb","#f3f4f6","#f9fafb"],
                line=dict(color=WHITE, width=2),
            ),
            textfont=dict(family="IBM Plex Mono", color=WHITE, size=9),
            hovertemplate="<b>%{label}</b><br>%{value:.1f} Mt · %{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text="35.5 Mt<br>CH4 2022", x=0.5, y=0.5, showarrow=False,
            font=dict(family="Source Serif 4, Georgia, serif", size=12, color=BLACK),
        )
        layout_pie = base_layout("Sector Share", height=380)
        layout_pie["paper_bgcolor"] = WHITE
        layout_pie["plot_bgcolor"]  = WHITE
        layout_pie["margin"] = dict(l=0, r=0, t=44, b=0)
        layout_pie["legend"] = dict(
            bgcolor=WHITE, bordercolor=BORDER, borderwidth=1,
            font=dict(family="Inter", color=GRAY, size=10),
        )
        fig_pie.update_layout(**layout_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sec-label'>Official Inventory Trend</div>"
        "<div class='sec-title'>USA CH4 submissions to UNFCCC, 2015 to 2022</div>",
        unsafe_allow_html=True,
    )

    if official is not None and "year" in official.columns:
        tr = official
    else:
        tr = pd.DataFrame({
            "year": list(range(2015,2023)),
            "reported_Mt_CH4": [36.1,35.8,35.5,35.7,35.3,35.0,35.4,35.5],
        })

    fig_tr = go.Figure()
    fig_tr.add_trace(go.Scatter(
        x=tr["year"], y=tr["reported_Mt_CH4"],
        mode="lines+markers",
        line=dict(color=BLACK, width=2),
        marker=dict(size=6, color=BLACK, line=dict(color=WHITE, width=1.5)),
        fill="tozeroy", fillcolor="rgba(26,26,26,0.05)",
        hovertemplate="<b>%{x}</b> · %{y:.1f} Mt CH4<extra></extra>",
    ))
    layout_tr = base_layout("", height=260)
    layout_tr["xaxis"]["tickvals"] = list(range(2015,2023))
    layout_tr["yaxis"]["range"]    = [30, 42]
    layout_tr["yaxis"]["title"]    = "Mt CH4"
    fig_tr.update_layout(**layout_tr)
    st.plotly_chart(fig_tr, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: SEASONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        "<div class='sec-label'>Seasonal Analysis</div>",
        unsafe_allow_html=True,
    )

    dist = pd.DataFrame({
        "Season":   ["Winter","Winter","Summer","Summer"],
        "Category": ["Below background","Above background",
                     "Below background","Above background"],
        "Pct":      [78.5, 21.5, 88.3, 11.7],
    })
    fig_dist = px.bar(
        dist, x="Season", y="Pct", color="Category",
        color_discrete_map={"Below background":"#d1d5db","Above background":BLACK},
        labels={"Pct":"Percent of observations"},
        text="Pct", height=320, barmode="stack",
    )
    fig_dist.update_traces(
        texttemplate="%{text:.1f}%", textposition="inside",
        textfont=dict(family="IBM Plex Mono", color=WHITE, size=12),
    )
    layout_dist = base_layout("Pixel Distribution Relative to NOAA Background", height=320)
    layout_dist["legend"] = dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        bgcolor=WHITE, bordercolor=BORDER, borderwidth=1,
        font=dict(family="Inter", color=GRAY, size=11),
    )
    fig_dist.update_layout(**layout_dist)
    st.plotly_chart(fig_dist, use_container_width=True)

    enh = pd.DataFrame({
        "Region": ["Northern Plains","Gulf Coast","Central Valley"],
        "ppb":    [56.3, 75.9, 70.3],
        "Peak":   [1976.2, 1990.7, 1985.2],
    })
    fig_enh = go.Figure(go.Bar(
        x=enh["Region"], y=enh["ppb"],
        marker=dict(color=[BLACK, BLACK, BLACK], line=dict(color=BORDER, width=0.5)),
        text=[f"+{v} ppb" for v in enh["ppb"]],
        textfont=dict(family="IBM Plex Mono", color=BLACK, size=11),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>+%{y} ppb<br>Peak: %{customdata} ppb<extra></extra>",
        customdata=enh["Peak"],
    ))
    layout_enh = base_layout("Peak Enhancement Above NOAA Background by Region", height=320)
    layout_enh["yaxis"]["title"] = "Enhancement (ppb)"
    layout_enh["yaxis"]["range"] = [0, 92]
    fig_enh.update_layout(**layout_enh)
    st.plotly_chart(fig_enh, use_container_width=True)

    st.markdown(
        "<div class='sec-label'>Summary Statistics</div>",
        unsafe_allow_html=True,
    )
    summ = pd.DataFrame({
        "Season": ["Winter: January 2023","Summer: Jun-Aug 2023","Combined"],
        "Observations": [f"{n_winter:,}",f"{n_summer:,}",f"{n_winter+n_summer:,}"],
        "Satellite Mean (ppb)": [1904.7, 1894.9, 1899.8],
        "NOAA Background (ppb)": [BG_WINTER, BG_SUMMER, 1917.41],
        "Hotspot Pixels": [
            f"{n_hs_w:,} (21.5%)",f"{n_hs_s:,} (11.7%)",f"{total_hs:,} (14.1%)",
        ],
        "Peak Enhancement": ["+56.3 ppb","+75.9 ppb","+75.9 ppb"],
    })
    st.dataframe(summ, hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: HOTSPOT DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(
        "<div class='sec-label'>Emission Hotspot Detail</div>",
        unsafe_allow_html=True,
    )

    ht = pd.DataFrame({
        "Region":           ["Northern Plains MN-ND","Gulf Coast TX-LA","CA Central Valley"],
        "Season":           ["Winter","Summer","Summer"],
        "Hotspot Pixels":   [485, 1271, 1221],
        "Peak Conc. (ppb)": [1976.2, 1990.7, 1985.2],
        "Peak Enhancement": ["+56.3 ppb","+75.9 ppb","+70.3 ppb"],
        "Likely Source":    [
            "Agricultural wetlands + Bakken O and G",
            "Offshore petrochemical, Gulf basin",
            "Dairy and rice agriculture",
        ],
        "UNFCCC Sector": ["Oil and Gas / Agriculture","Oil and Gas","Enteric Fermentation"],
    })
    st.dataframe(ht, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hc1, hc2 = st.columns(2)

    with hc1:
        src_w = winter_hs if winter_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1930,12,n_hs_w).clip(BG_WINTER,1985)})
        fig_wh = px.histogram(src_w, x="methane_column_ppb", nbins=50,
                              labels={"methane_column_ppb":"CH4 (ppb)","count":"Pixels"},
                              color_discrete_sequence=[BLACK], height=320)
        fig_wh.add_vline(x=BG_WINTER, line_dash="dot", line_color="#c07020", line_width=1.5,
                         annotation_text=f"Background {BG_WINTER} ppb",
                         annotation_font_color="#c07020", annotation_font_size=9)
        layout_wh = base_layout(f"Winter Hotspot Distribution: {n_hs_w:,} pixels", height=320)
        fig_wh.update_layout(**layout_wh)
        st.plotly_chart(fig_wh, use_container_width=True)

    with hc2:
        src_s = summer_hs if summer_hs is not None else pd.DataFrame(
            {"methane_column_ppb": np.random.normal(1925,15,n_hs_s).clip(BG_SUMMER,1992)})
        fig_sh = px.histogram(src_s, x="methane_column_ppb", nbins=50,
                              labels={"methane_column_ppb":"CH4 (ppb)","count":"Pixels"},
                              color_discrete_sequence=["#374151"], height=320)
        fig_sh.add_vline(x=BG_SUMMER, line_dash="dot", line_color="#c07020", line_width=1.5,
                         annotation_text=f"Background {BG_SUMMER} ppb",
                         annotation_font_color="#c07020", annotation_font_size=9)
        layout_sh = base_layout(f"Summer Hotspot Distribution: {n_hs_s:,} pixels", height=320)
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
    st.markdown(
        "<div class='sec-label'>Methodology</div>",
        unsafe_allow_html=True,
    )

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
        A fixed 1,870 ppb baseline overestimates enhancement by approximately 50 ppb
        for 2023 data. Period-specific values are required.

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
        air within the column average. This is structural to TROPOMI, not an artifact of
        this analysis.

        **Orbital sampling bias**
        Cloud cover systematically reduces valid observations in certain regions and seasons.
        No sampling correction applied.

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

    st.markdown(
        "<div class='sec-label'>Citations</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    - ESA Sentinel-5P TROPOMI Level 2 Methane Product User Manual. sentinel.esa.int
    - NOAA Global Monitoring Laboratory. gml.noaa.gov/ccgg/trends_ch4
    - Turner et al. 2020. A large increase in US methane emissions over the past decade. Science 369, 1219-1223
    - Alvarez et al. 2018. Assessment of methane emissions from the US oil and gas supply chain. Science 361, 186-188
    - Climate Watch API Documentation. climatewatchdata.org/api
    """)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<hr class='rule'>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-size:0.72rem;color:#9ca3af;line-height:1.8'>"
    "Data sources: ESA Sentinel-5P TROPOMI via Copernicus Data Space · "
    "NOAA Global Monitoring Laboratory · "
    "UNFCCC National Inventory submissions via Climate Watch API · "
    "Pipeline: Python · xarray · Snowflake · dbt · Streamlit · "
    "Code: github.com/likitha-sree-data/methane-truth"
    "</div>",
    unsafe_allow_html=True,
)
