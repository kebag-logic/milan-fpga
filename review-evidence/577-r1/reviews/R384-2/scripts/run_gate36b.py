#!/usr/bin/env python3
"""Run only builder gates 36a/36b (every registered gate-36 function) from a
given checkout root.  Usage: run_gate36b.py <checkout-root>
"""
import sys, os
root = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(root, "sw", "builder"))
os.chdir(root)
import test_builder as tb
names = ["test_audio_unit_rates_loader_contract", "test_audio_unit_shipping_rates",
         "test_shipping_image_contract", "test_shipping_image_contract_index_walk",
         "test_soc_shipping_image_contract", "test_shipping_image_contract_presence"]
for n in names:
    fn = getattr(tb, n)
    print(f"{n}:", flush=True)
    fn()
print("GATE36B-FOCUSED OK")
