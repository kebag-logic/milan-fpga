#!/usr/bin/env python3
"""Plant product mutants in a copy of docs_inventory.py and run its --selftest on each.

Usage: mutants_r787_3.py SOURCE WORKDIR [JOBS]
Prints one line per mutant: KILLED or SURVIVED, the mutant's name, and the first failing control.
An IDENTITY control must survive; a mutant whose anchor text is missing is reported as NOT-APPLIED.
"""
from __future__ import annotations

import concurrent.futures
import pathlib
import subprocess
import sys

GROUP = 'grouped.setdefault(lanes[finding.page], []).append((finding, line))'
WRITE = '(directory / f"{slug}.md").write_text("\\n".join(body), encoding="utf-8")'
SLUG = 'slug = re.sub(r"[^a-z0-9]+", "-", lane.lower()).strip("-")'
LOOP = 'for lane, entries in sorted(grouped.items()):'
ENTRY = 'for finding, line in entries:'
TITLE = 'body = [f"# D0 findings: {lane}", "", f"Verified against dev `{verified_at}`.",'
CITED = 'f"Source lines cite dev `{cited_at}`.", ""]'
HEAD = 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES])'
AUD = 'for line in text.split("\\n")[:BANNER_SCAN_LINES]:'
SCAN = 'BANNER_SCAN_LINES = 15'
REQ = r'(r"(REQUIREMENTS|THIRD_PARTY)\.md|docs/(reference|integration|traceability)/.*", "reference"),'
OVER = r'(r"(README|QUICKSTART)\.md|docs/(README|GLOSSARY|DOC_GENERATION)\.md", "overview and guides"),'
GUIDES = r'(r"docs/(guides|overview|limitations|diagrams)/.*", "overview and guides"),'
ARCH = '(r"docs/history/.*", "archive"),'

MUTANTS: list[tuple[str, str, str, str]] = [
    ("IDENTITY", "ruling-none", "", ""),
    # Lanes merged into one file.
    ("LM1 one constant lane, one title", "lane-merge", GROUP,
     'grouped.setdefault("all", []).append((finding, line))'),
    ("LM2 one file, each lane's titled section kept", "lane-merge", WRITE,
     'open(directory / "all.md", "a", encoding="utf-8").write("\\n".join(body))'),
    ("LM3 every entry under the README's lane", "lane-merge", GROUP,
     'grouped.setdefault(lanes["README.md"], []).append((finding, line))'),
    ("LM4 last lane overwrites one shared file", "lane-merge", WRITE,
     '(directory / "all.md").write_text("\\n".join(body), encoding="utf-8")'),
    # An entry filed outside its page's lane.
    ("LF1 REQUIREMENTS routed to overview", "lane-misfile", REQ,
     r'(r"(REQUIREMENTS|THIRD_PARTY)\.md|docs/(reference|integration|traceability)/.*", "overview and guides"),'),
    ("LF2 README routed to reference", "lane-misfile", OVER,
     r'(r"(README|QUICKSTART)\.md|docs/(README|GLOSSARY|DOC_GENERATION)\.md", "reference"),'),
    ("LF3 guides routed to reference", "lane-misfile", GUIDES,
     r'(r"docs/(guides|overview|limitations|diagrams)/.*", "reference"),'),
    ("LF4 reference and overview swapped at filing", "lane-misfile", GROUP,
     'grouped.setdefault({"reference": "overview and guides", "overview and guides": "reference"}'
     '.get(lanes[finding.page], lanes[finding.page]), []).append((finding, line))'),
    ("LF5 the copy filed under its recording page's lane", "lane-misfile", GROUP,
     'grouped.setdefault(lanes[next(f.page for f, _ in located if f.ident == finding.ident)], [])'
     '.append((finding, line))'),
    ("LF6 only the copy on REQUIREMENTS filed in overview", "lane-misfile", GROUP,
     'grouped.setdefault("overview and guides" if finding.page == "REQUIREMENTS.md" else lanes[finding.page], [])'
     '.append((finding, line))'),
    ("LF7 only the guide's entry filed in reference", "lane-misfile", GROUP,
     'grouped.setdefault("reference" if finding.page == "docs/guides/A.md" else lanes[finding.page], [])'
     '.append((finding, line))'),
    ("LF8 archive entries filed in overview at filing", "lane-misfile", GROUP,
     'grouped.setdefault("overview and guides" if lanes[finding.page] == "archive" else lanes[finding.page], [])'
     '.append((finding, line))'),
    ("LF9 archive routed to overview in the table", "lane-misfile", ARCH,
     '(r"docs/history/.*", "overview and guides"),'),
    ("LD1 every entry also appended to every other lane", "lane-duplicate", GROUP,
     'grouped.setdefault(lanes[finding.page], []).append((finding, line))\n'
     '    grouped = {lane: own + [e for other, rest in grouped.items() if other != lane for e in rest]'
     ' for lane, own in grouped.items()}'),
    ("LD2 reference's entry also appended to overview", "lane-duplicate", GROUP,
     'grouped.setdefault(lanes[finding.page], []).append((finding, line))\n'
     '    grouped.get("overview and guides", []).extend(grouped.get("reference", []))'),
    ("LD3 overview's entries also appended to reference", "lane-duplicate", GROUP,
     'grouped.setdefault(lanes[finding.page], []).append((finding, line))\n'
     '    grouped.get("reference", []).extend(grouped.get("overview and guides", []))'),
    # A lane file's name, title, order and baselines.
    ("LN1 lane file names swapped", "lane-name", SLUG,
     SLUG + '\n        slug = {"reference": "overview-and-guides", "overview-and-guides": "reference"}.get(slug, slug)'),
    ("LN2 slug keeps spaces", "lane-name", SLUG, 'slug = lane.lower()'),
    ("LT1 lane title loses its lane", "lane-title", TITLE,
     'body = ["# D0 findings", "", f"Verified against dev `{verified_at}`.",'),
    ("LT2 lane titles swapped", "lane-title", TITLE,
     'body = [f"# D0 findings: {dict(reference=\'overview and guides\').get(lane, \'reference\')}", "", '
     'f"Verified against dev `{verified_at}`.",'),
    ("LO1 entries reversed in a lane", "lane-order", ENTRY, 'for finding, line in entries[::-1]:'),
    ("LB1 lane baselines swapped", "lane-base", 'f"Source lines cite dev `{cited_at}`.", ""]',
     'f"Source lines cite dev `{verified_at}`.", ""]'),
    ("LK1 first lane only", "lane-drop", LOOP, 'for lane, entries in sorted(grouped.items())[:1]:'),
    ("LK2 last lane only", "lane-drop", LOOP, 'for lane, entries in sorted(grouped.items())[-1:]:'),
    ("LR1 --findings-dir exits 1 after writing", "lane-rc", '''        print(f"{directory / (slug + '.md')}: {len(entries)} finding(s)")
    return 0''', '''        print(f"{directory / (slug + '.md')}: {len(entries)} finding(s)")
    return 1'''),
    # The banner window.
    ("BN12 window 12", "banner", SCAN, 'BANNER_SCAN_LINES = 12'),
    ("BN14 window 14", "banner", SCAN, 'BANNER_SCAN_LINES = 14'),
    ("BN16 window 16", "banner", SCAN, 'BANNER_SCAN_LINES = 16'),
    ("BN17 window 17", "banner", SCAN, 'BANNER_SCAN_LINES = 17'),
    ("BN19 window 19", "banner", SCAN, 'BANNER_SCAN_LINES = 19'),
    ("BN1000 whole page", "banner", SCAN, 'BANNER_SCAN_LINES = 1000'),
    ("BH14 status head one short", "banner", HEAD, 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES - 1])'),
    ("BH16 status head one long", "banner", HEAD, 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES + 1])'),
    ("BH-all status head whole text", "banner", HEAD, 'head = text'),
    ("BD banner search dropped", "banner", 'banner = BANNER_RE.search(head)', 'banner = None'),
    ("BO head starts one line late", "banner", HEAD, 'head = "\\n".join(text.split("\\n")[1:BANNER_SCAN_LINES + 1])'),
    # The audience line shares the constant; the ruling names only the banner.
    ("AU14 audience window one short", "audience", AUD, 'for line in text.split("\\n")[:BANNER_SCAN_LINES - 1]:'),
    ("AU16 audience window one long", "audience", AUD, 'for line in text.split("\\n")[:BANNER_SCAN_LINES + 1]:'),
    ("AU2 audience window two lines", "audience", AUD, 'for line in text.split("\\n")[:2]:'),
    ("AU3 audience window three lines", "audience", AUD, 'for line in text.split("\\n")[:3]:'),
]


def run(args: tuple[int, tuple[str, str, str, str], str, pathlib.Path]) -> str:
    """Plant one mutant and report its selftest result."""
    index, (name, group, old, new), source, work = args
    if old and source.count(old) != 1:
        return f"NOT-APPLIED {group} :: {name} (anchor hits {source.count(old)})"
    folder = work / f"m{index:03d}" / "scripts"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "docs_inventory.py"
    target.write_text(source.replace(old, new) if old else source, encoding="utf-8")
    done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True,
                          cwd=work, check=False, timeout=120)
    fails = [line for line in done.stdout.splitlines() if line.startswith("selftest: FAIL")]
    if done.returncode == 0:
        return f"SURVIVED {group} :: {name}"
    first = fails[0][15:150] if fails else (done.stderr.strip().splitlines() or ["no output"])[-1][:135]
    return f"KILLED({len(fails)}) {group} :: {name} :: {first}"


def main() -> int:
    """Run the campaign."""
    source = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    work = pathlib.Path(sys.argv[2])
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        lines = list(pool.map(run, [(i, m, source, work) for i, m in enumerate(MUTANTS)]))
    print("\n".join(lines))
    killed = sum(line.startswith("KILLED") for line in lines)
    survived = sum(line.startswith("SURVIVED") for line in lines)
    print(f"total {len(lines)} killed {killed} survived {survived} "
          f"not-applied {sum(line.startswith('NOT-APPLIED') for line in lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
