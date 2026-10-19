"""usage: r3_failsets.py <campaign> <base-out-dir> <head-out-dir> [--json <summary.json>]
Compare one mutation campaign's base and head records, mutants and baselines apart.

The roster is the campaign's results.json, never a glob of its logs. Each record is a
baseline (a run that plants nothing and must pass: notify, d3 and acmp name theirs
"golden-...", aecp_dispatch "control <target>" with no patch, name_state "golden") or a
planted mutant. Only mutants enter the unchanged, changed, added and removed totals; the
baselines are compared and reported on their own lines. A record's failure IDs are the
leading check ID of each failing check: results.json's failing_checks (notify, d3, acmp),
its runs' failures (name_state), or for aecp_dispatch, whose results.json keeps only a
count, the FAIL: lines of the arm's own log, which must match that count."""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ID = re.compile(r"(?:\[[^\]]*\]\s*)?([A-Za-z][A-Za-z0-9_.-]*)")


def check_id(text: str) -> str:
    """The leading check ID of one failing-check text."""
    return ID.search(text).group(1)


def dispatch_failures(out: Path, record: dict) -> list[str]:
    """An aecp_dispatch record's failing checks, from the log its driver names for it."""
    if "patch" in record:
        log = out / f"{record['arm']}.log"
    else:
        log = out / f"control-{record['arm'].removeprefix('control ')}.log"
    lines = [line[len("FAIL:"):].strip() for line in log.read_text(errors="replace").splitlines()
             if line.startswith("FAIL:")]
    if "patch" in record and len(lines) != record["failures"]:
        raise SystemExit(f"{log}: {len(lines)} FAIL: lines, results.json says {record['failures']}")
    return lines


def roster(campaign: str, out: Path) -> tuple[dict, dict, str]:
    """(mutants, baselines, results.json sha256): each maps a name to (verdict, failure IDs)."""
    raw = (out / "results.json").read_bytes()
    mutants, baselines = {}, {}
    for r in json.loads(raw):
        if campaign == "aecp_dispatch":
            name = r["arm"]
            baseline = name.startswith("control ")
            if baseline == ("patch" in r):
                raise SystemExit(f"{campaign} {name}: name and patch disagree on baseline")
            fails = dispatch_failures(out, r)
        elif campaign == "name_state":
            name = r["name"]
            baseline = name == "golden"
            fails = [f for run in r["runs"] for f in run["failures"]]
        else:
            name = r["mutant"]
            baseline = name.startswith("golden-")
            if baseline != (r["named_checks"] == []):
                raise SystemExit(f"{campaign} {name}: name and named_checks disagree on baseline")
            fails = r["failing_checks"]
        side = baselines if baseline else mutants
        if name in side:
            raise SystemExit(f"{campaign} {name}: listed twice")
        side[name] = (r["verdict"], sorted(check_id(f) for f in fails))
    return mutants, baselines, hashlib.sha256(raw).hexdigest()


def compare(base: dict, head: dict) -> dict:
    """Names unchanged (same verdict and failure-ID multiset), changed, added and removed."""
    common = set(base) & set(head)
    changed = sorted(n for n in common if base[n] != head[n])
    return {"unchanged": len(common) - len(changed), "changed": changed,
            "added": sorted(set(head) - set(base)), "removed": sorted(set(base) - set(head))}


def ids(v: list[str]) -> str:
    """A failure-ID multiset as 'count: ID, ID...'."""
    return f"{len(v)}: {', '.join(f'{k} x{n}' if n > 1 else k for k, n in sorted(Counter(v).items()))}"


def main() -> int:
    """Print the comparison; with --json, also write its populations as a summary."""
    campaign, base_dir, head_dir = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    summary_path = Path(sys.argv[sys.argv.index("--json") + 1]) if "--json" in sys.argv else None
    bm, bb, bsha = roster(campaign, base_dir)
    hm, hb, hsha = roster(campaign, head_dir)
    m, b = compare(bm, hm), compare(bb, hb)
    print(f"campaign {campaign}")
    print(f"base results.json sha256 {bsha}")
    print(f"head results.json sha256 {hsha}")
    for side, mut, bas in (("base", bm, bb), ("head", hm, hb)):
        print(f"{side}: {len(mut)} mutants {dict(Counter(v for v, _ in mut.values()))}, "
              f"{len(bas)} baselines {dict(Counter(v for v, _ in bas.values()))}")
    print(f"MUTANTS: {m['unchanged']} unchanged, {len(m['changed'])} changed, "
          f"{len(m['added'])} added, {len(m['removed'])} removed")
    for n in m["changed"]:
        print(f"  CHANGED {n}: base {ids(bm[n][1])}")
        print(f"          {' ' * len(n)}  head {ids(hm[n][1])}")
    for n in m["added"]:
        print(f"  ADDED {n} ({hm[n][0]}): {ids(hm[n][1])}")
    for n in m["removed"]:
        print(f"  REMOVED {n} ({bm[n][0]}): {ids(bm[n][1])}")
    clean = sum(1 for n in set(bb) & set(hb) if bb[n] == hb[n] == ("PASS", []))
    print(f"BASELINES (not mutants): {b['unchanged'] + len(b['changed'])} at both, {clean} PASS "
          f"with no failing check at both, {len(b['changed'])} changed, {len(b['added'])} added, "
          f"{len(b['removed'])} removed")
    for n in sorted(set(bb) | set(hb)):
        print(f"  baseline {n}: base {bb.get(n, ('absent',))[0]}, head {hb.get(n, ('absent',))[0]}")
    if summary_path:
        summary_path.write_text(json.dumps({
            "campaign": campaign, "base_sha256": bsha, "head_sha256": hsha,
            "base_mutants": len(bm), "head_mutants": len(hm),
            "base_baselines": len(bb), "head_baselines": len(hb),
            "mutants": m, "baselines": b, "baselines_clean_at_both": clean}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
