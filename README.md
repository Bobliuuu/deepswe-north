# deepswe-north

DeepSWE v1.1 x **North-Mini-Code-1.0-fp8** (`CohereLabs/North-Mini-Code-1.0-fp8`).

| Arm | What | Status |
|---|---|---|
| 1. Baseline | stock model, 1xH100 Modal, default vLLM (`serve_baseline.py`) | smoke-10 done |
| 2. Optimized | north-star / inference-experiment optimizations (`optimized/`) | in progress |

## Baseline (smoke: 10 tasks, `--sample-seed 0`, 262k ctx, mini-swe-agent) - job `jobs/2026-11-06__14-09-57`
- pass@1 (reward): **0/10**
- mean partial: **0.580** (f2p 0.017, p2p 0.798)
- runtime 15m36s, 0 errored trials

Runner: `pier run -p deep-swe/tasks --agent mini-swe-agent --env modal --config north-baseline.yaml`
(`pier/` and `deep-swe/` are upstream clones, gitignored.) See `NOTES.md` for plumbing fixes.
