"""Usage: python3 -I shard_predict.py <repo>; prints predicted worker seconds from the repo's own suite_shards tables."""
import importlib.util, subprocess, sys
repo = sys.argv[1]
spec = importlib.util.spec_from_file_location("ss", f"{repo}/scripts/suite_shards.py")
ss = importlib.util.module_from_spec(spec); spec.loader.exec_module(ss)
bound = 120 * 60 * ss.HEADROOM_PERCENT // 100
print("bound_s", bound, "maap_s", ss.SUITE_SECONDS.get("maap"))
for i in range(5):
    out = subprocess.run([sys.executable, "-I", f"{repo}/scripts/suite_shards.py", "--suite-root", f"{repo}/tb/verilator", "--shard", f"{i}/5"], capture_output=True, text=True, check=True).stdout.split()
    t = ss.WORKER_OVERHEAD_SECONDS[i] + sum(ss.SUITE_SECONDS[s] for s in out)
    print(f"worker {i}: suites={len(out)} predicted_s={t} within={t <= bound} maap={'maap' in out}")
