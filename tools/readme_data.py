"""Derive README / video numbers from the full 113-task baseline job (jobs/2026-11-06__20-44-10) and the 10-task smoke job.
Writes results/derived/readme_data.json."""
import json, glob, os, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FULL = "jobs/2026-11-06__20-44-10"; SMOKE = "jobs/2026-11-06__14-09-57"
def job(j):
    d = json.load(open(os.path.join(ROOT, j, "result.json")))
    ev = list(d["stats"]["evals"].values())[0]
    m = ev["metrics"][0]
    return {"n_tasks": d["n_total_trials"], "n_verified": ev["n_trials"], "n_errored": d["stats"]["n_errored_trials"],
            "solved": m["reward"] * d["n_total_trials"], "partial": m["partial"], "f2p": m["f2p"], "p2p": m["p2p"],
            "f2p_passed": m["f2p_passed"], "f2p_total": m["f2p_total"], "p2p_passed": m["p2p_passed"], "p2p_total": m["p2p_total"],
            "wall_s": None}
out = {"full": job(FULL), "smoke": job(SMOKE)}
trials = [json.load(open(f)) for f in glob.glob(os.path.join(ROOT, FULL, "*", "result.json"))]
part = [t["verifier_result"]["rewards"]["partial"] for t in trials if t.get("verifier_result")]
bins = [("0", lambda p: p == 0), ("0 to 0.25", lambda p: 0 < p <= .25), ("0.25 to 0.5", lambda p: .25 < p <= .5),
        ("0.5 to 0.75", lambda p: .5 < p <= .75), ("0.75 to 0.9", lambda p: .75 < p <= .9), ("0.9 to 1", lambda p: .9 < p)]
out["hist"] = [{"bin": b, "tasks": sum(1 for p in part if f(p))} for b, f in bins]
out["n_part"] = len(part)
out["high"] = sum(1 for p in part if p > .9)
out["zero"] = sum(1 for p in part if p == 0)
out["perfect_partial"] = sum(1 for p in part if p >= .999)
steps = [t["agent_result"]["n_agent_steps"] for t in trials if t.get("agent_result") and t["agent_result"].get("n_agent_steps")]
out["avg_steps"] = sum(steps) / len(steps)
ex = collections.Counter((t["exception_info"] or {}).get("exception_type", "error") if t.get("exception_info") else "ok" for t in trials)
names = {"ok": "finished, verified", "NonZeroAgentExitCodeError": "agent exited non-zero", "ConflictError": "sandbox conflict (Modal)", "VerifierTimeoutError": "verifier timeout"}
out["outcomes"] = [{"outcome": names.get(k, k), "trials": v} for k, v in ex.most_common()]
out["f2p_vs_p2p"] = [{"metric": "tests that must pass after the fix (f2p)", "rate": out["full"]["f2p"]},
                     {"metric": "tests that must keep passing (p2p)", "rate": out["full"]["p2p"]},
                     {"metric": "partial score", "rate": out["full"]["partial"]}]
os.makedirs(os.path.join(ROOT, "results", "derived"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "results", "derived", "readme_data.json"), "w"), indent=1)
print(json.dumps({k: out[k] for k in ("full", "hist", "avg_steps", "outcomes", "perfect_partial")}, indent=1))
