#!/usr/bin/env python3
"""Mechanical checks of the ledger's statements against the tree, the standards and the issue states.

Usage: python3 -I auto_checks.py <tree> <ledger.jsonl> <issues.json> <prs.json> <std-dir> <out.jsonl>

For every numeric or normative statement it records what was checked
mechanically and the result:

  path      every cited repository path (backticked, or a relative link) exists
            in the tree or in an initialised submodule;
  issue     every #N names an issue or PR, with its state; wording that calls a
            closed item open or pending is flagged;
  register  a `0xNNN` + `NAME` pair (REGISTER_MAP row or prose) matches the
            RTL's `A_NAME` constant, and a map row's reset literal matches the
            RTL's csr_default for it;
  version   a firmware VERSION literal equals `milan_csr.sv`'s, unless the
            sentence marks it as history;
  clause    a cited clause or table of one of the six standards exists;
  command   a `python3 <script> --flag`, `make -C <dir>`, or `<script>.sh`
            names a tracked script and a flag the script defines.

A flag is a candidate for the manual pass, not a finding.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

tree, ledger, issues_p, prs_p, std, out = (Path(a) for a in sys.argv[1:7])
issues = {i["number"]: ("issue", i["state"]) for i in json.loads(issues_p.read_text())}
issues.update({p["number"]: ("pr", p["state"]) for p in json.loads(prs_p.read_text())})

tracked = set(subprocess.run(["git", "-C", str(tree), "ls-files"], capture_output=True, text=True).stdout.split("\n"))
for sub in ("protocol-processor", "gptp-processor"):
    listed = subprocess.run(["git", "-C", str(tree / sub), "ls-files"], capture_output=True, text=True).stdout
    tracked |= {f"{sub}/{p}" for p in listed.split("\n") if p}
dirs = {str(Path(p).parent) for p in tracked} | {str(q) for p in tracked for q in Path(p).parents}

rtl = (tree / "hdl/common/csr/milan_csr.sv").read_text()
addr_of = {}
for m in re.finditer(r"\b(A_[A-Z0-9_]+)\s*=\s*(?:11)?'h([0-9A-Fa-f_]+)", rtl):
    addr_of.setdefault(m.group(1)[2:], int(m.group(2).replace("_", ""), 16))
reset_of = {}
for m in re.finditer(r"\bA_([A-Z0-9_]+)\[10:0\]:\s*csr_default\s*=\s*32'h([0-9A-Fa-f_]+)", rtl):
    reset_of[m.group(1)] = int(m.group(2).replace("_", ""), 16)
version = re.search(r"VERSION[^\n]*?32'h([0-9A-Fa-f_]{8,9})", rtl)
version = int(version.group(1).replace("_", ""), 16) if version else None

TEXTS = {"milan": ["milan-1.2.txt"], "1722.1": ["1722.1-2021.txt"], "1722": ["1722-2016.txt"],
         "802.1AS": ["802.1AS-2011.txt", "802.1AS-2011_Cor1-2013.txt", "802.1AS-2011_Cor_2-2015.txt"],
         "802.1Q": ["8021Q-2022.txt", "802.1Q-2018.txt", "802.1Q-2014.txt"], "802.1BA": ["802.1BA-2011.txt"]}
heads, tables = {}, {}
for key, files in TEXTS.items():
    h, t = set(), set()
    for f in files:
        txt = (std / f).read_text(errors="replace")
        h |= set(re.findall(r"(?m)^\s*(\d+(?:\.\d+)+)\.?\s+\S", txt))
        h |= set(re.findall(r"(?m)^\s*(?:Annex\s+)?([A-Z](?:\.\d+)+)\.?\s+\S", txt))
        t |= {n.replace("­", "-") for n in re.findall(r"Table\s+([A-Z0-9]+[-.­]\d+)", txt)}
    heads[key], tables[key] = h, t
STD = (r"(?P<std>Milan(?: v?1\.2)?|(?:IEEE )?1722\.1(?:-2021)?|(?:IEEE )?1722(?:-2016)?|"
       r"(?:IEEE )?802\.1AS(?:-2011)?(?:\s*(?:\+\s*)?Cor\s?[12](?:-20\d\d)?)?|(?:IEEE )?802\.1Q(?:-20\d\d)?|"
       r"(?:IEEE )?802\.1BA(?:-2011)?)")
CITE = re.compile(STD + r"[,]?\s+(?:Section |section |clause |Clause |§\s?|subclause )?"
                  r"(?P<num>(?:\d+|[A-Z])(?:\.\d+)+)(?![\d.]*\d)")
TAB = re.compile(STD + r"[,]?\s+Table\s+(?P<num>[A-Z0-9]+[-.]\d+)")


def key_of(s: str) -> str:
    s = s.replace("IEEE ", "")
    for k in ("Milan", "1722.1", "1722", "802.1AS", "802.1Q", "802.1BA"):
        if s.startswith(k):
            return "milan" if k == "Milan" else k
    return ""


PATH_RE = re.compile(r"`((?:hdl|sw|tb|syn|configs|scripts|avdecc|tests|ci|tools|docs|protocol-processor|"
                     r"gptp-processor|third_party|\.github)/[^`\s<>*{}$]*[^`\s<>*{}$/.,:;)])/?`")
LINK_RE = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
ISSUE_RE = re.compile(r"(?<![\w/&#])#(\d{1,4})\b|kebag-logic/milan-fpga/(?:issues|pull)/(\d+)")
OPEN_WORDS = re.compile(r"\b(open|pending|remains? on|remains? open|tracked (?:by|in|on)|until|follow-?up|owed|"
                        r"waits? (?:for|on)|blocked|not yet|outstanding|in flight|TODO)\b", re.IGNORECASE)
HISTORY = re.compile(r"\b(was|were|before|earlier|prior|previous|since|from|until|changelog|history|"
                     r"historical|old|older|then|at the time|measured|minimum|at least|>=)\b", re.IGNORECASE)
CMD_PY = re.compile(r"python3?\s+(?:-I\s+)?((?:[\w.-]+/)*[\w.-]+\.py)((?:\s+--?[\w-]+(?:[= ][^\s`|;&]+)?)*)")
CMD_SH = re.compile(r"(?<![\w/])((?:sw|scripts|tb|syn|tools|ci|protocol-processor|gptp-processor)/[\w./-]+\.sh)\b")
CMD_MAKE = re.compile(r"make\s+(?:-j\s*\d+\s+)?-C\s+([\w./-]+)")
REG_PAIR = re.compile(r"`?0x([0-9A-Fa-f]{3})`?\s*\|?\s*`([A-Z][A-Z0-9_]+)`|`([A-Z][A-Z0-9_]+)`\s*\(\s*`?0x([0-9A-Fa-f]{3})`?\s*\)")
ROW = re.compile(r"^\|\s*`0x([0-9A-Fa-f]{3})(?:[-–]0x[0-9A-Fa-f]{3})?`\s*\|\s*`([A-Z][A-Z0-9_]*)`\s*\|\s*([^|]*)\|\s*([^|]*)\|")


def exists(ref: str) -> bool:
    ref = ref.rstrip("/")
    return ref in tracked or ref in dirs


def check(rec: dict) -> dict:
    text, page = rec["text"], rec["page"]
    res: dict = {}
    base = Path(page).parent
    paths = [m.group(1) for m in PATH_RE.finditer(text)]
    for m in LINK_RE.finditer(text):
        target = m.group(1)
        if "://" in target or target.startswith("mailto:"):
            continue
        resolved = (base / target).as_posix()
        parts = []
        for part in resolved.split("/"):
            if part == "..":
                if parts:
                    parts.pop()
            elif part not in (".", ""):
                parts.append(part)
        paths.append("/".join(parts))
    if paths:
        missing = [p for p in paths if not exists(p) and not re.search(r"[<*]|\.\.\.", p)]
        res["path"] = {"n": len(paths), "missing": missing}
    nums = [int(a or b) for a, b in ISSUE_RE.findall(text)]
    if nums:
        states = {n: issues.get(n, ("unknown", "?")) for n in nums}
        closed = [n for n, (_, st) in states.items() if st in ("CLOSED", "MERGED")]
        res["issue"] = {"n": len(nums), "states": {str(n): f"{k}:{s}" for n, (k, s) in states.items()},
                        "closed_called_open": closed if (closed and OPEN_WORDS.search(text)) else [],
                        "unknown": [n for n, (k, _) in states.items() if k == "unknown"]}
    pairs = []
    row = ROW.match(text) if page == "docs/reference/REGISTER_MAP.md" else None
    if row:
        pairs.append((int(row.group(1), 16), row.group(2)))
    for m in REG_PAIR.finditer(text):
        if m.group(1):
            pairs.append((int(m.group(1), 16), m.group(2)))
        else:
            pairs.append((int(m.group(4), 16), m.group(3)))
    if pairs:
        bad = [f"0x{a:03X} {n} (RTL {('0x%03X' % addr_of[n]) if n in addr_of else 'none'})"
               for a, n in pairs if n in addr_of and addr_of[n] != a]
        unknown = [n for _, n in pairs if n not in addr_of]
        res["register"] = {"n": len(pairs), "mismatch": bad, "not_an_rtl_name": sorted(set(unknown))}
        if row and row.group(2) in reset_of:
            lit = re.search(r"0x([0-9A-Fa-f_]+)", row.group(4))
            if lit:
                doc = int(lit.group(1).replace("_", ""), 16)
                res["register"]["reset"] = ("ok" if doc == reset_of[row.group(2)]
                                            else f"MISMATCH doc 0x{doc:X} rtl 0x{reset_of[row.group(2)]:X}")
    for m in re.finditer(r"0x0002_?00([0-9A-Fa-f]{2})", text):
        v = 0x00020000 | int(m.group(1), 16)
        res.setdefault("version", {"n": 0, "other": []})
        res["version"]["n"] += 1
        if v != version and not HISTORY.search(text):
            res["version"]["other"].append(f"0x{v:08X}")
    cites = []
    for m in CITE.finditer(text):
        k = key_of(m.group("std"))
        if k:
            cites.append((k, m.group("num"), m.group("num") in heads[k]))
    for m in TAB.finditer(text):
        k = key_of(m.group("std"))
        if k:
            cites.append((k, "Table " + m.group("num"), m.group("num").replace(".", "-") in tables[k]
                          or m.group("num") in tables[k]))
    if cites:
        res["clause"] = {"n": len(cites), "missing": [f"{k} {n}" for k, n, ok in cites if not ok]}
    cmds = []
    for m in CMD_PY.finditer(text):
        script, flags = m.group(1), re.findall(r"--[\w-]+", m.group(2))
        here = script if exists(script) else None
        if here:
            body = (tree / script).read_text(errors="replace")
            cmds.append((script, [f for f in flags if f not in body]))
        else:
            cmds.append((script, ["SCRIPT MISSING"]))
    for m in CMD_SH.finditer(text):
        cmds.append((m.group(1), [] if exists(m.group(1)) else ["SCRIPT MISSING"]))
    for m in CMD_MAKE.finditer(text):
        d = m.group(1).rstrip("/")
        cmds.append((f"make -C {d}", [] if exists(d + "/Makefile") else ["NO MAKEFILE"]))
    if cmds:
        res["command"] = {"n": len(cmds), "problems": [f"{s}: {p}" for s, p in cmds if p]}
    return res


count = flagged = 0
with out.open("w", encoding="utf-8") as handle:
    for line in ledger.read_text(encoding="utf-8").split("\n"):
        if not line:
            continue
        rec = json.loads(line)
        if not (rec["numeric"] or rec["normative"]):
            continue
        res = check(rec)
        problems = any(v.get(k) for v in res.values() for k in
                       ("missing", "closed_called_open", "unknown", "mismatch", "other", "problems"))
        if isinstance(res.get("register", {}).get("reset"), str) and res["register"]["reset"].startswith("MIS"):
            problems = True
        count += 1
        flagged += problems
        handle.write(json.dumps({"page": rec["page"], "line": rec["line"], "auto": res, "flag": problems},
                                ensure_ascii=False) + "\n")
print(f"{count} statements, {flagged} flagged for the manual pass")
print(f"RTL: {len(addr_of)} CSR constants, {len(reset_of)} reset literals, VERSION 0x{version:08X}")
