# HANDOFF r1 — lane 950 + 954 ([A811])

STATUS (02:30 CET, 2026-11-22): DONE, REVIEW READY at `287ca1ee` (9 commits on the flip train's head `15168e14`);
firmware final since `c7cfba76`. Every gate PASS at the final head or on byte-identical images (section 5): the full
CPU re-measure at both points holds every statement but one 1x1/1if AECP record, raised by the usual rule (255 us,
every row within its bound); the platform's 8x8 one-interface ROM entry raised to 58.5 by the owner's rule. The only
refusals are the docs workflow's three RV32 SDK install-verify steps, which this host's SDK refuses on the base too.

Branch `pf-950-954-1` from the flip train head `15168e14` (PR #945, reviewed, not merged into dev-soft-core).
Posted: `[A811] TAKEN`, #950 issuecomment-7062169345 (text: TAKEN-comment.md); `[A811] REVIEW READY`, #950
issuecomment-7072197641 (text: REVIEW-READY-comment.md). Nothing pushed; no PR (the manager's:
PR-BODY.md, base dev-soft-core, Closes #950, Closes #954, Relates to #665).

## 1. Task
- #950: the AECP core repeats the bound and running checks when it re-runs a waiting SET_STREAM_FORMAT (input 0,
  CRF input, every STREAM_OUTPUT); #947's serialization for inputs 1-7 stays. IEEE 1722.1-2021 7.4.9, 8.2.
- #954: ACMP GET_TX_STATE sets REGISTERING_FAILED with a Listener Asking Failed registered for the Talker's stream,
  drops it when it goes (Milan v1.2 Table 5.47), every output, both shapes; from #943's registrar state.

## 2. Commits (one-line subjects)
| Commit | What |
|---|---|
| `9ed4fc95` | tests first: `Core.AWaitingFormatChangeMakesItsRunningCheckAgainOnceApplied`; `Streams.S13`, `S14`, `T1` |
| `f41f6fff` | #950 core fix (aecp.c, aecp_commands.c, aecp_internal.h); aecp.h's and the AECP README's contract; the platform's wrapped-port comments |
| `4dece416` | #954 platform fix (ctrl_plat.c `source()`); the platform README |
| `f22c1454` | plants: 7 AECP rows, 5 waiting-command rows re-anchored on the core's new status; 6 control rows; READMEs; test_ctrl_firmware.py's arm text |
| `c7cfba76` | `aecp_again` names the waiting command by the change it noted (the shape the budget probes kept, section 6); its 4 plants re-anchored |
| `f90884e6` | the Python idiom gate: the AECP campaign's #950 rows in `aecp_again_mutants.py` (aecp_mutants.py 1,023 -> 993 lines), the sink table's stream rows in `streams()` (`mutants()` was 113 lines) |
| `4a08c90d` | the platform's 8x8 one-interface ROM entry 58.0 -> 58.5 RAMB36 by the owner's rule of 2026-11-15 (section 7) |
| `a00a3c96` | the memory test's ledgered product point at 58.5, refused at 59.0; the plan at this head in the design doc and both READMEs |
| `287ca1ee` | 1x1/1if's AECP record raised by the rule to 255 us (`load_grade.py`, both columns); the design doc's record of the re-measure (section 13) |

## 3. Changes (file:line at `287ca1ee` — reason)
- `sw/firmware/ctrl/aecp/aecp_commands.c:134-143` `aecp_again`: the checks a waiting command makes again once the
  platform applied it: a SET_STREAM_FORMAT's own running check (`running`, brief: a STREAM_INPUT bound, a
  STREAM_OUTPUT running), so a bind or start that settled during the wait refuses it with its dispatch's status
  (STREAM_IS_RUNNING; ENTITY_MISBEHAVING if the stream cannot be observed). Named by the change the waiting command
  noted: only SET_STREAM_FORMAT notes `AECP_CHANGE_FORMAT`, and nothing notes while one waits (aecp_rx refuses every
  change; aecp_poll returns before the lock expiry while waiting); the base's redo already re-notes from these fields.
  The other AECP_WAITS commands are unchanged.
- `sw/firmware/ctrl/aecp/aecp.c:957-976` the waiting command's end in `aecp_poll`: taken, its checks made again;
  passed, done again, answered, notified; refused or not taken in time, undone, the check's status (or
  ENTITY_MISBEHAVING), no notice; the face given the values in force (unchanged).
- `sw/firmware/ctrl/aecp/aecp_internal.h:42-44`, `aecp.h:203-216`, `aecp/README.md`: the declaration and contract.
- `sw/firmware/ctrl/plat/ctrl_plat.c:94-108` `source()` (#954): `asking_failed` while SRP's registrar on the source's
  interface holds a Listener for its stream that is not Ready or Ready Failed (`listener_present && !registered`, the
  state #943's GET_STREAM_INFO reads), whatever the Talker declares, as the release processor's talker answers it
  (`KL_acmp_talker.sv` `rf_live_w`). The ACMP core maps it to REGISTERING_FAILED.
- `sw/firmware/ctrl/plat/ctrl_plat.c:158-226` comments: after an applied wait the core's next change is that change,
  done again or refused with the values in force; #947's serialization for inputs 1-7 unchanged.
- `sw/firmware/ctrl/plat/README.md`: the source port's Asking Failed; the stale "asking-failed reads false" limit
  removed; the platsinks tests; the 8x8 images' block RAM.
- Tests: `test/test_aecp.cpp:1681-1747` (the core test, every STREAM_INPUT and STREAM_OUTPUT of the configuration);
  `test/test_plat_sinks.cpp:1074-1336` (`Streams`: S13, S14, T1 at 8x8/1if and 1x1/1if; the ACMP and SRP channels'
  receive rate refilled before each injected frame, the model's token bucket).
- Plants: `test/aecp_again_mutants.py` (new, 7 rows, appended to aecp_mutants.DEFECTS), `aecp_mutants.py` (5 rows
  re-anchored), `sink_mutants.py` `streams()` (6 rows).
- Budget and ledger: `tb/verilator/ctrl_service_budget/load_grade.py:217-229, 268-279` (1x1/1if record.aecp 255);
  `sw/litex/ctrl_memory.py:329-353` (58.5); `sw/litex/ctrl_memory_ledger.py`, `test_ctrl_memory.py` (its cases);
  `docs/design/SPLIT_CONTROL_MEMORY.md` (the ledger tables, the plan at this head, section 13's record);
  `tb/verilator/ctrl_split_boot/README.md`.

## 4. New checks (planted mutant — failing words)
Failing first (base + the test commit alone): `receipts/firmware/failing-first-*.txt` (S13 at input 0 and the CRF
input, S14 at every output, T1 at every output, both shapes; the core test at input 0).

| Plant | Campaign / arm | Failing words |
|---|---|---|
| `again-unchecked` (the shipped core) | AECP, app 1x1 if2 | "a waiting SET_STREAM_FORMAT makes its running check again once applied: STREAM_INPUT 0, bound meanwhile"; "STREAM_INPUT 0: the check is made again" |
| `again-other-command` | AECP | the first of those |
| `again-input-judged-by-streaming` | AECP | the first of those |
| `again-unobservable-taken` | AECP | "...: STREAM_INPUT 0, not observable once applied" |
| `again-refusal-done-again` | AECP | "a refused waiting SET_STREAM_FORMAT stays undone: STREAM_INPUT 0, bound meanwhile" |
| `again-refusal-notified` | AECP | "STREAM_INPUT 0, bound meanwhile: one final response, no notification" |
| `again-refusal-misbehaving` | AECP | the status words |
| 5 re-anchored: `waiting-change-not-redone`, `-success-not-notified`, `-failure-notified`, `-failure-not-republished`, `-failure-reports-the-request` | AECP | their own words, unchanged |
| `again-unchecked-onto-a-stream` (the shipped core) | control, platsinks8 + platsinks1 | "S13 ... refused STREAM_IS_RUNNING once acknowledged: input 0"; "S14 ...: output 0"; both shapes |
| `again-of-stream-zero` | control, platsinks1 | "S13 ...: input 1"; "S14 ...: output 1" |
| `asking-failed-unreported` (the shipped platform) | control, platsinks8 + 1 | "T1 REGISTERING_FAILED while a Listener Asking Failed is registered ... (Table 5.47): output 0, declaration 1" |
| `asking-failed-any-listener` | platsinks8 | "...: output 0, declaration 2" |
| `asking-failed-without-a-listener` | platsinks8 | "T1 no REGISTERING_FAILED with no Listener registered: output 0" |
| `asking-failed-of-output-zero` | platsinks8 | "T1 no other output carries output 0's Listener: output 1, Asking Failed" |

Not planted, equivalent at one interface (every arm the platform has is 1if): the registrar of interface 0 for the
source's own.

## 5. Gate table (receipts under receipts/, INDEX.md)
| Gate | Head | Result | Receipt |
|---|---|---|---|
| New tests fail first | base + `9ed4fc95` | FAIL at every stream named, both shapes | firmware/failing-first-* |
| New and re-anchored plants | `f22c1454`, `c7cfba76`, `f90884e6` | all caught (12/12, 6/6 + 1, 5/5, the moved 7/7) | firmware/plants-* |
| Firmware gate, 4 shards | `c7cfba76` | PASS: 1,856 invocations, control 832/832, AECP and SRP campaigns, 0 escaped | gates/firmware-gate-c7cfba76-s* |
| Firmware gate, 4 shards | `287ca1ee` | PASS: 1,856 invocations, control 832/832, 0 escaped | gates/firmware-gate-287ca1ee-s* |
| fw_coverage --selftest, --check | `c7cfba76` | PASS (40 files; aecp.c, aecp_commands.c 100 %; ctrl_plat.c 100 % after exclusions) | gates/fw-coverage-c7cfba76.txt |
| Firmware boundary, no Verilator / Verilator | `f90884e6` | PASS (3,849 / 1,240 compiled sources) | gates/boundary-* |
| Twin, twin-plants, twin-maps, twin-maps-plants | `c7cfba76` | PASS: 0 findings, 32 plants refused, the maps leg and its plant | twin/ |
| Release (all-fabric) image | base vs `c7cfba76` | IDENTICAL (bios.bin, disassembly, stripped ELF; the full ELF's debug paths differ) | release/ |
| plat_ledger | base, `f90884e6`, `4a08c90d` | base PASS; `f90884e6` FAIL 8x8-if1 (40 B past 58.0); `4a08c90d` PASS (58.5 by the rule) | ledger/ |
| test_ctrl_memory | `a00a3c96` | PASS, 0 failures | ledger/ |
| Docs workflow steps | `c7cfba76`, `a00a3c96` | `c7cfba76`: the idiom gate (fixed by `f90884e6`); `a00a3c96`: every step rc 0 but the 3 RV32 SDK install-verify steps, which refuse identically on the base (this host's SDK has no provenance receipt) | docs/ |
| Docs workflow steps | `287ca1ee` | 56 steps rc 0; the 3 RV32 SDK install-verify steps refuse as on the base; tree clean after | docs/docs-workflow-steps-287ca1ee.txt |
| CPU budget, tight statements probed | `c7cfba76` | section 6 | budget/tight-probes-1x1-8x8.txt, layout-search-1x1.txt |
| CPU budget, full re-measure | `c7cfba76`'s images (= `287ca1ee`'s) | 1x1/1if: 0 of 69 statements exceeded; the AECP records by class fail only the SET_STREAM_INFO record (255 by the rule vs 250) and PASS at the raised record; 241 groups, 0 refusals, the 14 held-egress misses, 0 of 384,551 passes over the share. 8x8/1if: 0 of 69 exceeded, the records by class PASS; 240 groups, 0 refusals, the 14 held-egress misses (egress_ledger PASS), the largest legal command's 4 passes over the share as on the train | budget/cpu-table-c7cfba76.md, groups-and-findings.txt, record-classes-*, survey-*, egress-ledger-8x8-1if.txt, image-hashes.txt |
| flip_grade --check, load_grade --check, shape_costs --check | `287ca1ee` | PASS at both points; 1x1/1if rows: last 127.43/130, ACMP 29.15/30, txL 47.98/49, load 0.512/0.70; 8x8/1if load 0.744/0.75, THE TRANSMIT 76.81/77 | budget/flip-grade-*-287ca1ee.txt |
| Harness self-tests | `287ca1ee` | run.py --self-test 0 failures; record_classes 26/26; flip_grade 616/616 | budget/harness-selftests-287ca1ee.txt |

## 6. The CPU budget: placement, and one statement over at 1x1/1if
- Base `15168e14`'s budget images are byte-identical to the train's measured `8c5e2b4f` (1x1/1if) and `92de01f7`
  (8x8/1if); the final head's are byte-identical to the measured `c7cfba76`'s (image-hashes.txt).
- The change runs only at a waiting command's end, which no group reaches, but moves code: `aecp_poll` +20 B (hot,
  every hot function after it 20 B later), `aecp_again` 40 B (cold code 60 B later). A committed-PC trace of the
  dearest paced map edit shows the same 4,030 instructions at the same addresses at base and in a shape whose hot
  code does not move, 231 cycles apart: the fetch L1's state when the record starts follows the cold code's place.
- Shapes measured at 1x1/1if (layout-search-1x1.txt): the paced map edit 29,960-30,224 (base 29,993, 30,000 the most
  315 us holds) and the SET_STREAM_INFO record 23,380-23,858 (base 23,726, 23,809 the most 250 holds). The kept shape,
  the simplest, is the only one measured with the map edit within 315; its SET_STREAM_INFO record is 23,858, 255 us by
  the rule, so 1x1/1if's `record.aecp` is raised to 255 by the usual rule (the train's practice, step 10 `0cfe1ddc`
  and ruling item 4's raise of placement-moved costs). Every row holds; no bound moves.

## 7. Notes / decisions
- Scope: SET_STREAM_FORMAT only (the issue's title and acceptance). SET_CONFIGURATION and SET_STREAM_INFO wait the
  same way without repeating their bound/running checks (`any_running`, `info.running`): reported for a new Issue,
  not changed (stated in TAKEN).
- The platform image's ROM ledger at `f90884e6`: FAIL at 8x8/1if, rom 139,304 B, 40 B past the 139,264 B that 58.0
  holds (+96 to +104 B at every point, `sram` and `ctrl_plat` unchanged). By the owner's rule of 2026-11-15 (#665
  issuecomment-6892332745: an image past its entry raises it to its measured size at the next half tile, as debt owed
  to S14), the entry is 58.5 (`4a08c90d`), refused at 59.0; ROM debt 2.5 RAMB36. Read for the platform image alone:
  no CPU-budget image, twin point or release image moves with it.
- #954 is the platform's port, so no CPU-budget image moves for it; the size fixture's source port stays a stub.
- The twin's scenario registers no Listener, so it does not exercise #954; no twin row is owed.
- CPU etiquette: the re-measure's units each ran on a range cpu_ranges.py picked. The session's own share of it ran
  with the session's 0-95 affinity until 18:57, so it also took time on other lanes' booked ranges; from 18:57 every
  measurement process of the session was pinned to the session pool, 64-95, and their children inherit it.
- Not posted: the project card (In progress) and executor/reviewer fields; the lane's rules allow only the two
  comments.
- Scratch: `/data-2/milan/tmp/950-a811` (clones, measurement, logs). Units: `milan-950-a811-*` only; none running
  once the final gates end.
