# 🚀 InsightGen – GenAI Analytics Dashboard

**Transform Natural Language into Data Insights**

InsightGen is an intelligent analytics dashboard that empowers users to explore and analyze structured datasets using plain English queries. Powered by Google's Gemini AI, it automatically converts natural language questions into SQL queries, executes them safely, and presents results through interactive visualizations and AI-generated insights.

**Stop writing SQL. Start asking questions.**

---

## ✨ Key Features

- 🧠 **Natural Language Queries** - Ask questions in plain English instead of writing SQL
- 🔍 **AI-Powered SQL Generation** - Gemini AI automatically generates optimal SQL queries
- 🛡️ **Secure Execution** - Strict query validation prevents harmful operations (only SELECT queries allowed)
- 📂 **CSV & Excel Support** - Upload custom datasets and analyze them instantly
- 📊 **Auto Schema Detection** - Automatically detects and understands your data structure
- 📈 **Interactive Visualizations** - Beautiful Plotly charts that adapt to your data
- 🎯 **Smart Chart Selection** - AI chooses the best visualization for your data
- 📝 **Query Explanations** - Understand exactly what SQL was generated
- 💡 **AI Insights** - Get analytical interpretations of your query results
- 🔄 **Conversation Memory** - Ask follow-up questions with full context
- 🖥️ **Responsive Dashboard** - Modern, user-friendly Streamlit interface

---

## 📸 Screenshots & Demo

### Dashboard Overview - Main Interface
![InsightGen Dashboard](InsightGen/screenshots/Dashboard.png)
*Main dashboard interface with natural language query input area, sample data loaded, and navigation sidebar*

### Query Results with Visualizations
![Query Results](InsightGen/screenshots/B.png)

![Query Results](InsightGen/screenshots/C.png)

![Query Results](InsightGen/screenshots/D.png)

![Query Results](InsightGen/screenshots/E.png)
*Automatic chart generation showing query results with interactive Plotly visualizations*

### Data Upload Feature
![Data Upload](InsightGen/screenshots/F.png)
*Easy dataset upload interface supporting CSV and Excel files with auto-schema detection*

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)               │
│              Upload Data | Ask Questions | View Results     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              QUERY PROCESSING PIPELINE                      │
├──────────────────────────────────────────────────────────────┤
│  • Schema Analysis        • AI Query Generation             │
│  • Query Validation       • Security Checks                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           DATABASE & VISUALIZATION LAYER                    │
├──────────────────────────────────────────────────────────────┤
│  • SQLite Database        • Plotly Visualizations          │
│  • Pandas Processing      • AI Insights Generation         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧰 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.28.1 |
| **Backend** | Python 3.9+ |
| **Database** | SQLite3 |
| **Data Processing** | Pandas 2.0+ |
| **Visualizations** | Plotly 5.0+ |
| **AI/LLM** | Google Gemini API |
| **Query Validation** | Custom SQL Parser |

---

## 🛠️ Installation Guide

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google Gemini API Key (get it from [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Sansii18/InsightGen.git
cd InsightGen

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r InsightGen/requirements.txt

# 4. Setup environment variables
cd InsightGen
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 5. Initialize database
python setup_db.py

# 6. Run the application
streamlit run app.py
```

Open your browser to `http://localhost:8501`

---

## 📖 How to Use

### Basic Workflow

1. **Open the Dashboard** at `http://localhost:8501`
2. **Enter Your Question** in natural language
3. **View Results** with automatic visualizations
4. **Upload Your Data** to analyze custom datasets
5. **Ask Follow-ups** with full context awareness

### Example Queries

```
• Category wise total sales
• Top 5 products by revenue
• Monthly sales trend
• Average order value by category
• Revenue distribution across products
• Number of orders per month
• Best performing category
• Sales growth year over year
```

---

## 📁 Project Structure

```
InsightGen/
├── app.py                      # Main application
├── setup_db.py                # Database setup
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── sales.db                   # SQLite database
├── screenshots/               # Demo screenshots
│   ├── Screenshot 2026-04-02 at 3.50.16 PM.png
│   ├── Screenshot 2026-04-02 at 3.52.38 PM.png
│   ├── Screenshot 2026-04-02 at 3.53.31 PM.png
│   ├── Screenshot 2026-04-02 at 3.55.10 PM.png
│   └── Screenshot 2026-04-02 at 3.55.36 PM.png
│
├── chart_utils.py            # Visualization utilities
├── schema_utils.py           # Schema analysis
├── memory_utils.py           # Conversation memory
├── sql_validator.py          # Query validation
└── README.md                 # Documentation
```

---

## 🔒 Security & Safety

InsightGen implements multiple security layers:

### Query Validation
- ✅ Only SELECT queries are executed
- ❌ Blocks dangerous operations: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE

### Additional Protections
- SQL injection prevention through parameterized queries
- Safe error handling without exposing database details
- User input validation and sanitization

---

## 💡 Example Use Cases

- **Business Intelligence** - Quick ad-hoc analysis without data teams
- **Data Exploration** - Exploratory data analysis (EDA) and pattern discovery
- **Decision Making** - Quick data-driven insights for strategic decisions
- **Education** - Learning SQL through AI-generated examples

---

## ⚙️ Configuration

### Environment Variables

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
```

### Getting Gemini API Key

1. Visit [aistudio.google.com](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Create new API key
4. Copy and paste into `.env` file

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | Ensure `.env` file exists with valid key |
| "No such table: sales" | Run `python setup_db.py` |
| Port in use | Change port: `streamlit run app.py --server.port 8502` |
| Import errors | Run `pip install -r requirements.txt --upgrade` |

---

## 📊 Sample Queries & Results

```
Query: "Show me total sales by category"
Result: Bar chart with category breakdown and AI insights

Query: "What's the sales trend over months?"
Result: Line chart showing sales progression with trend analysis

Query: "Which products are top performers?"
Result: Ranked list with visualizations and performance metrics
```

---

## 🚀 Advanced Features

### Conversation Memory
- Remembers previous queries and results
- Understands context for follow-up questions
- Enables multi-step analysis workflows

### Auto-Chart Selection
- Time series → Line charts
- Categories → Bar charts
- Distribution → Histograms
- Relationships → Scatter plots

### Schema Intelligence
- Automatic data type detection
- Relationship understanding
- Column availability tracking
- Data range analysis

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Support for more data sources (PostgreSQL, MySQL, etc.)
- [ ] Multi-language support
- [ ] Advanced data cleaning features
- [ ] Export results to PDF/Excel
- [ ] Scheduled reports
- [ ] Real-time data federation

---

## 📜 License

This project is open source. Please see LICENSE file for details.

---

## 👤 Author

**Sanskar Sansii**
- GitHub: [@Sansii18](https://github.com/Sansii18)
- Project: [InsightGen Repository](https://github.com/Sansii18/InsightGen)

---

## ⭐ Support

If you find InsightGen useful:
- Give it a ⭐ on GitHub
- Share it with your network
- Report issues and suggest features
- Contribute improvements

---

## 🔗 Useful Links

- [GitHub Repository](https://github.com/Sansii18/InsightGen)
- [Google Gemini API](https://aistudio.google.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Charts](https://plotly.com/python/)

---
