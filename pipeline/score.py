import os
import httpx
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, timezone

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_price_series(coin_id, start, end):
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={start_ts}&to={end_ts}"
    response = httpx.get(url, headers={"x-cg-demo-api-key": COINGECKO_API_KEY})
    data = response.json()
    return data["prices"]
    

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
    horizon_start = datetime.fromisoformat(prediction["horizon_start"])
    horizon_end = datetime.fromisoformat(prediction["horizon_end"]).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)        
    coin_id = COIN_IDS.get(asset, asset.lower())
    series = get_price_series(coin_id, start=horizon_start, end=min(horizon_end, now))

    result = "pending"    
    resolved_price = None
    resolved_at = None

    for ts, price in series:
        if direction == "long":
            if price >= target_price:
                result = "hit"
                resolved_price = price
                resolved_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                break
            elif price <= stop_price:
                result = "stopped"
                resolved_price = price
                resolved_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                break
        elif direction == "short":
            if price <= target_price:
                result = "hit"
                resolved_price = price
                resolved_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                break
            elif price >= stop_price:
                result = "stopped"
                resolved_price = price
                resolved_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                break

    if result == "pending" and now > horizon_end:
        result = "expired"
        resolved_price = series[-1][1]
        resolved_at = datetime.fromtimestamp(series[-1][0] / 1000, tz=timezone.utc)
    
    if result != "pending":
        supabase.table("outcomes").insert({
            "prediction_id": prediction["id"],
            "resolved_price": resolved_price,
            "result": result,
            "realized_return": None,
            "resolved_at": resolved_at.isoformat()
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
    calculate_analyst_scores()

def calculate_analyst_scores():
    analysts = supabase.table("analysts").select("*").execute()
    
    for analyst in analysts.data:
        outcomes = supabase.table("outcomes")\
            .select("*, predictions!inner(analyst_id)")\
            .eq("predictions.analyst_id", analyst["id"])\
            .execute()
        
        
        total = len(outcomes.data)
        hits = len([o for o in outcomes.data if o["result"] == "hit"])
        
        if total > 0:
            win_rate = hits / total * 100
            print(f"{analyst['handle']}: {hits}/{total} hit, win rate: {win_rate:.1f}%")
            supabase.table("analysts").update({
                "win_rate": win_rate,
                "sample_size": total
            }).eq("id", analyst["id"]).execute()
if __name__ == "__main__":
    main()
    
