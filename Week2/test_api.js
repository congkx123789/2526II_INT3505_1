const baseURL = 'http://localhost:3000';

async function runTests() {
  console.log("=== SCENARIO 1: Get all users (GET /users) ===");
  let res = await fetch(`${baseURL}/users`);
  console.log(`Status: ${res.status} ${res.statusText}`);
  let text = await res.text();
  try {
    console.log("Body:", JSON.parse(text));
  } catch(e) { console.log("Body:", text); }
  console.log("--------------------------------------------------\n");

  console.log("=== SCENARIO 2: Get user details for ID 1 (GET /users/1) ===");
  res = await fetch(`${baseURL}/users/1`);
  console.log(`Status: ${res.status} ${res.statusText}`);
  text = await res.text();
  try {
    console.log("Body:", JSON.parse(text));
  } catch(e) { console.log("Body:", text); }
  console.log("--------------------------------------------------\n");

  console.log("=== SCENARIO 3: Create a new user (POST /users) ===");
  res = await fetch(`${baseURL}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: "3", name: "Le Van C", email: "lvc@gmail.com" })
  });
  console.log(`Status: ${res.status} ${res.statusText}`);
  text = await res.text();
  try {
    console.log("Body:", JSON.parse(text));
  } catch(e) { console.log("Body:", text); }
  console.log("--------------------------------------------------\n");

  console.log("=== SCENARIO 4: Update email for user 1 (PATCH /users/1) ===");
  res = await fetch(`${baseURL}/users/1`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: "updated_email@gmail.com" })
  });
  console.log(`Status: ${res.status} ${res.statusText}`);
  text = await res.text();
  try {
    console.log("Body:", JSON.parse(text));
  } catch(e) { console.log("Body:", text); }
  console.log("--------------------------------------------------\n");

  console.log("=== SCENARIO 5: Delete user ID 2 (DELETE /users/2) ===");
  res = await fetch(`${baseURL}/users/2`, {
    method: 'DELETE'
  });
  console.log(`Status: ${res.status} ${res.statusText}`);
  text = await res.text();
  console.log("Body:", text === "{}" || text === "" ? "(Empty)" : text);
  console.log("--------------------------------------------------\n");

  console.log("=== ERROR TEST 1: Bad Request (GET /400) ===");
  res = await fetch(`${baseURL}/400`);
  console.log(`Status: ${res.status} ${res.statusText}`);
  text = await res.text();
  try {
    console.log("Body:", JSON.parse(text));
  } catch(e) { console.log("Body:", text); }
  console.log("--------------------------------------------------\n");

  console.log("=== ERROR TEST 2: Internal Server Error (GET /500) ===");
  res = await fetch(`${baseURL}/500`);
  console.log(`Status: ${res.status} ${res.statusText}`);
  text = await res.text();
  try {
    console.log("Body:", JSON.parse(text));
  } catch(e) { console.log("Body:", text); }
  console.log("--------------------------------------------------\n");
}

runTests().catch(console.error);
