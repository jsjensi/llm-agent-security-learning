"""CPU-only toy reproduction of MINJA's memory-retrieval attack chain.

This is an educational mechanism demo, not the paper's full LLM experiment.
It uses only Python's standard library so it also works offline.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
from collections import Counter
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from typing import Iterable


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase English/number tokenizer used by the transparent TF-IDF demo."""
    return TOKEN_PATTERN.findall(text.lower())


def tfidf_vectors(documents: list[str]) -> list[dict[str, float]]:
    """Return L2-normalized TF-IDF vectors without third-party dependencies."""
    tokenized = [tokenize(document) for document in documents]
    document_frequency: Counter[str] = Counter()
    for tokens in tokenized:
        document_frequency.update(set(tokens))

    document_count = len(documents)
    vectors: list[dict[str, float]] = []
    for tokens in tokenized:
        counts = Counter(tokens)
        total = max(len(tokens), 1)
        vector = {
            token: (count / total)
            * (math.log((1 + document_count) / (1 + document_frequency[token])) + 1)
            for token, count in counts.items()
        }
        norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        vectors.append({token: value / norm for token, value in vector.items()})
    return vectors


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    """Cosine similarity for already normalized sparse vectors."""
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(token, 0.0) for token, value in left.items())


@dataclass(frozen=True)
class MemoryRecord:
    record_id: str
    query: str
    answer: str
    poisoned: bool = False
    round_number: int = 0


@dataclass
class TfidfMemory:
    records: list[MemoryRecord] = field(default_factory=list)

    def add(self, record: MemoryRecord) -> None:
        self.records.append(record)

    def search(self, query: str, top_k: int = 3) -> list[tuple[MemoryRecord, float]]:
        if not self.records:
            return []
        documents = [record.query for record in self.records] + [query]
        vectors = tfidf_vectors(documents)
        query_vector = vectors[-1]
        scored = [
            (record, cosine_similarity(vector, query_vector))
            for record, vector in zip(self.records, vectors[:-1])
        ]
        return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]

    def ranked(self, query: str) -> list[tuple[MemoryRecord, float]]:
        return self.search(query, top_k=len(self.records))


@dataclass
class ToyAgent:
    """A deterministic agent that copies the answer from its Top-1 memory."""

    memory: TfidfMemory
    top_k: int = 3

    def answer(self, query: str) -> tuple[str, list[tuple[MemoryRecord, float]]]:
        retrieved = self.memory.search(query, self.top_k)
        if not retrieved:
            return "No matching memory.", []
        return retrieved[0][0].answer, retrieved

    def store_simulated_interaction(
        self, record_id: str, query: str, simulated_llm_trace: str, round_number: int
    ) -> None:
        """Store a test-fixture trace that stands in for unavailable LLM output."""
        self.memory.add(
            MemoryRecord(
                record_id=record_id,
                query=query,
                answer=simulated_llm_trace,
                poisoned=True,
                round_number=round_number,
            )
        )


def load_experiment(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_memory(raw_records: Iterable[dict]) -> TfidfMemory:
    return TfidfMemory(
        [
            MemoryRecord(
                record_id=item["id"],
                query=item["query"],
                answer=item["answer"],
            )
            for item in raw_records
        ]
    )


def top_record_id(agent: ToyAgent, query: str) -> str:
    retrieved = agent.memory.search(query, top_k=1)
    return retrieved[0][0].record_id if retrieved else ""


def utility_retention(
    baseline_records: list[dict], attacked_agent: ToyAgent, utility_queries: list[str]
) -> float:
    baseline_agent = ToyAgent(build_memory(baseline_records))
    unchanged = sum(
        top_record_id(baseline_agent, query) == top_record_id(attacked_agent, query)
        for query in utility_queries
    )
    return unchanged / len(utility_queries) if utility_queries else 1.0


def run_experiment(config: dict, top_k: int, seed: int) -> tuple[list[dict], dict]:
    random.seed(seed)
    rows: list[dict] = []
    scenario_summaries: list[dict] = []

    for scenario in config["scenarios"]:
        records = list(config["benign_records"])
        random.shuffle(records)
        agent = ToyAgent(build_memory(records), top_k=top_k)
        baseline_answer, baseline_retrieved = agent.answer(scenario["victim_query"])

        for round_number, attack_query in enumerate(scenario["attack_queries"], start=1):
            poison_id = f"poison-{scenario['name']}-r{round_number}"
            # A real MINJA run asks an LLM to generate this trace. With no LLM
            # available, the fixture supplies it so we can isolate retrieval.
            simulated_trace = f"{scenario['bridge']} {scenario['target_answer']}"
            agent.store_simulated_interaction(
                poison_id, attack_query, simulated_trace, round_number
            )

            ranked = agent.memory.ranked(scenario["victim_query"])
            rank = next(
                index
                for index, (record, _) in enumerate(ranked, start=1)
                if record.record_id == poison_id
            )
            similarity = next(
                score for record, score in ranked if record.record_id == poison_id
            )
            output, retrieved = agent.answer(scenario["victim_query"])
            top_record = retrieved[0][0]
            in_top_k = rank <= top_k
            attack_success = top_record.poisoned

            rows.append(
                {
                    "scenario": scenario["name"],
                    "round": round_number,
                    "poison_similarity": f"{similarity:.6f}",
                    "poison_rank": rank,
                    "in_top_k": int(in_top_k),
                    "attack_success": int(attack_success),
                    "top_record": top_record.record_id,
                    "agent_output": output,
                }
            )

        final_rows = [row for row in rows if row["scenario"] == scenario["name"]]
        scenario_summaries.append(
            {
                "scenario": scenario["name"],
                "victim_query": scenario["victim_query"],
                "baseline_top_record": baseline_retrieved[0][0].record_id,
                "baseline_correct": int(
                    baseline_retrieved[0][0].record_id
                    == scenario["expected_baseline_record"]
                ),
                "baseline_answer": baseline_answer,
                "final_answer": agent.answer(scenario["victim_query"])[0],
                "simplified_isr": final_rows[-1]["in_top_k"],
                "simplified_asr": final_rows[-1]["attack_success"],
                "utility_retention": round(
                    utility_retention(
                        config["benign_records"], agent, config["utility_queries"]
                    ),
                    4,
                ),
            }
        )

    summary = {
        "backend": "standard-library TF-IDF",
        "seed": seed,
        "top_k": top_k,
        "scenarios": scenario_summaries,
        "mean_simplified_isr": sum(
            item["simplified_isr"] for item in scenario_summaries
        )
        / len(scenario_summaries),
        "mean_baseline_accuracy": sum(
            item["baseline_correct"] for item in scenario_summaries
        )
        / len(scenario_summaries),
        "mean_simplified_asr": sum(
            item["simplified_asr"] for item in scenario_summaries
        )
        / len(scenario_summaries),
        "mean_utility_retention": sum(
            item["utility_retention"] for item in scenario_summaries
        )
        / len(scenario_summaries),
        "limitation": (
            "The LLM generation stage is simulated by a deterministic fixture; "
            "these values are not comparable to the paper's GPT-based results."
        ),
    }
    return rows, summary


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def write_metrics_svg(rows: list[dict], path: Path) -> None:
    width, height = 900, 500
    left, top, chart_width, chart_height = 85, 70, 760, 320
    scenario_names = sorted({row["scenario"] for row in rows})
    lines: list[str] = []
    for scenario_index, scenario in enumerate(scenario_names):
        scenario_rows = [row for row in rows if row["scenario"] == scenario]
        points = []
        for row in scenario_rows:
            x = left + (int(row["round"]) - 1) * chart_width / 2
            y = top + chart_height * (1 - float(row["poison_similarity"]))
            points.append(f"{x:.1f},{y:.1f}")
        dash = "" if scenario_index == 0 else f' stroke-dasharray="{4 + scenario_index * 3} 5"'
        lines.append(
            f'<polyline points="{" ".join(points)}" fill="none" '
            f'stroke="currentColor" stroke-width="{2 + scenario_index}"{dash}/>'
        )

    x_ticks = "".join(
        f'<text x="{left + index * chart_width / 2:.1f}" y="420" '
        f'text-anchor="middle">Round {index + 1}</text>'
        for index in range(3)
    )
    y_ticks = "".join(
        (
            f'<line x1="{left}" y1="{top + chart_height * (1-value):.1f}" '
            f'x2="{left + chart_width}" y2="{top + chart_height * (1-value):.1f}" '
            'stroke="currentColor" opacity="0.15"/>'
            f'<text x="65" y="{top + chart_height * (1-value) + 5:.1f}" '
            f'text-anchor="end">{value:.1f}</text>'
        )
        for value in [0.0, 0.25, 0.5, 0.75, 1.0]
    )
    legend = " | ".join(scenario_names)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Progressive shortening retrieval similarity</title>
<desc id="desc">Poison-record cosine similarity by shortening round.</desc>
<rect width="100%" height="100%" fill="white"/>
<g font-family="Arial, sans-serif" fill="#202124" color="#2563eb">
<text x="450" y="32" font-size="22" text-anchor="middle">Progressive shortening: poison similarity</text>
<text x="450" y="55" font-size="12" text-anchor="middle">Source: local TF-IDF toy experiment</text>
{y_ticks}
<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}" stroke="#202124"/>
<line x1="{left}" y1="{top + chart_height}" x2="{left + chart_width}" y2="{top + chart_height}" stroke="#202124"/>
{''.join(lines)}
{x_ticks}
<text x="20" y="250" font-size="13" transform="rotate(-90 20 250)">Cosine similarity (0–1)</text>
<text x="450" y="455" font-size="13" text-anchor="middle">Shortening round</text>
<text x="450" y="482" font-size="12" text-anchor="middle">{escape(legend)}</text>
</g></svg>"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def write_pipeline_svg(path: Path) -> None:
    labels = [
        "Attack query",
        "Agent writes memory",
        "Victim query",
        "Top-k retrieval",
        "Output redirected",
    ]
    boxes = []
    arrows = []
    for index, label in enumerate(labels):
        x = 30 + index * 180
        boxes.append(
            f'<rect x="{x}" y="90" width="145" height="70" rx="8" '
            'fill="white" stroke="#2563eb" stroke-width="2"/>'
            f'<text x="{x + 72.5}" y="132" text-anchor="middle">{escape(label)}</text>'
        )
        if index < len(labels) - 1:
            arrows.append(
                f'<line x1="{x + 145}" y1="125" x2="{x + 175}" y2="125" '
                'stroke="#202124" marker-end="url(#arrow)"/>'
            )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="930" height="240"
viewBox="0 0 930 240" role="img" aria-labelledby="title">
<title id="title">MINJA minimal reproduction pipeline</title>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4"
orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#202124"/></marker></defs>
<rect width="100%" height="100%" fill="white"/>
<g font-family="Arial, sans-serif" fill="#202124">
<text x="465" y="42" font-size="22" text-anchor="middle">MINJA minimal retrieval chain</text>
{''.join(arrows)}{''.join(boxes)}
<text x="465" y="205" font-size="13" text-anchor="middle">Local synthetic data · deterministic toy agent · no external target</text>
</g></svg>"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data", type=Path, default=root / "data" / "minja_toy_records.json"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=root / "data" / "results"
    )
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_experiment(args.data)
    rows, summary = run_experiment(config, top_k=args.top_k, seed=args.seed)

    write_csv(rows, args.output_dir / "minja_metrics.csv")
    write_json(summary, args.output_dir / "summary.json")
    root = Path(__file__).resolve().parents[1]
    write_metrics_svg(rows, root / "assets" / "minja_metrics.svg")
    write_pipeline_svg(root / "assets" / "minja_pipeline.svg")

    print("MINJA toy experiment completed")
    print(f"Backend: {summary['backend']}")
    print(f"Scenarios: {len(summary['scenarios'])}")
    print(f"Mean baseline accuracy: {summary['mean_baseline_accuracy']:.2f}")
    print(f"Mean simplified ISR: {summary['mean_simplified_isr']:.2f}")
    print(f"Mean simplified ASR: {summary['mean_simplified_asr']:.2f}")
    print(f"Mean utility retention: {summary['mean_utility_retention']:.2f}")
    # Keep console output GBK-safe on Windows paths that contain emoji.
    print("Results written to: data/results")


if __name__ == "__main__":
    main()
