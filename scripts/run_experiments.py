#!/usr/bin/env python3
"""
Master Execution Script for RunPod:
Runs the 4-way comparative benchmark for the Knowledge-Based Systems (KBS) submission.
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ontology.schema import load_ontology_from_json
from src.dataset.loader import BenchmarkDatasetLoader
from src.models.baseline import VanillaAgent, PromptGuardedAgent
from src.models.posthoc_guard import PostHocClassifierAgent
from src.models.constrained import OntologyConstrainedAgent
from src.eval.metrics import BenchmarkEvaluator
from src.eval.statistics import StatisticalReporter


def main():
    parser = argparse.ArgumentParser(
        description="Run Q1 KBS Experiment: Ontology-Constrained LLM Agent Security Benchmark"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Target base model identifier from Hugging Face"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=300,
        help="Total evaluation samples (balanced 50/50 attack/benign)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/enterprise_rbac_ontology.json",
        help="Path to declarative RBAC ontology"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to run inference on (cuda / cpu)"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in simulation/mock mode for fast local verification without GPU"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Directory to save LaTeX tables and JSON metrics"
    )
    args = parser.parse_args()

    print("==================================================================")
    print("  KBS Q1 RESEARCH BENCHMARK: ONTOLOGY-CONSTRAINED AGENT DECODING  ")
    print("==================================================================")
    print(f"Target Model       : {args.model}")
    print(f"Sample Count       : {args.samples}")
    print(f"Ontology Config    : {args.config}")
    print(f"Simulation Mode    : {args.mock}")
    print("------------------------------------------------------------------")

    # Step 1: Ingest Ontology
    print("[1/5] Loading Enterprise RBAC Security Ontology...")
    ontology = load_ontology_from_json(args.config)
    print(f"      Loaded {len(ontology.roles)} roles with {len(ontology.global_security_axioms)} global axioms.")

    # Step 2: Ingest Benchmark Dataset
    print("[2/5] Loading Enterprise Business Benchmark Suite (InjecAgent subset)...")
    loader = BenchmarkDatasetLoader(seed=42)
    dataset = loader.load_benchmark_split(total_samples=args.samples)
    print(f"      Ingested {len(dataset)} samples (150 adversarial, 150 benign).")

    # Step 3: Initialize Model Harnesses
    print("[3/5] Initializing Experimental Conditions...")
    evaluator = BenchmarkEvaluator(ontology)

    m0_vanilla = VanillaAgent(model_name=args.model, device=args.device, is_mock=args.mock)
    m1_prompt = PromptGuardedAgent(model_name=args.model, device=args.device, is_mock=args.mock)
    m2_posthoc = PostHocClassifierAgent(base_agent=m0_vanilla, is_mock=args.mock)
    m_star_proposed = OntologyConstrainedAgent(
        model_name=args.model,
        ontology=ontology,
        device=args.device,
        is_mock=args.mock
    )

    # Step 4: Run Comparative Evaluations
    print("[4/5] Executing Comparative Benchmarks across 4 Conditions...")
    results = []

    print("      -> Evaluating M0: Vanilla Unconstrained Agent...")
    res_m0 = evaluator.evaluate_harness("M0 (Vanilla Llama-3-8B)", m0_vanilla, dataset)
    results.append(res_m0)

    print("      -> Evaluating M1: In-Context Prompt-Guarded Agent...")
    res_m1 = evaluator.evaluate_harness("M1 (Prompt Guard)", m1_prompt, dataset)
    results.append(res_m1)

    print("      -> Evaluating M2: Post-Hoc Classifier Guardrail...")
    res_m2 = evaluator.evaluate_harness("M2 (Llama-Guard-3 Filter)", m2_posthoc, dataset)
    results.append(res_m2)

    print("      -> Evaluating M*: Proposed Ontology-Constrained Decoder (O-CTD)...")
    res_m_star = evaluator.evaluate_harness("M* (Proposed O-CTD)", m_star_proposed, dataset)
    results.append(res_m_star)

    # Step 5: Statistical Analysis & Reporting
    print("[5/5] Computing Non-Parametric Statistics & Exporting Deliverables...")
    StatisticalReporter.print_ascii_summary(results)

    # Run Wilcoxon Signed-Rank Test between M1 and M*
    m1_violations = [1 if r.is_violation else 0 for r in res_m1.records]
    m_star_violations = [1 if r.is_violation else 0 for r in res_m_star.records]
    wilcoxon_test = StatisticalReporter.compute_wilcoxon_test(m1_violations, m_star_violations)

    print(f"      Wilcoxon Signed-Rank Test (M1 vs M*):")
    print(f"      Statistic: {wilcoxon_test.get('statistic')}, p-value: {wilcoxon_test.get('p_value'):.5e}")
    print(f"      Result: {wilcoxon_test.get('interpretation')}")

    # Export LaTeX Table
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tex_path = str(out_dir / "table1_main_results.tex")
    StatisticalReporter.export_latex_table(results, tex_path)

    # Export Full JSON metrics
    json_path = out_dir / "summary_metrics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "meta": {"model": args.model, "samples": args.samples},
                "conditions": [r.model_dump(exclude={"records"}) for r in results],
                "wilcoxon_test": wilcoxon_test
            },
            f,
            indent=2
        )
    print(f"[Export] Saved detailed metrics to {json_path}")
    print("\n[SUCCESS] Benchmark run complete! Deliverables ready for manuscript inclusion.")


if __name__ == "__main__":
    main()
