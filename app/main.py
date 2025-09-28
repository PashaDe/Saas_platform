from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="MoySklad → Google Sheets SaaS")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

app.include_router(api_router)


