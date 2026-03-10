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
# CUSTOM CSS STYLING FOR MODERN DASHBOARD
# =====================================================================

DASHBOARD_CSS = """
<style>
    /* Main container padding and background */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        color: white;
    }
    
    .header-subtitle {
        font-size: 1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
        color: white;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    /* Section containers */
    .section-container {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #1a1a1a;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Input styling */
    .query-input {
        border: 2px solid #e0e0e0;
        border-radius: 6px;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .query-input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 6px;
    }
    
    /* Insights styling */
    .insights-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    .insight-item {
        padding: 0.75rem 0;
        font-size: 1rem;
        color: #1a1a1a;
        line-height: 1.6;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Responsive layout */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }
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
    return sqlite3.connect("sales.db")

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
    st.markdown("## 📁 Dataset Management")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"],
        help="Upload your dataset to replace the default sales data"
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
    st.markdown("### 📊 Dataset Info")
    
    col1, col2 = st.columns(2)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", df.shape[1])
    
    st.markdown("**Column Types:**")
    dtype_info = df.dtypes.astype(str)
    for col, dtype in dtype_info.items():
        st.caption(f"• `{col}`: {dtype}")

# =====================================================================
# MAIN CONTENT: HEADER
# =====================================================================

st.markdown("""
<div class="header-container">
    <h1 class="header-title">📊 InsightGen</h1>
    <p class="header-subtitle">AI-Powered Analytics Dashboard | Ask questions, get insights instantly</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# KPI METRICS ROW
# =====================================================================

schema_str = generate_schema_string(df, table_name="dataset")

# Calculate KPIs
kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric(
        "📈 Total Rows",
        f"{df.shape[0]:,}",
        help="Number of records in the dataset"
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
            "📊 Avg Value",
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
</div>
""", unsafe_allow_html=True)

query_col1, query_col2 = st.columns([4, 1])

with query_col1:
    user_question = st.text_input(
        "Enter a business question",
        placeholder="e.g., Show me the top 5 products by revenue...",
        label_visibility="collapsed"
    )

with query_col2:
    generate_btn = st.button("🚀 Generate", use_container_width=True)

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
    <h2 class="section-title">📝 Generated Query</h2>
</div>
""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.expander("📋 View SQL Query", expanded=True):
                st.code(sql_query, language="sql")
        
        with col2:
            with st.expander("💡 Query Explanation"):
                if sql_query.startswith("-- ERROR"):
                    st.error(sql_query)
                else:
                    explanation = generate_sql_explanation(sql_query)
                    st.markdown(explanation)

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
</div>
""", unsafe_allow_html=True)

        # Create chart
        fig = generate_chart(df_result)
        
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ No suitable chart available for this result.")

        # Data Table
        st.markdown("**📑 Data Table:**")
        st.dataframe(df_result, use_container_width=True)

        # ================================================================
        # AI INSIGHTS SECTION
        # ================================================================
        
        st.markdown("---")
        st.markdown("""
<div class="insights-container">
    <h3 style="color: #667eea; margin-top: 0;">✨ AI-Generated Insights</h3>
</div>
""", unsafe_allow_html=True)

        insights_text = generate_insights(df_result)
        
        # Parse insights and display nicely
        insights_lines = insights_text.split("\n")
        for line in insights_lines:
            if line.strip():
                st.markdown(f"<div class='insight-item'>{line}</div>", unsafe_allow_html=True)

# =====================================================================
# FOOTER
# =====================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #888;">
    <p>🚀 InsightGen – Powered by Google Gemini | Built with Streamlit & SQLite</p>
    <p style="font-size: 0.85rem;">© 2026 InsightGen Analytics</p>
</div>
""", unsafe_allow_html=True)
