# HANDOFF r1 — lane 943 ([A800])

STATUS (17:35 CET): DONE — REVIEW READY at `502b041c` (13 commits on the flip train's head `0839453f`; firmware and
harness final since `211c1ede`). Every gate run at the final code: all green but `firmware-boundary`, which refuses
two files this branch does not touch, identically at the base. Nothing pushed; no PR (the manager's). ETA: done.

Branch `943-out-status` from the flip train head `0839453f` (PR #945). Posted: `[A800] TAKEN`, #943
issuecomment-7007476448; `[A800] REVIEW READY`, #943 issuecomment-7015365492 (text: REVIEW-READY-comment.md).
Nothing pushed; no PR (the manager's: PR-BODY.md, base dev-soft-core, Closes #943, Relates to #665).

Commits (one-line subjects): `36f89b45` test (fails first), `b605d1fa` fix, `8937f6ee` plants, `22b4def4` AECP README,
`8f077ee4` twin row and plants, `c637eb00` the output arm as a plain else (coverage), `deda5d6b` docs inventory,
`cb71d1a7` brief map check (superseded), `6d3f8673` the final bridge/core shape, `211c1ede` 8x8/1if long-record
restatement, `5d431cc3` README sentence, `c30af98a` memory page line, `502b041c` rows_tiers.py comment reflowed to
1,000 lines (the Python idiom gate's long-module ratchet).

## Changes (file:line — reason)

- `sw/firmware/ctrl/app/ctrl_app_aecp.c:50-67` `output()` and `:69-93` `stream()`: for a STREAM_OUTPUT observed whole
  (not brief) that the face reports declaring (STREAM_DEST_MAC_VALID, `0x10000000`): stream_dest_mac = ACMP source
  port's address when `dest_mac_valid` (what PROBE_TX_RESPONSE carries), else 0; REGISTERING (flags_ex 1) when SRP's
  registrar copy on the output's own interface (`acmp cfg.source_interface[index]`) has a Listener for its stream_id
  (`listener_present`), any declaration; REGISTERING_FAILED (flags 0x40) when that Listener is not Ready/Ready Failed
  (`!registered`), i.e. Asking Failed. Undeclared: the face's answer, which is the fabric's (0, neither flag). Brief
  (a running check's): the face's, bound and running alone. An output ACMP holds no source for: not answered.
  No SRP, or a source past SRP's generated shape: no Listener. `else` arm only reachable for type 6 (the core asks
  this port of types 5 and 6 only, `aecp_commands.c` observe).
- `sw/firmware/ctrl/aecp/aecp_commands.c:116-122` `aecp_stream_read` keeps the caller's `brief` (was always whole);
  `:385` GET/SET_STREAM_INFO's read initialised whole. `aecp_internal.h:32` its contract.
  `sw/firmware/ctrl/aecp/aecp_maps.c:128-133` `idle()`: an output map edit's check of its stream observed briefly, a
  running check, as SET_CONFIGURATION's and SET_STREAM_FORMAT's are.
- WHY the core change (CPU budget): the 1x1/1if paced one-row edit (answering-ports `aecp-fanout`, REMOVE of an
  output row) is stated 310 us; the base measures 29,331 cycles (310 by the rule). The bridge's completion run inside
  the edit's full-read `idle()` check, and the code moves it caused, put it at 30,744 to 31,749 cycles (325 to 335 us)
  in four variants. Restated by the rule to 325, 1x1/1if's `last` queued-notice row is 141.54 ms over its 140 ms
  bound (`flip_grade.py --check --point 1x1/1if` FAILs; the most it holds is 315 us, 30,000 cycles). The final shape
  keeps the completion out of every running check and the edit path on hot-listed code: 29,422 cycles, 310 us by the
  rule, within its statement; no 1x1/1if statement restated.
- `tb/verilator/ctrl_service_budget/rows_tiers.py:128-137` LONG_RECORD_US['8x8/1if'] 1715 -> 1720 us by the rule: the
  answering-ports `aecp-largest-notice` record 163,520 cycles at this image (152,504 at the base). 8x8/1if's rows by
  every source are reported, not held; `flip_grade.py --check` PASSes at both points with it (8x8/1if load 0.744 of
  0.75 and THE TRANSMIT row 76.81 of 77 ms, both unchanged).
- Reading of the clause: Milan v1.2 Table 5.8 / 5.12 REGISTERING = declaring and registering a matching Listener
  Ready, Ready Failed **or Asking Failed** (the release fabric's `gsi_oreging_w` is the same). The ruling's
  parenthetical names Ready/Ready Failed; this lane follows the table it cites, stated in TAKEN.
- `sw/firmware/ctrl/test/test_aecp.cpp`: `App::connecting()` hook; fixture `AppOutputs` and test
  `AppOutputs.OutputInfoCarriesItsTalkersAddressAndItsListenersRegistration` (outputs on n % MBX_N_IF, distinct
  stream_ids, links up, real MSRP Listener MRPDUs via the SRP channel, GET_STREAM_INFO parsed on the wire; the face
  mock answering as the split's does); `Core.TheRunningCheckObservesEveryStreamBriefly` +3 lines (an output map edit's
  check is brief).
- `sw/firmware/ctrl/test/aecp_arms.py`: `OUTPUTS` arm at 8x8 one interface (out dir `outputs`).
- `sw/firmware/ctrl/test/aecp_output_mutants.py` (new), `aecp_mutants.py`: 15 plants appended to DEFECTS.
  `aecp_configuration_mutants.py`: `stream-read-brief` re-anchored on `aecp_stream_read`'s new lines (same defect:
  every read brief), caught by its own words.
- `tb/verilator/milan_dp/twin_compare.py`, `twin_plants.py`, `Makefile`, `README.md`: OWED emptied (row
  `stream-output-0-dest-mac` deleted); `vanished-owed` -> `output-dest-mac-zero`; `output-notice-dropped` refused by
  the notice comparison's words.
- `sw/firmware/ctrl/aecp/README.md:115-122`; `docs/DOCUMENTATION_AUDIT.md` regenerated (one line).

## New checks (planted mutant — failing words)

Failing first on the unfixed bridge: receipts/firmware/failing-first-1x1-if1.txt, failing-first-8x8-if1.txt.

| Plant (aecp_output_mutants.py) | Words |
|---|---|
| output-dest-mac-the-faces (the shipped behaviour) | a declaring STREAM_OUTPUT's stream_dest_mac is its Talker's MAAP address |
| output-listener-unread (the shipped behaviour) | REGISTERING while declaring and registering a matching Listener (Table 5.8); REGISTERING_FAILED for a Listener Asking Failed alone (Table 5.11) |
| output-completed-undeclared | an undeclared STREAM_OUTPUT's stream_dest_mac is 0, as the fabric answers; both clear once the Talker withdraws |
| output-brief-completed | a brief observation of an output, a running check's, is the face's: bound and running alone |
| output-dest-mac-unallocated | no address MAAP does not hold |
| output-registering-ready-only | REGISTERING ... (Table 5.8) |
| output-registering-failed-any-listener | REGISTERING_FAILED for a Listener Asking Failed alone (Table 5.11) |
| output-registering-failed-without-a-listener | the face's flags, and no REGISTERING_FAILED with no Listener |
| output-registering-without-a-listener | no REGISTERING with no Listener; both clear once the Listener leaves |
| output-listener-on-interface-zero | REGISTERING ... (Table 5.8) (two interfaces; equivalent at one) |
| output-listener-of-output-zero | REGISTERING ... (Table 5.8); at one interface also "no other output shows its Listener" |
| output-answered-past-acmps-sources | an output ACMP holds no source for is not answered |
| output-unanswered-without-srp | without SRP, an output is still answered |
| output-unanswered-past-srps-shape | a source past SRP's shape is answered |
| map-idle-reads-whole (aecp_maps.c) | Core.TheRunningCheckObservesEveryStreamBriefly: an output map edit's running check is brief |

15 of 15 caught at the campaign's arm (1x1, two interfaces) on the final code; `stream-read-brief` caught after its
re-anchor; `aecp_mutants.controls()` PASS (381 defects, every test named). The firmware gate plants them again.
Twin: `output-dest-mac-zero` refused by "AECP notice GET_STREAM_INFO 0x0006/0 frame 0 differs at byte 66";
`output-notice-dropped` by "the fabric sent and the split did not: AECP notice GET_STREAM_INFO 0x0006/0 to the first
controller".

## Gate table

Final head `502b041c`; the code (firmware and harness) final since `211c1ede`, every later commit Markdown or a
comment. Receipts under receipts/ (INDEX.md).

| Gate | Head | Result | Receipt |
|---|---|---|---|
| New test fails first | `0839453f` + test | FAIL at every output, 1x1/1if and 8x8/1if | firmware/failing-first-*.txt |
| AECP app arms (all tests) | final code | PASS: 176 at 1x1 if1 and if2; AppOutputs at 8x8 if1 | firmware gate |
| Firmware gate, 4 shards | `211c1ede` | PASS: 1,804 invocations; control 825/825; AECP 381 (the 15 output plants); SRP and pins; 0 escaped | gates/firmware-gate-211c1ede-shard*.txt |
| fw_coverage --check | `211c1ede` | PASS (40 files); ctrl_app_aecp.c, aecp_commands.c, aecp_maps.c 100 % | gates/fw-coverage-211c1ede.txt |
| firmware-unit self-tests | `211c1ede` | tally, RV32 (25), coverage self-test, saved-state store: PASS | gates/firmware-unit-selftests-211c1ede.txt |
| firmware-verilator boundary | `211c1ede` | PASS | gates/boundary-verilator-211c1ede.txt |
| firmware-boundary (no Verilator) | `211c1ede` and base | REFUSED both, the same two files this branch does not touch (sink_mutants.py, talker_notice.py) | gates/boundary-without-verilator-head-and-base.txt |
| Twin, row still in | `22b4def4` | "the difference has gone": both halves 91e0f0000100 | twin/twin-22b4def4-row-gone.txt |
| Twin + twin-plants | `211c1ede` | 0 findings; 32 refusals, 0 escapes | twin/twin-and-plants-211c1ede.txt |
| plat_ledger | `211c1ede` | PASS; rom +280 B at every point, RAMB36 unchanged (45/46/58/63) | ledger/ |
| test_ctrl_memory | `211c1ede` | PASS, 0 failures | memory/ |
| Release image | `211c1ede` vs `0839453f` | bios.bin, disassembly, stripped ELF identical at 1x1 and 8x8 | release/ |
| Docs steps | `502b041c` | every gate step rc 0; 3 RV32 SDK install verifies refused by this host's SDK | docs/ |
| Budget arm A 1x1/1if | `211c1ede` | 99 groups, 0 refusals, 7 misses (the held-egress rows), 0 of 161,369 passes over the share, no STATED | budget/arm-a-1x1-* |
| Budget arm A 8x8/1if | `211c1ede` | 98 groups, 0 refusals, 7 misses (the held-egress rows, ledger PASS 0.38-0.86 ms inside), 0 of 277,945 passes over the share, no STATED | budget/arm-a-8x8-1if-*, egress-ledger-8x8-1if-211c1ede.txt |
| answering-ports AECP groups | `211c1ede` | 0 misses at both points; AECP rows vs the train's | budget/answering-ports-aecp-* |
| answering-every-port | `211c1ede` | 0 misses; 192 / 640 queued notices within 140 / 130 ms | budget/answering-every-port-* |
| talker-notices | `211c1ede` | 0 misses; notices at most 3.758 / 8.163 ms of 20 | budget/talker-notices-* |
| record_classes 1x1/1if (arm A + B + every-port) | `211c1ede` | RESULT: PASS (paced 310/310, long 965/975, other 225/245) | budget/record-classes-1x1-211c1ede.txt |
| record_classes 8x8/1if (arm A + B + every-port) | `211c1ede` | RESULT: PASS (long 1,720/1,720, paced 600/685, other 205/265) | budget/record-classes-8x8-1if-211c1ede.txt |
| AECP rows of arm A | `211c1ede` | every one fits: 40 at 1x1/1if, 33 at 8x8/1if | budget/arm-a-aecp-rows-*.txt |
| record classes across images, declaring-face arm | base + 5 images | see Notes | budget/aecp-record-classes-by-image.txt, declaring-face-measurement.txt |
| flip_grade --check | `211c1ede` | PASS at 1x1/1if and 8x8/1if; the 325 us trial FAILs 1x1/1if's last row | budget/flip-grade-* |
| Harness self-tests | `211c1ede` | run.py rc 0; record_classes 20/20 controls; flip_grade 616/616 | budget/harness-selftests-211c1ede.txt |

## Notes / decisions

- Out of scope, as #943 records them: a notice on a Listener registration change (Table 5.22), MSRP_FAILURE_VALID and
  the failure code/bridge ID, the declaring bit being the DA gate.
- The completion's own cost on a declaring output is measured outside the formal arms only: a measurement-only
  declaring-face arm (budget/declaring-face-measurement.txt) puts SET_STREAM_INFO of a declaring output at 240 of
  245 us (1x1/1if) and 210 of 265 (8x8/1if); on that image the paced edit and the long record (which never run the
  completion) measure 325 and 1,920 us: placement. A formal declaring-face arm is the owner's to decide.
- Placement sensitivity (budget/aecp-record-classes-by-image.txt): the same work measured 29,331 to 31,749 cycles
  (1x1/1if paced edit) and 152,504 to 173,295 (8x8/1if long record) across this branch's images.
- firmware-boundary refuses sw/firmware/ctrl/test/sink_mutants.py (#946) and talker_notice.py (#936), unclassified
  in ctrl_configs.py, at the base 0839453f as at the head; for the manager to route (the train or a follow-up).
- Arm A was run as a main run plus parts (pB-pE) on byte-identical images and graded together with
  `run.py --reuse-build --regrade` (tools/merge_arm.py in scratch); the save-burst journal is merged with its log.
- Seen beside it (not changed; for the manager to file): the split's GET_TX_STATE never sets REGISTERING_FAILED —
  the platform's ACMP source port reports `asking_failed = false` always (`plat/ctrl_plat.c` source()), Milan v1.2
  Table 5.47.
- fw_coverage's ratchet is fraction-based; its recorded totals were already stale for many files, so not rewritten.
- Docs steps not run, each an install or a hosted recorder: pip/apt installs, sv2v install, the RV32 SDK install's
  verify (the host SDK has no provenance receipt; its self-test passes), the evidence recorders, fail-fast.
- Scratch: `/data-2/milan/tmp/943-a800` (clones, builds, logs). Units: `milan-943-a800-*` only.
