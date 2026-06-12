import time

import pytest

from tests.assertions import assert_has_fields, assert_json_response, assert_positive_number


@pytest.mark.api
def test_service_availability(api_context, settings):
    response = api_context.get(f"/payment-history/v2/persons/{settings['wallet']}/payments", params={"rows": "1", "operation": "ALL"})
    body = assert_json_response(response)
    assert_has_fields(body, ["data"], "payment history")
    assert isinstance(body["data"], list)


@pytest.mark.api
def test_balance_is_greater_than_zero(api_context, settings):
    response = api_context.get(f"/funding-sources/v2/persons/{settings['wallet']}/accounts")
    body = assert_json_response(response)
    rub = next((a for a in body["accounts"] if a.get("alias") == "qw_wallet_rub"), None)
    assert rub is not None
    assert rub["balance"]["currency"] == 643
    assert_positive_number(rub["balance"]["amount"], "balance.amount")


@pytest.fixture
def created_payment(api_context, settings):
    payload = {
        "id": str(int(time.time() * 1000)),
        "sum": {"amount": 1, "currency": "643"},
        "paymentMethod": {"type": "Account", "accountId": "643"},
        "comment": "basis-qa-test",
        "fields": {"account": settings["recipient_wallet"]},
    }
    response = api_context.post("/sinap/api/v2/terms/99/payments", data=payload)
    body = assert_json_response(response)
    assert body["sum"]["amount"] == 1
    assert body["sum"]["currency"] == "643"
    assert body["fields"]["account"] == settings["recipient_wallet"]
    return body["transaction"]["id"]


@pytest.mark.api
def test_create_payment_for_one_rub(created_payment):
    assert created_payment


@pytest.mark.api
def test_execute_created_payment(api_context, created_payment):
    response = api_context.get(f"/payment-history/v2/transactions/{created_payment}", params={"type": "OUT"})
    body = assert_json_response(response)
    assert str(body["txnId"]) == str(created_payment)
    assert body["type"] == "OUT"
    assert body["sum"]["amount"] == 1
    assert body["sum"]["currency"] == 643
    assert body["errorCode"] in {0, None}
    assert body["error"] in {None, ""}
    assert body["status"] == "SUCCESS"
