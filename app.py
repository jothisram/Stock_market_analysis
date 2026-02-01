"""
Data-Driven Stock Analysis Dashboard
Enhanced Streamlit Application with Modern Glassmorphism UI
Author: Stock Analysis Team | Enhanced by AI
Date: January 2025
Version: 2.1 Pro (Fixed)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import pickle
import warnings
from streamlit_option_menu import option_menu
import time

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION & ENHANCED THEME SETUP
# ============================================================================

st.set_page_config(
    page_title="NIFTY 50 Pro Analytics",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': "https://github.com",
        'About': "# NIFTY 50 Pro Analytics\nEnhanced Stock Dashboard v2.1"
    }
)

# Premium Sunset Glow Palette with Gradients
SUNSET_GLOW = {
    'dark_orange': '#FF6B35',
    'coral': '#F7931E',
    'peach': '#FFD166',
    'light_yellow': '#F5D547',
    'pink': '#EF476F',
    'dark_bg': '#0a0e1a',
    'card_bg': 'rgba(20, 25, 40, 0.7)',
    'light_bg': '#151b2d',
    'white_text': '#f8fafc',
    'muted_text': '#94a3b8',
    'accent': '#FFB703',
    'success': '#06d6a0',
    'danger': '#ef476f',
    'gradient_start': '#FF6B35',
    'gradient_end': '#F7931E'
}

# Helper function to convert hex to rgba
def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

# Advanced CSS with Animated Mesh Gradient Background
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        /* Animated Mesh Gradient Background */
        .main {{
            background: 
                radial-gradient(at 0% 0%, rgba(255, 107, 53, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(247, 147, 30, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(255, 179, 3, 0.1) 0px, transparent 50%),
                radial-gradient(at 0% 100%, rgba(239, 71, 111, 0.1) 0px, transparent 50%),
                linear-gradient(135deg, {SUNSET_GLOW['dark_bg']} 0%, #0f172a 50%, {SUNSET_GLOW['light_bg']} 100%);
            background-attachment: fixed;
            animation: gradientShift 15s ease infinite;
            background-size: 200% 200%;
        }}
        
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Floating Orbs Background */
        .main::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(255, 107, 53, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(247, 147, 30, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(255, 179, 3, 0.05) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
        }}
        
        /* Grid Pattern Overlay */
        .main::after {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
        }}
        
        /* Ensure content is above background */
        .block-container {{
            position: relative;
            z-index: 1;
        }}
        
        /* Glassmorphism Cards */
        .glass-card {{
            background: {SUNSET_GLOW['card_bg']};
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4),
                        inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .glass-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(255, 107, 53, 0.15),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 107, 53, 0.3);
        }}
        
        /* Headers with Gradient Text */
        h1, h2, h3 {{
            font-family: 'Space Grotesk', sans-serif;
            background: linear-gradient(135deg, {SUNSET_GLOW['peach']} 0%, {SUNSET_GLOW['coral']} 50%, {SUNSET_GLOW['dark_orange']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {{
            background: linear-gradient(180deg, rgba(20, 25, 40, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        /* Metric Cards */
        .metric-container {{
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(247, 147, 30, 0.05) 100%);
            border-left: 4px solid {SUNSET_GLOW['coral']};
            border-radius: 16px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .metric-container:hover {{
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(247, 147, 30, 0.1) 100%);
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.1);
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: 700;
            color: {SUNSET_GLOW['peach']};
            text-shadow: 0 0 20px rgba(255, 107, 53, 0.3);
        }}
        
        .metric-label {{
            color: {SUNSET_GLOW['muted_text']};
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 4px;
        }}
        
        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 16px;
            background-color: rgba(20, 25, 40, 0.6);
            padding: 12px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {SUNSET_GLOW['muted_text']};
            font-weight: 600;
            padding: 12px 24px;
            border-radius: 12px;
            transition: all 0.3s;
            border: 1px solid transparent;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {SUNSET_GLOW['coral']} 0%, {SUNSET_GLOW['dark_orange']} 100%);
            color: white !important;
            box-shadow: 0 4px 20px rgba(255, 107, 53, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {SUNSET_GLOW['coral']} 0%, {SUNSET_GLOW['dark_orange']} 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 53, 0.5);
            background: linear-gradient(135deg, {SUNSET_GLOW['dark_orange']} 0%, {SUNSET_GLOW['coral']} 100%);
        }}
        
        /* DataFrames */
        .dataframe {{
            background-color: rgba(20, 25, 40, 0.6) !important;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {SUNSET_GLOW['dark_bg']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, {SUNSET_GLOW['coral']}, {SUNSET_GLOW['dark_orange']});
            border-radius: 5px;
        }}
        
        /* Loading Animation */
        .stSpinner > div {{
            border-top-color: {SUNSET_GLOW['coral']} !important;
        }}
        
        /* Info Boxes */
        .info-box {{
            background: linear-gradient(135deg, rgba(6, 214, 160, 0.1) 0%, rgba(6, 214, 160, 0.05) 100%);
            border-left: 4px solid {SUNSET_GLOW['success']};
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, rgba(239, 71, 111, 0.1) 0%, rgba(239, 71, 111, 0.05) 100%);
            border-left: 4px solid {SUNSET_GLOW['danger']};
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        /* Chart Containers */
        .chart-container {{
            background: {SUNSET_GLOW['card_bg']};
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            height: 100%;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate-in {{
            animation: fadeIn 0.6s ease-out forwards;
        }}
        
        /* Select Box Styling */
        .stSelectbox div[data-baseweb="select"] {{
            background-color: rgba(20, 25, 40, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* MultiSelect */
        .stMultiSelect div[data-baseweb="select"] {{
            background-color: rgba(20, 25, 40, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* Slider */
        .stSlider > div > div > div {{
            background: linear-gradient(90deg, {SUNSET_GLOW['coral']}, {SUNSET_GLOW['dark_orange']}) !important;
        }}
        
        /* Divider */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, {SUNSET_GLOW['coral']}, transparent);
            margin: 3rem 0;
        }}
        
        /* Table Styling */
        .stDataFrame {{
            border-radius: 16px;
            overflow: hidden;
        }}
        
        /* Plotly Chart Background Override */
        .js-plotly-plot {{
            border-radius: 12px;
        }}
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING WITH LOADING STATE
# ============================================================================

@st.cache_resource
def load_processed_data():
    """Load pre-processed data with error handling"""
    try:
        with open('./processed_data/processed_data.pkl', 'rb') as f:
            data = pickle.load(f)
        return data
    except FileNotFoundError:
        st.error("⚠️ Data not found. Please ensure processed_data.pkl exists in ./processed_data/")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading data: {str(e)}")
        return None

# Loading State with Animation
with st.spinner("🌅 Loading Market Data..."):
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)
    
    data = load_processed_data()
    progress_bar.empty()

if data is None:
    st.stop()

master_df = data['master_data']
metrics_df = data['metrics']
correlation_matrix = data['correlation_matrix']
monthly_df = data['monthly_performance']
market_summary = data['market_summary']

# ============================================================================
# HEADER SECTION WITH ANIMATED TITLE
# ============================================================================

st.markdown("""
    <div class='animate-in' style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #FFD166 0%, #F7931E 50%, #FF6B35 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🌅 NIFTY 50 <span style='color: #F7931E;'>Pro Analytics</span>
        </h1>
        <p style='color: #94a3b8; font-size: 1.3rem; font-weight: 300; letter-spacing: 0.1em; text-transform: uppercase;'>
            Next-Generation Market Intelligence
        </p>
        <div style='display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; font-size: 0.9rem; color: #64748b;'>
            <span>📅 """ + datetime.now().strftime("%B %d, %Y") + """</span>
            <span>•</span>
            <span>⏱ Live Market Data</span>
            <span>•</span>
            <span>🔔 Real-time Analysis</span>
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)

# ============================================================================
# ENHANCED SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 1rem;'>
            <h2 style='color: white; font-size: 1.5rem; margin-bottom: 0.5rem;'>🎯 Navigation</h2>
            <p style='color: {SUNSET_GLOW['muted_text']}; font-size: 0.9rem;'>Select Dashboard Module</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_page = option_menu(
        menu_title=None,
        options=["Market Overview", "Top Performers", "Worst Performers", 
                "Volatility Analysis", "Cumulative Returns", "Sector Analysis",
                "Correlation Matrix", "Monthly Trends", "Stock Comparator"],
        icons=["graph-up", "trophy", "graph-down", "activity", "trending-up", 
               "pie-chart", "shuffle", "calendar", "git-compare"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": SUNSET_GLOW['coral'], "font-size": "1.2rem"},
            "nav-link": {
                "color": SUNSET_GLOW['muted_text'],
                "font-size": "0.95rem",
                "font-weight": "600",
                "padding": "1rem 1.5rem",
                "margin": "0.5rem 0",
                "border-radius": "12px",
                "transition": "all 0.3s",
                "border": "1px solid transparent"
            },
            "nav-link-selected": {
                "background": f"linear-gradient(135deg, {SUNSET_GLOW['coral']} 0%, {SUNSET_GLOW['dark_orange']} 100%)",
                "color": "white",
                "box-shadow": f"0 4px 20px rgba(255, 107, 53, 0.4)",
                "border": f"1px solid rgba(255, 255, 255, 0.2)"
            }
        }
    )

# ============================================================================
# HELPER FUNCTIONS FOR VISUALIZATIONS
# ============================================================================

def create_gauge_chart(value, title, max_val=100):
    """Create a beautiful gauge chart for metrics"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': SUNSET_GLOW['white_text']}},
        gauge={
            'axis': {'range': [None, max_val], 'tickcolor': SUNSET_GLOW['muted_text']},
            'bar': {'color': SUNSET_GLOW['coral']},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.1)",
            'steps': [
                {'range': [0, max_val*0.3], 'color': "rgba(255,255,255,0.05)"},
                {'range': [max_val*0.3, max_val*0.7], 'color': "rgba(255,255,255,0.08)"},
                {'range': [max_val*0.7, max_val], 'color': "rgba(255,255,255,0.12)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': SUNSET_GLOW['white_text']},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def style_plotly_chart(fig, title):
    """Apply consistent styling to Plotly charts"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,25,40,0.3)',
        title={
            'text': title,
            'font': {'size': 24, 'color': SUNSET_GLOW['accent'], 'family': 'Space Grotesk'},
            'x': 0.5,
            'xanchor': 'center'
        },
        font=dict(color=SUNSET_GLOW['white_text']),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color=SUNSET_GLOW['muted_text'])
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color=SUNSET_GLOW['muted_text'])
        ),
        legend=dict(
            bgcolor='rgba(20,25,40,0.8)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(color=SUNSET_GLOW['white_text'])
        ),
        hoverlabel=dict(
            bgcolor='rgba(20,25,40,0.9)',
            font_color=SUNSET_GLOW['white_text'],
            bordercolor=SUNSET_GLOW['coral']
        )
    )
    return fig

# ============================================================================
# MARKET OVERVIEW PAGE (ENHANCED)
# ============================================================================

if selected_page == "Market Overview":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Total Stocks", market_summary['Total_Stocks'], "Nifty 50 Constituents", "🎯"),
        ("Green Stocks", market_summary['Green_Stocks'], f"{market_summary['Green_Percentage']:.1f}% of Market", "🚀"),
        ("Red Stocks", market_summary['Red_Stocks'], f"{market_summary['Red_Percentage']:.1f}% of Market", "📉"),
        ("Avg Return", f"{market_summary['Avg_Return']:.2f}%", "Yearly Performance", "💰")
    ]
    
    for col, (label, value, delta, icon) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
                <div class='glass-card' style='text-align: center;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{icon}</div>
                    <div class='metric-value'>{value}</div>
                    <div class='metric-label'>{label}</div>
                    <div style='color: {SUNSET_GLOW['muted_text']}; font-size: 0.85rem; margin-top: 4px;'>
                        {delta}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Secondary Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_price = master_df['Close'].mean()
        st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid {SUNSET_GLOW["success"]};'>
                <h4 style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.9rem;'>💵 Average Price</h4>
                <h2 style='margin: 10px 0; color: white; font-size: 2rem;'>₹{avg_price:,.2f}</h2>
                <p style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.85rem;'>
                    Mean closing price across all stocks
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_volume = master_df['Volume'].mean()
        st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid {SUNSET_GLOW["accent"]};'>
                <h4 style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.9rem;'>📊 Avg Volume</h4>
                <h2 style='margin: 10px 0; color: white; font-size: 2rem;'>{avg_volume:,.0f}</h2>
                <p style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.85rem;'>
                    Daily trading volume average
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        market_return = metrics_df['Yearly_Return'].sum()
        st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid {SUNSET_GLOW["coral"]};'>
                <h4 style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.9rem;'>📈 Total Return</h4>
                <h2 style='margin: 10px 0; color: white; font-size: 2rem;'>{market_return:,.2f}%</h2>
                <p style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.85rem;'>
                    Aggregated market performance
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Market Distribution with Plotly
    st.markdown("<div class='glass-card' style='margin-top: 2rem;'>", unsafe_allow_html=True)
    st.subheader("🎯 Market Sentiment Distribution")
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Green Stocks', 'Red Stocks'],
        values=[market_summary['Green_Stocks'], market_summary['Red_Stocks']],
        hole=0.65,
        marker=dict(
            colors=[SUNSET_GLOW['success'], SUNSET_GLOW['danger']],
            line=dict(color='rgba(255,255,255,0.2)', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=16, color='white', family='Inter'),
        hovertemplate='<b>%{label}</b><br>Stocks: %{value}<br>Share: %{percent}<extra></extra>'
    )])
    
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
        height=500,
        annotations=[dict(
            text=f"<b>{market_summary['Green_Stocks']}</b><br><span style='font-size:14px;color:#94a3b8'>Advancing</span>",
            x=0.5, y=0.5,
            font_size=28,
            font_color=SUNSET_GLOW['success'],
            showarrow=False,
            font_family='Space Grotesk'
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TOP PERFORMERS PAGE (ENHANCED)
# ============================================================================

elif selected_page == "Top Performers":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("🏆 Elite Performers - Top 10 Gainers")
    
    top_10 = metrics_df.head(10).copy()
    top_10['Return_Val'] = top_10['Yearly_Return']
    
    # Interactive Bar Chart
    fig = go.Figure()
    
    colors_list = [SUNSET_GLOW['success'] if x > 50 else SUNSET_GLOW['peach'] if x > 25 else SUNSET_GLOW['coral'] for x in top_10['Yearly_Return']]
    
    fig.add_trace(go.Bar(
        x=top_10['Symbol'],
        y=top_10['Yearly_Return'],
        marker=dict(
            color=colors_list,
            line=dict(color='rgba(255,255,255,0.2)', width=2)
        ),
        text=top_10['Yearly_Return'].apply(lambda x: f'+{x:.2f}%'),
        textposition='outside',
        textfont=dict(color=SUNSET_GLOW['white_text'], size=13, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Return: %{y:.2f}%<br>Rank: %{customdata}<extra></extra>',
        customdata=[f'#{i+1}' for i in range(len(top_10))]
    ))
    
    fig = style_plotly_chart(fig, "Top 10 Performing Stocks - Annual Returns")
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Cards
    st.subheader("💎 Detailed Performance Metrics")
    cols = st.columns(5)
    for idx, (_, row) in enumerate(top_10.head(5).iterrows()):
        with cols[idx]:
            st.markdown(f"""
                <div class='glass-card' style='text-align: center; border-top: 4px solid {SUNSET_GLOW["success"]};'>
                    <h3 style='margin: 0; color: {SUNSET_GLOW["peach"]}; font-size: 1.5rem;'>{row['Symbol']}</h3>
                    <p style='margin: 5px 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.85rem;'>{row['Sector']}</p>
                    <h2 style='margin: 15px 0; color: {SUNSET_GLOW["success"]}; font-size: 2rem;'>+{row['Yearly_Return']:.2f}%</h2>
                    <div style='background: rgba(255,255,255,0.05); border-radius: 8px; padding: 8px; margin-top: 10px;'>
                        <p style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.8rem;'>
                            Volatility: {row['Volatility']:.2f}
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Data Table with Styling
    st.subheader("📋 Complete Rankings")
    display_df = top_10[['Symbol', 'Sector', 'Yearly_Return', 'Volatility', 'Avg_Price']].copy()
    display_df.columns = ['Symbol', 'Sector', 'Annual Return (%)', 'Volatility', 'Avg Price (₹)']
    
    st.dataframe(
        display_df.style
        .background_gradient(subset=['Annual Return (%)'], cmap='YlOrRd', vmin=0, vmax=100)
        .format({'Annual Return (%)': '{:.2f}%', 'Volatility': '{:.2f}', 'Avg Price (₹)': '₹{:.2f}'})
        .set_properties(**{'background-color': 'rgba(20,25,40,0.5)', 'color': 'white', 'border-color': 'rgba(255,255,255,0.1)'}),
        use_container_width=True,
        height=400
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# WORST PERFORMERS PAGE (ENHANCED)
# ============================================================================

elif selected_page == "Worst Performers":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("⚠️ Risk Alert - Top 10 Decliners")
    
    worst_10 = metrics_df.tail(10).copy().sort_values('Yearly_Return')
    
    colors_list = [SUNSET_GLOW['danger'] if x < -30 else '#f87171' if x < -15 else '#fca5a5' for x in worst_10['Yearly_Return']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=worst_10['Symbol'],
        y=worst_10['Yearly_Return'],
        marker=dict(
            color=colors_list,
            line=dict(color='rgba(255,255,255,0.2)', width=2)
        ),
        text=worst_10['Yearly_Return'].apply(lambda x: f'{x:.2f}%'),
        textposition='outside',
        textfont=dict(color=SUNSET_GLOW['white_text'], size=13)
    ))
    
    fig = style_plotly_chart(fig, "Stocks Requiring Attention - Annual Performance")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Indicators
    st.subheader("🚨 Risk Assessment Cards")
    cols = st.columns(5)
    for idx, (_, row) in enumerate(worst_10.head(5).iterrows()):
        with cols[idx]:
            st.markdown(f"""
                <div class='glass-card' style='text-align: center; border-top: 4px solid {SUNSET_GLOW["danger"]};'>
                    <h3 style='margin: 0; color: {SUNSET_GLOW["danger"]}; font-size: 1.5rem;'>{row['Symbol']}</h3>
                    <p style='margin: 5px 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.85rem;'>{row['Sector']}</p>
                    <h2 style='margin: 15px 0; color: {SUNSET_GLOW["danger"]}; font-size: 2rem;'>{row['Yearly_Return']:.2f}%</h2>
                    <div style='background: rgba(239, 71, 111, 0.1); border-radius: 8px; padding: 8px; margin-top: 10px;'>
                        <p style='margin: 0; color: {SUNSET_GLOW["danger"]}; font-weight: 600; font-size: 0.8rem;'>
                            HIGH RISK
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# VOLATILITY ANALYSIS PAGE (ENHANCED)
# ============================================================================

elif selected_page == "Volatility Analysis":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("📊 Volatility & Risk Assessment")
    
    st.markdown("""
        <div class='glass-card info-box' style='margin-bottom: 2rem;'>
            <h4 style='margin: 0 0 10px 0; color: #06d6a0;'>💡 Understanding Volatility</h4>
            <p style='margin: 0; color: #cbd5e1; font-size: 0.95rem;'>
                Higher volatility indicates higher risk but potentially higher returns. 
                Lower volatility suggests stability suitable for conservative portfolios.
                <b>X-axis:</b> Risk (Volatility) | <b>Y-axis:</b> Return (Annual %)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    top_volatile = metrics_df.nlargest(10, 'Volatility')
    
    # Volatility Scatter Plot
    fig = px.scatter(
        metrics_df,
        x='Volatility',
        y='Yearly_Return',
        color='Yearly_Return',
        size='Avg_Price',
        hover_data=['Symbol', 'Sector'],
        color_continuous_scale=['#ef476f', '#ffd166', '#06d6a0'],
        title="Risk vs Return Analysis - Complete Market View"
    )
    
    fig = style_plotly_chart(fig, "Risk-Return Matrix")
    fig.update_traces(
        marker=dict(
            line=dict(color='rgba(255,255,255,0.3)', width=1),
            sizemode='area',
            sizeref=2.*max(metrics_df['Avg_Price'])/(40.**2)
        ),
        selector=dict(mode='markers')
    )
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=2)
    fig.add_vline(x=metrics_df['Volatility'].median(), line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=2)
    fig.add_annotation(x=metrics_df['Volatility'].max()*0.9, y=metrics_df['Yearly_Return'].max()*0.9,
                      text="High Risk<br>High Return", showarrow=False, font=dict(color='white', size=12),
                      bgcolor='rgba(255,255,255,0.1)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Volatile Stocks
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("⚡ Highest Volatility Stocks")
        fig_bar = go.Figure(go.Bar(
            x=top_volatile['Symbol'],
            y=top_volatile['Volatility'],
            marker=dict(
                color=top_volatile['Volatility'],
                colorscale='Reds',
                line=dict(color='rgba(255,255,255,0.2)', width=2)
            ),
            text=top_volatile['Volatility'].apply(lambda x: f'{x:.2f}'),
            textposition='auto',
            textfont=dict(color='white')
        ))
        fig_bar = style_plotly_chart(fig_bar, "Volatility Rankings")
        fig_bar.update_layout(height=450)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("📈 Distribution")
        fig_hist = go.Figure(go.Histogram(
            x=metrics_df['Volatility'],
            nbinsx=20,
            marker=dict(
                color=SUNSET_GLOW['coral'],
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            opacity=0.8
        ))
        fig_hist = style_plotly_chart(fig_hist, "Volatility Spread")
        fig_hist.update_layout(
            height=450,
            bargap=0.1,
            xaxis_title="Volatility (%)",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# CUMULATIVE RETURNS PAGE (FIXED)
# ============================================================================

elif selected_page == "Cumulative Returns":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("🚀 Wealth Growth Trajectory")
    
    # Stock Selector
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_stocks = st.multiselect(
            "Select Stocks to Compare (Max 5)",
            options=metrics_df['Symbol'].tolist(),
            default=metrics_df.head(5)['Symbol'].tolist()
        )
    with col2:
        time_range = st.selectbox("Time Range", ["1Y", "6M", "3M", "1M"], index=0)
    
    if len(selected_stocks) > 5:
        st.warning("⚠️ Please select maximum 5 stocks for optimal viewing")
        selected_stocks = selected_stocks[:5]
    
    if selected_stocks:
        # Calculate Cumulative Returns
        fig = go.Figure()
        colors = px.colors.sequential.Plasma[:len(selected_stocks)]
        
        for idx, symbol in enumerate(selected_stocks):
            symbol_data = master_df[master_df['Symbol'] == symbol].sort_values('Date')
            symbol_data['Cumulative_Return'] = (1 + symbol_data['Daily_Return'] / 100).cumprod() - 1
            
            # Convert hex color to rgba for fill
            fill_color = hex_to_rgba(colors[idx], 0.1) if idx == 0 else 'rgba(0,0,0,0)'
            
            fig.add_trace(go.Scatter(
                x=symbol_data['Date'],
                y=symbol_data['Cumulative_Return'] * 100,
                mode='lines',
                name=symbol,
                line=dict(color=colors[idx], width=3),
                fill='tonexty' if idx == 0 else 'none',
                fillcolor=fill_color
            ))
        
        fig = style_plotly_chart(fig, "Cumulative Returns Comparison")
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Cumulative Return (%)",
            hovermode="x unified",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance Summary Table
        summary_data = []
        for symbol in selected_stocks:
            sym_data = metrics_df[metrics_df['Symbol'] == symbol].iloc[0]
            summary_data.append({
                'Symbol': symbol,
                'Total Return': f"{sym_data['Yearly_Return']:.2f}%",
                'Volatility': f"{sym_data['Volatility']:.2f}",
                'Risk Class': "🔴 High" if sym_data['Volatility'] > 30 else "🟡 Medium" if sym_data['Volatility'] > 20 else "🟢 Low"
            })
        
        st.subheader("📊 Performance Summary")
        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df.style.set_properties(**{'background-color': 'rgba(20,25,40,0.6)', 'color': 'white', 'font-size': '1rem'}))
    else:
        st.info("👆 Please select at least one stock to view cumulative returns")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# SECTOR ANALYSIS PAGE (ENHANCED)
# ============================================================================

elif selected_page == "Sector Analysis":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("🏭 Sector Intelligence")
    
    sector_performance = metrics_df.groupby('Sector').agg({
        'Yearly_Return': ['mean', 'count', 'sum'],
        'Volatility': 'mean'
    }).round(2)
    
    sector_performance.columns = ['Avg_Return', 'Stock_Count', 'Total_Return', 'Avg_Volatility']
    sector_performance = sector_performance.reset_index().sort_values('Avg_Return', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sunburst Chart
        fig = go.Figure(go.Sunburst(
            labels=sector_performance['Sector'].tolist() + metrics_df['Symbol'].tolist(),
            parents=['']*len(sector_performance) + sector_performance['Sector'].tolist(),
            values=sector_performance['Stock_Count'].tolist() + [1]*len(metrics_df),
            branchvalues="total",
            marker=dict(
                colors=sector_performance['Avg_Return'].tolist() + metrics_df['Yearly_Return'].tolist(),
                colorscale='RdYlGn',
                cmid=0
            ),
            hovertemplate='<b>%{label}</b><br>Return: %{color:.2f}%<extra></extra>',
            maxdepth=2
        ))
        
        fig.update_layout(
            margin=dict(t=20, l=0, r=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sector Leaderboard")
        for idx, row in sector_performance.iterrows():
            color = SUNSET_GLOW['success'] if row['Avg_Return'] > 0 else SUNSET_GLOW['danger']
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "•"
            st.markdown(f"""
                <div class='glass-card' style='margin: 10px 0; padding: 16px; border-left: 4px solid {color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h4 style='margin: 0; color: white; font-size: 1.1rem;'>{medal} {row['Sector']}</h4>
                            <p style='margin: 5px 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.85rem;'>
                                {int(row['Stock_Count'])} stocks • Avg Vol: {row['Avg_Volatility']:.1f}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <h3 style='margin: 0; color: {color}; font-size: 1.5rem;'>{row['Avg_Return']:.2f}%</h3>
                        </div>
                    </div>
                    <div style='background: rgba(255,255,255,0.05); height: 4px; border-radius: 2px; margin-top: 10px; overflow: hidden;'>
                        <div style='width: {min(abs(row['Avg_Return'])*2, 100)}%; height: 100%; background: {color}; border-radius: 2px;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# CORRELATION MATRIX PAGE (ENHANCED)
# ============================================================================

elif selected_page == "Correlation Matrix":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("🔗 Portfolio Correlation Matrix")
    
    st.markdown("""
        <div class='glass-card info-box'>
            <h4 style='margin: 0 0 10px 0; color: #06d6a0;'>🔍 Correlation Guide</h4>
            <p style='margin: 0; color: #cbd5e1; font-size: 0.9rem;'>
                <b>1.0:</b> Perfect positive correlation (move together) | 
                <b>-1.0:</b> Perfect negative correlation (hedge opportunity) | 
                <b>0:</b> No correlation (independent movement)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Interactive Correlation Selection
    num_stocks = st.slider("Select Number of Stocks to Display", 5, 30, 15)
    top_symbols = metrics_df.nlargest(num_stocks, 'Yearly_Return')['Symbol'].tolist()
    corr_subset = correlation_matrix.loc[top_symbols, top_symbols]
    
    # Heatmap with better colorscale
    fig = px.imshow(
        corr_subset,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale=[
            [0, "#ef476f"],
            [0.5, "#ffd166"],
            [1, "#06d6a0"]
        ],
        zmin=-1,
        zmax=1
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=SUNSET_GLOW['white_text']),
        height=800,
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        title=dict(
            text=f"Correlation Heatmap - Top {num_stocks} Performers",
            font=dict(size=24, color=SUNSET_GLOW['accent']),
            x=0.5,
            xanchor='center'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Insights
    st.subheader("💡 Correlation Insights")
    corr_pairs = []
    for i in range(len(corr_subset.columns)):
        for j in range(i+1, len(corr_subset.columns)):
            corr_pairs.append({
                'Stock 1': corr_subset.columns[i],
                'Stock 2': corr_subset.columns[j],
                'Correlation': corr_subset.iloc[i, j]
            })
    
    corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📈 Highly Correlated (Move Together)**")
        high_corr = corr_df.head(5)
        for _, row in high_corr.iterrows():
            st.markdown(f"""
                <div style='background: rgba(6, 214, 160, 0.1); padding: 12px; border-radius: 10px; margin: 8px 0; border-left: 3px solid {SUNSET_GLOW['success']};'>
                    <b style='color: white;'>{row['Stock 1']}</b> ↔ <b style='color: white;'>{row['Stock 2']}</b><br>
                    <span style='color: {SUNSET_GLOW['success']}; font-weight: 600;'>Correlation: {row['Correlation']:.3f}</span>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**📉 Negatively Correlated (Hedge Potential)**")
        low_corr = corr_df.tail(5)
        for _, row in low_corr.iterrows():
            st.markdown(f"""
                <div style='background: rgba(239, 71, 111, 0.1); padding: 12px; border-radius: 10px; margin: 8px 0; border-left: 3px solid {SUNSET_GLOW['danger']};'>
                    <b style='color: white;'>{row['Stock 1']}</b> ↔ <b style='color: white;'>{row['Stock 2']}</b><br>
                    <span style='color: {SUNSET_GLOW['danger']}; font-weight: 600;'>Correlation: {row['Correlation']:.3f}</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MONTHLY TRENDS PAGE (FULLY FIXED)
# ============================================================================

elif selected_page == "Monthly Trends":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("📅 Temporal Analysis")
    
    # Month Selector with Styling
    months = sorted(monthly_df['Month_Year'].unique(), reverse=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_month = st.selectbox("📆 Select Analysis Period", months, index=0)
    
    month_data = monthly_df[monthly_df['Month_Year'] == selected_month].copy()
    month_data = month_data.sort_values('Monthly_Return', ascending=False)
    
    # Monthly Overview Cards
    total_gain = len(month_data[month_data['Monthly_Return'] > 0])
    total_loss = len(month_data[month_data['Monthly_Return'] < 0])
    avg_monthly = month_data['Monthly_Return'].mean()
    
    cols = st.columns(4)
    metrics = [
        ("📈 Advancing", total_gain, "Stocks Up", SUNSET_GLOW['success']),
        ("📉 Declining", total_loss, "Stocks Down", SUNSET_GLOW['danger']),
        ("📊 Avg Return", f"{avg_monthly:.2f}%", "Monthly Average", SUNSET_GLOW['accent']),
        ("🎯 Best Performer", month_data.iloc[0]['Symbol'], f"+{month_data.iloc[0]['Monthly_Return']:.2f}%", SUNSET_GLOW['peach'])
    ]
    
    for col, (label, value, sub, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div class='glass-card' style='text-align: center; border-top: 4px solid {color};'>
                    <h4 style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.9rem;'>{label}</h4>
                    <h2 style='margin: 10px 0; color: {color};'>{value}</h2>
                    <p style='margin: 0; color: {SUNSET_GLOW["muted_text"]}; font-size: 0.8rem;'>{sub}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FIXED: Top Gainers and Losers Side by Side
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("<h3 style='color: #06d6a0; margin-bottom: 20px; text-align: center;'>🚀 Top 5 Gainers</h3>", unsafe_allow_html=True)
            top_gainers = month_data.head(5)
            
            fig1 = go.Figure(go.Bar(
                x=top_gainers['Symbol'],
                y=top_gainers['Monthly_Return'],
                marker=dict(
                    color='#06d6a0',
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=top_gainers['Monthly_Return'].apply(lambda x: f'+{x:.2f}%'),
                textposition='outside',
                textfont=dict(color='white', size=12, family='Inter'),
                hovertemplate='<b>%{x}</b><br>Return: %{y:.2f}%<extra></extra>'
            ))
            
            fig1.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(20,25,40,0.3)',
                height=400,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis=dict(
                    tickangle=0,
                    gridcolor='rgba(255,255,255,0.05)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white', size=12),
                    title=dict(text='Stock Symbol', font=dict(color='white', size=13))
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white', size=11),
                    title=dict(text='Monthly Return (%)', font=dict(color='white', size=13))
                ),
                font=dict(color='white'),
                showlegend=False,
                title=dict(
                    text=f'Top Gainers - {selected_month}',
                    font=dict(color='#06d6a0', size=18, family='Space Grotesk'),
                    x=0.5,
                    xanchor='center'
                )
            )
            
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        with st.container():
            st.markdown("<h3 style='color: #ef476f; margin-bottom: 20px; text-align: center;'>⚠️ Top 5 Losers</h3>", unsafe_allow_html=True)
            top_losers = month_data.tail(5).sort_values('Monthly_Return')
            
            fig2 = go.Figure(go.Bar(
                x=top_losers['Symbol'],
                y=top_losers['Monthly_Return'],
                marker=dict(
                    color='#ef476f',
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=top_losers['Monthly_Return'].apply(lambda x: f'{x:.2f}%'),
                textposition='outside',
                textfont=dict(color='white', size=12, family='Inter'),
                hovertemplate='<b>%{x}</b><br>Return: %{y:.2f}%<extra></extra>'
            ))
            
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(20,25,40,0.3)',
                height=400,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis=dict(
                    tickangle=0,
                    gridcolor='rgba(255,255,255,0.05)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white', size=12),
                    title=dict(text='Stock Symbol', font=dict(color='white', size=13))
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    linecolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='white', size=11),
                    title=dict(text='Monthly Return (%)', font=dict(color='white', size=13))
                ),
                font=dict(color='white'),
                showlegend=False,
                title=dict(
                    text=f'Top Losers - {selected_month}',
                    font=dict(color='#ef476f', size=18, family='Space Grotesk'),
                    x=0.5,
                    xanchor='center'
                )
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    # FIXED: Monthly Movers Table with Sector merge
    st.subheader("📋 Complete Monthly Performance")
    
    # Merge with metrics_df to get Sector information
    month_display = month_data[['Symbol', 'Monthly_Return']].copy()
    month_display = month_display.merge(
        metrics_df[['Symbol', 'Sector']], 
        on='Symbol', 
        how='left'
    )
    month_display = month_display[['Symbol', 'Sector', 'Monthly_Return']]
    month_display.columns = ['Symbol', 'Sector', 'Return (%)']
    
    st.dataframe(
        month_display.style
        .background_gradient(subset=['Return (%)'], cmap='RdYlGn', vmin=-20, vmax=20)
        .format({'Return (%)': '{:.2f}%'})
        .set_properties(**{'background-color': 'rgba(20,25,40,0.6)', 'color': 'white'}),
        use_container_width=True,
        height=400
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
# ============================================================================
# STOCK COMPARATOR PAGE (NEW FEATURE)
# ============================================================================

elif selected_page == "Stock Comparator":
    st.markdown("<div class='animate-in'>", unsafe_allow_html=True)
    st.header("⚖️ Advanced Stock Comparator")
    
    col1, col2 = st.columns(2)
    with col1:
        stock1 = st.selectbox("Select Stock A", metrics_df['Symbol'].tolist(), index=0)
    with col2:
        stock2 = st.selectbox("Select Stock B", metrics_df['Symbol'].tolist(), index=1)
    
    if stock1 and stock2:
        s1_data = metrics_df[metrics_df['Symbol'] == stock1].iloc[0]
        s2_data = metrics_df[metrics_df['Symbol'] == stock2].iloc[0]
        
        # Comparison Cards
        cols = st.columns(3)
        metrics_comp = [
            ('Annual Return', 'Yearly_Return', '%'),
            ('Volatility', 'Volatility', ''),
            ('Avg Price', 'Avg_Price', '₹')
        ]
        
        for metric, key, prefix in metrics_comp:
            val1 = s1_data[key]
            val2 = s2_data[key]
            winner = stock1 if val1 > val2 else stock2
            diff = abs(val1 - val2)
            
            with cols[metrics_comp.index((metric, key, prefix))]:
                st.markdown(f"""
                    <div class='glass-card' style='text-align: center;'>
                        <h4 style='color: {SUNSET_GLOW["muted_text"]}; font-size: 0.9rem; margin-bottom: 15px;'>{metric}</h4>
                        <div style='display: flex; justify-content: space-around; align-items: center; margin: 20px 0;'>
                            <div style='text-align: center;'>
                                <h3 style='margin: 0; color: {SUNSET_GLOW["peach"] if winner == stock1 else SUNSET_GLOW["white_text"]}; font-size: 1.2rem;'>{stock1}</h3>
                                <h2 style='margin: 5px 0; font-size: 1.8rem;'>{prefix}{val1:.2f}</h2>
                            </div>
                            <div style='color: {SUNSET_GLOW["coral"]}; font-weight: bold; font-size: 0.8rem;'>VS</div>
                            <div style='text-align: center;'>
                                <h3 style='margin: 0; color: {SUNSET_GLOW["peach"] if winner == stock2 else SUNSET_GLOW["white_text"]}; font-size: 1.2rem;'>{stock2}</h3>
                                <h2 style='margin: 5px 0; font-size: 1.8rem;'>{prefix}{val2:.2f}</h2>
                            </div>
                        </div>
                        <div style='background: rgba(255,107,53,0.1); border-radius: 8px; padding: 8px; margin-top: 10px;'>
                            <p style='margin: 0; color: {SUNSET_GLOW["coral"]}; font-weight: 600; font-size: 0.85rem;'>
                                🏆 {winner} leads by {prefix}{diff:.2f}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Price Movement Comparison Chart
        s1_hist = master_df[master_df['Symbol'] == stock1].sort_values('Date')
        s2_hist = master_df[master_df['Symbol'] == stock2].sort_values('Date')
        
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
        
        fig.add_trace(go.Scatter(
            x=s1_hist['Date'],
            y=s1_hist['Close'],
            name=stock1,
            line=dict(color=SUNSET_GLOW['coral'], width=3),
            mode='lines',
            fill='tonexty',
            fillcolor=hex_to_rgba(SUNSET_GLOW['coral'], 0.1)
        ))
        
        fig.add_trace(go.Scatter(
            x=s2_hist['Date'],
            y=s2_hist['Close'],
            name=stock2,
            line=dict(color=SUNSET_GLOW['success'], width=3),
            mode='lines',
            fill='tonexty',
            fillcolor=hex_to_rgba(SUNSET_GLOW['success'], 0.1)
        ))
        
        fig = style_plotly_chart(fig, f"Price Movement Comparison: {stock1} vs {stock2}")
        fig.update_layout(
            height=500,
            yaxis_title="Price (₹)",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
    <div style='text-align: center; padding: 3rem 2rem; margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.1); position: relative; z-index: 1;'>
        <h3 style='color: {SUNSET_GLOW['coral']}; margin-bottom: 1rem; font-family: Space Grotesk;'>🌅 NIFTY 50 Pro Analytics</h3>
        <p style='color: {SUNSET_GLOW['muted_text']}; font-size: 0.9rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
            Advanced financial analytics and market intelligence platform. 
            Built with cutting-edge technology for sophisticated investors.
        </p>
        <div style='display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; color: {SUNSET_GLOW['muted_text']};'>
            <span style='display: flex; align-items: center; gap: 5px;'>📊 Data-Driven</span>
            <span style='display: flex; align-items: center; gap: 5px;'>⚡ Real-Time</span>
            <span style='display: flex; align-items: center; gap: 5px;'>🔒 Secure</span>
        </div>
        <p style='color: {SUNSET_GLOW['muted_text']}; font-size: 0.8rem;'>
            Last Updated: {datetime.now().strftime("%B %d, %Y at %H:%M:%S")} | 
            System Status: <span style='color: {SUNSET_GLOW['success']}; font-weight: 600;'>● Operational</span>
        </p>
        <p style='color: {SUNSET_GLOW['muted_text']}; font-size: 0.75rem; margin-top: 1rem; opacity: 0.7;'>
            © 2025 Stock Analysis Team. All rights reserved.
        </p>
    </div>
""", unsafe_allow_html=True)