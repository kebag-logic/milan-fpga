#!/usr/bin/env python3
"""Reviewer-owned mutation campaign for PR #619 at 859fa5d5.

usage: mutants.py <clone> <pins-python> <item> [...]
Each entry replaces one exact text (asserted to occur exactly once) in one
tracked file, runs the named check, and restores the file with git checkout.
EXPECT is KILL (check must fail) or PASS (a control). A result row reads
ID | item | expect | observed rc | verdict (OK when observed matches expect).
"""
import subprocess, sys, tempfile, textwrap
from pathlib import Path

C, PINS = Path(sys.argv[1]).resolve(), sys.argv[2]
ITEMS = set(sys.argv[3:])
SYS = sys.executable
TCC = "sw/builder/test_clock_contract.py"
EB = "sw/builder/endstation_builder.py"
SOC = "sw/litex/milan_soc.py"
MK = "tb/verilator/milan_dp/Makefile"
SIM = "tb/verilator/milan_dp/sim_ax1x1gptp.cpp"
SX = "sw/litex/sweep_extra.sh"
TB = "sw/builder/test_builder.py"
SHIP = "sw/builder/test_shipping_clock_constraints.py"

def fn(py, module, *names):
    """argv importing `module` from sw/builder and calling each named test."""
    body = "; ".join(f"m.{n}()" for n in names)
    return [py, "-B", "-c",
            f"import sys, importlib; sys.path.insert(0, 'sw/builder'); m = importlib.import_module({module!r}); {body}"]


def clock(*names, py=SYS):
    return fn(py, "test_clock_contract", *names)

def ship(config="ax7101_1x1_tdm8", port="e1"):
    out = tempfile.mkdtemp(prefix="r396-ship-")
    return ([PINS, "-B", str(C / SHIP), "--config", config, "--port", port, "--output-dir", out], "sw/litex")

ARTY_ANCHOR = '    if args.board == "arty":\n        platform.toolchain.bitstream_commands += ['
M = [
 # item 1: AX 1x1 gPTP simulation clock
 ("1-CTL", "1", "PASS", None, None, None, clock("test_sim_clock")),
 ("1-A Makefile literal clock", "1", "KILL", MK,
  "AX_GPTP_HZ := $(shell python3 -I -c 'import runpy, sys; print(runpy.run_path(sys.argv[1])[\"CPU_HZ\"])' $(CLOCK_RECIPE))",
  "AX_GPTP_HZ := 50000000", clock("test_sim_clock")),
 ("1-B ROM rule literal", "1", "KILL", MK, "--clk-hz $(AX_GPTP_HZ) --mac", "--clk-hz 50000000 --mac", clock("test_sim_clock")),
 ("1-C harness -D dropped", "1", "KILL", MK, '-CFLAGS "-DMILAN_CLK_HZ_TB=$(AX_GPTP_HZ) -Wall -Wextra"', '-CFLAGS "-Wall -Wextra"', clock("test_sim_clock")),
 ("1-D elaboration literal", "1", "KILL", MK, "-GMILAN_CLK_FREQ_HZ=$(AX_GPTP_HZ) -GGPTP_PLANE_EN_P=1", "-GMILAN_CLK_FREQ_HZ=50000000 -GGPTP_PLANE_EN_P=1", clock("test_sim_clock")),
 ("1-E shell status not taken", "1", "KILL", MK, "ifneq ($(.SHELLSTATUS),0)\n$(error $(CLOCK_RECIPE)", "ifneq (x,x)\n$(error $(CLOCK_RECIPE)", clock("test_sim_clock")),
 ("1-F harness literal kHz", "1", "KILL", SIM, "constexpr uint64_t kHz = MILAN_CLK_HZ_TB;", "constexpr uint64_t kHz = 50000000;", clock("test_sim_clock")),
 ("1-G harness report literal 50 MHz", "1", "KILL", SIM, 'printf("ax1x1gptp PHYSICAL: %g MHz', 'printf("ax1x1gptp PHYSICAL: 50 MHz %g', clock("test_sim_clock")),
 # item 2: sweep_extra.sh
 ("2-CTL", "2", "PASS", None, None, None, clock("test_extra_sweep_clocks", "test_extra_sweep_invocation")),
 ("2-A entity dir not passed", "2", "KILL", SX, '"--entity-gen-dir", gen, sep="\\n")', 'sep="\\n")', clock("test_extra_sweep_clocks", "test_extra_sweep_invocation")),
 ("2-B old positional parse", "2", "KILL", SX, "main() {\n  parse_args \"$@\"",
  "main() {\n  BOARD=${1:?board}; TAG=${2:?tag}; DRY=0; [ \"${3:-}\" = --dry-run ] && DRY=1", clock("test_extra_sweep_invocation")),
 ("2-C unknown option kept as argument", "2", "KILL", SX, '      -*) usage "unknown option $arg";;\n', "", clock("test_extra_sweep_invocation")),
 ("2-D extra arguments ignored", "2", "KILL", SX, '[ "${#positional[@]}" -eq 2 ]', '[ "${#positional[@]}" -ge 2 ]', clock("test_extra_sweep_invocation")),
 ("2-E empty tag accepted", "2", "KILL", SX, '  [ -n "$TAG" ] || usage "empty tag"\n', "", clock("test_extra_sweep_invocation")),
 ("2-F launch guard removed", "2", "KILL", SX, "    if built != gen:\n", "    if False:\n", clock("test_extra_sweep_invocation")),
 ("2-G interpreter exported late", "2", "KILL", SX,
  '  export PATH="$HOME/litex-milan/venv/bin:$PATH"\n', "", clock("test_extra_sweep_invocation")),
 ("2-H entity dir named wrong", "2", "KILL", SX, 'gen = eb.ROOT / eb.GEN_CONFIG_DIR / cfg["name"]', 'gen = eb.ROOT / eb.GEN_CONFIG_DIR / "endstation_ax7101_8x8"', clock("test_extra_sweep_clocks")),
 ("2-I launch guard always refuses (positive launch path)", "2", "KILL", SX, "    if built != gen:\n", "    if True:\n", clock("test_extra_sweep_invocation")),
 # item 3: contract clock by path
 ("3-CTL builder", "3", "PASS", None, None, None, clock("test_builder_clock_source")),
 ("3-B5 builder literal mirror", "3", "KILL", EB,
  'BAREMETAL_CLK_HZ = runpy.run_path(ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]',
  "BAREMETAL_CLK_HZ = 50_000_000", clock("test_builder_clock_source")),
 ("3-Bns builder namespace import", "3", "KILL", EB,
  'BAREMETAL_CLK_HZ = runpy.run_path(ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]\nsys.path.insert(0, str(ROOT))',
  'sys.path.insert(0, str(ROOT))\nfrom tb.verilator.nvm_capture_cpu.recipe import CPU_HZ as BAREMETAL_CLK_HZ', clock("test_builder_clock_source")),
 ("3-CTL SoC", "3", "PASS", None, None, None, clock("test_soc_clock_contract", py=PINS)),
 ("3-S7 SoC literal mirror", "3", "KILL", SOC,
  'BAREMETAL_CLK_HZ = runpy.run_path(REPO_ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]',
  "BAREMETAL_CLK_HZ = 50_000_000", clock("test_soc_clock_contract", py=PINS)),
 ("3-Sns SoC namespace import", "3", "KILL", SOC,
  'BAREMETAL_CLK_HZ = runpy.run_path(REPO_ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]\nsys.path.insert(0, str(REPO_ROOT))',
  'sys.path.insert(0, str(REPO_ROOT))\nfrom tb.verilator.nvm_capture_cpu.recipe import CPU_HZ as BAREMETAL_CLK_HZ', clock("test_soc_clock_contract", py=PINS)),
 # item 4: equal-clock skip in the ledger
 ("4-CTL", "4", "PASS", None, None, None, fn(SYS, "test_builder", "test_rom_clock_skip_reaches_the_ledger")),
 ("4-A skip printed only", "4", "KILL", TCC, '                skip("clock contract", f"{path.stem}: system-clock ROM control not applicable, "',
  '                _print_skip("clock contract", f"{path.stem}: system-clock ROM control not applicable, "', fn(SYS, "test_builder", "test_rom_clock_skip_reaches_the_ledger")),
 ("4-B wrapper drops the ledger", "4", "KILL", TB, "    test_gptp_rom_clock(skip=skip)\n", "    test_gptp_rom_clock()\n", fn(SYS, "test_builder", "test_rom_clock_skip_reaches_the_ledger")),
 ("4-C run list bypasses the wrapper", "4", "KILL", TB, "test_baremetal_clock_contract, test_rom_clock_contract, test_rom_clock_skip_reaches_the_ledger,",
  "test_baremetal_clock_contract, test_gptp_rom_clock, test_rom_clock_skip_reaches_the_ledger,", fn(SYS, "test_builder", "test_rom_clock_skip_reaches_the_ledger")),
 ("4-D ledger kind changed", "4", "KILL", TB, "    test_gptp_rom_clock(skip=skip)\n", "    test_gptp_rom_clock(skip=lambda g, w: skip(g, w, 'gate'))\n", fn(SYS, "test_builder", "test_rom_clock_skip_reaches_the_ledger")),
 # item 6: MAC and hex shapes
 ("6-CTL", "6", "PASS", None, None, None, [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-A doubled underscores", "6", "KILL", EB, 'r"(?:0[xX])?([0-9A-Fa-f](?:_?[0-9A-Fa-f])*)"', 'r"(?:0[xX])?([0-9A-Fa-f](?:_*[0-9A-Fa-f])*)"', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-B prefix match not fullmatch", "6", "KILL", EB, "    match = HEX_TEXT.fullmatch(v)\n", "    match = HEX_TEXT.match(v)\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-C width off by one", "6", "KILL", EB, "    if len(digits) > bits // 4:\n", "    if len(digits) >= bits // 4:\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-D width dropped", "6", "KILL", EB, "    if len(digits) > bits // 4:\n", "    if int(digits, 16) >> bits:\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-E mixed separators", "6", "KILL", EB, r'[0-9A-Fa-f]{2}(?:\1[0-9A-Fa-f]{2}){4}', r'[0-9A-Fa-f]{2}(?:[:-][0-9A-Fa-f]{2}){4}', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-F short MAC digit strings", "6", "KILL", EB, "    if len(digits) != MAC48_MAX.bit_length() // 4:\n", "    if not digits or len(digits) > MAC48_MAX.bit_length() // 4:\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-G unpadded octets", "6", "KILL", EB, r'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{2}([:-])[0-9A-Fa-f]{2}(?:\1[0-9A-Fa-f]{2}){4}")',
  r'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{1,2}([:-])[0-9A-Fa-f]{1,2}(?:\1[0-9A-Fa-f]{1,2}){4}")', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-H sign admitted", "6", "KILL", EB, 'r"(?:0[xX])?([0-9A-Fa-f]', 'r"[+-]?(?:0[xX])?([0-9A-Fa-f]', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-I Unicode digits via \\d", "6", "KILL", EB, 'r"(?:0[xX])?([0-9A-Fa-f](?:_?[0-9A-Fa-f])*)"', r'r"(?:0[xX])?([\dA-Fa-f](?:_?[\dA-Fa-f])*)"', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-J capabilities width 24", "6", "KILL", EB, '_declared_uint(ent["entity_capabilities"], 32,', '_declared_uint(ent["entity_capabilities"], 24,', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-K OUI width 32", "6", "KILL", EB, '_declared_uint(ent["vendor_oui"], 24,', '_declared_uint(ent["vendor_oui"], 32,', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-L DMAC width 64", "6", "KILL", EB, 'dmac = _hex_text(s["stream_dmac_base"], MAC48_MAX.bit_length(),', 'dmac = _hex_text(s["stream_dmac_base"], 64,', [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-M prefix on octets", "6", "KILL", EB, "    octets = MAC_OCTETS.fullmatch(v)\n", "    octets = MAC_OCTETS.fullmatch(v.removeprefix('0x'))\n    v = v.removeprefix('0x')\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-N whitespace stripped", "6", "KILL", EB, "    match = HEX_TEXT.fullmatch(v)\n", "    match = HEX_TEXT.fullmatch(v.strip())\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 ("6-O MAC hex without underscores", "6", "KILL", EB, "    elif text:\n        digits = text[1].replace(\"_\", \"\")\n", "    elif text and '_' not in v:\n        digits = text[1]\n", [SYS, "-B", "sw/builder/test_declarations.py"]),
 # item 7: shipping probe asserts #395 hooks
 ("7-CTL 1x1 e1", "7", "PASS", None, None, None, ship()),
 ("7-MD bitstream_commands replaced (1x1 e1)", "7", "KILL", SOC, ARTY_ANCHOR, "    platform.toolchain.bitstream_commands = []\n" + ARTY_ANCHOR, ship()),
 ("7-ME pre_placement cleared (1x1 e1)", "7", "KILL", SOC, ARTY_ANCHOR, "    platform.toolchain.pre_placement_commands.clear()\n" + ARTY_ANCHOR, ship()),
 ("7-MD bitstream_commands replaced (8x8 e2)", "7", "KILL", SOC, ARTY_ANCHOR, "    platform.toolchain.bitstream_commands = []\n" + ARTY_ANCHOR, ship("ax7101_8x8", "e2")),
 ("7-ME pre_placement cleared (8x8 e2)", "7", "KILL", SOC, ARTY_ANCHOR, "    platform.toolchain.pre_placement_commands.clear()\n" + ARTY_ANCHOR, ship("ax7101_8x8", "e2")),
 ("7-C configure moved after placement", "7", "KILL", SOC, ARTY_ANCHOR,
  "    _cfg = [c for c in platform.toolchain.pre_placement_commands if c.startswith('kl_timing_grade_configure')]\n"
  "    platform.toolchain.pre_placement_commands[:] = [c for c in platform.toolchain.pre_placement_commands if c not in _cfg]\n"
  "    platform.toolchain.pre_routing_commands[:0] = _cfg\n" + ARTY_ANCHOR, ship()),
 ("7-D reports moved before routing", "7", "KILL", SOC, ARTY_ANCHOR,
  "    _rep = [c for c in platform.toolchain.bitstream_commands if c.startswith('kl_timing_grade_reports')]\n"
  "    platform.toolchain.bitstream_commands[:] = [c for c in platform.toolchain.bitstream_commands if c not in _rep]\n"
  "    platform.toolchain.pre_routing_commands[:0] = _rep\n" + ARTY_ANCHOR, ship()),
 ("7-E configure duplicated", "7", "KILL", SOC, ARTY_ANCHOR,
  "    platform.toolchain.pre_placement_commands += [c for c in platform.toolchain.pre_placement_commands if c.startswith('kl_timing_grade_configure')]\n" + ARTY_ANCHOR, ship()),
 ("7-OLD probe without hook check under MD (before-state control)", "7", "PASS", [(SHIP, "            assert_timing_grade_hooks(commands)\n", ""), (SOC, ARTY_ANCHOR, "    platform.toolchain.bitstream_commands = []\n" + ARTY_ANCHOR)], None, None, ship()),
]

def git(*a):
    return subprocess.run(["git", "-C", str(C), *a], capture_output=True, text=True)

rows = []
for mid, item, expect, path, old, new, cmd in M:
    if item not in ITEMS:
        continue
    edits = path if isinstance(path, list) else ([(path, old, new)] if path else [])
    touched = []
    try:
        for p, o, n in edits:
            f = C / p
            text = f.read_text()
            assert text.count(o) == 1, f"{mid}: anchor occurs {text.count(o)} times in {p}"
            f.write_text(text.replace(o, n))
            touched.append(p)
        argv, cwd = (cmd if isinstance(cmd, tuple) else (cmd, "."))
        r = subprocess.run(argv, cwd=C / cwd, capture_output=True, text=True, timeout=900)
        observed = "KILL" if r.returncode else "PASS"
        why = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or [""])[-1][:200]
    finally:
        for p in touched:
            git("checkout", "--", p)
    status = "OK" if observed == expect else "MISMATCH"
    rows.append((mid, item, expect, observed, status, why))
    print(f"{mid} | item {item} | expect {expect} | observed {observed} (rc={r.returncode}) | {status} | {why}", flush=True)
dirty = git("status", "--porcelain").stdout.strip()
print(f"SUMMARY entries={len(rows)} mismatches={sum(r[4] != 'OK' for r in rows)} tree_clean_after={'yes' if not dirty else 'NO: ' + dirty}")
