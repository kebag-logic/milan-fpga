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

GREEN. `pf-963-1` -> `dev-soft-core`, on PR #960's reviewed flip head `dd163e41`: once #960 lands, this PR's diff is
this lane's commits only. Head `4cca9569`; the firmware is final at `25d3dd7a` (`50d3f10e` re-anchors one plant,
`4cca9569` is the design doc).

- **The finding, fixed.** At 8x8/1if `aecp-largest-notice` has no work pass over THE SHARE in either arm that runs it.
  Graded strictly, so that a pass over THE SHARE fails the run, both arms are rc 0 at the head and rc 1 at the base.
- **Exact behaviour.** The CPU service-budget harness ran every group of every arm at 1x1/1if and 8x8/1if, base and
  head: 481 groups a tree, every save window included, every run rc 0. All 481 groups are the base's byte for byte,
  with nothing masked: every wire frame in order, publication write, TXC count, refusal and probe verdict.
- **No regression.**
  - The measured load is the base's exactly (0.48911 at 1x1/1if, 0.60082 at 8x8/1if).
  - Every held AECP record class is within its statement and none is above the base's.
  - Every image has the base's ROM and SRAM bytes.
- **Gates:** the firmware gate's four shards (1,846 plants caught, none escaped); the firmware-unit steps and the
  coverage ratchet; the twin and its plants; the harness self-test; the portable gates; the docs workflow.

## Linked Issue / roles

Closes #963
Relates to #665

Executor: `[A819]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

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
- **Its observation.** `aecp_stream_read` makes it, as before, now zeroing it once. The port is called exactly as
  before.
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
| `sw/firmware/ctrl/test/test_aecp.cpp` | `Core.MapEditsAreTheirDefinitionRowForRow`: the definition reads the port once a stream, its legal mappings over two streams; new `Core.MapEditWorkObservesEachOutputStreamOnce` (the work arm too) |
| `sw/firmware/ctrl/test/aecp_map_mutants.py`, `aecp_output_mutants.py` | four new plants; two rows caught by the edit's map; two re-anchored where this fix rewrote their text |
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
git fetch origin pf-963-1 && git checkout --detach 4cca9569
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
- the shard passes with every plant caught (`map-stream-*` among them);
- each harness run exits 0, prints `0 of 106 work passes over the per-pass share`, and has no `SHARE` line. At the
  base the same commands exit 1 with `2 of 108`.

## Known limitations / out of scope

- **The port's reads change.** The stream port is read once a stream an edit maps, not once a mapping. Every status,
  the map, the response and the notices are unchanged. Only a window that answers a stream's first read in a record and
  not a later one could tell the two apart: the base then refused at the later mapping, while the head keeps the first
  answer for the edit.
- **Not run.** The full native Verilator sweep (four shards). Four CPU ranges were never free.
- **Not this lane's.** The other base findings of #872's round 3.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
