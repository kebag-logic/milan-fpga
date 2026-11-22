#!/usr/bin/env python3
"""pack.py OUT HEAD REBUILT: assemble round 2's identity packet (receipts/identity) from the scratch operands: the shipping
image pairs, the checkpoint dumps (xz), the 16 CPU-budget image pairs, the 13 groups' results and raw logs (gzip),
the sanitised tools, binding.json and the rebuild receipts. MANIFEST.sha256 is written by seal.py afterwards."""
import gzip
import hashlib
import json
import lzma
import shutil
import sys
from pathlib import Path

OUT, HEAD, REBUILT = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
S = Path("<scratch>")
T = Path("<train-scratch>")
MEAS = {"1x1": T / "r6meas/8c5e2b4f0a487690cf0168f08b55e7f7be91a09c/1x1",
        "8x8-1if": T / "r6meas/92de01f756299c7d83bd6945dbf62d4b311a683e/8x8-1if"}
ARMS = ("none", "answering-every-port", "answering-ports", "answering-later", "declaring-outputs", "shutdown-entry",
        "talker-notices", "valid-destinations")
STEM = {"1x1": "endstation_ax7101_1x1_tdm8", "8x8": "endstation_ax7101_8x8"}
SIDES = {"bench": (T / "gate15/work/g{p}", T / "gate15/clones/g{p}"),
         "flip": (S / "gate/work/flip-{p}", S / "gate/clones/flip-{p}")}
EXPORT = ("aem_desc.bin", "aem_desc.json", "aem_desc.map", "csr.csv", "csr.json", "flashboot_layout.json",
          "image_manifest.json")
SANITISE = ((str(T), "<train-scratch>"), (str(S), "<scratch>"), ("<lane>", "<lane>"),
            ("<home>", "<home>"), ("<host-tools>", "<host-tools>"),
            ("<host-tmp>", "<host-tmp>"), ("<host-data>", "<host-data>"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(src, rel, mode="copy"):
    dst = OUT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = Path(src).read_bytes()
    if mode == "xz":
        dst = dst.with_name(dst.name + ".xz")
        dst.write_bytes(lzma.compress(data, preset=9))
    elif mode == "gz":
        dst = dst.with_name(dst.name + ".gz")
        dst.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    elif mode == "text":
        text = data.decode()
        for old, new in SANITISE:
            text = text.replace(old, new)
        dst.write_text(text)
    else:
        dst.write_bytes(data)
    return dst


if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
binding = {"operands": [], "rebuilds": []}

# shipping pairs
for p in ("1x1", "8x8"):
    for side, (work, clone) in SIDES.items():
        w = Path(str(work).format(p=p)) / "build_ExtraPostPlacementOpt"
        c = Path(str(clone).format(p=p))
        base = f"shipping/{p}/{side}"
        put(w / "gateware/alinx_ax7101.bit", f"{base}/alinx_ax7101.bit")
        put(c / f"sw/builder/out/{STEM[p]}/ctrl_app.elf", f"{base}/ctrl_app.elf")
        for name in EXPORT:
            put(w / name, f"{base}/{name}")
        for f in sorted((w / "gateware").glob("alinx_ax7101_rom_bank*.init")) + [w / "gateware/alinx_ax7101_mem.init"]:
            put(f, f"{base}/gateware/{f.name}")
        argv = Path(str(work).format(p=p)) / "argv.txt"
        if argv.is_file():
            put(argv, f"{base}/argv.txt", "text")
published = json.loads((S / "bin/published.json").read_text())
binding["checkpoints"] = [
    {"shape": p, "side": side, "file": "alinx_ax7101_route.dcp", "bytes": dcp.stat().st_size, "sha256": sha(dcp),
     "note": "the routed checkpoint tools/dump.tcl read; not published here (over the size limit)"}
    for p in ("1x1", "8x8") for side, (work, _clone) in SIDES.items()
    for dcp in [Path(str(work).format(p=p)) / "build_ExtraPostPlacementOpt/gateware/alinx_ax7101_route.dcp"]]
binding["operands"] += published["operands"]

# dumps
for p, d in (("1x1", S / "vdump/1x1"), ("8x8", S / "vdump/r2-8x8")):
    for side in ("bench", "flip"):
        for kind in ("cells", "nets"):
            if (d / f"{side}.{kind}").is_file():
                put(d / f"{side}.{kind}", f"shipping/{p}/dump/{side}.{kind}", "xz")
        if (d / f"{side}.summary").is_file():
            put(d / f"{side}.summary", f"shipping/{p}/dump/{side}.summary")
for p, d in (("1x1", S / "vdump/r2-1x1"), ("8x8", S / "vdump/8x8")):
    for side in ("bench", "flip"):
        if (d / f"{side}.bram").is_file():
            put(d / f"{side}.bram", f"shipping/{p}/dump/{side}.bram", "xz")

# harness pairs and the 13 groups
for point, measured in MEAS.items():
    for arm in ARMS:
        base = f"harness/{point}/{arm}"
        put(measured / arm / "image/ctrl_app.elf", f"{base}/measured.elf")
        put(S / "meas" / point / arm / "image/ctrl_app.elf", f"{base}/head.elf")
        put(measured / arm / "parts.json", f"{base}/measured.parts.json")
        put(S / "meas" / point / arm / "parts.json", f"{base}/head.parts.json")
        for label, tree, rel in (("bench head 8c5e2b4f", S / "meas-bench", "measured.elf"),
                                 (f"this head {HEAD}", S / REBUILT, "head.elf")):
            binding["rebuilds"].append({"operand": f"{base}/{rel}", "head": label,
                                        "sha256": sha(tree / point / arm / "image/ctrl_app.elf"),
                                        "why": "the harness build (legs.py build) rerun at that head in a clean clone"})
        parts = json.loads((measured / arm / "parts.json").read_text())["parts"]
        for mine in sorted((S / "meas" / point / arm / "subset").glob("*.json")):
            if mine.name == "results.json":
                continue
            k = next(i for i, part in enumerate(parts) if mine.stem in part["groups"])
            theirs = measured / arm / f"part{k}"
            g = f"groups/{point}/{arm}/{mine.stem}"
            put(theirs / mine.name, f"{g}.measured.json")
            put(mine, f"{g}.head.json")
            put(theirs / f"{mine.stem}.log.gz", f"{g}.measured.log.gz")
            put(mine.with_suffix(".log"), f"{g}.head.log", "gz")
            binding.setdefault("groups", []).append({"group": g, "measured_part": f"part{k}"})

# tools (sanitised) and receipts
for name in ("replay.py", "bitheader.py", "bitdiff.py", "elfdiff.py", "bramdiff.py", "hcompare.py", "hcompare2.py",
             "hsubset.sh", "hbuild.sh", "hbuild2.sh", "dump.tcl", "bramdump.tcl", "vdump.sh", "vdump2.sh",
             "bramdump.sh", "compare_inputs.py", "carry2.sh", "pack.py", "seal.py", "rmutants.py"):
    put(S / "bin" / name, f"tools/{name}", "text")
put(S / "tools/legs.py", "tools/legs.py", "text")
for name in ("carry.sh", "gprep.sh", "gbuild.sh", "gchain.sh"):
    put(S / "gate/tools" / name, f"tools/{name}", "text")
for p, H in (("1x1", HEAD[:10]), ("8x8", HEAD[:10])):
    put(S / f"logs2/inputs-carry-{p}-{H}.txt", f"receipts/inputs-carry-{p}-{H}.txt", "text")
for point in MEAS:
    put(S / "meas-bench" / point / "hashes.txt", f"receipts/harness-rebuild-8c5e2b4f-{point}.txt", "text")
    put(S / REBUILT / point / "hashes.txt", f"receipts/harness-rebuild-{HEAD[:10]}-{point}.txt", "text")
for f in sorted((S / "logs2").glob("harness-*.txt")):
    put(f, f"receipts/{f.name}", "text")
put(S / "bin/identity-README.md", "README.md", "text")
(OUT / "binding.json").write_text(json.dumps(binding, indent=1) + "\n")
big = [(p, p.stat().st_size) for p in OUT.rglob("*") if p.is_file() and p.stat().st_size > 20 * 2 ** 20]
total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
print(f"packed {sum(1 for p in OUT.rglob('*') if p.is_file())} files, {total:,} B; over 20 MiB: {big}")
