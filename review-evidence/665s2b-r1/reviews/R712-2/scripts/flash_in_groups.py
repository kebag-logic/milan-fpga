"""Per group: flash loads (count/cycles/min/max), the store's and the flash port's cycles, and the longest work pass.

Usage: python3 -I flash_in_groups.py <results-root> <label>...
"""
import json
import sys

root = sys.argv[1]
for label in sys.argv[2:]:
    d = json.load(open(f"{root}/{label}/results.json"))
    print(f"== {label}")
    for r in d["results"]:
        s = r["summary"]
        m = r["modules"]
        w = r["passes"]["worst"]
        print(f"   {r['group']:20s} load_flash={s.get('load_flash'):24s} nvm_store={m.get('nvm_store', 0):8d} "
              f"litespi={m.get('nvm_flash_litespi', 0):8d} klj2={m.get('nvm_klj2', 0):8d} worst={w['ms']:.3f} ms "
              f"(worst-pass nvm_store={w['modules'].get('nvm_store', 0)}, litespi={w['modules'].get('nvm_flash_litespi', 0)})")
