#!/usr/bin/env python3
"""R357-1 reviewer mutants for the #571 unit-count checks.

Usage: probe_binding_mutants.py <tree-root>

Independent of the author's self-test mutants. Each RTL mutant edits the
datapath or KL_pp_shadow text IN MEMORY and calls the gate's
check_unit_bindings; each header mutant edits a generated header text and
calls check_unit_header against the builder's own census. A mutant is
KILLED when the gate records a failure naming the expected parameter or
symbol. The baseline (unmutated) must pass. Writes nothing in the tree.
"""
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
sys.path.insert(0, str(root / "sw/builder"))
import check_entity_shape as G  # noqa: E402
spec = importlib.util.spec_from_file_location(
    "endstation_builder", root / "sw/builder/endstation_builder.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

DP = G.read_text(G.RTL.datapath)
SH = G.read_text(G.PP_SHADOW)
T = G.TALLY


def run(fn):
    saved = T.fails, T.checks, T.quiet
    T.fails, T.checks, T.quiet = [], 0, True
    try:
        fn()
    except Exception as exc:  # noqa: BLE001
        T.fails.append(f"EXC {type(exc).__name__}: {exc}")
    fails = T.fails
    T.fails, T.checks, T.quiet = saved
    return fails


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"SETUP {label}: {old!r} occurs {n} times")
    return text.replace(old, new)


# (label, hop-file, [(old, new), ...], token the rejection must name)
DP_AU = "      .N_AUDIO_UNIT_P      (AEM_N_AUDIO_UNIT_C),\n"
DP_CD = "      .N_CLK_DOM_P         (AEM_N_CLKDOM_C),\n"
DP_CT = "      .N_CONTROL_P         (AEM_N_CONTROL_C)\n"
SH_AU = "      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),\n"
SH_CD = "      .N_CLK_DOMAIN_P (N_CLK_DOM_P),\n"
SH_CT = "      .N_CONTROL_P    (N_CONTROL_P),\n"
RTL_MUTANTS = [
    # hop 0: milan_datapath -> KL_pp_shadow
    ("h0 CONTROL unbound (last entry, comma fixed)", "dp",
     [(DP_CD + "      //! IDENTIFY CONTROL rows in the processor use that same census.\n"
       + DP_CT, DP_CD.replace("),\n", ")\n"))], ".N_CONTROL_P derives"),
    ("h0 AUDIO_UNIT unbound", "dp", [(DP_AU, "")], ".N_AUDIO_UNIT_P derives"),
    ("h0 CLK_DOM literal 1", "dp", [(DP_CD, "      .N_CLK_DOM_P (1),\n")],
     ".N_CLK_DOM_P derives"),
    ("h0 CONTROL literal 32'd1", "dp",
     [(DP_CT, "      .N_CONTROL_P (32'd1)\n")], ".N_CONTROL_P derives"),
    ("h0 CONTROL bound to wrong generated constant AEM_NAME_ENTRIES_C", "dp",
     [(DP_CT, "      .N_CONTROL_P (AEM_NAME_ENTRIES_C)\n")], ".N_CONTROL_P derives"),
    ("h0 CONTROL expression AEM_N_CONTROL_C*0+1", "dp",
     [(DP_CT, "      .N_CONTROL_P (AEM_N_CONTROL_C*0+1)\n")], ".N_CONTROL_P derives"),
    ("h0 swap CONTROL/CLK_DOM", "dp",
     [(DP_CD, "      .N_CLK_DOM_P (AEM_N_CONTROL_C),\n"),
      (DP_CT, "      .N_CONTROL_P (AEM_N_CLKDOM_C)\n")],
     (".N_CLK_DOM_P derives", ".N_CONTROL_P derives")),
    ("h0 one-sided CONTROL<-AEM_N_AUDIO_UNIT_C", "dp",
     [(DP_CT, "      .N_CONTROL_P (AEM_N_AUDIO_UNIT_C)\n")], ".N_CONTROL_P derives"),
    ("h0 CONTROL bound only inside a comment", "dp",
     [(DP_CT, "      // .N_CONTROL_P (AEM_N_CONTROL_C)\n"),
      (DP_CD, DP_CD.replace("),\n", ")\n"))], ".N_CONTROL_P derives"),
    ("h0 duplicate CONTROL binding", "dp",
     [(DP_CD, DP_CD + "      .N_CONTROL_P (1),\n")], ".N_CONTROL_P derives"),
    # hop 1: KL_pp_shadow -> protocol_processor_top u_pp
    ("h1 CLK_DOMAIN unbound", "sh", [(SH_CD, "")], ".N_CLK_DOMAIN_P derives"),
    ("h1 all three unbound (base shape)", "sh",
     [(SH_AU, ""), (SH_CD, ""), (SH_CT, "")],
     (".N_AUDIO_UNIT_P derives", ".N_CLK_DOMAIN_P derives", ".N_CONTROL_P derives")),
    ("h1 AUDIO_UNIT literal 1", "sh",
     [(SH_AU, "      .N_AUDIO_UNIT_P (1),\n")], ".N_AUDIO_UNIT_P derives"),
    ("h1 CONTROL literal 1", "sh",
     [(SH_CT, "      .N_CONTROL_P    (1),\n")], ".N_CONTROL_P derives"),
    ("h1 swap AUDIO_UNIT/CONTROL", "sh",
     [(SH_AU, "      .N_AUDIO_UNIT_P (N_CONTROL_P),\n"),
      (SH_CT, "      .N_CONTROL_P    (N_AUDIO_UNIT_P),\n")],
     (".N_AUDIO_UNIT_P derives", ".N_CONTROL_P derives")),
    ("h1 CLK_DOMAIN bound to N_AUDIO_UNIT_P (one-sided)", "sh",
     [(SH_CD, "      .N_CLK_DOMAIN_P (N_AUDIO_UNIT_P),\n")], ".N_CLK_DOMAIN_P derives"),
    ("h1 CLK_DOMAIN bound to processor-side name N_CLK_DOMAIN_P", "sh",
     [(SH_CD, "      .N_CLK_DOMAIN_P (N_CLK_DOMAIN_P),\n")], ".N_CLK_DOMAIN_P derives"),
    ("h1 CONTROL moved from u_pp to u_nvm map", "sh",
     [(SH_CT, ""), ("      .N_CLK_DOM_P     (N_CLK_DOM_P),\n",
                    "      .N_CLK_DOM_P     (N_CLK_DOM_P),\n      .N_CONTROL_P (N_CONTROL_P),\n")],
     ".N_CONTROL_P derives"),
    ("h1 AUDIO_UNIT bound through a local alias", "sh",
     [(SH_AU, "      .N_AUDIO_UNIT_P (PP_AU_C),\n")], ".N_AUDIO_UNIT_P derives"),
]

HDR = B.emit_adp_shape_svh(B.load_config(str(root / "configs/endstation_ax7101_8x8.yaml")))
CENSUS = dict(AUDIO_UNIT=1, CLOCK_DOMAIN=1, CONTROL=1)
H_CT = "  localparam int AEM_N_CONTROL_C    = 1;\n"
HDR_MUTANTS = [
    ("hdr CONTROL line removed", [(H_CT, "")], "AEM_N_CONTROL_C == CONTROL"),
    ("hdr CONTROL zero", [(H_CT, H_CT.replace("= 1", "= 0"))], "AEM_N_CONTROL_C == CONTROL"),
    ("hdr CONTROL two", [(H_CT, H_CT.replace("= 1", "= 2"))], "AEM_N_CONTROL_C == CONTROL"),
    ("hdr CONTROL duplicated", [(H_CT, H_CT + H_CT)], "AEM_N_CONTROL_C == CONTROL"),
    ("hdr CLKDOM zero", [("AEM_N_CLKDOM_C     = 1;", "AEM_N_CLKDOM_C     = 0;")],
     "AEM_N_CLKDOM_C == CLOCK_DOMAIN"),
]

results = []
base = run(lambda: G.check_unit_bindings(DP, SH))
results.append(("baseline RTL (must PASS)", not base, base))
base_h = run(lambda: G.check_unit_header(HDR, CENSUS, "baseline"))
results.append(("baseline header (must PASS)", not base_h, base_h))
killed = total = 0
for label, which, edits, need in RTL_MUTANTS:
    dp, sh = DP, SH
    for old, new in edits:
        if which == "dp":
            dp = sub(dp, old, new, label)
        else:
            sh = sub(sh, old, new, label)
    fails = run(lambda: G.check_unit_bindings(dp, sh))
    need = (need,) if isinstance(need, str) else need
    ok = bool(fails) and all(any(n in f for f in fails) for n in need)
    total += 1
    killed += ok
    results.append((f"MUTANT {label}", ok, fails))
for label, edits, need in HDR_MUTANTS:
    h = HDR
    for old, new in edits:
        h = sub(h, old, new, label)
    fails = run(lambda: G.check_unit_header(h, CENSUS, "mutant"))
    ok = bool(fails) and any(need in f for f in fails)
    total += 1
    killed += ok
    results.append((f"MUTANT {label}", ok, fails))

for label, ok, fails in results:
    print(f"{'KILLED/OK' if ok else 'SURVIVED/BAD'}: {label}")
    for f in fails[:3]:
        print(f"      {f}")
print(f"reviewer mutants killed: {killed}/{total}")
sys.exit(0 if killed == total and all(r[1] for r in results[:2]) else 1)
