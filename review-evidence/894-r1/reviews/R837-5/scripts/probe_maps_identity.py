#!/usr/bin/env python3
"""Independent probe of aecp_maps.c between two commits (#894 round 10, item 1).

usage: python3 -I probe_maps_identity.py REPO BASE HEAD SCRATCH
For every checked-in endstation_*.yaml configuration and both wider key geometries (aecp_arms.KEY_GEOMETRIES):
  1. the preprocessed translation (gcc -E -P, the arms' C flags) of BASE's and HEAD's aecp_maps.c, compared after
     dropping each _Static_assert declaration, whitespace and parentheses (MAP_DOMAIN parenthesizes the product):
     equal means the change is assertions and macro grouping;
  2. host objects (gcc -c, the arms' C flags, no debug info) of both, compared byte for byte;
  3. HEAD's file with each planted table: the campaign's row (each direction's own product), the floor alone,
     and the row with BASE's assertion restored; compile rc and the static assertion that fires.
REPO is read through `git show` only and never written."""
import re, shutil, subprocess, sys
from pathlib import Path
repo, base, head, scratch = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
from ctrl_build import C_FLAGS, STACK, STACK_INCLUDE, HARNESS  # noqa: E402
SRC = "sw/firmware/ctrl/aecp/aecp_maps.c"
def show(rev): return subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{SRC}"], check=True, capture_output=True, text=True).stdout
texts = {"base": show(base), "head": show(head)}
SLOTS = "#define MAP_SLOTS MAP_MOST(MAP_DOMAIN, MAP_FLOOR)"
EACH = ("#define MAP_SLOTS MAP_MOST(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS, "
        "AECP_ENTITY_KEY_CLUSTERS * AECP_ENTITY_KEY_CLUSTER_CHANNELS)")
new_assert = re.search(r"_Static_assert\(sizeof \(\(struct edit \*\)0\)->slot.*?;\n", texts["head"], re.S)[0]
old_assert = re.search(r"_Static_assert\(AECP_ENTITY_KEY_STREAMS \*.*?;\n", texts["base"], re.S)[0]
assert texts["head"].count(SLOTS) == 1
texts["plant-each-direction"] = texts["head"].replace(SLOTS, EACH)
texts["plant-floor-only"] = texts["head"].replace(SLOTS, "#define MAP_SLOTS MAP_FLOOR")
texts["plant-each-direction+base-assert"] = texts["plant-each-direction"].replace(new_assert, old_assert)
work = scratch / "maps-probe"; shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
src_dir = repo / "sw/firmware/ctrl"
configs = sorted((repo / "configs").glob("endstation_*.yaml"))
configs += [aecp_arms.key_geometry(work / "geometries", *shape) for shape in aecp_arms.KEY_GEOMETRIES]
def strip(t): return re.sub(r"[\s()]+", "", re.sub(r"_Static_assert\s*\((?:[^;]|\n)*?\)\s*;", "", t))
bad = 0
for config in configs:
    gen = work / f"gen-{config.stem}"; gen.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-B", str(src_dir / "aecp/aecp_entity.py"), str(config), "-o", str(gen / "aecp_entity_gen.h")], check=True, capture_output=True)
    keys = {k: int(v) for k, v in re.findall(r"#define AECP_ENTITY_KEY_(\w+) (\d+)u", (gen / "aecp_entity_gen.h").read_text())}
    dom = max(keys["STREAMS"], keys["CLUSTERS"]) * max(keys["STREAM_CHANNELS"], keys["CLUSTER_CHANNELS"])
    each = max(keys["STREAMS"] * keys["STREAM_CHANNELS"], keys["CLUSTERS"] * keys["CLUSTER_CHANNELS"])
    inc = [f"-I{src_dir / 'aecp'}", f"-I{STACK.resolve() / STACK_INCLUDE}", f"-I{HARNESS}", f"-I{gen}", f"-I{src_dir / 'test'}"]
    out = {}
    for name, text in texts.items():
        c = work / config.stem / name / "aecp_maps.c"; c.parent.mkdir(parents=True, exist_ok=True); c.write_text(text)
        r = subprocess.run(["gcc", *C_FLAGS, "-g0", *inc, "-c", str(c), "-o", str(c.with_suffix(".o"))], capture_output=True, text=True)
        fired = [l.split("error: ")[-1] for l in r.stderr.splitlines() if "static assertion failed" in l]
        out[name] = (r.returncode, fired)
        if name in ("base", "head"):
            e = subprocess.run(["gcc", *C_FLAGS, *inc, "-E", "-P", str(c)], capture_output=True, text=True, check=True).stdout
            (c.parent / "pp.txt").write_text(e)
    pp_equal = strip((work / config.stem / "base/pp.txt").read_text()) == strip((work / config.stem / "head/pp.txt").read_text())
    obj_equal = out["base"][0] == out["head"][0] == 0 and (work / config.stem / "base/aecp_maps.o").read_bytes() == (work / config.stem / "head/aecp_maps.o").read_bytes()
    print(f"{config.stem}: domain {dom}, each direction's {each}; base rc {out['base'][0]}, head rc {out['head'][0]}; "
          f"preprocessed equal but assertions and grouping {pp_equal}; host objects equal {obj_equal}")
    for name in ("plant-each-direction", "plant-floor-only", "plant-each-direction+base-assert"):
        rc, fired = out[name]
        print(f"  {name}: rc {rc}" + (f" {fired[0]}" if fired else ""))
    # expectations: committed code identical and compiling; a planted table fires exactly where it is under the domain
    want_each = 1 if each < dom else 0
    want_floor = 1 if 256 < dom else 0
    bad += not (pp_equal and obj_equal and out["plant-each-direction"][0] == want_each and
                out["plant-floor-only"][0] == want_floor and out["plant-each-direction+base-assert"][0] == 0)
print(f"RESULT {'PASS' if bad == 0 else 'FAIL'} ({bad} configurations off expectation)")
sys.exit(1 if bad else 0)
