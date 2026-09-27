#!/usr/bin/env python3
"""R356-1 reviewer-owned mutants against the #571 binding/header checks.

Independent of the author's self-test mutants. Every mutant is applied in
memory to the exact-head sources; nothing on disk is modified. For each one
the expected verdict (KILL = the gate must reject, PASS = an equivalent
rewrite the gate must accept) is compared with what the gate actually did.
Usage: probe_gate_mutants.py <repo root at the exact head>
"""
import re
import sys
import types
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "scripts"))
import check_entity_shape as gate  # noqa: E402

DP = gate.read_text(gate.RTL.datapath)
SH = gate.read_text(gate.PP_SHADOW)
RESULTS = []


def run(fn):
    t = gate.TALLY
    saved = (t.fails, t.checks, t.quiet)
    t.fails, t.checks, t.quiet = [], 0, True
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        t.fails.append(f"{type(e).__name__}: {e}")
    fails = list(t.fails)
    t.fails, t.checks, t.quiet = saved
    return fails


def sub1(text, old, new):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"SETUP: {old!r} occurs {n} times")
    return text.replace(old, new)


def record(mid, desc, expect, fails):
    got = "KILL" if fails else "PASS"
    ok = got == expect
    RESULTS.append(ok)
    why = fails[0][:110] if fails else ""
    print(f"{'OK ' if ok else 'BAD'} {mid:6} expect={expect:4} got={got:4} {desc}"
          + (f"\n        reason: {why}" if why else ""))


def bind(mid, desc, dp=DP, sh=SH, expect="KILL"):
    record(mid, desc, expect, run(lambda: gate.check_unit_bindings(dp, sh)))


# ---- baseline: the real sources must pass -----------------------------------
bind("B0", "exact-head sources", expect="PASS")

# ---- hop 0: milan_datapath -> KL_pp_shadow (pp_shadow) ------------------------
CTL0 = ".N_CONTROL_P         (AEM_N_CONTROL_C)"
AU0 = ".N_AUDIO_UNIT_P      (AEM_N_AUDIO_UNIT_C)"
CD0 = ".N_CLK_DOM_P         (AEM_N_CLKDOM_C)"
bind("H0-a", "CONTROL bound to the CLOCK_DOMAIN symbol (wrong symbol, no swap)",
     dp=sub1(DP, CTL0, ".N_CONTROL_P (AEM_N_CLKDOM_C)"))
bind("H0-b", "AUDIO_UNIT bound to sized literal 32'd1",
     dp=sub1(DP, AU0, ".N_AUDIO_UNIT_P (32'd1)"))
rot = sub1(sub1(sub1(DP, AU0, ".N_AUDIO_UNIT_P (@CD@)"), CD0, ".N_CLK_DOM_P (@CT@)"),
           CTL0, ".N_CONTROL_P (@AU@)")
rot = rot.replace("@CD@", "AEM_N_CLKDOM_C").replace("@CT@", "AEM_N_CONTROL_C") \
         .replace("@AU@", "AEM_N_AUDIO_UNIT_C")
bind("H0-c", "three-way rotation of the three values", dp=rot)
bind("H0-d", "CONTROL binding commented out (line comment), comma removed",
     dp=sub1(sub1(DP, "(AEM_N_CLKDOM_C),", "(AEM_N_CLKDOM_C)"), CTL0, "// " + CTL0))
bind("H0-e", "CONTROL bound through a local alias localparam",
     dp=sub1(DP, CTL0, ".N_CONTROL_P (PP_N_CTL_C)"))
bind("H0-f", "ifdef-guarded alternate literal CONTROL binding",
     dp=sub1(DP, CTL0, "`ifdef R356_ALT\n .N_CONTROL_P (1)\n`else\n " + CTL0 + "\n`endif"))
bind("H0-g", "CONTROL and CLOCK_DOMAIN both fed AEM_N_CLKDOM_C (duplicate value)",
     dp=sub1(DP, CTL0, ".N_CONTROL_P (AEM_N_CLKDOM_C)"))
bind("H0-h", "pp_shadow instance renamed (map no longer found)",
     dp=sub1(DP, ") pp_shadow (", ") pp_shadow_x ("))
bind("H0-i", "block comment inside the value (equivalent rewrite)",
     dp=sub1(DP, CTL0, ".N_CONTROL_P ( /* same census */ AEM_N_CONTROL_C )"), expect="PASS")
bind("H0-j", "value on its own line (equivalent rewrite)",
     dp=sub1(DP, CTL0, ".N_CONTROL_P(\n        AEM_N_CONTROL_C\n      )"), expect="PASS")

# ---- hop 1: KL_pp_shadow -> protocol_processor_top (u_pp) ---------------------
CTL1 = ".N_CONTROL_P    (N_CONTROL_P)"
AU1 = ".N_AUDIO_UNIT_P (N_AUDIO_UNIT_P)"
CD1 = ".N_CLK_DOMAIN_P (N_CLK_DOM_P)"
bind("H1-a", "u_pp CONTROL bound to N_AUDIO_UNIT_P (wrong symbol, no swap)",
     sh=sub1(SH, CTL1, ".N_CONTROL_P (N_AUDIO_UNIT_P)"))
bind("H1-b", "u_pp AUDIO_UNIT bound to sized literal 32'd1",
     sh=sub1(SH, AU1, ".N_AUDIO_UNIT_P (32'd1)"))
bind("H1-c", "u_pp CLOCK_DOMAIN unbound via block comment",
     sh=sub1(SH, CD1 + ",", "/* " + CD1 + ", */"))
rot1 = sub1(sub1(sub1(SH, AU1, ".N_AUDIO_UNIT_P (@CD@)"), CD1, ".N_CLK_DOMAIN_P (@CT@)"),
            CTL1, ".N_CONTROL_P (@AU@)")
rot1 = rot1.replace("@CD@", "N_CLK_DOM_P").replace("@CT@", "N_CONTROL_P") \
           .replace("@AU@", "N_AUDIO_UNIT_P")
bind("H1-d", "u_pp three-way rotation", sh=rot1)
bind("H1-e", "u_pp CLOCK_DOMAIN bound to a same-named but undeclared N_CLK_DOMAIN_P",
     sh=sub1(SH, CD1, ".N_CLK_DOMAIN_P (N_CLK_DOMAIN_P)"))
bind("H1-f", "u_pp instance renamed (map no longer found)",
     sh=sub1(SH, ") u_pp (", ") u_pp_x ("))
bind("H1-g", "u_pp CONTROL bound to an arithmetic expression N_CONTROL_P - 1",
     sh=sub1(SH, CTL1, ".N_CONTROL_P (N_CONTROL_P - 1)"))
bind("H1-h", "u_pp all three unbound together",
     sh=sub1(SH, "      " + AU1 + ",\n      " + CD1 + ",\n      " + CTL1 + ",\n", ""))
bind("H1-i", "u_pp value wrapped over lines (equivalent rewrite)",
     sh=sub1(SH, CTL1, ".N_CONTROL_P (\n        N_CONTROL_P)"), expect="PASS")

# ---- header derivation: builder emitter mutants ------------------------------
BSRC = (ROOT / "sw/builder/endstation_builder.py").read_text()
EMIT = "a(f\"  localparam int AEM_N_CONTROL_C    = {int(dc['CONTROL'])};\")"


def mutant_builder(src):
    mod = types.ModuleType("endstation_builder")
    mod.__file__ = str(ROOT / "sw/builder/endstation_builder.py")
    sys.modules["endstation_builder"] = mod
    sys.path.insert(0, str(ROOT / "sw/builder"))
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


real_builder = gate.load_builder()
cfg_path = ROOT / "configs/endstation_ax7101_8x8.yaml"
emitters = {
    "E-a": ("emitter cross-wired: CONTROL line reads CLOCK_DOMAIN",
            sub1(BSRC, EMIT, EMIT.replace("dc['CONTROL']", "dc['CLOCK_DOMAIN']"))),
    "E-b": ("emitter literal: CONTROL line hard-codes 1",
            sub1(BSRC, EMIT, EMIT.replace("{int(dc['CONTROL'])}", "1"))),
    "E-c": ("emitter omits the CONTROL line", sub1(BSRC, EMIT, "pass")),
    "E-d": ("census literal CONTROL: 2 in _overlay_document",
            sub1(BSRC, '"CLOCK_DOMAIN": 1, "CONTROL": 1,',
                 '"CLOCK_DOMAIN": 1, "CONTROL": 2,')),
    "E-e": ("emitter cross-wired: AUDIO_UNIT line reads CLOCK_DOMAIN",
            sub1(BSRC, "dc.get('AUDIO_UNIT', 0)", "dc.get('CLOCK_DOMAIN', 0)")),
}
import entity_shape_selftest as st  # noqa: E402
for mid, (desc, src) in emitters.items():
    b = mutant_builder(src)
    # (1) the ordinary gate arm over a shipping config (counts all equal 1)
    shipping = run(lambda: gate.check_config(b, cfg_path))
    # (2) the self-test's distinct-census oracle, as CI runs it (--self-test)
    distinct = run(lambda: st._prove_unit_counts(b, cfg_path))
    record(mid + "/g", desc + " -- ordinary gate, shipping 8x8",
           "KILL" if mid in ("E-c", "E-d") else "PASS", shipping)
    record(mid + "/s", desc + " -- self-test distinct-census oracle",
           "PASS" if mid == "E-d" else "KILL", distinct)
sys.modules["endstation_builder"] = real_builder

# ---- ROM side: descriptor constructor drops the IDENTIFY CONTROL -------------
sys.path.insert(0, str(ROOT / "avdecc"))
import aem_assemble  # noqa: E402
orig = aem_assemble._entity_descriptors


def no_control(spec):
    return [d for d in orig(spec) if d[0] != aem_assemble.CONTROL]


aem_assemble._entity_descriptors = no_control
record("R-a", "aem_assemble emits no CONTROL descriptor -- ordinary gate", "KILL",
       run(lambda: gate.check_config(real_builder, cfg_path)))
aem_assemble._entity_descriptors = orig
record("R-0", "restored constructor -- ordinary gate", "PASS",
       run(lambda: gate.check_config(real_builder, cfg_path)))

print(f"\nreviewer mutants: {len(RESULTS)} verdicts, "
      f"{sum(RESULTS)} as expected, {len(RESULTS) - sum(RESULTS)} unexpected")
sys.exit(0 if all(RESULTS) else 1)
