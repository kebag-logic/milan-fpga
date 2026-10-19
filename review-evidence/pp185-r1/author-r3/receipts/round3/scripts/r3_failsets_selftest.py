"""usage: r3_failsets_selftest.py <comparison-script> [<old-script>]
Run a comparison script on synthetic campaign records with known populations and fail
(rc 1) on any wrong count. Cases: a baseline-only comparison (must give zero mutants), a
mixed comparison, an aecp_dispatch roster whose log disagrees with its count (must be
refused), and a record whose name and planted checks disagree (must be refused). With an
old script, also print what it reports for the baseline-only case."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def golden(name: str) -> dict:
    return {"mutant": name, "named_checks": [], "failing_checks": [], "verdict": "PASS"}


def mutant(name: str, fails: list[str]) -> dict:
    return {"mutant": name, "named_checks": [fails[0][:3]], "failing_checks": fails,
            "verdict": "KILLED"}


def write(d: Path, records: list[dict], logs: dict[str, str]) -> Path:
    d.mkdir(parents=True)
    (d / "results.json").write_text(json.dumps(records))
    for name, text in logs.items():
        (d / f"{name}.log").write_text(text)
    return d


def run(script: str, campaign: str, base: Path, head: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-I", script, campaign, str(base), str(head)],
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return r.returncode, r.stdout


def main() -> int:
    script = sys.argv[1]
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        g = [golden(f"golden-s{i}") for i in range(3)]
        glogs = {f"golden-s{i}": "10 checks: 10 PASS, 0 FAIL\n" for i in range(3)}
        b1, h1 = write(t / "b1", g, glogs), write(t / "h1", g, glogs)
        b2 = write(t / "b2", g[:2] + [mutant("m1", ["AA1: x"]), mutant("m2", ["BB1: y"]),
                                     mutant("m3", ["CC1: z"])], {})
        h2 = write(t / "h2", g[:2] + [mutant("m1", ["AA1: x"]), mutant("m2", ["BB1: y", "DD1: w"]),
                                     mutant("m3", ["CC1: z"]), mutant("m4", ["DD1: v"])], {})
        arm = {"arm": "a1", "patch": "a1", "target": "t", "rc": 2, "failures": 2, "named": 1,
               "verdict": "KILLED"}
        ctl = {"arm": "control t", "rc": 0, "verdict": "PASS"}
        dl = {"a1": "FAIL: RD1 one\n", "control-t": "5 checks: 5 PASS, 0 FAIL\n"}
        b3, h3 = write(t / "b3", [ctl, arm], dl), write(t / "h3", [ctl, arm], dl)
        odd = dict(golden("golden-x"), named_checks=["XX1"])
        b4, h4 = write(t / "b4", [odd], {}), write(t / "h4", [odd], {})
        cases = [
            ("baseline-only", "notify", b1, h1, 0,
             ["MUTANTS: 0 unchanged, 0 changed, 0 added, 0 removed", "3 baselines",
              "BASELINES (not mutants): 3 at both, 3 PASS"]),
            ("mixed", "d3", b2, h2, 0,
             ["base: 3 mutants", "head: 4 mutants", "2 baselines",
              "MUTANTS: 2 unchanged, 1 changed, 1 added, 0 removed", "CHANGED m2", "ADDED m4"]),
            ("dispatch count mismatch", "aecp_dispatch", b3, h3, 1,
             ["1 FAIL: lines, results.json says 2"]),
            ("name/plant disagreement", "notify", b4, h4, 1,
             ["name and named_checks disagree on baseline"]),
        ]
        for label, campaign, b, h, want_rc, words in cases:
            rc, out = run(script, campaign, b, h)
            missing = [w for w in words if w not in out]
            ok = (rc != 0) == (want_rc != 0) and not missing
            bad += not ok
            print(f"{'PASS' if ok else 'FAIL'}: {label}: rc {rc}"
                  + (f", missing {missing!r}" if missing else ""))
            if not ok:
                print("    " + out.replace("\n", "\n    "))
        if len(sys.argv) > 2:
            r = subprocess.run([sys.executable, "-I", sys.argv[2], str(b1), str(h1)], text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            print(f"old script on the baseline-only case: {r.stdout.strip()}")
    print(f"selftest: {4 - bad} of 4 cases PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
