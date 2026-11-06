# DeepSWE v1.1 x North-Mini-Code (2026-11-06)
Arm 1 (NOW): baseline = stock North-Mini-Code-1.0-fp8, 1xH100 Modal, default vLLM (serve_baseline.py).
Arm 2 (LATER, only after baseline done): our optimizations (best-claim: FP8 KV, no spec, chunk 1024, 2 TP1 replicas + prefix-affine router).
Runner: pier run -p deep-swe/tasks --agent mini-swe-agent --env modal ; smoke = --n-tasks 10 --sample-seed 0.
Note: Modal HF-token secret copy denied by classifier; model fetched unauthenticated.

## Baseline smoke (10 tasks, seed 0) - job jobs/2026-11-06__12-22-56 (run 4; runs 1-3 were plumbing failures)
Fixes needed: MSWEA_API_KEY=x; --ak extra_python_packages=["mcp"]; endpoint must be in config_file (north-baseline.yaml) so pier allowlists it.
Result: pass@1 0/10, mean partial 0.49. 2 trials hit ContextWindowExceeded (server max-model-len 98304 = my choice).
p2p=0 on fastapi/meriyah/query-persist: suspect broken patch/build, not yet inspected.

## Run 5 (262k ctx) job 2026-11-06__14-09-57: see results above in transcript; committed.
