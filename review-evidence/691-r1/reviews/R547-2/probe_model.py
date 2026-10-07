#!/usr/bin/env python3
"""Compare both generated artifacts as bytes; refuse the exact prior artifacts."""
import importlib.util, json, pathlib, subprocess, sys
repo, packet=map(pathlib.Path,sys.argv[1:3])
sys.path.insert(0,str(repo/"sw/litex"))
import gen_mac_tx_model as model
assert model.HAVE_LITEX, "strong conversion unavailable"
fresh_v, fresh_m=model.generate()
assert fresh_v.encode()==model.OUT_V.read_bytes()
assert (json.dumps(fresh_m,indent=2,sort_keys=True)+"\n").encode()==model.OUT_MANIFEST.read_bytes()
print("Fresh Verilog AND serialized manifest are byte-identical")
control=packet/"scratch/old-model"; control.mkdir(exist_ok=True)
for attr, name in (("OUT_V","mac_tx_chain.v"),("OUT_MANIFEST","manifest.json")):
    target=control/name
    target.write_bytes(subprocess.check_output(["git","show","35fb2a95:tb/verilator/gptp_txts/generated/"+name],cwd=repo))
    setattr(model,attr,target)
assert model.check()==1, "stale model escaped strong check"
print("Exact 35fb2a95 model and manifest refused by strong check")
