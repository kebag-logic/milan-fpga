"""Component maxima over the cited elaborate runs with run 41678609075 attempt 3, and what the ruling's rule then implies (#737 round 3)."""
from itertools import product

# Member verdict rows in a LiteX leg on a worker of its own (receipts of 41583428850; job logs of 41678609075 a1 and a3).
rows = {
    "41583428850": {"test_cpu_memory_port_cdc": 70, "test_ctrl_memory": 280, "test_gmii_rx_capture": 0,
                    "test_gptp_tx_timestamp": 461, "test_pp_boot_bus_freeze": 25, "test_pp_mem_bridge": 14,
                    "test_retained_cdc_storage": 331, "test_soc_timing_cuts": 240},
    "41678609075 a1": {"test_cpu_memory_port_cdc": 72, "test_ctrl_memory": 224, "test_gmii_rx_capture": 0,
                       "test_gptp_tx_timestamp": 246, "test_pp_boot_bus_freeze": 25, "test_pp_mem_bridge": 15,
                       "test_retained_cdc_storage": 336, "test_soc_timing_cuts": 369},
    "41678609075 a3": {"test_cpu_memory_port_cdc": 71, "test_ctrl_memory": 284, "test_gmii_rx_capture": 0,
                       "test_gptp_tx_timestamp": 462, "test_pp_boot_bus_freeze": 25, "test_pp_mem_bridge": 14,
                       "test_retained_cdc_storage": 333, "test_soc_timing_cuts": 510},
}
largest = {name: max(run[name] for run in rows.values()) for name in rows["41583428850"]}
print("member largest:", largest)
setups = {"a1 max (worker 0)": 255, "a3 gates-0": 362, "a3 gates-1": 399, "a3 gates-2": 442, "a3 gates-3": 485,
          "a3 gates-4": 398}
setup = max(setups.values())
verilator, selftest, allowance = 431, 3, 338
leg0, leg1 = 1130, 1119
budget = 1800 - allowance - setup - verilator - selftest
print("setup", setup, "LEG_BUDGET", budget)
current = [["test_gptp_tx_timestamp"],
           ["test_cpu_memory_port_cdc", "test_gmii_rx_capture", "test_pp_boot_bus_freeze", "test_pp_mem_bridge",
            "test_retained_cdc_storage"], ["test_ctrl_memory", "test_soc_timing_cuts"]]
print("current legs at largest:", [sum(largest[n] for n in leg) for leg in current])
names = list(largest)
best = min(max(sum(largest[n] for n, leg in zip(names, assign) if leg == k) for k in range(3))
           for assign in product(range(3), repeat=len(names)))
print("best possible three-leg partition, fullest leg:", best, "fits" if best <= budget else "does not fit")
best4 = min(max(sum(largest[n] for n, leg in zip(names, assign) if leg == k) for k in range(4))
            for assign in product(range(4), repeat=len(names)))
print("best possible four-leg partition, fullest leg:", best4, "fits" if best4 <= budget else "does not fit")
print("worker 0 projection", setup + leg0, "worker 1", setup + leg1, "workflow", setup + leg0 + allowance,
      "with the former 270 allowance", setup + leg0 + 270)
