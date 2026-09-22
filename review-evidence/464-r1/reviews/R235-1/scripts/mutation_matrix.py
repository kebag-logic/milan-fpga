#!/usr/bin/env python3
"""R235 independent mutation controls for the #464 AEM store self-test.

Each mutant is one or more EXACT textual edits applied to a minimal copy of
the head tree (avdecc/ + hdl/common/csr/milan_csr.sv, the only files the
self-test reads). Every edit must match its `old` text exactly `count` times
or the mutant is reported INVALID (an edit that finds nothing proves nothing).
The self-test then runs under each interpreter; a mutant is DETECTED when the
run exits non-zero. Expectation per mutant:
  caught      - the self-test must exit non-zero (loss of a claimed bound)
  control     - the self-test must still pass (edit is behaviour-neutral for
                the pristine tree: removing a check that nothing currently
                trips)
  undetected  - deliberately weakened self-test + defect that the weakening
                lets through; must PASS, which demonstrates the removed piece
                is load-bearing
  observe     - no expectation; recorded to characterise sensitivity
Usage: mutation_matrix.py <head-extract> <work-root> <receipt-dir>
"""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, WORK, OUT = (Path(a) for a in sys.argv[1:4])
PYS = ["/usr/bin/python3.14", str(Path.home() / ".local/bin/python3.12")]
MAPS, GEN, ASM, SPECS, DESC = ("avdecc/aem_maps.py", "avdecc/gen_aem_store.py",
                               "avdecc/aem_assemble.py", "avdecc/aem_specs.py",
                               "avdecc/aem_descriptors.py")

# (id, description, expectation, [(file, old, new, count), ...])
E = lambda f, o, n, c=1: (f, o, n, c)  # noqa: E731
M = [
    ("P00", "pristine minimal tree (harness control)", "control", []),
    # --- production AUDIO_MAP bounds (aem_maps.py) ---
    ("M01", "Table 7-33 cluster_offset bound removed", "caught",
     [E(MAPS, 'if co >= port["clusters"]:', "if False:")]),
    ("M02", "cluster_offset bound off-by-one loosened (>= -> >)", "caught",
     [E(MAPS, 'if co >= port["clusters"]:', 'if co > port["clusters"]:')]),
    ("M03", "7.2.16 cluster_channel bound removed", "caught",
     [E(MAPS, "if cc >= SMAP_CLUSTER_CHANNELS:", "if False:")]),
    ("M04", "7.2.13 stream_index bound removed", "caught",
     [E(MAPS, "if si >= side.n_streams:", "if False:")]),
    ("M05", "CRF no-channel refusal removed", "caught",
     [E(MAPS, "    if not chans:\n", "    if False:\n")]),
    ("M06", "7.2.19 INPUT duplicate rule removed", "caught",
     [E(MAPS, "if (co, cc) in seen:", "if False:")]),
    ("M07", "7.2.19 OUTPUT duplicate rule removed", "caught",
     [E(MAPS, "if (si, sc) in cfg_stream_ch:", "if False:")]),
    ("M08", "7.2.13 number_of_maps bound removed", "caught",
     [E(MAPS, 'if port["maps"] != 1:', "if False:")]),
    ("M09", "7.2.13 base_map bound removed", "caught",
     [E(MAPS, "if not 0 <= bm < len(maps):", "if False:")]),
    ("M10", "Table 7-32 mapping-count bound removed", "caught",
     [E(MAPS, "if len(rows) > SMAP_MAX_ROWS:", "if False:")]),
    ("M11", "Table 7-32 maximum loosened 62 -> 63", "caught",
     [E(MAPS, "SMAP_MAX_ROWS = 62", "SMAP_MAX_ROWS = 63")]),
    ("M12", "INPUT duplicate rule applied to both directions", "caught",
     [E(MAPS, 'if side.direction == "INPUT":', "if True:")]),
    ("M13", "OUTPUT duplicate rule applied to both directions", "caught",
     [E(MAPS, 'if side.direction == "INPUT":', "if False:")]),
    ("M14", "allowlist reverted to the stale AUDIO_MAP[1] index", "caught",
     [E(MAPS, '"STREAM_PORT_OUTPUT[0] AUDIO_MAP[0] mapping (0,%d,%d,0)',
        '"STREAM_PORT_OUTPUT[0] AUDIO_MAP[1] mapping (0,%d,%d,0)')]),
    ("M15", "allowlist widened by one entry (range(1, 8))", "caught",
     [E(MAPS, "    for c in range(2, 8)\n}", "    for c in range(1, 8)\n}")]),
    ("M16", "allowlist narrowed by one entry (range(3, 8))", "caught",
     [E(MAPS, "    for c in range(2, 8)\n}", "    for c in range(3, 8)\n}")]),
    ("M17", "assert_no_map_deviations neutered", "caught",
     [E(MAPS, "    if new:\n", "    if False:\n")]),
    ("M18", "stream_channel deviation no longer recorded", "caught",
     [E(MAPS, "if sc >= max(chans):", "if False:")]),
    ("M19", "every port treated as dynamic (static gate bypassed)", "caught",
     [E(MAPS, 'if p.get("map_mode", "static") == "dynamic":', "if True:")]),
    ("M20", "any static STREAM_PORT_INPUT map refused", "caught",
     [E(MAPS, "        bm, rows = _static_map_of(p, tag, maps)\n",
        "        if side.direction == \"INPUT\":\n"
        "            raise ValueError(f\"{tag}: static input map refused\")\n"
        "        bm, rows = _static_map_of(p, tag, maps)\n")]),
    # --- deployed model (aem_specs.py) ---
    ("D01", "deployed model gains one new deviation (forward check only)", "caught",
     [E(SPECS, "audio_maps=[[[0, ch, ch, 0] for ch in range(8)]],",
        "audio_maps=[[[0, ch, ch, 0] for ch in range(8)] + [[0, 8, 0, 0]]],")]),
    ("D02", "deployed model loses one deviation (reverse check only)", "caught",
     [E(SPECS, "audio_maps=[[[0, ch, ch, 0] for ch in range(8)]],",
        "audio_maps=[[[0, ch, ch, 0] for ch in range(7)]],")]),
    # --- self-test structure (gen_aem_store.py) ---
    ("S01", "fixture shared across vectors (first copy reused)", "caught",
     [E(GEN, "        spec = _map_fixture()\n        mutate(spec)",
        "        spec = _map_fixture.__dict__.setdefault(\"s\", _map_fixture())\n"
        "        mutate(spec)")]),
    ("S02", "vectors mutate the deployed geometry instead of the fixture", "caught",
     [E(GEN, "        spec = _map_fixture()\n        mutate(spec)",
        "        spec = builtin_spec()\n        mutate(spec)")]),
    ("S03", "cause oracle removed (any ValueError accepted)", "control",
     [E(GEN, "            if cause in str(e):", "            if True:")]),
    ("S04", "reverse exactness (stale) check removed", "control",
     [E(GEN, "    if stale:\n", "    if False:\n")]),
    ("S05", "62-mapping vector reverted to the base geometry", "control",
     [E(GEN, "                1, [[0, c, c % 8, 0] for c in range(63)]),",
        "                0, [[0, c % 8, c, 0] for c in range(63)]),")]),
    ("S06", "fixture-acceptance arm removed", "control",
     [E(GEN, '    accepts("the two-map fixture the vectors mutate builds", _map_fixture())\n', "")]),
    # --- load-bearing demonstrations (weakened self-test + defect) ---
    ("X1", "S03 no oracle + M05 CRF refusal removed", "undetected",
     [E(GEN, "            if cause in str(e):", "            if True:"),
      E(MAPS, "    if not chans:\n", "    if False:\n")]),
    ("X2", "S04 no reverse check + M15 widened allowlist", "undetected",
     [E(GEN, "    if stale:\n", "    if False:\n"),
      E(MAPS, "    for c in range(2, 8)\n}", "    for c in range(1, 8)\n}")]),
    ("X3", "S03 no oracle + S05 base 62-vector + M10 count bound removed", "undetected",
     [E(GEN, "            if cause in str(e):", "            if True:"),
      E(GEN, "                1, [[0, c, c % 8, 0] for c in range(63)]),",
        "                0, [[0, c % 8, c, 0] for c in range(63)]),"),
      E(MAPS, "if len(rows) > SMAP_MAX_ROWS:", "if False:")]),
    ("X4", "S05 base 62-vector (oracle kept) + M10 count bound removed", "caught",
     [E(GEN, "                1, [[0, c, c % 8, 0] for c in range(63)]),",
        "                0, [[0, c % 8, c, 0] for c in range(63)]),"),
      E(MAPS, "if len(rows) > SMAP_MAX_ROWS:", "if False:")]),
    ("X5", "S03 no oracle (new 62-vector geometry) + M10 count bound removed", "caught",
     [E(GEN, "            if cause in str(e):", "            if True:"),
      E(MAPS, "if len(rows) > SMAP_MAX_ROWS:", "if False:")]),
    ("X6", "S03 no oracle + M13 OUTPUT rule applied to both", "undetected",
     [E(GEN, "            if cause in str(e):", "            if True:"),
      E(MAPS, 'if side.direction == "INPUT":', "if False:")]),
    ("X7", "S06 fixture-acceptance arm removed + M20 static inputs refused", "caught",
     [E(GEN, '    accepts("the two-map fixture the vectors mutate builds", _map_fixture())\n', ""),
      E(MAPS, "        bm, rows = _static_map_of(p, tag, maps)\n",
        "        if side.direction == \"INPUT\":\n"
        "            raise ValueError(f\"{tag}: static input map refused\")\n"
        "        bm, rows = _static_map_of(p, tag, maps)\n")]),
    # --- preserved directory / name / Base-format arms ---
    ("P01", "directory contiguity assertion removed", "observe",
     [E(ASM, "        elif prev_t != t:\n", "        elif False:\n")]),
    ("P02", "directory zero-based ascending assertion removed", "observe",
     [E(ASM, "        if i != runs[t][1]:\n", "        if False:\n")]),
    ("P03", "two-level equivalence check neutered", "caught",
     [E(ASM, "    for (t, i) in sorted(probes):\n", "    for (t, i) in []:\n")]),
    ("P04", "NAMED structural equivalence check neutered", "caught",
     [E(ASM, "    for key in sorted(probes):\n", "    for key in []:\n")]),
    ("P05", "whole two_level_directory layout assertions removed", "caught",
     [E(ASM, "        elif prev_t != t:\n", "        elif False:\n"),
      E(ASM, "        if i != runs[t][1]:\n", "        if False:\n"),
      E(ASM, "    for (t, i) in sorted(probes):\n", "    for (t, i) in []:\n")]),
    ("P06", "Base-family cover ignores the ut bit", "caught",
     [E(MAPS, "got |= {c for c in MILAN_BASE_CHANNELS if c <= ch} if ut \\",
        "got |= {ch} & set(MILAN_BASE_CHANNELS) if ut \\")]),
    ("P07", "FORMATS loses its ut entry", "caught",
     [E(DESC, "FORMATS = [0x0205022000806000, 0x0215022002006000]",
        "FORMATS = [0x0205022000806000]")]),
    ("P08", "Base-family cover always reports the whole family", "caught",
     [E(MAPS, "    return got\n", "    return set(MILAN_BASE_CHANNELS)\n")]),
]


def build(mid, edits):
    d = WORK / mid
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(HEAD / "avdecc", d / "avdecc")
    (d / "hdl/common/csr").mkdir(parents=True)
    shutil.copy2(HEAD / "hdl/common/csr/milan_csr.sv", d / "hdl/common/csr/milan_csr.sv")
    for f, old, new, count in edits:
        p = d / f
        text = p.read_text()
        n = text.count(old)
        if n != count:
            return d, f"INVALID: {f} has {n} x {old!r}, expected {count}"
        p.write_text(text.replace(old, new))
    return d, None


def run(mid, desc, expect, edits):
    d, invalid = build(mid, edits)
    res = {"id": mid, "desc": desc, "expect": expect, "invalid": invalid, "runs": {}}
    if invalid:
        return res
    for py in PYS:
        ver = subprocess.run([py, "-c", "import sys;print('%d.%d'%sys.version_info[:2])"],
                             capture_output=True, text=True).stdout.strip()
        p = subprocess.run([py, "-B", "-E", "-s", "avdecc/gen_aem_store.py", "--self-test"],
                           cwd=d, capture_output=True, text=True,
                           env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]})
        log = p.stdout + p.stderr
        (OUT / f"{mid}-py{ver}.log").write_text(log)
        fails = [l.strip()[:150] for l in log.splitlines() if "[FAIL]" in l]
        crash = [l for l in log.splitlines() if l and not l.startswith(" ")
                 and ("Error" in l.split(":")[0] or "Exception" in l.split(":")[0])]
        res["runs"][ver] = {"rc": p.returncode, "fails": fails, "crash": crash[-1:] }
    return res


def verdict(r):
    if r["invalid"]:
        return "INVALID"
    rcs = {v["rc"] for v in r["runs"].values()}
    if len(rcs) != 1:
        return "INTERPRETER-DISAGREE"
    det = rcs.pop() != 0
    want = {"caught": True, "control": False, "undetected": False}.get(r["expect"])
    if want is None:
        return "DETECTED" if det else "NOT-DETECTED"
    return "MET" if det == want else "NOT-MET"


OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(lambda m: run(*m), M))
lines = []
for r in results:
    v = verdict(r)
    rr = r["runs"]
    detail = r["invalid"] or "; ".join(
        f"py{ver} rc={x['rc']} FAIL={len(x['fails'])}"
        + (f" crash={x['crash'][0][:60]}" if x["crash"] else "")
        for ver, x in rr.items())
    first = next((x["fails"][0] for x in rr.values() if x["fails"]), "")
    lines.append(f"{r['id']:4s} {r['expect']:10s} {v:14s} {r['desc']}\n"
                 f"     {detail}\n" + (f"     first FAIL: {first}\n" if first else ""))
summary = "".join(lines)
tally = {}
for r in results:
    tally[verdict(r)] = tally.get(verdict(r), 0) + 1
summary += f"\nTALLY: {json.dumps(tally, sort_keys=True)}  mutants={len(results)}\n"
(OUT / "SUMMARY.txt").write_text(summary)
(OUT / "results.json").write_text(json.dumps(results, indent=1))
print(summary)
