#!/usr/bin/env python3
"""Re-run the three erased-prefix mutations in disposable source copies."""
import pathlib, sys
root=pathlib.Path.cwd();packet=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/"sw/firmware/ctrl_nvm/test"))
import nvm_bench, nvm_mutants, fw_gtest
work=packet/"scratch/prefix-probes";work.mkdir(parents=True,exist_ok=True)
inputs=nvm_bench.shape_inputs(root/"configs/endstation_ax7101_1x1_tdm8.yaml",work/"inputs")
binary=next(b for b in nvm_bench.UNITS if b.name=="prefix")
build=fw_gtest.Build(jobs=2)
selected=[m for m in nvm_mutants.MUTANTS if m.name.startswith("erased_payload_")]
assert len(selected)==3
for m in selected:
 tree=work/m.name/"tree";nvm_mutants.plant(m,tree)
 exe=nvm_bench.build_suite(inputs,work/m.name/"build",build,binary,tree)
 passed,log=nvm_bench.run_suite(exe,work,["codec_erased_loaded_prefix"])
 (packet/"receipts"/(m.name+".log")).write_text(log)
 assert not passed and not nvm_mutants.survivors(m,log),m.name
 if m.name=="erased_payload_end_bound":assert "AddressSanitizer: heap-buffer-overflow" in log
 print("CAUGHT",m.name,flush=True)
print("PASS: 3/3 erased payload defects caught at candidate")
