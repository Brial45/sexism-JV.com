packages:
	pip install -r requirements.txt

run_api:
	uvicorn sexism_jv_forum.api.fast:app --reload

test_api_root:
	TEST_ENV=development pytest tests/api -k 'test_root' --asyncio-mode=strict -W "ignore"

test_api_predict:
	TEST_ENV=development pytest tests/api -k 'test_predict' --asyncio-mode=strict -W "ignore"

load_data:
	python -c 'from interface.csvFile import load_file; load_file()'
