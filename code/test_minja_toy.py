"""Regression tests for the offline MINJA toy experiment."""

from __future__ import annotations

import unittest
from pathlib import Path

from run_minja_toy import load_experiment, run_experiment, tfidf_vectors


ROOT = Path(__file__).resolve().parents[1]
CONFIG = load_experiment(ROOT / "data" / "minja_toy_records.json")


class MinjaToyTests(unittest.TestCase):
    def test_identical_documents_have_unit_similarity(self) -> None:
        vectors = tfidf_vectors(["same short document", "same short document"])
        similarity = sum(
            value * vectors[1].get(token, 0.0)
            for token, value in vectors[0].items()
        )
        self.assertAlmostEqual(similarity, 1.0)

    def test_baseline_and_final_attack_for_three_seeds(self) -> None:
        for seed in (7, 42, 2026):
            with self.subTest(seed=seed):
                _, summary = run_experiment(CONFIG, top_k=3, seed=seed)
                self.assertEqual(summary["mean_baseline_accuracy"], 1.0)
                self.assertEqual(summary["mean_simplified_isr"], 1.0)
                self.assertEqual(summary["mean_simplified_asr"], 1.0)
                self.assertEqual(summary["mean_utility_retention"], 1.0)

    def test_final_shortened_record_is_more_similar(self) -> None:
        rows, _ = run_experiment(CONFIG, top_k=3, seed=42)
        for scenario in CONFIG["scenarios"]:
            scenario_rows = [
                row for row in rows if row["scenario"] == scenario["name"]
            ]
            first = float(scenario_rows[0]["poison_similarity"])
            final = float(scenario_rows[-1]["poison_similarity"])
            self.assertGreater(final, first)
            self.assertEqual(scenario_rows[-1]["poison_rank"], 1)


if __name__ == "__main__":
    unittest.main()

