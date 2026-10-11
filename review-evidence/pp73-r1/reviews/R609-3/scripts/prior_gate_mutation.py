#!/usr/bin/env python3
"""Reviewer probe (R608-2): does the AECP gate's self-test notice when one of
its finding or refusal sites is disabled?

For each line of scripts/aecp_gate/{inputs,table,rtl,rom,record,doc,gate}.py
that opens a finding (`<x>.append(`) or a refusal (`raise GateError(`), a copy
of the tree gets that one site disabled (the append becomes a no-op call; the
raise becomes a bare construction), and `check_aecp_commands.py --selftest` is
run on the copy. A site whose disabling leaves the self-test green is a
SURVIVOR: no plant needs that site.

usage: python3 -I gate_mutation.py --src DIR --out DIR [--jobs N]
"""
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MODS = ("inputs", "table", "rtl", "rom", "record", "doc", "gate")
SITE = re.compile(r"\b(?:ck\.p|p|out|lines)\.append\(|raise GateError\(")


def sites(src: Path) -> list:
    out = []
    for m in MODS:
        rel = f"scripts/aecp_gate/{m}.py"
        for i, line in enumerate((src / rel).read_text().splitlines()):
            if SITE.search(line) and not line.lstrip().startswith("#"):
                if ".append(" in line and "GateError" not in line:
                    # only appends that build gate output text
                    if not re.search(r"\.append\(f?[\"']", line) and "append(f" not in line:
                        continue
                out.append((rel, i))
    return out


def one(args) -> dict:
    src, rel, i = args
    with tempfile.TemporaryDirectory(prefix="r608-2-gmut-") as tmp:
        root = Path(tmp)
        for d in ("hdl", "scripts", "tb/common", "tb/aecp_cmds", "docs"):
            shutil.copytree(src / d, root / d, ignore=shutil.ignore_patterns(
                "obj_dir", "*.hex", "image.bin", "__pycache__"))
        p = root / rel
        lines = p.read_text().splitlines(keepends=True)
        orig = lines[i]
        if "raise GateError(" in orig:
            new = orig.replace("raise GateError(", "GateError(", 1)
        else:
            new = re.sub(r"\b(?:ck\.p|p|out|lines)\.append\(", "(lambda *_: None)(", orig, count=1)
        lines[i] = new
        p.write_text("".join(lines))
        r = subprocess.run(["python3", "-B", "scripts/check_aecp_commands.py", "--selftest"],
                           cwd=root, capture_output=True, text=True, timeout=300)
    tail = [x for x in (r.stdout + r.stderr).splitlines() if x.strip()][-2:]
    return {"site": f"{rel}:{i + 1}", "line": orig.strip()[:120], "selftest_rc": r.returncode,
            "survivor": r.returncode == 0, "tail": tail}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=12)
    a = ap.parse_args()
    src = a.src.resolve()
    todo = [(src, rel, i) for rel, i in sites(src)]
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, todo))
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "gate-mutation.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
    surv = [r for r in res if r["survivor"]]
    summary = [f"sites disabled: {len(res)}; self-test failed (site needed): "
               f"{len(res) - len(surv)}; survivors: {len(surv)}"]
    summary += [f"SURVIVOR {r['site']}: {r['line']}" for r in surv]
    (a.out / "gate-mutation.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
