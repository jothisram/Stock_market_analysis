# 📈 Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends

A comprehensive **Nifty 50 Stock Performance Dashboard** built with Python, Streamlit, and Power BI — designed to help investors, analysts, and enthusiasts make data-driven decisions through interactive visualizations and deep market insights.

---

## 🚀 Project Overview

This project analyzes **daily stock data (Open, Close, High, Low, Volume)** for all 50 Nifty stocks over the past year. Raw data provided in YAML format is extracted, cleaned, transformed into structured CSVs, loaded into a SQL database, and finally visualized through interactive dashboards.

**Domain:** Finance / Data Analytics

---

## 🎯 Business Use Cases

- **Stock Performance Ranking** — Identify the top 10 best-performing (green) and worst-performing (red) stocks over the year.
- **Market Overview** — Summarize overall market performance including average price, average volume, and green vs. red stock ratio.
- **Investment Insights** — Spot stocks with consistent growth or significant declines at a glance.
- **Decision Support** — Understand volatility, sector trends, and correlations useful for both retail and institutional traders.

---

## 🛠️ Tech Stack

| Layer | Tools / Libraries |
|---|---|
| Language | Python 3.x |
| Data Processing | Pandas, PyYAML |
| Database | MySQL / PostgreSQL, SQLAlchemy |
| Visualization | Matplotlib, Seaborn, Power BI |
| Dashboard | Streamlit |
| Standards | PEP 8 |

---

## 📂 Project Structure

```
data-driven-stock-analysis/
│
├── data/
│   ├── raw/                  # YAML files organized by month/date
│   ├── processed/            # 50 CSV files (one per Nifty 50 symbol)
│   └── sector_data.csv       # Sector mapping for each stock
│
├── scripts/
│   ├── extract_transform.py  # YAML → CSV extraction
│   ├── data_cleaning.py      # Data validation and cleaning
│   ├── db_loader.py          # Load CSVs into SQL database
│   └── analysis.py           # Key metrics and visualizations
│
├── streamlit_app/
│   └── app.py                # Streamlit interactive dashboard
│
├── powerbi/
│   └── stock_dashboard.pbix  # Power BI dashboard file
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Workflow & Execution

### Step 1 — Clone the Repository
```bash
git clone https://github.com/your-username/data-driven-stock-analysis.git
cd data-driven-stock-analysis
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Extract & Transform Data (YAML → CSV)
```bash
python scripts/extract_transform.py
```
> This reads the YAML data organized by month/date and outputs **50 CSV files** (one per Nifty 50 symbol) into `data/processed/`.

### Step 4 — Clean the Data
```bash
python scripts/data_cleaning.py
```

### Step 5 — Load Data into SQL Database
```bash
python scripts/db_loader.py
```
> Configure your DB credentials in a `.env` file before running.

### Step 6 — Run Analysis & Generate Visualizations
```bash
python scripts/analysis.py
```

### Step 7 — Launch the Streamlit Dashboard
```bash
streamlit run streamlit_app/app.py
```

---

## 📊 Analysis & Visualizations

### 1. 🔥 Volatility Analysis
- Calculates **standard deviation of daily returns** for each stock.
- Daily return formula: `(Close - Previous Close) / Previous Close`
- Bar chart showing the **Top 10 Most Volatile Stocks**.

### 2. 📈 Cumulative Return Over Time
- Tracks running cumulative return for each stock throughout the year.
- Line chart for the **Top 5 Best-Performing Stocks**.

### 3. 🏭 Sector-wise Performance
- Maps each stock to its sector using `sector_data.csv`.
- Bar chart showing **Average Yearly Return by Sector**.

### 4. 🔗 Stock Price Correlation
- Computes correlation matrix using `pandas.DataFrame.corr()`.
- **Heatmap** visualizing relationships between closing prices of all stocks.

### 5. 📅 Top 5 Gainers & Losers (Month-wise)
- Monthly percentage return calculated for each stock.
- 12 bar charts (one per month) showing **Top 5 Gainers and Losers**.

---

## 📦 Project Deliverables

- ✅ **SQL Database** — Clean, processed, query-optimized stock data
- ✅ **Python Scripts** — Modular scripts for ETL, analysis, and DB interaction
- ✅ **Power BI Dashboard** — Interactive visual reports
- ✅ **Streamlit Application** — Real-time, browser-based stock dashboard

---

## 🗃️ Dataset

The dataset contains daily OHLCV data for all 50 Nifty stocks, organized in YAML format by month and date.

📁 [Access Dataset](https://drive.google.com/drive/folders/1dfLGdGNeHmkuf4-7jZT6KYl6aU-t2v6M?usp=sharing)

---

## 📋 Results

- A fully functional dashboard showing top-performing and worst-performing stocks over the last year.
- Clear market overview with green vs. red stock indicators.
- Interactive Power BI and Streamlit dashboards for accessible, real-time analysis.

---

## 📌 Coding Standards

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python coding standards:
- Consistent naming conventions
- Modular and reusable functions
- Well-documented code with inline comments
- Optimized SQL queries for large datasets

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Jothisram R**
- 💼 [LinkedIn](https://www.linkedin.com/in/jothisram-r-2877b728b/)
- 🐙 [GitHub](https://github.com/jothisram)
