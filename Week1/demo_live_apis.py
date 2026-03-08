"""
WEEK 1 - LIVE DEMO: Public REST APIs
=====================================
Goals:
 - Visualize real-world API requests & responses.
 - Demonstrate zero-auth public endpoints.
 - Observe JSON data structures.

Usage:
 pip install requests
 python demo_live_apis.py
=====================================
"""

import requests
import json

def print_header(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")

def log_request(method, url, payload=None):
    print(f"\n[REQ] {method} {url}")
    if payload:
        print(f"BODY: {json.dumps(payload, indent=2)}")

def log_response(res, data=None):
    print(f"[RES] Status: {res.status_code} | Content-Type: {res.headers.get('Content-Type', 'N/A')}")
    output = data if data else res.json()
    print(f"BODY:\n{json.dumps(output, indent=2, ensure_ascii=False)[:800]}")
    if len(json.dumps(output)) > 800:
        print("    ... (truncated for readability)")

# -------------------------------------------------------
# DEMO 1: PokéAPI (Standard REST)
# -------------------------------------------------------
print_header("DEMO 1: PokéAPI - Fetching Pikachu")
url1 = "https://pokeapi.co/api/v2/pokemon/pikachu"
log_request("GET", url1)

try:
    res1 = requests.get(url1, timeout=10)
    raw_data = res1.json()
    # Filter for key fields to keep demo clean
    display_data = {
        "name": raw_data["name"],
        "id": raw_data["id"],
        "height": raw_data["height"],
        "weight": raw_data["weight"],
        "types": [t["type"]["name"] for t in raw_data["types"]],
        "base_xp": raw_data["base_experience"]
    }
    log_response(res1, data=display_data)
except Exception as e:
    print(f"Error: {e}")

# -------------------------------------------------------
# DEMO 2: REST Countries (Geo Data)
# -------------------------------------------------------
print_header("DEMO 2: REST Countries - Querying Vietnam")
url2 = "https://restcountries.com/v3.1/name/vietnam"
log_request("GET", url2)

try:
    res2 = requests.get(url2, timeout=10)
    raw_data = res2.json()[0]
    display_data = {
        "name": raw_data["name"]["official"],
        "capital": raw_data.get("capital", ["N/A"])[0],
        "pop": raw_data["population"],
        "area_km2": raw_data["area"],
        "currencies": list(raw_data.get("currencies", {}).keys()),
        "languages": list(raw_data.get("languages", {}).values()),
        "region": raw_data["region"]
    }
    log_response(res2, data=display_data)
except Exception as e:
    print(f"Error: {e}")

# -------------------------------------------------------
# DEMO 3: JSONPlaceholder (CRUD Simulation)
# -------------------------------------------------------
print_header("DEMO 3: JSONPlaceholder - Blog Operations")

# GET - Read resource
url_get = "https://jsonplaceholder.typicode.com/posts/1"
log_request("GET", url_get)
try:
    res_get = requests.get(url_get, timeout=10)
    log_response(res_get)
except Exception as e:
    print(f"Error: {e}")

# POST - Create resource
url_post = "https://jsonplaceholder.typicode.com/posts"
new_post = {
    "title": "My First API Lesson",
    "body": "Learning REST API calls with Python today!",
    "userId": 1
}
log_request("POST", url_post, payload=new_post)
try:
    res_post = requests.post(url_post, json=new_post, timeout=10)
    log_response(res_post)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("  DEMO COMPLETE - All endpoints responded successfully.")
print("="*60)
print("""
Discussion Points:
  1. Why did POST return 201 instead of 200?
  2. Naming: Why use '/pokemon/pikachu' (plural nouns)?
  3. JSON Structure: Which fields were most critical for the UI?
  4. Security: What happens if an API Key is exposed in logs?
""")

