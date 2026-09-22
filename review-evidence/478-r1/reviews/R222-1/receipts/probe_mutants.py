#!/usr/bin/env python3
"""[R222] Focused mutation probes for gate 36a, in memory, against a scratch root.

Usage: probe_mutants.py <scratch-root>

Nothing on disk under <scratch-root> is modified: builder mutants are the
tracked source text with one textual substitution, executed as a fresh module
and swapped into test_builder's `eb` global; pp_shadow mutants are written to a
private temporary root that test_builder's ROOT is pointed at for one call.
Each row states the expected outcome (FAIL = the gate must catch it; PASS = a
non-defect or residual control) and the observed one.
"""
import copy
import importlib.util
import sys
import tempfile
import types
from pathlib import Path

import yaml

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(
    "test_builder", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = tb
spec.loader.exec_module(tb)
BUILDER = root / "sw/builder/endstation_builder.py"
PRISTINE_EB = tb.eb
SRC = BUILDER.read_text()
SIM = (root / "tb/verilator/pp_shadow/sim_main.cpp").read_text()
REAL_ROOT, REAL_CONFIGS = tb.ROOT, dict(tb.CONFIGS)

LOADER = "test_audio_unit_rates_loader_contract"
SHIP = "test_audio_unit_shipping_rates"
SHADOW = "test_pp_shadow_audio_unit_rates_match_config"


def builder_module(old: str, new: str) -> types.ModuleType:
    assert SRC.count(old) == 1, f"mutation anchor not unique: {old!r}"
    mod = types.ModuleType("endstation_builder")
    mod.__file__ = str(BUILDER)
    sys.modules["endstation_builder"] = mod
    try:
        exec(compile(SRC.replace(old, new), str(BUILDER), "exec"), mod.__dict__)
    finally:
        sys.modules["endstation_builder"] = PRISTINE_EB
    return mod


def run(fn_name: str) -> str:
    try:
        getattr(tb, fn_name)()
    except BaseException as exc:
        return f"FAIL ({type(exc).__name__}: {str(exc)[:150]})"
    return "PASS"


rows = []


def row(label: str, fn_name: str, expect: str, observed: str) -> None:
    ok = observed.startswith(expect)
    rows.append(ok)
    print(f"{'OK ' if ok else 'BAD'} expect={expect:4} got={observed} :: "
          f"{fn_name} :: {label}")


# ---------------------------------------------------------------- builder
BUILDER_MUTANTS = [
    ("MAX_AUDIO_UNIT_RATES 8 -> 9", "MAX_AUDIO_UNIT_RATES = 8",
     "MAX_AUDIO_UNIT_RATES = 9", "FAIL"),
    ("MAX_AUDIO_UNIT_RATES 8 -> 7", "MAX_AUDIO_UNIT_RATES = 8",
     "MAX_AUDIO_UNIT_RATES = 7", "FAIL"),
    ("count test > -> >=", "if len(rates) > MAX_AUDIO_UNIT_RATES:",
     "if len(rates) >= MAX_AUDIO_UNIT_RATES:", "FAIL"),
    ("duplicate refusal removed",
     "    if len(set(rates)) != len(rates):\n        raise ConfigError(\"clocking.audio_unit_rates_hz contains duplicate entries\")\n",
     "", "FAIL"),
    ("duplicate test on raw (pre-int) values",
     "if len(set(rates)) != len(rates):",
     "if len(set(clk.get('audio_unit_rates_hz', [rate]))) != len(rates):", "FAIL"),
    ("duplicates silently dropped instead of refused",
     "    if len(set(rates)) != len(rates):\n        raise ConfigError(\"clocking.audio_unit_rates_hz contains duplicate entries\")\n",
     "    rates[:] = list(dict.fromkeys(rates))\n", "FAIL"),
    ("list silently truncated to the bound instead of refused",
     "    if len(rates) > MAX_AUDIO_UNIT_RATES:\n        raise ConfigError(",
     "    del rates[MAX_AUDIO_UNIT_RATES:]\n    if False:\n        raise ConfigError(", "FAIL"),
    ("list sorted (order not preserved)",
     "audio_unit_rates_hz=[int(r) for r in\n                             clk.get(\"audio_unit_rates_hz\", [rate])],",
     "audio_unit_rates_hz=sorted([int(r) for r in\n                             clk.get(\"audio_unit_rates_hz\", [rate])]),", "FAIL"),
    ("count message drops the L10 rule name", "(L10, \"", "(\"", "FAIL"),
    ("count message drops the walk bound", "processor walk bound is {MAX_AUDIO_UNIT_RATES}",
     "processor limit exceeded", "FAIL"),
    ("omitted list defaults to every base rate",
     "clk.get(\"audio_unit_rates_hz\", [rate])",
     "clk.get(\"audio_unit_rates_hz\", sorted(BASE_RATE_HZ))", "FAIL"),
    ("current-rate membership check removed",
     "    if rate not in rates:\n        raise ConfigError(\"sampling_rate_hz must appear in audio_unit_rates_hz\")\n",
     "", "FAIL"),
    ("NON-DEFECT: duplicate check moved before count check",
     "    if len(rates) > MAX_AUDIO_UNIT_RATES:\n",
     "    if len(set(rates)) != len(rates):\n        raise ConfigError(\"clocking.audio_unit_rates_hz contains duplicate entries\")\n    if len(rates) > MAX_AUDIO_UNIT_RATES:\n",
     "PASS"),
]
for label, old, new, expect in BUILDER_MUTANTS:
    tb.eb = builder_module(old, new)
    try:
        row(label, LOADER, expect, run(LOADER))
    finally:
        tb.eb = PRISTINE_EB

# Each negative arm on its own: a builder that refuses everything the loader
# gate lists EXCEPT one arm must fail that arm (so no arm is masked by another).
ARM_ISOLATION = [
    ("only the distinct-ninth arm unenforced (count check removed)",
     "    if len(rates) > MAX_AUDIO_UNIT_RATES:\n        raise ConfigError(",
     "    if False:\n        raise ConfigError("),
]
for label, old, new in ARM_ISOLATION:
    tb.eb = builder_module(old, new)
    try:
        row(label, LOADER, "FAIL", run(LOADER))
    finally:
        tb.eb = PRISTINE_EB

# ---------------------------------------------------------- shipping image
real_overlay = PRISTINE_EB.emit_aem_overlay


def reversed_overlay(cfg):
    ovl = real_overlay(cfg)
    ovl = copy.deepcopy(ovl)
    ovl["sampling_rates_hz"] = list(reversed(ovl["sampling_rates_hz"]))
    return ovl


PRISTINE_EB.emit_aem_overlay = reversed_overlay
try:
    row("overlay/image rate order reversed (config unchanged)", SHIP, "FAIL", run(SHIP))
finally:
    PRISTINE_EB.emit_aem_overlay = real_overlay

tmpdir = Path(tempfile.mkdtemp(prefix="r222-probe-"))


def cfg_variant(name: str, rates: list) -> Path:
    cfg = yaml.safe_load(REAL_CONFIGS[name].read_text())
    cfg["clocking"]["audio_unit_rates_hz"] = rates
    out = tmpdir / f"{name}.yaml"
    out.write_text(yaml.safe_dump(cfg))
    return out


tb.CONFIGS = dict(REAL_CONFIGS, arty_4x4=cfg_variant("arty_4x4", [48000, 96000]))
try:
    row("arty_4x4 shipping list widened to [48000, 96000]", SHIP, "FAIL", run(SHIP))
finally:
    tb.CONFIGS = dict(REAL_CONFIGS)

# --------------------------------------------------------------- pp_shadow
DECL = "static constexpr uint32_t AU_RATES_C[3] = {\n        48000u, 96000u, 192000u};"
assert SIM.count(DECL) == 1, "real declaration anchor moved"


def shadow_with(sim_text: str, configs=None) -> str:
    fake = Path(tempfile.mkdtemp(prefix="r222-root-", dir=tmpdir))
    (fake / "tb/verilator/pp_shadow").mkdir(parents=True)
    (fake / "tb/verilator/pp_shadow/sim_main.cpp").write_text(sim_text)
    tb.ROOT = fake
    if configs is not None:
        tb.CONFIGS = configs
    try:
        return run(SHADOW)
    finally:
        tb.ROOT, tb.CONFIGS = REAL_ROOT, dict(REAL_CONFIGS)


SHADOW_MUTANTS = [
    ("real sim_main.cpp unchanged (copied control)", SIM, None, "PASS"),
    ("real AU_RATES_C value 96000u -> 88200u",
     SIM.replace(DECL, DECL.replace("96000u", "88200u")), None, "FAIL"),
    ("real AU_RATES_C order 48000u,96000u swapped",
     SIM.replace(DECL, DECL.replace("48000u, 96000u", "96000u, 48000u")), None, "FAIL"),
    ("real AU_RATES_C declared length [3] -> [4] (implicit zero fill)",
     SIM.replace(DECL, DECL.replace("[3]", "[4]")), None, "FAIL"),
    ("real AU_RATES_C initializer shortened to two words",
     SIM.replace(DECL, DECL.replace(", 192000u", "")), None, "FAIL"),
    ("second AU_RATES_C declaration added",
     SIM.replace(DECL, DECL + "\n    " + DECL.replace("AU_RATES_C", "AU_RATES_C")), None, "FAIL"),
    ("real declaration commented out", SIM.replace(DECL, "/* " + DECL + " */"), None, "FAIL"),
    ("YAML arty_current list -> [48000, 96000], bench unchanged", SIM,
     dict(REAL_CONFIGS, arty_current=cfg_variant("arty_current", [48000, 96000])), "FAIL"),
    ("RESIDUAL: image count literal put16be_v(d, 142, 3) -> 4",
     SIM.replace("put16be_v(d, 142, 3);", "put16be_v(d, 142, 4);"), None, "PASS"),
    ("RESIDUAL: rate loop bound k < 3 -> k < 2",
     SIM.replace("for (size_t k = 0; k < 3; k++)", "for (size_t k = 0; k < 2; k++)"), None, "PASS"),
    ("RESIDUAL: AU_LEN_C 144 + 4 * 3 -> 144 + 4 * 2",
     SIM.replace("AU_LEN_C     = 144 + 4 * 3;", "AU_LEN_C     = 144 + 4 * 2;"), None, "PASS"),
    ("RESIDUAL: AU_CUR_RATE_C 48000u -> 96000u",
     SIM.replace("AU_CUR_RATE_C = 48000u;", "AU_CUR_RATE_C = 96000u;"), None, "PASS"),
]
for label, text, configs, expect in SHADOW_MUTANTS:
    if text is not SIM:
        assert text != SIM, f"mutation did not apply: {label}"
    row(label, SHADOW, expect, shadow_with(text, configs))

# co-updated YAML and AU_RATES_C, every other hand spelling of the count left at 3
co_yaml = dict(REAL_CONFIGS, arty_current=cfg_variant("arty_current", [48000, 96000]))
co_sim = SIM.replace(DECL, "static constexpr uint32_t AU_RATES_C[2] = {\n        48000u, 96000u};")
row("RESIDUAL: YAML and AU_RATES_C both shortened to 2, count literal/loop/AU_LEN_C left at 3",
    SHADOW, "PASS", shadow_with(co_sim, co_yaml))

print(f"\n{sum(rows)}/{len(rows)} rows matched their expectation")
sys.exit(0 if all(rows) else 1)
