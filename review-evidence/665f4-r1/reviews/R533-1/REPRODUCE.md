R533-1 reproduction

Run from the candidate repository at the report's exact head. Initialize the four required submodules at their gitlinks. The scripts accept a repository path; all generated files stay in the packet's scratch directory. Set `MILAN_RV32_CC` to the verified RV32 compiler and `REVIEW_VERILATOR` to the scoped 5.050 executable. The review used the pinned SDK described by the PR; source-and-build-identity.log records the actual identities. Host test dependencies, Python YAML, C/C++ compilation, CMake and the behavior runner must be available. No shared installation is performed.

In the commands below, `review_packet` is this packet directory and `review_repo` is the exact-head isolated checkout. Export `TMPDIR="$review_packet/scratch"` and `PYTHONDONTWRITEBYTECODE=1`. Create `scratch/` if reproducing a published packet.

```sh
python3 "$review_packet/scripts/run_gate.py" probes python3 "$review_packet/scripts/build_probes.py" "$review_repo" --jobs 4
python3 "$review_packet/scripts/run_gate.py" confirm-cases python3 "$review_packet/scripts/confirm_cases.py" "$review_repo" --jobs 4
python3 "$review_packet/scripts/run_gate.py" coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$review_packet/scratch/coverage"
python3 "$review_packet/scripts/run_gate.py" firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$review_packet/scratch/firmware"
python3 "$review_packet/scripts/run_gate.py" srp-campaign python3 "$review_packet/scripts/srp_campaign.py" "$review_repo"
python3 "$review_packet/scripts/run_gate.py" focused-static python3 "$review_packet/scripts/focused_static.py"
python3 "$review_packet/scripts/prepare_dependencies.py"
python3 "$review_packet/scripts/run_gate.py" upstream python3 "$review_packet/scripts/upstream_gate.py" "$review_repo"
python3 "$review_packet/scripts/run_gate.py" upstream-mutations python3 "$review_packet/scripts/upstream_mutations.py" "$review_repo"
python3 "$review_packet/scripts/prepare_mailbox.py" "$review_repo"
make -C "$review_packet/scratch/mailbox/tb/verilator/mbx" -j16 run-wb run-axil VERILATOR="$review_packet/scripts/verilator_bounded.py"
python3 "$review_packet/scripts/run_gate.py" final-integrity python3 "$review_packet/scripts/verify_integrity.py" "$review_repo"
```

Keep each invocation in the foreground. Independent firmware/coverage campaigns may run concurrently within the stated resource cap. Do not run the 16-job dependency build beside other compilation. The mailbox command starts exactly two HDL builds, with four child jobs each. Run no prohibited full banks.

Expected defect evidence: four of the five independent behavior tests fail on this head; the LV original-deadline control passes. All six reviewer source mutants compile and fail their named tests. The probe collector records those failures and may itself exit zero: read each test log and `.rc`, not the collector status as a product verdict. The first `independent-cases.log` predates the added link-pulse probe and expanded observation; `independent-cases-final.log` is the final five-case run. The supplied initial full driver invocation terminated with 143 after its normal arms and 97 existing mutations; the separate SRP campaign completed successfully. The original failed setup attempts are disclosed in REPORT.md.

The scripts read source from the exact checkout and plant only scratch copies. Rerunning overwrites receipt files, so reproduce in a copied packet if retaining the original hashes. No standards PDFs, binary builds, downloaded dependencies or scratch copies are published.
