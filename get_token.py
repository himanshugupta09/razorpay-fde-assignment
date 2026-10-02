import httpx

url = "https://accounts.zoho.in/oauth/v2/token"
data = {
    "code": "1000.6a56433ce7ffbc4a55cf7601972dfeee.6863b0f16b73d188dbd7e6f031f37499",
    "client_id": "1000.IABDY3FYIKPFLUYD1ZBEHM1D07K70E",
    "client_secret": "a24da7d84b1b05c202333923990bb85ce771fc55dd",
    "grant_type": "authorization_code"
}

response = httpx.post(url, data=data)
print(response.json())