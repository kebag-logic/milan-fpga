# R250-2 probe runbook

All probes run in disposable copies under `<PACKET>/scratch/` of a clean
checkout at `7463ab0889da9a95fce7c921e386d6035d69778e` (`scratch/probe`,
made with `cp -a` of the review clone, submodules at their gitlinks).
The review clone itself is never edited; `receipts/integrity-before.txt`
and `receipts/integrity-after.txt` are byte-identical.

Environment: pinned Verilator 5.050 (`receipts/verilator-identity.txt`),
reached through `scripts/vl-capped.sh`, which rewrites every `-j` value to
`$VL_JOBS` because the csr and pp_shadow recipes hard-code `--build -j 0`.
`scripts/mutant.py` applies one literal plant (must occur exactly once),
runs one command, restores the original bytes and re-hashes them.

| Step | Command (from `<PACKET>`, tree `scratch/probe` unless stated) | Receipt |
|---|---|---|
| declarations gate | `python3 sw/builder/test_declarations.py` | `head-declarations.log` |
| csr + pp_shadow | `make -C tb/verilator/{csr,pp_shadow}` | `head-csr.log`, `head-pp_shadow.log` |
| gate 35 alone | `python3 scripts/gate35.py` | `head-gate35.log` |
| firmware host test | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | `head-nvm-firmware.log` |
| round-2 control | same, with that file taken from `2d61e7ed` | `control-nvm-firmware-2d61e7ed.log` |
| builder/boot mutants | `scripts/mutant.py ... -- python3 sw/builder/test_declarations.py` or `-- python3 scripts/gate35.py` | `mutants-builder.log` |
| RTL mutants R1-R6 | `sh scripts/rtl_mutants.sh <PACKET> <PINNED_VERILATOR>` | `rtl-R1.log`, `rtl-R4.log`..`rtl-R6.log` |
| VID-73 legs R2/R3 | `sh scripts/rtl_vid73.sh <PACKET> <PINNED_VERILATOR>` | `rtl-R2.log`, `rtl-R3.log` |
| child-hop R7a-c, R8 | `scripts/mutant.py` on `KL_srp_top.sv:341` / `milan_datapath.sv` (commands in REPORT.md) | `rtl-R7a.log`..`rtl-R7c.log`, `rtl-R8.log` |
| timer override S1 | `scripts/mutant.py` adding `.LEAVE_MS_P (600)` at `u_srp` | `mutant-S1.log` |
| NxN 4x4 leg N0-N2 | `sh scripts/nxn_leg.sh <tree> <PACKET>` (exact `obj_nxn` line of `make -n run`) | `nxn-N0-head.log`, `nxn-N1.log`, `nxn-N2.log` |
| area base/head | `OOC_TMP=... bash syn/yosys/ooc.sh milan_csr KL_pp_shadow milan_datapath` with one added `milan_csr` list entry in both arms; base arm = `git checkout 864b36f5 -- .` in a copy | `ooc-base.log`, `ooc-head.log` |
| nvm_cosim | `make -C tb/verilator/nvm_cosim quick JOBS=2 POOL=2` at head and at base | `nvm_cosim-quick-head.log`, `nvm_cosim-quick-base.log` |
| nvm_cosim probe | same at head with the `run_cases.py:131` call given `fabric_constants(overlay, lwsrp)` (disposable, reverted) | `nvm_cosim-quick-head-adapted-probe.log` |
| model ids | `python3 scripts/model_ids.py <tree>` for base and head | `model-ids-base.txt`, `model-ids-head.txt` |
| docs gates | light gates listed in `head-doc-gates.log`; diagram `--check` | `head-doc-gates.log`, `head-diagram-check.log`, `head-emdash-scan.txt` |
| hosted (read only) | check runs and the shard 1/5 suite-log artifact at the exact head | `hosted-checks-7463ab08.txt`, `hosted-nvm_cosim-7463ab08.txt` |

`receipts/invocation-error/` keeps the first R2/R3 attempt, which failed on
an unquoted make argument (a runner error, not a measurement); the rerun
receipts replace it.
