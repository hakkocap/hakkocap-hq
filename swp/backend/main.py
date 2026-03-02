"""
Sovereign Workflow Protocol (SWP)
Main Entry Point
"""

import sys
from pathlib import Path

# Add backend to path for absolute imports
BACKEND_DIR = Path(__file__).parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.main import app as routes_app

# Create main app
app = FastAPI(
    title="Sovereign Workflow Protocol",
    description="AI Agent Management & Orchestration System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-application
app.mount("/", routes_app)

@app.get("/health")
def health():
    return {"status": "operational", "system": "SWP"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
