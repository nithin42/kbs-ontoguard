#!/usr/bin/env python3
"""
Master Execution Script for RunPod:
Runs the 4-way comparative benchmark for the Knowledge-Based Systems (KBS) submission.
Architected to share a single GPU model instance to guarantee zero CPU offloading.
"""

import argparse
import json
import sys
import os
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
        default="Qwen/Qwen2.5-7B-Instruct",
        help="Target model on Hugging Face (default: Qwen/Qwen2.5-7B-Instruct)"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=100,
        help="Total evaluation samples (balanced 50/50 attack/benign, default: 100)"
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
        "--hf-token",
        type=str,
        default=None,
        help="Hugging Face access token for gated models (or set HF_TOKEN env var)"
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
        help="Directory to save LaTeX tables, plots, and JSON metrics"
    )
    args = parser.parse_args()

    hf_token = args.hf_token or os.environ.get("HF_TOKEN")

    print("==================================================================")
    print("  KBS Q1 RESEARCH BENCHMARK: ONTOLOGY-CONSTRAINED AGENT DECODING  ")
    print("==================================================================")
    print(f"Target Model       : {args.model}")
    print(f"Sample Count       : {args.samples}")
    print(f"Ontology Config    : {args.config}")
    print(f"Device             : {args.device}")
    print(f"Simulation Mode    : {args.mock}")
    print("------------------------------------------------------------------")

    # Step 1: Ingest Ontology
    print("[1/5] Loading Enterprise RBAC Security Ontology...")
    ontology = load_ontology_from_json(args.config)
    print(f"      Loaded {len(ontology.roles)} roles with {len(ontology.global_security_axioms)} global axioms.")

    # Step 2: Ingest Benchmark Dataset
    print(f"[2/5] Loading Enterprise Business Benchmark Suite ({args.samples} samples)...")
    loader = BenchmarkDatasetLoader(seed=42)
    dataset = loader.load_benchmark_split(total_samples=args.samples)
    print(f"      Ingested {len(dataset)} balanced enterprise business cases.")

    # Step 3: Initialize Model Harnesses (Sharing single GPU instance)
    print("[3/5] Initializing Single GPU Model Instance (Zero CPU Offloading)...")
    evaluator = BenchmarkEvaluator(ontology)

    m0_vanilla = VanillaAgent(
        model_name=args.model,
        device=args.device,
        is_mock=args.mock,
        hf_token=hf_token
    )

    # M1 and M2 share the exact same GPU weights and tokenizer
    m1_prompt = PromptGuardedAgent(
        model_name=args.model,
        device=args.device,
        is_mock=args.mock,
        hf_token=hf_token,
        shared_model=m0_vanilla.model,
        shared_tokenizer=m0_vanilla.tokenizer
    )

    m2_posthoc = PostHocClassifierAgent(
        base_agent=m0_vanilla,
        is_mock=args.mock
    )

    m_star_proposed = OntologyConstrainedAgent(
        model_name=args.model,
        ontology=ontology,
        device=args.device,
        is_mock=args.mock,
        hf_token=hf_token
    )

    # Step 4: Run Comparative Evaluations
    print("[4/5] Executing Comparative Benchmarks across 4 Conditions...")
    results = []

    print("      -> Evaluating M0: Vanilla Unconstrained Agent...")
    res_m0 = evaluator.evaluate_harness("M0 (Vanilla Base LLM)", m0_vanilla, dataset)
    results.append(res_m0)

    print("      -> Evaluating M1: In-Context Prompt-Guarded Agent...")
    res_m1 = evaluator.evaluate_harness("M1 (Prompt Guard)", m1_prompt, dataset)
    results.append(res_m1)

    print("      -> Evaluating M2: Post-Hoc Classifier Guardrail...")
    res_m2 = evaluator.evaluate_harness("M2 (Post-Hoc Classifier)", m2_posthoc, dataset)
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
    print(f"      Effect Size (r): {wilcoxon_test.get('effect_size_r', 0.0):.3f}")
    print(f"      Interpretation: {wilcoxon_test.get('interpretation')}")

    # Export LaTeX Tables & Figures
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tex_table1 = str(out_dir / "table1_main_results.tex")
    StatisticalReporter.export_latex_table(results, tex_table1)

    tex_table2 = str(out_dir / "table2_category_ablation.tex")
    StatisticalReporter.export_category_ablation_table(results, tex_table2)

    StatisticalReporter.export_publication_plots(results, str(out_dir / "plots"))

    # Export Detailed JSON
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
    print("\n[SUCCESS] Elite Q1 Benchmark complete! All LaTeX tables and vector figures generated.")


if __name__ == "__main__":
    main()
