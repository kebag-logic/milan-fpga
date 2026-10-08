#!/usr/bin/env python3
"""R548-3 integration seed probe: patch a DISPOSABLE copy of the tree.

Usage: seed_probe_patch.py <tree> [--mutant-mac-at-reset]

Adds a read-only public on KL_maap.lfsr_r to the crflic leg's .vlt and a
shadow LFSR to tb/verilator/milan_dp/sim_crf_licence.cpp. The shadow loads
0xACE1 on every axis_clk edge with axis_resetn low and steps the
x^16+x^15+x^13+x^4+1 Fibonacci step otherwise; every edge it must equal the
real milan_datapath's g_maap.maap_engine.lfsr_r. A counterfactual shadow
seeded from the harness's programmed MAC (02:00:00:00:00:01 -> seed 0xACE0)
must differ. --mutant-mac-at-reset makes milan_csr reset MAC_ADDR_LO/HI to
that MAC (a planted "MAC known at reset" integration), which the probe must
catch (PROBE-FAIL).
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
mutant = "--mutant-mac-at-reset" in sys.argv[2:]

vlt = tree / "tb/verilator/milan_dp/crflic_probes.vlt"
vlt.write_text(vlt.read_text() +
               'public_flat_rd -module "KL_maap" -var "lfsr_r"\n')

cpp = tree / "tb/verilator/milan_dp/sim_crf_licence.cpp"
s = cpp.read_text()

hi_old = ("void CrfLicenceHarness::hi() {\n"
          "    dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1;\n"
          "    dut->eval();\n")
assert s.count(hi_old) == 1, "hi() anchor"
hi_new = (
    "static uint16_t r548_step(uint16_t l) {\n"
    "    return static_cast<uint16_t>((l << 1) | (((l >> 15) ^ (l >> 14) ^ (l >> 12) ^ (l >> 3)) & 1u));\n"
    "}\n"
    "static uint16_t r548_sh = 0, r548_cf = 0;\n"
    "static uint64_t r548_edges = 0, r548_mism = 0, r548_cf_eq = 0, r548_post = 0;\n"
    "static bool r548_armed = false;\n"
    "void CrfLicenceHarness::hi() {\n"
    "    const bool r548_rst = !dut->axis_resetn;\n"
    "    dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1;\n"
    "    dut->eval();\n"
    "    if (r548_rst) { r548_sh = 0xACE1u; r548_cf = 0xACE0u; r548_armed = true; }\n"
    "    else if (r548_armed) { r548_sh = r548_step(r548_sh); r548_cf = r548_step(r548_cf); r548_post++; }\n"
    "    if (r548_armed) {\n"
    "        r548_edges++;\n"
    "        const uint16_t real = dut->rootp->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r;\n"
    "        if (real != r548_sh) { if (r548_mism < 4) printf(\"R548-PROBE mismatch edge %llu real %04x shadow %04x\\n\", (unsigned long long)r548_edges, real, r548_sh); r548_mism++; }\n"
    "        if (!r548_rst && real == r548_cf) r548_cf_eq++;\n"
    "    }\n")
s = s.replace(hi_old, hi_new)

main_old = ("    CrfLicenceHarness harness;\n"
            "    // The former --unwarmed-refusal opt-in is now unconditional.\n"
            "    return harness.run();\n")
assert s.count(main_old) == 1, "main anchor"
main_new = (
    "    CrfLicenceHarness harness;\n"
    "    // The former --unwarmed-refusal opt-in is now unconditional.\n"
    "    const int rc = harness.run();\n"
    "    const bool ok = r548_armed && r548_post > 1000 && r548_mism == 0 && r548_cf_eq == 0;\n"
    "    printf(\"R548-PROBE %s: edges %llu post-reset %llu mismatches %llu counterfactual-equal %llu harness-rc %d\\n\",\n"
    "           ok ? \"PASS\" : \"FAIL\", (unsigned long long)r548_edges, (unsigned long long)r548_post,\n"
    "           (unsigned long long)r548_mism, (unsigned long long)r548_cf_eq, rc);\n"
    "    return ok ? rc : 3;\n")
s = s.replace(main_old, main_new)
cpp.write_text(s)

if mutant:
    csr = tree / "hdl/common/csr/milan_csr.sv"
    c = csr.read_text()
    old = "mac_alo <= 32'h0; mac_ahi <= 32'h0;"
    assert c.count(old) == 1, "csr anchor"
    csr.write_text(c.replace(old, "mac_alo <= 32'h2; mac_ahi <= 32'h100;"))
print("patched", tree, "mutant" if mutant else "clean")
