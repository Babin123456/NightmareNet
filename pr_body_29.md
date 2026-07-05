Fixes #29.
This PR implements the multi-model ensemble orchestrator, allowing NightmareNet to evaluate multiple models iteratively. It includes:
- `configs/ensemble_benchmark.yaml` template schema with Pydantic validation.
- `pareto_analysis.py` for computing the Pareto frontier (Robustness vs. Latency).
- `degradation_curves.py` for aggregating results.
- `ensemble_benchmark.py` orchestrator with isolated sub-processes to respect VRAM limits.
- Updates to `cli.py` to support the benchmark suite.
- Comprehensive unit tests covering timeout limits, schema validation, and sequential loading logic.
