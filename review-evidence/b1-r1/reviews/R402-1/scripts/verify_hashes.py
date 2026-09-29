#!/usr/bin/env python3
"""Cross-check the archived bench packet against the two findings pages.

usage: verify_hashes.py <packet-root: .../review-evidence/b1-r1> <repo-root at the reviewed head>

Checks, printing one line per check and a final PASS/FAIL count:
  1. every line of author/MANIFEST.sha256 matches the archived file bytes;
  2. every MANIFEST.json published_sha256 matches the archived file bytes;
  3. every tool hash quoted in the pages matches author/tools/<file>;
  4. every raw-artifact row (action, file, bytes, sha256) in the pages equals the
     action's archived raw-artifacts.json entry, and the reverse (no unlisted raw file);
  5. archived analysis files that are also raw (baseline controller.jsonl, dryrun and
     final console/controller) hash to the raw-artifacts.json value.
No network, no bench access.
"""
import hashlib, json, re, sys
from pathlib import Path

pk, repo = Path(sys.argv[1]), Path(sys.argv[2])
au = pk / "author"
ok = bad = 0


def res(cond, msg):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
    print(("PASS " if cond else "FAIL ") + msg)


sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

# 1. author manifest
for line in (au / "MANIFEST.sha256").read_text().splitlines():
    if not line.strip():
        continue
    h, name = line.split(None, 1)
    name = name.lstrip("*").strip()
    p = au / name
    res(p.exists() and sha(p) == h, "author manifest %s" % name)

# 2. publication manifest
for e in json.loads((pk / "MANIFEST.json").read_text()):
    p = pk / e["file"]
    res(p.exists() and sha(p) == e["published_sha256"], "published %s%s" % (e["file"], " (redacted)" if e["path_redacted"] else ""))

pages = {n: (repo / "docs/findings" / n).read_text() for n in ("599_394_E1_LINK_CYCLES.md", "387_SOFTWARE_GM_STEP.md")}

# 3. tool hashes quoted in the pages
tool_rows = {
    "b1_action.py": "b1_action.py", "b1_analyze.py": "b1_analyze.py", "b1_summary.py": "b1_summary.py",
    "census_compare.py": "census_compare.py", "wire_summary.py": "wire_summary.py", "console_poll.py": "console_poll.py",
    "Controller reader": "avdecc_ro.py", "Controller actions": "a438_controller.py", "phc_restore.py": "phc_restore.py",
}
for page, text in pages.items():
    for row in re.findall(r"^\| ([^|]+) \| `([0-9a-f]{64})` \|$", text, re.M):
        label, h = row
        f = next((v for k, v in tool_rows.items() if k in label), None)
        if f:
            res(sha(au / "tools" / f) == h, "%s tool row '%s' = tools/%s" % (page, label.strip(), f))
        elif "configuration" in label and ("Grandmaster" in label or "Alignment" in label):
            f = "gm/gm.cfg" if "Grandmaster" in label else "gm/slave.cfg"
            res(sha(au / f) == h, "%s config row '%s' = %s" % (page, label.strip(), f))
        elif "UART grader" in label:
            res(sha(repo / "scripts/baremetal_uart_smoke.py") == h, "%s grader row = scripts/baremetal_uart_smoke.py at head" % page)
        else:
            print("INFO %s unverifiable-from-packet row '%s' %s" % (page, label.strip(), h))

# 4. raw artifact rows
rowre = re.compile(r"^\| (\w[\w-]*) \| (`[^`]+`|alignment port log|grandmaster port log) \| (\d+) \| `([0-9a-f]{64})` \|$", re.M)
seen = {}
for page, text in pages.items():
    for action, art, size, h in rowre.findall(text):
        ra = json.loads((au / "bench" / action / "raw-artifacts.json").read_text())
        by_hash = {e["sha256"]: e for e in ra}
        e = by_hash.get(h)
        name = art.strip("`")
        if name == "alignment port log":
            name = "ptp4l-slave.log"
        elif name == "grandmaster port log":
            name = "ptp4l-gm.log"
        cond = e is not None and e["size"] == int(size) and Path(e["path"]).name == name
        res(cond, "%s raw row %s/%s %s bytes" % (page, action, name, size))
        seen.setdefault(action, set()).add(h)
for action, hs in sorted(seen.items()):
    ra = json.loads((au / "bench" / action / "raw-artifacts.json").read_text())
    big = [e for e in ra if Path(e["path"]).suffix in (".jsonl", ".pcap", ".log") and e["size"] > 0]
    missing = [Path(e["path"]).name for e in big if e["sha256"] not in hs]
    res(not missing, "%s: every raw jsonl/pcap/log of the index is in a page table%s" % (action, (" missing " + ",".join(missing)) if missing else ""))

# 5. archived raw copies
for action in sorted(p.name for p in (au / "bench").iterdir()):
    ra = {Path(e["path"]).name: e for e in json.loads((au / "bench" / action / "raw-artifacts.json").read_text())}
    for f in sorted((au / "bench" / action).iterdir()):
        if f.name in ra and f.name not in ("raw-artifacts.json", "analysis.json", "check.txt"):
            red = f.name.endswith("capture.txt")
            if red:
                print("INFO %s/%s archived copy is redacted (interface name); raw hash %s, archived %s" % (
                    action, f.name, ra[f.name]["sha256"][:12], sha(f)[:12]))
            else:
                res(sha(f) == ra[f.name]["sha256"] and f.stat().st_size == ra[f.name]["size"], "archived raw copy %s/%s" % (action, f.name))

print("TOTAL pass=%d fail=%d" % (ok, bad))
sys.exit(1 if bad else 0)
