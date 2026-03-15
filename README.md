🚀 InsightGen – GenAI Analytics Dashboard

InsightGen is a natural language analytics dashboard that enables users to explore and analyze structured datasets using plain English queries. The application converts user questions into SQL queries, executes them safely on a dataset, and presents the results through interactive visualizations and analytical insights.

The goal of InsightGen is to simplify data exploration by allowing users to interact with their data without needing to manually write SQL queries.

**✨ Features**

🧠 Natural language interface for querying datasets

🔍 Automatic SQL query generation using a large language model

🛡️ Secure SQL execution with strict query validation

📂 Support for uploading custom datasets (CSV and Excel)

📊 Automatic schema detection from uploaded data

📈 Interactive visualizations using Plotly

🎯 Smart chart selection based on dataset structure

📝 SQL query explanations for better transparency

💡 AI-generated analytical insights from query results

🔄 Conversation memory for follow-up queries

🖥️ Streamlit-based responsive dashboard interface


**🧰 Technology Stack**

**Backend**

🐍 Python

🗄️ SQLite

📑 Pandas

**Frontend**

🎛️ Streamlit

📊 Plotly

**AI Integration**

🤖 Google Gemini API


**⚙️ How It Works**

1️⃣ The user enters a business question in natural language.

2️⃣ The system analyzes the dataset schema.

3️⃣ The query and schema are sent to the language model.

4️⃣ The model generates a SQL query.

5️⃣ The query is validated to ensure it is safe to execute.

6️⃣ The query is executed against the dataset.

7️⃣ Results are processed and visualized through interactive charts.

8️⃣ Additional insights and explanations are generated to help interpret the data.

**🏗️ System Architecture**
<img width="6128" height="327" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/46a93820-8875-4527-88b2-e89089fa6160" />

The system follows a modular pipeline where natural language queries are transformed into SQL queries, executed on a dataset, and returned with visualizations and insights.

🛠️ Setup Instructions

1️⃣ Clone the repository 

git clone https://github.com/<your-username>/InsightGen.git
cd InsightGen

2️⃣ Create environment file
(Create a .env file in the root directory)

GEMINI_API_KEY=your_api_key_here

3️⃣ Install dependencies
(pip install -r requirements.txt)

4️⃣ Run the application

streamlit run app.py

**📂 Dataset Support**

InsightGen supports both default datasets and user-uploaded datasets.
Users can upload datasets directly from the sidebar.

**Supported formats:**
CSV, Excel (.xlsx).
After uploading, the application automatically detects the dataset schema and uses it for query generation and visualization.

💬 Example Queries:

-> Category wise total sales

-> Top 5 products by revenue

-> Monthly sales trend

-> Average order value by category

-> Revenue distribution across products

**📁 Project Structure**

InsightGen

│

├── app.py

├── chart_utils.py

├── schema_utils.py

├── memory_utils.py

├── sql_validator.py

├── requirements.txt

├── README.md

🔒 Security Considerations

To ensure safe database interaction, the system includes strict SQL validation rules.

The application blocks queries containing operations such as:
INSERT,
UPDATE, 
DELETE, 
DROP, 
ALTER, 
TRUNCATE

**Only read-only SELECT queries are executed.**

⭐ If you found this project interesting, consider giving the repository a star.
