from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepoSmokeTests(unittest.TestCase):
    def run_script(self, relative_script_path: str) -> str:
        completed = subprocess.run(
            [sys.executable, relative_script_path],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        return completed.stdout

    def test_inference_demo_runs(self) -> None:
        output = self.run_script("clean_waveform_benchmark/inference_demo.py")
        self.assertIn("Target: site_class", output)
        self.assertIn("Target: fill_state", output)
        self.assertIn("Single-row inference example", output)

    def test_raw_payload_generator_runs(self) -> None:
        output = self.run_script("raw_payload_runs/generate_mock_compaction_data.py")
        self.assertIn("Wrote 725 records to raw_payload_runs/all_runs.jsonl", output)
        self.assertIn("Wrote scenario files to raw_payload_runs/scenarios/", output)


if __name__ == "__main__":
    unittest.main()
