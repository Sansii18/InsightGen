\# InsightGen – GenAI Dashboard Generator



InsightGen is a GenAI-powered dashboard generator that converts natural language business questions into SQL queries, executes them safely, visualizes results, and generates business insights.



\## Features

\- Natural language to SQL using Gemini
- File upload (CSV/Excel) with dynamic dataset handling
- Automatic schema detection from uploaded or default data
- Enhanced charting with Plotly and smart chart selection
- Conversation memory for follow-up questions
- SQL explanations and AI-generated business insights
- Strong SQL validation (SELECT-only, blocking DML/DDL)
- Streamlit-based UI with sidebar and caching




\## Tech Stack

\- Python

\- Streamlit

\- SQLite

\- Google Gemini (GenAI)

\- Pandas



\## Setup Instructions

1\. Clone the repository

2\. Create a `.env` file

3\. Add:

&nbsp;  GEMINI\_API\_KEY=your\_api\_key\_here

4\. Install dependencies:

&nbsp;  pip install -r requirements.txt

5\. Run the app:

&nbsp;  streamlit run app.py

6\. (Optional) Upload your own dataset via the sidebar. Supported formats are CSV and Excel. If you upload a file it will replace the default sales data and be used for subsequent queries.



\## Sample Queries

\- Category wise total sales

\- Top 5 products by revenue

\- Monthly sales trend



