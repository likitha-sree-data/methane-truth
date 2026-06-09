import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="The Methane Truth | Satellite vs Official Reports",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0a0e1a;
        color: #e8eaf0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1529 50%, #0a1628 100%);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1529 0%, #0a1628 100%);
        border-right: 1px solid #1e3a5f;
    }
    
    section[data-testid="stSidebar"] * {
        color: #c8d6e5 !important;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0d2137 0%, #0a1628 50%, #051020 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d4ff, #0099ff, #0066cc);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #7fa8cc;
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        color: #00d4ff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0d1f35 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #0099ff;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #7fa8cc;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #00d4ff;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    .finding-card {
        background: linear-gradient(135deg, #0d1f35 0%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: border-color 0.2s ease;
    }
    
    .finding-card:hover {
        border-color: #0099ff;
    }
    
    .finding-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .finding-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .finding-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 0.25rem;
    }
    
    .finding-desc {
        font-size: 0.85rem;
        color: #7fa8cc;
        line-height: 1.5;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ffffff;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1e3a5f;
    }
    
    .info-box {
        background: rgba(0, 153, 255, 0.08);
        border: 1px solid rgba(0, 153, 255, 0.25);
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        color: #c8d6e5;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .tag {
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.2);
        color: #00d4ff;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-right: 0.4rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1f35;
        border-radius: 10px;
        padding: 0.25rem;
        gap: 0.25rem;
        border: 1px solid #1e3a5f;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #7fa8cc;
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0a4a7a, #0066cc) !important;
        color: #ffffff !important;
    }
    
    .stRadio > div {
        background: #0d1f35;
        border-radius: 10px;
        padding: 0.75rem;
        border: 1px solid #1e3a5f;
    }
    
    .stRadio label {
        color: #c8d6e5 !important;
    }
    
    div[data-testid="stDataFrame"] {
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .footer-container {
        background: #0d1f35;
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
        color: #7fa8cc;
        font-size: 0.85rem;
    }
    
    .footer-container a {
        color: #00d4ff;
        text-decoration: none;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, li, span {
        color: #c8d6e5;
    }
    
    .stMarkdown p {
        color: #c8d6e5;
    }
    
    hr {
        border-color: #1e3a5f;
    }
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,31,53,0.5)',
        font=dict(family='Inter', color='#c8d6e5'),
        title=dict(font=dict(color='#ffffff', size=14)),
        xaxis=dict(
            gridcolor='#1e3a5f',
            linecolor='#1e3a5f',
            tickcolor='#7fa8cc',
            tickfont=dict(color='#7fa8cc')
        ),
        yaxis=dict(
            gridcolor='#1e3a5f',
            linecolor='#1e3a5f',
            tickcolor='#7fa8cc',
            tickfont=dict(color='#7fa8cc')
        ),
        legend=dict(
            bgcolor='rgba(13,31,53,0.8)',
            bordercolor='#1e3a5f',
            borderwidth=1,
            font=dict(color='#c8d6e5')
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color='#c8d6e5'),
            title=dict(font=dict(color='#c8d6e5'))
        )
    )
)

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem 0;">
        <div style="font-size:1.4rem; font-weight:700; color:#ffffff; 
        letter-spacing:-0.5px;">🛰️ Methane Truth</div>
        <div style="font-size:0.75rem; color:#7fa8cc; margin-top:0.25rem;
        text-transform:uppercase; letter-spacing:1px;">
        Open Source Climate Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#0d1f35; border:1px solid #1e3a5f; 
    border-radius:10px; padding:1rem; margin-bottom:1rem;">
        <div style="font-size:0.7rem; text-transform:uppercase; 
        letter-spacing:1px; color:#00d4ff; font-weight:600; 
        margin-bottom:0.75rem;">About This Project</div>
        <div style="font-size:0.85rem; color:#c8d6e5; line-height:1.6;">
        This platform analyzes <strong style="color:#ffffff;">304,611 real 
        ESA Sentinel 5P TROPOMI</strong> satellite methane observations over 
        the continental USA and compares them against official UNFCCC 
        government inventory submissions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#0d1f35; border:1px solid #1e3a5f;
    border-radius:10px; padding:1rem; margin-bottom:1rem;">
        <div style="font-size:0.7rem; text-transform:uppercase;
        letter-spacing:1px; color:#00d4ff; font-weight:600;
        margin-bottom:0.75rem;">Study Period</div>
        <div style="font-size:0.85rem; color:#c8d6e5;">
        🌨️ <strong style="color:#ffffff;">Winter</strong> — January 2023<br>
        ☀️ <strong style="color:#ffffff;">Summer</strong> — June to August 2023
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#0d1f35; border:1px solid #1e3a5f;
    border-radius:10px; padding:1rem; margin-bottom:1rem;">
        <div style="font-size:0.7rem; text-transform:uppercase;
        letter-spacing:1px; color:#00d4ff; font-weight:600;
        margin-bottom:0.75rem;">Data Sources</div>
        <div style="font-size:0.82rem; color:#c8d6e5; line-height:1.8;">
        🛰️ ESA Copernicus Data Space<br>
        🌍 NOAA Global Monitoring Lab<br>
        📊 UNFCCC via Climate Watch API
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#0d1f35; border:1px solid #1e3a5f;
    border-radius:10px; padding:1rem; margin-bottom:1rem;">
        <div style="font-size:0.7rem; text-transform:uppercase;
        letter-spacing:1px; color:#00d4ff; font-weight:600;
        margin-bottom:0.75rem;">Methodology</div>
        <div style="font-size:0.82rem; color:#c8d6e5; line-height:1.7;">
        Quality filter: <strong style="color:#ffffff;">qa_value > 0.5</strong><br>
        Background Jan 2023: <strong style="color:#ffffff;">1919.93 ppb</strong><br>
        Background Summer 2023: <strong style="color:#ffffff;">1914.89 ppb</strong><br>
        Source: NOAA GML verified monthly means
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#0d1f35; border:1px solid #1e3a5f;
    border-radius:10px; padding:1rem; margin-bottom:1rem;">
        <div style="font-size:0.7rem; text-transform:uppercase;
        letter-spacing:1px; color:#00d4ff; font-weight:600;
        margin-bottom:0.75rem;">Tech Stack</div>
        <div style="font-size:0.82rem; color:#c8d6e5; line-height:1.8;">
        Python · Snowflake · dbt<br>
        Apache Airflow · Streamlit · Plotly<br>
        Google Colab · ESA Copernicus API
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#0d1f35; border:1px solid #1e3a5f;
    border-radius:10px; padding:1rem;">
        <div style="font-size:0.7rem; text-transform:uppercase;
        letter-spacing:1px; color:#00d4ff; font-weight:600;
        margin-bottom:0.75rem;">Author</div>
        <div style="font-size:0.85rem; color:#ffffff; font-weight:600;">
        Likitha Yarabarla</div>
        <div style="font-size:0.8rem; color:#7fa8cc; margin-bottom:0.75rem;">
        Climate Data Engineer</div>
        <div style="font-size:0.82rem;">
        <a href="https://linkedin.com/in/likitha-sree" 
        style="color:#00d4ff; text-decoration:none;">
        🔗 LinkedIn</a> &nbsp;·&nbsp;
        <a href="https://github.com/likitha-sree-data/methane-truth"
        style="color:#00d4ff; text-decoration:none;">
        💻 GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🛰️ Open Source Climate Intelligence</div>
    <h1 class="hero-title">The Methane Truth</h1>
    <p class="hero-subtitle">
    304,611 ESA Sentinel 5P TROPOMI Observations · Continental USA · 
    January and June–August 2023 · Compared Against Official UNFCCC Inventory Data
    </p>
    <div style="margin-top:1rem;">
    <span class="tag">ESA Sentinel 5P</span>
    <span class="tag">NOAA GML</span>
    <span class="tag">UNFCCC</span>
    <span class="tag">Open Source</span>
    <span class="tag">Zero Proprietary Data</span>
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
    st.error("Data files not found. Please check the repository.")
    st.stop()

st.markdown('<div class="section-header">At a Glance</div>', 
            unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

metrics = [
    ("304,611", "Total Observations", "Quality filtered satellite pixels"),
    (f"{len(winter_hotspots):,}", "Winter Hotspots", "21.5% of winter pixels above background"),
    (f"{len(summer_hotspots):,}", "Summer Hotspots", "11.7% of summer pixels above background"),
    ("75.9 ppb", "Peak Enhancement", "Gulf Coast summer maximum"),
    ("35.5 Mt CH4", "Official Reported", "UNFCCC 2022 submission"),
]

for col, (value, label, delta) in zip(
    [col1, col2, col3, col4, col5], metrics
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="finding-card">
        <div class="finding-icon">🏔️</div>
        <div class="finding-title">Northern Plains</div>
        <div class="finding-value">+56.3 ppb</div>
        <div class="finding-desc">
        Peak 1976.2 ppb · Winter 2023<br>
        Agricultural wetlands and oil gas operations along the 
        Minnesota-North Dakota border
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="finding-card">
        <div class="finding-icon">🌊</div>
        <div class="finding-title">Gulf Coast</div>
        <div class="finding-value">+75.9 ppb</div>
        <div class="finding-desc">
        Peak 1990.7 ppb · Summer 2023<br>
        Highest single pixel in entire dataset. 
        Offshore oil gas and petrochemical corridor TX-LA.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="finding-card">
        <div class="finding-icon">🌾</div>
        <div class="finding-title">California Central Valley</div>
        <div class="finding-value">+70.3 ppb</div>
        <div class="finding-desc">
        Peak 1985.2 ppb · Summer 2023<br>
        Dairy farming and agricultural operations. 
        Largest agricultural methane source in western USA.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️  Satellite Maps",
    "📊  Gap Analysis",
    "🔥  Emission Hotspots",
    "📋  Methodology"
])

def style_plotly(fig):
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    return fig

with tab1:
    st.markdown('<div class="section-header">Satellite Methane Concentration Maps</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#7fa8cc; font-size:0.9rem; margin-bottom:1rem;">
    Each point represents a real ESA Sentinel 5P TROPOMI satellite pixel at 
    5.5 × 3.5 km resolution. Color encodes methane column concentration in 
    parts per billion (ppb). Red indicates higher concentrations above background.
    </p>
    """, unsafe_allow_html=True)
    
    season = st.radio(
        "Select dataset",
        [
            "🌨️  Winter — January 2023 (77,134 observations)",
            "☀️  Summer — June to August 2023 (227,477 observations)",
            "🎯  Hotspots Only — Pixels exceeding NOAA background"
        ],
        horizontal=True
    )
    
    if "Winter" in season:
        plot_df = winter_df.sample(min(20000, len(winter_df)), random_state=42)
        title = "Winter Methane Concentrations — USA · January 2023"
        cmin, cmax = 1870, 1980
        caption = "NOAA verified background: 1919.93 ppb · January 2023"
    elif "Summer" in season:
        plot_df = summer_df.sample(min(20000, len(summer_df)), random_state=42)
        title = "Summer Methane Concentrations — USA · June to August 2023"
        cmin, cmax = 1870, 1995
        caption = "NOAA verified background: 1914.89 ppb · Summer 2023 average"
    else:
        plot_df = pd.concat(
            [winter_hotspots, summer_hotspots], ignore_index=True
        )
        title = "Emission Hotspots — Pixels Exceeding NOAA Verified Background"
        cmin, cmax = 1915, 1995
        caption = "Only pixels above NOAA monthly mean background shown"
    
    st.caption(caption)
    
    fig_map = px.scatter_mapbox(
        plot_df,
        lat="latitude",
        lon="longitude",
        color="methane_column_ppb",
        color_continuous_scale="RdYlGn_r",
        range_color=[cmin, cmax],
        mapbox_style="carto-darkmatter",
        zoom=3,
        center={"lat": 38, "lon": -96},
        title=title,
        labels={"methane_column_ppb": "CH₄ (ppb)"},
        height=560,
        hover_data={
            "latitude": ":.3f",
            "longitude": ":.3f",
            "methane_column_ppb": ":.1f"
        }
    )
    
    fig_map.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title=dict(font=dict(color='#ffffff', size=13)),
        coloraxis_colorbar=dict(
            title=dict(text="CH₄ ppb", font=dict(color='#c8d6e5')),
            tickfont=dict(color='#c8d6e5'),
            thickness=12,
            len=0.6,
            bgcolor='rgba(13,31,53,0.8)',
            bordercolor='#1e3a5f',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.caption(
        "Source: ESA Sentinel 5P TROPOMI L2 CH₄ product · "
        "Copernicus Data Space · Quality filter: qa_value > 0.5"
    )

with tab2:
    st.markdown('<div class="section-header">Gap Analysis and Seasonal Statistics</div>',
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
                "Below Background": "#1e3a5f",
                "Above Background": "#0099ff"
            },
            title="Pixel Distribution Above vs Below NOAA Background",
            labels={"Percentage": "% of Observations"},
            text="Percentage",
            height=380,
            barmode="stack"
        )
        fig_dist.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="inside",
            textfont=dict(color="white", size=12)
        )
        fig_dist = style_plotly(fig_dist)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        fig_trend = px.line(
            official_data,
            x="year",
            y="reported_Mt_CH4",
            markers=True,
            title="USA Official UNFCCC Methane Inventory 2015–2022",
            labels={
                "reported_Mt_CH4": "Mt CH₄ per year",
                "year": "Year"
            },
            height=380
        )
        fig_trend.update_traces(
            line=dict(width=2.5, color="#0099ff"),
            marker=dict(size=8, color="#00d4ff",
                       line=dict(color="#0099ff", width=2))
        )
        fig_trend.update_layout(yaxis=dict(range=[30, 42]))
        fig_trend = style_plotly(fig_trend)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown('<div class="section-header">Seasonal Summary</div>',
                unsafe_allow_html=True)
    
    summary_df = pd.DataFrame({
        "Season": [
            "Winter · January 2023",
            "Summer · June–Aug 2023",
            "Annual Average"
        ],
        "Observations": [
            f"{len(winter_df):,}",
            f"{len(summer_df):,}",
            f"{len(winter_df)+len(summer_df):,}"
        ],
        "Satellite Mean (ppb)": [1904.7, 1894.9, 1899.8],
        "NOAA Background (ppb)": [1919.93, 1914.89, 1917.41],
        "Enhancement (ppb)": [-15.2, -19.97, -17.58],
        "Hotspot Pixels": [
            f"{len(winter_hotspots):,} (21.5%)",
            f"{len(summer_hotspots):,} (11.7%)",
            "43,086 (14.1%)"
        ]
    })
    
    st.dataframe(summary_df, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="info-box">
    <strong style="color:#00d4ff;">Key Insight:</strong> The satellite mean 
    concentration falls below the NOAA verified global background for both seasons. 
    This reveals a fundamental characteristic of national scale passive satellite 
    monitoring: the majority of pixels capture background air rather than emission 
    plumes, which disperse rapidly across the 5.5 km pixel footprint. Only 14.1% 
    of pixels show detectable enhancement above background. But those pixels 
    cluster with remarkable geographic precision over known emission sources.
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Emission Hotspot Analysis</div>',
                unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#7fa8cc; font-size:0.9rem; margin-bottom:1.5rem;">
    The 43,086 pixels exceeding the NOAA verified background do not distribute 
    randomly across the continental USA. They cluster with geographic precision 
    over three distinct emission source regions.
    </p>
    """, unsafe_allow_html=True)
    
    hotspot_regions = pd.DataFrame({
        "Region": [
            "Northern Plains MN-ND Border",
            "Gulf Coast TX-LA Offshore",
            "California Central Valley"
        ],
        "Season": ["Winter", "Summer", "Summer"],
        "Hotspot Pixels": [485, 1271, 1221],
        "Peak (ppb)": [1976.2, 1990.7, 1985.2],
        "Enhancement (ppb)": ["+56.3", "+75.9", "+70.3"],
        "Emission Source": [
            "Agricultural wetlands · Oil and gas",
            "Offshore petrochemical corridor",
            "Dairy farming · Agriculture"
        ]
    })
    
    st.dataframe(
        hotspot_regions,
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        fig_w = px.histogram(
            winter_hotspots,
            x="methane_column_ppb",
            nbins=40,
            title=f"Winter Hotspots · n={len(winter_hotspots):,} pixels",
            labels={"methane_column_ppb": "CH₄ Concentration (ppb)",
                   "count": "Pixel Count"},
            color_discrete_sequence=["#0099ff"],
            height=360
        )
        fig_w.add_vline(
            x=1919.93,
            line_dash="dash",
            line_color="#ff4444",
            line_width=2,
            annotation_text="NOAA background 1919.93 ppb",
            annotation_font_color="#ff4444",
            annotation_font_size=11
        )
        fig_w = style_plotly(fig_w)
        st.plotly_chart(fig_w, use_container_width=True)
    
    with col2:
        fig_s = px.histogram(
            summer_hotspots,
            x="methane_column_ppb",
            nbins=40,
            title=f"Summer Hotspots · n={len(summer_hotspots):,} pixels",
            labels={"methane_column_ppb": "CH₄ Concentration (ppb)",
                   "count": "Pixel Count"},
            color_discrete_sequence=["#ff6b00"],
            height=360
        )
        fig_s.add_vline(
            x=1914.89,
            line_dash="dash",
            line_color="#ff4444",
            line_width=2,
            annotation_text="NOAA background 1914.89 ppb",
            annotation_font_color="#ff4444",
            annotation_font_size=11
        )
        fig_s = style_plotly(fig_s)
        st.plotly_chart(fig_s, use_container_width=True)
    
    st.markdown("""
    <div class="info-box">
    <strong style="color:#00d4ff;">The Core Finding:</strong> 
    Satellite monitoring at the national scale is not primarily a tool for 
    verifying whether a country's total emission inventory is correct. 
    It is a tool for locating <em>where</em> emissions originate with 
    geographic precision that no ground based inventory system can match. 
    The real accountability question is whether official inventories correctly 
    attribute emissions to the right geographic sources at the right scale.
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">Methodology and Reproducibility</div>',
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Pipeline Architecture
        
        **Ingestion**  
        ESA Sentinel 5P TROPOMI L2 methane product downloaded via 
        Copernicus Data Space API. Parsed from netCDF4 format using 
        xarray. Quality filtered at qa_value > 0.5 per ESA documentation.
        
        **Storage**  
        304,611 processed observations loaded to Snowflake cloud data 
        warehouse in batches with deduplication on date, latitude, 
        and longitude.
        
        **Transformation**  
        dbt models for staging, intermediate, and mart layers with 
        full test coverage on every model.
        
        **Background Values**  
        NOAA Global Monitoring Laboratory monthly mean methane 
        concentrations used as period specific background. Critical 
        distinction: using the correct 2023 background of ~1920 ppb 
        rather than a historical value of 1870 ppb changes enhancement 
        calculations by approximately 50 ppb.
        
        **Official Inventory**  
        UNFCCC national submissions accessed via Climate Watch API, 
        filtered for CH₄ and USA.
        """)
    
    with col2:
        st.markdown("""
        #### Key Limitations
        
        **Temporal Coverage**  
        Four months covering winter and summer only. Spring and autumn 
        data would complete the annual picture and improve seasonal 
        averaging.
        
        **Spatial Resolution**  
        TROPOMI pixel footprint of 5.5 × 3.5 km means emission 
        plumes from individual facilities are diluted by surrounding 
        clean air in the column average.
        
        **Orbital Coverage**  
        Not all regions receive equal overpass frequency. Cloud cover 
        reduces valid observations in some areas.
        
        **Conversion Factor**  
        The Turner et al 2020 ppb-to-Mt conversion assumes uniform 
        atmospheric mixing and full national coverage. Neither 
        assumption fully holds for this dataset.
        
        #### How to Reproduce
        
        1. Free account at dataspace.copernicus.eu
        2. Free Snowflake trial at snowflake.com
        3. Open notebook in Google Colab
        4. Run cells sequentially
        
        Total runtime approximately 2 hours for full dataset.
        All data sources are free and publicly accessible.
        """)
    
    st.markdown('<div class="section-header">Citations</div>',
                unsafe_allow_html=True)
    
    st.markdown("""
    - ESA Sentinel 5P TROPOMI L2 Product User Manual · sentinel.esa.int
    - NOAA Global Monitoring Laboratory · gml.noaa.gov/ccgg/trends_ch4
    - Turner et al 2020 · Science 369 · 1219-1223
    - Climate Watch API Documentation · climatewatchdata.org/api
    - Alvarez et al 2018 · Science 361 · 186-188
    """)

st.markdown("""
<div class="footer-container">
    <div style="font-size:1rem; font-weight:600; color:#ffffff; 
    margin-bottom:0.5rem;">
    Built with real satellite data · Zero proprietary sources · 
    Full reproducibility
    </div>
    <div style="margin-top:0.5rem;">
    ESA Sentinel 5P TROPOMI · NOAA GML · UNFCCC via Climate Watch &nbsp;·&nbsp;
    <a href="https://github.com/likitha-sree-data/methane-truth">💻 GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/likitha-sree">🔗 LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="https://medium.com/the-quantastic-journal/the-blue-carbon-market-promised-to-save-the-worlds-coastlines-the-data-tells-a-different-story-6b4f4ec774bd">
    📖 Blue Carbon Analysis</a>
    </div>
</div>
""", unsafe_allow_html=True)
