[A560]

# Round 14 reproduction

Candidate: `fe1cd0679f5028c749af7242c903a82ca2b3d692`.
Parent: `154722e14781c7373f3229420b6e007f9bcf9835`.
Assignment: issue #665 comment 6055458854.
Only `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` change.

Use a clean candidate checkout at `$SOURCE`, disk scratch at `$SCRATCH`,
and the verified CI-pinned ilp32d SDK at `$SDK`. The SDK archive digest is
`d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.
Initialize the four public submodules at their gitlinks. Before Git commands
inside a dependency, verify its top-level directory equals that dependency.
The shipping default and dependency pins are unchanged.

Export `TMPDIR=$SCRATCH`, `PYTHONDONTWRITEBYTECODE=1`,
`MILAN_RV32_CC=$SDK/bin/riscv32-buildroot-linux-gnu-gcc`, and `VERILATOR_JOBS=2`.
Use the locked documentation environment and Verilator 5.050. The retained
launcher wraps Verilator with two process locks and limits each make to `-j8`.
Each long job starts with `setsid nohup`, with a distinct log and exit receipt;
foreground status waits last less than nine minutes. Resource samples require
memory below 9 GB and at least 30 GB free disk.

## Runner and controls

Run the candidate offline self-test only inside a disposable job. The measured
job used the existing full Ubuntu image `2d09d1152abe`, no network, a read-only
source snapshot, a separate writable disk scratch mount, an unprivileged UID,
all capabilities dropped, no-new-privileges, a 2 GB memory limit and 512 PID
limit. No host credentials or Docker socket enter it.

```sh
python3 -I scripts/act_ci.py --selftest
```

The retained `round14-helpers/runner-job.sh` specifies the disposable boundary.
The runner's tested SHA256 is
`35890beace97bf9e2b26bb24a8016b585767e24566ffbf9a62a0ada0beccfd66`;
size 568102 bytes. The runner itself is retained in Git, never copied into this
packet. The snapshot's runner bytes equal the candidate's committed blob.

The retained `round14-helpers/runner-mutants.py` runs the focused manifest self-test from isolated source
copies inside that same disposable boundary. It requires a passing baseline
and each named FAIL. It deletes the trusted entry, drops required
materialization, disables exact manifest comparison for three named checks,
disables duplicate rejection, and disables gitlink comparison for two checks.
Eight check/plant pairs represent five distinct source mutations. The standing
self-test also plants two candidate-controlled expected-manifest faults.

## Contract, docs and firmware

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$SCRATCH/ctrl-build"
python3 sw/builder/test_builder.py --require-rv32
python3 sw/builder/test_firmware_compiler.py --sdk-destination "$SDK" --audit "$SCRATCH/rv32-pinned.jsonl"
python3 sw/builder/test_firmware_compiler.py --selftest
```

Run the builder and compiler audit in separate disposable initialized worktrees
at the candidate. The builder retains its established absolute compiler
selector; the audit changes only compiler argv[0] to the pinned SDK and records
every invocation. It does not change the selector, HOME, PATH or shared tools.
The ctrl gate uses the pinned SDK directly through its supported environment.

The documentation bank contains the same 75 workflow-derived commands as the
previous round, with the new parent as the added-line base and new scratch
outputs. The complete command list, exits, log sizes and SHA256 values are in
`ROUND14-GATES.json` and `ROUND14-GATES.md`. Generated outputs remain in disk
scratch or are moved there after a generator completes. No gate is piped.

## Limits

This packet supplies execution evidence. It grants no review verdict and no
merge authorization. Manager-owned trusted replay uses dev's runner plus the
reviewed manifest entry, as the assignment directs. Hosted checks, corrected-head
review and merge-candidate validation remain separate duties. Firmware coverage
is retained from Round 13 because firmware/test source bytes do not change;
this round does not claim a new coverage measurement or a hardware result.
