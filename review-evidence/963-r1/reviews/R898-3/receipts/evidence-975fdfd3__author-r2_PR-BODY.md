[A819]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN for every gate that ran, each at the head named below. The local verification bar is **not complete**: the full
native Verilator sweep has not run, and is owed to the merge candidate. `pf-963-1` -> `dev-soft-core`, on PR #960's
reviewed flip head `dd163e41`, which `dev-soft-core` now holds (`854bd723`); `dd163e41` is the merge base. Head
`a18f0996`. The firmware is final at `25d3dd7a`. After it, `50d3f10e` re-anchors one plant, `4cca9569` is the design
doc, and `a18f0996` adds an illegal mapping of an existing stream to the edit definition's test, with its plant (test
only, round 2's answer to review suggestion S1).

- **The finding, fixed.** At 8x8/1if `aecp-largest-notice` has no work pass over THE SHARE in either arm that runs it.
  Graded strictly, so that a pass over THE SHARE fails the run, both arms are rc 0 at the head and rc 1 at the base.
- **Exact behaviour.** The CPU service-budget harness ran every group of every arm at 1x1/1if and 8x8/1if, base and
  head: 481 groups a tree, every save window included, every run rc 0. All 481 groups are the base's byte for byte,
  with nothing masked: every wire frame in order, publication write, TXC count, refusal and probe verdict.
- **No regression.**
  - The measured load is the base's exactly (0.48911 at 1x1/1if, 0.60082 at 8x8/1if).
  - Every held AECP record class is within its statement and none is above the base's.
  - Every image has the base's ROM and SRAM bytes.

**What ran, and at which head.** No firmware, RTL or `tb/` file changed after `25d3dd7a`
(`git diff --stat 25d3dd7a a18f0996`: `test_aecp.cpp`, `aecp_map_mutants.py`, the design doc).

| Gate | Head | Result |
|---|---|---|
| `aecp-largest-notice` at 8x8/1if, strict grade, both arms | `25d3dd7a` | rc 0, 0 of 106 over each; longest 149,307 and 153,071 (base rc 1, 2 of 108 each) |
| CPU service-budget harness, every group of every arm, both points, base and head; strict differential | `25d3dd7a` | every run rc 0; 481 of 481 groups exact, nothing masked |
| Record classes; measured load | `25d3dd7a` | RESULT: PASS; the load the base's exactly |
| Images: the 16 harness arm images; the target platform's split images | `25d3dd7a`; `50d3f10e` | the base's ROM and SRAM bytes; 8x8/1if 139,208 B, 58.0 RAMB36 |
| Firmware gate shard 0, the suites (`--shard 0/4`) | `25d3dd7a` | PASS: 88 suite arms. **Not re-run at the final head.** At `a18f0996`, its 18 AECP arms, the only arms that compile `test_aecp.cpp`, pass, after the gate's own inventory (`1848 live invocations`, shard sizes `[88, 827, 391, 542]`) |
| Firmware gate shard 1, the control plants (`--shard 1/4`) | `50d3f10e` | PASS: `mutants: 826 of 826 caught` |
| Firmware gate shard 2, the AECP campaign (`--shard 2/4`) | `50d3f10e`; `a18f0996` | PASS: 389 plants caught, 0 escaped. At `a18f0996` the campaign's 390 rows, `map-read-before-legal` among them, through its own entry point in 20 partitions (`aecp_mutants.py --shard i 20`): 390 caught, 0 escaped, each row once. The gate command itself was not run at `a18f0996` |
| Firmware gate shard 3, the SRP campaigns (`--shard 3/4`) | `50d3f10e` | PASS: 541 plants caught (359, 167 and 15 in its three campaigns), 0 escaped; and 2 dependency-pin controls refused |
| Coverage ratchet | `a18f0996` | `firmware coverage: PASS (40 files)`; `aecp_maps.c` 352/352 lines, 423/424 branches |
| Firmware-unit steps: tally, RV32, saved-state store suites | `50d3f10e` | rc 0 each |
| The twin, `make twin`, `make twin-plants` | `50d3f10e` | `twin: 0 finding(s)`; every plant refused by its words |
| Harness self-test | `b63c4179` | `self-test: 0 failures` (no `tb/` file changed since) |
| Portable gates: model gates, hot list, memory planner, split boot at both points and its plants | `50d3f10e` | rc 0 each |
| Docs workflow gate steps | `a18f0996` | 43 of 46 rc 0, the em-dash step among them (0 findings over 1 added line against `dd163e41`). `gate_24` (compiler-absent firmware controls) did not complete. The builder legs `gate_25_0` and `gate_25_1` did not run. All three were rc 0 at `4cca9569`, and neither their step scripts nor `sw/builder/` names `sw/firmware/ctrl/test/` |
| Full native Verilator sweep (four shards) | none | **NOT RUN. Owed to the merge candidate** (CONTRIBUTING 2.1 step 7) |

**The plant tally, each shard's own unit, counted from the lines the gate prints.** At `50d3f10e` the three plant
campaigns caught 1,756 plants: 826 (shard 1), 389 (shard 2) and 541 (shard 3). None escaped. Beside them, shard 3
refused 2 dependency-pin controls. Shard 0's 88 are suite arms, not plants. Round 1 published "1,846 plants caught",
which added those 88 suite arms and the 2 pin controls to the 1,756 plants. At `a18f0996` the AECP campaign has 390
plants and caught all 390.

## Linked Issue / roles

Closes #963
Relates to #665

Executor: `[A819]`
Internal cleared-context reviewer: `[R898]`
External reviewer: `[R899]`

## Description

**The finding (#963; #872's round 3, Item 2).** At 8x8/1if, the flip's shipping shape, `aecp-largest-notice` had 2 of
108 work passes over THE SHARE (2.0 ms, 200,000 CPU cycles at 100 MHz): the passes that take its REMOVE and
ADD_AUDIO_MAPPINGS of 63 mappings.

| Arm | REMOVE's pass | ADD's pass |
|---|---:|---:|
| answering-ports | 222,104 | 215,566 |
| declaring-outputs | 227,112 | 220,503 |

**The cause: which notice.** Each such pass carries three pieces of work:
- the polls' base;
- the command's record;
- the poll item that sends the 550 B CHANGE_MAP notice to 15 controllers. That notice is the unsolicited
  REMOVE/ADD_AUDIO_MAPPINGS response (`0x802d`, `0x802c`) for STREAM_PORT_OUTPUT 0, carrying 63 copies of one mapping.

**The cause: which map walk.** At 8x8 the input maps have capacity 0, so the group edits the output map. The edit's
check loop walks the command's 63 mappings (`aecp_maps.c`, `aecp_map_command`). Each mapping's turn ran the output
port's running check (`idle`, #943): a brief observation of the mapping's STREAM_OUTPUT through the stream port, 63
observations of one stream an edit. A committed-PC trace of the four passes:

| Arm | `aecp_stream_read` calls a pass | Their cycles, inclusive |
|---|---:|---:|
| answering-ports | 63 | 55,052 |
| declaring-outputs | 63 | 56,005 |

Each call also zeroed the 48-byte observation twice. The record did that at every mapping, an input port's too. In the
product each observation is a datapath window read.

**The cut** (`sw/firmware/ctrl/aecp/aecp_maps.c`). The check observes each stream an edit maps once, at the first of
its mappings to reach the check, and holds it for the rest of the edit:
- **Its table.** One bit a stream, in a zero-initialized table local to the edit.
- **Its observation.** `aecp_stream_read` makes it, as before, now zeroing it once. Each observation calls the port as
  before: a brief observation of the mapping's STREAM_OUTPUT.
- **Its refusal.** A stream found running, or whose observation goes unanswered, refuses the edit at that mapping, as
  before. The table dies with the record, so a later mapping of a held stream is only ever checked after that stream
  was found idle in the same record, which nothing else runs beside.
- **What does not change.** Each status, the map, the response and every notice. The work becomes one observation a
  stream the edit maps, at most the shape's STREAM_OUTPUTs, for any legal-length edit.
- **What else does not change.** THE SHARE, every stated cost, the rows' limits, the mailbox contract and the RTL.

**Why this form.** Two earlier forms were measured and set aside. The first made the observation through the running
check SET_CONFIGURATION uses (`running`). The split image's hot list does not hold `running`, so the one-row output
edit's first observation fetched cold, and 1x1/1if's held paced record went over its 315 us. The second kept the table
in the edit's struct: `aecp_map_command` grew 36 B and moved the code after it, and the complete measured-load audit
found 8x8/1if's load 0.6008 -> 0.6066 by placement alone. In the form kept, `aecp_map_command` is the base's size and
every loaded byte outside it is the base's in all 16 harness arm images.

**The check order, held by a test (`a18f0996`).** Each mapping's checks run in command order: its legality first, then
the running check. Until `a18f0996`, the edit definition's only illegal mapping named stream 65535, which no descriptor
holds, so the port was never reached in either order. A running check moved before the legality check went uncaught.
The seeded edits now also map an existing stream at the channel one past its format's: refused before its port is read.
The first 4,000 seeded edits are drawn exactly as before, and the 16 other rows the test grades are each caught on
their own words, as before. A further 4,000 edits carry the new mapping, and 86 of them are output edits refused at
such a mapping of a stream not yet read.
The new plant `map-read-before-legal` moves the running check before the legality check. It is caught on the test's
words, and it escapes against the test as it was at `4cca9569`.

**The result at the head.**

| 8x8/1if, `aecp-largest-notice` | Base `dd163e41` | Head `25d3dd7a` |
|---|---:|---:|
| answering-ports: work passes over THE SHARE | 2 of 108 | **0 of 106** |
| answering-ports: longest work pass | 222,104 | **149,307** |
| answering-ports: largest record | 163,316 | 90,258 |
| declaring-outputs: work passes over THE SHARE | 2 of 108 | **0 of 106** |
| declaring-outputs: longest work pass | 227,112 | **153,071** |
| declaring-outputs: largest record | 167,691 | 93,591 |

| Held AECP record class (record_classes.py, complete) | 1x1/1if base -> head | 8x8/1if base -> head | Statements |
|---|---|---|---|
| long (the largest legal command) | 91,641 -> 82,546 | 163,316 -> 90,258 | 975 / 1,720 us |
| paced | 29,993 -> 29,822 | 56,492 -> 56,327 | 315 / 685 us |
| other | 23,726 -> 23,726 | 20,202 -> 20,202 | 250 / 265 us |

| File | What |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_maps.c` | `idle(a, observed, input, r)`: one observation a stream an edit, zeroed once; the table local to the edit |
| `sw/firmware/ctrl/test/test_aecp.cpp` | `Core.MapEditsAreTheirDefinitionRowForRow`: the definition reads the port once a stream, its legal mappings over two streams, and its illegal mappings also name an existing stream past its format's channels; new `Core.MapEditWorkObservesEachOutputStreamOnce` (the work arm too) |
| `sw/firmware/ctrl/test/aecp_map_mutants.py`, `aecp_output_mutants.py` | five new plants (`map-stream-*`, `map-read-before-legal`); two rows caught by the edit's map; two re-anchored where this fix rewrote their text |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | "The running check, once a stream" |

## Authoritative references

- FR_NFR.md 3.4.1 (T_svc, 20 ms) and `ctrl_loop.h` THE SHARE (2.0 ms a pass).
- IEEE 1722.1-2021 7.4.45 and 7.4.46 (ADD and REMOVE_AUDIO_MAPPINGS), 9.2.2.6 (the largest legal command).
- Milan v1.2 5.4.2.27 and 5.4.2.28: without TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING, a mapping that references a channel
  of a currently streaming Stream Output is invalid (BAD_ARGUMENTS, no mapping changed). The condition is the Stream
  Output's, so one observation of each per command decides it for every one of its mappings. Milan v1.2 5.4.5
  (unsolicited notifications).
- #894 (the bounded map work, the running check, `LONG_RECORD_US`); #943 (the output map's running check);
  #872 issuecomment-7073387312, Item 2.
- [Split control memory](../docs/design/SPLIT_CONTROL_MEMORY.md), "The running check, once a stream".

## How to get into the same state

```sh
git fetch origin pf-963-1 && git checkout --detach a18f0996
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

The CPU service-budget harness needs the prerequisites in its README (the product LiteX tree, the pinned RV32 SDK,
Verilator 5.050; `COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).

## How to validate

```sh
# the cut's tests and plants (AECP's campaign)
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
# the group at 8x8/1if in both arms that edit the output map, graded so a pass over THE SHARE fails the run
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <scratch>/b-ap --variant answering-ports \
  --groups aecp-largest-notice --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <scratch>/b-do --variant declaring-outputs \
  --groups aecp-largest-notice --record-budget-findings
```

Expected result / pass criteria:
- the shard passes with every plant caught (`map-stream-*` and `map-read-before-legal` among them);
- each harness run exits 0, prints `0 of 106 work passes over the per-pass share`, and has no `SHARE` line. At the
  base the same commands exit 1 with `2 of 108`.

## Known limitations / out of scope

- **The port's reads change.** The stream port is read once a stream an edit maps, not once a mapping. Every status,
  the map, the response and the notices are unchanged. Only a window that answers a stream's first read in a record and
  not a later one could tell the two apart: the base then refused at the later mapping, while the head keeps the first
  answer for the edit.
- **Not run at the source head, and owed to the merge candidate:** the full native Verilator sweep (four shards).
  CONTRIBUTING 2.1 step 7 requires it, with Yosys and the other banks, on the candidate merge tree. This PR's record is
  the source head's. A future candidate result is the candidate's and is not claimed here.
- **Not re-run at the final head `a18f0996`:** the firmware gate's shards as gate commands (shard 0 ran at `25d3dd7a`,
  shards 1 to 3 at `50d3f10e`). At `a18f0996` only shard 0's AECP arms and shard 2's whole table ran, as the table above
  says. Also the docs workflow's `gate_24` and its two builder legs.
- **Not this lane's.** The other base findings of #872's round 3.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (not yet: the full native Verilator sweep has not run, owed to the merge candidate; see the table in Status)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
