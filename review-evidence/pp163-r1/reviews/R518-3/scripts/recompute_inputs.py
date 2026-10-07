#!/usr/bin/env python3
"""Independently recompute the pp_resource_gate inputs digest of the #163 final-head OOC record.

Usage:
  recompute_inputs.py --evidence DIR --processor GITDIR --parent GITDIR --gptp GITDIR --axis GITDIR
                      --parent-rev REV --gptp-rev REV --axis-rev REV --processor-rev REV [--processor-rev REV ...]

DIR is review-evidence/pp163-r1 of the evidence branch. The file order, include folders and
generics are taken from the published OOC recipe (ooc-m3final/baseline_ooc.tcl) with the gate's
own regular expressions, NOT from the published component list. Every repository file is hashed
from the git blob at the given revision (no checkout). The four non-repository inputs (the two
VexiiRiscv RAM models, the generated VexiiRiscv core and the normalized generated top) and the
clock constraint are taken from their published copies. Prints one JSON document.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

READS = re.compile(r"^(?:read_verilog(?: -v)?|read_xdc|source) \{?([^{}\s]+)\}?[ \t]*$", re.M)
INCLUDES = re.compile(r" -include_dirs \{([^}]*)\}")
GENERICS = re.compile(r" -generic \{([^}]*)\}")
PARENT = "$VALIDATION_STORAGE/pp163-a553/parent/"


def blob(gitdir, rev, path):
    out = subprocess.run(["git", "-C", gitdir, "cat-file", "blob", f"{rev}:{path}"],
                         capture_output=True, check=False)
    if out.returncode:
        raise SystemExit(f"missing blob {rev}:{path} in {gitdir}: {out.stderr.decode().strip()}")
    return out.stdout


def tree_names(gitdir, rev, folder):
    out = subprocess.run(["git", "-C", gitdir, "ls-tree", "--name-only", f"{rev}:{folder}"],
                         capture_output=True, check=True, text=True)
    return out.stdout.split()


def main():
    ap = argparse.ArgumentParser()
    for name in ("evidence", "processor", "parent", "gptp", "axis", "parent-rev", "gptp-rev", "axis-rev"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--processor-rev", action="append", required=True)
    a = ap.parse_args()
    ev = Path(a.evidence)
    meas = ev / "author-r3/measurement-m3final"
    script = (meas / "ooc-m3final/baseline_ooc.tcl").read_text()
    published = json.loads((meas / "inputs-digest/inputs-components.json").read_text())
    images = json.loads((meas / "ooc-m3final/baseline_images.json").read_text())
    pub_inputs = meas / "inputs-digest/inputs"
    reads = READS.findall(script)
    folders = [f for group in INCLUDES.findall(script) for f in group.split()]
    generics = [re.sub(r'"[^"]*/([^/"]+)"', r'"\1"', g) for g in GENERICS.findall(script)]

    def locate(raw):
        """Map one recipe path to (source kind, repository-relative path)."""
        if raw.startswith(PARENT + "protocol-processor/"):
            return "processor", raw[len(PARENT + "protocol-processor/"):]
        if raw.startswith(PARENT + "gptp-processor/"):
            return "gptp", raw[len(PARENT + "gptp-processor/"):]
        if raw.startswith(PARENT + "third_party/verilog-axis/"):
            return "axis", raw[len(PARENT + "third_party/verilog-axis/"):]
        if raw.startswith(PARENT):
            return "parent", raw[len(PARENT):]
        name = Path(raw).name
        if name == "alinx_ax7101.v":
            return "published-normalized", "alinx_ax7101.normalized.v"
        if name == "clock.xdc" and not raw.startswith("$"):
            return "published-xdc", "ooc-m3final/clock.xdc"
        if (pub_inputs / name).is_file():
            return "published", name
        raise SystemExit(f"unmapped recipe path: {raw}")

    rows = [(raw, *locate(raw)) for raw in reads]
    headers = []
    for folder in folders:
        if not folder.startswith(PARENT):
            raise SystemExit(f"include folder outside the parent: {folder}")
        rel = folder[len(PARENT):]
        for name in sorted(tree_names(a.parent, a.parent_rev, rel)):
            if Path(name).suffix in (".svh", ".vh"):
                headers.append((folder + "/" + name, "parent", rel + "/" + name))
    rows += headers

    result = {"recipe_reads": len(reads), "include_folders": folders, "headers": [h[2] for h in headers],
              "generics": generics, "generics_match_published": generics == published["generics"],
              "per_revision": {}}
    pub_rows = published["files"]
    result["file_count_matches_published"] = len(rows) == len(pub_rows)
    order_ok = all(Path(raw).name == p["name"] for (raw, _k, _r), p in zip(rows, pub_rows))
    result["order_and_names_match_published"] = order_ok and len(rows) == len(pub_rows)

    for prev in a.processor_rev:
        digest = hashlib.sha256()
        components = []
        for (raw, kind, rel), pub in zip(rows, pub_rows):
            if kind == "processor":
                data = blob(a.processor, prev, rel)
            elif kind == "gptp":
                data = blob(a.gptp, a.gptp_rev, rel)
            elif kind == "axis":
                data = blob(a.axis, a.axis_rev, rel)
            elif kind == "parent":
                data = blob(a.parent, a.parent_rev, rel)
            elif kind == "published-xdc":
                data = (meas / rel).read_bytes()
            else:
                data = (pub_inputs / rel).read_bytes()
            comp = hashlib.sha256(data).hexdigest()
            digest.update(Path(raw).name.encode() + b"\0" + bytes.fromhex(comp))
            components.append({"order": len(components) + 1, "name": Path(raw).name, "source": kind,
                               "path": rel, "sha256": comp, "published": pub["component_sha256"],
                               "equal": comp == pub["component_sha256"]})
        for g in generics:
            digest.update(g.encode() + b"\0")
        for im in sorted(images, key=lambda r: Path(r["path"]).name):
            digest.update(f"{Path(im['path']).name}\0{im['sha256']}\0".encode())
        result["per_revision"][prev] = {
            "inputs_sha256": digest.hexdigest(),
            "components_differing_from_published_c4539ff_list": [c for c in components if not c["equal"]],
            "components": components}
    json.dump(result, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
