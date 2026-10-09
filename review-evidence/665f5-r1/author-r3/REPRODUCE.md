# F5 reproduction

Use head `1e68d1b62ef2facdf0e8dbad28a202297d433c61`, base
`5603c353137e90c1fa95429f6d00ef7a2298d9ee`. Run from the candidate root.
Set `PACKET` to this packet, `F5_SCRATCH` to disk-backed scratch, and
`DOC_PYTHON` to an interpreter with the workflow's hash-locked Markdown
requirements, YAML, waveform renderer and HDL parser dependencies installed.
`BUILDER_PYTHON` has the existing build dependencies. No dependencies, binaries,
archives or exported trees are contained in this packet.

Set `MILAN_RV32_CC` explicitly to the RV32 compiler under comparison. Final
fixture and regression measurements used GCC 14.3.0 (Buildroot 2026.05), the
existing absolute selector. The freestanding runtime was built with GCC 14.3.0
from the 2025.08-1 archive. These are different installations and are not claimed
to have identical executables. The latter archive digest is
`d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.
The archive installer/provenance gate passed on a new scratch installation.
Every linked object is checked as RV32I ILP32; no SDK hosted libc is linked.

Set `PINNED_VERILATOR` to the pinned 5.050 executable. Use `VERILATOR_JOBS=2`
and eight compile jobs per wire build. Run no more than two such builds at once.
Campaign drivers use at most four workers. Every invocation below is foreground,
with a 560-second cap. Select one `PART` per invocation; the packet records the
complete partition union. Avoid launching enough independent campaigns to push
MemoryCurrent above 9 GB; clean build-file cache can dominate that accounting.

```sh
export TMPDIR="$F5_SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export MILAN_RV32_CC VERILATOR_JOBS=2
mkdir -p "$F5_SCRATCH"
git rev-parse HEAD
git diff --check
```

Submodules must be initialized at their pins. Before any command inside a
submodule, verify that `git -C "$SUBMODULE" rev-parse --show-toplevel` equals
that exact directory. The two-interface processor reference is a scratch archive
of processor revision `c9f74b6866a63dd3c0e4534724bfc07a86ad142b` (merged issue
69), exposed as `PROCESSOR_69_REFERENCE`. Its content fingerprint is recorded
by the differential driver. The single-interface driver uses the repository pin
`2ad2f845dd583f8310075fa2380cb60a04fd091a`.

## New behavior and normal regressions

```sh
timeout 560 python3 -B sw/mailbox/gen_mailbox.py --check
timeout 560 python3 -u -B sw/firmware/ctrl/test/test_ctrl_firmware.py \
  --require-rv32 --jobs 4 --build-dir "$F5_SCRATCH/firmware-bank-final"
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_arms.py \
  --app --interfaces 2 --asan --output "$F5_SCRATCH/asan-current"
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_arms.py \
  --mailbox --interfaces 1 --filter 'Latency.*' --output "$F5_SCRATCH/latency-max-if1"
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_arms.py \
  --mailbox --interfaces 2 --filter 'Latency.*' --output "$F5_SCRATCH/latency-max"
timeout 560 python3 -u -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py \
  --require-rv32 --jobs 4
timeout 560 python3 -u -B sw/firmware/gtest/fw_coverage.py \
  --check --jobs 4 --keep "$F5_SCRATCH/coverage" --lwsrp third_party/lwSRP
timeout 560 python3 -B sw/firmware/gtest/fw_coverage.py --selftest
timeout 560 python3 -B sw/firmware/gtest/fw_rv32_selftest.py
```

The suite tally reader is `scripts/suite_tally.py --selftest`.
All commands return 0. The saved-state normal bank grades 435 tests across five
shapes. The composed AECP sanitizer arm grades 62 tests. The full normal bank
also runs all five generated images (three tests each) and the diagnostic guard.

## Source-defect campaigns

Each selected partition returns 0 only when every named assertion fails on its
plant. For AECP use `PART=0,1` with the first command. For the inherited controls
use 0 through 15; SRP 0 through 7; one-interface SRP 0 through 3. The latter
includes the complete existing interface-sensitive subset, 68 plants.

```sh
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_mutants.py \
  --shard "$PART" 2 --output "$F5_SCRATCH/aecp-mutants-$PART"
timeout 560 python3 -u -B "$PACKET/run_gate_partition.py" \
  --root . --scratch "$F5_SCRATCH" --family ctrl --part "$PART" --parts 16
timeout 560 python3 -u -B "$PACKET/run_gate_partition.py" \
  --root . --scratch "$F5_SCRATCH" --family srp --part "$PART" --parts 8
timeout 560 python3 -u -B "$PACKET/run_gate_partition.py" \
  --root . --scratch "$F5_SCRATCH" --family srp1 --part "$PART" --parts 4
timeout 560 python3 -u -B "$PACKET/run_nvm_partition.py" \
  --root . --output "$F5_SCRATCH/nvm-part$PART" --part "$PART" --parts 4
```

Totals: 59 new AECP plants, 471 inherited control plants, 169 SRP plants,
68 interface-sensitive SRP plants, 109 saved-state plants. The saved-state
partition changes only the iterable passed to the original plant pool. Full
shape preparation, binary listing and test-to-plant ownership checks remain in
every invocation. The original plant and assertion grader is unchanged.
Run the two pin controls with the existing grader after verifying the submodule root:

```sh
python3 -B -c 'import sys; from pathlib import Path; sys.path.insert(0,"sw/firmware/ctrl/test"); import ctrl_mutants; raise SystemExit(ctrl_mutants.lwsrp_pin_arms(Path(__import__("os").environ["F5_SCRATCH"])/"pin-controls",Path("third_party/lwSRP").resolve()))'
```

The two lwSRP pin controls also return 0; they reject a modified compiled source
and a different revision without touching the repository submodule.

## Wire differential

```sh
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_wire.py \
  --reference protocol-processor --interfaces 1 --output "$F5_SCRATCH/wire-one" \
  --verilator "$PINNED_VERILATOR"
timeout 560 python3 -u -B sw/firmware/ctrl/test/aecp_wire.py \
  --reference "$PROCESSOR_69_REFERENCE" --interfaces 2 --output "$F5_SCRATCH/wire-two" \
  --verilator "$PINNED_VERILATOR"
```

Both return 0, including six observation plants per ingress. See HANDOFF.md for
the four allowed differences and clauses. All reference sources are fingerprinted
before compilation. Only external bench providers and generated test inputs are
adapted; no product RTL or configuration is changed.

## Linked fixtures

`PICOLIBC`, `COMPILER_RT` and `LITEX_SOFTWARE` identify the runtime source roots
whose file hashes are in `runtime-provenance.json`. Select the recorded runtime
compiler for the first command, then the fixture compiler for links. The replay
adds the explicit no-stack-protector flag to the generator's recorded recipe.

```sh
timeout 560 python3 -B sw/firmware/ctrl/test/ctrl_image_runtime.py \
  --picolibc "$PICOLIBC" --compiler-rt "$COMPILER_RT" \
  --litex-software "$LITEX_SOFTWARE" --output "$F5_SCRATCH/runtime"
timeout 560 python3 -B "$PACKET/rebuild_runtime.py" \
  "$F5_SCRATCH/runtime" "$F5_SCRATCH/runtime-freestanding"
timeout 560 python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --with-aecp \
  --config "configs/endstation_ax7101_$SHAPE.yaml" --interfaces "$INTERFACES" \
  --output "$F5_SCRATCH/final-$SHAPE-if$INTERFACES" \
  --libc "$F5_SCRATCH/runtime-freestanding/libc.a" \
  --compiler-runtime "$F5_SCRATCH/runtime-freestanding/libcompiler_rt.a"
```

Run the link for `SHAPE=1x1_tdm8,8x8` and `INTERFACES=1,2`. Baseline comparison
uses the F4 entry without `--with-aecp` and the same archives; the F4 input units
are unchanged from the base. All four final spans and all static pools are in
`size-matrix.json`. No archive, ELF, map or generated image is copied into the
packet; their SHA-256 and sizes are retained instead.

## Mailbox, builder and documentation banks

The mailbox default target was run from a scratch candidate export with the
initialized submodule roots linked read-only by convention. A scratch-only
Makefile adjustment adds `--jobs 2` to its quick campaign command; this retains
every test while obeying the build concurrency limit. Use `VBUILD_JOBS=8` and
serial top-level make:

```sh
timeout 560 make -C "$VALIDATION_TREE/tb/verilator/mbx" \
  VBUILD_JOBS=8 VERILATOR="$PINNED_VERILATOR"
```

Builder functions except the long profile gate are divided into four partitions,
`PART=0..3`. The profile gate's four independent tables (accepted firmware,
accepted Makefiles, source plants and disconnected identity controls) also use
four partitions. Their setup, reason controls and all other assertions repeat
unchanged. Source SHA-256 and full/selected table names are retained per run.
The same partitioning is applied to the existing absent-compiler audit, preserving
its cross-candidate hiding and host-compilation refusal. Whole-bank attempts that
hit the 560-second cap are not counted as successes.

```sh
timeout 560 "$BUILDER_PYTHON" -u -B "$PACKET/run_gate_partition.py" \
  --root . --scratch "$F5_SCRATCH" --family builder --part "$PART" --parts 4
timeout 560 "$BUILDER_PYTHON" -u -B "$PACKET/run_profile_partition.py" \
  --root . --output "$F5_SCRATCH/profile-final$PART" --part "$PART" --parts 4
timeout 560 "$BUILDER_PYTHON" -u -B "$PACKET/run_profile_partition.py" \
  --root . --output "$F5_SCRATCH/absent$PART" --part "$PART" --parts 4 --absent
```

The packet's `docs-commands.json` enumerates the 73 workflow commands.
Use `PART=0..2`; dependencies are those declared in `.github/workflows/docs.yml`.

```sh
timeout 560 "$DOC_PYTHON" -u -B "$PACKET/run_docs_partition.py" \
  --root . --scratch "$F5_SCRATCH" --part "$PART" --parts 3
timeout 560 "$DOC_PYTHON" -B scripts/check_em_dash.py --base 5603c353
timeout 560 python3 -B scripts/check_wire_accountability.py --self-test
timeout 560 python3 -B scripts/ci_rv32_sdk.py \
  --destination "$F5_SCRATCH/verified-sdk" --archive "$SDK_ARCHIVE"
```

Also run `scripts/docs_check.py` and `scripts/check_feature_status.py` in a fresh
HEAD export with no `.git`. The offline local-replica self-test runs only inside
a disposable job container: read-only candidate, writable disk-backed scratch,
no host container socket and no forwarded credential. Its image needs the
workflow's Python/YAML, Git, sudo and container CLI prerequisites. Inside that
boundary run `python3 -I scripts/act_ci.py --selftest`; it returns 0. Do not run
the candidate as a host-side orchestrator.

The existing physical calibration arm is explicitly NOT RUN because its report
is unavailable and hardware access is prohibited. No hosted status, independent
review or merge validation is implied by these local commands.
