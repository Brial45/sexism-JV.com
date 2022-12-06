packages:
	pip install -r requirements.txt

run_api:
	uvicorn jvcom.api.fast:app --reload

test_api_root:
	TEST_ENV=development pytest tests/api -k 'test_root' --asyncio-mode=strict -W "ignore"

test_api_predict:
	TEST_ENV=development pytest tests/api -k 'test_predict' --asyncio-mode=strict -W "ignore"

main:
	python jvcom/main.py
