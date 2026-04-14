import os
import requests
import pandas as pd
from dotenv import load_dotenv
from database import engine

# Load environment variables
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_jobs(role="python", country="in", city="chennai"):
    """Extract: Fetch jobs from Adzuna API"""
    print(f"Fetching '{role}' jobs in {city.capitalize()}, {country.upper()}...")
    
    # Notice the country variable is now in the URL
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 50,
        "what": role,
        "where": city  # NEW: This tells Adzuna exactly which city to search
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print("Error fetching data:", response.status_code)
        return []

def transform_data(raw_data):
    if not raw_data: return pd.DataFrame()
    df = pd.json_normalize(raw_data)
    
    # 1. Keep only columns we care about
    cols_to_keep = ['id', 'title', 'company.display_name', 'location.display_name', 'description', 'salary_min', 'salary_max', 'redirect_url']
    
    df = df[[c for c in cols_to_keep if c in df.columns]] 
    
    # 2. Rename columns for our database schema
    df = df.rename(columns={
        'company.display_name': 'company',
        'location.display_name': 'location'
    })
    
    # 3. Clean up salaries (fill NaNs with 0 or None)
    if 'salary_min' in df.columns:
        df['salary_min'] = df['salary_min'].fillna(0)
        df['salary_max'] = df['salary_max'].fillna(0)
    
    # 4. Extract tech stack (Simple keyword matching)
    keywords = ['python', 'sql', 'aws', 'docker', 'fastapi', 'pandas']
    df['tech_stack'] = df['description'].apply(
        lambda x: ','.join([kw for kw in keywords if kw in str(x).lower()])
    )
    
    # 5. Drop duplicate job IDs
    df = df.drop_duplicates(subset=['id'])
    
    return df

from sqlalchemy import text # Make sure this is imported

def load_data(df):
    """Load: Maintain a 7-day rolling window of jobs"""
    if df.empty:
        print("No data to load.")
        return
    
    try:
        with engine.connect() as conn:
            # 1. Clean up: Remove jobs older than 7 days
            # This keeps your free tier storage safe!
            conn.execute(text("DELETE FROM jobs WHERE created_at < NOW() - INTERVAL '7 days'"))
            conn.commit()
            
            # 2. Deduplicate: Remove jobs that are already in the DB 
            # so we don't upload them again
            existing_ids = pd.read_sql("SELECT id FROM jobs", engine)['id'].tolist()
            df = df[~df['id'].isin(existing_ids)]

            if not df.empty:
                df.to_sql('jobs', engine, if_exists='append', index=False)
                print(f"✅ Loaded {len(df)} new unique jobs. Storage optimized!")
            else:
                print("Checking... All fetched jobs already exist in DB. Skipping upload.")
                
    except Exception as e:
        print(f"❌ Error during optimized load: {e}")


def run_pipeline():
    """Run the full ETL process"""
    print("🚀 Starting ETL Pipeline...")
    
    # 1. Extract - Now looking for Data Engineer (or whatever you prefer) in Chennai!
    raw_data = fetch_jobs(role="data engineer", country="in", city="chennai") 
    
    # 2. Transform
    clean_df = transform_data(raw_data)
    print(f"Processed {len(clean_df)} jobs.")
    
    # 3. Load
    load_data(clean_df)
    
    return clean_df

if __name__ == "__main__":
    run_pipeline()