import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai

from schema_utils import generate_schema_string
from chart_utils import generate_chart
from memory_utils import init_memory, update_memory, get_context_prompt
from sql_validator import is_safe_sql

# =====================================================================
# CUSTOM CSS STYLING FOR PREMIUM MODERN DASHBOARD
# =====================================================================

DASHBOARD_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Root color variables for dark/light mode */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --accent-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --border-color: #475569;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 100%);
        color: var(--text-primary);
    }
    
    body {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 100%);
        color: var(--text-primary);
    }
    
    /* Header Section */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 25px -5px rgba(102, 126, 234, 0.3),
            0 8px 10px -2px rgba(102, 126, 234, 0.2),
            inset 0 1px 1px rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(30px, -30px) rotate(5deg); }
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        margin-top: 0.75rem;
        opacity: 0.95;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.4) 100%);
        padding: 1.75rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 
            0 10px 30px -5px rgba(0, 0, 0, 0.3),
            inset 0 1px 1px rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 
            0 20px 40px -5px rgba(102, 126, 234, 0.3),
            inset 0 1px 1px rgba(255, 255, 255, 0.1);
    }
    
    /* Section Containers */
    .section-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(51, 65, 85, 0.3) 100%);
        padding: 2.25rem;
        border-radius: 14px;
        margin-bottom: 2rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 
            0 15px 40px -5px rgba(0, 0, 0, 0.3),
            inset 0 1px 1px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    
    .section-container:hover {
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 
            0 20px 50px -5px rgba(102, 126, 234, 0.2),
            inset 0 1px 1px rgba(255, 255, 255, 0.08);
    }
    
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 1.75rem;
        color: #f1f5f9;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-bottom: 2px solid;
        border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
        padding-bottom: 0.75rem;
        letter-spacing: -0.3px;
    }
    
    /* Input Styling */
    .streamlit-textinput input {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-textinput input:focus {
        border-color: #667eea !important;
        background-color: rgba(102, 126, 234, 0.1) !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2) !important;
        outline: none !important;
    }
    
    .streamlit-textinput input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 10px 25px -5px rgba(102, 126, 234, 0.4),
            0 4px 6px -2px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.3px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 15px 35px -5px rgba(102, 126, 234, 0.5),
            0 8px 12px -2px rgba(0, 0, 0, 0.4);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        padding: 12px 16px;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #cbd5e1;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    /* Insights Container */
    .insights-container {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid rgba(79, 172, 254, 0.3);
        box-shadow: 
            0 10px 30px -5px rgba(79, 172, 254, 0.2),
            inset 0 1px 1px rgba(255, 255, 255, 0.1);
    }
    
    .insight-item {
        padding: 0.9rem 0;
        font-size: 1.05rem;
        color: #cbd5e1;
        line-height: 1.7;
        transition: all 0.3s ease;
        padding-left: 1rem;
        border-left: 3px solid transparent;
        border-image: linear-gradient(180deg, #667eea, #764ba2) 1;
    }
    
    .insight-item:hover {
        color: #f1f5f9;
        padding-left: 1.3rem;
    }
    
    /* Table Styling */
    .stDataFrame {
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame [data-testid="stDataFrameContainer"] {
        background-color: rgba(30, 41, 59, 0.4) !important;
    }
    
    /* Code Block Styling */
    .stCodeBlock {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 10px !important;
    }
    
    code {
        background: rgba(102, 126, 234, 0.15) !important;
        color: #f1f5f9 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [style*="flex-direction"] > button {
        width: 100%;
    }
    
    /* File Uploader Styling */
    .uploadedFile {
        background: rgba(79, 172, 254, 0.1) !important;
        border: 2px dashed rgba(79, 172, 254, 0.5) !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    /* Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px !important;
        border-left: 4px solid !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSuccess {
        background: rgba(79, 172, 254, 0.15) !important;
        border-color: #4facfe !important;
        color: #60a5fa !important;
    }
    
    .stError {
        background: rgba(245, 87, 108, 0.15) !important;
        border-color: #f5576c !important;
        color: #ff6b7a !important;
    }
    
    .stWarning {
        background: rgba(250, 112, 154, 0.15) !important;
        border-color: #fa709a !important;
        color: #ff8fa3 !important;
    }
    
    .stInfo {
        background: rgba(102, 126, 234, 0.15) !important;
        border-color: #667eea !important;
        color: #93a5ff !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: #667eea !important;
    }
    
    /* Dividers */
    .divider {
        border-color: rgba(148, 163, 184, 0.3);
        margin: 2rem 0;
    }
    
    /* Responsive Layout */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .header-container {
            padding: 1.5rem;
        }
        
        .section-container {
            padding: 1.5rem;
        }
        
        .section-title {
            font-size: 1.3rem;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #667eea);
    }
    
    /* Animation for loading state */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Tooltip and Help text */
    .streamlit-tooltip {
        background: rgba(30, 41, 59, 0.95) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        color: #cbd5e1 !important;
    }
    
    /* Custom badge styling */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-right: 0.5rem;
    }
</style>
"""

# =====================================================================
# CONFIG & INITIALIZATION
# =====================================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("🔑 GEMINI_API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="InsightGen – AI Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

# Initialize conversational memory
init_memory()

# Track dataset version to bust cache when user uploads new data
if 'data_version' not in st.session_state:
    st.session_state.data_version = 0

# =====================================================================
# DATABASE HELPERS
# =====================================================================

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), "sales.db")
    return sqlite3.connect(db_path)

@st.cache_data
def load_default_data() -> pd.DataFrame:
    """Load the built-in sales table."""
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM sales", conn)

@st.cache_data
def run_query(sql: str, version: int) -> pd.DataFrame:
    """Execute SQL and cache results. The version arg allows cache invalidation."""
    with get_connection() as conn:
        return pd.read_sql(sql, conn)

# =====================================================================
# GENERATIVE AI HELPERS
# =====================================================================

def clean_sql(sql: str) -> str:
    """Remove code fences or markdown around SQL returned by the LLM."""
    return sql.replace("```sql", "").replace("```", "").strip()

def generate_sql(user_question: str, schema: str, context: str = "") -> str:
    """Generate SQL from natural language question."""
    prompt = f"""
You are an expert SQL developer.

{schema}

Rules:
- Generate ONLY a SELECT SQL query
- SQLite compatible SQL
- No explanations, only SQL
"""
    if context:
        prompt += "\n\nPrevious conversation:\n" + context + "\n"
    prompt += f"\nUser question:\n{user_question}\n\nSQL:\n"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return clean_sql(response.text)
    except Exception as e:
        return f"-- ERROR: {str(e)}"

def generate_sql_explanation(sql: str) -> str:
    """Get Gemini to explain a SQL query in business terms."""
    prompt = f"""
You are a business analyst. Explain the following SQL query in simple
business language, one or two sentences, without repeating the query.

SQL:
{sql}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate explanation: {e}"

def generate_insights(df: pd.DataFrame) -> str:
    """Create three short business insights from dataframe."""
    preview = df.head(10).to_string(index=False)
    prompt = f"""
You are a business analyst.

Given this data:
{preview}

Give 3 short business insights in bullet points.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"- Unable to generate insights: {e}"

# =====================================================================
# SIDEBAR: DATASET MANAGEMENT
# =====================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #667eea; font-size: 1.5rem; margin: 0;">⚙️ Settings</h2>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0.5rem 0 0 0;">Manage your data</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📤 Upload Dataset")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"],
        help="📁 Upload your own dataset to replace the default sales data"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            with get_connection() as conn:
                df.to_sql("dataset", conn, if_exists="replace", index=False)
            
            st.success("✅ Dataset uploaded successfully!")
            st.session_state.data_version += 1
        except Exception as e:
            st.error(f"❌ Failed to load file: {e}")
            df = load_default_data()
    else:
        df = load_default_data()
        with get_connection() as conn:
            df.to_sql("dataset", conn, if_exists="replace", index=False)
    
    # Dataset Info Card
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%); 
                border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 1.5rem;">
        <h3 style="color: #667eea; margin: 0 0 1rem 0; display: flex; align-items: center;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">📊</span> Dataset Info
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📈 Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("📋 Columns", df.shape[1])
    
    st.markdown("**Column Types:**")
    dtype_info = df.dtypes.astype(str)
    
    with st.expander("👁️ View All Columns", expanded=False):
        for col, dtype in dtype_info.items():
            dtype_icon = "🔤" if "object" in dtype else "🔢" if "int" in dtype or "float" in dtype else "📅"
            st.caption(f"{dtype_icon} `{col}`: {dtype}")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #94a3b8; font-size: 0.85rem;">
        <p style="margin: 0;">💡 Pro Tip: Upload your own CSV or Excel file to analyze custom data</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# MAIN CONTENT: HEADER
# =====================================================================

st.markdown("""
<div class="header-container">
    <h1 class="header-title">📊 InsightGen</h1>
    <p class="header-subtitle">✨ AI-Powered Analytics Dashboard | Transform data into actionable insights instantly</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# KPI METRICS ROW
# =====================================================================

schema_str = generate_schema_string(df, table_name="dataset")

# Display metrics with enhanced styling
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h3 style="color: #cbd5e1; font-size: 1.3rem; font-weight: 600; letter-spacing: 0.5px;">📈 Key Dataset Metrics</h3>
</div>
""", unsafe_allow_html=True)

# Calculate KPIs
kpi_cols = st.columns(4, gap="large")

with kpi_cols[0]:
    st.metric(
        "📊 Total Records",
        f"{df.shape[0]:,}",
        help="Total number of rows in dataset",
        delta=None
    )

# Try to calculate revenue if price/quantity columns exist
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
if len(numeric_cols) > 0:
    with kpi_cols[1]:
        total_revenue = df[numeric_cols[0]].sum()
        st.metric(
            "💰 Total Value",
            f"{total_revenue:,.0f}",
            help=f"Sum of {numeric_cols[0]}"
        )
    
    with kpi_cols[2]:
        avg_value = df[numeric_cols[0]].mean()
        st.metric(
            "📊 Average Value",
            f"{avg_value:,.0f}",
            help=f"Average of {numeric_cols[0]}"
        )

# Try to show top category if object columns exist
object_cols = df.select_dtypes(include=['object']).columns.tolist()
if len(object_cols) > 0:
    with kpi_cols[3]:
        top_cat = df[object_cols[0]].value_counts().idxmax()
        st.metric(
            "🏆 Top Category",
            str(top_cat)[:20],
            help=f"Most frequent value in {object_cols[0]}"
        )

# =====================================================================
# QUERY INPUT SECTION
# =====================================================================

st.markdown("---")
st.markdown("""
<div class="section-container">
    <h2 class="section-title">🤖 Ask AI a Question</h2>
    <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem;">
        💡 Type any question about your data and we'll generate SQL to find the answer
    </p>
</div>
""", unsafe_allow_html=True)

query_col1, query_col2 = st.columns([4, 1], gap="medium")

with query_col1:
    user_question = st.text_input(
        "Enter a business question",
        placeholder="📌 e.g., Show me the top 5 products by revenue in 2024...",
        label_visibility="collapsed"
    )

with query_col2:
    generate_btn = st.button("🚀 Generate Query", use_container_width=True, key="generate_btn")

# =====================================================================
# PROCESS QUERY
# =====================================================================

if generate_btn:
    if not user_question.strip():
        st.warning("⚠️ Please enter a question first.")
    else:
        context = get_context_prompt()
        
        with st.spinner("🔄 Generating SQL..."):
            sql_query = generate_sql(user_question, schema_str, context)

        # SQL Display Section
        st.markdown("---")
        st.markdown("""
<div class="section-container">
    <h2 class="section-title">📝 Generated Query & Explanation</h2>
</div>
""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            with st.expander("🔍 View SQL Query", expanded=True):
                if sql_query.startswith("-- ERROR"):
                    st.error("❌ SQL generation failed!")
                    st.code(sql_query, language="sql")
                else:
                    st.markdown("""
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(102, 126, 234, 0.3); 
                                 border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;">✅ SQL Query Ready</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(sql_query, language="sql")
        
        with col2:
            with st.expander("💡 Query Explanation", expanded=True):
                if sql_query.startswith("-- ERROR"):
                    st.error(sql_query)
                else:
                    explanation = generate_sql_explanation(sql_query)
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%);
                                 border: 1px solid rgba(79, 172, 254, 0.3); border-radius: 10px; padding: 1.5rem;">
                    """, unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #cbd5e1; line-height: 1.7; font-size: 1rem;'>{explanation}</p>", 
                               unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

        # Validate and Execute
        if sql_query.startswith("-- ERROR"):
            st.error("❌ SQL generation failed. Please try a different question.")
            st.stop()

        if not is_safe_sql(sql_query):
            st.error("❌ Unsafe SQL detected. Only read-only SELECT queries are allowed.")
            st.stop()

        try:
            df_result = run_query(sql_query, st.session_state.data_version)
        except Exception as e:
            st.error(f"❌ SQL execution failed: {e}")
            st.stop()

        if df_result.empty:
            st.warning("⚠️ No data found for this query.")
            st.stop()

        # Update conversation memory
        update_memory(user_question, sql_query, df_result)

        # ================================================================
        # RESULTS SECTION: CHARTS GRID
        # ================================================================
        
        st.markdown("---")
        st.markdown("""
<div class="section-container">
    <h2 class="section-title">📊 Results & Visualization</h2>
    <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1rem;">
        Interactive charts and data tables from your query results
    </p>
</div>
""", unsafe_allow_html=True)

        # Create chart
        fig = generate_chart(df_result)
        
        if fig is not None:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(51, 65, 85, 0.3) 100%);
                         border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
            """, unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("📌 No suitable chart available for this result type.")

        # Data Table
        st.markdown("""
        <div style="margin-top: 1.5rem;">
            <h3 style="color: #cbd5e1; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center;">
                <span style="color: #667eea; margin-right: 0.5rem;">📑</span> Data Table
            </h3>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_result, use_container_width=True)

        # ================================================================
        # AI INSIGHTS SECTION
        # ================================================================
        
        st.markdown("---")
        st.markdown("""
<div class="insights-container">
    <h3 style="color: #4facfe; margin-top: 0; margin-bottom: 1.5rem; display: flex; align-items: center; font-size: 1.4rem;">
        <span style="margin-right: 0.7rem; font-size: 1.5rem;">✨</span> AI-Generated Business Insights
    </h3>
    <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1.5rem;">
        Smart analysis from Google Gemini AI
    </p>
</div>
""", unsafe_allow_html=True)

        insights_text = generate_insights(df_result)
        
        # Parse insights and display nicely
        insights_lines = insights_text.split("\n")
        
        # Create columns for better layout
        for idx, line in enumerate(insights_lines):
            if line.strip():
                # Add numbered badge styling
                st.markdown(f"""
                <div style="margin-bottom: 1rem; padding: 1rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%);
                            border: 1px solid rgba(102, 126, 234, 0.3); border-left: 4px solid rgba(102, 126, 234, 0.8);
                            border-radius: 8px; transition: all 0.3s ease;">
                    <p style="color: #cbd5e1; margin: 0; line-height: 1.6; font-weight: 500;">
                        💡 {line}
                    </p>
                </div>
                """, unsafe_allow_html=True)

# =====================================================================
# FOOTER
# =====================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2.5rem; margin-top: 2rem; 
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            border-top: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px;">
    <h3 style="color: #667eea; margin-top: 0; font-size: 1.2rem; letter-spacing: 0.5px;">
        🚀 InsightGen
    </h3>
    <p style="color: #cbd5e1; margin: 0.5rem 0; font-size: 0.95rem; line-height: 1.6;">
        Powered by <span style="color: #4facfe; font-weight: 600;">Google Gemini AI</span> | 
        Built with <span style="color: #764ba2; font-weight: 600;">Streamlit</span> & 
        <span style="color: #667eea; font-weight: 600;">SQLite</span>
    </p>
    <p style="color: #94a3b8; font-size: 0.85rem; margin: 1rem 0 0 0;">
        © 2026 InsightGen Analytics • Transform Data Into Intelligence
    </p>
</div>
""", unsafe_allow_html=True)
