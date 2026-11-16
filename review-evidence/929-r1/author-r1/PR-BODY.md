[A792]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> base.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `37255683`: each of the three gates passes from a clean clone (the twin 0 findings, its 21 plants refused; `dynmap-mutants` 71 of 71 from a fresh clone; `srp_mbx.cpp` 74 of 74 at both entities and both interface counts), with every job the change touches replayed green on fresh clones.

`929-base-gates` -> `dev-soft-core`: five commits on `70f4056f` (#901's merge). Tests, harnesses and docs only: no
firmware, RTL, mailbox-contract or CPU-budget-bound change.

## Linked Issue / roles

Closes #929
Relates to #665

Executor: `[A792]`
Internal cleared-context reviewer: `[R<n>]` (to be named by the manager)
External reviewer: `[R<n>]` (to be named by the manager)

## Description

Three gates failed at dev-soft-core's base. Each is reproduced at `70f4056f` on a clean clone, its cause found, and
fixed at that cause, with a planted defect caught by name.

**1. The twin's owed row `split-talker-failed` (`make -C tb/verilator/milan_dp twin` exited 2).** The row owed the
split's "Talker Failed for both sources' streams from boot, never withdrawn", caused by no SRP adapter entry taking
MAAP's allocation. #895 added that entry (`srp_mbx_allocation`) and declares a source only while its SRP parameters
are valid. At the base the split declares no Talker Failed in the twin's stimulus; its Talker Advertise for
STREAM_OUTPUT 0's stream runs from 5190 ms to its Leave at 20190 ms, the fabric's from 5200 ms to 20000 ms. The
remaining count differences are each half's own join and LeaveAll timers, and both halves pass the Table 10-3 grade.
So the owed difference has gone, and the row is deleted, as the twin's rule asks of the lane that fixed it.
#925's change (PR #932) does not move this: at its head `09a948d4` the twin's two captures are byte-identical to the
base's (the split half receives no MSRPDU, and #932 changes how received Talker registrations decide the Listener).

| Piece | Change |
|---|---|
| `tb/verilator/milan_dp/twin_compare.py` | the row and its constants deleted; the Talker attributes are compared like every other MSRP attribute (the LeaveAll-boundary declarations and the Table 10-3 grade). `stream-output-0-notices`' cause restated to what is true since #895 (values unchanged). `srp-plus-k`'s and `leave-all-declaration`'s words restated to the findings that now refuse them |
| `tb/verilator/milan_dp/twin_plants.py`, `Makefile` | new capture plant `talker-failed-back`: the split's Talker Advertise re-encoded in place as Talker Failed, code 2 (the row's old behaviour), refused by name |
| `tb/verilator/milan_dp/README.md` | the owed rows, the deletion and why, the plants (21), what the twin finds |

**2. `dynmap-mutants`' listener control on a fresh clone.** The campaign builds each leg through its suite's recipe
with `-o` for the generated inputs the leg reads, and `make dynmap-mutants` makes only milan_dp's own legs first. A
fresh clone has made nothing in `milan_dp_render`, so the listener leg ran with no ROM, microcode or entity image and
failed its control (`[FAIL] the unmutated gateware does NOT pass the listener leg (caught)`). `capture_coherence`'s
talker leg ran without its two inputs too, and passed.

| Piece | Change |
|---|---|
| `tb/verilator/milan_dp/dynmap_mutants.py` | `prepare()`: before each selected leg's clean control, make its declared inputs through that suite's own rules; a leg whose inputs are still absent is refused by name, `[FAIL] the <leg> leg's inputs are not made: ...` |
| `tb/verilator/milan_dp/README.md` | the campaign's input step |

**3. Two `srp_mbx.cpp` startup tests at the 8x8 entity.** Both were written for the 1x1 entity (two sources, two
sinks); the 8x8 entity compiles nine and nine. The firmware does what its rule says (`srp_mbx.c`, the Talker
declarations: Advertise when allocated and admitted, else Failed with code 2 when unallocated, IEEE 802.1Q-2018
35.2.2.8.7, Table 35-6), so these are test defects.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/test/srp_mbx.cpp` | `StartupDeclaresTalkersDomainAndVlan` holds each source of the compiled shape by its own StreamID (type, New/New/JoinMt timing, TSpec, code 2) and exactly three Talker declarations per source; at 1x1 it is the old test. `OneLoopOwnsTheGlobalCentisecondDispatch` gives its two adapters two of the shape's SRP pools, where a 1x1-sized pool refused the second `srp_mbx_init` at 8x8 with two interfaces |
| `sw/firmware/ctrl/test/srp_arms.py`, `test_ctrl_firmware.py` | `srp_mbx.cpp` at the 8x8 entity at both interface counts in the suites phase (`firmware-unit`), the clean control for the plants below |
| `sw/firmware/ctrl/test/srp_mutants.py` | three plants at the 8x8 entity in the two-interface campaign, each caught by its named check |
| `sw/firmware/ctrl/srp/README.md` | the 8x8 arms |

**Planted defects, each caught by name.**

| Plant | Where | Caught by |
|---|---|---|
| `talker-failed-back` (new) | twin capture plant: the split's Talker Advertise re-encoded as Talker Failed | `MSRP declarations at the LeaveAll boundaries differ: the fabric's [{Talker Advertise stream_id 0200000000010000; Domain value 06030002} x1, {Domain value 06030002} x5], the split's [{Talker Failed stream_id 0200000000010000; Domain value 06030002} x1` |
| `srp-plus-k` (words restated) | twin split plant: the first Talker vector's FirstValue one higher | `MSRP Talker Advertise stream_id 0200000000010001` |
| `leave-all-declaration` (words restated) | twin capture plant | the same LeaveAll-boundary finding, now with the Talker's first boundary, `{none} x3` kept |
| the input step's make skipped (one-off, fresh clone) | `dynmap_mutants.py` | `[FAIL] the listener leg's inputs are not made: its suite did not make ltn_rom.hex, ucode.hex, tdm8r_aemi.bin` |
| the input step removed (one-off, fresh clone) | `dynmap_mutants.py` | `[FAIL] the unmutated gateware does NOT pass the listener leg (caught)`, the base's failure |
| `startup-8x8-sources-past-two-undeclared` (new) | SRP two-interface campaign, 8x8 | `each source's three Talker declarations and no other`; escapes at 1x1 |
| `startup-8x8-failure-code-past-two` (new) | SRP two-interface campaign, 8x8 | `source 2's failure code`; escapes at 1x1 |
| `duplicate-tick-owner-8x8` (new) | SRP two-interface campaign, 8x8 | `srp_mbx_attach` |

The three kept plants that name the two changed tests (`startup-vid`, `duplicate-tick-owner`,
`transmit-first-link-up-owes-nothing`) are still caught by their words.

**Images.** The release image is byte-identical to the base's at `37255683`: `bios.bin`, its disassembly and the debug-stripped ELF at both AX7101 configs; the whole ELFs differ only in debug sections, by the clone path. No split image changes: the platform image at every ledger point (1x1 and 8x8, one and two interfaces) and the split SoC's images are identical, whole ELF, stripped and loadable, and `plat_ledger.py` passes at every point with the base's figures. milan_dp's make database differs from the base's only in `TWIN_CAPTURE_PLANTS`, so every recipe the sweep runs there is unchanged.

## Authoritative references

- #929 and its comment (the third finding); #925 issuecomment-6929001329; #895, #901 (the split's Talker
  declarations); #925 / PR #932.
- IEEE 802.1Q-2018 35.2.2.8, 35.2.2.8.7 and Table 35-6 (Talker Failed, its code); Table 10-3 (the Applicant).
- Milan v1.2 4.3.3.2 Table 4.4 (MaxFrameSize); 5.4.5.2, Table 5.22 (GET_STREAM_INFO notices).
- `tb/verilator/milan_dp/README.md` (the two-placement simulation, `dynmap-mutants`);
  `sw/firmware/ctrl/srp/README.md` (the Talker declarations, the evidence).

## How to get into the same state

```sh
git fetch origin 929-base-gates && git checkout --detach 37255683
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
make -C tb/verilator/milan_dp twin
make -C tb/verilator/milan_dp twin-plants
make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=8      # from a fresh clone
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 scripts/docs_check.py
```

Expected result / pass criteria:

- `twin`: exit 0, `twin: 0 finding(s)`; the notes list `stream-output-0-notices`, `entity-available-index` and the
  three fabric grade rows as owed.
- `twin-plants`: exit 0, each of 21 plants `REFUSED` by its words against its own half and between the placements.
- `dynmap-mutants`: every leg's control `[PASS]` (the listener's included), `71 checks: 71 PASS, 0 FAIL`.
- The firmware shards PASS: `srp_mbx` arms `[ok]` at 1x1 and 8x8, one and two interfaces; the SRP campaign 424
  caught (the base's 421 and the three 8x8 plants), 0 escaped; `firmware coverage: PASS`.
- `docs_check`: 0 findings.

**Evidence at `37255683`** (clean clones; each workflow job replayed step by step on its own fresh clone):
- rtl-fast `changes`, `firmware-unit`, `firmware-srp-mutants`, `firmware-control-mutants`, `firmware-aecp-mutants`,
  `firmware-boundary`, `firmware-verilator`, `split-cdc`, and docs' six jobs: 88 steps rc 0, 56 hosted-only steps
  not run with their reasons, 0 bad.
- `make -C tb/verilator/milan_dp twin`: rc 0, 0 findings; `twin-plants`: rc 0, 21 plants refused both ways.
- `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=8` from a fresh clone: rc 0,
  `71 checks: 71 PASS, 0 FAIL`.
- At the base `70f4056f`, on clean clones, each gate failed with the words above; at #932's head `09a948d4` the twin
  failed as at the base, with byte-identical captures.
- The native Verilator sweep was not run: no suite it runs reads a changed file, and milan_dp's make database differs
  from the base's only in `TWIN_CAPTURE_PLANTS`.

## Known limitations / out of scope

- **`stream-output-0-notices` (the twin) still holds**, by the same values. Its cause is restated: the split's
  Talker declares and withdraws since #895, and the split sends no GET_STREAM_INFO notice of STREAM_OUTPUT 0 at either
  change (Milan v1.2 5.4.5.2, Table 5.22). No issue owns that yet; the row names #665 and leaves the step unnamed.
- **The twin compares Talker declarations by type and StreamID, not by TSpec.** The halves' MaxFrameSize differs:
  the split's 217 (Table 4.4 at the entity's 8 channels), the fabric's 73 (the same formula at 2). The twin builds
  both datapaths at `TALKER_WIRE_CHANS_P`'s default of 2, where the shipping AX shape builds 8, and the fabric's
  source 0 declares its `LWSRP_TSPEC` word; which sets the 73 is not diagnosed. The deleted row pinned each half's
  value on its own and never compared the two. Reported here, not changed.
- The milan_dp README's SRP-transmit section still describes the boot-time Talker Failed of before #895 (the licence
  scenario's fixture); that leg is not this issue's.
- No firmware, RTL, lwSRP, mailbox-contract or CPU-budget-bound change.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
