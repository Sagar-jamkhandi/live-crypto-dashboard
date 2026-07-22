# 📈 Live Cryptocurrency Market Dashboard

A real-time, auto-refreshing dashboard that pulls live market data (price, market cap,
24h volume, % change) for major cryptocurrencies from the public **CoinGecko API** and
visualizes it with interactive charts.

Built to demonstrate: consuming a live REST API, data wrangling with pandas, and
building an interactive analytics UI with Streamlit + Plotly.

## 🚀 Live Demo
> Deploy this for free on [Streamlit Community Cloud](https://streamlit.io/cloud) and
> put the live link here. Recruiters click links — a working live demo is worth far
> more than a screenshot.

## ✨ Features
- Real-time prices for 6+ coins (Bitcoin, Ethereum, Solana, Dogecoin, Cardano, Ripple),
  configurable via the sidebar
- KPI cards showing current price and 24h % change
- Market cap comparison bar chart
- 24h % change bar chart (color-coded red/green)
- Historical price trend line chart (1–30 day window, per coin)
- Auto-refreshes every 60 seconds — no manual reload needed
- Data cached for 60s to stay within the free API's rate limits

## 🛠️ Tech Stack
| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Data source | [CoinGecko public API](https://www.coingecko.com/en/api) (no key required) |
| Data handling | pandas |
| Visualization | Plotly |
| Web app framework | Streamlit |

## 📦 Project Structure
```
project1-live-crypto-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

## ⚙️ Setup & Run Locally
```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/live-crypto-dashboard.git
cd live-crypto-dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```
The app opens automatically at `http://localhost:8501`.

## ☁️ Deploy for Free (so you have a live link for your resume)
1. Push this project to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app** → select this repo → set main file to `app.py` → Deploy.
4. Copy the live URL and add it to your resume / LinkedIn / GitHub profile README.

## 📊 What This Project Demonstrates (for your resume/interview)
- Consuming and parsing a third-party REST API in real time
- Handling API rate limits with caching (`st.cache_data`)
- Transforming nested JSON into clean tabular data with pandas
- Building interactive, multi-chart dashboards
- Basic error handling for network/API failures

## 🔮 Possible Extensions
- Add price alerts (email/SMS when a coin crosses a threshold)
- Store historical snapshots in a database (SQLite/PostgreSQL) to track your own history
  instead of relying solely on CoinGecko's chart endpoint
- Add a portfolio tracker (input holdings, see live portfolio value)

## 📝 Resume Bullet (copy/adapt this)
> Built a real-time cryptocurrency analytics dashboard in Python (Streamlit, Plotly)
> consuming a live REST API, featuring auto-refresh, interactive visualizations, and
> historical trend analysis across 6+ assets; deployed publicly on Streamlit Cloud.

## 📄 License
MIT — free to use and adapt.
