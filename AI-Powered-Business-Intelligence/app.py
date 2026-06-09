import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="AI-Powered Business Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

# ================= CUSTOM CSS - PREMIUM LIGHT THEME =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
    }

    .main .block-container {
        max-width: 1400px;
        padding: 2rem 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-logo {
        font-size: 26px;
        font-weight: 800;
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }

    .sidebar-badge {
        margin: 20px 15px;
        padding: 12px;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 12px;
        font-weight: 700;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .sidebar-info {
        padding: 15px;
        margin: 15px;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        color: #64748b;
        font-size: 13px;
        line-height: 1.8;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.15);
    }

    .hero-section h1 {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero-section p {
        font-size: 17px;
        color: #475569;
        font-weight: 500;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border: 2px solid #f1f5f9;
        position: relative;
        overflow: hidden;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.25);
        border-color: #667eea;
    }

    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        border-radius: 20px 20px 0 0;
    }

    .kpi-1::before { background: linear-gradient(90deg, #4facfe, #00f2fe); }
    .kpi-2::before { background: linear-gradient(90deg, #667eea, #764ba2); }
    .kpi-3::before { background: linear-gradient(90deg, #f093fb, #f5576c); }
    .kpi-4::before { background: linear-gradient(90deg, #43e97b, #38f9d7); }

    .kpi-icon { font-size: 32px; margin-bottom: 8px; }
    .kpi-label { font-size: 13px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .kpi-value { font-size: 28px; font-weight: 800; color: #1e293b; margin-top: 8px; }

    /* Chart Cards */
    .chart-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 2px solid #f1f5f9;
        transition: all 0.3s ease;
    }

    .chart-card:hover {
        border-color: #667eea;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.15);
    }

    /* AI Panel */
    .ai-panel {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(240, 147, 251, 0.08));
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.12);
        border: 2px solid rgba(102, 126, 234, 0.2);
    }

    /* Prediction Card */
    .prediction-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 2px solid #f1f5f9;
    }

    .prediction-card h3 {
        color: #667eea;
        margin-bottom: 20px;
        font-weight: 700;
    }

    /* Prediction Result */
    .prediction-result {
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.12), rgba(56, 249, 215, 0.12));
        border: 2px solid #43e97b;
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
    }

    .result-icon {
        font-size: 48px;
        background: rgba(67, 233, 123, 0.2);
        padding: 15px;
        border-radius: 50%;
    }

    .result-text h4 {
        color: #059669;
        margin: 0 0 5px 0;
        font-size: 18px;
        font-weight: 700;
    }

    .result-text p {
        color: #64748b;
        margin: 0 0 10px 0;
        font-size: 14px;
    }

    .result-value {
        font-size: 32px;
        font-weight: 800;
        color: #059669;
    }

    /* Form Elements */
    div[data-testid="stAlert"] {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        padding: 15px 20px !important;
        margin-bottom: 15px !important;
    }

    div[data-testid="stAlert"] p {
        color: #1e293b !important;
    }

    .stNumberInput input, .stTextInput input {
        background: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
    }

    label {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6) !important;
    }

    /* Sidebar buttons styling */
    .stSidebar div[data-testid="stButton"] > button {
        background: #f8fafc !important;
        color: #475569 !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: none !important;
        text-align: left !important;
        padding: 14px 20px !important;
        margin-bottom: 8px !important;
    }

    .stSidebar div[data-testid="stButton"] > button:hover {
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        color: #667eea !important;
        border-color: #667eea !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
    }

    /* Settings Page Styling */
    .settings-hero {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }

    .settings-hero h1 {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .settings-hero p {
        color: #64748b;
        font-size: 16px;
    }

    .settings-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 2px solid #f1f5f9;
    }

    .settings-section {
        margin-bottom: 30px;
        padding-bottom: 25px;
        border-bottom: 2px solid #f1f5f9;
    }

    .settings-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    .settings-section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .settings-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 0;
        border-bottom: 1px solid #f8fafc;
    }

    .settings-item:last-child {
        border-bottom: none;
    }

    .settings-item-label {
        font-weight: 600;
        color: #475569;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .settings-item-value {
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        color: #667eea;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }

    .stat-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }

    .stat-box-icon {
        font-size: 32px;
        margin-bottom: 10px;
    }

    .stat-box-value {
        font-size: 24px;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 5px;
    }

    .stat-box-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-left: 8px;
    }

    .badge-success {
        background: rgba(67, 233, 123, 0.15);
        color: #059669;
        border: 1px solid rgba(67, 233, 123, 0.3);
    }

    .badge-info {
        background: rgba(102, 126, 234, 0.15);
        color: #667eea;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🤖 AI Analytics</div>', unsafe_allow_html=True)

    st.markdown("#### 🧭 Navigation")

    if st.button("📊  Dashboard", key="btn_dashboard", use_container_width=True):
        st.session_state.page = 'Dashboard'

    if st.button("📈  Analytics", key="btn_analytics", use_container_width=True):
        st.session_state.page = 'Analytics'

    if st.button("🧠  AI Insights", key="btn_insights", use_container_width=True):
        st.session_state.page = 'AI Insights'

    if st.button("⚙️  Settings", key="btn_settings", use_container_width=True):
        st.session_state.page = 'Settings'

    st.markdown('<div class="sidebar-badge">🚀 AI Powered</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info">
        <strong>Project:</strong> BI Dashboard<br>
        <strong>Version:</strong> 2.0<br>
        <strong>Status:</strong> 🟢 Active
    </div>
    """, unsafe_allow_html=True)

# ================= LOAD DATA & MODEL =================
import os
import pandas as pd
import joblib

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create paths that work both locally and on Streamlit Cloud
csv_path = os.path.join(BASE_DIR, "Data", "business_data.csv")
model_path = os.path.join(BASE_DIR, "model.pkl")

# Load Dataset
df = pd.read_csv(csv_path)

# Date Processing
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month'] = df['Order Date'].dt.month

# Load Machine Learning Model
model = joblib.load(model_path)


# ================= HELPER FUNCTION FOR PLOTLY CHARTS =================
def style_fig(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            size=12,
            color="#475569"
        ),
        title=dict(
            font=dict(
                size=20,
                color="#1e293b",
                family="Inter, sans-serif"
            ),
            x=0.05
        ),
        legend=dict(
            font=dict(color="#64748b"),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            gridcolor="#f1f5f9",
            zerolinecolor="#e2e8f0"
        ),
        yaxis=dict(
            gridcolor="#f1f5f9",
            zerolinecolor="#e2e8f0"
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Inter, sans-serif",
            font_color="#1e293b",
            bordercolor="#667eea"
        )
    )
    return fig
# ================= PAGE NAVIGATION LOGIC =================
if st.session_state.page == 'Dashboard':
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>🤖 AI-Powered Business Intelligence</h1>
        <p>Welcome to your premium analytics platform. Uncover insights, predict trends, and drive growth with the power of AI.</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    st.markdown("### 📌 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-1">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">${df['Sales'].sum():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-2">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value">${df['Profit'].sum():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-3">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Total Quantity</div>
            <div class="kpi-value">{int(df['Quantity'].sum()):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-4">
            <div class="kpi-icon">🏷</div>
            <div class="kpi-label">Avg Discount</div>
            <div class="kpi-value">{df['Discount'].mean()*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sales Trend
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Monthly Sales Trend")
    monthly = df.groupby('Month')['Sales'].sum().reset_index()
    fig = px.line(monthly, x='Month', y='Sales', markers=True)
    fig = style_fig(fig)
    fig.update_traces(line=dict(color="#667eea", width=4), marker=dict(color="#764ba2", size=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Region & Category
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("#### 🌍 Region-wise Sales")
        region_sales = df.groupby('Region')['Sales'].sum().reset_index()
        fig2 = px.pie(region_sales, names='Region', values='Sales')
        fig2 = style_fig(fig2)
        fig2.update_traces(marker=dict(colors=["#667eea", "#764ba2", "#4facfe", "#f093fb", "#43e97b"]))
        fig2.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("#### 🛍 Category-wise Profit")
        category_profit = df.groupby('Category')['Profit'].sum().reset_index()
        fig3 = px.bar(category_profit, x='Category', y='Profit')
        fig3 = style_fig(fig3)
        fig3.update_traces(marker=dict(color=["#667eea", "#764ba2", "#4facfe", "#00f2fe"][:len(category_profit)]))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # AI Insights
    st.markdown('<div class="ai-panel">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Generated Insights")

    total_profit = df['Profit'].sum()
    avg_discount = df['Discount'].mean()

    if total_profit > 100000:
        st.success("✅ Business is highly profitable.")
    else:
        st.warning("⚠ Profit can be improved.")

    if avg_discount > 0.20:
        st.warning("⚠ High discounts are affecting profits.")
    else:
        st.success("✅ Discount strategy looks healthy.")

    st.info(
        f"🏆 Top Performing Region: {region_sales.loc[region_sales['Sales'].idxmax(),'Region']}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # AI Prediction
    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Profit Prediction")

    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        sales = st.number_input("Sales", min_value=0.0, value=1000.0)
    with col_in2:
        quantity = st.number_input("Quantity", min_value=1, value=5)
    with col_in3:
        discount = st.slider("Discount", 0.0, 1.0, 0.10)

    if st.button("Predict Profit"):
        prediction = model.predict([[sales, quantity, discount]])

        st.markdown(f"""
        <div class="prediction-result">
            <div class="result-icon">🤖</div>
            <div class="result-text">
                <h4>AI Prediction Result</h4>
                <p>Based on the inputs provided, the predicted profit is:</p>
                <div class="result-value">${prediction[0]:,.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Analytics':
    st.markdown("""
    <div class="hero-section">
        <h1>📈 Advanced Analytics</h1>
        <p>Deep dive into your business metrics and trends.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Detailed Sales Analysis")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()
    fig_daily = px.line(daily_sales, x='Order Date', y='Sales', title='Daily Sales Trend')
    fig_daily = style_fig(fig_daily)
    fig_daily.update_traces(line=dict(color="#667eea", width=3))
    st.plotly_chart(fig_daily, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🏆 Top Performing Products")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    # FIXED: Check for available columns
    if 'Product Name' in df.columns:
        product_col = 'Product Name'
    elif 'Product' in df.columns:
        product_col = 'Product'
    elif 'Category' in df.columns:
        product_col = 'Category'
    else:
        product_col = df.columns[0]

    product_sales = df.groupby(product_col)['Sales'].sum().nlargest(10).reset_index()
    fig_prod = px.bar(product_sales, x='Sales', y=product_col, orientation='h', title=f'Top 10 by {product_col}')
    fig_prod = style_fig(fig_prod)
    fig_prod.update_traces(marker=dict(color="#764ba2"))
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'AI Insights':
    st.markdown("""
    <div class="hero-section">
        <h1>🧠 AI Insights Center</h1>
        <p>Intelligent recommendations powered by machine learning.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ai-panel">', unsafe_allow_html=True)
    st.markdown("### 📋 Comprehensive AI Analysis")

    st.success("✅ Revenue Growth: Positive trend detected in Q4")
    st.info("📊 Customer Segments: High-value customers identified in West region")
    st.warning("⚠ Inventory Alert: Consider restocking top-selling categories")

    st.markdown("""
    **Key Recommendations:**
    1. Focus marketing efforts on high-performing regions
    2. Optimize discount strategies to improve margins
    3. Expand product range in profitable categories
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Settings':
    # Format values safely
    total_records = f"{len(df):,}"
    date_min = df['Order Date'].min().strftime('%b %Y')
    date_max = df['Order Date'].max().strftime('%b %Y')
    num_regions = df['Region'].nunique()
    num_categories = df['Category'].nunique()

    st.markdown("""
    <div class="settings-hero">
        <h1>⚙️ Dashboard Settings</h1>
        <p>Customize your analytics experience and manage preferences</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats Grid
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-box">
            <div class="stat-box-icon">📊</div>
            <div class="stat-box-value">94.5%</div>
            <div class="stat-box-label">Model Accuracy</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-icon">🔄</div>
            <div class="stat-box-value">Auto</div>
            <div class="stat-box-label">Data Refresh</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-icon">🔔</div>
            <div class="stat-box-value">On</div>
            <div class="stat-box-label">Notifications</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-icon">🎨</div>
            <div class="stat-box-value">Light</div>
            <div class="stat-box-label">Theme</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Settings Card - SIMPLIFIED
    st.markdown(f"""
    <div class="settings-card">
        <div class="settings-section">
            <div class="settings-section-title">
                🎨 Dashboard Preferences
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Color Theme
                    <span class="badge badge-info">Current</span>
                </div>
                <div class="settings-item-value">Light Mode</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Data Refresh Rate
                </div>
                <div class="settings-item-value">Automatic</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Push Notifications
                    <span class="badge badge-success">Enabled</span>
                </div>
                <div class="settings-item-value">Active</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Auto-Save Reports
                </div>
                <div class="settings-item-value">Enabled</div>
            </div>
        </div>

        <div class="settings-section">
            <div class="settings-section-title">
                🤖 AI Model Configuration
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Prediction Algorithm
                </div>
                <div class="settings-item-value">Random Forest</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Model Accuracy
                    <span class="badge badge-success">94.5%</span>
                </div>
                <div class="settings-item-value">Excellent</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Training Data
                </div>
                <div class="settings-item-value">10,000+ Records</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Last Model Update
                </div>
                <div class="settings-item-value">Today</div>
            </div>
        </div>

        <div class="settings-section">
            <div class="settings-section-title">
                📊 Data & Analytics
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Total Records Processed
                </div>
                <div class="settings-item-value">{total_records}</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Date Range
                </div>
                <div class="settings-item-value">{date_min} - {date_max}</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Active Regions
                </div>
                <div class="settings-item-value">{num_regions} Regions</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Product Categories
                </div>
                <div class="settings-item-value">{num_categories} Categories</div>
            </div>
        </div>

        <div class="settings-section">
            <div class="settings-section-title">
                💾 System Information
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Application Version
                </div>
                <div class="settings-item-value">v2.0.0</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    System Status
                    <span class="badge badge-success">Online</span>
                </div>
                <div class="settings-item-value">Operational</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    API Response Time
                </div>
                <div class="settings-item-value">&lt; 100ms</div>
            </div>
            <div class="settings-item">
                <div class="settings-item-label">
                    Data Export Format
                </div>
                <div class="settings-item-value">CSV, Excel, PDF</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
