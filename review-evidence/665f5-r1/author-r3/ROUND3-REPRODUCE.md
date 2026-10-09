# Round 3 reproduction

[A572] Relates to #665. Run from the candidate root. Set `PACKET` to this
packet and `F5_SCRATCH` to an empty directory on disk. Set `PINNED_VERILATOR`
to the pinned 5.050 executable and `PROCESSOR_69_REFERENCE` to an unchanged
archive of processor revision `c9f74b6866a63dd3c0e4534724bfc07a86ad142b`.
The wire driver checks the reference source inventory. `DOC_PYTHON` needs the
hash-locked Markdown and HDL parser dependencies from the repository plus
its workflow's YAML and waveform dependencies. The builder discovers the
existing build environment using its normal documented search.

Use the same RV32 compiler selector and freestanding runtime archives recorded
in `runtime-provenance.json`. The round 3 links reuse those archives; no
compiler, runtime, image, tree export or package is stored in this packet.

Every command below runs in the foreground. A partition returns zero only when
all its selected cases pass; all listed partitions are required. Keep at most
two simulation builds active, use eight compile jobs per simulation build,
limit campaign jobs to four, and keep memory consumption below 9 GB.

```sh
export TMPDIR="$F5_SCRATCH" PYTHONDONTWRITEBYTECODE=1 VERILATOR_JOBS=2
mkdir -p "$F5_SCRATCH"
git rev-parse HEAD
git diff --check
```

Before any Git operation inside a submodule, verify its top-level directory:

```sh
git -C "$SUBMODULE" rev-parse --show-toplevel
```

Run the normal firmware bank:

```sh
timeout 560 python3 -u -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$F5_SCRATCH/firmware-bank"
```

Expected: the firmware bank returns zero, including composed AECP at one/two
interfaces, all five images and the diagnostic guard. The 59 arms produce 65 tallies and 1408 checks, with zero failures.

```sh
timeout 560 python3 -u -B sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$F5_SCRATCH/coverage" --lwsrp third_party/lwSRP
timeout 560 python3 -B sw/firmware/gtest/fw_coverage.py --selftest
timeout 560 python3 -B sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
timeout 560 python3 -B scripts/suite_tally.py --selftest
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_mutants.py --shard "$PART" 2 --output "$F5_SCRATCH/mutants-$PART"
timeout 250 python3 -u -B sw/firmware/ctrl/test/aecp_arms.py --app --interfaces "$INTERFACES" --asan --output "$F5_SCRATCH/asan-$INTERFACES"
```

Run mutation `PART=0,1` and sanitizer `INTERFACES=1,2`. Expected: 100% raw
coverage for the eight AECP/application production units with no new
exclusion, all 72 named source plants caught, and 70 tests per sanitizer arm.

```sh
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_wire.py --reference protocol-processor --interfaces 1 --output "$F5_SCRATCH/wire-1" --verilator "$PINNED_VERILATOR"
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_wire.py --reference "$PROCESSOR_69_REFERENCE" --interfaces 2 --output "$F5_SCRATCH/wire-2" --verilator "$PINNED_VERILATOR"
timeout 560 python3 -B sw/mailbox/gen_mailbox.py --check
```

Expected: 132 observations at one interface, 137 on each ingress at two,
seven oracle controls per ingress, and current generated mailbox files.

Run the default mailbox target in a scratch copy of `tb/verilator/mbx` and
`tb/common`, with links to the candidate's `hdl`, `sw`, `third_party` and
processor directories. The scratch Makefile adds `--jobs 2` to
`mutants.py --quick`; it selects the same complete quick table.

```sh
timeout 560 make -C "$VALIDATION_TREE/tb/verilator/mbx" VBUILD_JOBS=8 VERILATOR="$PINNED_VERILATOR"
```

Run builder `PART=0..3` sequentially: several tests temporarily plant files in
the candidate tree and restore them. The four profile partitions operate on
independent in-memory fixture tables and may run concurrently. Their receipts
must have the exact union of the original tables. Run docs `PART=0..2`.

```sh
timeout 560 python3 -u -B "$PACKET/run_gate_partition.py" --root . --scratch "$F5_SCRATCH/builder" --family builder --part "$PART" --parts 4
timeout 560 python3 -u -B "$PACKET/run_profile_partition.py" --root . --output "$F5_SCRATCH/profile-$PART" --part "$PART" --parts 4
timeout 560 "$DOC_PYTHON" -u -B "$PACKET/run_docs_partition.py" --root . --scratch "$F5_SCRATCH/docs" --part "$PART" --parts 3
timeout 560 "$DOC_PYTHON" -B scripts/check_em_dash.py --base 5603c353
```

Re-link for `SHAPE=1x1_tdm8,8x8` and `INTERFACES=1,2`. `LIBC` and
`COMPILER_RUNTIME` are the recorded freestanding archives. All four commands
must return zero and remain below the 224 KB ceiling.

```sh
timeout 560 python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --with-aecp --config "configs/endstation_ax7101_$SHAPE.yaml" --interfaces "$INTERFACES" --output "$F5_SCRATCH/size-$SHAPE-if$INTERFACES" --libc "$LIBC" --compiler-runtime "$COMPILER_RUNTIME"
```

The maximum measured span is 221728 bytes including the 8192-byte stack
reservation. These are linked opt-in fixtures. Physical calibration, routed
memory fit, hosted checks, independent re-review and merge validation remain
outside this local evidence.


## Round 3 reviewer controls

Extract only the two scripts and the probe source from
`review-evidence/665f5-r1/reviews/R564-2/` on evidence commit
`0d45b1d52ab180dfa45f0057c89795a9755e4360` into `$REVIEW_PACKET`. They are public review artifacts. Preserve
`scripts/` and `probes/` beneath that directory and verify the supplied manifest.
Run the unchanged probes at both interface counts and all five review plants:

```sh
timeout 560 python3 -B "$REVIEW_PACKET/scripts/run_probes.py" . "$REVIEW_PACKET" r564-2
timeout 560 python3 -B "$REVIEW_PACKET/scripts/run_review_mutants.py" . "$REVIEW_PACKET"
```

Expected: Q1-Q5 pass at both interface counts. Every reviewer plant returns 1
from completed assertion failures. The first two plants must each name both
`Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` and
`Core.SetStreamInfoWithoutSubcommandPreservesState` as failing tests. The review
script's own zero exit is insufficient: inspect its `results.json` and logs.
The maintained source-plant gate additionally requires the named diagnostics.

The no-subcommand wire record stores 67890 and requests 765432. Both interface
runs must reject the `nosub-latency` control with the diagnostic
`SET requested or current latency`. All seven controls run for each ingress.

The current head is `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`. No production
source changed from Round 2. The four section/pool tables are unchanged; compare
load bytes extracted from each ELF with the corresponding Round 2 result. All
four match. ELF metadata can differ with build paths and is not this comparison.

## Exact execution receipts

`round3/commands.json` contains the exact argument vectors, return codes and
elapsed times with installation locations expressed as environment variables.
`round3/audit.json` records exact fixture-table unions, source-plant coverage,
reviewer controls and the firmware tally. `round3/attempts.json` preserves the
superseded setup attempts separately from the passing gate table.
