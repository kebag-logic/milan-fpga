#!/usr/bin/env python3
"""The map table's compile-time bound (aecp_maps.c, #894 round 10, item 1) at every configuration and both wider
key geometries, for the tree's own source and for planted undersized tables.

usage: probe_table_assert.py TREE SCRATCH
Copies TREE/sw/firmware/ctrl to SCRATCH/ctrl-<variant>, plants the variant, and compiles aecp_maps.c with the
arms' C flags (ctrl_build.C_FLAGS, -fsyntax-only) against each configuration's generated header: the five
checked-in ones and aecp_arms.KEY_GEOMETRIES. Prints one line a variant and configuration: its compile rc and the
static assertion it fails, if any, then each configuration's domain (MAP_FIRSTS x MAP_CHANNELS). TREE is never
written. Variants:
  tree                 the source as committed
  each-direction       MAP_SLOTS the larger of the two directions' own products (the campaign's row)
  floor-only           MAP_SLOTS the 256-slot floor alone
  array-at-floor       the slot array declared at the floor, MAP_SLOTS unchanged
  each-direction+r9    each-direction with round 9's assertion in place of the tree's (the check's own mutant)
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
from ctrl_build import C_FLAGS, STACK, STACK_INCLUDE, HARNESS  # noqa: E402

SLOTS = "#define MAP_SLOTS MAP_MOST(MAP_DOMAIN, MAP_FLOOR)\n"
EACH = ("#define MAP_SLOTS MAP_MOST(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS, "
        "AECP_ENTITY_KEY_CLUSTERS * AECP_ENTITY_KEY_CLUSTER_CHANNELS)\n")
ASSERT = ("_Static_assert(sizeof ((struct edit *)0)->slot / sizeof ((struct edit *)0)->slot[0] >= (size_t)MAP_DOMAIN,\n"
          "\t       \"the table holds every position place() forms\");\n")
R9 = ("_Static_assert(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS <= MAP_SLOTS &&\n"
      "\t       AECP_ENTITY_KEY_CLUSTERS * AECP_ENTITY_KEY_CLUSTER_CHANNELS <= MAP_SLOTS,\n"
      "\t       \"the table holds every key of the port's domain\");\n")
VARIANTS = {
    "tree": [],
    "each-direction": [(SLOTS, EACH)],
    "floor-only": [(SLOTS, "#define MAP_SLOTS MAP_FLOOR\n")],
    "array-at-floor": [("\tuint8_t slot[MAP_SLOTS];", "\tuint8_t slot[MAP_FLOOR];")],
    "each-direction+r9": [(SLOTS, EACH), (ASSERT, R9)],
}
configs = sorted((tree / "configs").glob("endstation_*.yaml"))
configs += [aecp_arms.key_geometry(scratch / "geometries", *shape) for shape in aecp_arms.KEY_GEOMETRIES]
headers = {}
for config in configs:
    gen = scratch / f"gen-{config.stem}"
    gen.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-B", str(tree / "sw/firmware/ctrl/aecp/aecp_entity.py"), str(config),
                    "-o", str(gen / "aecp_entity_gen.h")], check=True)
    text = (gen / "aecp_entity_gen.h").read_text()
    keys = {k: int(v) for k, v in re.findall(r"#define AECP_ENTITY_KEY_(\w+) (\d+)u", text)}
    firsts = max(keys["STREAMS"], keys["CLUSTERS"])
    channels = max(keys["STREAM_CHANNELS"], keys["CLUSTER_CHANNELS"])
    each = max(keys["STREAMS"] * keys["STREAM_CHANNELS"], keys["CLUSTERS"] * keys["CLUSTER_CHANNELS"])
    headers[config.stem] = (gen, f"domain {firsts} x {channels} = {firsts * channels}, each direction's {each}")
stack = STACK.resolve()
for name, edits in VARIANTS.items():
    src = scratch / f"ctrl-{name}"
    if src.exists():
        shutil.rmtree(src)
    shutil.copytree(tree / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__"))
    path = src / "aecp/aecp_maps.c"
    text = path.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    path.write_text(text)
    for stem, (gen, _) in headers.items():
        r = subprocess.run(["gcc", *C_FLAGS, "-fsyntax-only", f"-I{src / 'aecp'}", f"-I{stack / STACK_INCLUDE}",
                            f"-I{HARNESS}", f"-I{gen}", f"-I{src / 'test'}", str(path)],
                           capture_output=True, text=True)
        failed = [line.split("error: ")[-1] for line in r.stderr.splitlines() if "static assertion failed" in line]
        other = [line for line in r.stderr.splitlines() if "error:" in line and "static assertion" not in line]
        print(f"{name} {stem}: compile rc {r.returncode}" + (f" {failed[0]}" if failed else "") +
              (f" OTHER {other[0]}" if other else ""), flush=True)
for stem, (_, domain) in headers.items():
    print(f"# {stem}: {domain}")
