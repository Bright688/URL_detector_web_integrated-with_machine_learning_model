from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import whois
from datetime import datetime
import socket
import ssl
import requests
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
import time

app = Flask(__name__)

# Load the saved model and scaler
model = pickle.load(open('model.pkl', 'rb'))
# Define the columns in the expected order

# Load the scaler
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Define headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://google.com',
}

# Fetch URL with retries
def fetch_url(url, retries=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.content
        except (requests.exceptions.RequestException, NewConnectionError, MaxRetryError, ConnectionError):
            time.sleep(2)
    return None

# Function to check SSL certificate
def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                return True
    except:
        return False

# Check for IP address in URL
def contains_ip(url):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    return bool(ip_pattern.search(url))

# Compile the shortening services regex pattern
shortening_services_pattern = re.compile(r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|"
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|"
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|"
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|"
                      r"tr\.im|link\.zip\.net")

# Count special characters in URL
def count_special_chars(url):
    return sum(not c.isalnum() and c not in ['.', '-', '_', ':', '/', '?', '&', '=', '%'] for c in url)

# Check for URL shortening services using the provided regex pattern
def shortening_services(url):
    return bool(re.search(shortening_services_pattern, url))

# Extract features from URL
def extract_features(url):
    features = {}
    domain = urlparse(url).netloc
    features['url'] = url
    features['url_length'] = len(url)
    features['contains_ip'] = int(contains_ip(url))
    features['shortening_services'] = int(shortening_services(url))
    features['special_chars'] = count_special_chars(url)
    
    content = fetch_url(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        features['html_length'] = len(content)
        features['js_length'] = sum(len(s.string) for s in soup.find_all('script') if s.string)
        features['num_links'] = len(soup.find_all('a'))
        features['num_forms'] = len(soup.find_all('form'))
    
        try:
            domain_info = whois.whois(domain)
            creation_date = domain_info.creation_date
            updated_date = domain_info.updated_date
            expiration_date = domain_info.expiration_date
            
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(updated_date, list):
                updated_date = updated_date[0]
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            
            features['domain_age'] = (datetime.now() - creation_date).days if creation_date else None
        except Exception as e:
            print(f"Error fetching domain info for {domain}: {e}")
            features['domain_age'] = None

        features['has_ssl'] = 1 if check_ssl(domain) else 0
    else:
        features.update({
            'html_length': 0,
            'js_length': 0,
            'num_links': 0,
            'num_forms': 0,
            'contains_ip': 0,
            'shortening_services': 0,
            'url_length': len(url),
            'special_chars': count_special_chars(url),
            'num_subdomains': 0,
            'domain_age': None,
            'has_ssl': 0,
        })

    return features

#Load the processed data
X = pd.read_csv('processed_data.csv')


# Classify URL using the model and scaler
def classify_url(url, model, scaler, feature_columns_order):
    features = extract_features(url)
    features_df = pd.DataFrame([features])
    
    # Ensure all required columns are present
    for col in feature_columns_order:
        if col not in features_df.columns:
            features_df[col] = 0
    
    features_df = features_df[feature_columns_order]
    
    
    # Scale and predict
    features_scaled = scaler.transform(features_df)
    prediction = model.predict(features_scaled)
    return "Legitimate" if prediction == 0 else "Phishing"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check/', methods=['POST'])
def check_url():
    url=None
    url = request.form['url']
    result = classify_url(url, model, scaler, X.columns)
    return render_template('index.html', result=result, show_result=True)

if __name__ == '__main__':
    app.run(debug=False, host=0.0.0.0)
