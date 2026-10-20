#!/usr/bin/env python3
"""Assemble the round-2 receipts under <output>/receipts/round2 from the scratch
records. Host paths are replaced by <scratch>, <lane>, <submodule>, <parent> and
the like; files over 200 KB, and every per-arm campaign receipt, are listed
(sha256, size) instead of copied. Round-1 receipts are never touched."""
import hashlib
import re
import shutil
from pathlib import Path

S = Path("<scratch>")
O = Path("<management>/2026-09-23/pp188-a651")
R = O / "receipts" / "round2"
LIMIT = 200 * 1024
KEEP = {"HANDOFF-round1.md", "PR-BODY-round1.md"}
REPL = [
    ("<submodule>", "<submodule>"),
    ("<parent>", "<parent>"),
    ("<scratch>", "<scratch>"),
    ("<lane>", "<lane>"),
    ("<container layers>", "<container layers>"),
    ("<management>", "<management>"),
    ("<vivado install>", "<vivado install>"),
    ("<home>", "<home>"),
    ("<tools>", "<tools>"),
]
external = []


def scrub(text: str) -> str:
    for a, b in REPL:
        text = text.replace(a, b)
    text = re.sub(r"<tmp> "<tmp>", text)
    return text


def put(src: Path, dst: Path) -> None:
    """Copy a scrubbed text record, or list it when too large or not text."""
    data = src.read_bytes()
    rel = scrub(str(src))
    if len(data) > LIMIT:
        external.append((rel, len(data), hashlib.sha256(data).hexdigest()))
        return
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        external.append((rel, len(data), hashlib.sha256(data).hexdigest()))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(scrub(text))


def put_dir(src: Path, dst: Path) -> None:
    """The files directly under one record directory."""
    if not src.exists():
        return
    for p in sorted(src.iterdir()):
        if p.is_file():
            put(p, dst / p.name)


def arms_csv(work: Path, out: Path) -> None:
    """sha256 and size of every per-arm receipt under a campaign work dir."""
    rows = ["record,bytes,sha256"]
    if work.exists():
        for p in sorted(work.rglob("*")):
            if p.is_file():
                data = p.read_bytes()
                rows.append(f"{scrub(str(p))},{len(data)},{hashlib.sha256(data).hexdigest()}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(rows) + "\n")


def main() -> None:
    R.mkdir(parents=True, exist_ok=True)
    for p in R.iterdir():
        if p.name in KEEP:
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    rec = S / "rec2"
    for d, tgt in {"base-gates": "gates/base", "head-gates": "gates/head",
                   "base-camps": "campaigns/base", "head-camps": "campaigns/head",
                   "cons-base": "consumers/base", "cons-head": "consumers/head",
                   "ooc-base": "consumers/ooc-base", "ooc-head": "consumers/ooc-head"}.items():
        put_dir(rec / d, R / tgt)
    arms_csv(rec / "base-camps" / "work", R / "campaign-arms-base.csv")
    arms_csv(rec / "head-camps" / "work", R / "campaign-arms-head.csv")
    # records cut by the host reset, and those taken at superseded heads
    st = rec / "stopped"
    if st.exists():
        for d in sorted(st.iterdir()):
            if d.is_dir():
                put_dir(d, R / "superseded" / d.name)
    # the reviewer verifications at the exact head
    pr = rec / "probes"
    if pr.exists():
        for p in sorted(pr.iterdir()):
            if p.is_file():
                put(p, R / "reviewer-checks" / p.name)
        for sub in ("r665",):
            put_dir(pr / sub, R / "reviewer-checks" / sub)
    # the records outside the gate list: full pp_top at base and head, per-shape lint
    for p in sorted((S / "r2rec").iterdir()):
        if p.is_file():
            put(p, R / "extra" / p.name)
    # the development runs cited (new checks and their controls before the commits)
    dev = S / "r2dev"
    for name in ("acmp-coalesce2.log", "srp-188all.log", "srp-wk12.log", "acmp-sticky.log",
                 "acmp-tdecl.log", "no-record-probe.log", "r666-repro-apply.log", "make-check2.log"):
        if (dev / name).exists():
            put(dev / name, R / "dev" / name)
    for sub in ("acmp-coalesce2", "srp-wk12", "acmp-sticky"):
        put_dir(dev / sub, R / "dev" / sub)
    # comparisons and the scripts that produced the records
    cmp2 = S / "cmp2"
    if cmp2.exists():
        for p in sorted(cmp2.rglob("*")):
            if p.is_file():
                put(p, R / "compare" / p.relative_to(cmp2))
    for p in sorted((S / "scripts" / "r2").iterdir()):
        if p.is_file():
            put(p, R / "scripts" / p.name)
    for name in ("run_gates.sh", "run_camps2.sh", "run_consumers.sh", "run_ooc.sh", "env.sh"):
        put(S / "scripts" / name, R / "scripts" / name)
    lines = ["record,bytes,sha256"] + [f"{r},{n},{h}" for r, n, h in external]
    (R / "EXTERNAL-RECORDS.csv").write_text("\n".join(lines) + "\n")
    print(f"external records: {len(external)}")


if __name__ == "__main__":
    main()
