Portable review tools (R826-3). Set R=<this packet>, C=<exact-head clone>, PY=<product LiteX venv python3>,
RV32_BIN=<pinned RV32 SDK bin>, VERILATOR_WRAPPER=<pinned Verilator 5.050 wrapper>, VERILATOR_ROOT=<its root>, then
run tools/run_all.sh (concurrent: test_ctrl_memory.py, region-decode self-test, guard_probe2.py, decode_arm.py).
noguard/sitecustomize.py on PYTHONPATH refuses any CPU generator command, so the shared netlist cache is never
written. decode_arm.py <tree> runs only the CPU decode arm. guard_probe2.py and hash_inputs.py are the previous
round's tools, unchanged. Controls: <tree> = a git-archive copy of 596e2ae3, and of the head with the one line
`named.append(list(VexiiRiscv.memory_regions))` reverted to `named.append(VexiiRiscv.memory_regions)`
(receipts/reverted-control.diff), each with the submodules linked from the clone.
