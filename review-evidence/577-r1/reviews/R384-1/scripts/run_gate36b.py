#!/usr/bin/env python3
"""Run only builder gate 36b (and 36a neighbours) from a given checkout root.

Usage: run_gate36b.py <checkout-root>
"""
import sys, os
root = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(root, "sw", "builder"))
os.chdir(root)
import test_builder as tb
fns = [tb.test_audio_unit_rates_loader_contract, tb.test_audio_unit_shipping_rates,
       tb.test_shipping_image_contract, tb.test_shipping_image_contract_index_walk]
for fn in fns:
    print(f"{fn.__name__}:", flush=True)
    fn()
print("GATE36B-FOCUSED OK")
