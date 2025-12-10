import httpx
import asyncio

async def run_tests():
    # 1. Healthy Request
    async with httpx.AsyncClient() as client:
        print("Testing Normal Request...")
        resp = await client.post("http://localhost:8000/api/login", json={"user": "admin", "password": "password123"})
        print(f"Status: {resp.status_code}") # Should be 200
        print(f"Response: {resp.json()}")

        # 2. Malicious Request (SQLi)
        print("\nTesting Malicious Request (SQLi)...")
        resp = await client.post("http://localhost:8000/api/login", json={"user": "admin", "password": "' OR 1=1 --"})
        print(f"Status: {resp.status_code}") # Should be 403 or 200 (if detection fails)
        if resp.status_code == 403:
            print("Response:", resp.json())
        else:
            print("Passed (Detection needs tuning?)")

        # 3. Rate Limit Test
        print("\nTesting Rate Limit (Sending 105 requests)...")
        blocked = False
        for i in range(105):
            resp = await client.get("http://localhost:8000/api/status")
            if resp.status_code == 403:
                print(f"Blocked at request #{i+1}")
                blocked = True
                break
        
        if not blocked:
            print("Rate limit failed to trigger (or limit too high)")
        
        # 4. Management API
        print("\nTesting Management API (Add Rule)...")
        # Key matches the default in .env
        headers = {"x-admin-key": "change_this_to_a_secure_random_key_in_production"}
        resp = await client.post("http://localhost:8000/firewall/api/v1/rules/add", 
                                 json={"id": "test1", "type": "ip_block", "value": "1.2.3.4"},
                                 headers=headers)
        print(f"Add Rule Status: {resp.status_code}")
        print(resp.json())

if __name__ == "__main__":
    asyncio.run(run_tests())
