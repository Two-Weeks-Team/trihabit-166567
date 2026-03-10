from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes import router
from models import engine, Base
import os

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router with no prefix (DigitalOcean may strip '/api')

@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health", response_model=dict)
async def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <html>
    <head>
        <title>TriHabit API</title>
        <style>
            body { background-color: #0e1117; color: #e5e7eb; font-family: Arial, Helvetica, sans-serif; text-align: center; padding: 2rem; }
            a { color: #60a5fa; }
            table { margin: 0 auto; border-collapse: collapse; }
            th, td { padding: 0.5rem 1rem; border: 1px solid #374151; }
        </style>
    </head>
    <body>
        <h1>TriHabit – AI‑guided Habit Tracking</h1>
        <p>Focus on what matters most with AI‑generated coaching.</p>
        <h2>Available Endpoints</h2>
        <table>
            <tr><th>Method</th><th>Path</th><th>Description</th></tr>
            <tr><td>GET</td><td>/health</td><td>Health check</td></tr>
            <tr><td>GET</td><td>/habits</td><td>List user habits (demo data)</td></tr>
            <tr><td>POST</td><td>/habits/{id}/check-in</td><td>Record a habit check‑in</td></tr>
            <tr><td>GET</td><td>/habits/{id}/coaching</td><td>AI‑generated coaching suggestion</td></tr>
            <tr><td>GET</td><td>/insights</td><td>Weekly AI‑driven insights</td></tr>
        </table>
        <p>API docs: <a href="/docs">/docs</a> | <a href="/redoc">/redoc</a></p>
        <h3>Tech Stack</h3>
        <ul style="list-style:none;">
            <li>FastAPI 0.115.0</li>
            <li>PostgreSQL via SQLAlchemy 2.0.35</li>
            <li>DigitalOcean Serverless Inference (openai‑gpt‑oss‑120b)</li>
            <li>Python 3.12+</li>
        </ul>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
