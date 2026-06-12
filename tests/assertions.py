from typing import Any


def assert_json_response(response: Any, expected_status: int = 200) -> dict:
    assert response.status == expected_status, f"Expected HTTP {expected_status}, got {response.status}"
    assert "application/json" in response.headers.get("content-type", "").lower()
    return response.json()


def assert_has_fields(payload: dict, fields: list[str], object_name: str = "object") -> None:
    missing = [field for field in fields if field not in payload]
    assert not missing, f"{object_name} is missing fields: {missing}"


def assert_positive_number(value: Any, field_name: str) -> None:
    assert isinstance(value, (int, float)), f"{field_name} must be numeric"
    assert value > 0, f"{field_name} must be greater than 0"
