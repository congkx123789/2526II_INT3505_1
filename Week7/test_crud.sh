#!/bin/bash
API_URL="http://localhost:8080/v1/products"

echo "--- 1. POST /products (Create) ---"
CREATE_RES=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 15", "price": 999, "description": "Apple Flagship"}')
echo "Response: $CREATE_RES"

PRODUCT_ID=$(echo $CREATE_RES | grep -oP '"id":\s*"\K[^"]+')
echo "Extracted ID: $PRODUCT_ID"

echo -e "\n--- 2. GET /products (List) ---"
curl -s -X GET "$API_URL"

echo -e "\n\n--- 3. GET /products/{id} (Detail) ---"
curl -s -X GET "$API_URL/$PRODUCT_ID"

echo -e "\n\n--- 4. PUT /products/{id} (Update) ---"
curl -s -X PUT "$API_URL/$PRODUCT_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 15 Pro", "price": 1099, "description": "Updated Description"}'

echo -e "\n\n--- 5. GET /products/{id} (Verify Update) ---"
curl -s -X GET "$API_URL/$PRODUCT_ID"

echo -e "\n\n--- 6. DELETE /products/{id} (Delete) ---"
curl -s -X DELETE "$API_URL/$PRODUCT_ID"

echo -e "\n--- 7. GET /products (Verify Delete) ---"
curl -s -X GET "$API_URL"
echo ""
