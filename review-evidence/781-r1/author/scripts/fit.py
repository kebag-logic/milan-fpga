import sys
sys.path.insert(0, "scripts")
import suite_shards as s
suites = s.expand_suites(s.sweep_suites(s.SUITE_ROOT))
wf = s.WORKFLOW.read_text()
_, load, bounds = s.headroom_problems(suites, wf)
reg = load[:-1]
print("balanced load sum", sum(reg), "capacity", 15*1620, "slack", 15*1620-sum(reg))
last_ok = None
for v in range(900, 1901, 1):
    p, l, b = s.headroom_problems(suites, wf, {**s.SUITE_SECONDS, "media_phase": v})
    if not p: last_ok = v
    elif v in (901,1000,1100,1200,1500,1800) or (last_ok == v-1):
        print(v, "REFUSED:", p[0])
print("largest media_phase figure the 16-worker layout accepts:", last_ok)
