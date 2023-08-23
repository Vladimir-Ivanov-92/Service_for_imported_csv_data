import json


async def test_create_user(client, get_user_from_database):
    user_data = {
        "login": "new_user",
        "email": "new_user@adress.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["login"] == user_data["login"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["login"] == user_data["login"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_create_user_already_existing_in_db(client, get_user_from_database):
    user_data = {
        "login": "new_user",
        "email": "new_user@adress.com",
    }

    user_data_same_email = {
        "login": "new_user1",
        "email": "new_user@adress.com",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["login"] == user_data["login"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["login"] == user_data["login"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
    resp = client.post("/user/", data=json.dumps(user_data_same_email))
    assert resp.status_code == 503
    assert "A User with this email is already exist" == resp.json()["detail"]
