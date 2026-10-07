The report reviews `a6e6916826448f81de2b779ca61a87a9f8c47278`. Run these scripts from a clean checkout at that commit, with its required submodules initialized. Keep this packet outside the checkout. All generated trees belong in the packet's `scratch/` directory, which is excluded from publication.

Set `REVIEW_PACKET` to this packet's absolute directory. The receipt wrapper sets `TMPDIR`, disables bytecode generation, selects `scratch/sdk/bin/riscv32-linux-gcc`, runs its child in the foreground, and records its exit code and log. Logs substitute `$PACKET`, `$CHECKOUT` and `$USER_HOME` for machine paths; both original and published hashes are recorded. The wrapper does not detach a process. Run separate foreground terminal sessions concurrently for independent suites, keeping their combined parallelism at or below 16 and memory below 12 GB. Campaign and coverage commands use four jobs. The mailbox command uses `make -j16 VBUILD_JOBS=2`.

Install the repository-pinned SDK into `scratch/sdk` with `scripts/ci_rv32_sdk.py --destination "$REVIEW_PACKET/scratch/sdk"`; an existing matching archive may be supplied with `--archive`. The receipt records the archive digest and compiler identity. Set `REVIEW_VERILATOR` to the verified scoped 5.050 executable for the mailbox and MAAP differential commands. Runtime image inputs are the source trees identified by `receipts/runtime-provenance.json`: supply their local paths to `ctrl_image_runtime.py` as recorded in `receipts/runtime.json`, writing its output to `scratch/runtime`. Source digests, not installation paths, identify these inputs.

The decisive probe is:

```sh
python3 "$REVIEW_PACKET/run_receipt.py" binding-delivery python3 "$REVIEW_PACKET/binding_probe.py"
```

At this head, the wrapper exits zero only when the required-behavior assertion fails on every tested interface and the direct-delivery positive control succeeds. It is a confirmed defect reproduction, not a passing delivery test. The original `binding-probe` receipt preserves an earlier wrapper assertion error: it counted both the detailed failure and summary. The final script counts only detailed `[FAIL]` lines; no production code changed.

The other principal commands are:

```sh
python3 "$REVIEW_PACKET/run_receipt.py" ctrl-campaign python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$REVIEW_PACKET/scratch/ctrl-campaign"
python3 "$REVIEW_PACKET/run_receipt.py" four-way-plants python3 "$REVIEW_PACKET/collect_campaign.py"
python3 "$REVIEW_PACKET/run_receipt.py" coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$REVIEW_PACKET/scratch/coverage"
python3 "$REVIEW_PACKET/run_receipt.py" f3-images python3 sw/firmware/ctrl/test/ctrl_image.py --out "$REVIEW_PACKET/scratch/f3-images"
python3 "$REVIEW_PACKET/run_receipt.py" srp-images python3 "$REVIEW_PACKET/images.py"
python3 "$REVIEW_PACKET/run_receipt.py" image-controls python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
python3 "$REVIEW_PACKET/run_receipt.py" image-comparison python3 "$REVIEW_PACKET/compare_images.py"
python3 "$REVIEW_PACKET/run_receipt.py" maap-differential python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$REVIEW_PACKET/scratch/maap-differential"
python3 "$REVIEW_PACKET/run_receipt.py" bound-table python3 "$REVIEW_PACKET/check_bounds.py"
python3 "$REVIEW_PACKET/run_receipt.py" merge-retention python3 "$REVIEW_PACKET/review_static.py"
python3 "$REVIEW_PACKET/run_receipt.py" integrity-final python3 "$REVIEW_PACKET/verify_tree.py"
```

For the mailbox gate, extract `git archive HEAD` into the empty directory `scratch/mailbox`, then run the following with `REVIEW_VERILATOR` exported:

```sh
python3 "$REVIEW_PACKET/run_receipt.py" mailbox make -C "$REVIEW_PACKET/scratch/mailbox/tb/verilator/mbx" -j16 VBUILD_JOBS=2
```

Run `collect_campaign.py` after the campaign completes; it checks the final return code and named failed observables before retaining the twelve composition-plant logs. `receipts/*.json` contains every additional command and result. `audit_public.py` verifies retained logs using the public evidence commit's git objects; it executes no author script. Fetch that commit into the isolated checkout before running it if necessary. Public source receipts and reviewer executions are attributed separately in the report. The manifest lists exactly the portable files and receipts selected for publication, never `scratch/`.
