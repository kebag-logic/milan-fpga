#!/usr/bin/env python3
"""Copy this round's logs into the receipts with host paths replaced, keep a log
over 190 KB as its digest, size and tail, and index the files present.
Usage: collect_receipts.py <receipts> <head>"""
import hashlib
import re
import shutil
import sys
from pathlib import Path

receipts, head = Path(sys.argv[1]), sys.argv[2]
S = Path("$VALIDATION_STORAGE/797-a711g")
SOURCES = {
    "gates": S / "gates/run3/logs",
    "lane": S / "aux3/logs",
    "plants": S / "plants/logs",
}
FILES = {
    "gates/memory.txt": S / "gates/run3/memory.txt",
    "gates/memory_max_5s.txt": S / "gates/run3/memory_max_5s.txt",
    "earlier_run_c73cecf1/verify_docs_yml.txt": S / "gates/run2/logs/verify_docs_yml.txt",
    "earlier_run_c73cecf1/verify_docs_yml.rc": S / "gates/run2/logs/verify_docs_yml.rc",
    "earlier_run_c73cecf1/memory.txt": S / "gates/run2/memory.txt",
    "earlier_run_c73cecf1/docs-gates-2__gate_41.log": S / "gates/run2/logs/docs-gates-2__gate_41.log",
    "export/head_csr.csv": S / "aux/export/out/csr.csv",
    "export/head_aem_desc.json": S / "aux/export/out/aem_desc.json",
    "export/parent_csr.csv": S / "parent/out/csr.csv",
    "export/parent_aem_desc.json": S / "parent/out/aem_desc.json",
    "export/parent_soc_from_check.log": S / "parent/soc_from_check_parent.log",
    "export/parent_soc_from_check.rc": S / "parent/soc_from_check_parent.rc",
    "export/head_soc_write_probe.log": S / "aux/logs/soc_write_probe.log",
    "export/merge_soc_from_check.log": S / "aux/logs/soc_from_check.log",
    "export/merge_soc_from_check.rc": S / "aux/logs/soc_from_check.rc",
    "export/sdk_install.log": S / "gates/sdk_install.log",
}
LIMIT = 190_000
PATHS = (
    (r"$VALIDATION_STORAGE/797-a711g/gates/run[23]/[a-z0-9-]+/wt", "<clone>"),
    (r"$VALIDATION_STORAGE/797-a711g/aux[23]?/wt", "<clean-clone>"),
    (r"$VALIDATION_STORAGE/797-a711g/parent/wt", "<parent-clone>"),
    (r"$VALIDATION_STORAGE/797-a711g/gates/venv", "<venv>"),
    (r"$VALIDATION_STORAGE/797-a711g/gates/home", "<scratch-home>"),
    (r"$VALIDATION_STORAGE/797-a711g/[A-Za-z0-9_./-]*", "<scratch>"),
    (r"$VALIDATION_TOOLS/pinned-verilator-5.050", "<pinned-verilator>"),
    (r"$VALIDATION_TOOLS/sv2v-v0.0.12", "<sv2v>"),
    (r"$VALIDATION_STORAGE/scratch/a662/make43/bin", "<make>"),
    (r"$LANES/797-r1-regref", "<lane>"),
    (r"$HOME/litex-milan/venv", "<litex-venv>"),
    (r"$HOME/milan-fpga-management/tools/tsn-gen-deca300c", "<tsn-gen>"),
    (r"$HOME", "<home>"),
)


def clean(text: str) -> str:
    """The text with every host path replaced by its placeholder."""
    for pattern, placeholder in PATHS:
        text = re.sub(pattern, placeholder, text)
    return text


def put(source: Path, target: Path) -> None:
    """Copy one file, cleaned; a large one is kept as digest, size and tail."""
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    text = clean(raw.decode("utf-8", "replace"))
    if len(raw) > LIMIT:
        tail = "\n".join(text.splitlines()[-60:])
        target.with_name(target.name + ".tail").write_text(
            f"sha256 {hashlib.sha256(raw).hexdigest()} size {len(raw)}; the whole log stays out of the packet.\n{tail}\n")
    else:
        target.write_text(text)


for name, directory in SOURCES.items():
    if (receipts / name).exists():
        shutil.rmtree(receipts / name)
    for source in sorted(directory.iterdir()):
        if source.is_file():
            put(source, receipts / name / source.name)
for rel, source in FILES.items():
    put(source, receipts / rel)
(receipts / "HEAD.txt").write_text(f"{head}\n")
rows = ["# Receipts", "", f"Head `{head}`. Generated from the files present.", "",
        "| File | Bytes | sha256 |", "|---|---:|---|"]
for path in sorted(receipts.rglob("*")):
    if path.is_file() and path.name != "INDEX.md":
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(receipts).as_posix()}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |")
(receipts / "INDEX.md").write_text("\n".join(rows) + "\n")
print(f"{len(rows) - 6} files indexed")
