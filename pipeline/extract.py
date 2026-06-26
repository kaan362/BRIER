import os
from dotenv import load_dotenv
from anthropic import Anthropic
from supabase import create_client
from pydantic import BaseModel
import json


load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

client = Anthropic(api_key=ANTHROPIC_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class Prediction(BaseModel):
    asset: str
    direction: str
    target_price: float
    stop_price: float
    horizon_end: str

def extract_prediction(text: str, analyst_id: int, source_id: int):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Bu analist metninden finansal prediction çıkar ve SADECE JSON döndür, başka hiçbir şey yazma:

{text}

JSON formatı:
{{
    "asset": "BTC veya ETH gibi kripto para",
    "direction": "long veya short",
    "target_price": sayı,
    "stop_price": sayı,
    "horizon_end": "YYYY-MM-DD formatında tarih"
}}"""
            }
        ]
    )
    raw = response.content[0].text
    data = json.loads(raw)
    prediction = Prediction(**data)

    supabase.table("predictions").insert({
        "analyst_id": analyst_id,
        "source_id": source_id,
        "asset": prediction.asset,
        "direction": prediction.direction,
        "target_price": prediction.target_price,
        "stop_price": prediction.stop_price,
        "horizon_end": prediction.horizon_end,
        "status": "pending"
    }).execute()

    return prediction


if __name__ == "__main__":
    test_text = "BTC bu ay 70 bin dolara çıkacak, stop loss 60 bin, hedef tarih 2024-12-31"
    result = extract_prediction(test_text, analyst_id=1, source_id=1)
    print(result)
