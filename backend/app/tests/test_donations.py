def register_user(client, *, name, email, role):
    return client.post(
        "/api/v1/auth/register",
        json={
            "full_name": name,
            "email": email,
            "password": "supersecure123",
            "role": role,
        },
    )


def login_user(client, *, email):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "supersecure123"}
    )
    return response.json()["access_token"]

def create_org(client, token, payload):
    return client.post(
        "/api/v1/organizations",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

def test_restaurant_can_create_and_food_bank_can_claim_donation(client):
    register_user(client, name="Restaurant", email="r@example.com", role="restaurant")
    register_user(client, name="Food Bank", email="f@example.com", role="food_bank")

    restaurant_token = login_user(client, email="r@example.com")
    food_bank_token = login_user(client, email="f@example.com")

    restaurant_org = create_org(
        client,
        restaurant_token,
        {
            "name": "Good Eats",
            "type": "restaurant",
            "address": "123 Main St",
            "latitude": 33.501,
            "longitude": -81.965,
            "phone": "555-111-2222",
        },
    )
    food_bank_org = create_org(
        client,
        food_bank_token,
        {
            "name": "Helping Hands",
            "type": "food_bank",
            "address": "999 Center St",
            "latitude": 33.502,
            "longitude": -81.964,
            "phone": "555-333-4444",
        },
    )

    donation_response = client.post(
        "/api/v1/donations",
        headers={"Authorization": f"Bearer {restaurant_token}"},
        json={
            "organization_id": restaurant_org.json()["id"],
            "title": "Fresh Sandwiches",
            "description": "Packaged turkey sandwiches available for pickup",
            "food_type": "prepared_meal",
            "quantity": 50,
            "unit": "itmes",
            "prepared_at": "2026-03-07T15:00:00Z",
            "expires_at": "2026-03-07T20:00:00Z",
            "pickup_deadline": "2026-03-07T19:00:00Z",
            "location_address": "123 Main St",
            "latitude": 33.501,
            "longitude": -81.965,
            "special_handling": "Keep refridgerated",
        },
    )
    assert donation_response.status_code == 201

    claim_response = client.post(
        f"/api/v1/donations/{donation_response.json()['id']}/claim",
        headers={"authorization": f"Bearer {food_bank_token}"},
        json={
            "recipient_organization_id": food_bank_org.json()["id"],
            "needs_volunteer": True,
        },
    )
    assert claim_response.status_code == 200
    assert claim_response.json()["status"] == "needs_volunteer"