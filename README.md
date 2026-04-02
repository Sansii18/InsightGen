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

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sansii18/InsightGen.git
cd InsightGen
```

### Step 2: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the `InsightGen` directory:

```bash
cd InsightGen
```

Create `.env` file with:

```env
# Gemini API Key - Get it from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_actual_api_key_here

# Optional Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
```

**⚠️ Important:** Replace `your_actual_api_key_here` with your actual Gemini API key.

### Step 5: Initialize Database (Optional)

To populate the dashboard with sample sales data:

```bash
python setup_db.py
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

---

## 📖 How to Use

### Basic Workflow

1. **Open the Dashboard**
   - Navigate to `http://localhost:8501`
   - The app loads with sample sales data by default

2. **Enter Your Question**
   - Type a business question in natural language
   - Examples:
     - "What are the top 5 products by revenue?"
     - "Show me monthly sales trends"
     - "How many orders do we have by category?"
     - "What's the average order value?"

3. **View Results**
   - AI generates and validates the SQL query
   - Query executes on your database
   - Results display with automatic visualizations
   - AI insights explain what you're looking at

4. **Upload Your Own Data**
   - Click "Upload Dataset" in the sidebar
   - Select CSV or Excel file
   - System automatically detects schema
   - Start querying your data immediately

### Example Queries

```
Category wise total sales
Top 5 products by revenue
Monthly sales trend
Average order value by category
Revenue distribution across products
Number of orders per month
Best performing category
Sales growth year over year
```

---

## 📁 Project Structure

```
InsightGen/
├── app.py                 # Main Streamlit application
├── setup_db.py           # Database initialization script
├── requirements.txt      # Python dependencies
├── requirements-minimal.txt  # Lightweight dependencies
├── .env                  # Environment variables (create this)
├── sales.db             # SQLite database (auto-generated)
│
├── chart_utils.py       # Chart generation utilities
├── schema_utils.py      # Database schema analysis
├── memory_utils.py      # Conversation memory management
├── sql_validator.py     # SQL safety validation
│
├── README.md            # Project documentation
└── .gitignore          # Git ignore rules
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main application entry point with UI and orchestration |
| `chart_utils.py` | Functions for intelligent chart generation based on data |
| `schema_utils.py` | Analyzes database schema and generates context |
| `memory_utils.py` | Manages conversation history for context-aware queries |
| `sql_validator.py` | Validates SQL queries for safety |
| `setup_db.py` | Creates and populates sample database |

---

## 📸 Screenshots & Demo

### Dashboard Overview - Main Interface

![InsightGen Dashboard Interface](screenshots/Screenshot%202026-04-02%20at%203.50.16%20PM.png)

*Main dashboard interface showing natural language query input area, sample sales data loaded, and interactive navigation sidebar*

### Query Results with Visualizations

![Query Results](screenshots/Screenshot%202026-04-02%20at%203.52.38%20PM.png)

*Automatic chart generation showing query results with interactive Plotly visualizations*

### AI-Generated Insights

![AI Insights](screenshots/Screenshot%202026-04-02%20at%203.53.31%20PM.png)

*AI-powered insights and analysis of query results with business-friendly interpretations*

### Data Upload Feature

![Data Upload](screenshots/Screenshot%202026-04-02%20at%203.55.10%20PM.png)

*Easy dataset upload interface supporting CSV and Excel files with auto-schema detection*

### Advanced Query Interface

![Advanced Query](screenshots/Screenshot%202026-04-02%20at%203.55.36%20PM.png)

*Query history, conversation memory, and refined result display with multiple visualization options*

---

## 🔒 Security & Safety

InsightGen implements multiple security layers:

### Query Validation
- ✅ Only SELECT queries are executed
- ❌ Blocks dangerous operations:
  - `INSERT` - Prevent data insertion
  - `UPDATE` - Prevent data modification
  - `DELETE` - Prevent data deletion
  - `DROP` - Prevent table deletion
  - `ALTER` - Prevent schema changes
  - `TRUNCATE` - Prevent data clearing

### Additional Protections
- SQL injection prevention through parameterized queries
- Rate limiting on API calls
- Safe error handling without exposing database details
- User input validation and sanitization

---

## 💡 Example Use Cases

### Business Intelligence
- Quick ad-hoc analysis without data teams
- Real-time business metrics
- Customer insights and KPI tracking

### Data Exploration
- Exploratory data analysis (EDA)
- Pattern discovery in large datasets
- Hypothesis testing

### Decision Making
- Quick data-driven insights
- Support for strategic decisions
- Real-time reporting

### Education
- Learning SQL through AI-generated examples
- Understanding data relationships
- Data literacy improvement

---

## 🚀 Advanced Features

### Conversation Memory
The system remembers previous queries and results, allowing follow-up questions:
```
User: "What are top products?"
AI: Shows top 5 products by revenue

User: "Show me sales trend for the top product"
AI: Understands context and analyzes top product over time
```

### Auto-Chart Selection
Intelligent visualization selection based on data types:
- Time series → Line charts
- Categories → Bar charts
- Distribution → Histograms
- Relationships → Scatter plots

### Schema Intelligence
Automatic understanding of:
- Data types
- Relationships
- Available columns
- Data ranges and distributions

---

## ⚙️ Configuration

### Environment Variables

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
STREAMLIT_SERVER_PORT=8501          # Port to run app on
STREAMLIT_SERVER_HEADLESS=false     # Run without browser opening
STREAMLIT_LOGGER_LEVEL=info        # Logging level
```

### Database Configuration

By default, the app uses SQLite with `sales.db`. To use a different database:

1. Modify `get_connection()` in `app.py`
2. Update connection string
3. Ensure schema is compatible

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:**
- Ensure `.env` file exists in the InsightGen directory
- Check API key is correctly set
- Reload the app after updating `.env`

### Issue: "No such table: sales"
**Solution:**
```bash
cd InsightGen
python setup_db.py
```

### Issue: Port already in use
**Solution:**
```bash
# Change port in .env or run on different port
streamlit run app.py --server.port 8502
```

### Issue: Import errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📊 Sample Queries & Results

### Sales by Category
```
Query: "Show me total sales by category"
Result: Bar chart with category breakdown
```

### Monthly Trends
```
Query: "What's the sales trend over months?"
Result: Line chart showing sales over time
```

### Product Performance
```
Query: "Which products are top performers?"
Result: Ranked list with visualizations
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Support for more data sources (PostgreSQL, MySQL, etc.)
- [ ] Multi-language support
- [ ] Advanced data cleaning features
- [ ] Export results to PDF/Excel
- [ ] Scheduled reports
- [ ] Real-time data federation

---

## 📝 API Documentation

### Key Functions

#### `load_default_data()`
Loads the built-in sales dataset.

#### `run_query(sql: str, version: int) -> pd.DataFrame`
Executes SQL query and returns results.

#### `generate_chart(df: pd.DataFrame, title: str)`
Auto-generates appropriate visualization for data.

#### `generate_sql_explanation(sql: str) -> str`
Explains what the SQL query does in plain English.

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLite Tutorial](https://www.sqlite.org/docs.html)
- [Google Gemini API](https://ai.google.dev/)
- [Plotly Documentation](https://plotly.com/python/)

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

## 🔗 Links

- [GitHub Repository](https://github.com/Sansii18/InsightGen)
- [Google Gemini API](https://aistudio.google.com/)
- [Streamlit App Hosting](https://streamlit.io/cloud)

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

## 🎯 Roadmap

### v1.1
- [ ] Multi-dataset federation
- [ ] Advanced filtering options
- [ ] Custom visualization library

### v1.2
- [ ] Real-time data streaming
- [ ] Scheduled report generation
- [ ] User authentication

### v2.0
- [ ] Support for NoSQL databases
- [ ] Advanced ML features
- [ ] Enterprise deployment options

---

**Made with ❤️ for data enthusiasts and business analysts**

*Last Updated: April 2, 2026*
