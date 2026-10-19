#!/usr/bin/env python3
"""Assemble the receipts under the output directory from the scratch records.
Host paths are replaced by <scratch>, <lane> and <processor> names; files over
200 KB are listed (sha256, size) instead of copied."""
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

S = Path("<scratch>")
O = Path("<home>/milan-fpga-management/2026-09-23/pp188-a651")
R = O / "receipts"
LIMIT = 200 * 1024
REPL = [
    ("<submodule>", "<submodule>"),
    ("<parent>", "<parent>"),
    ("<scratch>", "<scratch>"),
    ("<lane>", "<lane>"),
    ("<container layers>", "<container layers>"),
    ("<vivado install>", "<vivado install>"),
    ("<home>", "<home>"),
    ("<tools>", "<tools>"),
]


def scrub(text: str) -> str:
    for a, b in REPL:
        text = text.replace(a, b)
    text = re.sub(r"<tmp> "<tmp>", text)
    return text


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


external = []


def put(src: Path, dst: Path) -> None:
    """Copy a scrubbed text record, or list it when it is too large."""
    data = src.read_bytes()
    rel = scrub(str(src))
    if len(data) > LIMIT:
        external.append((rel, len(data), hashlib.sha256(data).hexdigest()))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        dst.write_text(scrub(data.decode("utf-8")))
    except UnicodeDecodeError:
        external.append((rel, len(data), hashlib.sha256(data).hexdigest()))


def main() -> None:
    if R.exists():
        for p in R.iterdir():
            if p.name in ("toolchain.txt",):
                continue
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
    R.mkdir(parents=True, exist_ok=True)
    # gate, campaign and consumer top-level records
    sets = {
        "base-gates": "gates/base", "head-gates": "gates/head",
        "base-camps": "campaigns/base", "head-camps3": "campaigns/head",
        "head-camps": "campaigns/head-bacfb90", "cons-base": "consumers/base",
        "cons-head": "consumers/head", "ooc-base": "consumers/ooc-base",
        "ooc-head": "consumers/ooc-head",
        "head-gates-bacfb90": "superseded/gates-bacfb90",
        "head-gates-ea5226c": "superseded/gates-ea5226c",
        "head-gates-2176035": "superseded/gates-2176035",
        "head-camps2": "superseded/campaign-acmp-2176035",
    }
    for d, tgt in sets.items():
        src = S / "rec" / d
        if not src.exists():
            continue
        for p in sorted(src.iterdir()):
            if p.is_file():
                put(p, R / tgt / p.name)
    # every per-arm campaign receipt (the files directly under each
    # campaign's output directory) is listed (sha256, size), not copied
    arms = {"base-camps": ("campaign-arms-base.csv", None),
            "head-camps3": ("campaign-arms-head.csv", None),
            "head-camps": ("campaign-arms-head-bacfb90.csv", ("srp_top", "srp_admission"))}
    for d, (name, only) in arms.items():
        rows = ["record,bytes,sha256"]
        for c in sorted((S / "rec" / d / "work").iterdir()):
            if only and c.name not in only:
                continue
            for p in sorted(c.iterdir()):
                if p.is_file():
                    data = p.read_bytes()
                    rows.append(f"{scrub(str(p))},{len(data)},{hashlib.sha256(data).hexdigest()}")
        (R / name).write_text("\n".join(rows) + "\n")
    # comparison outputs
    for p in sorted((S / "cmp").rglob("*")):
        if p.is_file():
            put(p, R / "compare" / p.relative_to(S / "cmp"))
    # the scripts that produced the records
    for p in sorted((S / "scripts").iterdir()):
        if p.is_file():
            put(p, R / "scripts" / p.name)
    lines = ["record,bytes,sha256"] + [f"{r},{n},{h}" for r, n, h in external]
    (R / "EXTERNAL-RECORDS.csv").write_text("\n".join(lines) + "\n")
    print(f"external records: {len(external)}")


if __name__ == "__main__":
    main()
