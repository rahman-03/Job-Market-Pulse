# 📊 Job Market Pulse: Automated ETL Pipeline
A professional-grade data engineering project that automates the collection, cleaning, and analysis of job market data. This tool helps job seekers in Chennai, India, identify tech trends and salary insights in real-time.

## 🚀 Project Overview
This project builds a complete automated pipeline that:
1.  **Extracts** raw job listings from the Adzuna API (filtered for Chennai, India).
2.  **Transforms** data using Python & Pandas (normalizing salaries, deduplicating records, and extracting tech keywords).
3.  **Loads** data into a PostgreSQL cloud database (Supabase) using a 7-day rolling window strategy.
4.  **Exposes** insights via a FastAPI web server with automated daily background synchronization.


## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Data Processing:** Pandas, SQLAlchemy
* **Database:** PostgreSQL (Supabase)
* **API Framework:** FastAPI
* **Automation:** APScheduler
* **Deployment:** Koyeb / Render

## 📋 Key Features
* **Automated Sync:** Runs every 24 hours to keep job listings fresh.
* **Storage Optimized:** Automatically purges records older than 7 days to maintain a clean database and stay within free-tier limits.
* **Smart Deduplication:** Identifies and skips duplicate job IDs to ensure data integrity.
* **Tech Stack Extraction:** Automatically parses job descriptions to identify demand for Python, SQL, AWS, Docker, and more.
* **Live Documentation:** Integrated Swagger UI for testing API endpoints.

## 📡 API Endpoints
* `GET /jobs/latest`: Returns the freshest job listings in Chennai with direct application links.
* `GET /stats/tech`: Analyzes the most in-demand skills in the current local market.
* `GET /run-manual-sync`: Manually triggers the ETL pipeline for immediate data updates.

## ⚙️ Installation & Setup
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/your-username/job-market-pulse.git](https://github.com/your-username/job-market-pulse.git)
    cd job-market-pulse
    ```
2.  **Set up Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    Create a `.env` file and add:
    ```ini
    ADZUNA_APP_ID=your_id
    ADZUNA_APP_KEY=your_key
    DATABASE_URL=postgresql://postgres:[password]@[aws-0-region.pooler.supabase.com:6543/postgres](https://aws-0-region.pooler.supabase.com:6543/postgres)
    ```
5.  **Run the API:**
    ```bash
    uvicorn main:app --reload
    ```

## 📈 Why This Project?
This project demonstrates the ability to manage the entire lifecycle of data—from external extraction to cloud storage and API delivery. It solves the real-world problem of navigating an unorganized job market by providing structured, actionable insights.
