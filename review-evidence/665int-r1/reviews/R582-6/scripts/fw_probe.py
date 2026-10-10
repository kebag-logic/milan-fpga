#!/usr/bin/env python3
"""fw_probe.py - run the SRP firmware arms of a disposable clone of the head, optionally with source edits.

Usage:
  python3 -I fw_probe.py CLONE LWSRP OUT [--edit PATH OLD NEW]... [--interfaces 1 2]

CLONE is a disposable git clone of the head under review (with its
protocol-processor submodule at the pin), never the review checkout. Each
edit is applied there (its OLD text must occur exactly once), the SRP arms the
firmware gate runs for each interface count are built under OUT and run, and
the edited files are restored with git checkout. Prints one line per arm and
exits 0 when every arm passed, 1 when one failed, 2 on a refusal.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SUITES = ("srp_mbx.cpp", "srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp", "srp_latency.cpp", "srp_walk.cpp")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base", type=Path)
    ap.add_argument("lwsrp", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--edit", nargs=3, action="append", default=[], metavar=("PATH", "OLD", "NEW"))
    ap.add_argument("--interfaces", type=int, nargs="+", default=[1, 2])
    ap.add_argument("--suites", nargs="+", default=list(SUITES))
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    tree_root = args.base
    for path, old, new in args.edit:
        old, new = old.encode().decode("unicode_escape"), new.encode().decode("unicode_escape")
        f = tree_root / path
        text = f.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"REFUSED: the edit's old text occurs {text.count(old)} times in {path}")
            return 2
        f.write_text(text.replace(old, new), encoding="utf-8")
        print(f"edit applied: {path}")
    test_dir = tree_root / "sw/firmware/ctrl/test"
    sys.path[:0] = [str(test_dir), str(tree_root / "sw/firmware/gtest")]
    import fw_gtest  # noqa: E402
    import srp_arms  # noqa: E402
    from ctrl_build import CTRL, Refusal, Tree  # noqa: E402
    from ctrl_reuse import cut_reuse  # noqa: E402
    assert CTRL.resolve().is_relative_to(tree_root.resolve()), CTRL
    build = args.out / "build"
    tree = Tree(CTRL, build / "checkout", build / "reuse", fw_gtest.Build(jobs=args.jobs))
    cut_reuse(tree.reuse)
    failed = False
    try:
        for i in args.interfaces:
            for suite in args.suites:
                o = srp_arms.arm_srp(tree, args.lwsrp.resolve(), i, test=suite)
                print(f"[{'ok' if o.rc == 0 else 'FAIL'}] arm {o.arm}", flush=True)
                if o.rc:
                    failed = True
                    for ln in o.log.splitlines():
                        if "[FAIL]" in ln or "FAILED" in ln or "Failure" in ln:
                            print(f"    {ln.strip()[:220]}")
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        return 2
    finally:
        for path, _old, _new in args.edit:
            subprocess.run(["git", "-C", str(tree_root), "checkout", "--", path], check=True)
            print(f"restored: {path}")
    print(f"fw_probe: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
