#!/usr/bin/env python3
"""Reviewer driver: run a subset of the SRP planted-defect table (srp_mutants.DEFECTS) plus reviewer probes.

usage: talker_campaign.py --repo CLONE --root OUT --interfaces {1,2} [--prefix talker-] [--shard K/N] [--probes]

Plants each defect into a copy of CLONE/sw/firmware/ctrl under OUT (never into CLONE), runs its named test through
the repository's own srp_mutants.campaign, and prints [ok]/[ESCAPED] lines. With --probes it instead runs the
reviewer's own probe defects (below) against whole test groups and reports whether ANY test failed (rc 1) or not.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


PROBES = (
    # name, path, old, new, suite, gtest filter
    ("probe-hold-off-without-jointime", "srp/srp_mbx.c",
     "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)",
     "#define SRP_REDECLARE_CS (2u * 1000u + (CTRL_LOOP_TX_MS + 9u) / 10u)", "srp_talker.cpp", "Talker.*"),
    ("probe-hold-off-exactly-two-leaveall", "srp/srp_mbx.c",
     "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)",
     "#define SRP_REDECLARE_CS (2u * 1000u)", "srp_talker.cpp", "Talker.*"),
    ("probe-hold-off-short-by-150cs", "srp/srp_mbx.c",
     "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)",
     "#define SRP_REDECLARE_CS (2u * 1000u - 150u)", "srp_talker.cpp", "Talker.*"),
    ("probe-hold-off-short-by-150cs-composed", "srp/srp_mbx.c",
     "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)",
     "#define SRP_REDECLARE_CS (2u * 1000u - 150u)", "test_acmp_mbx.cpp", "SrpGate.*"),
    ("probe-gate-of-interface-0-everywhere", "app/ctrl_app_srp.c",
     "app->maap.published_gate[interface],", "app->maap.published_gate[0],", "test_acmp_mbx.cpp", "SrpGate.*"),
    ("probe-swap-leaves-before-join", "srp/srp_mbx.c",
     "        if (valid && !waits && (how != SRP_DECLARE_CHANGED || (i->talkers & bit) == 0u || admitted != was)) {\n",
     "        if ((i->talkers & bit) != 0u && valid && admitted != was) {\n"
     "            (void)mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,&value);\n"
     "        }\n"
     "        if (valid && !waits && (how != SRP_DECLARE_CHANGED || (i->talkers & bit) == 0u || admitted != was)) {\n",
     "srp_talker.cpp", "Talker.*"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--interfaces", type=int, choices=(1, 2), required=True)
    ap.add_argument("--prefix", default="talker-")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--probes", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    sys.path.insert(0, str(a.repo / "sw/firmware/ctrl/test"))
    import srp_mutants  # noqa: E402  (the repository's own driver)
    from ctrl_build import CTRL, ROOT, Tree  # noqa: E402
    from srp_arms import arm_srp  # noqa: E402
    import fw_gtest  # noqa: E402
    k, n = (int(x) for x in a.shard.split("/"))
    lwsrp = (a.repo / "third_party/lwSRP").resolve()
    if not a.probes:
        chosen = [d for d in srp_mutants.DEFECTS if d.name.startswith(a.prefix)]
        chosen = chosen[k::n]
        print(f"defects selected: {len(chosen)} (shard {a.shard}, prefix {a.prefix!r}, interfaces {a.interfaces})",
              flush=True)
        srp_mutants.DEFECTS = tuple(chosen)
        failed = srp_mutants.campaign(a.root, lwsrp, a.jobs, a.interfaces)
        return 1 if failed else 0
    build = fw_gtest.Build(jobs=a.jobs)
    a.root.mkdir(parents=True, exist_ok=True)
    for name, path, old, new, suite, filt in PROBES[k::n]:
        out = a.root / ("work-" + name)
        src = out / "ctrl"
        shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        target = src / path
        text = target.read_text()
        if text.count(old) != 1:
            print(f"[REFUSED] {name}: {text.count(old)} planting sites", flush=True)
            continue
        target.write_text(text.replace(old, new))
        cfg = {"config": ROOT / "configs/endstation_ax7101_8x8.yaml"} if a.interfaces == 2 else {}
        result = arm_srp(Tree(src, out / "build", out / "reuse", build), lwsrp, a.interfaces, test=(suite, filt), **cfg)
        (a.root / (name + ".log")).write_text(result.log)
        fails = [ln.strip() for ln in result.log.splitlines() if ln.strip().startswith("[FAIL] ")]
        verdict = "CAUGHT" if result.rc != 0 else "ESCAPED"
        print(f"[{verdict}] {name} ({suite} {filt}, if{a.interfaces}) rc {result.rc}; failing: {sorted(set(fails))[:6]}",
              flush=True)
        shutil.rmtree(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
