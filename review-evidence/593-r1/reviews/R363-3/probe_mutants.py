#!/usr/bin/env python3
"""R363-3 reviewer mutation probe for the #593 release oracles.

Usage: probe_mutants.py <repo> <out.tsv>
Copies tb/tools/torture_campaign.py into a private temp dir per mutant,
applies one textual mutation, runs the unchanged --self-test, and records
KILLED (rc 1 with a named FAIL/ERROR) or SURVIVED. The repo is never written.
Mutants are generated mechanically:
  A. every comparison operator inside the #593 oracle functions is flipped to
     its boundary twin (< <-> <=, > <-> >=) or negated (== <-> !=);
  B. every '+ observation_resolution_s' / '- resolution_s'-style term is dropped;
  C. every string fragment of the soak.mr-causes-and-hold and
     soak.tu-within-holdover assertion texts is removed;
  D. hand-written targeted mutants listed in TARGETED.
Parallelism: 8 workers.
"""
from __future__ import annotations

import ast
import concurrent.futures as cf
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FUNCS = ("check_release_tu", "check_release_tu_history", "_release_mr_records_valid",
         "_release_mr_toggles", "_release_media_resets", "check_release_mr")
ASSERTS = ("soak.mr-causes-and-hold", "soak.tu-within-holdover")
TARGETED = (
    ("T1 tu limit tightened", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2",
     "RELEASE_TU_RESOLUTION_LIMIT_S = 0.1249"),
    ("T2 tu limit one-sided", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2",
     "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25"),
    ("T3 minimum constant weakened", 'Decimal("0.25") if gm_events_s', 'Decimal("0.2499") if gm_events_s'),
    ("T4 minimum constant strengthened", 'Decimal("0.25") if gm_events_s', 'Decimal("0.2501") if gm_events_s'),
    ("T5 minimum drops R", "if minimum_clear_s is not None and clear_s + observation_resolution_s < minimum_clear_s:",
     "if minimum_clear_s is not None and clear_s < minimum_clear_s:"),
    ("T6 minimum uses 2R", "if minimum_clear_s is not None and clear_s + observation_resolution_s < minimum_clear_s:",
     "if minimum_clear_s is not None and clear_s + 2 * observation_resolution_s < minimum_clear_s:"),
    ("T7 minimum uses min GM", "minimum_clear_s = max(gm_events_s) + ", "minimum_clear_s = min(gm_events_s) + "),
    ("T8 latest clear uses 2R", "latest_clear_s = clear_s + observation_resolution_s",
     "latest_clear_s = clear_s + 2 * observation_resolution_s"),
    ("T9 deadline drops R", "deadline_s = last_discontinuity_s + holdover_bound_s + observation_resolution_s",
     "deadline_s = last_discontinuity_s + holdover_bound_s"),
    ("T10 deadline uses first event", "last_discontinuity_s = max(events_s)", "last_discontinuity_s = min(events_s)"),
    ("T11 single limit literal 0.25", "    resolution_limit_s = RELEASE_TU_RESOLUTION_LIMIT_S\n",
     "    resolution_limit_s = 0.25\n"),
    ("T12 history limit uses 0.25", "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):",
     "or not 0 <= observation_resolution_s < 0.25):"),
    ("T13 detail latest_clear drops R", "latest_clear_s=float(latest_clear_s),", "latest_clear_s=float(clear_s),"),
    ("T14 uncovered GM loop start strict", "        if not any(start_s - resolution_s <= gm_s < clear_s\n",
     "        if not any(start_s - resolution_s < gm_s < clear_s\n"),
    ("T15 uncovered GM loop drops R", "        if not any(start_s - resolution_s <= gm_s < clear_s\n",
     "        if not any(start_s <= gm_s < clear_s\n"),
    ("T16 uncovered GM loop includes clear", "        if not any(start_s - resolution_s <= gm_s < clear_s\n",
     "        if not any(start_s - resolution_s <= gm_s <= clear_s\n"),
    ("T17 uncovered GM loop removed", "            return \"FAIL\", dict(detail, why=\"GM change lacks a covering tu minimum\", gm_change_s=event)",
     "            pass"),
    ("T18 pdu index floor -1", ' or pdu["pdu_index"] < 0\n', ' or pdu["pdu_index"] < -1\n'),
    ("T19 pdu index floor 1", ' or pdu["pdu_index"] < 0\n', ' or pdu["pdu_index"] < 1\n'),
    ("T20 plan tu limit literal 0.25", "tu_resolution_limit_s=RELEASE_TU_RESOLUTION_LIMIT_S,",
     "tu_resolution_limit_s=0.25,"),
    ("T21 single NOT RUN detail omits limit on early return",
     '        return "NOT RUN", dict(detail, why="complete interval, discontinuity and GM history required")',
     '        return "NOT RUN", {"why": "complete interval, discontinuity and GM history required"}'),
    ("T22 uncorrelated FAIL omits limit", 'return "FAIL", {"why": "uncorrelated tu fails", **detail}',
     'return "FAIL", {"why": "uncorrelated tu fails"}'),
    ("T23 mr capture NOT RUN omits detail",
     '        return "NOT RUN", dict(detail, why="recorded capture window required")',
     '        return "NOT RUN", {"why": "recorded capture window required"}'),
    ("T24 mr invalid-record NOT RUN omits detail",
     '        return "NOT RUN", dict(detail, why="invalid recorded evidence")',
     '        return "NOT RUN", {"why": "invalid recorded evidence"}'),
    ("T25 history nested verdict omits detail",
     '            return verdict, dict(detail, interval=interval, evidence=evidence)',
     '            return verdict, dict(interval=interval, evidence=evidence)'),
    ("T26 history finite-event NOT RUN omits detail",
     '        return "NOT RUN", dict(detail, why="finite event history required")',
     '        return "NOT RUN", {"why": "finite event history required"}'),
    ("T27 history interval NOT RUN omits detail",
     '            return "NOT RUN", dict(detail, why="ordered, separate positive intervals required")',
     '            return "NOT RUN", {"why": "ordered, separate positive intervals required"}'),
)


def func_spans(text: str) -> list[tuple[int, int]]:
    tree = ast.parse(text)
    return [(n.lineno, n.end_lineno) for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name in FUNCS]


def operator_mutants(text: str) -> list[tuple[str, str, str]]:
    lines = text.splitlines(keepends=True)
    out = []
    swaps = {"<=": "<", "<": "<=", ">=": ">", ">": ">=", "==": "!=", "!=": "=="}
    pat = re.compile(r"(?<![<>=!-])(<=|>=|==|!=|<|>)(?![<>=])")
    for lo, hi in func_spans(text):
        for idx in range(lo - 1, hi):
            line = lines[idx]
            code = line.split("#", 1)[0]
            # skip lines that are pure string/docstring content or annotations
            if code.strip().startswith(('"', "'", "def ", ")", "->")) or "->" in code:
                continue
            for m in pat.finditer(code):
                # ignore operators inside string literals on this line
                if code[:m.start()].count('"') % 2 == 1:
                    continue
                new = line[:m.start()] + swaps[m.group(1)] + line[m.end():]
                out.append((f"A L{idx + 1} col{m.start()} {m.group(1)}->{swaps[m.group(1)]}", idx, new))
            for term in re.finditer(r"\s[+-] (observation_resolution_s|resolution_s|Decimal\(str\(resolution_s\)\)|"
                                    r"Decimal\(str\(observation_resolution_s\)\))", code):
                new = line[:term.start()] + line[term.end():]
                out.append((f"B L{idx + 1} drop '{term.group(0).strip()}'", idx, new))
    return [(name, "".join(lines[:i]) + new + "".join(lines[i + 1:]), "") for name, i, new in out]


def assert_mutants(text: str) -> list[tuple[str, str, str]]:
    out = []
    lines = text.splitlines(keepends=True)
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "AssertSpec"
                and isinstance(node.args[0], ast.Constant) and node.args[0].value in ASSERTS):
            # Implicitly concatenated literals merge into one AST constant, so
            # enumerate the STRING tokens of the clause argument instead.
            import io
            import tokenize
            arg = node.args[1]
            chunk = "".join(lines[arg.lineno - 1:arg.end_lineno])
            for tok in tokenize.generate_tokens(io.StringIO(chunk).readline):
                if tok.type != tokenize.STRING or len(tok.string) <= 2:
                    continue
                lineno = arg.lineno + tok.start[0] - 1
                line = lines[lineno - 1]
                new = line[:tok.start[1]] + '""' + line[tok.end[1]:]
                mutated = "".join(lines[:lineno - 1]) + new + "".join(lines[lineno:])
                out.append((f"C {node.args[0].value} L{lineno} drop {tok.string[:70]!r}", mutated, ""))
    return out


def targeted(text: str) -> list[tuple[str, str, str]]:
    out = []
    for name, old, new in TARGETED:
        if text.count(old) != 1:
            out.append((name, None, f"anchor count {text.count(old)}"))
        else:
            out.append((name, text.replace(old, new), ""))
    return out


def run(item: tuple[str, str | None, str]) -> tuple[str, str, str]:
    name, mutated, note = item
    if mutated is None:
        return name, "ANCHOR-MISSING", note
    with tempfile.TemporaryDirectory(prefix="r363p-") as d:
        p = Path(d) / "torture_campaign.py"
        p.write_text(mutated, encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-B", str(p), "--self-test"], capture_output=True,
                               text=True, timeout=600)
        except subprocess.TimeoutExpired:
            return name, "TIMEOUT", ""
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", r.stderr, re.M)))
        if r.returncode == 0:
            return name, "SURVIVED", ""
        if failed:
            return name, "KILLED", ",".join(failed)
        return name, f"CRASH rc={r.returncode}", r.stderr.strip().splitlines()[-1][:120] if r.stderr.strip() else ""


def main() -> int:
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    text = (repo / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
    items = operator_mutants(text) + assert_mutants(text) + targeted(text)
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(run, items))
    with out.open("w") as f:
        for name, status, note in results:
            f.write(f"{status}\t{name}\t{note}\n")
    counts = {}
    for _, s, _ in results:
        counts[s.split()[0]] = counts.get(s.split()[0], 0) + 1
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
