# Basis QA QIWI Wallet Tests

Test assignment repository with Postman collection and Python Playwright API tests.

## What is covered

- service availability check by read-only payment history endpoint;
- balance check: balance must be greater than 0;
- create payment for 1 RUB;
- verify created payment execution by transaction status.

## Run autotests

```bash
python -m venv .venv
pip install -r requirements.txt
pytest
```

Tests use a local mock server by default, because the assignment says that real API responses are not expected to be successful.

## Real API mode

Create `.env` from `.env.example`, set `USE_MOCK_SERVER=false` and fill API credentials.

## Postman

Import files from `postman/` and run requests from top to bottom. The payment creation request saves `transaction_id`, and the final request uses it for execution check.
