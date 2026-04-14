from fastapi import FastAPI
from sqlalchemy import text
from database import engine
from etl import run_pipeline # Import your ETL function
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

scheduler = BackgroundScheduler()
scheduler.add_job(run_pipeline, 'interval', hours=24)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title="Job Market Pulse API",
    description="Live job market insights for Chennai, India.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def home():
    return {"message": "Welcome to the Job Market Pulse API! The scheduler is active."}

@app.get("/jobs/latest")
def get_latest_jobs(limit: int = 10):
    with engine.connect() as conn:
        query = text(f"SELECT title, company, location, tech_stack, redirect_url FROM jobs LIMIT {limit}")
        result = conn.execute(query)
        jobs = [dict(row._mapping) for row in result]
    return {"status": "success", "count": len(jobs), "data": jobs}

@app.get("/stats/tech")
def get_tech_stats():
    """See which skills are currently trending in the local database"""
    with engine.connect() as conn:
        query = text("""
            SELECT tech_stack, COUNT(*) as job_count 
            FROM jobs 
            WHERE tech_stack != '' 
            GROUP BY tech_stack 
            ORDER BY job_count DESC
            LIMIT 5
        """)
        result = conn.execute(query)
        stats = [dict(row._mapping) for row in result]
        
    return {"status": "success", "data": stats}

@app.get("/run-manual-sync")
def sync_now():
    """Endpoint to manually trigger the ETL if you don't want to wait 24 hours"""
    run_pipeline()
    return {"status": "success", "message": "ETL pipeline triggered manually."}