R531-5 focused reproduction

Use a detached clone at `13e715136b0b7c8d9763e0b730d9709f2c9f5932`, with the three required submodules initialized at their gitlinks. Install the normal repository host prerequisites before starting. Copy the portable scripts into a new packet directory to preserve these receipts. Commands below run from the clone. Set `REVIEW_PACKET` to that new directory, `REVIEW_CHECKOUT` to the clone, `REVIEW_SIM` to the verified 5.050 executable, and `REVIEW_SDK_ARCHIVE` to the pinned SDK archive. These are task-specific variables.

```sh
mkdir -p "$REVIEW_PACKET/scratch"
python3 -B "$REVIEW_PACKET/verify_source.py" "$REVIEW_CHECKOUT"
python3 -B "$REVIEW_PACKET/run_focused.py" "$REVIEW_CHECKOUT" --jobs 4
python3 -B "$REVIEW_PACKET/run_mailbox.py" "$REVIEW_CHECKOUT" "$REVIEW_SIM"
python3 -B "$REVIEW_PACKET/run_mutations.py" "$REVIEW_CHECKOUT" --jobs 4
python3 -B scripts/ci_rv32_sdk.py --archive "$REVIEW_SDK_ARCHIVE" --destination "$REVIEW_PACKET/scratch/sdk"
python3 -B "$REVIEW_PACKET/run_measure.py" "$REVIEW_CHECKOUT"
python3 -B "$REVIEW_PACKET/audit_images.py" "$REVIEW_PACKET/scratch/image" "$REVIEW_PACKET/scratch/sdk/bin/riscv32-linux-"
python3 -B sw/mailbox/gen_mailbox.py --check --crosscheck
python3 -B sw/mailbox/gen_mailbox.py --selftest
python3 -B scripts/check_baremetal_only.py --check
python3 -B scripts/docs_check.py
git diff --check 021b9c1fb966e9a1a4acef6b5233edd3518f32a0..13e715136b0b7c8d9763e0b730d9709f2c9f5932
python3 -B "$REVIEW_PACKET/verify_source.py" "$REVIEW_CHECKOUT"
```

Every command exits 0. The firmware and mutation drivers use three workers with `--jobs 4` each. The mailbox driver exports tracked inputs to scratch, then runs `make -j16 VBUILD_JOBS=2 run-wb run-axil run-cosim run-if2`. The image measurement and self-test run concurrently. Every driver joins all children before returning; do not launch these driver groups simultaneously because their combined compiler budget would exceed the review cap. The mutation driver depends on the stimulus extraction produced by the focused driver. Reproduction emits new receipts beside the scripts and puts all disposable files under scratch.

Actual review inputs were the supplied detached clone, simulator `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, and the existing pinned archive `$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz`. The installer verified the archive digest and created a fresh local SDK. No shared installation was modified.

The generator check and generator self-test were independent executions. Documentation, bare-metal and diff checks ran concurrently in a foreground driver. The source and submodule byte/index verification was repeated after removing only the generated interpreter caches. See REPORT.md for observed counts, caveats and full public authority links.

Publication normalization: mailbox.log replaces the host-specific compiler installation prefix with `$SIM_ROOT`. No command, diagnostic, assertion or result is changed. The unnormalized receipt remains in unpublished scratch. Other execution receipts retain their emitted text.
