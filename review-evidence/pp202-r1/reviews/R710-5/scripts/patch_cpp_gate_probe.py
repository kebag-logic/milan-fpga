"""Scan every C/C++ file a unified patch ADDS or MODIFIES with the parent Rule 11 gate's scan().

Usage: python3 -I patch_cpp_gate_probe.py <gate_scripts_dir> <patch> [<patch> ...]
New files are rebuilt whole from their '+' lines; for modified files only the added lines are
scanned (a line-local check such as ES.10 is fully decided by them).
"""
import re
import sys
import types

gate_dir, *patches = sys.argv[1:]
stub = types.ModuleType("code_quality_scope")
stub.PROJECT_SUBMODULES = ("protocol-processor", "gptp-processor")
stub.tracked = lambda *a: []
sys.modules["code_quality_scope"] = stub
sys.path.insert(0, gate_dir)
import check_cpp_idiom as g  # noqa: E402

for p in patches:
    files = {}
    cur = None
    for line in open(p, encoding="utf-8"):
        m = re.match(r"^\+\+\+ b/(.*)$", line)
        if m:
            cur = m.group(1) if m.group(1).endswith(g.SCANNED_SUFFIXES) else None
            if cur:
                files[cur] = []
            continue
        if line.startswith("diff --git"):
            cur = None
        elif cur and line.startswith("+"):
            files[cur].append(line[1:])
    for f, lines in files.items():
        text = "".join(lines)
        c = {k: v for k, v in g.scan(text, f).items() if v and k != "long function"}
        es10 = g.sites(text, "multi-declarator declaration", f)
        print(f"{p.rsplit('/', 1)[-1]} {f}: added lines {len(lines)}, nonzero {c or 'none'}")
        for ln, s in es10:
            print(f"    ES.10 added-line {ln}: {s.strip()}")
