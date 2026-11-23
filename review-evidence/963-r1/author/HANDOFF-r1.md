# HANDOFF, lane 963 round 1 ([A819])

STATUS (2026-11-23 10:30 CET): DONE. REVIEW READY posted on #963 (issuecomment-7096625846) for head `4cca9569`;
TAKEN is issuecomment-7076985987. Every gate green (table below). No unit of this lane is running. Nothing pushed;
the manager pushes `pf-963-1` and opens the PR from `PR-BODY.md` once #960 lands `dd163e41` in `dev-soft-core`.
ETA: none (done).

Lane: /data-2/milan/lanes/fix-963, branch `pf-963-1`, on PR #960's reviewed flip head `dd163e41`. Head `4cca9569`
(firmware final at `25d3dd7a`; `50d3f10e` re-anchors one AECP plant, test only; `4cca9569` is the design doc). Nothing
pushed. The host crashed at 00:39; every measurement and gate it cut off was re-run from clean state after 05:45, and
no partial result is counted (below).

## Cause (which notice, which map walk)

- **The notice.** The over-share passes take `aecp-largest-notice`'s REMOVE and ADD_AUDIO_MAPPINGS of 63 mappings at
  8x8/1if (`0x802d`, `0x802c`). The response and each notice are 550 B; each notice goes to 15 controllers and names
  STREAM_PORT_OUTPUT 0 with 63 copies of one mapping (`receipts/target-current/notice-identity.json`). At 8x8 the
  input maps have capacity 0, so the group edits the output map.
- **The map walk.** The edit's check loop walks the command's 63 mappings (`aecp_maps.c`, `aecp_map_command`). At each
  mapping it ran the output port's running check (`idle`, #943): a brief observation of the one STREAM_OUTPUT through
  the stream port, 63 an edit.
- **The trace.** A committed-PC trace of the base's four over-share passes (`receipts/cause/`):

| Arm | Pass | Cycles | `aecp_stream_read` calls | Their cycles, inclusive |
|---|---|---:|---:|---:|
| answering-ports | REMOVE's | 222,104 | 63 | 55,052 |
| answering-ports | ADD's | 215,566 | 63 | 55,052 |
| declaring-outputs | REMOVE's | 227,112 | 63 | 56,005 |
| declaring-outputs | ADD's | 220,503 | 63 | 56,005 |

Each call site also zeroed the 48-byte observation before `aecp_stream_read` zeroed it again, at every mapping, input
ports included. Each pass is the polls' base, the command's record and the poll item that fans the notice out.

## Changes (file:line, reason)

| Commit | What |
|---|---|
| `b9b5704b` | the cut, its tests and its plants (first form: a per-edit table of streams in `struct edit`) |
| `9504ba5d` | that table first in `struct edit` (a short stack offset) |
| `b63c4179` | the observation through the running check `aecp_running`: product image within its bank, but the cold `running` put 1x1/1if's held paced record 68 cycles over its statement |
| `e54e064a` | design doc |
| `e9627b31` | the observation through the hot `aecp_stream_read` again: every held record within; but the complete measured-load audit found 8x8/1if's load 0.6008 -> 0.6066 by placement (`aecp_map_command` +36 B moved the code after it) |
| `1b3e27ce`, `9860395a` | design doc; a check-loop comment |
| `25d3dd7a` | **the final firmware**: the table a zero-initialized local array, `idle` given the known input mode; `aecp_map_command` is the base's size and every loaded byte outside it the base's in all 16 harness arm images (`receipts/placement-correction/image-proof.json`) |
| `50d3f10e` | `aecp_map_mutants.py:260`: `edit-before-the-checks` re-anchored (its old anchor was the comment this fix rewrote; same planted store, same assertion) |
| `4cca9569` | the design doc at the final figures |

Final code (`git diff dd163e41`: `aecp_maps.c`, `test_aecp.cpp`, `aecp_map_mutants.py`, `aecp_output_mutants.py`,
the design doc):
- `sw/firmware/ctrl/aecp/aecp_maps.c:275` `idle(a, observed, input, r)`.
  - An output port's running check observes each stream once an edit, at the first of its mappings to reach the
    check: the stream's bit is set, then `aecp_stream_read` makes the brief observation, zeroing it once.
  - A stream found running or unanswered refuses the edit at that mapping (the table dies with the record), so a later
    mapping of a stream the table holds is only checked after the stream was found idle in the same record.
  - Input ports read nothing, as before.
  - The word index is reduced to the table (`% MAP_IDLE_WORDS`, `:179`).
- `aecp_maps.c:485`: `uint32_t observed[MAP_IDLE_WORDS] = {0};` cleared with the slots. `:534`: the check loop passes
  it, its order unchanged.
- `sw/firmware/ctrl/test/test_aecp.cpp:2867` `Core.MapEditsAreTheirDefinitionRowForRow`: the definition reads the port
  once for each output stream it reaches, its legal mappings over two streams.
- `test_aecp.cpp:2985` `Core.MapEditWorkObservesEachOutputStreamOnce` (new; the work arm runs it too). ADD and REMOVE
  of 63 over two streams read the port twice, briefly, in order; a running or unanswered stream refuses at its first
  mapping and changes nothing; the next edit observes again.
- `sw/firmware/ctrl/test/aecp_map_mutants.py:122-138`: four new plants. `:106, 110`: `map-port-rows-unread`,
  `map-owners-unread` caught by the edit's map. `aecp_output_mutants.py:76`: `map-idle-reads-whole` at the new site.
- `docs/design/SPLIT_CONTROL_MEMORY.md:2628`: "The running check, once a stream (#963)".

## New checks (planted mutant, failing words)

| Plant | Test | Failing words |
|---|---|---|
| `map-stream-observed-every-mapping` (the bit never set) | `Core.MapEditWorkObservesEachOutputStreamOnce`, `Core.MapEditsAreTheirDefinitionRowForRow` | "an edit observes each stream it maps once, in its order"; "the edit reads its port once for each output stream its definition reaches" |
| `map-stream-idle-uncleared` (the table seeded stale, `{UINT32_MAX}`) | `Core.MapEditWorkObservesEachOutputStreamOnce` | "an edit observes each stream it maps once, in its order" |
| `map-stream-idle-one-bit` (every stream one bit) | `Core.MapEditWorkObservesEachOutputStreamOnce` | "a stream found running refuses the edit at its first mapping" |
| `map-stream-running-accepted` (`running` ignored) | `Core.MapEditWorkObservesEachOutputStreamOnce` | "a stream found running refuses the edit at its first mapping" |
| the base's `aecp_maps.c` (`dd163e41`) | both tests | each fails on its words (`receipts/tests/`) |

## Gate table

| Gate | Head | Result | Receipt |
|---|---|---|---|
| `aecp-largest-notice` at 8x8/1if, strict grade (a pass over THE SHARE fails the run) | `25d3dd7a` | answering-ports rc 0, 0 of 106 over, longest 149,307; declaring-outputs rc 0, 0 of 106 over, longest 153,071 (base: rc 1 and rc 1, 2 of 108 over each, 222,104 and 227,112) | `share/strict-regrade-final.md` |
| CPU service-budget harness, every group of every arm at 1x1/1if and 8x8/1if, base and head (481 groups a tree, every save window) | `25d3dd7a` | every group rc 0 under the formal options; the process checkpoint driver calibrated in all 16 arms (an ordinary complete log byte-identical) | `harness-final/` |
| Strict differential, nothing masked, frame order kept per channel | `25d3dd7a` | **481 of 481 groups exact**: every wire frame, publication write, TXC count, refusal, probe status and verdict the base's; the target exact in all 5 point-arm combinations | `harness-final/strict-diff.txt` |
| Record classes, complete | `25d3dd7a` | RESULT: PASS. 1x1/1if: long 82,546 (base 91,641), paced 29,822 (29,993), other 23,726 (23,726). 8x8/1if: long 90,258 (163,316), paced 56,327 (56,492), other 20,202 (20,202). Reported only, as at the base: 1x1/1if declaring-outputs paced 30,688 (30,839) | `harness-final/record-classes-head.txt`, `harness-complete/base/` |
| Measured load (#872's model on this lane's complete measurements) | `25d3dd7a` | 1x1/1if 0.48911, 8x8/1if 0.60082, **the base's exactly** (bounds 0.70, 0.75) | `harness-final/load-comparison.json` |
| Owner model gates: load gate, flip check at 1x1/1if and 8x8/1if, shape table | `50d3f10e` | rc 0, outputs byte-identical to the base's (no stated cost moved) | `gates-final2/portable-50d3f10e/` |
| Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4` | `25d3dd7a` (0), `50d3f10e` (1-3) | PASS each: plants caught 88, 826, 389 (AECP's, the four new among them), 543; none escaped. Shard 0's partition holds no plant `50d3f10e` touches | `gates-current/firmware-0/`, `gates-final2/firmware-shard*/` |
| Firmware-unit steps: tally, RV32, saved-state store suites, coverage ratchet | `50d3f10e` | rc 0 each; `firmware coverage: PASS (40 files)` | `gates-final2/firmware-unit-50d3f10e/` |
| The twin, `make twin`, `make twin-plants` | `50d3f10e` | `twin: 0 finding(s)`; every plant refused by its words | `gates-final2/twin-50d3f10e/` |
| Harness self-test | `b63c4179` (no file under `tb/` changes) | `self-test: 0 failures` | `gates/twin-selftest/` |
| Images: the 16 harness arm images | `25d3dd7a` | ROM and SRAM bytes the base's in every arm; tiles 43.0 and 56.0 | `images/harness-images-final.md` |
| Images: the target platform's split images | `50d3f10e` | 8x8/1if 139,208 B ROM, the base's, 58.0 tiles, its ledger 58.0; 1x1/1if 126,432 B, 45.0 | `images/product-images-final.md` |
| Portable gates (diff check, em dash, idiom, hygiene, test evidence, naming, fail-fast, TODO, bare-metal, docs, hot list, model gates, memory planner, split boot at both points and its plants) | `50d3f10e`; the doc-reading ones again at `4cca9569` | rc 0 each (29 and 9) | `gates-final2/portable-*` |
| Docs workflow's gate steps | `4cca9569` | 45 of 46 gate steps rc 0 in the workflow pass; the em-dash step, which reads the hosted event, rc 0 against the PR's merge base `59b09884` (0 findings over 181 added lines in 33 pages); the no-git docs gate also on a fresh checkout, rc 0 | `gates-final2/docs-4cca9569/` |

## Notes

- **The crash (00:39).** Killed: the head's harness campaign (5 of 481 groups done), shards 1 to 3, the auxiliary gates,
  the docs gates. All re-ran from clean state after 05:45. The partial campaign outputs were set aside, never counted, and deleted
  once the re-run completed. The shards ran on fresh clones, one each.
- **Supersedes.** The `e9627b31` evidence (`gates-final/`, `harness/`, `harness-complete/`) is the intermediate head's.
  Its unmasked differential needed two timing equivalences (a grandmaster flood identity, AECP notice order across
  descriptors); the final form needs none.
- **Not run.** The full native Verilator sweep (four shards) was prepared but never had four free CPU ranges (another
  lane's candidate shards hold 0-63). No placeholder booking was made.
- **CPU.** With the picker finding no free range, this lane's units ran at the session's own affinity.
- **The one behaviour change.** The port's reads are one a stream an edit maps, not one a mapping. Only a window that
  answers a stream's first read in a record and not a later one could tell the two apart.

REVIEW READY 4cca956932073b3f704f12f81c53f2934cfa215c
