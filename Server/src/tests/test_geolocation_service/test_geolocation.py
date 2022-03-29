import json

# Important run tests only if no auth needed!
# Below test are just a sketch for future development, you can treat it as a part of specs


def test_get_all_geolocations(test_app):
    response = test_app.get(f"/geolocations")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_create_geolocation_with_ip(test_app):
    response = test_app.post(
        "/geolocations", data=json.dumps({"type": "ip", "value": "1.1.1.1"})
    )
    assert response.status_code == 201


def test_create_geolocation_with_url(test_app):
    response = test_app.post(
        "/geolocations",
        data=json.dumps({"type": "url", "value": "https://www.sofomo.com/"}),
    )
    assert response.status_code == 201


def test_get_one_geolocation_by_ip(test_app):
    response = test_app.get("/geolocation?ip=1.1.1.1")
    assert response.status_code == 200


def test_get_one_geolocation_by_url(test_app):
    response = test_app.get("/geolocation?url=https://www.sofomo.com/")
    assert response.status_code == 200
