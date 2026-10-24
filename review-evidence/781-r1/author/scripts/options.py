"""What each out-of-scope remedy needs, from the checker's own balance()."""
import math, sys
sys.path.insert(0, sys.argv[1])
import suite_shards as s
suites = s.expand_suites(s.sweep_suites(s.SUITE_ROOT))
for figure in (1240, 1500, 1800):
    table = {**s.SUITE_SECONDS, "media_phase": figure}
    _, load16 = s.balance(suites, 16, table, (122,) * 16)
    reg16 = max(load16[:-1])
    print(f"figure {figure} s:")
    print(f"  16 workers: busiest regular worker {reg16} s (bound 1620 s); "
          f"needs regular timeout-minutes >= {math.ceil(reg16 / 36)} AND the absolute "
          f"1620 s rule raised to >= {reg16} s; balanced demand {sum(load16[:-1])} s vs capacity 24300 s")
    _, load17 = s.balance(suites, 17, table, (122,) * 17)
    owners, _ = s.balance(suites, 17, table, (122,) * 17)
    print(f"  17 workers (worker 16 = media-clock leg A alone): regular max {max(load17[:-1])} s, "
          f"min {min(load17[:-1])} s, last {load17[-1]} s; media_phase on worker {owners['media_phase']}")
