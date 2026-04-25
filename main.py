from fastapi import FastAPI
from ai import analyze_trade

app = FastAPI()

@app.get("/")
def home():
    return {"status": "IA trader online"}

@app.post("/analyze")
def analyze(data: dict):
    return analyze_trade(data)
