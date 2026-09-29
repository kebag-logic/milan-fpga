#!/usr/bin/env python3
"""Reproduce the #387 page's published peer-delay claim from the raw consoles.

Claim (docs/findings/387_SOFTWARE_GM_STEP.md, deviation section): in the
console sample where asCapable cleared, the DUT's published peer delay read
0 ns at all five takeovers and 4,039-4,701 ns at all five releases, and
373-389 ns in every other sample of the five runs.

Inputs, hash-checked first: gmNN/console.jsonl (every 250 ms `milan_status`
round: PDELAY_NS, ASCAPABLE, SYNC, TU, GPTP_GM) and gmNN/events.jsonl (the
software-grandmaster start). Times are seconds after that start, as on the
page. The grandmaster is printed by role, never by clock identity.

usage: extract_pdelay.py <raw-root> <repo-at-head>
"""
import sys

from b1r2_common import Inputs, gm_role, jsonl, status_fields

RUNS = ["gm01", "gm02", "gm03", "gm04", "gm05"]


def main():
    inp = Inputs(sys.argv[1], sys.argv[2])
    clears = {"takeover": [], "release": []}
    other = []
    anomalous_total = 0
    for run in RUNS:
        ev = jsonl(inp.path(f"{run}/events.jsonl"))
        t0 = next(e["t"] for e in ev if e["kind"] == "gm-start")
        rows = [r for r in jsonl(inp.path(f"{run}/console.jsonl")) if r["cmd"] == "milan_status"]
        samples = []
        for r in rows:
            f = status_fields(r["raw"])
            samples.append((r["t"] - t0, int(f["ASCAPABLE"]), int(f["PDELAY_NS"]), gm_role(f["GPTP_GM"])))
        edges = [i for i in range(1, len(samples)) if samples[i - 1][1] == 1 and samples[i][1] == 0]
        print(f"{run}: {len(samples)} samples, asCapable 1->0 at {len(edges)} samples")
        if len(edges) != 2:
            print(f"FAIL {run}: expected two asCapable clears, one per edge")
            sys.exit(1)
        marked = set()
        for kind, i in zip(("takeover", "release"), edges):
            t, _, pd, gm = samples[i]
            j = i
            while j < len(samples) and samples[j][2] == pd:
                marked.add(j)
                j += 1
            # the published value may already read the same one sample earlier
            k = i - 1
            while k >= 0 and samples[k][2] == pd and samples[k][1] == 0:
                marked.add(k)
                k -= 1
            print(f"  {kind:8s} clear at {t:6.2f} s: PDELAY_NS {pd}, GM {gm}; "
                  f"that value held for {j - k - 1} samples, {samples[k + 1][0]:.2f}-{samples[j - 1][0]:.2f} s")
            clears[kind].append(pd)
        rest = [s[2] for n, s in enumerate(samples) if n not in marked]
        anomalous_total += len(marked)
        print(f"  every other sample: {len(rest)} samples, PDELAY_NS {min(rest)}-{max(rest)}")
        other += rest
    print()
    print(f"takeover clears: {clears['takeover']} ns")
    print(f"release clears:  {clears['release']} ns, range {min(clears['release'])}-{max(clears['release'])}")
    print(f"every other sample of the five runs: {len(other)} samples, {min(other)}-{max(other)} ns "
          f"({anomalous_total} samples carried a clear value)")
    ok = (clears["takeover"] == [0] * 5 and min(clears["release"]) == 4039 and max(clears["release"]) == 4701
          and min(other) == 373 and max(other) == 389)
    print("CLAIM 0 / 4,039-4,701 / 373-389 ns:", "REPRODUCED" if ok else "NOT REPRODUCED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
