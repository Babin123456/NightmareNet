## Summary

Implements multi-model ensemble robustness benchmarking to compare adversarial resistance across architectures.

## Motivation

Closes #29

Currently, the suite only evaluates a single model. This PR introduces an `EnsembleOrchestrator` to evaluate multiple models iteratively via a configuration file, perform Pareto analysis, generate degradation curves, and format results.

## Changes

- Defined Pydantic schema for ensemble configuration in `ensemble_benchmark.py`
- Implemented `EnsembleOrchestrator` to run models in isolated sub-processes (respecting 4GB VRAM limits)
- Added `pareto_analysis.py` to compute Pareto frontier (robustness vs. latency vs. params)
- Added `degradation_curves.py` for aggregation
- Added `format_results.py` to output JSON, CSV, and LaTeX tables
- Updated `cli.py` to support `benchmark --config`

## Acceptance Criteria

- [x] Ensemble config YAML schema defined and validated (via Pydantic)
- [x] CLI accepts ensemble configs
- [x] 3+ models benchmarked in a single run with comparative output (supported by orchestrator)
- [x] Degradation curves generated (JSON + optional PNG)
- [x] Pareto analysis identifies optimal tradeoff
- [x] LaTeX table auto-generated
- [ ] Results cached for incremental re-runs (future improvement)
- [x] Works within 4GB VRAM (sequential loading via ProcessPoolExecutor)
- [ ] Frontend ensemble view (or data contract for future) (UI/React changes not in this PR scope)
- [x] Tests: at least 5 unit tests for orchestration logic

## Type

- [x] Feature (non-breaking change that adds functionality)

## Pre-submission Checklist

- [x] I have **starred** this repository
- [x] I have **followed** [@Adit-Jain-srm](https://github.com/Adit-Jain-srm)
- [x] I have read [CONTRIBUTING.md](https://github.com/Adit-Jain-srm/NightmareNet/blob/main/CONTRIBUTING.md)

## Quality Checklist

- [x] `ruff check nightmarenet/ tests/` passes with 0 errors
- [x] `mypy nightmarenet/ --ignore-missing-imports` passes
- [x] `pytest tests/` — all tests pass
- [x] Added tests for new functionality (if applicable)
- [x] Updated documentation (if applicable)
- [x] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [x] All acceptance criteria from the linked issue are satisfied (or exceptions noted above)

## Screenshots (if UI change)
N/A
