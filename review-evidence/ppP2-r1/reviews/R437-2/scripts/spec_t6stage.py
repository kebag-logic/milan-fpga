# Attribution probe: only T6's poke is re-staged (TMO / 10 cycles after the accept,
# inside the ERASE's completion wait at every bound), the port untouched.
PROBES = {"T6_restaged": [("SIM",
    "  for (int i = 0; i < kStageCycles; ++i) h.tick();\n  CHECK(dut->nvm_busy_o, \"T6 op still in flight at the poke\");",
    "  for (int i = 0; i < TMO / 10; ++i) h.tick();\n  CHECK(dut->nvm_busy_o, \"T6 op still in flight at the poke\");")]}
RUNS = [("T6_restaged", m, t) for t in (37, 100, 500, 1000, 100000)
        for m in ("pristine", "coincident completion", "unsolicited completion")]
