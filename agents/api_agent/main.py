from fastapi import FastAPI
import requests

app = FastAPI()

# Dummy portfolio breakdown
PORTFOLIO = {
    "TSMC": 12,
    "Samsung": 10,
    "Apple": 8,
    "Meta": 5,
}

ASIA_TECH = ["TSMC", "Samsung"]
TOTAL_AUM = sum(PORTFOLIO.values())

ALPHA_VANTAGE_API_KEY = "FK6Q5STPQL3GGDDW"


ALPHA_TICKERS = {
    "TSMC": "TSM"
   
}


@app.get("/asia_tech_allocation")
def get_asia_tech_allocation():
    asia_tech_aum = sum([PORTFOLIO[stock] for stock in ASIA_TECH])
    return {
        "asia_tech_percent": round(100 * asia_tech_aum / TOTAL_AUM, 2),
        "details": {stock: PORTFOLIO[stock] for stock in ASIA_TECH}
    }


@app.get("/earnings_surprises")
def get_earnings_surprises():
    data = {}

    for stock in ASIA_TECH:
        if stock == "Samsung":
            eps_actual = 1.8
            eps_expected = 1.7
            surprise = round(100 * (eps_actual - eps_expected) / eps_expected, 2)
            data[stock] = {
                "actual": eps_actual,
                "expected": eps_expected,
                "surprise_percent": surprise,
                "note": "Simulated due to Alpha Vantage data unavailability"
            }
            continue

        
        symbol = ALPHA_TICKERS.get(stock)
        if not symbol:
            data[stock] = {"error": "No Alpha Vantage symbol mapping"}
            continue

        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "EARNINGS",
                "symbol": symbol,
                "apikey": ALPHA_VANTAGE_API_KEY
            }
            resp = requests.get(url, params=params, timeout=10)
            json_data = resp.json()

            quarterly = json_data.get("quarterlyEarnings", [])
            if not quarterly:
                raise ValueError("No earnings data returned from Alpha Vantage")

            latest = quarterly[0]
            eps_actual = float(latest["reportedEPS"])
            eps_expected = float(latest.get("estimatedEPS", eps_actual * 0.95))

            surprise = round(100 * (eps_actual - eps_expected) / eps_expected, 2)
            data[stock] = {
                "actual": eps_actual,
                "expected": eps_expected,
                "surprise_percent": surprise
            }

        except Exception as e:
            data[stock] = {"error": str(e)}

    return data
