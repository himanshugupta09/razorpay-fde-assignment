from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import time
from typing import Optional

app = FastAPI(title="ZOHO FDE Connector")
import os
from dotenv import load_dotenv

load_dotenv()


ZOHO_ORG_ID = os.getenv("ZOHO_ORG_ID")
ZOHO_DOMAIN = os.getenv("ZOHO_DOMAIN")
CONNECTOR_API_KEY = os.getenv("CONNECTOR_API_KEY")
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")

print(ZOHO_ORG_ID)
print(ZOHO_DOMAIN)
print(CONNECTOR_API_KEY)
print(ZOHO_ACCESS_TOKEN)


RATE_LIMIT = 5 
RATE_LIMIT_WINDOW = 60 
client_requests = {}

def check_rate_limit(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in client_requests:
        client_requests[client_ip] = []
        
    client_requests[client_ip] = [req_time for req_time in client_requests[client_ip] 
                                  if current_time - req_time < RATE_LIMIT_WINDOW]
    
    if len(client_requests[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
        
    client_requests[client_ip].append(current_time)

def verify_api_key(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {CONNECTOR_API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

def get_zoho_headers():
    """Zoho requires the OAuth token in the header."""
    return {
        "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}"
    }

# --- Core FDE Endpoints ---
@app.get("/items", dependencies=[Depends(verify_api_key), Depends(check_rate_limit)])
async def list_items(name: Optional[str] = None):
    """Fetch inventory items. Optionally filter by name."""
    url = f"https://www.zohoapis.in/inventory/v1/items"
    
    # organization_id MUST be a query parameter in Zoho Inventory
    params = {"organization_id": ZOHO_ORG_ID}
    
    if name:
        params["name_contains"] = name
        
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_zoho_headers(), params=params)
        
        if response.status_code != 200:
            error_data = response.json()
            raise HTTPException(status_code=response.status_code, detail=error_data)
            
        return response.json()

@app.get("/items/{item_id}", dependencies=[Depends(verify_api_key), Depends(check_rate_limit)])
async def get_item(item_id: str):
    """Fetch a specific inventory item by ID."""
    url = f"https://www.zohoapis.in/inventory/v1/items/{item_id}"
    
    params = {"organization_id": ZOHO_ORG_ID}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_zoho_headers(), params=params)
        
        if response.status_code != 200:
            error_data = response.json()
            raise HTTPException(status_code=response.status_code, detail=error_data)
            
        return response.json()