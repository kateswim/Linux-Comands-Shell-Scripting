import requests
import os

url = "https://openapiv1.coinstats.app/coins"
params = {"limit": 5, "currency": "USD"}   # what data

# Get API key from environment variable or use placeholder
api_key = os.getenv("COINSTATS_API_KEY", "your_api_key_here")

headers = {
    "X-API-KEY": api_key,
    "accept": "application/json"           # how you want it
}

response = requests.get(url, headers=headers, params=params)

# Check response status
if response.status_code != 200:
    print(f"Error: API returned status code {response.status_code}")
    try:
        error_data = response.json()
        print(f"Message: {error_data.get('message', 'Unknown error')}")
        if response.status_code == 401:
            print("\n⚠️  Your API Key is invalid or missing.")
            print("Please:")
            print("1. Get your API key from https://openapi.coinstats.app")
            print("2. Set it as an environment variable: export COINSTATS_API_KEY='your_key'")
            print("   Or update the api_key variable in this script")
    except:
        print(f"Response: {response.text}")
    exit(1)

data = response.json()

# Handle different response structures
if isinstance(data, list):
    # Response is a list of coins
    coins = data
elif isinstance(data, dict):
    # Try different possible keys for the coins array
    coins = data.get("coins") or data.get("result") or data.get("data") or []
    if not coins:
        print(f"Error: Could not find coins data in response.")
        print(f"Available keys: {list(data.keys())}")
        print(f"Response: {data}")
        exit(1)
else:
    print(f"Error: Unexpected response format: {type(data)}")
    exit(1)

# Display the coins
print("Here are your first 5 coins:")
for c in coins[:5]:
    name = c.get('name', 'N/A')
    price = c.get('price', 'N/A')
    print(f"{name} - {price} USD")
