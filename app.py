from flask import Flask, request, redirect, session
import requests
import os

app = Flask(__name__)

# Retrieve client details from environment variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5500/callback'
AUTHORIZE_URL = 'https://auth.tesla.com/oauth2/v3/authorize'
TOKEN_URL = 'https://auth.tesla.com/oauth2/v3/token'

# Set a fixed secret key for sessions (for debugging)
app.secret_key = 'YourFixedSecretKey123!'  # Use a strong, static key here

@app.route('/')
def home():
    state = os.urandom(16).hex()
    session['state'] = state

    print("Generated state (home):", state)  # Debug print

    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid vehicle_device_data offline_access',
        'state': state
    }
    return redirect(f'{AUTHORIZE_URL}?{requests.compat.urlencode(params)}')

@app.route('/callback')
def callback():
    # No state validation
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': request.args.get('code'),
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(TOKEN_URL, data=token_data)
    tokens = response.json()
    return tokens


if __name__ == '__main__':
    app.debug = True
    app.run(port=5500)
