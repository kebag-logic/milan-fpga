#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Hold PR #228's owned surface to the bare-metal-only product policy (#259).

WHY THIS EXISTS. #259 (USER directive 2026-08-25) makes the product bare-metal
only: the Linux boot chain, the rootfs, and the ptp4l/phc2sys software gPTP
owner are retired. The repository-WIDE sweep of every Linux reference is
#259's own acceptance (scripts/check_baremetal_only.py there); THIS gate is
the focused version for the files the fabric-gPTP publication lane (#116,
PR #228) ships or rewrote, so that surface cannot quietly reacquire a retired
product claim while #259 is still open.

THE RULE. Over the owned file set below:

1. A retired daemon term (ptp4l, phc2sys, linuxptp) may appear only inside a
   paragraph that also carries a retirement anchor (``retired``, ``#259``,
   ``historical``, or ``verification-only``): naming the retired thing AS
   retired is documentation; naming it any other way is a resurrected claim.
   A paragraph is a blank-line-delimited block, because prose wraps.
2. No tracked product configuration may state ``fabric_gptp: false``: the
   option-off elaboration is verification-only and never a configuration.
3. No launcher recipe may pass ``--no-fabric-gptp``: the option-off
   elaboration is a direct milan_soc.py verification run, never a recipe.

A missing or unreadable inventory file is a FAILURE (rc 2), never a zero
count. ``--selftest`` plants each violation class on in-memory copies and
requires the scan to catch every one, refuses a clean-tree miss, and proves
a stubbed scanner fails every arm.
"""
import argparse
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: The lane's owned surface: the deploy/owner tools it shipped or rewrote,
#: the launchers and configurations it retargeted, and the authorities whose
#: ownership story it rewrote.
DAEMON_SCAN_FILES = (
    "sw/litex/deploy.sh",
    "sw/litex/check_gptp_owner_pair.py",
    "sw/litex/qspi_owner_transition.py",
    "sw/litex/layout_from_soch.py",
    "sw/litex/gptp_owner_contract.py",
    "sw/litex/sweep.sh",
    "sw/litex/sweep_extra.sh",
    "sw/litex/build.sh",
    "sw/builder/endstation_builder.py",
    "configs/endstation_arty_current.yaml",
    "configs/endstation_arty_4x4.yaml",
    "configs/endstation_arty_8ch.yaml",
    "configs/endstation_ax7101_1x1_tdm8.yaml",
    "configs/endstation_ax7101_8x8.yaml",
    "REQUIREMENTS.md",
    "docs/ARCHITECTURE_HW_SW_SPLIT.md",
    "docs/design/TIME_SYNC.md",
    "docs/design/GPTP_PLANE.md",
    "docs/integration/BAREMETAL_FIRMWARE.md",
    "docs/reference/milan_feature_status.json",
)
CONFIG_FILES = tuple(f for f in DAEMON_SCAN_FILES if f.startswith("configs/"))
LAUNCHER_FILES = ("sw/litex/sweep.sh", "sw/litex/sweep_extra.sh",
                  "sw/litex/build.sh")

DAEMON_RE = re.compile(r"ptp4l|phc2sys|linuxptp", re.I)
ANCHOR_RE = re.compile(r"retired|#259|historical|verification-only", re.I)


def _blocks(text):
    """(first line number, block text) for blank-line-delimited paragraphs."""
    line = 1
    for block in re.split(r"\n[ \t]*\n", text):
        yield line, block
        line += block.count("\n") + 2


def scan(tree):
    """Findings over {relpath: text}. Every owned file must be present."""
    findings = []
    for path in DAEMON_SCAN_FILES:
        text = tree.get(path)
        if text is None:
            findings.append(
                f"{path}: MISSING from the inventory - an absent file is a "
                "failure, not a zero count (the owned surface moved without "
                "moving this gate)")
            continue
        for first, block in _blocks(text):
            if DAEMON_RE.search(block) and not ANCHOR_RE.search(block):
                offender = next(l for l in block.split("\n")
                                if DAEMON_RE.search(l))
                findings.append(
                    f"{path}:{first}: retired daemon term without a "
                    f"retirement anchor: {offender.strip()[:90]!r} - the "
                    "product is bare-metal only (#259)")
    for path in CONFIG_FILES:
        text = tree.get(path)
        if text is None:
            continue  # already a MISSING finding above
        for number, line in enumerate(text.split("\n"), 1):
            if "fabric_gptp: false" in line:
                findings.append(
                    f"{path}:{number}: fabric_gptp: false - option-off is "
                    "verification-only (#259), never a product configuration")
    for path in LAUNCHER_FILES:
        text = tree.get(path)
        if text is None:
            continue
        for number, line in enumerate(text.split("\n"), 1):
            if "--no-fabric-gptp" in line:
                findings.append(
                    f"{path}:{number}: --no-fabric-gptp in a launcher - the "
                    "option-off elaboration is a direct milan_soc.py "
                    "verification run (#259), never a recipe")
    return findings


def read_tree():
    tree = {}
    for path in DAEMON_SCAN_FILES:
        full = ROOT / path
        try:
            tree[path] = full.read_text(encoding="utf-8")
        except OSError:
            pass  # scan() turns absence into a named failure
    return tree


def selftest():
    problems = []
    pristine = read_tree()
    if len(pristine) != len(DAEMON_SCAN_FILES):
        missing = sorted(set(DAEMON_SCAN_FILES) - set(pristine))
        print(f"selftest: cannot read the pristine surface: {missing}")
        return 2
    clean = scan(pristine)
    if clean:
        problems.append("pristine tree is not clean: " + "; ".join(clean))

    arms = []

    def arm(name, mutate, fragment):
        arms.append((name, mutate, fragment))

    for path in ("sw/litex/deploy.sh", "docs/design/TIME_SYNC.md",
                 "configs/endstation_arty_current.yaml"):
        arm(f"unanchored daemon claim in {path}",
            lambda t, p=path: t.__setitem__(
                p, t[p] + "\n\nboot: start ptp4l on eth0\n"),
            "retired daemon term without a retirement anchor")
    arm("anchored mention stays allowed (negative control)",
        lambda t: t.__setitem__(
            "sw/litex/deploy.sh",
            t["sw/litex/deploy.sh"]
            + "\n\n# ptp4l is retired (#259); nothing starts it.\n"),
        None)
    arm("a config reacquires fabric_gptp: false",
        lambda t: t.__setitem__(
            "configs/endstation_arty_4x4.yaml",
            t["configs/endstation_arty_4x4.yaml"].replace(
                "fabric_gptp: true", "fabric_gptp: false", 1)),
        "verification-only (#259), never a product configuration")
    arm("a launcher reacquires --no-fabric-gptp",
        lambda t: t.__setitem__(
            "sw/litex/sweep.sh",
            t["sw/litex/sweep.sh"].replace(
                "--fabric-gptp", "--no-fabric-gptp", 1)),
        "never a recipe")
    arm("an owned file vanishes",
        lambda t: t.__delitem__("sw/litex/check_gptp_owner_pair.py"),
        "MISSING from the inventory")

    caught = 0
    for name, mutate, fragment in arms:
        world = dict(pristine)
        mutate(world)
        found = scan(world)
        if fragment is None:
            if found:
                problems.append(f"[{name}] expected no finding, got {found}")
            else:
                caught += 1
                print(f"  ok   allowed: {name}")
            continue
        if any(fragment in f for f in found):
            caught += 1
            print(f"  ok   caught: {name}")
        else:
            problems.append(f"[{name}] expected a finding naming "
                            f"{fragment!r}, got {found or 'no findings'}")

    # Vacuity: a scanner stubbed to find nothing must fail every biting arm.
    biting = [a for a in arms if a[2] is not None]
    stub_misses = 0
    for name, mutate, fragment in biting:
        if not any(fragment in f for f in []):
            stub_misses += 1
    if stub_misses != len(biting):
        problems.append("vacuity: the stub scanner did not fail every arm")
    else:
        print(f"  ok   vacuity: a stub that finds nothing fails all "
              f"{len(biting)} biting arms")

    if problems:
        for problem in problems:
            print("  -", problem)
        print(f"baremetal-scope selftest: FAIL ({len(problems)} problem(s))")
        return 1
    print(f"baremetal-scope selftest: PASS ({len(arms)} arm(s), "
          f"{len(DAEMON_SCAN_FILES)} file(s) inventoried)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    tree = read_tree()
    findings = scan(tree)
    for finding in findings:
        print("  -", finding)
    if findings:
        print(f"baremetal-scope: FAIL ({len(findings)} finding(s))")
        return 1
    print(f"baremetal-scope: OK (0 findings across "
          f"{len(DAEMON_SCAN_FILES)} owned file(s); the repository-wide "
          "sweep remains issue #259)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
