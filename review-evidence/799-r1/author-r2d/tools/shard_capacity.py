#!/usr/bin/env python3
"""Shard-timing analysis for #799 round 2. Run from the lane root:
    python3 -I <this> <measure-dir>
<measure-dir> holds one `suite_shards.py --measure` output per hosted run,
named measure-<run>.txt. Reads scripts/suite_shards.py of the checkout."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts").resolve()))
import suite_shards as s

LANE = ("40724689169", "40740015218")          # this PR, ca39dc1b and 4f3ebffb
OTHER = ("40449656086", "40460559108", "40724442337", "40745912014")
# suites whose Makefile compiles RTL or test sources this PR changes
TOUCHED = ("aaf aaf_audio_loop avtp_parser capture_coherence chmap_capture csr "
           "follow_ring maap mbx media_phase milan_dp milan_dp_mclk "
           "milan_dp_render nvm_backend nvm_cosim pp_shadow tdm").split()
FOLLOW_RING = 1493   # no completed window at this head (cut at >1356 s);
                     # largest complete hosted window, dev run 40460559108

def load(directory, run):
    text = (Path(directory) / f"measure-{run}.txt").read_text()
    return {k: int(v) for k, v in re.findall(r'"(\S+)": (\d+),', text)}

def main(directory):
    runs = {run: load(directory, run) for run in LANE + OTHER}
    lane = {}
    for run in LANE:
        for k, v in runs[run].items():
            lane[k] = max(v, lane.get(k, 0))
    suites = s.expand_suites(s.sweep_suites(s.SUITE_ROOT))
    print("== milan_dp legs: recorded vs hosted windows")
    print("run          " + "  ".join(f"leg{i}" for i in range(4)) + "  total")
    print("recorded     " + "  ".join(f"{v:4d}" for v in s.PIECE_SECONDS["milan_dp"])
          + f"  {sum(s.PIECE_SECONDS['milan_dp'])}")
    for run in OTHER + LANE:
        legs = [runs[run].get(f"milan_dp__{i}", 0) for i in range(4)]
        print(f"{run}  " + "  ".join(f"{v:4d}" for v in legs) + f"  {sum(legs)}"
              + ("  (this PR)" if run in LANE else ""))

    real = dict(s.SUITE_SECONDS); real.update(lane); real["follow_ring"] = FOLLOW_RING
    def simulate(table):
        owners, load_ = s.balance(suites, 17, table)
        at = [122 + sum(real[x] for x in suites if owners[x] == w) for w in range(17)]
        return max(load_[:-1]), at
    print("\n== plans against this PR's measured windows (regular limit 2700 s, bound 1620 s)")
    minimal = dict(s.SUITE_SECONDS); minimal["follow_ring"] = FOLLOW_RING
    for i in range(4):
        minimal[f"milan_dp__{i}"] = lane[f"milan_dp__{i}"]
    for name, table in (("head as recorded", s.SUITE_SECONDS),
                        ("milan_dp legs and follow_ring only", minimal)):
        predicted, at = simulate(table)
        print(f"{name}: predicted max {predicted} s; at measured windows max "
              f"{max(at[:-1])} s, workers over 1620 s: "
              f"{[(w, v) for w, v in enumerate(at[:-1]) if v > 1620]}")

    print("\n== capacity: every PR-touched figure replaced by its largest lane window")
    table = dict(s.SUITE_SECONDS); changed = []
    for k in table:
        if k.split("__")[0] in TOUCHED and k in lane and lane[k] != table[k]:
            changed.append((k, table[k], lane[k])); table[k] = lane[k]
    table["follow_ring"] = FOLLOW_RING
    for k, old, new in changed:
        print(f"  {k}: {old} -> {new}")
    print(f"  follow_ring: {s.SUITE_SECONDS['follow_ring']} -> {FOLLOW_RING}")
    for keep in (False, True):
        t = dict(table)
        if keep:
            t["media_phase"] = s.SUITE_SECONDS["media_phase"]
        regular = sum(t.values()) - t["milan_dp_mclk__0"]
        print(f"media_phase {t['media_phase']}: regular work {regular} s, capacity of 16 "
              f"regular workers {16 * (1620 - 122)} s")
        for total in (17, 18, 19):
            _, l = s.balance(suites, total, t, (122,) * total)
            print(f"  {total} workers: regular max {max(l[:-1])} s, min {min(l[:-1])} s,"
                  f" dedicated {l[-1]} s")

if __name__ == "__main__":
    main(sys.argv[1])
