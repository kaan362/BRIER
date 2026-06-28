import os
import httpx
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_current_price(coin_id: str) -> float:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = httpx.get(url, headers={"x-cg-demo-api-key": COINGECKO_API_KEY})
    data = response.json()
    return data[coin_id]["usd"]
COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana"
}

def resolve_prediction(prediction: dict):
    asset = prediction["asset"]
    direction = prediction["direction"]
    target_price = prediction["target_price"]
    stop_price = prediction["stop_price"]
    horizon_end = datetime.fromisoformat(prediction["horizon_end"])

    coin_id = COIN_IDS.get(asset, asset.lower())
    current_price = get_current_price(coin_id)
    now = datetime.now()

    if horizon_end < now:
        result = "expired"
        print(f"horizon_end: {horizon_end}, now: {now}")
    elif direction == "long":
        if current_price >= target_price:
            result = "hit"
        elif current_price <= stop_price:
            result = "stopped"
        else:
            result = "pending"
    else:
        if current_price <= target_price:
            result = "hit"
        elif current_price >= stop_price:
            result = "stopped"
        else:
            result = "pending"
    
    if result != "pending":
        supabase.table("outcomes").insert({
            "prediction_id": prediction["id"],
            "resolved_price": current_price,
            "result": result,
            "realized_return": None,
            "resolved_at": now.isoformat()
        }).execute()

        supabase.table("predictions").update({
            "status": result
        }).eq("id", prediction["id"]).execute()
        
    return result    
    
def main():
    predictions = supabase.table("predictions").select("*").eq("status", "pending").execute()
    for prediction in predictions.data:
        result = resolve_prediction(prediction)
        print(f"Resolved: {prediction['asset']} → {result}")

if __name__ == "__main__":
    main()