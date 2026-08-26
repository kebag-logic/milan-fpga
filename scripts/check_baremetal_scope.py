#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Hold the tracked first-party surface to the bare-metal-only product policy.

WHY THIS EXISTS. #259 (2026-08-25) makes the product bare-metal only: fabric
gPTP is the one PHC/publication owner, and the Linux boot chain (kernel,
OpenSBI, DTB, Buildroot rootfs), the ALSA-over-Linux surface and the
ptp4l/phc2sys/linuxptp software owner are retired. The option-off elaboration
(GPTP_PLANE_EN_P=0) survives ONLY as verification-only hardware reached
through ``milan_soc.py --no-fabric-gptp``, never through a configuration and
never flashable.

INVENTORY BY DISCOVERY. The scan set is ``git ls-files`` minus submodule
gitlinks, ``third_party/``, the retired-history archive
(``historical_now_obsolete/`` and pages whose first line is the
``[OBSOLETE + date]`` header check_archive.py owns), the verification trees
(``tb/``, ``tests/``, ``test_*.py``: fixtures there must be free to name the
things they prove are refused), binary/image file extensions, and this gate
itself. A failed or empty inventory is a hard failure (rc 2), never a zero
count: an inventory that silently shrinks is how the 20-file hand list this
gate replaced went blind.

POLICY CLASSES (each finding names its class):

A. retired daemon COMMAND: ptp4l/phc2sys invoked on an executable line (a
   shell/recipe code line, a fenced doc line, ExecStart/systemd/init/package
   lines, BR2_PACKAGE_LINUXPTP). An executable line is a finding REGARDLESS
   of retirement words nearby: "# retired\\nexec ptp4l" still starts ptp4l.
B. retired launcher option or default: ``--software-profile linux``,
   ``--flashboot full``, ``--sound-card``, ``--no-fabric-gptp``, or a shell
   ``MILAN_PROFILE`` default of ``linux``. On a code/recipe/fenced
   line this is always a finding. In prose or a comment it is accepted only
   under a retirement anchor. The single code home for these tokens is
   ``sw/litex/milan_soc.py``, the launcher authority that defines and
   refuses them.
C. ``fabric_gptp: false`` in any tracked YAML, found by PARSING the file
   (yaml.safe_load, full mapping walk), so spacing and scalar case cannot
   hide it and a substring can never be the check.
D. Linux-boot-chain product claim: prose that pairs a boot-chain term
   (rootfs, OpenSBI, DTB, Buildroot, ALSA, Linux, the daemon names) with a
   product-status claim (product, shipping, buildable, flashable, on-target)
   in a small window with no retirement anchor in reach.

RETIREMENT ANCHOR: ``retired``, ``#259``, ``historical`` or
``verification-only`` (or an explicit denial such as ``unsupported`` or
``refused``) in the SAME SENTENCE as the policy term, or in the governing
Markdown heading. A nearby sentence about some other retired path is not
authority for the claim being graded. Anchors excuse prose only; they never
excuse an executable line. An explicit ``external peer only`` / ``external
bench only`` scope also keeps host-side test dependencies out of the target
product rule.

``--selftest`` plants the review's escape mutations, including an unrelated
adjacent retirement sentence and an option-off ``ptp4l`` ownership claim,
spaced/case-varied YAML, an omitted-authority path, a clean retired-history
paragraph and a missing-inventory arm, and requires every biting arm to add
findings to a clean pristine scan.
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
SELF = "scripts/check_baremetal_scope.py"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_archive import OBSOLETE_HEADER_RE  # the one owner of "obsolete"

#: the launcher authority: defines the retired tokens in order to refuse them.
LAUNCH_AUTHORITY = "sw/litex/milan_soc.py"

SKIP_PREFIXES = ("third_party/", "historical_now_obsolete/", "tb/", "tests/")
SKIP_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf", ".svg",
    ".drawio", ".bit", ".bin", ".fbi", ".hex", ".xz", ".gz", ".zip",
    ".tar", ".7z", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".vcd",
    ".fst", ".wav", ".mp3", ".mp4", ".log", ".patch", ".dcp",
}
TEST_FILE_RE = re.compile(r"(?:^|/)test_[^/]*\.py$|_test\.py$")

ANCHOR_RE = re.compile(r"retired|#259|historical|verification[- ]only", re.I)
NON_TARGET_RE = re.compile(
    r"\b(?:external (?:peer|bench)(?: host| equipment)? only|"
    r"peer[- ]side only|host[- ]side only|not (?:part of )?target runtime)\b",
    re.I)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^#{1,6}\s")

# -- class A: daemon command shapes ----------------------------------------
_WRAP = (r"(?:(?:exec|sudo|nohup|setsid|env|chrt|taskset|timeout|watch|"
         r"start|restart|run|launch|spawn|daemonize)\s+(?:-{1,2}\S+\s+|\d+\s+)*)*")
_ASSIGN = r"(?:[A-Za-z_]\w*=(?:\"[^\"]*\"|'[^']*'|\S*)\s+)*"
DAEMON_HEAD_RE = re.compile(
    rf"^{_ASSIGN}{_WRAP}(ptp4l|phc2sys)(?:\s|$)")
SYSTEMD_RE = re.compile(
    r"(?:ExecStart\w*\s*=|start-stop-daemon\b)[^\n]*\b(?:ptp4l|phc2sys|linuxptp)\b"
    r"|\b(?:systemctl|service)\s+(?:start|enable|restart)\b[^\n]*"
    r"\b(?:ptp4l|phc2sys|linuxptp)\b"
    r"|BR2_PACKAGE_LINUXPTP"
    r"|\b(?:apt-get|apt|opkg|pacman|dnf|yum)\b[^\n]*install[^\n]*linuxptp")
_SEG_SPLIT_RE = re.compile(r"[;&|:`]|\$\(")
#: a daemon name that is a log prefix ("ptp4l: rms ...", "ptp4l[123]: ...")
#: or a quoted mapping key ('"ptp4l":') names output or data, not a command.
_LOG_PREFIX_RE = re.compile(r"\b(ptp4l|phc2sys)(\[[^\]]*\])?[\"']?:")

# -- class B: retired launcher options -------------------------------------
OPTION_RES = (
    (re.compile(r"--software-profile[ =]+linux\b"), "--software-profile linux"),
    (re.compile(r"--flashboot[ =]+full\b"), "--flashboot full"),
    (re.compile(r"--sound-card\b"), "--sound-card"),
    (re.compile(r"--no-fabric-gptp\b"), "--no-fabric-gptp"),
    (re.compile(r"MILAN_PROFILE:-linux\b"), "MILAN_PROFILE default linux"),
)

# -- class D: boot-chain product claims ------------------------------------
BOOT_RE = re.compile(
    r"\b(rootfs|opensbi|buildroot|dtb|device[- ]tree|alsa|kernel|linux|"
    r"linuxptp|ptp4l|phc2sys)\b", re.I)
CLAIM_RE = re.compile(
    r"\b(product|production|shipping|ship(?:s|ped)?|buildable|flashable|"
    r"on[- ]target|supported|active|mandatory|available|remains)\b",
    re.I)
OWNER_CLAIM_RE = re.compile(
    r"(?:\b(?:ptp4l|phc2sys|linuxptp)\b.{0,110}\b(?:owner|comparison|"
    r"option[- ]off)\b|\b(?:owner|comparison|option[- ]off)\b.{0,110}"
    r"\b(?:ptp4l|phc2sys|linuxptp)\b)", re.I)
_POLICY_OBJECT = (r"(?:linux(?:ptp)?|ptp4l|phc2sys|rootfs|opensbi|buildroot|"
                  r"dtb|device[- ]tree|alsa|kernel|owner|image|path|"
                  r"--(?:software-profile|flashboot|sound-card|"
                  r"no-fabric-gptp))")
DENIAL_RE = re.compile(
    rf"(?:\b(?:no|without)(?:\s+[\w/-]+){{0,4}}\s+{_POLICY_OBJECT}\b|"
    rf"\b{_POLICY_OBJECT}\b(?:\s+[\w/-]+){{0,4}}\s+"
    rf"(?:(?:is|are|was|were|remain(?:s|ed)?|stay(?:s|ed)?)\s+)?"
    rf"(?:(?:not|never|no\s+longer)\s+(?:a\s+|an\s+|the\s+)?"
    rf"(?:supported|shipping|shipped|a?live|active|available|buildable|"
    rf"flashable|loaded|started|run|used|included|retained|product|owner)|"
    rf"unsupported|absent|forbidden|gone|refused|removed|omitted)\b|"
    rf"\b(?:refus(?:e|ed|es|ing)|"
    rf"remov(?:e|ed|es|ing)|omit(?:s|ted|ting)|forbid(?:s|den|ding)?)\b"
    rf".{{0,80}}\b{_POLICY_OBJECT}\b)", re.I)

_COMMENT_PREFIXES = ("#", "//", "/*", "*", "<!--", ";", "!")


class InventoryError(RuntimeError):
    """The tracked-file inventory could not be established."""


def inventory(root=ROOT):
    """Tracked first-party scan set. Failure raises, never returns empty."""
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-s"],
                             capture_output=True, text=True)
    except (OSError, subprocess.SubprocessError) as exc:
        raise InventoryError(f"git ls-files failed: {exc}")
    if out.returncode != 0:
        raise InventoryError(
            f"git ls-files rc={out.returncode}: not a git working tree?")
    files = []
    for line in out.stdout.splitlines():
        head, _, path = line.partition("\t")
        if not path:
            continue
        if head.split()[0] == "160000":  # submodule gitlink
            continue
        files.append(path)
    if not files:
        raise InventoryError("git ls-files returned an empty inventory")
    return [p for p in files if in_scope(p)]


def in_scope(rel):
    if rel == SELF or rel.startswith(SKIP_PREFIXES):
        return False
    if pathlib.Path(rel).suffix.lower() in SKIP_EXTS:
        return False
    if TEST_FILE_RE.search(rel):
        return False
    return True


def read_tree(paths):
    tree = {}
    for rel in paths:
        full = ROOT / rel
        try:
            data = full.read_bytes()
        except OSError as exc:
            raise InventoryError(
                f"tracked policy file cannot be read: {rel}: {exc.strerror}")
        if b"\x00" in data[:4096]:
            continue  # binary content without a binary extension
        text = data.decode("utf-8", errors="replace")
        if rel.endswith(".md"):
            first = text.split("\n", 1)[0]
            if OBSOLETE_HEADER_RE.fullmatch(first):
                continue  # in-place-obsolete record (check_archive rule)
        tree[rel] = text
    return tree


def _is_comment(line):
    return line.lstrip().startswith(_COMMENT_PREFIXES)


def _daemon_command(line):
    """True when ptp4l/phc2sys sits in command position on this line."""
    if SYSTEMD_RE.search(line):
        return True
    stripped = _LOG_PREFIX_RE.sub("LOGPFX:", line.strip())
    if stripped[:2] in ("$ ", "> ", "% "):
        stripped = stripped[2:]
    for seg in _SEG_SPLIT_RE.split(stripped):
        seg = seg.strip().lstrip("\"'([{ \t")
        if seg and DAEMON_HEAD_RE.match(seg):
            return True
    return False


def _class_d_scope(rel):
    if rel.startswith("hdl/"):
        return False  # RTL comment surface, no recipes; edits are out of scope
    return rel.endswith((".md", ".py", ".sh", ".yaml", ".yml", ".json"))


def _paragraph(lines, index, is_md):
    """Return prose containing *index* and that line's offset within it.

    Markdown wraps one sentence across physical lines, so grading only the
    current line would reject an honest ``... is\nretired (#259).`` spelling.
    Code and comments keep line scope: joining adjacent source lines would let
    one comment authorize another.
    """
    if not is_md or lines[index].lstrip().startswith("|"):
        return lines[index], 0
    start = index
    while start > 0:
        prior = lines[start - 1]
        if (not prior.strip() or HEADING_RE.match(prior)
                or FENCE_RE.match(prior)):
            break
        start -= 1
    end = index + 1
    while end < len(lines):
        following = lines[end]
        if (not following.strip() or HEADING_RE.match(following)
                or FENCE_RE.match(following)):
            break
        end += 1
    parts = [line.strip() for line in lines[start:end]]
    offset = sum(len(part) + 1 for part in parts[:index - start])
    return " ".join(parts), offset


def _sentence_at(text, position):
    """Return sentence containing *position* and its sentence-local offset."""
    boundaries = [0]
    boundaries.extend(match.end()
                      for match in re.finditer(r"[.!?](?:\s+|$)", text))
    if boundaries[-1] != len(text):
        boundaries.append(len(text))
    for left, right in zip(boundaries, boundaries[1:]):
        if left <= position < right or (position == len(text) == right):
            return text[left:right], position - left
    return text, position


def _clause_at(text, position):
    """Return the table/punctuation clause containing *position*."""
    left = 0
    for match in re.finditer(r"[|,;.!?]", text[:position]):
        left = match.end()
    match = re.search(r"[|,;.!?]", text[position:])
    right = position + match.start() if match else len(text)
    return text[left:right], position - left


def _policy_sentence(lines, index, column, is_md):
    paragraph, offset = _paragraph(lines, index, is_md)
    return _sentence_at(paragraph, offset + column)


def _walk_yaml(node, hits, string_scalars=False):
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).strip().lower() == "fabric_gptp":
                off = (value is False or
                       (string_scalars and isinstance(value, str)
                        and value.strip().lower() in ("false", "no", "off")))
                if off:
                    hits.append(str(key))
            _walk_yaml(value, hits, string_scalars)
    elif isinstance(node, (list, tuple)):
        for item in node:
            _walk_yaml(item, hits, string_scalars)


def scan(tree):
    """Findings over {relpath: text}."""
    findings = []

    def emit(rel, lineno, cls, msg):
        findings.append(f"{rel}:{lineno}: [{cls}] {msg} (#259: bare-metal only)")

    for rel, text in sorted(tree.items()):
        lines = text.split("\n")
        is_md = rel.endswith(".md")
        in_fence = False
        heading = ""

        for i, line in enumerate(lines):
            if is_md and FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if is_md and not in_fence and HEADING_RE.match(line):
                heading = line
            # a comment line is prose even inside a fence or a script: the
            # executable-regardless rule bites the command line itself.
            code_ctx = ((in_fence if is_md else True)
                        and not _is_comment(line))
            heading_anchored = bool(ANCHOR_RE.search(heading))

            # -- class A: a daemon command is active regardless of anchors --
            if code_ctx and _daemon_command(line):
                emit(rel, i + 1, "A", "retired daemon command: "
                     f"{line.strip()[:90]!r}")

            # -- class B: retired launcher options --------------------------
            if rel != LAUNCH_AUTHORITY:
                for rx, name in OPTION_RES:
                    match = rx.search(line)
                    if not match:
                        continue
                    if code_ctx:
                        emit(rel, i + 1, "B", f"retired option {name} on an "
                             f"executable line: {line.strip()[:90]!r}")
                    else:
                        sentence, column = _policy_sentence(
                            lines, i, match.start(), is_md)
                        clause, _ = _clause_at(sentence, column)
                        anchored = (heading_anchored
                                    or bool(ANCHOR_RE.search(clause))
                                    or bool(DENIAL_RE.search(clause)))
                        if anchored:
                            continue
                        emit(rel, i + 1, "B", f"retired option {name} in "
                             "prose without a retirement anchor")

            # -- class D: boot-chain product claims -------------------------
            # the claim must sit NEAR the boot-chain term (one sentence-ish
            # span), or a wide TOC/table line pairs unrelated cells.
            if _class_d_scope(rel):
                for match in BOOT_RE.finditer(line):
                    sentence, column = _policy_sentence(
                        lines, i, match.start(), is_md)
                    clause, column = _clause_at(sentence, column)
                    span = clause[max(0, column - 110):
                                  column + len(match.group(0)) + 110]
                    anchored = (heading_anchored
                                or bool(ANCHOR_RE.search(clause))
                                or bool(DENIAL_RE.search(clause))
                                or bool(NON_TARGET_RE.search(clause)))
                    claim = (bool(CLAIM_RE.search(span))
                             or bool(OWNER_CLAIM_RE.search(clause)))
                    if claim and not anchored:
                        emit(rel, i + 1, "D", "Linux-boot-chain product "
                             "claim without a retirement anchor: "
                             f"{line.strip()[:90]!r}")
                        break

        # -- class C: parsed YAML ------------------------------------------
        if rel.endswith((".yaml", ".yml")):
            if yaml is None:
                emit(rel, 0, "C", "pyyaml is unavailable; the semantic "
                     "fabric_gptp check cannot run")
                continue
            hits = []
            try:
                for document in yaml.safe_load_all(text):
                    _walk_yaml(document, hits)
            except yaml.YAMLError:
                # custom application tags: fall back to the structure-only
                # loader (scalars stay strings; compare them semantically).
                try:
                    for document in yaml.load_all(text, Loader=yaml.BaseLoader):
                        _walk_yaml(document, hits, string_scalars=True)
                except yaml.YAMLError as exc:
                    emit(rel, 0, "C", "unparseable YAML "
                         f"({exc.__class__.__name__}); the fabric_gptp "
                         "check cannot certify it")
                    continue
            for key in hits:
                emit(rel, 0, "C", f"parsed key {key} is false: option-off is "
                     "verification-only, never a configuration")
    return findings


# ---------------------------------------------------------------- selftest --

RETIRED_OK = ("\n\nfiller line.\n\nThe Linux boot chain (kernel, OpenSBI, "
              "DTB, Buildroot rootfs) is retired (#259); ptp4l and phc2sys "
              "never run on the product.\n")


def selftest():
    problems = []
    try:
        pristine = read_tree(inventory())
    except InventoryError as exc:
        print(f"selftest: cannot inventory the tree: {exc}")
        return 2
    # Tree conformance is --check's verdict (the docs job runs both); the
    # selftest proves the scanner's teeth, so every arm below is graded on
    # the DELTA against this baseline and pre-existing findings only warn.
    clean = scan(pristine)
    if clean:
        print(f"  note pristine tree carries {len(clean)} finding(s); "
              "--check reports them, arms are graded on deltas")

    arms = []

    def arm(name, mutate, fragment):
        arms.append((name, mutate, fragment))

    # the review's mutation (a): a product claim paragraph in a doc
    arm("review mutation a: Linux product-claim paragraph",
        lambda t: t.__setitem__(
            "docs/design/TIME_SYNC.md",
            t["docs/design/TIME_SYNC.md"] + "\n\nfiller line.\n\nproduct "
            "boots Linux with rootfs, OpenSBI and DTB; use "
            "--software-profile linux --flashboot full\n"),
        "product claim")
    # the review's mutation (b): anchored comment, executable daemon line
    arm("review mutation b: anchored exec ptp4l stays a finding",
        lambda t: t.__setitem__(
            "sw/litex/deploy.sh",
            t["sw/litex/deploy.sh"] + "\n# retired by #259\n"
            "exec ptp4l --software-profile linux --flashboot full\n"),
        "retired daemon command")
    arm("unrelated retirement sentence cannot anchor a Linux shipping claim",
        lambda t: t.__setitem__(
            "docs/design/TIME_SYNC.md",
            t["docs/design/TIME_SYNC.md"]
            + "\n\nThe RGMII path is retired. The Linux driver now ships "
            "in a private test repository.\n"),
        "product claim")
    arm("unrelated denial cannot anchor a Linux shipping claim",
        lambda t: t.__setitem__(
            "docs/design/TIME_SYNC.md",
            t["docs/design/TIME_SYNC.md"]
            + "\n\nThere is no timing concern, but the Linux driver ships "
            "as a supported product.\n"),
        "product claim")
    arm("unrelated same-clause negation cannot anchor a Linux product claim",
        lambda t: t.__setitem__(
            "sw/litex/patches/apply.sh",
            t["sw/litex/patches/apply.sh"]
            + "\n# A patch the shipping Linux recipe needs is not optional.\n"),
        "product claim")
    arm("production and mandatory are active Linux product claims",
        lambda t: t.__setitem__(
            "docs/design/selftest_production.md",
            "Linux is mandatory in the production configuration.\n"),
        "product claim")
    arm("explicit external-peer scope is not target product authority",
        lambda t: t.__setitem__(
            "docs/design/selftest_external_peer.md",
            "External peer only, not target runtime: Linux is supported "
            "for the peer test host.\n"),
        None)
    arm("unrelated table cell cannot anchor a Linux shipping claim",
        lambda t: t.__setitem__(
            "docs/design/selftest_table.md",
            "| Linux ships as a supported product | NaxRiscv is historical |\n"),
        "product claim")
    arm("option-off ptp4l comparison is an active ownership claim",
        lambda t: t.__setitem__(
            "docs/design/selftest_owner.md",
            "| selftest | `ptp4l` only in the option-off comparison |\n"),
        "product claim")
    arm("spaced YAML scalar is parsed, not substring-matched",
        lambda t: t.__setitem__(
            "configs/selftest_spacing.yaml",
            "board:\n  features:\n    fabric_gptp :   False\n"),
        "parsed key")
    arm("case-varied YAML scalar is parsed",
        lambda t: t.__setitem__(
            "configs/selftest_case.yaml",
            "board:\n  features:\n    FABRIC_GPTP: FALSE\n"),
        "parsed key")
    arm("omitted authority: violation outside the old 20-file inventory",
        lambda t: t.__setitem__(
            "scripts/new_recovery_tool.sh",
            "#!/bin/sh\nptp4l -i eth0 -m\n"),
        "retired daemon command")
    arm("legitimate retired-history paragraph stays accepted",
        lambda t: t.__setitem__(
            "docs/design/TIME_SYNC.md",
            t["docs/design/TIME_SYNC.md"] + RETIRED_OK),
        None)
    arm("anchored comment mention stays accepted",
        lambda t: t.__setitem__(
            "sw/litex/deploy.sh",
            t["sw/litex/deploy.sh"]
            + "\n# ptp4l is retired (#259); nothing starts it.\n"),
        None)
    arm("a launcher reacquires --no-fabric-gptp",
        lambda t: t.__setitem__(
            "sw/litex/sweep.sh",
            t["sw/litex/sweep.sh"].replace(
                "--fabric-gptp", "--no-fabric-gptp", 1)),
        "retired option --no-fabric-gptp"),
    arm("a launcher reacquires a Linux default profile",
        lambda t: t.__setitem__(
            "scripts/hostplane_smoke.sh",
            t["scripts/hostplane_smoke.sh"].replace(
                "MILAN_PROFILE:-baremetal", "MILAN_PROFILE:-linux", 1)),
        "retired option MILAN_PROFILE default linux"),
    arm("a config reacquires fabric_gptp: false",
        lambda t: t.__setitem__(
            "configs/endstation_arty_4x4.yaml",
            t["configs/endstation_arty_4x4.yaml"].replace(
                "fabric_gptp: true", "fabric_gptp: false", 1)),
        "parsed key")
    arm("a fenced doc line runs the retired daemon",
        lambda t: t.__setitem__(
            "docs/design/TIME_SYNC.md",
            t["docs/design/TIME_SYNC.md"]
            + "\n```sh\nptp4l -i eth0 -m\n```\n"),
        "retired daemon command")

    passed = 0
    for name, mutate, fragment in arms:
        world = dict(pristine)
        mutate(world)
        found = scan(world)
        added = [f for f in found if f not in clean]
        if fragment is None:
            if added:
                problems.append(f"[{name}] expected no new finding, got {added}")
            else:
                passed += 1
                print(f"  ok   allowed: {name}")
            continue
        if any(fragment in f for f in added):
            passed += 1
            print(f"  ok   caught: {name}")
        else:
            problems.append(f"[{name}] expected a new finding naming "
                            f"{fragment!r}, got {added or 'no findings'}")

    # a tree that is not a git working tree must be a hard failure
    with tempfile.TemporaryDirectory() as tmp:
        try:
            inventory(pathlib.Path(tmp))
            problems.append("missing-inventory arm: a non-git tree did not "
                            "raise InventoryError")
        except InventoryError:
            passed += 1
            print("  ok   caught: a non-git tree is a hard failure, "
                  "never a zero count")

    # A path returned by the tracked inventory must not disappear between
    # discovery and reading: treating that race/deletion as an empty omission
    # would recreate the hand-maintained inventory escape this gate replaced.
    try:
        read_tree(["docs/selftest_missing_policy_surface.md"])
        problems.append("missing-tracked-file arm: unreadable inventory member "
                        "did not raise InventoryError")
    except InventoryError:
        passed += 1
        print("  ok   caught: an unreadable tracked policy file is a hard "
              "inventory failure")

    total = len(arms) + 2
    if problems:
        for problem in problems:
            print("  -", problem)
        print(f"baremetal-scope selftest: FAIL ({len(problems)} problem(s))")
        return 1
    print(f"baremetal-scope selftest: PASS ({total} arm(s), "
          f"{len(pristine)} file(s) in the discovered inventory)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        tree = read_tree(inventory())
    except InventoryError as exc:
        print(f"baremetal-scope: INVENTORY FAILURE: {exc}")
        return 2
    findings = scan(tree)
    for finding in findings:
        print("  -", finding)
    if findings:
        print(f"baremetal-scope: FAIL ({len(findings)} finding(s) across "
              f"{len(tree)} scanned file(s))")
        return 1
    print(f"baremetal-scope: OK (0 findings across {len(tree)} tracked "
          "first-party file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
