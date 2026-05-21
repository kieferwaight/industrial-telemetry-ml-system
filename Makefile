PYTHON ?= python3

.PHONY: run-demo run-api generate-raw test

run-demo:
	$(PYTHON) clean_waveform_benchmark/inference_demo.py

run-api:
	$(PYTHON) clean_waveform_benchmark/inference_api.py

generate-raw:
	$(PYTHON) raw_payload_runs/generate_mock_compaction_data.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v
