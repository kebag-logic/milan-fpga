#!/usr/bin/env python3
"""Regenerate all five configurations at dev 0eff6d2e and at the reviewed head
from `git archive` exports, and compare every emitted file byte for byte.

Usage: regen_compare.py CLONE WORKDIR
Also checks that each emitted adp_shape_defaults.svh equals the committed copy.
Exit 0 only when both exports emit identical, non-empty file sets.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

DEV = "0eff6d2ee3818a6d2b1f1fdcd0084d81b28f247a"
HEAD = "6c5ca18f12191a252447ec7c7c75363b851f2771"
CONFIGS = ["endstation_arty_4x4", "endstation_arty_8ch", "endstation_arty_current",
           "endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"]


def export(clone: Path, commit: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=False)
    arch = subprocess.run(["git", "-C", str(clone), "archive", commit], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(dest)], input=arch.stdout, check=True)
    # The builder reads the gPTP generator; export each gitlink at its pinned
    # commit from the clone's initialised submodule (both commits pin the same).
    for sub in ("gptp-processor", "protocol-processor"):
        pin = subprocess.run(["git", "-C", str(clone), "rev-parse", f"{commit}:{sub}"],
                             capture_output=True, text=True, check=True).stdout.strip()
        arch = subprocess.run(["git", "-C", str(clone / sub), "archive", pin],
                              capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(dest / sub)], input=arch.stdout, check=True)


def generate(tree: Path, out: Path) -> dict[str, str]:
    for cfg in CONFIGS:
        r = subprocess.run([sys.executable, "-B", "sw/builder/endstation_builder.py",
                            f"configs/{cfg}.yaml", "-o", str(out)], cwd=tree,
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"{tree.name} {cfg}: rc {r.returncode}\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
    return {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(out.rglob("*")) if p.is_file()}


def main() -> int:
    clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    results = {}
    for name, commit in (("dev", DEV), ("head", HEAD)):
        tree = work / f"{name}-tree"
        export(clone, commit, tree)
        results[name] = generate(tree, work / f"{name}-out")
    dev, head = results["dev"], results["head"]
    bad = 0
    for path in sorted(set(dev) | set(head)):
        same = dev.get(path) == head.get(path)
        bad += not same
        print(f"[{'ok' if same else 'DIFF'}] {path} {head.get(path, 'absent')}")
    for cfg in CONFIGS:
        emitted = work / "head-out" / cfg / "adp_shape_defaults.svh"
        committed = work / "head-tree/configs/generated" / cfg / "gen/adp_shape_defaults.svh"
        same = emitted.is_file() and emitted.read_bytes() == committed.read_bytes()
        bad += not same
        print(f"[{'ok' if same else 'DIFF'}] emitted {cfg} shape header equals the committed copy")
    print(f"{len(head)} head artifacts, {len(dev)} dev artifacts, {bad} difference(s)")
    return 1 if bad or not head else 0


if __name__ == "__main__":
    sys.exit(main())
