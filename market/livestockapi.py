import requests
from config import Config


# Get Reliance stock data
def get_reliance_data():
    url = "https://stock.indianapi.in/stock"

    headers = {
        "X-Api-Key": Config.INDIAN_API_KEY
    }

    params = {
        "name": "Reliance"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    # Reliance data i need
    return {
        "company": data.get("companyName"),
        "current_price": data.get("currentPrice"),
        "percent_change": data.get("percentChange"),
        "year_high": data.get("yearHigh"),
        "year_low": data.get("yearLow")
    }



if __name__ == "__main__":
    reliance = get_reliance_data()
    print(reliance)