PYTHON ?= python3

.PHONY: run-demo generate-raw test

run-demo:
	$(PYTHON) clean_waveform_benchmark/inference_demo.py

generate-raw:
	$(PYTHON) raw_payload_runs/generate_mock_compaction_data.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v
