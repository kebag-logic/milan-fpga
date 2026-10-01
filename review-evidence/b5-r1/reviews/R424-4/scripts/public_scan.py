#!/usr/bin/env python3
"""Public-text scan of the B5 page, PR body, commit messages and evidence archive.

usage: public_scan.py <repo> <archive-git-dir> <pr-body.md> <out-dir>

Three pattern families, all built in memory and never written:

1. DERIVED: the private values the archive's mask commit replaced. For every
   hunk of `git diff -U0 PRE MASK -- review-evidence/b5-r1/author` whose
   removed and added line counts are equal, each added line containing a
   `<label>` is turned into a regex and matched against its removed line; the
   captured text is that label's private value. Values are scanned literally
   (word-bounded) when they are not bare numbers; bare numbers are scanned
   only in the label's own context (a channel count or a channel index next
   to the word channel or ch). The same is done for the peer's stream counts
   the round 4 ruling withdrew, read from the page at the round 3 head.
2. RULES: the repository's own scrub rules (scripts/docs_check.py
   SCRUB_RULES: peer, switch-vendor, lab, suite and plan names, home paths,
   bench addresses, bench host prefix, MAC-derived interfaces, USB serials).
3. GENERIC: reviewer classes for interface names, USB bus positions, SoC
   product names, digital-audio link types, instrument vendors, host names,
   wiring words, clock-topology words and peer stream counts.

Every pattern must first hit a planted line built in memory, or the scan
refuses. Output names the class, the target and the line, never a derived
value: for DERIVED hits only path:line is printed; for the other families the
public target lines (page, PR body, commit messages) are printed in full, and
archive hits are printed as path:line only.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

PRE = "ef3a709151f9bdbd4718c0783d0b8991ede7fd36"
MASK = "8e6be4329008137a152f9171638e48a43e549fb7"
BASE = "e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b"
HEAD = "e216dfe4f0cab7b0c7352d7973acb4d33c157f70"
R3 = "cf38633ad9a5bdb05517bedba73ce50965af967b"
PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
LABEL = re.compile(r"<([a-z][a-z0-9_-]*)>")
NUM_WORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
             "thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty")


def git(gdir, *args, bare=False):
    flag = ["--git-dir", gdir] if bare else ["-C", gdir]
    return subprocess.run(["git", *flag, *args], check=True,
                          capture_output=True).stdout.decode(errors="replace")


def derive_mask_values(archive):
    diff = git(archive, "diff", "-U0", PRE, MASK, "--", "review-evidence/b5-r1/author", bare=True)
    values = {}
    rem, add, unmatched = [], [], []

    def flush():
        # Each added line carrying a label is matched against every removed
        # line of its hunk, so hunks whose line counts differ are covered too.
        for a in add:
            if not LABEL.search(a):
                continue
            parts = LABEL.split(a)
            rx = "".join(re.escape(p) if i % 2 == 0 else "(.+?)" for i, p in enumerate(parts))
            for r in rem:
                m = re.fullmatch(rx, r)
                if m:
                    for lab, val in zip(parts[1::2], m.groups()):
                        if val != f"<{lab}>":
                            values.setdefault(lab, set()).add(val.strip())
                    break
            else:
                unmatched.append(a)
        rem.clear()
        add.clear()

    for line in diff.splitlines():
        if line.startswith("@@"):
            flush()
        elif line.startswith("-") and not line.startswith("---"):
            rem.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            add.append(line[1:])
    flush()
    # The peer map line was reworded as well as labelled, so it never pairs:
    # take its phrases from the removed side directly.
    for line in diff.splitlines():
        if line.startswith("-") and "dynamic map:" in line:
            seg = line.split("dynamic map:", 1)[1].split(". External", 1)[0]
            for v in re.findall(r"(?:clusters?|inputs?|outputs?) \d+(?:/\d+)?(?: channels)? ?\d*-\d+", seg):
                values.setdefault("peer-channel-map", set()).add(v.strip())
    return values, len(unmatched)


def derive_peer_counts(repo):
    old = git(repo, "show", f"{R3}:{PAGE}")
    nums = set()
    for rx in (r"All 4 DUT and (\d+) reference-peer stream states",
               r"All (\d+) unbound", r"in (\d+) of (\d+) entries",
               r"owns (\w+) audio clusters", r"stream ports' (\d+) clusters",
               r"(\d+) reads of type 0x0010", r"indices 0 to (\d+)"):
        for m in re.finditer(rx, old):
            nums.update(m.groups())
    return nums


def build_patterns(mask_values, peer_counts):
    pats = []  # (family, class, regex, planted line)
    for lab, vals in sorted(mask_values.items()):
        for v in sorted(vals):
            if re.fullmatch(r"\d+(?:/\d+)?", v):
                if "/" in v:
                    a, b = v.split("/")
                    rx = rf"\b{a}\s*/\s*{b}\b|channels?\s+{a}\s*(?:and|,)\s*{b}\b"
                    plant = f"capture channels {a} and {b}"
                elif "count" in lab:
                    rx = rf"\b{v}\s*ch\b|\b{v}[- ]channels?\b|all {v} channels|cap-all-{v}ch"
                    plant = f"all {v} channels kept"
                else:
                    rx = rf"(?:capture|cap)[^.\n|]{{0,30}}channels?\s+{v}\b|\bch\s*{v}\b"
                    plant = f"capture channel {v}"
            elif len(v) < 3:
                continue
            else:
                rx = r"(?<![A-Za-z0-9])" + re.escape(v) + r"(?![A-Za-z0-9])"
                plant = f"x {v} y"
            pats.append(("DERIVED", f"mask:{lab}", re.compile(rx, re.I), plant))
    for v in sorted(peer_counts):
        rx = (rf"\b{v}\b[^.\n|]{{0,40}}(?:stream states?|streams?\b|stream ports?|clusters?|entries)"
              rf"|(?:stream states?|stream ports?|clusters?|entries)[^.\n|]{{0,20}}\b{v}\b")
        pats.append(("DERIVED", "peer-stream-count", re.compile(rx, re.I),
                     f"the {v} peer stream states"))
    spec = importlib.util.spec_from_file_location("docs_check", Path(REPO) / "scripts/docs_check.py")
    dc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dc)
    fixtures = {label: None for _, label, _ in dc.SCRUB_RULES}
    for fx in getattr(dc, "_SCRUB_FIXTURES", ()):
        # (relpath, text, label) shaped fixtures in the gate's own self-test
        text = next((x for x in fx if isinstance(x, str) and "\n" not in x and x not in fixtures), None)
        lab = next((x for x in fx if isinstance(x, str) and x in fixtures), None)
        if lab and text and fixtures[lab] is None:
            fixtures[lab] = text
    for rx, label, _ in dc.SCRUB_RULES:
        plant = fixtures.get(label)
        if plant is None or not rx.search(plant):
            own = [*getattr(dc, "_LAB_TOKENS", ()), *(str(getattr(dc, n, "")) for n in (
                "_PLAN_TOKEN", "_PLAN_PHRASE", "_SUITE_TOKEN", "_PEER_TOKEN",
                "_VENDOR_TOKEN", "_VENDOR_MARK"))]
            plant = next((s for s in _rule_plants() + [f"x {t} y" for t in own if t]
                          if rx.search(s)), None)
        pats.append(("RULES", f"docs_check:{label}", rx, plant))
    generic = [
        ("interface-name", r"\b(?:enp\d+s\d+\w*|eno\d+\w*|ens\d+\w*|eth\d+|wlp\w+|wlan\d+|enx[0-9a-f]{6,}|br-[0-9a-f]{6,})\b", "dev <host-iface> up"),
        ("usb-bus-position", r"usb-\d{4}:[0-9a-f]{2}:[0-9a-f]{2}\.\d|\b\d-\d+(?:\.\d+)*:\d\.\d\b", "<usb-bus-position>"),
        ("soc-product", r"\bAM\d{2,4}\w*|\bBeagle\w*|\bSitara\b|\bJ7\d\w*", "an AM335x board"),
        ("link-type", r"\bAES(?:3|/EBU|-EBU)?\b|S/?PDIF|\bADAT\b|TOSLINK|\boptical\b|\bcoax(?:ial)?\b|\bMADI\b", "the AES output"),
        ("instrument-vendor", r"\b(?:RME|Fireface|Babyface|Digiface|HDSPe?|Focusrite|Scarlett|Clarett|MOTU|Behringer|Steinberg|PreSonus|Apogee|Antelope|Audient|Tascam|Mackie|Lynx|Prism|Ferrofish|Merging|Digigram|Roland|Yamaha|Allen ?& ?Heath|Midas|Saleae|Keysight|Tektronix|Rigol|Audio Precision|Motu|Zoom)\b", "an RME interface"),
        ("host-name", r"\bpw\d+\b|\bamx-\w+|\bubuntu\b|\bbuild ?box\b|\.local\b|\.lan\b", "on pw1 today"),
        ("wiring", r"\b(?:cable[ds]?|cabled|patch(?:ed)? (?:cable|to)|wired to|plugged|XLR|BNC|RCA|jack \d|switch port \d+|port \d+ of the)\b", "an XLR cable"),
        ("clock-topology", r"\bword ?clock\b|\bwordclock\b|\bclock master\b|\bslaved\b|\bexternal clock\b|\bgrandmaster\b|\bGM\b", "a word clock line"),
        ("peer-stream-count-generic", rf"\b(?:\d+|{NUM_WORDS})\b[^.\n|]{{0,30}}\b(?:stream states?|streams|stream ports?|(?:audio )?clusters)\b", "the 7 peer stream states"),
        ("capture-channel-generic", r"capture channels? \d+|\b\d+\s*ch\.raw|cap-all-\d+ch", "capture channel 3"),
    ]
    for cls, rx, plant in generic:
        pats.append(("GENERIC", cls, re.compile(rx, re.I if cls not in ("peer-stream-count-generic",) else re.I), plant))
    return pats


def _rule_plants():
    # Fallback plants for the repository rules, assembled from code points as
    # the gate assembles its own tokens, so this file never spells them.
    a = lambda *c: "".join(map(chr, c))
    return [
        a(47, 104, 111, 109, 101) + "/someone/x", a(49, 57, 50, 46, 49, 54, 56) + ".7.1",
        a(97, 109, 120) + "-box", a(101, 110, 120) + "00e04c680001",
        "serial/by-id/" + a(117, 115, 98) + "-X1", a(68, 83, 50, 48) + " unit",
        a(97, 117, 100, 105, 111, 116, 101, 99, 104, 110, 105, 107),
        a(97, 118, 110, 117), a(97, 101, 116, 115) + " suite",
        a(109, 105, 108, 97, 110, 101, 110, 100, 115, 116, 97, 116) + "x",
        a(100, 38, 98) + " x",
    ]


def targets(repo, archive, pr_body, tip):
    out = []  # (target-kind, name, text, public_print)
    out.append(("page", f"{PAGE}@{HEAD[:8]}", git(repo, "show", f"{HEAD}:{PAGE}"), True))
    out.append(("index", f"docs/findings/README.md@{HEAD[:8]}",
                "\n".join(l for l in git(repo, "show", f"{HEAD}:docs/findings/README.md").splitlines()
                          if "117_AUDIO_CONTINUITY" in l), True))
    out.append(("pr-body", "PR #628 body (live)", Path(pr_body).read_text(encoding="utf-8"), True))
    out.append(("commits", f"messages {BASE[:8]}..{HEAD[:8]}",
                git(repo, "log", "--format=%H%n%B", f"{BASE}..{HEAD}"), True))
    added = [l[1:] for l in git(repo, "diff", "-U0", BASE, HEAD).splitlines()
             if l.startswith("+") and not l.startswith("+++")]
    out.append(("added-lines", f"added lines {BASE[:8]}..{HEAD[:8]}", "\n".join(added), True))
    files = git(archive, "ls-tree", "-r", "--name-only", tip, "review-evidence/b5-r1", bare=True).split()
    for f in files:
        raw = subprocess.run(["git", "--git-dir", archive, "show", f"{tip}:{f}"],
                             capture_output=True, check=True).stdout
        if b"\0" in raw[:8000]:
            continue
        out.append(("archive", f, raw.decode(errors="replace"), False))
    return out


def main():
    global REPO
    REPO, archive, pr_body, outdir = sys.argv[1:5]
    tip = git(archive, "rev-parse", "b5-review-evidence", bare=True).strip()
    mv, n_unpaired = derive_mask_values(archive)
    pc = derive_peer_counts(REPO)
    pats = build_patterns(mv, pc)
    lines = [f"archive tip {tip}; mask {MASK[:8]} over {PRE[:8]}; page head {HEAD}"]
    lines.append(f"derived mask labels: {', '.join(f'{k} ({len(v)} value(s))' for k, v in sorted(mv.items()))}")
    lines.append(f"labelled lines not paired by the generic derivation: {n_unpaired} (peer map handled by phrase)")
    lines.append(f"derived peer stream-count values: {len(pc)} (from the round 3 page)")
    bad_plant = [c for _, c, rx, p in pats if not p or not rx.search(p)]
    lines.append(f"patterns: {len(pats)}; planted controls hit: {len(pats) - len(bad_plant)} of {len(pats)}")
    if bad_plant:
        lines.append(f"REFUSED: unplanted or missed controls: {bad_plant}")
        print("\n".join(lines))
        sys.exit(2)
    tg = targets(REPO, archive, pr_body, tip)
    kinds = sorted({k for k, *_ in tg})
    lines.append(f"targets: {', '.join(f'{k} {sum(1 for x in tg if x[0] == k)}' for k in kinds)} "
                 f"(archive: every text file under review-evidence/b5-r1 at the tip)")
    summary = {}
    detail = []
    for fam, cls, rx, _ in pats:
        for kind, name, text, public in tg:
            for n, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    key = (fam, cls, kind)
                    summary[key] = summary.get(key, 0) + 1
                    if fam == "DERIVED" or not public:
                        detail.append(f"{fam} {cls} {kind} {name}:{n}")
                    else:
                        detail.append(f"{fam} {cls} {kind} {name}:{n}: {line.strip()[:220]}")
    lines.append("")
    lines.append("hits by family, class and target (absent = 0):")
    for (fam, cls, kind), c in sorted(summary.items()):
        lines.append(f"  {fam:8s} {cls:40s} {kind:12s} {c}")
    by_class = {}
    for fam, cls, _, _ in pats:
        by_class.setdefault((fam, cls), 0)
    zero = [f"{f}:{c}" for (f, c) in by_class if not any(k[0] == f and k[1] == c for k in summary)]
    lines.append(f"classes with 0 hits on every target: {len(zero)} of {len(by_class)}")
    lines.append("")
    lines.append("hit detail:")
    lines.extend("  " + d for d in detail)
    Path(outdir, "public_scan.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:8 + len(summary)]))


if __name__ == "__main__":
    REPO = None
    main()
