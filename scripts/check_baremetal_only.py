#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The tracked tree is bare-metal only: zero retired-stack references (#259).

WHY THIS EXISTS. #259 (USER directive 2026-08-25) removes the retired host
software stack from the product AND from the tracked checkout: no kernel,
rootfs, Buildroot, OpenSBI, device-tree boot, ALSA host plane, linuxptp
daemon, or host-service path may appear in first-party sources, docs,
generated artifacts or test fixtures. Git history keeps the story; the
checkout does not. This gate REPLACES the transitional
check_baremetal_scope.py, whose anchored retired-history allowance #259
retires: an anchor excused prose, and #259 wants the terms gone.

INVENTORY BY DISCOVERY. The scan set is ``git ls-files`` minus submodule
gitlinks, ``third_party/``, binary file extensions, and this gate itself
(its term table and self-test fixtures must be free to name what they
refuse). Nothing else is excluded: docs, configs, RTL, testbenches, test
suites, generated .svg/.drawio text and archive pages are all scanned, so a
generator or fixture cannot reintroduce a term this gate cannot see. A
failed or EMPTY inventory is rc 2, never a zero count, and an unreadable
inventory file is a finding, never a skip.

POLICY CLASSES (each finding names its class):

T. retired-stack TERM, anywhere, any context: the appearance itself is the
   finding. Comments, prose, strings, fixture data and generated text all
   count; there is no anchor allowance. The one suppression is the
   cross-toolchain TRIPLET allowlist below (issue #259 non-goal: host-side
   development tooling is not the product target, and the RV32 cross
   compiler's triplet names its libc and the pinned sv2v release asset's
   file name names the host OS its binary runs on, not a product path).
O. retired launcher option token: ``--sound-card``, ``--flashboot full``,
   ``--flashboot kernel``; and ``--no-fabric-gptp`` anywhere but its one
   code home, ``sw/litex/milan_soc.py`` (the verification-only door), and
   the launch-recipe gate that proves recipes never carry it.
Y. ``fabric_gptp: false`` in any tracked YAML, found by PARSING the file
   (yaml.safe_load, full mapping walk), so spacing and scalar case cannot
   hide it and a substring can never be the check.

``--selftest`` builds pristine scratch git trees and proves: every term in
the table is caught on its own; a term planted in a generated .svg is
caught (generated outputs are scanned); each option token and the parsed
YAML arm bite, spacing and case included; the host-tooling allowlist
suppresses ONLY its exact spellings and cannot launder a second term on the
same line; a missing/unreadable inventory fails rather than
counting zero; and the clean control stays clean.
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:  # the YAML class is load-bearing; refuse to run blind
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
SELF = "scripts/check_baremetal_only.py"

#: The verification-only door's one code home, plus the gate that proves
#: launch recipes never carry it.
OPTION_HOMES = ("sw/litex/milan_soc.py", "sw/builder/test_builder.py")

#: Binary payloads: nothing greppable lives here. Generated TEXT formats
#: (.svg, .drawio) are deliberately NOT in this set.
SKIP_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf",
    ".bit", ".bin", ".fbi", ".hex", ".xz", ".gz", ".zip",
    ".tar", ".7z", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".vcd",
    ".fst", ".wav", ".mp3", ".mp4", ".dcp",
}

#: Class T: the retired stack, one token per row. Word-bounded and
#: case-insensitive; the appearance is the finding.
TERMS = (
    "linux", "linuxptp", "ptp4l", "phc2sys", "rootfs", "initramfs",
    "buildroot", "opensbi", "alsa", "pipewire", "aplay", "systemd",
    "udev", "devicetree", "dtb", "dtc",
)
TERM_RE = re.compile(r"\b(" + "|".join(TERMS) + r")\b", re.IGNORECASE)
#: multi-word spellings the word-bound row above cannot carry
PHRASE_RE = re.compile(r"device.?tree", re.IGNORECASE)

#: Issue #259 non-goal: the host-side tooling a developer builds WITH is not
#: a product path. Two families qualify, and ONLY these exact spellings are
#: suppressed, nothing wider:
#:   * the cross toolchain, whose triplet names the toolchain's libc;
#:   * the pinned sv2v release asset, whose file name carries the host OS the
#:     binary runs on (the CI jobs and the install recipes must be able to
#:     name the artifact they download).
#: Suppression is a MASK, not a line skip: a second, unmasked occurrence on
#: the same line still fires, which the selftest proves for both families.
ALLOWED_HOST_TOOLING = ("riscv32-linux-gcc", "riscv64-linux-gnu-gcc",
                        "sv2v-Linux.zip", "sv2v-Linux")
TRIPLET_RE = re.compile("|".join(re.escape(t) for t in ALLOWED_HOST_TOOLING))

#: Class O: retired option tokens.
OPT_RE = re.compile(r"--sound-card\b|--flashboot[ =](?:full|kernel)\b")
DOOR_RE = re.compile(r"--no-fabric-gptp\b")


def inventory(root):
    """Tracked first-party text files, discovered, never listed by hand."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-s"],
            capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, OSError) as exc:
        raise InventoryError(f"git ls-files failed: {exc}")
    files = []
    for line in out.stdout.splitlines():
        mode, _sha, _stage_path = line.split(None, 2)
        path = line.split("\t", 1)[1]
        if mode == "160000":
            continue  # submodule gitlink
        if path.startswith("third_party/") or path == SELF:
            continue
        if pathlib.Path(path).suffix.lower() in SKIP_EXTS:
            continue
        files.append(path)
    if not files:
        raise InventoryError("the inventory is empty: a tree with no "
                             "first-party files is a broken scan, not a "
                             "clean one")
    return files


class InventoryError(RuntimeError):
    pass


def scan_file(root, path):
    findings = []
    try:
        text = (root / path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"{path}: [inventory] unreadable ({exc}) - an unreadable "
                f"file is a finding, never a skip"]
    for n, line in enumerate(text.splitlines(), 1):
        probe = TRIPLET_RE.sub("", line)
        m = TERM_RE.search(probe) or PHRASE_RE.search(probe)
        if m:
            findings.append(
                f"{path}:{n}: [T] retired-stack term {m.group(0)!r}: "
                f"{line.strip()[:100]!r} (#259: the checkout is bare-metal "
                f"only; history lives in git)")
            continue
        m = OPT_RE.search(line)
        if m:
            findings.append(
                f"{path}:{n}: [O] retired option token {m.group(0)!r}: "
                f"{line.strip()[:100]!r}")
            continue
        if DOOR_RE.search(line) and path not in OPTION_HOMES:
            findings.append(
                f"{path}:{n}: [O] --no-fabric-gptp outside its code home "
                f"({', '.join(OPTION_HOMES)}): the verification-only door "
                f"is never a recipe")
    if path.endswith((".yaml", ".yml")) and yaml is not None:
        findings += scan_yaml(root, path, text)
    return findings


def scan_yaml(root, path, text):
    def walk(node, crumb):
        hits = []
        if isinstance(node, dict):
            for k, v in node.items():
                if str(k) == "fabric_gptp" and v is False:
                    hits.append(f"{path}: [Y] {crumb}fabric_gptp is false "
                                f"(parsed): the fabric plane is the one "
                                f"product owner (#259)")
                hits += walk(v, f"{crumb}{k}.")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                hits += walk(v, f"{crumb}[{i}].")
        return hits
    try:
        docs = list(yaml.safe_load_all(text))
    except yaml.YAMLError:
        return []  # malformed YAML is another gate's business
    hits = []
    for doc in docs:
        hits += walk(doc, "")
    return hits


def check(root=ROOT):
    files = inventory(root)
    findings = []
    for path in files:
        findings += scan_file(pathlib.Path(root), path)
    return findings, len(files)


def selftest():
    problems, arms = [], 0

    def scratch_tree(build):
        d = tempfile.TemporaryDirectory(prefix="bmonly.")
        root = pathlib.Path(d.name)
        subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
        (root / "clean.md").write_text("The bare-metal firmware owns boot "
                                       "policy and identity.\n")
        build(root)
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        return d, root

    def arm(name, build, expect_hit, needle=None):
        nonlocal arms
        arms += 1
        d, root = scratch_tree(build)
        try:
            findings, _ = check(root)
        except InventoryError as exc:
            findings = [f"[inventory] {exc}"]
        finally:
            hit = bool(findings)
            text = "\n".join(findings)
            d.cleanup()
        if expect_hit and not hit:
            problems.append(f"[{name}] planted defect not caught")
        elif expect_hit and needle and needle not in text:
            problems.append(f"[{name}] caught, but not by the right class: "
                            f"wanted {needle!r} in\n{text}")
        elif not expect_hit and hit:
            problems.append(f"[{name}] clean fixture flagged:\n{text}")

    # the clean control
    arm("clean-control", lambda r: None, False)

    # T: every term in the table bites on its own, in a plain doc line
    for term in sorted(set(TERMS)):
        arm(f"term-{term}",
            lambda r, t=term: (r / "page.md").write_text(
                f"the product boots {t} at power-on\n"), True, "[T]")
    arm("term-phrase-device-tree",
        lambda r: (r / "page.md").write_text(
            "boot is described by a device tree blob\n"), True, "[T]")

    # generated outputs are scanned: a term planted in an .svg text node
    arm("term-in-generated-svg",
        lambda r: (r / "diagram.svg").write_text(
            "<svg><text>rootfs hand-off</text></svg>\n"), True, "[T]")

    # the host-tooling allowlist suppresses ONLY the exact spellings
    arm("triplet-allowed",
        lambda r: (r / "notes.md").write_text(
            "the census drives riscv32-linux-gcc when present\n"), False)
    arm("triplet-does-not-launder",
        lambda r: (r / "notes.md").write_text(
            "riscv32-linux-gcc builds the linux image\n"), True, "[T]")
    arm("sv2v-asset-allowed",
        lambda r: (r / "install.sh").write_text(
            "curl -fsSL .../sv2v-Linux.zip -o /tmp/sv2v.zip\n"), False)
    arm("sv2v-asset-does-not-launder",
        lambda r: (r / "install.sh").write_text(
            "unzip sv2v-Linux.zip then boot the linux image\n"), True, "[T]")

    # O: option tokens, both spellings of the flashboot value
    arm("opt-sound-card",
        lambda r: (r / "run.sh").write_text("./soc --sound-card\n"),
        True, "[O]")
    arm("opt-flashboot-full",
        lambda r: (r / "run.sh").write_text("./soc --flashboot full\n"),
        True, "[O]")
    arm("opt-flashboot-eq-kernel",
        lambda r: (r / "run.sh").write_text("./soc --flashboot=kernel\n"),
        True, "[O]")
    arm("opt-door-outside-home",
        lambda r: (r / "recipe.sh").write_text("./soc --no-fabric-gptp\n"),
        True, "[O]")

    # Y: parsed YAML, spacing and case cannot hide it
    arm("yaml-fabric-gptp-false",
        lambda r: (r / "c.yaml").write_text(
            "board:\n  features:\n    fabric_gptp :   False\n"), True, "[Y]")

    # inventory failure modes
    arms += 1
    with tempfile.TemporaryDirectory(prefix="bmonly.") as d:
        try:
            check(pathlib.Path(d))
            problems.append("[missing-inventory] a non-git directory "
                            "scanned as zero findings")
        except InventoryError:
            pass
    arms += 1
    d, root = scratch_tree(lambda r: (r / "page.md").write_text("clean\n"))
    try:
        (root / "page.md").chmod(0)
        findings, _ = check(root)
        if not any("[inventory] unreadable" in f for f in findings):
            problems.append("[unreadable-file] an unreadable file scanned "
                            "as clean")
    finally:
        (root / "page.md").chmod(0o644)
        d.cleanup()

    return problems, arms


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if yaml is None:
        print("baremetal-only: FATAL: pyyaml is unavailable and the parsed "
              "YAML class is load-bearing", file=sys.stderr)
        return 2
    if args.selftest:
        problems, arms = selftest()
        for p in problems:
            print("  -", p, file=sys.stderr)
        if problems:
            return 2
        print(f"baremetal-only selftest: PASS ({arms} arm(s))")
        return 0
    try:
        findings, n = check()
    except InventoryError as exc:
        print(f"baremetal-only: FATAL: {exc}", file=sys.stderr)
        return 2
    for f in findings[:40]:
        print("  -", f)
    if len(findings) > 40:
        print(f"  ... and {len(findings) - 40} more")
    if findings:
        print(f"baremetal-only: FAIL ({len(findings)} finding(s) across "
              f"{n} scanned file(s))")
        return 1
    print(f"baremetal-only: OK (0 findings across {n} tracked first-party "
          f"file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
