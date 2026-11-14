These receipts belong to the external independent review of source head `716a8ae7979a31315a6e085959dc4dcc8b7ee022`, base `7398ec0aeea468d92ff642a03a06e291a0cd58d1`.

Set `ROOT` to the candidate checkout, `PACKET` to this directory, and `ARCHIVE` to `review-evidence/894b-r1` extracted from public evidence commit `54b9e537dd9c8daab1fdb0590f8d61b2fd27de37`. All generated files and disposable checkouts belong beneath `$PACKET/scratch/`. The source checkout was never edited. The dependency installations were read only.

Commands and results:

```sh
python3 -B "$PACKET/focused_checks.py" "$ROOT"                   # focused.log: 53 checks, 17 mutants, rc 0
python3 -B "$ROOT/tb/verilator/ctrl_service_budget/shape_costs.py" --check --selftest
# shapes.log: 24/24, rc 0
python3 -B "$ROOT/tb/verilator/ctrl_service_budget/flip_grade.py" --check --point 8x8/1if --selftest
# flip.log: 581/581, load 0.711, rc 0
python3 -B "$PACKET/host_probe.py" "$ROOT" "$PACKET/scratch/host" \
  "Mailbox.EveryNotice*:Mailbox.ARefusedAttemptIsChargedToItsRound:Mailbox.ARoundWithRoomPastARefusalGoesOnToTheNextPort:Mailbox.ARoundFillsWhatItsPassHasLeft"
# The exact executed selection is the test-name list in host.log: four passes, the pre-existing test fails.
python3 -B "$PACKET/host_probe.py" "$PACKET/scratch/base" "$PACKET/scratch/base-host" \
  "Mailbox.ARoundFillsWhatItsPassHasLeft"
# base-host.log: same two assertions fail at 7398ec0a, rc 1 (expected diagnostic result).
python3 -B "$PACKET/notice_fault.py" "$ROOT" "$PACKET/scratch/notice-fault" \
  notice-dropped-with-its-descriptors-next configs/endstation_ax7101_8x8.yaml 1
# notice-fault.log: planted defect caught by its named assertion; diagnostic rc 0.
python3 -I "$PACKET/probe_evidence_gate.py" "$ARCHIVE" "$PACKET/scratch/gate-probes"
# evidence-gate-probes.log: control passes; larger-egress and unmeasured inputs also pass.
python3 -I "$PACKET/audit_archive.py" "$ARCHIVE"
# archive-audit.log: 149 published hashes match; image hash chain and workflow counts checked.
python3 -I "$PACKET/source_comment_audit.py" "$ROOT"
python3 -I "$PACKET/verify_checkout.py" "$ROOT"
```

The host builds used the existing test-library include/library paths. `notice_fault.py` is the public author-r2 `scripts/one_aecp_plant.py`, copied verbatim and run against this exact head; its outputs and mutation remain only in scratch.

The focused CPU execution used an unmodified disposable exact-head checkout at `scratch/cpu`, the existing configured SoC Python environment, the existing preferred RV32 compiler (14.3.0), and the scoped simulator 5.050. `simulator-identity.log` records the verified identity. `PYTHONHASHSEED=0` selected the existing cached CPU netlist. `safe_build_guard.py` refused shared netlist generation/checkout commands and Python file writes outside scratch. No shared install or SDK change occurred. Two initial setup attempts were refused before simulation (missing cached netlist selection); the final receipt and rc refer to the completed run. They are not evidence of candidate failures.

The command implemented by `run_cpu.sh` was:

```sh
# On PATH: the existing scoped simulator and compiler; MILAN_RV32_CC selects that compiler.
"$SOC_PYTHON" -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if \
  --build-dir "$PACKET/scratch/cpu-build" --variant answering-every-port \
  --groups notice-burst-0,notice-burst-3 --jobs 8 \
  --record-budget-findings --record-share-findings
# cpu.rc = 0. The flags preserve observed misses; the raw grades show none in these two groups.
python3 -B "$PACKET/audit_costs.py" "$ROOT" "$PACKET/scratch/cpu-build/results"
python3 -B "$PACKET/audit_events.py" "$ROOT" "$PACKET/scratch/cpu-build/results"
```

Both simulation commands were launched concurrently by the campaign driver. The native build used `make -j16`; no other heavy build overlapped it. All processes completed before the report was finalized. The extra host mutation ran while simulation was active, within the job cap. No full bank, physical implementation, hardware, container runner, or hosted acceptance was run by this reviewer.

The CPU raw traces are gzip-compressed without content changes; their uncompressed hashes and compressed-file hashes are in `receipt-provenance.json`. `cpu/*.json` are the actual grades. Only host directory prefixes in the build metadata and four console logs were normalized; original and published hashes are recorded. The originals remain in unpublished scratch. Trace cycle counts, instructions, assertions and results were not changed. `package_receipts.py` documents this packaging. The full author evidence remains at its immutable public archive; it is not duplicated in this packet.

The `cpu/build.json` input hashes identify the independently built answering-every-port image and its dependencies. This is not a manager source-bank receipt, a hosted-job verdict, a current-dev merge-candidate result, or physical calibration proof.
