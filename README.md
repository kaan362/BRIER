# Brier

Kripto analistlerinin tahmin doğruluğunu takip eden bir leaderboard. Analistlerin tahminleri gerçek fiyat verisiyle (CoinGecko) çözülür ve isabet oranlarına göre sıralanır.

## Nasıl Çalışır

Analist metni → Claude ile tahmin çıkarımı → Supabase → CoinGecko ile çözüm → skor → leaderboard.

## Kurulum

### Gereksinimler
- Python 3.x
- Node.js
- Supabase hesabı, Anthropic API anahtarı, CoinGecko API anahtarı

### 1. Repoyu klonla
​```
git clone https://github.com/kaan362/BRIER.git
cd BRIER
​```

### 2. Pipeline (Python)
​```
cd pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
​```

### 3. Frontend (Next.js)
​```
cd web
npm install
​```

## Environment Variables

### Pipeline (`pipeline/.env`)
​```
SUPABASE_URL=<Supabase proje URL>
SUPABASE_SERVICE_KEY=<Supabase service_role key>
ANTHROPIC_API_KEY=<Anthropic API key>
COINGECKO_API_KEY=<CoinGecko API key>
​```

### Frontend (`web/.env.local`)
​```
NEXT_PUBLIC_SUPABASE_URL=<Supabase proje URL>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<Supabase publishable/anon key>
​```

**Not:** `service_role` key sadece pipeline'da kullanılır, asla frontend'e konmaz. Frontend yalnızca anon key kullanır; veriyi Supabase RLS korur.

## Pipeline Nasıl Çalıştırılır

​```
cd pipeline
source venv/bin/activate
python extract.py   # metinden tahmin çıkarır, Supabase'e yazar
python score.py     # tahminleri CoinGecko ile çözer, skorları hesaplar
​```

## Frontend Nasıl Çalıştırılır

​```
cd web
npm run dev         # localhost:3000
​```

Canlı: https://brier-nine.vercel.app