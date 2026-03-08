"""
test_api.py - Automated Testing: Bad vs Good API
Run: python test_api.py (Ensure app.py is running on port 5000)
"""
import requests
import json
import sys

BASE = "http://localhost:5000"

def print_header(title):
    line = "=" * 60
    print(f"\n{line}\n  {title}\n{line}")

def call(method, url, data=None, label=""):
    full_url = BASE + url
    try:
        r = getattr(requests, method)(full_url, json=data, timeout=5)
        color = "\033[92m" if r.status_code < 300 else "\033[91m"
        print(f"\n--- [{label}] ---")
        print(f"{method.upper()} {url} | Status: {color}{r.status_code}\033[0m")
        if r.status_code != 204:
            print(json.dumps(r.json(), ensure_ascii=False, indent=2))
        else:
            print("[No Content]")
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Failed. Is app.py running?")
        sys.exit(1)

# -------------------------------------------------------
# 1. BAD API - Identifying Issues
# -------------------------------------------------------
print_header("BAD API DEMO - Design Flaws")

call("get", "/bad/getAllUsers",
     label="Issue: Verb in URL + Flat Array")

call("get", "/bad/User_Profile?UserID=1",
     label="Issue: Casing + Query String ID + Inconsistent Fields")

call("get", "/bad/getOrdersByUserID/1",
     label="Issue: No Hierarchy + Verb in URL")

call("post", "/bad/createUser",
     data={"UserName": "test", "Email": "t@test.com"},
     label="Issue: status 200 on Create + Opaque Response")


# -------------------------------------------------------
# 2. GOOD API - Best Practices
# -------------------------------------------------------
print_header("GOOD API DEMO - Best Practices")

call("get", "/good/v1/users",
     label="List Users (Envelope + Pagination)")

call("get", "/good/v1/users?page=1&limit=2",
     label="Pagination via Query String")

call("get", "/good/v1/users?name=nguyen",
     label="Filtering via Query String")

call("get", "/good/v1/users/1",
     label="Resource Retrieval via Path Parameter")

call("get", "/good/v1/users/99",
     label="Error Handling (404 + Error Envelope)")

call("post", "/good/v1/users",
     data={"username": "top_talent", "email_address": "pro@dev.com", "phone_number": "123456789"},
     label="Create User (201 + Full Resource Body)")

call("post", "/good/v1/users",
     data={"username": "incomplete"},
     label="Validation Error (400 + Field Details)")

call("patch", "/good/v1/users/1",
     data={"email_address": "new_email@company.com"},
     label="Partial Update (PATCH)")

call("get", "/good/v1/users/1/orders",
     label="Sub-resource Hierarchy (User's Orders)")

call("get", "/good/v1/users/1/orders?status=pending",
     label="Sub-resource Filtering")

call("patch", "/good/v1/orders/ord_001",
     data={"status": "cancelled"},
     label="Update Sub-resource (PATCH)")

call("patch", "/good/v1/orders/ord_001",
     data={"status": "INVALID"},
     label="Enum Validation Error")

print(f"\n{'=' * 60}\n  Tests Complete!\n{'=' * 60}\n")

