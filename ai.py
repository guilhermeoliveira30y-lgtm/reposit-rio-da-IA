def analyze_trade(data: dict):
    price = data.get("price", 0)
    trend = data.get("trend", "")
    volume = data.get("volume", 0)

    score = 0

    if trend == "up":
        score += 50
    elif trend == "down":
        score += 30

    if volume > 1000:
        score += 20

    if price > 0:
        score += 10

    decision = "BUY" if score >= 60 else "NO TRADE"

    return {
        "score": score,
        "decision": decision
    }
