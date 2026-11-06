#!/usr/bin/env python3
"""Disposable mutants of scripts/docs_inventory.py for the round 3 lane and banner controls.

usage: r3_mutants.py <repo clone> <commit> <scratch dir> <jobs>
Each mutant is one exact text replacement on the file at <commit>; `--selftest` of the
mutated copy decides: rc 0 survives, rc 1 killed. Prints one TSV row per mutant.
"""
import concurrent.futures as cf
import pathlib
import subprocess
import sys

GROUP = "grouped.setdefault(lanes[finding.page], []).append((finding, line))"
WRITE = '(directory / f"{slug}.md").write_text("\\n".join(body), encoding="utf-8")'
SLUG = 'slug = re.sub(r"[^a-z0-9]+", "-", lane.lower()).strip("-")'
CONST = "BANNER_SCAN_LINES = 15"
HEAD = 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES])'
AUD = 'for line in text.split("\\n")[:BANNER_SCAN_LINES]:'
SEARCH = "banner = BANNER_RE.search(head)"
ALSO = GROUP + "\n        "
M = [
    ("IDENTITY", GROUP, GROUP),
    ("L01 every finding under reference", GROUP, 'grouped.setdefault("reference", []).append((finding, line))'),
    ("L02 every finding under overview", GROUP, 'grouped.setdefault("overview and guides", []).append((finding, line))'),
    ("L03 copy under its origin's lane", GROUP, "grouped.setdefault(lanes[finding.origin or finding.page], []).append((finding, line))"),
    ("L04 lanes merged into one file, titled sections kept", WRITE,
     'open(directory / "all.md", "a", encoding="utf-8").write("\\n".join(body))'),
    ("L05 recorded finding under a wrong named lane", GROUP,
     'grouped.setdefault(lanes[finding.page] if finding.origin else "design", []).append((finding, line))'),
    ("L06 copy under a wrong named lane", GROUP,
     'grouped.setdefault("design" if finding.origin else lanes[finding.page], []).append((finding, line))'),
    ("L07 the guide's entry also filed after the reference lane's entries", GROUP,
     ALSO + 'if finding.page == "docs/guides/A.md": grouped.setdefault("reference", []).append((finding, line))'),
    ("L08 every entry also filed in a third catch-all file", GROUP,
     ALSO + 'grouped.setdefault("all findings", []).append((finding, line))'),
    ("L09 a copy also filed under its origin's lane (duplicate)", GROUP,
     ALSO + "if finding.origin: grouped.setdefault(lanes[finding.origin], []).append((finding, line))"),
    ("L10 the reference lane's entry also filed last in the overview lane", GROUP,
     ALSO + 'if lanes[finding.page] == "overview and guides" and finding.page.startswith("docs/"): '
     'grouped["overview and guides"] += [e for e in grouped.get("reference", [])]'),
    ("L11 an archive page's entry filed under overview", GROUP,
     'grouped.setdefault("overview and guides" if finding.page.startswith("docs/history/") else lanes[finding.page], [])'
     ".append((finding, line))"),
    ("L12 lane files lose their unique name (first letter)", SLUG, "slug = lane[:1].lower()"),
    ("L13 every lane written to one name, last wins", WRITE,
     '(directory / "all.md").write_text("\\n".join(body), encoding="utf-8")'),
    ("L14 lane file renamed", WRITE, '(directory / f"lane-{slug}.md").write_text("\\n".join(body), encoding="utf-8")'),
    ("L15 a leading blank line in a lane file", WRITE,
     '(directory / f"{slug}.md").write_text("\\n" + "\\n".join(body), encoding="utf-8")'),
    ("L16 lane title dropped", 'body = [f"# D0 findings: {lane}", "", f"Verified', 'body = ["# D0 findings", "", f"Verified'),
    ("L17 baselines swapped in the lane file", 'f"Verified against dev `{verified_at}`.",\n                f"Source lines cite dev `{cited_at}`.", ""]',
     'f"Verified against dev `{cited_at}`.",\n                f"Source lines cite dev `{verified_at}`.", ""]'),
    ("L18 only the last finding of a lane kept", "for finding, line in entries:\n            body +=",
     "for finding, line in entries[-1:]:\n            body +="),
    ("L19 a copy's note dropped from its lane entry", 'f"- Contradicted by: {source_of(finding)}"', 'f"- Contradicted by: {finding.source}"'),
    ("L20 --findings-dir exits non-zero", 'print(f"{directory / (slug + \'.md\')}: {len(entries)} finding(s)")\n    return 0', 'print(f"{directory / (slug + \'.md\')}: {len(entries)} finding(s)")\n    return 1'),
    ("T4 the route's closing sentence dropped", '"That command still names its line.", ', ''),
    ("B1 the page's two baselines swapped", 'f"Statements on D0 pages were checked at dev `{verified_at}`.", "Other pages wait for their area lane.", "",\n           f"Findings cite source lines at dev `{cited_at}` and its submodule pins.", ""]',
     'f"Statements on D0 pages were checked at dev `{cited_at}`.", "Other pages wait for their area lane.", "",\n           f"Findings cite source lines at dev `{verified_at}` and its submodule pins.", ""]'),
    ("B14 window of 14", CONST, "BANNER_SCAN_LINES = 14"),
    ("B16 window of 16", CONST, "BANNER_SCAN_LINES = 16"),
    ("B17 window of 17", CONST, "BANNER_SCAN_LINES = 17"),
    ("B18 window of 18", CONST, "BANNER_SCAN_LINES = 18"),
    ("B19 window of 19", CONST, "BANNER_SCAN_LINES = 19"),
    ("B30 window of 30", CONST, "BANNER_SCAN_LINES = 30"),
    ("B31 status window one short", HEAD, 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES - 1])'),
    ("B32 status window one long", HEAD, 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES + 1])'),
    ("B33 banner searched on the whole page", SEARCH, "banner = BANNER_RE.search(text)"),
    ("B34 window counts non-blank lines", HEAD,
     'head = "\\n".join([x for x in text.split("\\n") if x.strip()][:BANNER_SCAN_LINES])'),
    ("B35 window taken from the page's end", HEAD, 'head = "\\n".join(text.split("\\n")[-BANNER_SCAN_LINES:])'),
    ("B36 banner rule removed", SEARCH, "banner = None"),
    ("B37 audience window one short (shared constant, not the banner)", AUD, 'for line in text.split("\\n")[:BANNER_SCAN_LINES - 1]:'),
    ("B38 audience window one long (shared constant, not the banner)", AUD, 'for line in text.split("\\n")[:BANNER_SCAN_LINES + 1]:'),
]


def run(args):
    index, (name, old, new), source, scratch = args
    if source.count(old) != 1:
        return name, "NOT-APPLIED", f"{source.count(old)} matches"
    where = scratch / f"m{index:02d}" / "scripts"
    where.mkdir(parents=True, exist_ok=True)
    target = where / "docs_inventory.py"
    target.write_text(source.replace(old, new), encoding="utf-8")
    done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True, timeout=500)
    lines = [x for x in (done.stdout + done.stderr).splitlines() if x.strip()]
    first = lines[0][:150] if lines else ""
    return name, {0: "SURVIVED", 1: "KILLED"}.get(done.returncode, f"rc{done.returncode}"), first


def main():
    repo, commit, scratch, jobs = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]), int(sys.argv[4])
    source = subprocess.run(["git", "-C", repo, "show", f"{commit}:scripts/docs_inventory.py"], capture_output=True,
                            text=True, check=True).stdout
    with cf.ThreadPoolExecutor(jobs) as pool:
        for row in pool.map(run, [(i, m, source, scratch) for i, m in enumerate(M)]):
            print("\t".join(row), flush=True)


if __name__ == "__main__":
    main()
