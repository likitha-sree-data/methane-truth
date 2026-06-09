import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="The Methane Truth | Satellite vs Official Reports",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a4a6a;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .finding-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
    }
    .sidebar-info {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/ESA_logo_simple.svg/200px-ESA_logo_simple.svg.png",
        width=80
    )
    st.markdown("### About This Project")
    st.markdown("""
    This platform analyzes **304,611 real ESA Sentinel 5P TROPOMI** 
    satellite methane observations over the continental USA and 
    compares them against official UNFCCC government inventory submissions.
    
    **Study Period:**
    - Winter: January 2023
    - Summer: June - August 2023
    
    **Data Sources:**
    - ESA Copernicus Data Space
    - NOAA Global Monitoring Laboratory  
    - UNFCCC via Climate Watch API
    
    **Tech Stack:**
    Python · Snowflake · dbt · Airflow · Streamlit
    """)
    
    st.divider()
    
    st.markdown("### Methodology")
    st.markdown("""
    Quality filter: qa_value > 0.5 per ESA documentation
    
    Background: NOAA GML monthly means
    - January 2023: **1919.93 ppb**
    - Summer 2023 avg: **1914.89 ppb**
    
    Enhancement = Satellite mean minus NOAA background
    """)
    
    st.divider()
    
    st.markdown("### Author")
    st.markdown("""
    **Likitha Yarabarla**  
    Climate Data Engineer  
    
    [LinkedIn](https://linkedin.com/in/likitha-sree) |
    [GitHub](https://github.com/likitha-sree-data/methane-truth) |
    [Blue Carbon Analysis](https://medium.com/the-quantastic-journal/the-blue-carbon-market-promised-to-save-the-worlds-coastlines-the-data-tells-a-different-story-6b4f4ec774bd)
    """)

# Main content
st.markdown('<p class="main-header">🛰️ The Methane Truth</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">304,611 ESA Sentinel 5P Observations · '
    'USA · January and June–August 2023 · '
    'Compared Against Official UNFCCC Inventory Data</p>',
    unsafe_allow_html=True
)

# Load data
@st.cache_data
def load_data():
    try:
        winter = pd.read_csv("satellite_usa_winter.csv")
        summer = pd.read_csv("satellite_usa_summer.csv")
        hotspots_w = pd.read_csv("winter_hotspots.csv")
        hotspots_s = pd.read_csv("summer_hotspots.csv")
        official = pd.read_csv("unfccc_usa_totals.csv")
        corrected = pd.read_csv("corrected_gap_analysis.csv")
        return winter, summer, hotspots_w, hotspots_s, official, corrected
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None, None

winter_df, summer_df, winter_hotspots, summer_hotspots, official_data, corrected = load_data()

if winter_df is None:
    st.error("Data files not found. Please check the repository.")
    st.stop()

# Key metrics row
st.markdown("### At a Glance")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Satellite Observations",
        value="304,611",
        help="Quality filtered ESA Sentinel 5P TROPOMI pixels"
    )
with col2:
    st.metric(
        label="Winter Hotspot Pixels",
        value=f"{len(winter_hotspots):,}",
        delta=f"{len(winter_hotspots)/len(winter_df)*100:.1f}% of winter data",
        help="Observations exceeding NOAA January 2023 background of 1919.93 ppb"
    )
with col3:
    st.metric(
        label="Summer Hotspot Pixels",
        value=f"{len(summer_hotspots):,}",
        delta=f"{len(summer_hotspots)/len(summer_df)*100:.1f}% of summer data",
        help="Observations exceeding NOAA summer 2023 background of 1914.89 ppb"
    )
with col4:
    st.metric(
        label="Peak Enhancement",
        value="75.9 ppb",
        help="Maximum single pixel enhancement above NOAA background. Gulf Coast summer 2023."
    )
with col5:
    st.metric(
        label="Official UNFCCC Reported",
        value="35.5 Mt CH4",
        help="USA official methane inventory submission to UNFCCC for 2022"
    )

st.divider()

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Satellite Maps",
    "📊 Gap Analysis",
    "🔥 Emission Hotspots",
    "📋 Methodology"
])

# TAB 1: MAPS
with tab1:
    st.markdown("### Satellite Methane Concentration Maps")
    st.markdown(
        "Each dot represents a real ESA Sentinel 5P satellite pixel. "
        "Color indicates methane concentration in parts per billion. "
        "Red indicates higher concentrations."
    )
    
    season = st.radio(
        "Select dataset to visualize",
        [
            "Winter — January 2023 (77,134 observations)",
            "Summer — June to August 2023 (227,477 observations)",
            "Hotspots Only — Pixels above NOAA background"
        ],
        horizontal=True
    )
    
    if "Winter" in season:
        plot_df = winter_df.sample(min(20000, len(winter_df)), random_state=42)
        title = "Winter Methane Concentrations — USA January 2023"
        cmin, cmax = 1870, 1980
        bg_note = "NOAA background: 1919.93 ppb"
    elif "Summer" in season:
        plot_df = summer_df.sample(min(20000, len(summer_df)), random_state=42)
        title = "Summer Methane Concentrations — USA June to August 2023"
        cmin, cmax = 1870, 1995
        bg_note = "NOAA background: 1914.89 ppb"
    else:
        plot_df = pd.concat([winter_hotspots, summer_hotspots], ignore_index=True)
        title = "Emission Hotspots — Pixels Exceeding NOAA Global Background"
        cmin, cmax = 1915, 1995
        bg_note = "Only pixels above NOAA verified background shown"
    
    st.caption(bg_note)
    
    fig_map = px.scatter_mapbox(
        plot_df,
        lat="latitude",
        lon="longitude",
        color="methane_column_ppb",
        color_continuous_scale="RdYlGn_r",
        range_color=[cmin, cmax],
        mapbox_style="open-street-map",
        zoom=3,
        center={"lat": 38, "lon": -96},
        title=title,
        labels={"methane_column_ppb": "CH4 (ppb)"},
        height=550,
        hover_data={
            "latitude": ":.3f",
            "longitude": ":.3f",
            "methane_column_ppb": ":.1f"
        }
    )
    
    fig_map.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="CH4 ppb",
            thickness=15,
            len=0.7
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.caption(
        "Data: ESA Sentinel 5P TROPOMI L2 CH4 product via Copernicus Data Space. "
        "Quality filtered at qa_value > 0.5 per ESA documentation."
    )

# TAB 2: GAP ANALYSIS
with tab2:
    st.markdown("### Seasonal Analysis and Gap Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Pixel Distribution Above Background")
        
        dist_data = pd.DataFrame({
            "Season": ["Winter January", "Winter January", 
                      "Summer June-Aug", "Summer June-Aug"],
            "Category": ["Below Background", "Above Background",
                        "Below Background", "Above Background"],
            "Percentage": [78.5, 21.5, 88.3, 11.7],
            "Count": [
                len(winter_df) - len(winter_hotspots),
                len(winter_hotspots),
                len(summer_df) - len(summer_hotspots),
                len(summer_hotspots)
            ]
        })
        
        fig_dist = px.bar(
            dist_data,
            x="Season",
            y="Percentage",
            color="Category",
            color_discrete_map={
                "Below Background": "#90CAF9",
                "Above Background": "#EF5350"
            },
            title="Percentage of Pixels Above vs Below NOAA Background",
            labels={"Percentage": "Percentage of Observations"},
            text="Percentage",
            height=400
        )
        fig_dist.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        fig_dist.update_layout(showlegend=True, legend_title="Category")
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### Official UNFCCC Reported Trend 2015 to 2022")
        
        fig_trend = px.line(
            official_data,
            x="year",
            y="reported_Mt_CH4",
            markers=True,
            title="USA Official Methane Inventory Submissions",
            labels={
                "reported_Mt_CH4": "Mt CH4 per year",
                "year": "Year"
            },
            height=400
        )
        fig_trend.update_traces(
            line=dict(width=2.5, color="#1565C0"),
            marker=dict(size=8, color="#1565C0")
        )
        fig_trend.update_layout(
            yaxis=dict(range=[30, 42]),
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.divider()
    
    st.markdown("#### Seasonal Summary Statistics")
    
    summary_df = pd.DataFrame({
        "Season": ["Winter January 2023", "Summer June-Aug 2023", "Annual Average"],
        "Observations": [f"{len(winter_df):,}", f"{len(summer_df):,}", f"{len(winter_df)+len(summer_df):,}"],
        "Satellite Mean ppb": [1904.7, 1894.9, 1899.8],
        "NOAA Background ppb": [1919.93, 1914.89, 1917.41],
        "Enhancement ppb": [-15.2, -19.97, -17.58],
        "Pixels Above Background": [f"{len(winter_hotspots):,} (21.5%)", f"{len(summer_hotspots):,} (11.7%)", "43,086 (14.1%)"]
    })
    
    st.dataframe(
        summary_df,
        hide_index=True,
        use_container_width=True
    )
    
    st.info("""
    **Interpretation:** The satellite mean concentration falls below the NOAA verified 
    global background for both seasons. This reveals a fundamental characteristic of 
    national scale passive satellite monitoring: the majority of pixels capture background 
    air rather than emission plumes, which disperse rapidly across the 5.5 km pixel footprint.
    This does not indicate a satellite failure. It reveals the spatial resolution constraints 
    of column average measurements at the national scale.
    """)

# TAB 3: HOTSPOTS
with tab3:
    st.markdown("### Identified Emission Hotspots")
    st.markdown(
        "These are the pixels that exceed the NOAA verified background. "
        "They cluster with geographic precision over known emission sources."
    )
    
    hotspot_regions = pd.DataFrame({
        "Region": [
            "Northern Plains MN-ND Border",
            "Gulf Coast TX-LA Offshore",
            "California Central Valley"
        ],
        "Season": ["Winter", "Summer", "Summer"],
        "Hotspot Observations": [485, 1271, 1221],
        "Peak Concentration ppb": [1976.2, 1990.7, 1985.2],
        "Peak Enhancement ppb": [56.3, 75.9, 70.3],
        "Mean Hotspot ppb": [1935.6, 1926.7, 1925.3],
        "Likely Emission Source": [
            "Agricultural wetlands and oil gas operations",
            "Offshore oil gas and petrochemical corridor",
            "Dairy farming and agricultural operations"
        ]
    })
    
    st.dataframe(
        hotspot_regions,
        hide_index=True,
        use_container_width=True
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Winter Hotspot Distribution")
        fig_w = px.histogram(
            winter_hotspots,
            x="methane_column_ppb",
            nbins=40,
            title=f"Winter Hotspot Pixels n={len(winter_hotspots):,}",
            labels={"methane_column_ppb": "CH4 Concentration ppb"},
            color_discrete_sequence=["#1565C0"],
            height=350
        )
        fig_w.add_vline(
            x=1919.93,
            line_dash="dash",
            line_color="red",
            annotation_text="NOAA background 1919.93 ppb"
        )
        st.plotly_chart(fig_w, use_container_width=True)
    
    with col2:
        st.markdown("#### Summer Hotspot Distribution")
        fig_s = px.histogram(
            summer_hotspots,
            x="methane_column_ppb",
            nbins=40,
            title=f"Summer Hotspot Pixels n={len(summer_hotspots):,}",
            labels={"methane_column_ppb": "CH4 Concentration ppb"},
            color_discrete_sequence=["#E65100"],
            height=350
        )
        fig_s.add_vline(
            x=1914.89,
            line_dash="dash",
            line_color="red",
            annotation_text="NOAA background 1914.89 ppb"
        )
        st.plotly_chart(fig_s, use_container_width=True)
    
    st.markdown("#### The Core Finding")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background:#E3F2FD; padding:1.2rem; border-radius:8px; 
        border-left:4px solid #1565C0;">
        <h4 style="color:#1565C0; margin:0;">🏔️ Northern Plains</h4>
        <p style="margin:0.5rem 0 0 0;">
        Peak: <strong>1976.2 ppb</strong><br>
        Enhancement: <strong>+56.3 ppb</strong><br>
        Agricultural wetlands and Bakken adjacent oil gas operations
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background:#FFF3E0; padding:1.2rem; border-radius:8px;
        border-left:4px solid #E65100;">
        <h4 style="color:#E65100; margin:0;">🌊 Gulf Coast</h4>
        <p style="margin:0.5rem 0 0 0;">
        Peak: <strong>1990.7 ppb</strong><br>
        Enhancement: <strong>+75.9 ppb</strong><br>
        Highest single pixel in entire dataset. Offshore petrochemical corridor.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background:#F3E5F5; padding:1.2rem; border-radius:8px;
        border-left:4px solid #6A1B9A;">
        <h4 style="color:#6A1B9A; margin:0;">🌾 California Central Valley</h4>
        <p style="margin:0.5rem 0 0 0;">
        Peak: <strong>1985.2 ppb</strong><br>
        Enhancement: <strong>+70.3 ppb</strong><br>
        Dairy farming and agricultural methane emissions
        </p>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: METHODOLOGY
with tab4:
    st.markdown("### Methodology and Reproducibility")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Data Pipeline Architecture
        
        **Step 1: Satellite Data Ingestion**
        ESA Sentinel 5P TROPOMI L2 methane product downloaded 
        via Copernicus Data Space API using Python requests and 
        processed from netCDF4 format using xarray.
        
        **Step 2: Quality Filtering**
        Only observations with qa_value greater than 0.5 retained 
        per ESA TROPOMI Level 2 Product documentation standards. 
        Physical plausibility filter applied: 1600 to 2200 ppb range.
        
        **Step 3: Geographic Filtering**
        Continental USA bounding box: latitude 24 to 50 north, 
        longitude 125 to 66 west.
        
        **Step 4: Warehouse Loading**
        Processed observations loaded to Snowflake in batches 
        of 10,000 records with deduplication on date, latitude, 
        and longitude.
        
        **Step 5: Background Comparison**
        NOAA Global Monitoring Laboratory monthly mean methane 
        concentrations used as period specific background values.
        Enhancement calculated as satellite mean minus NOAA background.
        
        **Step 6: Official Data**
        UNFCCC national GHG inventory submissions accessed via 
        Climate Watch API filtered for CH4 gas and USA region.
        """)
    
    with col2:
        st.markdown("""
        #### Key Methodological Decisions
        
        **Background Value Selection**
        
        Using the correct period specific NOAA background is critical. 
        The global mean methane has risen significantly over recent decades. 
        Using a historical fixed value of 1870 ppb would overestimate 
        enhancement by approximately 50 ppb for 2023 data.
        
        January 2023 NOAA GML mean: **1919.93 ppb**  
        Summer 2023 NOAA GML mean: **1914.89 ppb**
        
        **Limitations**
        
        This analysis covers four months representing winter and summer 
        only. Spring and autumn data would complete the annual picture.
        
        Orbital pass coverage is not uniform across all regions. 
        Cloud cover reduces valid observations in some areas.
        
        The Turner et al 2020 ppb to Mt conversion factor assumes 
        uniform atmospheric mixing and full national coverage. 
        Neither assumption fully holds for this dataset.
        
        **Reproducibility**
        
        Full pipeline code available at GitHub link below.
        All data sources are free and publicly accessible.
        Zero proprietary data used.
        """)
    
    st.divider()
    
    st.markdown("#### Reproduce This Analysis")
    
    st.code("""
# Step 1: Create free accounts
# dataspace.copernicus.eu - ESA satellite data
# snowflake.com - Cloud data warehouse

# Step 2: Open notebook in Google Colab
# github.com/likitha-sree-data/methane-truth

# Step 3: Run Cell 1 - installs packages and mounts Drive
# Step 4: Run Cell 2 - defines all functions  
# Step 5: Follow cells sequentially

# All data sources are free and publicly accessible
# Total runtime approximately 2 hours for full dataset
    """, language="bash")
    
    st.markdown("""
    #### Citations
    
    ESA Sentinel 5P TROPOMI methane product documentation: 
    sentinel.esa.int/web/sentinel/technical-guides/sentinel-5p
    
    NOAA Global Monitoring Laboratory methane data: 
    gml.noaa.gov/ccgg/trends_ch4
    
    Turner et al 2020 methane conversion methodology: 
    Science 369, 1219-1223
    
    Climate Watch API documentation: 
    climatewatchdata.org/api
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; font-size:0.85rem; padding:1rem;">
Built with real satellite data · Zero proprietary sources · Full reproducibility<br>
ESA Sentinel 5P TROPOMI · NOAA GML · UNFCCC via Climate Watch · 
<a href="https://github.com/likitha-sree-data/methane-truth">GitHub</a> · 
<a href="https://linkedin.com/in/likitha-sree">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
