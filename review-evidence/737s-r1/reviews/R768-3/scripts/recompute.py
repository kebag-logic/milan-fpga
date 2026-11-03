"""Recompute LEG_BUDGET, every elaborate projection and the workflow figure by the
re-measurement rule in docs/testing/CI_WORKFLOWS.md, at the stated figures and with
the exact-head run 41705989293 (attempts 1 and 2) folded in. Pure arithmetic."""
LEGS = (("test_gptp_tx_timestamp",),
        ("test_cpu_memory_port_cdc", "test_gmii_rx_capture", "test_pp_boot_bus_freeze", "test_pp_mem_bridge",
         "test_retained_cdc_storage"),
        ("test_ctrl_memory", "test_soc_timing_cuts"))
STATED = dict(setup=485, verilator=431, selftest=3, leg0=1130, leg1=1119, agg=19 + 85, collector=149, tail=25,
              largest={"test_cpu_memory_port_cdc": 72, "test_ctrl_memory": 284, "test_gmii_rx_capture": 0,
                       "test_gptp_tx_timestamp": 462, "test_pp_boot_bus_freeze": 25, "test_pp_mem_bridge": 15,
                       "test_retained_cdc_storage": 336, "test_soc_timing_cuts": 510})
# Exact-head maxima: setup 739 (gates-1, a2), Verilator 393, builder legs 1098/737, aggregate 3+18/15+14,
# collector 183, tail 29; member rows a1 (logs) and a2 (leg receipts).
HEAD = dict(setup=739, verilator=393, leg0=1098, leg1=737, agg_checkout=15, agg_rest=18, collector=183, tail=29,
            rows={"test_gptp_tx_timestamp": 477, "test_cpu_memory_port_cdc": 70, "test_gmii_rx_capture": 0,
                  "test_pp_boot_bus_freeze": 25, "test_pp_mem_bridge": 14, "test_retained_cdc_storage": 331,
                  "test_ctrl_memory": 277, "test_soc_timing_cuts": 472})


def figures(f):
    budget = 2700 - 600 - f["setup"] - f["verilator"] - f["selftest"]
    held = [sum(f["largest"][n] for n in leg) for leg in LEGS]
    builders = [f["setup"] + f["leg0"], f["setup"] + f["leg1"]]
    cold = [f["setup"] + f["verilator"] + f["selftest"] + h for h in held]
    warm = [f["setup"] + f["selftest"] + h for h in held]
    allowance = f["agg"] + f["collector"] + 120 + f["tail"]
    return dict(LEG_BUDGET=budget, legs_at_largest=held, fits=max(held) <= budget, builders=builders,
                builder_margins=[2700 - b for b in builders], litex_cold=cold, litex_cold_margins=[2700 - c for c in cold],
                litex_restored=warm, allowance=allowance, workflow_restored=max(builders + warm) + allowance,
                workflow_cold=max(builders + cold) + allowance, min_margin=2700 - max(builders + cold))


print("stated:", figures(STATED))
merged = dict(STATED)
for key in ("setup", "verilator", "leg0", "leg1", "collector", "tail"):
    merged[key] = max(STATED[key], HEAD[key])
merged["agg"] = max(19, HEAD["agg_checkout"]) + max(85, HEAD["agg_rest"])
merged["largest"] = {n: max(v, HEAD["rows"][n]) for n, v in STATED["largest"].items()}
print("with exact-head run:", figures(merged))
print("components above stated:", {k: (STATED[k], merged[k]) for k in ("setup", "collector", "tail") if merged[k] > STATED[k]},
      {n: (STATED["largest"][n], merged["largest"][n]) for n in merged["largest"] if merged["largest"][n] > STATED["largest"][n]})
print("measured worker spans vs stated projection: gates-2 a1 1414 vs 1381 cold (exceeded by 33)")
