#!/usr/bin/env python3
"""Re-execute the committed tb/srp_top/mutants.py campaign in partitions.

The committed driver runs every arm sequentially. To keep each foreground
command bounded, the arms are split round-robin into PARTS partitions and one
batch of partitions runs concurrently (at most 8 driver processes). Each
partition invokes the unmodified committed driver from the head extraction with
--only, so each partition re-runs its own positive controls first. Coverage of
the K1..O8 assertion families is recomputed here as the union of the tags of
killed arms across all partitions (the committed driver computes it only for an
unpartitioned run).

usage: r375_campaign.py batch <index> | summary
"""
import ast
import concurrent.futures as cf
import os
from pathlib import Path
import re
import subprocess
import sys

PKT = Path(__file__).resolve().parents[1]
HEAD = PKT / "scratch" / "head"
OUT = PKT / "receipts" / "campaign"
PINNED = os.environ.get("R375_PINNED_BIN",
                        "$VALIDATION_STORAGE/pp127-manager-0404675d/pinned-tool-bin")
PARTS = 14
PER_BATCH = 7


def arms() -> list[tuple]:
    """Read the MUTANTS table of the committed driver without importing it."""
    tree = ast.parse((HEAD / "tb" / "srp_top" / "mutants.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and node.targets[0].id == "MUTANTS":
            return ast.literal_eval(node.value)
    raise SystemExit("MUTANTS table not found")


def run_part(index: int, labels: list[str]) -> str:
    """Run one partition through the committed driver and keep its receipt."""
    out = OUT / f"part{index:02d}"
    out.mkdir(parents=True, exist_ok=True)
    tmp = PKT / "scratch" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PATH=PINNED + ":" + os.environ["PATH"], TMPDIR=str(tmp))
    with (OUT / f"part{index:02d}.driver.log").open("w") as log:
        rc = subprocess.run([sys.executable, str(HEAD / "tb" / "srp_top" / "mutants.py"),
                             "--output", str(out), "--only", ",".join(labels)],
                            stdout=log, stderr=subprocess.STDOUT, env=env,
                            check=False).returncode
    return f"part{index:02d} rc={rc} arms={','.join(labels)}"


def summary() -> int:
    """Union the per-partition driver results into one campaign verdict."""
    table = arms()
    verdict = {}
    controls = []
    for log in sorted(OUT.glob("part*.driver.log")):
        for line in log.read_text().splitlines():
            m = re.match(r"^([\w-]+): rc=(-?\d+) failures=(\d+) (KILLED|UNPROVEN) tags=(.*)$", line)
            if m:
                verdict[m.group(1)] = (m.group(4), int(m.group(3)), m.group(5))
            if line.startswith("control "):
                controls.append(f"{log.name}: {line}")
    covered = set()
    lines = []
    for label, suite, group, expected in table:
        state, fails, tags = verdict.get(label, ("MISSING", 0, ""))
        named = expected.rstrip(":")
        if state == "KILLED":
            covered.update(t for t in tags.split(",") if t)
        lines.append(f"{label}\t{suite}\t{group or '-'}\trequired={named}\t{state}\tfailures={fails}\ttags={tags}")
    families = {f"{g}{i}" for g, n in [("K", 12), ("L", 4), ("M", 12), ("N", 13), ("O", 8)]
                for i in range(1, n + 1)}
    missing = sorted(families - covered)
    killed = sum(1 for v in verdict.values() if v[0] == "KILLED")
    bad_controls = [c for c in controls if not c.endswith("PASS")]
    print("\n".join(controls))
    print("\n".join(lines))
    print(f"arms: {killed}/{len(table)} KILLED; controls: {len(controls) - len(bad_controls)}/"
          f"{len(controls)} PASS; family coverage {len(families) - len(missing)}/{len(families)} "
          f"missing={missing}")
    return int(bool(bad_controls) or killed != len(table) or bool(missing))


def main() -> int:
    """Dispatch a batch of partitions or print the campaign summary."""
    if sys.argv[1:2] == ["summary"]:
        return summary()
    batch = int(sys.argv[2])
    labels = [a[0] for a in arms()]
    parts = [labels[i::PARTS] for i in range(PARTS)]
    chosen = range(batch * PER_BATCH, min(PARTS, (batch + 1) * PER_BATCH))
    OUT.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=PER_BATCH) as pool:
        for result in pool.map(lambda i: run_part(i, parts[i]), chosen):
            print(result, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
