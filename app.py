import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="The Methane Truth | Satellite vs Official Reports",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8f9fc;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e9f0;
    }
    
    .hero {
        background: linear-gradient(135deg, #0f2942 0%, #1a3f6f 100%);
        border-radius: 12px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #7eb8f7;
        margin-bottom: 0.75rem;
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        color: #a8c8f0;
        margin: 0;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .hero-tags {
        margin-top: 1.25rem;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .tag {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        color: #d0e8ff;
        padding: 0.2rem 0.75rem;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        border-top: 3px solid #1a3f6f;
    }
    
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0f2942;
        letter-spacing: -1px;
        margin: 0;
    }
    
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #6b7a99;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0.2rem 0 0 0;
    }
    
    .kpi-note {
        font-size: 0.78rem;
        color: #9aa5bc;
        margin: 0.3rem 0 0 0;
    }
    
    .finding-card {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        border-left: 4px solid #1a3f6f;
    }
    
    .finding-region {
        font-size: 0.7rem;
        font-weight: 600;
        color: #6b7a99;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
    }
    
    .finding-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a3f6f;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .finding-detail {
        font-size: 0.82rem;
        color: #6b7a99;
        margin-top: 0.4rem;
        line-height: 1.5;
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f2942;
        margin: 1.75rem 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid #e5e9f0;
        letter-spacing: -0.2px;
    }
    
    .insight-box {
        background: #f0f5ff;
        border: 1px solid #c5d5f0;
        border-left: 4px solid #1a3f6f;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #2d3f5e;
        line-height: 1.7;
    }
    
    .sidebar-section {
        background: #f8f9fc;
        border: 1px solid #e5e9f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .sidebar-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: #1a3f6f;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.6rem;
    }
    
    .sidebar-text {
        font-size: 0.82rem;
        color: #4a5568;
        line-height: 1.7;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 8px;
        padding: 0.2rem;
        gap: 0.2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #6b7a99;
        border-radius: 6px;
        padding: 0.5rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0f2942 !important;
        color: #ffffff !important;
    }
    
    .footer {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 10px;
        padding: 1.25rem 2rem;
        text-align: center;
        margin-top: 2rem;
        font-size: 0.82rem;
        color: #6b7a99;
    }
    
    .footer a {
        color: #1a3f6f;
        text-decoration: none;
        font-weight: 500;
    }
    
    h1, h2, h3, h4 {
        color: #0f2942 !important;
    }
    
    p {
        color: #4a5568;
    }
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#f8f9fc',
    font=dict(family='Inter', color='#4a5568', size=12),
    title=dict(font=dict(color='#0f2942', size=13, family='Inter'), x=0),
    xaxis=dict(
        gridcolor='#e5e9f0',
        linecolor='#e5e9f0',
        tickfont=dict(color='#6b7a99', size=11)
    ),
    yaxis=dict(
        gridcolor='#e5e9f0',
        linecolor='#e5e9f0',
        tickfont=dict(color='#6b7a99', size=11)
    ),
    legend=dict(
        bgcolor='#ffffff',
        bordercolor='#e5e9f0',
        borderwidth=1,
        font=dict(color='#4a5568', size=11)
    ),
    margin=dict(l=10, r=10, t=40, b=10)
)

with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.5rem 0; border-bottom:1px solid #e5e9f0; 
    margin-bottom:1rem;">
        <div style="font-size:1rem; font-weight:700; color:#0f2942; 
        letter-spacing:-0.3px;">The Methane Truth</div>
        <div style="font-size:0.72rem; color:#6b7a99; margin-top:0.2rem;
        text-transform:uppercase; letter-spacing:1px; font-weight:500;">
        Open Source Climate Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">About</div>
        <div class="sidebar-text">
        This platform analyzes <strong>304,611 ESA Sentinel 5P TROPOMI</strong> 
        satellite methane observations over the continental USA and compares 
        them against official UNFCCC inventory submissions using NOAA verified 
        atmospheric background values.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">Study Period</div>
        <div class="sidebar-text">
        Winter — January 2023<br>
        Summer — June to August 2023
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">Data Sources</div>
        <div class="sidebar-text">
        ESA Copernicus Data Space<br>
        NOAA Global Monitoring Laboratory<br>
        UNFCCC via Climate Watch API
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">Quality Standards</div>
        <div class="sidebar-text">
        Quality filter: qa_value greater than 0.5<br>
        Per ESA TROPOMI documentation<br><br>
        Background Jan 2023: <strong>1919.93 ppb</strong><br>
        Background Summer 2023: <strong>1914.89 ppb</strong><br>
        Source: NOAA GML monthly means
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">Pipeline</div>
        <div class="sidebar-text">
        Python · Snowflake · dbt<br>
        Apache Airflow · Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">Author</div>
        <div class="sidebar-text">
        <strong>Likitha Yarabarla</strong><br>
        Climate Data Engineer<br>
        Worldview Development USA<br><br>
        <a href="https://linkedin.com/in/likitha-sree" 
        style="color:#1a3f6f; text-decoration:none; font-weight:500;">
        LinkedIn</a> &nbsp;·&nbsp;
        <a href="https://github.com/likitha-sree-data/methane-truth"
        style="color:#1a3f6f; text-decoration:none; font-weight:500;">
        GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-label">Open Source Climate Intelligence</div>
    <h1 class="hero-title">The Methane Truth</h1>
    <p class="hero-subtitle">
    304,611 ESA Sentinel 5P TROPOMI observations over the continental USA.<br>
    January and June through August 2023. 
    Compared against official UNFCCC inventory submissions 
    using NOAA verified atmospheric background values.
    </p>
    <div class="hero-tags">
        <span class="tag">ESA Sentinel 5P</span>
        <span class="tag">NOAA GML</span>
        <span class="tag">UNFCCC</span>
        <span class="tag">Open Source</span>
        <span class="tag">Zero Proprietary Data</span>
        <span class="tag">Fully Reproducible</span>
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        winter = pd.read_csv("satellite_usa_winter.csv")
        summer = pd.read_csv("satellite_usa_summer.csv")
        hotspots_w = pd.read_csv("winter_hotspots.csv")
        hotspots_s = pd.read_csv("summer_hotspots.csv")
        official = pd.read_csv("unfccc_usa_totals.csv")
        return winter, summer, hotspots_w, hotspots_s, official
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None

winter_df, summer_df, winter_hotspots, summer_hotspots, official_data = load_data()

if winter_df is None:
    st.error("Data files not found. Please check the repository structure.")
    st.stop()

st.markdown('<div class="section-title">Key Performance Indicators</div>',
            unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

kpis = [
    ("304,611", "Total Observations", 
     "Quality filtered satellite pixels"),
    (f"{len(winter_hotspots):,}", "Winter Hotspot Pixels",
     "21.5% of winter observations"),
    (f"{len(summer_hotspots):,}", "Summer Hotspot Pixels",
     "11.7% of summer observations"),
    ("75.9 ppb", "Peak Enhancement",
     "Gulf Coast summer maximum"),
    ("35.5 Mt CH4", "Official Reported",
     "UNFCCC 2022 submission"),
]

for col, (value, label, note) in zip(
    [col1, col2, col3, col4, col5], kpis
):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <p class="kpi-value">{value}</p>
            <p class="kpi-label">{label}</p>
            <p class="kpi-note">{note}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Primary Findings</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

findings = [
    (
        "Northern Plains",
        "+56.3 ppb",
        "Peak 1976.2 ppb · Winter 2023. "
        "Agricultural wetlands and oil gas operations along "
        "the Minnesota-North Dakota border. "
        "485 hotspot pixels identified."
    ),
    (
        "Gulf Coast",
        "+75.9 ppb",
        "Peak 1990.7 ppb · Summer 2023. "
        "Highest single pixel in the entire dataset. "
        "Offshore oil gas and petrochemical corridor "
        "between Houston and New Orleans. "
        "1,271 hotspot pixels identified."
    ),
    (
        "California Central Valley",
        "+70.3 ppb",
        "Peak 1985.2 ppb · Summer 2023. "
        "Dairy farming and agricultural methane emissions. "
        "Largest agricultural methane source region "
        "in the western United States. "
        "1,221 hotspot pixels identified."
    )
]

for col, (region, value, detail) in zip([col1, col2, col3], findings):
    with col:
        st.markdown(f"""
        <div class="finding-card">
            <div class="finding-region">{region}</div>
            <p class="finding-value">{value}</p>
            <p class="finding-detail">{detail}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Satellite Maps",
    "Seasonal Analysis",
    "Hotspot Detail",
    "Methodology"
])

with tab1:
    st.markdown('<div class="section-title">Satellite Methane Concentration Maps</div>',
                unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#6b7a99; font-size:0.88rem; margin-bottom:1.25rem;">
    Each point represents an ESA Sentinel 5P TROPOMI satellite pixel at 
    5.5 x 3.5 km resolution. Color encodes methane column concentration 
    in parts per billion. Warmer colors indicate higher concentrations 
    above the NOAA verified global background.
    </p>
    """, unsafe_allow_html=True)
    
    dataset = st.radio(
        "Select dataset",
        [
            "Winter — January 2023 (77,134 observations)",
            "Summer — June to August 2023 (227,477 observations)",
            "Hotspots — Pixels exceeding NOAA background only"
        ],
        horizontal=True
    )
    
    if "Winter" in dataset:
        plot_df = winter_df.sample(min(20000, len(winter_df)), random_state=42)
        title = "Winter Methane Concentrations — USA, January 2023"
        cmin, cmax = 1870, 1980
        caption = "NOAA verified background: 1919.93 ppb — January 2023"
    elif "Summer" in dataset:
        plot_df = summer_df.sample(min(20000, len(summer_df)), random_state=42)
        title = "Summer Methane Concentrations — USA, June to August 2023"
        cmin, cmax = 1870, 1995
        caption = "NOAA verified background: 1914.89 ppb — Summer 2023 average"
    else:
        plot_df = pd.concat(
            [winter_hotspots, summer_hotspots], ignore_index=True
        )
        title = "Emission Hotspots — Pixels Exceeding NOAA Verified Background"
        cmin, cmax = 1915, 1995
        caption = "Combined winter and summer pixels above NOAA monthly mean background"
    
    st.caption(caption)
    
    fig_map = px.scatter_mapbox(
        plot_df,
        lat="latitude",
        lon="longitude",
        color="methane_column_ppb",
        color_continuous_scale="RdYlGn_r",
        range_color=[cmin, cmax],
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 38, "lon": -96},
        title=title,
        labels={"methane_column_ppb": "CH4 (ppb)"},
        height=560,
        hover_data={
            "latitude": ":.3f",
            "longitude": ":.3f",
            "methane_column_ppb": ":.1f"
        }
    )
    
    fig_map.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title=dict(
            font=dict(color='#0f2942', size=13, family='Inter'), x=0
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text="CH4 ppb",
                font=dict(color='#4a5568', size=11)
            ),
            tickfont=dict(color='#6b7a99', size=10),
            thickness=12,
            len=0.6
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(
        "Source: ESA Sentinel 5P TROPOMI L2 CH4 product via Copernicus "
        "Data Space. Quality filter qa_value greater than 0.5."
    )

with tab2:
    st.markdown('<div class="section-title">Seasonal Analysis</div>',
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        dist_data = pd.DataFrame({
            "Season": [
                "Winter Jan", "Winter Jan",
                "Summer Jun-Aug", "Summer Jun-Aug"
            ],
            "Category": [
                "Below Background", "Above Background",
                "Below Background", "Above Background"
            ],
            "Percentage": [78.5, 21.5, 88.3, 11.7],
        })
        
        fig_dist = px.bar(
            dist_data,
            x="Season",
            y="Percentage",
            color="Category",
            color_discrete_map={
                "Below Background": "#cbd5e8",
                "Above Background": "#1a3f6f"
            },
            title="Pixel Distribution Relative to NOAA Background",
            labels={"Percentage": "Percentage of Observations (%)"},
            text="Percentage",
            height=380,
            barmode="stack"
        )
        fig_dist.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="inside",
            textfont=dict(color="white", size=12, family="Inter")
        )
        fig_dist.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        fig_trend = px.line(
            official_data,
            x="year",
            y="reported_Mt_CH4",
            markers=True,
            title="USA Official UNFCCC Methane Inventory 2015 to 2022",
            labels={
                "reported_Mt_CH4": "Mt CH4 per year",
                "year": "Year"
            },
            height=380
        )
        fig_trend.update_traces(
            line=dict(width=2.5, color="#1a3f6f"),
            marker=dict(
                size=8,
                color="#1a3f6f",
                line=dict(color="#ffffff", width=1.5)
            )
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#f8f9fc',
            font=dict(family='Inter', color='#4a5568', size=12),
            title=dict(
                font=dict(color='#0f2942', size=13, family='Inter'), x=0
            ),
            xaxis=dict(
                gridcolor='#e5e9f0',
                linecolor='#e5e9f0',
                tickfont=dict(color='#6b7a99', size=11)
            ),
            yaxis=dict(
                range=[30, 42],
                gridcolor='#e5e9f0',
                linecolor='#e5e9f0',
                tickfont=dict(color='#6b7a99', size=11)
            ),
            legend=dict(
                bgcolor='#ffffff',
                bordercolor='#e5e9f0',
                borderwidth=1,
                font=dict(color='#4a5568', size=11)
            ),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown('<div class="section-title">Seasonal Summary Statistics</div>',
                unsafe_allow_html=True)
    
    summary_df = pd.DataFrame({
        "Season": [
            "Winter — January 2023",
            "Summer — June to August 2023",
            "Annual Average"
        ],
        "Observations": [
            f"{len(winter_df):,}",
            f"{len(summer_df):,}",
            f"{len(winter_df)+len(summer_df):,}"
        ],
        "Satellite Mean (ppb)": [1904.7, 1894.9, 1899.8],
        "NOAA Background (ppb)": [1919.93, 1914.89, 1917.41],
        "Enhancement (ppb)": [-15.2, -20.0, -17.6],
        "Hotspot Pixels": [
            f"{len(winter_hotspots):,} (21.5%)",
            f"{len(summer_hotspots):,} (11.7%)",
            "43,086 (14.1%)"
        ]
    })
    
    st.dataframe(summary_df, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>Interpretation:</strong> The satellite mean concentration falls 
    below the NOAA verified global background for both seasons. This reveals 
    a fundamental characteristic of national scale passive satellite monitoring. 
    The majority of pixels capture background air rather than emission plumes, 
    which disperse rapidly across the 5.5 km pixel footprint. Only 14.1 percent 
    of pixels show detectable enhancement above background. Those pixels, however, 
    cluster with remarkable geographic precision over known emission sources, 
    demonstrating that satellite data functions as a geographic localization 
    tool rather than a national inventory verification tool.
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Emission Hotspot Detail</div>',
                unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#6b7a99; font-size:0.88rem; margin-bottom:1.25rem;">
    The 43,086 pixels exceeding the NOAA verified background do not 
    distribute randomly. They concentrate with geographic precision 
    over three distinct source regions, consistent with known emission 
    inventories for those areas.
    </p>
    """, unsafe_allow_html=True)
    
    hotspot_table = pd.DataFrame({
        "Region": [
            "Northern Plains MN-ND",
            "Gulf Coast TX-LA",
            "California Central Valley"
        ],
        "Season": ["Winter", "Summer", "Summer"],
        "Hotspot Pixels": [485, 1271, 1221],
        "Peak Concentration (ppb)": [1976.2, 1990.7, 1985.2],
        "Peak Enhancement (ppb)": [56.3, 75.9, 70.3],
        "Mean Hotspot (ppb)": [1935.6, 1926.7, 1925.3],
        "Emission Source": [
            "Agricultural wetlands and oil gas",
            "Offshore petrochemical operations",
            "Dairy farming and agriculture"
        ]
    })
    
    st.dataframe(hotspot_table, hide_index=True, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        fig_w = px.histogram(
            winter_hotspots,
            x="methane_column_ppb",
            nbins=40,
            title=f"Winter Hotspot Distribution — {len(winter_hotspots):,} pixels",
            labels={
                "methane_column_ppb": "CH4 Concentration (ppb)",
                "count": "Pixel Count"
            },
            color_discrete_sequence=["#1a3f6f"],
            height=360
        )
        fig_w.add_vline(
            x=1919.93,
            line_dash="dash",
            line_color="#e53e3e",
            line_width=1.5,
            annotation_text="NOAA background 1919.93 ppb",
            annotation_font_color="#e53e3e",
            annotation_font_size=10
        )
        fig_w.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_w, use_container_width=True)
    
    with col2:
        fig_s = px.histogram(
            summer_hotspots,
            x="methane_column_ppb",
            nbins=40,
            title=f"Summer Hotspot Distribution — {len(summer_hotspots):,} pixels",
            labels={
                "methane_column_ppb": "CH4 Concentration (ppb)",
                "count": "Pixel Count"
            },
            color_discrete_sequence=["#744210"],
            height=360
        )
        fig_s.add_vline(
            x=1914.89,
            line_dash="dash",
            line_color="#e53e3e",
            line_width=1.5,
            annotation_text="NOAA background 1914.89 ppb",
            annotation_font_color="#e53e3e",
            annotation_font_size=10
        )
        fig_s.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_s, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>Core Finding:</strong> National scale satellite monitoring 
    is not primarily a tool for verifying whether a country's total 
    emission inventory is correct. It is a tool for locating where 
    emissions originate with geographic precision that no ground based 
    inventory system can replicate. The accountability question worth 
    asking is whether official inventories correctly attribute emissions 
    to the right geographic sources at the right magnitude. That is 
    where satellite data provides genuine independent value.
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">Methodology</div>',
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Pipeline Architecture
        
        **Satellite Ingestion**  
        ESA Sentinel 5P TROPOMI L2 methane product downloaded via 
        Copernicus Data Space API. Parsed from netCDF4 format using 
        xarray. The PRODUCT group contains methane_mixing_ratio_bias_corrected, 
        qa_value, latitude, and longitude arrays with shape 
        (time, scanline, ground_pixel).
        
        **Quality Filtering**  
        Observations retained at qa_value greater than 0.5 per ESA TROPOMI 
        Level 2 Product documentation. Physical plausibility filter 
        applied at 1600 to 2200 ppb. Spatial filter: continental USA 
        bounding box latitude 24 to 50, longitude 125 to 66 west.
        
        **Data Warehouse**  
        Processed observations loaded to Snowflake in batches of 10,000 
        records with deduplication on observation date, latitude, and 
        longitude.
        
        **Background Selection**  
        NOAA Global Monitoring Laboratory monthly mean methane used as 
        period specific background. January 2023: 1919.93 ppb. 
        Summer 2023 average: 1914.89 ppb. Using a historical fixed 
        background of 1870 ppb would overestimate enhancement by 
        approximately 50 ppb for 2023 data.
        
        **Official Inventory**  
        UNFCCC national submissions accessed via Climate Watch API, 
        filtered for CH4 gas, USA region, all sectors combined.
        """)
    
    with col2:
        st.markdown("""
        #### Limitations
        
        **Temporal Coverage**  
        Four months representing winter and summer only. Spring and 
        autumn data would complete the annual picture and reduce 
        seasonal sampling bias.
        
        **Pixel Footprint**  
        TROPOMI pixel footprint of 5.5 x 3.5 km means emission plumes 
        from individual facilities are diluted by surrounding clean air 
        in the column average measurement. This is why the national mean 
        falls below background despite real localized emission signals.
        
        **Orbital Sampling**  
        Not all regions receive equal overpass frequency. Cloud cover 
        systematically reduces valid observations in some areas and 
        seasons. This analysis does not correct for sampling bias.
        
        **Conversion Factor**  
        The Turner et al 2020 ppb to Mt conversion assumes uniform 
        atmospheric mixing and full national coverage. Neither assumption 
        holds for this dataset, which is why emission totals are not 
        the primary output of this analysis.
        
        #### Reproduce This Analysis
        
        1. Free account at dataspace.copernicus.eu
        2. Free Snowflake trial at snowflake.com  
        3. Open notebook at github.com/likitha-sree-data/methane-truth
        4. Run in Google Colab following cell sequence
        
        Total runtime approximately 2 hours. All data sources are 
        free and publicly accessible. Zero proprietary data used.
        """)
    
    st.markdown('<div class="section-title">Citations</div>',
                unsafe_allow_html=True)
    
    st.markdown("""
    - ESA Sentinel 5P TROPOMI Level 2 Methane Product User Manual
    - NOAA Global Monitoring Laboratory · gml.noaa.gov/ccgg/trends_ch4
    - Turner et al 2020 · A large increase in U.S. methane emissions over the past decade · Science 369
    - Alvarez et al 2018 · Assessment of methane emissions from the U.S. oil and gas supply chain · Science 361
    - Climate Watch API Documentation · climatewatchdata.org/api
    """)

st.markdown("""
<div class="footer">
    Built with real satellite data. Zero proprietary sources. Full reproducibility.<br>
    ESA Sentinel 5P TROPOMI · NOAA GML · UNFCCC via Climate Watch &nbsp;·&nbsp;
    <a href="https://github.com/likitha-sree-data/methane-truth">GitHub Repository</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/likitha-sree">LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="https://medium.com/the-quantastic-journal/the-blue-carbon-market-promised-to-save-the-worlds-coastlines-the-data-tells-a-different-story-6b4f4ec774bd">
    Blue Carbon Analysis</a>
</div>
""", unsafe_allow_html=True)
