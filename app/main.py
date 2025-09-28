from fastapi import FastAPI

app = FastAPI(title="MoySklad → Google Sheets SaaS")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


