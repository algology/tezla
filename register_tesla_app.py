import http.client
import json
import os

# Set your domain
app_domain = 'raw.githubusercontent.com/algology/tezla'  # This might not be acceptable to Tesla

# Optionally, your CSR string if you have one
public_key_csr = ''  # Leave empty if not applicable

# Retrieve the Tesla API token from environment variables
tesla_api_token = os.getenv('TESLA_API_TOKEN')

conn = http.client.HTTPSConnection("fleet-api.prd.na.vn.cloud.tesla.com")
payload = json.dumps({
    "domain": app_domain,
    "csr": public_key_csr
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {tesla_api_token}'
}
conn.request("POST", "/api/1/partner_accounts", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
