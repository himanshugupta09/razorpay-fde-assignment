import httpx
import os
import load_dotenv
load_dotenv()
# --- Fill these in carefully ---
ZOHO_ORG_ID =  os.getenv("ZOHO_ORG_ID")
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")

def test_connection():
    url = "https://www.zohoapis.in/inventory/v1/items"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}"
    }
    
    params = {
        "organization_id": ZOHO_ORG_ID
    }
    
    print(f"Testing connection to: {url}")
    print(f"With Org ID: {ZOHO_ORG_ID}")
    
    response = httpx.get(url, headers=headers, params=params)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_connection()