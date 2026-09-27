#!/usr/bin/env python3
"""Compare the committed 50 MHz input manifest with a reviewer's independent exports.

usage: verify_inputs.py MANIFEST.json REPO CPU_PACKAGE_ROOT WORK_DEFAULT WORK_ATTRIBUTION [variant...]

Every source_inputs and images record is rehashed from the reviewer's own tree.
Records under root "work" are mapped by their leading variant directory; the
reviewer's generated files differ only where they embed the absolute build root,
so those are reported separately and additionally compared after normalization.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path


def sha(path: Path) -> tuple[int, str]:
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def normalize(text: str, roots: list[str]) -> str:
    for root in roots:
        text = text.replace(root, "$BUILD")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//[^\n]*", "", text)
    return text


def main() -> int:
    manifest, repo, cpu, work_default, work_attr, *variants = sys.argv[1:]
    variants = variants or ["default", "attribution"]
    doc = json.loads(Path(manifest).read_text())
    repo = Path(repo)
    roots = {"repository": repo, "protocol_processor": repo / "protocol-processor",
             "gptp_processor": repo / "gptp-processor",
             "axis_library": repo / "third_party/verilog-axis",
             "cpu_package": Path(cpu)}
    works = {"default": Path(work_default), "attribution": Path(work_attr)}
    bad = 0
    for variant in variants:
        m = doc["measurements"][variant]
        counts = {"match": 0, "work_differs": 0, "mismatch": 0}
        for kind in ("source_inputs", "images"):
            for rec in m[kind]:
                if rec["root"] == "work":
                    head, rest = rec["path"].split("/", 1)
                    path = works[head] / rest
                else:
                    path = roots[rec["root"]] / rec["path"]
                if not path.exists():
                    print(f"MISSING {variant} {kind} {rec['root']}:{rec['path']}")
                    counts["mismatch"] += 1
                    continue
                size, digest = sha(path)
                if (size, digest) == (rec["bytes"], rec["sha256"]):
                    counts["match"] += 1
                elif rec["root"] == "work":
                    counts["work_differs"] += 1
                    print(f"WORK-DIFFERS {variant} {kind} {rec['path']} "
                          f"committed={rec['bytes']}/{rec['sha256'][:12]} "
                          f"reviewer={size}/{digest[:12]}")
                else:
                    counts["mismatch"] += 1
                    print(f"MISMATCH {variant} {kind} {rec['root']}:{rec['path']} "
                          f"committed={rec['bytes']}/{rec['sha256'][:12]} "
                          f"reviewer={size}/{digest[:12]}")
        print(f"SUMMARY {variant} records={sum(counts.values())} {counts}")
        bad += counts["mismatch"]
    # Normalized generated-Verilog comparison across the reviewer's two exports.
    texts = {}
    for variant, work in works.items():
        v = work / "ax8x8/gateware/alinx_ax7101.v"
        if v.exists():
            extra = [r for r in os.environ.get("NORMALIZE_ROOTS", "").split(":") if r]
            texts[variant] = normalize(v.read_text(),
                                       [str(w) for w in works.values()] + extra)
    for variant, text in texts.items():
        print(f"NORMALIZED {variant} sha256={hashlib.sha256(text.encode()).hexdigest()}")
    if len(texts) == 2:
        print(f"NORMALIZED-EQUAL {texts['default'] == texts['attribution']}")
    print(f"COMMITTED normalized_verilog_sha256={doc['export_comparison']['normalized_verilog_sha256']}"
          f" equal={doc['export_comparison']['equal']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
