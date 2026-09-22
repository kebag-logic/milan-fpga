#!/usr/bin/env python3
"""Focused, independent controls for issue #478 at the exact head.

Runs inside the scratch clones only (never the review checkout):
  HEAD_ROOT = <scratch>/git-sub   (1496558d, submodules at their gitlinks)
  BASE_ROOT = <scratch>/base-sub  (88e9276b, the PR's current base)

Sections
  A  the three gate 36a functions and gate 32 at the head, pristine
  B  the head's gate 36a functions against the BASE builder (can the gate fail
     for the defect it claims to detect?)
  C  builder mutants (source-text edits of the head builder, loaded as a
     separate module and swapped in as test_builder.eb)
  D  mutants of the REAL tb/verilator/pp_shadow/sim_main.cpp (written into the
     scratch clone, restored and blob-checked after each row); R rows are the
     residual spellings outside the settled comparison (recorded, not graded)
  E  mutants of the REAL shipping YAML (scratch only, restored after each row)
  F  loader-versus-image behaviour and pre-existing edge cases, head and base

Each row prints: section/id, expectation, observed outcome, MATCH/MISMATCH.
Exit status is non-zero if any graded row mismatches or a restore fails.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
import traceback
from pathlib import Path

SCRATCH = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/r222-478-r2-scratch")
HEAD_ROOT = SCRATCH / "git-sub"
BASE_ROOT = SCRATCH / "base-sub"
SIM = HEAD_ROOT / "tb/verilator/pp_shadow/sim_main.cpp"
YAML_CUR = HEAD_ROOT / "configs/endstation_arty_current.yaml"
YAML_4X4 = HEAD_ROOT / "configs/endstation_arty_4x4.yaml"

sys.path.insert(0, str(HEAD_ROOT / "sw/builder"))
import test_builder as tb  # noqa: E402  (inserts the head's sys.path entries)

HEAD_EB = tb.eb
mismatches = 0


def load_builder(source: str, file_path: Path, name: str):
    """Execute builder source text as a fresh module whose __file__ is the
    given checkout's builder path (so its ROOT/HERE resolve there)."""
    spec = importlib.util.spec_from_loader(name, loader=None, origin=str(file_path))
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = str(file_path)
    sys.modules[name] = mod
    exec(compile(source, str(file_path), "exec"), mod.__dict__)
    return mod


def run(fn, eb=None) -> tuple[str, str]:
    """Run one gate function quietly; return (PASS|FAIL, first line of why)."""
    saved = tb.eb
    if eb is not None:
        tb.eb = eb
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn()
        return "PASS", ""
    except BaseException as exc:  # noqa: BLE001 - a probe records every failure kind
        return "FAIL", f"{type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}"[:160]
    finally:
        tb.eb = saved


def grade(row: str, expect: str, got: tuple[str, str], graded: bool = True) -> None:
    global mismatches
    verdict = "MATCH" if got[0] == expect else ("MISMATCH" if graded else "RESIDUAL")
    if graded and got[0] != expect:
        mismatches += 1
    print(f"{row:<58} expect {expect:<4} got {got[0]:<4} {verdict:<8} {got[1]}")


def git_blob(path: Path) -> str:
    return subprocess.run(["git", "hash-object", "--no-filters", str(path)],
                          check=True, capture_output=True, text=True).stdout.strip()


def head_blob(rel: str) -> str:
    return subprocess.run(["git", "-C", str(HEAD_ROOT), "rev-parse", f"HEAD:{rel}"],
                          check=True, capture_output=True, text=True).stdout.strip()


@contextlib.contextmanager
def mutated(path: Path, old: str, new: str, count: int = 1):
    """Replace `old` by `new` in a real scratch file; restore and verify."""
    global mismatches
    original = path.read_bytes()
    text = original.decode()
    assert text.count(old) >= 1, f"{path.name}: pattern not found: {old!r}"
    path.write_text(text.replace(old, new, count))
    try:
        yield
    finally:
        path.write_bytes(original)
        rel = str(path.relative_to(HEAD_ROOT))
        if git_blob(path) != head_blob(rel):
            mismatches += 1
            print(f"RESTORE FAILED for {rel}")


LOADER = tb.test_audio_unit_rates_loader_contract
SHIP = tb.test_audio_unit_shipping_rates
PPS = tb.test_pp_shadow_audio_unit_rates_match_config
DOCMAP = tb.test_builder_doc_key_map

print(f"head root {HEAD_ROOT} @ {subprocess.run(['git','-C',str(HEAD_ROOT),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()}")
print(f"base root {BASE_ROOT} @ {subprocess.run(['git','-C',str(BASE_ROOT),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()}")
print(f"python {sys.version.split()[0]}; MAX_AUDIO_UNIT_RATES at head = {HEAD_EB.MAX_AUDIO_UNIT_RATES}")

print("\n== A: pristine head")
grade("A1 gate 36a loader contract", "PASS", run(LOADER))
grade("A2 gate 36a shipping images", "PASS", run(SHIP))
grade("A3 gate 36a pp_shadow AU_RATES_C vs YAML", "PASS", run(PPS))
grade("A4 gate 32 builder doc key map", "PASS", run(DOCMAP))

print("\n== B: head gate 36a against the base (88e9276b) builder")
base_src_path = BASE_ROOT / "sw/builder/endstation_builder.py"
BASE_EB = load_builder(base_src_path.read_text(), base_src_path, "eb_base")
print(f"base builder has MAX_AUDIO_UNIT_RATES: {hasattr(BASE_EB, 'MAX_AUDIO_UNIT_RATES')}")
grade("B1 loader contract vs base builder", "FAIL", run(LOADER, BASE_EB))
grade("B2 shipping images vs base builder", "PASS", run(SHIP, BASE_EB))
grade("B3 pp_shadow comparison vs base builder", "PASS", run(PPS, BASE_EB))

print("\n== C: builder mutants (head source, loaded separately)")
head_src_path = HEAD_ROOT / "sw/builder/endstation_builder.py"
HEAD_SRC = head_src_path.read_text()
COUNT_BLOCK = (
    "    if len(rates) > MAX_AUDIO_UNIT_RATES:\n"
    "        raise ConfigError(\n"
    "            f\"clocking.audio_unit_rates_hz has {len(rates)} entries; \"\n"
    "            f\"processor walk bound is {MAX_AUDIO_UNIT_RATES} (L10, \"\n"
    "            \"protocol-processor/docs/architecture/07_memory_maps.md section 3.1)\")\n")
DUP_BLOCK = (
    "    if len(set(rates)) != len(rates):\n"
    "        raise ConfigError(\"clocking.audio_unit_rates_hz contains duplicate entries\")\n")
MEMBER_BLOCK = (
    "    if rate not in rates:\n"
    "        raise ConfigError(\"sampling_rate_hz must appear in audio_unit_rates_hz\")\n")
assert HEAD_SRC.count(COUNT_BLOCK) == 1 and HEAD_SRC.count(DUP_BLOCK) == 1
assert HEAD_SRC.count(MEMBER_BLOCK) == 1
MUTANTS = [
    ("C1 bound 8 -> 9", "MAX_AUDIO_UNIT_RATES = 8\n", "MAX_AUDIO_UNIT_RATES = 9\n", "FAIL"),
    ("C2 bound 8 -> 7", "MAX_AUDIO_UNIT_RATES = 8\n", "MAX_AUDIO_UNIT_RATES = 7\n", "FAIL"),
    ("C3 '>' -> '>=' in the count test", "if len(rates) > MAX_AUDIO_UNIT_RATES:",
     "if len(rates) >= MAX_AUDIO_UNIT_RATES:", "FAIL"),
    ("C4 duplicate refusal removed", DUP_BLOCK, "", "FAIL"),
    ("C5 duplicate test on raw (pre-int) values", "    if len(set(rates)) != len(rates):\n",
     "    _raw = list(clk.get(\"audio_unit_rates_hz\", [rate]))\n"
     "    if len(set(_raw)) != len(_raw):\n", "FAIL"),
    ("C6 rates stored sorted", "    rates = clocking[\"audio_unit_rates_hz\"]\n",
     "    clocking[\"audio_unit_rates_hz\"].sort()\n    rates = clocking[\"audio_unit_rates_hz\"]\n", "FAIL"),
    ("C7 omitted list defaults to [48000] always", "clk.get(\"audio_unit_rates_hz\", [rate])",
     "clk.get(\"audio_unit_rates_hz\", [48000])", "FAIL"),
    ("C8 duplicate test before count test (equivalent)", COUNT_BLOCK + DUP_BLOCK,
     DUP_BLOCK + COUNT_BLOCK, "PASS"),
    ("C9 current-rate membership removed", MEMBER_BLOCK, "", "FAIL"),
    ("C10 count refusal no longer names L10", "(L10, \"", "(rule, \"", "FAIL"),
    ("C11 count refusal removed", COUNT_BLOCK, "", "FAIL"),
    ("C12 count refusal truncates instead of refusing", COUNT_BLOCK,
     "    del rates[MAX_AUDIO_UNIT_RATES:]\n", "FAIL"),
]
for label, old, new, expect in MUTANTS:
    assert HEAD_SRC.count(old) >= 1, label
    mod = load_builder(HEAD_SRC.replace(old, new, 1), head_src_path,
                       "eb_mut_" + label.split()[0])
    got = run(LOADER, mod)
    if label.startswith("C7"):
        got = got if got[0] == "FAIL" else run(SHIP, mod)
    grade(label, expect, got)

print("\n== D: real pp_shadow sim_main.cpp mutants (gate 36a pp_shadow arm)")
DECL = "static constexpr uint32_t AU_RATES_C[3] = {\n        48000u, 96000u, 192000u};"
assert SIM.read_text().count(DECL) == 1
D_ROWS = [
    ("D1 value 96000u -> 88200u", DECL, DECL.replace("96000u", "88200u"), "FAIL"),
    ("D2 order 48000u,96000u swapped", DECL, DECL.replace("48000u, 96000u", "96000u, 48000u"), "FAIL"),
    ("D3 declared length [3] -> [4]", DECL, DECL.replace("[3]", "[4]"), "FAIL"),
    ("D4 initializer shortened (implicit zero fill)", DECL, DECL.replace(", 192000u", ""), "FAIL"),
    ("D5 declaration commented out (block comment)", DECL, "/* " + DECL + " */", "FAIL"),
    ("D6 second literal declaration added", DECL, DECL + "\n    " + DECL, "FAIL"),
    ("D7 hex literal word 0xBB80u for 48000u", DECL, DECL.replace("48000u,", "0xBB80u,"), "FAIL"),
    ("D8 declared length as expression [1 + 2]", DECL, DECL.replace("[3]", "[1 + 2]"), "FAIL"),
    ("D9 trailing comma in initializer (legal C++)", DECL, DECL.replace("192000u}", "192000u,}"), "PASS"),
    ("D10 uppercase U suffix (legal C++)", DECL, DECL.replace("u,", "U,").replace("192000u", "192000U"), "PASS"),
]
for label, old, new, expect in D_ROWS:
    with mutated(SIM, old, new):
        grade(label, expect, run(PPS))
R_ROWS = [
    ("R1 AU_CUR_RATE_C 48000u -> 96000u", "AU_CUR_RATE_C = 48000u;", "AU_CUR_RATE_C = 96000u;"),
    ("R2 image sampling_rates_count literal 3 -> 2", "put16be_v(d, 142, 3);", "put16be_v(d, 142, 2);"),
    ("R3 fill loop bound k < 3 -> k < 2", "for (size_t k = 0; k < 3; k++)", "for (size_t k = 0; k < 2; k++)"),
    ("R4 AU_LEN_C 144 + 4 * 3 -> 144 + 4 * 2", "AU_LEN_C     = 144 + 4 * 3;", "AU_LEN_C     = 144 + 4 * 2;"),
]
for label, old, new in R_ROWS:
    with mutated(SIM, old, new):
        grade(label + " (S1 residual)", "PASS", run(PPS), graded=False)

print("\n== E: real shipping YAML mutants (scratch only)")
Y_OLD = "audio_unit_rates_hz: [48000, 96000, 192000]"
E_ROWS = [
    ("E1 arty_current list shortened to [48000, 96000]", YAML_CUR, Y_OLD,
     "audio_unit_rates_hz: [48000, 96000]", [("pp_shadow", PPS), ("shipping", SHIP)]),
    ("E2 arty_current list reordered", YAML_CUR, Y_OLD,
     "audio_unit_rates_hz: [96000, 48000, 192000]", [("pp_shadow", PPS), ("shipping", SHIP)]),
    ("E3 arty_current duplicate appended", YAML_CUR, Y_OLD,
     "audio_unit_rates_hz: [48000, 96000, 192000, 192000]", [("shipping", SHIP)]),
    ("E4 arty_4x4 advertises 96000 too", YAML_4X4, "audio_unit_rates_hz: [48000]",
     "audio_unit_rates_hz: [48000, 96000]", [("shipping", SHIP)]),
]
for label, path, old, new, fns in E_ROWS:
    with mutated(path, old, new):
        for name, fn in fns:
            grade(f"{label} -> {name}", "FAIL", run(fn))

print("\n== F: loader versus image, head and base")


def outcome(eb, rates, current=48000, omit=False):
    """load_config then the packed image for a variant of arty_current."""
    def mutate(c):
        c["clocking"]["sampling_rate_hz"] = current
        if omit:
            c["clocking"].pop("audio_unit_rates_hz", None)
        else:
            c["clocking"]["audio_unit_rates_hz"] = rates
    path = tb._variant(tb.CONFIGS["arty_current"], mutate)
    try:
        try:
            cfg = eb.load_config(str(path))
        except Exception as exc:  # noqa: BLE001
            return f"load_config {type(exc).__name__}: {str(exc)[:110]}"
        loaded = cfg["clocking"]["audio_unit_rates_hz"]
        try:
            ovl = eb.emit_aem_overlay(cfg)
            img = eb._entity_model_image(cfg, ovl)["aem_desc.bin"]
            desc = tb.image_descriptor(img, 0x0002)
            import struct
            off, cnt = struct.unpack_from(">HH", desc, 140)
            words = list(struct.unpack_from(f">{cnt}I", desc, off))
            return f"loaded {loaded}; image offset {off} count {cnt} rates {words}"
        except Exception as exc:  # noqa: BLE001
            return f"loaded {loaded}; image {type(exc).__name__}: {str(exc)[:90]}"
    finally:
        path.unlink()


EIGHT = [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000]
F_ROWS = [
    ("F1 eight distinct (gate 36a's legal eight)", dict(rates=EIGHT)),
    ("F2 nine distinct", dict(rates=EIGHT + [22050])),
    ("F3 nine copies of 48000", dict(rates=[48000] * 9)),
    ("F4 [48000, '48000'] (duplicate after int())", dict(rates=[48000, "48000"])),
    ("F5 [48000, 48000.5] (duplicate after int())", dict(rates=[48000, 48000.5])),
    ("F6 base rates reordered [192000, 48000, 96000]", dict(rates=[192000, 48000, 96000])),
    ("F7 omitted list, current 96000", dict(rates=None, current=96000, omit=True)),
    ("F8 empty list", dict(rates=[])),
    ("F9 scalar 48000 (not a list)", dict(rates=48000)),
    ("F10 null", dict(rates=None)),
    ("F11 eight copies of 48000", dict(rates=[48000] * 8)),
]
for label, kw in F_ROWS:
    print(f"{label}")
    print(f"    head: {outcome(HEAD_EB, **kw)}")
    print(f"    base: {outcome(BASE_EB, **kw)}")

print(f"\ngraded mismatches: {mismatches}")
status = subprocess.run(["git", "-C", str(HEAD_ROOT), "status", "--porcelain",
                         "--untracked-files=no"], capture_output=True, text=True).stdout
print(f"head scratch tracked changes after probes: {len(status.splitlines())}")
sys.exit(1 if mismatches else 0)
