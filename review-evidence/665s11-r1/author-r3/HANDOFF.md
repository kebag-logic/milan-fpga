# HANDOFF: #871 (#665 S11), AECP REBOOT on the core ([A761c], rounds 2 and 3)

Status: REVIEW READY (round 3) at `6171d65473875239d97e6f6b9327c394db65aab8`, one commit on round 2's `d08d30c6ec`; every gate the ruling lists passed there; nothing pushed. REVIEW READY: issuecomment-6809079212 (2026-11-11). Acceptance items 2 to 5 met; item 1 partial as ruled, so the PR still says Relates to #871.

## Round 3 (ruling issuecomment-6806697914 on R821-2 F1 and R822-2 F1)

The ruling: every mailbox channel's receive refused from the SUCCESS (ADP, ACMP, AECP, MAAP and SRP, each named); no channel but ADP's ENTITY_DEPARTING starting a transmission after ENTITY_DEPARTING; each assertion from the SUCCESS's own cycle; a planted defect per channel, failing by its own words. No firmware behaviour change: no test exposed a channel the gate misses, so `ctrl_plat.c` and `aecp.c` are unchanged (the reviewers' probe anchors still apply).

Commit `6171d65473`: tests, mutant tables and two documents only.

| File:line | Change, reason |
|---|---|
| `sw/firmware/ctrl/test/test_plat_boot.cpp:182`, `:184` | `busy_ch` (any channel's ring holds a frame) replaces the ACMP-only hook; `aecp_full` (AECP's transmit ring full, so no AECP frame is handed over) |
| `test_plat_boot.cpp:348` `ch_writes`, `:358` `maap_probe`, `:369` `msrp_pdu`, `:378` `one_frame_per_channel`, `:912` `kChannels` | one channel's register writes; a MAAP PROBE for the entity's own range (the mailbox's range term passes it, IEEE 1722-2016 B.2) and an MSRP PDU (IEEE 802.1Q-2018 35.2.2) so MAAP's and SRP's channels get a frame; the five channels by name |
| `test_plat_boot.cpp:915` NoFrameOfAnyChannelIsTakenFromTheSuccess | a frame on each of the five channels after the SUCCESS; each channel's `RX_TAIL` checked by name |
| `test_plat_boot.cpp:947` NoOtherChannelTransmitsAfterTheDeparting | each of ACMP, AECP, MAAP and SRP checked by name for a `TX_HEAD` write after the DEPARTING |
| `test_plat_boot.cpp:992` TheDepartingWaitsForEveryOtherRing | the ACMP, MAAP and SRP rings held in turn, each with its own boot. AECP's ring holds only the REBOOT's frames once the loop has stopped, which `aecp_reboot_due` waits for (B12), so its wait is not load-bearing |
| `test_plat_boot.cpp:1025` B22TheGateHoldsInThePassThatTakesTheReboot (new) | a MAAP PROBE, an MSRP PDU and a second AEM command queued with the REBOOT; none taken in the pass that takes it (MAAP and SRP are serviced after AECP in a pass), before its SUCCESS is handed over |
| `test_plat_boot.cpp:1054` B23TheGateHoldsWhileTheResponseCannotBeHandedOver (new) | AECP's transmit ring full, so the SUCCESS is accepted (`reboot` 1) but not handed over; a frame on each of the five channels stays in its ring; then the REBOOT completes |
| B19, B22, B23 preconditions | read `ctrl_plat.aecp.core.reboot`, not the accessor the gate reads, so a defect in the accessor reaches the per-channel checks (the first campaign run caught the handover defect on fewer words for this reason) |
| `sw/firmware/ctrl/test/test_aecp.cpp:1842` | `aecp_reboot_accepted` true straight after `aecp_rx` of the REBOOT, before any poll |
| `sw/firmware/ctrl/test/aecp_mutants.py:829` | `reboot-accepted-only-at-the-handover` |
| `sw/firmware/ctrl/test/plat_mutants.py:286` `channel_gate_mutants`, `:304` `channel_wait_mutants`, `:265` | five per-channel gate defects, three per-ring wait defects, `plat-reboot-accepted-at-the-handover`; the whole-gate, loop-on and whole-wait defects now require the per-channel words |
| `docs/design/REBOOT_RESET.md` section 8 evidence rows, `sw/firmware/ctrl/plat/README.md` | the claims as the tests now prove them; 62 platform defects (22 REBOOT), AECP 14 REBOOT defects |
| header comments of the edited tests | keyed by the tests' names, not by bench labels (the owner's comment rule; R822-2 R1's form) |

New planted defects (each caught on its own words; `platmut4` and `aecpmut3` campaign logs):

| Defect | Edit | Test | Failing words |
|---|---|---|---|
| `plat-reboot-takes-adp-frames-after-the-success`, `-acmp-`, `-maap-`, `-srp-` | the gate open on that one channel (`taking`) | B19, B23 | B19 no <channel> frame is taken after the REBOOT's SUCCESS; B23 no <channel> frame is taken while the REBOOT's SUCCESS waits to be handed over |
| `plat-reboot-takes-aecp-frames-after-the-success` | AECP's channel taken whatever the gate and AECP's own ready say (AECP refuses a command from its SUCCESS too, so one layer alone changes nothing) | B19, B23 | as above, AECP |
| `plat-reboot-accepted-at-the-handover` | `aecp_reboot_accepted` true only from `reboot` 2 | B22, B23 | B22 no MAAP / SRP frame queued with the REBOOT is taken; B23 no ADP / ACMP / MAAP / SRP frame is taken while ... |
| `plat-reboot-departs-past-the-acmp-ring`, `-maap-`, `-srp-` | the DEPARTING's wait skipping that ring | B21 | B21 no ENTITY_DEPARTING while the <channel> ring holds a frame |
| `reboot-accepted-only-at-the-handover` (AECP core) | the same accessor edit | `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete` | accepted at its SUCCESS, before any poll hands its frames over |

Not taken (not in the ruling's list): R822-2 R2 (ADP's poll "from the loop's last pass" in three documents), R821-2 S1 to S6 and R822-2 S1 to S4. R822-2 R1 is applied only to the comment lines this round rewrote.

Reviewer probes at `6171d654`, each script byte-identical to the reviewer's (`receipts/round3/scripts/reviewer2`, digests in its `RAW.tsv`; results `receipts/round3/probes`):

| Probe | Result |
|---|---|
| R821-2 `probe_plat.py head` | platboot1 rc 0, 0 failed checks |
| R821-2 `probe_plat.py gate-skips-maap-and-srp` | platboot1 rc 1, 12 failed REBOOT checks: B19, B22 and B23 on their MAAP and SRP words |
| R821-2 `probe_plat.py gate-from-the-handover` | platboot1 rc 1, 12 failed REBOOT checks: B22 (MAAP, SRP) and B23 (ADP, ACMP, MAAP, SRP). Its `unit` arm holds no REBOOT test, rc 0 |
| R821-2 `probe_aecp.py head` / `handover` | rc 0 / rc 1: `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete` on "accepted at its SUCCESS, before any poll hands its frames over" |
| R822-2 `r822_probes.py clean` | platboot1, platboot2 and the AECP core arm rc 0 |
| R822-2 `r822_probes.py gate-skips-maap-and-srp` | platboot1 rc 1 (13 failures: B19, B22, B23 on MAAP and SRP) |
| R822-2 `r822_probes.py depart-ignores-maap-and-srp-rings` | platboot1 rc 1 (B21 on "the MAAP ring" and "the SRP ring") |

The probe clone was clean after every probe (`final.txt`).

Gates at `6171d65473875239d97e6f6b9327c394db65aab8` (the ruling's list), each on a fresh clean clone, receipts under `receipts/round3/`:

| Gate | Command | Result | Receipt |
|---|---|---|---|
| AECP and platform host tests and mutants | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `test_ctrl_firmware: PASS`; control campaign 592 of 592 caught (the 22 platform REBOOT defects among them) | `gates/lane/fw_selftest.log` (listed in `LARGE.tsv`) |
| AECP mutant driver | `aecp_mutants.py --output ...` | 153 `[ok]` (the 14 REBOOT defects among them), rc 0 | `gates/lane/aecp_mutants.log` |
| The REBOOT defects alone, through the campaigns' own code | the reviewers' `reboot_plat_mutants.py` / `reboot_aecp_mutants.py` drivers on the lane tree before the commit | platform 23 of 23 (`platmut4`), AECP 14 of 14 with the table-drift control (`aecpmut3`); the earlier `platmut3` caught the handover defect on fewer words, fixed by the precondition change above | `campaigns/` |
| The REBOOT simulation | `ctrl_reboot/run.py --self-test --jobs 3`, no seed in the environment | `ctrl_reboot: PASS (0 finding(s))`, 12 of 12 plants and controls | `gates/lane/reboot.log` |
| `docs.yml` | the 829 docs runner and verifier | 64 ran rc 0, 31 not run with reasons, 0 bad | `gates/docs-table.md`, `gates/docs/` |
| Whitespace | `git diff --check <merge base> HEAD` | rc 0, no output | `gates/lane/diffcheck.log` |

Round 2's full pass (every workflow step, the sweep, S2, the builder, behave, coverage) ran at `d08d30c6ec` and is below. The round 3 delta `d08d30c6ec..6171d654` touches only `test_plat_boot.cpp`, `test_aecp.cpp`, the two mutant tables, `REBOOT_RESET.md` and the platform README. The ruling did not ask for those gates again.

---

# Round 2 (as handed off at `d08d30c6ec`)

Status: REVIEW READY at `d08d30c6ecbac2e45867c3a509ef309ed081ab15` (five commits on `b29f94d7aa`); every gate below passed there; nothing pushed. Acceptance items 2 to 5 met; item 1 partial as before (the ruling, item 7), so the PR says Relates to #871. Base of this round: `b29f94d7aa` (round 1 head, PR #881). TAKEN: issuecomment-6789381472; REVIEW READY: issuecomment-6802401488 (both 2026-11-11).

Commits added on `b29f94d7aa` (no merge, rebase, force or amend; one-line subjects, no body, no trailers):

| Commit | What |
|---|---|
| `b679e220be` | the firmware's parity (receive gate, loop stop, DEPARTING last), host tests B19 to B21 and B17 widened, AECP index-before-lock and acceptance tests, five planted defects, the memory ledger |
| `c8b2abd954` | the CPU simulation: the early-reset plant before the SUCCESS, the window's AEM command and BIND_RX, frames after the DEPARTING and the port graded, own-words plants and controls, the mixed-replay control, the hash seed |
| `9534d51f0f` | REBOOT_RESET.md section 8, MAILBOX_SPLIT.md (R822-1 R1), the CDC census row |
| `10b0fe93ef` | one AECP mutant row wrapped inside 120 columns: docs-gates-0 gate_39 (Python idiom) refused it at `9534d51f0f` |
| `d08d30c6ec` | the coverage exclusion for the receive gate's unbound-channel test: `fw_coverage.py --check` refused `ctrl_plat.c` branches 79/80 at `10b0fe93ef` |

**History, not cited as the final evidence.** A host reset cut the session (the host was back up at 09:51, by its uptime); its uncommitted work survived and was reviewed file by file before the first commit, and a size run and an S2-base copy it cut were redone. The first gate pass, at `9534d51f0f`, was stopped when gate_39 refused one line (receipts/history-9534d51f; its SDK install step also failed once on DNS and passed on a rerun). The second, at `10b0fe93ef`, was stopped once the coverage ratchet refused the one untaken arc (`if (p->rx[ch].fn != NULL)`, false side) and the split boot simulation refused twice with no hash seed (receipts/history-10b0fe93). The arc is unreachable: every channel has its handler before the gate is set. It now has an exclusion row, checked by the gate's own judgement over the kept measurement: PASS with the row, FAIL without it (receipts/coverage). The boot refusal is the split boot simulation's own: it pins no seed (R822-F3's class, in a harness this lane does not own, and run by no workflow), so the final pass runs it with `PYTHONHASHSEED=0`, as round 1 did. It is named below for a new issue. Round 1's helper environment exported that seed, which is how round 1 passed it. This round's unsets it, so the REBOOT simulation's own pin is what is tested.

## Ruling items (issuecomment-6789331293)

| Item | Status | Where |
|---|---|---|
| 1 parity: from the SUCCESS no received frame of any channel is taken | done | `ctrl_plat.c:175-196` gate; B19; defect `plat-reboot-takes-frames-after-the-success`; CPU plant `frames-taken-after-the-success` |
| 1 parity: after ENTITY_DEPARTING no other channel starts a transmission | done | `ctrl_plat.c:352-386`; B20, B21, B17; defects `plat-reboot-transmits-after-the-departing`, `plat-reboot-departs-before-the-rings-drain`, `plat-reboot-serves-the-loop-after-the-port`; CPU control `frame-after-the-departing` |
| 1 R821 `fw_probes.py ... behaviour-acmp-after-success` unchanged | passes | receipts/probes/r821 |
| 1 R822 `run_probe_window.sh` | `sink.bound` 0, no ACMP frame | receipts/probes/r822 |
| 1 REBOOT_RESET.md section 8 (`:264`, `:270`) | done | `docs/design/REBOOT_RESET.md` section 8 |
| 2 plant fires the port before the SUCCESS leaves; per-plant words | done | `run.py:678` plant, `run.py:797` and `:809` |
| 3 PYTHONHASHSEED pinned | done | `run.py:825`; two runs with no seed: gates lane `reboot` and `reboot_plain` |
| 4 bound text | done | REBOOT_RESET.md section 8 "The bound", "One measurement"; ctrl_reboot README BOUND row; PR body |
| 5 R822-1 R1 | done, exact text | `docs/design/MAILBOX_SPLIT.md` "Default build" |
| 6 R821 S1 index before lock | done | `test_aecp.cpp:1826`; defect `reboot-lock-before-the-index`; reviewer probe `lock-before-the-index` now caught |
| 6 R821 S3 / R822 S1 mixed replay | done | `run.py:734` `_mixed_replay`, control `replay-mixed` |
| 6 R821 S4 tie `i_reboot_req` 0, exports byte-identical | NOT TAKEN: conflict, published | receipts/exports: the tie adds `.i_reboot_req (1'd0),` to the all-fabric top `.v`; without it the head's exports equal the base's (timestamps and the hierarchy comment's order aside, which vary run to run) |
| 6 R822 S2 base side of the S2 compare | done | receipts/s2-base |
| 6 R822 S3 CDC census row | done | `docs/diagrams/cdc_census.gen.py:123`, SVG and drawio by the generator (matched byte for byte by a rerun), PNG by `rsvg-convert -w 1900` |
| 7 item 1 partial, "Relates to #871" | unchanged | PR-BODY |

## Decisions

- **The receive gate wraps each channel's binding through the loop's public API** (`ctrl_loop_bind_rx`, `ctrl_loop_set_rx_ready`), installed at the end of the boot only when a reset port exists, reading `aecp_reboot_accepted` at every take. A gate set from a poll would let MAAP's and SRP's channels (3 and 4) take frames in the same pass as the REBOOT (AECP is channel 2). `sw/firmware/ctrl/loop/` (S2b) is untouched. A frame not taken stays in its ring; the mailbox drops whole one that then finds no room (`RX_DROP`, `mbx_model.c`'s header), the split's equivalent of the processor's discard.
- **The transmit gate is the loop's stop.** From `aecp_reboot_due` `ctrl_plat_step` runs `depart` instead of the loop, so no producer runs. ADP's SHUTDOWN waits for every other channel's ring (`drained`), because the datapath reads the rings independently: a frame committed before the DEPARTING could otherwise follow it on the wire. Then ADP's own poll retries an owed DEPARTING; the port fires once ADP's ring has drained.
- **The due check moved from the console's poll to `ctrl_plat_step`**, so the console's poll is base's again; the split image never sleeps (no `CTRL_MBX_WFI`), so no wake is lost.
- **R821 S4 is not taken.** The ruling's condition (the all-fabric exports still byte-identical) cannot hold with any Instance tie: measured at both shipping configs, the tie's only effect on the export is the one binding line. The repo keeps the shipping top `.v` byte-identical by design (`milan_soc.py`'s additive-discipline comments). The port is unread at `CTRL_SPLIT_P = 0`. Needs a decision if the line is acceptable.

## Changes (file:line, reason)

| File:line | Reason |
|---|---|
| `sw/firmware/ctrl/aecp/aecp.h:243`, `aecp.c:205` `aecp_reboot_accepted` | the platform's gate reads AECP's acceptance at its SUCCESS |
| `sw/firmware/ctrl/plat/ctrl_plat.c:175` `taking`, `:181` `taken`, `:187` `gate` | every channel's take behind the acceptance, each module's binding behind it |
| `sw/firmware/ctrl/plat/ctrl_plat.c:199` `drained` | any channel's ring drained (was ADP's only) |
| `sw/firmware/ctrl/plat/ctrl_plat.c:298` | the console's poll unwrapped again (base) |
| `sw/firmware/ctrl/plat/ctrl_plat.c:321` | the gate installed at the end of the boot, with a port only |
| `sw/firmware/ctrl/plat/ctrl_plat.c:331` `quiet` | from the loop's last pass, not from the port |
| `sw/firmware/ctrl/plat/ctrl_plat.c:352` `depart` | other rings drained, then SHUTDOWN, then ADP's poll and ring, then the port |
| `sw/firmware/ctrl/plat/ctrl_plat.c:377` `ctrl_plat_step` | due stops the loop; `depart` from then |
| `sw/firmware/ctrl/plat/ctrl_plat.h:26-42`, `:127`, `:129` | the contract; the stages; the saved bindings |
| `sw/firmware/ctrl/test/test_plat_boot.cpp:801` B17, `:852` B19, `:883` B20, `:920` B21 | the parity tests; helpers `ring_writes`, `bind_rx`, `discover`, `bound`, flags `acmp_busy`, `held_at` |
| `sw/firmware/ctrl/test/test_aecp.cpp:1826`, `:1844` | index before lock; acceptance reported |
| `sw/firmware/ctrl/test/plat_mutants.py:197-261`, `aecp_mutants.py:797`, `:825` | anchors moved with the code; three platform defects and two AECP defects added |
| `sw/litex/ctrl_memory.py:217`, `ctrl_memory_ledger.py:26`, `docs/design/SPLIT_CONTROL_MEMORY.md:97` | `sizeof(struct ctrl_plat)` re-measured (receipts/size) |
| `tb/verilator/ctrl_reboot/sim_main.cpp:363` `answered` step | waits for a tagged command's response to leave, so the window's command and bind reach the mailbox after the SUCCESS |
| `tb/verilator/ctrl_reboot/run.py:264-266` | the window: AEM command and BIND_RX after the SUCCESS |
| `tb/verilator/ctrl_reboot/run.py:556-575` | ORDER: frames after the DEPARTING, after the port, the bind's arrival in the window, the bind answered |
| `tb/verilator/ctrl_reboot/run.py:678-700`, `:722-760`, `:797`, `:809` | plants and controls with their own words |
| `tb/verilator/ctrl_reboot/run.py:825` | `PYTHONHASHSEED` 0 for every child export |
| `docs/design/REBOOT_RESET.md` section 8, `MAILBOX_SPLIT.md` "Default build", `sw/firmware/ctrl/{aecp,plat}/README.md`, `tb/verilator/ctrl_reboot/README.md` | the parity, the bound, the evidence |
| `docs/diagrams/cdc_census.{gen.py,svg,drawio,png}` | the census row |

## New checks (planted mutant, failing words)

Host platform (`plat_mutants.py`, arm `platboot1`), the ones new or changed this round:

| Mutant | Edit | Test | Failing words |
|---|---|---|---|
| `plat-reboot-takes-frames-after-the-success` | the gate's acceptance test removed | B19 | B19 no frame of any channel is taken after the REBOOT's SUCCESS; B19 a BIND_RX after the REBOOT's SUCCESS is not applied |
| `plat-reboot-transmits-after-the-departing` | the loop serviced until the port | B20 | B20 no other channel starts a transmission after ENTITY_DEPARTING (18 frames: SRP 13, MAAP 4, ACMP 1, receipts/probes/b20mut) |
| `plat-reboot-departs-before-the-rings-drain` | SHUTDOWN without the other rings' wait | B21 | B21 no ENTITY_DEPARTING while another channel's ring holds a frame |
| `plat-reboot-serves-the-loop-after-the-port` (was `...-takes-frames-after-the-port`) | the loop serviced after the port | B17 | B17 nothing is sent once the reset port fired |
| `plat-reboot-before-the-response` (moved) | the port written in the take that accepts the REBOOT | B12 | B12 no reset while the mailbox holds the response |
| `plat-reboot-departing-owed-ignored`, `plat-reboot-before-departing-left`, `plat-reboot-ignored` (anchors moved) | as round 1 | B18, B12, B11/B15/B16 | as round 1 |

AECP (`aecp_mutants.py`): `reboot-lock-before-the-index` (index and lock checks swapped; `Core.RebootRefusalsLeaveTheEntityInService`: NO_SUCH_DESCRIPTOR for another ENTITY index under another controller's lock); `reboot-acceptance-unreported` (`aecp_reboot_accepted` false; `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete`: accepted at its SUCCESS, so the platform takes no frame).

CPU simulation (`run.py --self-test`), each caught only by its own words:

| Plant or control | Words |
|---|---|
| plant `reset-before-the-response` | ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired |
| plant `request-ignored` | ORDER: the reset port never fired |
| plant `write-torn` | JOURNAL: the drain ended cap, not because the state was durable |
| plant `any-descriptor-type` | REFUSE: refuse-input answered status 0 at cdl 16, not 11 at cdl 16 |
| plant `frames-taken-after-the-success` (new) | ORDER: a BIND_RX given after the REBOOT's SUCCESS had left was answered |
| control `response-after-the-port` | ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired |
| control `frame-after-the-departing` (new) | ORDER: a frame other than ADP's left the mailbox after ENTITY_DEPARTING |
| control `drain-at-its-cap` | JOURNAL: the drain ended cap |
| control `no-advertisement` | ADP: no ENTITY_AVAILABLE after the reset |
| control `name-reverted` | RESTORE: the #396 grader says FAIL ... entity_names |
| control `binding-lost` | RESTORE: the #396 grader says FAIL ... stream_binding |
| control `replay-mixed` (new) | JOURNAL: the cut's replay reads ... a write half applied |

## Reviewer probes at the fixed head

All at `d08d30c6ec`, on a disposable clone of the head, each script byte-identical to the reviewer's (receipts/scripts/reviewer; digests in receipts/scripts/RAW.tsv):

| Probe | Result |
|---|---|
| R821 `fw_probes.py`, `behaviour-acmp-after-success` | rc 0, no test failed: `acmp_frames_after_success=0 sink_bound=0 frames_after_departing=0`; with the DEPARTING out before the port, `acmp_frames_after_departing=0 port_writes=1` |
| R821 `lock-before-the-index` (S1) | now caught (`Core.RebootRefusalsLeaveTheEntityInService`, 2 failures) |
| R821 `end-one-early`, `older-completion-moves-back`, `due-without-the-reentry-guard`, `refusing-ignored` | caught, as at round 1 |
| R821 `quiet-without-the-face-poll` (S2, not taken by the ruling) | escapes, as at round 1 |
| R821 `drained-reads-the-aecp-ring`, `shutdown-before-due` | not planted: their anchors (`adp_drained`, `reboot_step`) no longer exist; the parity rewrite replaced both, and B12, B21 and the drained-ring defects cover the new code |
| R822 `run_probe_window.sh` | `sink.bound` 0; `acmp_frames=0`; frames AECP (ch 2), ADP DEPARTING (ch 0), then the port; its host gate run PASS; the clone restored |
| B20 under `plat-reboot-transmits-after-the-departing` | 18 frames after ENTITY_DEPARTING: SRP 13, MAAP 4, ACMP 1 (receipts/probes/b20mut.out) |

## Gate table

All at `d08d30c6ecbac2e45867c3a509ef309ed081ab15`, each on its own fresh clean clone of the head (`git status` empty before and after, recorded per job); receipts under `receipts/` (index `receipts/INDEX.md`; host prefixes replaced by named placeholders; a file over 200 KB listed in its directory's `LARGE.tsv` by size and sha256; `RAW.tsv` holds each source file's digest).

| Gate | Command | Result | Receipt |
|---|---|---|---|
| `rtl-fast`, `elaborate`, `rtl`: every `run:` step of every job a pull_request to dev-soft-core triggers | `run_wf.py` per job (firmware-boundary and the elaborate gates with the LiteX venv first on PATH), `verify_wf.py <head> <root> rtl/yosys-shards=4` | 88 ran, rc 0; 167 not run, each with its reason (`gates/tools/wf/not_run.json`); 0 bad. firmware-boundary and firmware-verilator `ctrl_boundary: PASS`; firmware-unit PASS with `firmware coverage: PASS (35 files)`; control mutants 583 of 583 over four shards; AECP mutants 152; SRP 280; yosys-shards 0 to 3 of 4 and yosys-portability rc 0. **gate_19** (elaborate-gates-1, the LiteX simulations) first ended UNKNOWN, exit 92: `test_soc_timing_cuts` hit the runner's 900 s wall clock while the pass loaded the host (`gates/wf/elaborate.elaborate-gates-1__gate_19.first-run.log`). The step rerun alone on the same clone passed, 8 of 8 (`...__gate_19.log`, rc 0); the test alone with no wall clock also passed in 1,712 s (`...__gate_19.standalone-test_soc_timing_cuts.log`) | `gates/wf-table.md`, `gates/wf/` |
| publication-census (rtl-fast) | its own unit, MemoryMax 10G, after its first run in the session unit was stopped for memory (history-d08d30c6-census) | 6 shapes, 246 checks, 0 failures; self-test 0 of 164 arms failed; the REBOOT plants refused | `gates/wf/rtl-fast.publication-census__*` |
| `docs.yml`: every `run:` step | the 829 docs runner and verifier | 64 ran, rc 0; 31 not run, each with its reason; 0 bad | `gates/docs-table.md`, `gates/docs/` |
| Full sweep | `native-shards.py`, 4 units (MemoryMax 10G), `MAKEFLAGS=-j4 --no-print-directory`, CPU ranges `cpu_ranges.pick8` read live (72-79, 8-15, 88-91, 80-87), the capture_coherence shard (2) on 4 CPUs | 65 of 65 suites, 2,192,899 checks, 0 in-suite failures, 0 timed out; suite-cancellation preflight PASS on each shard (no #833 rerun needed) | `sweep/` |
| Firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `test_ctrl_firmware: PASS`; control campaign 583 of 583 caught | `gates/lane/fw_selftest.log` |
| Coverage ratchet | `fw_coverage.py --check --jobs 4` | `firmware coverage: PASS (35 files)` | `gates/lane/fw_coverage.log` |
| AECP mutant driver | `aecp_mutants.py --output ...` | 152 `[ok]`, the 13 REBOOT defects among them | `gates/lane/aecp_mutants.log` |
| Saved-state mutant campaign | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | 5 shapes, 435 tests, all 109 planted defects reddened | `gates/lane/nvm_selftest.log` |
| S2's harness | `ctrl_service_budget/run.py --self-test`; `--point 1x1`, `--point 8x8`, `--record-budget-findings --jobs 8` | self-test 0 failures; 1x1/1if 18 groups, 0 refusals, 34 T_svc misses (13 of 81 paths); 8x8/2if 17 groups, 0 refusals, 57 misses (29 of 129 paths), recorded as S2's ruling says. Against the base: the 13 and 31 paths as published; against round 1's head every path +0.000 ms (S2 builds the SRP fixture image, which this round's platform changes do not reach) | `gates/lane/s2_*.log`, `s2-base/` |
| Builder | `test_builder.py --require-rv32` | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 11's calibration arm (a Vivado place report this host lacks) and gate 1b's `MAKEFLAGS += -e` mutation, which this run's make 4.3 cannot show. Gate 1b alone with the host's GNU Make 4.4.1: `ALL GATES PASS` | `gates/lane/builder.log`, `gates/lane/builder_gate1b_hostmake.log` |
| behave | `cd tests && behave` | 14 features, 508 scenarios, 2,330 steps passed | `gates/lane/behave.log` |
| Whitespace | `git diff --check <merge base> HEAD` | rc 0, no output | `gates/lane/diffcheck.log` |
| The REBOOT simulation, twice with no seed in the environment | `ctrl_reboot/run.py --self-test --jobs 3`; `ctrl_reboot/run.py` | both `ctrl_reboot: PASS (0 finding(s))`; 12 of 12 plants and controls caught on their own words | `gates/lane/reboot*.log` |
| The split boot simulation | `PYTHONHASHSEED=0 ctrl_split_boot/run.py`, and `--self-test` | rc 0; 6 of 6 native controls, 2 of 2 plants, 0 placement controls wrong (with no seed it refused at `10b0fe93ef`, Open risks 4) | `gates/lane/boot_*.log` |
| The saved-state target | `nvm_split_target/run.py --self-test` | rc 0, 73 checks, 0 failures | `gates/lane/nvm_target_selftest.log` |
| All-fabric exports | `export_fabric.py` at the base (twice), the head and round 1's head with the tie, one clone path, `export_cmp.py` | 1x1 and 8x8, head against base: all 22 generated files equal, LiteX's timestamps and hierarchy-comment order aside (which differ between two exports of one commit too); with the tie, one line more | `exports/compare.txt` |
| Linked size | `ctrl_plat_image.py` at four points, base and head | `size/delta.md`; the ledgered 8x8/2if image plans at 59.0 with `ctrl_plat` 21,328 B | `size/` |

Not run: the mailbox's full RTL mutant set (`make -C tb/verilator/mbx mutants`): the mailbox RTL is unchanged; the sweep's mbx suite ran its quick set. The bench, flashing and Vivado routes are outside this lane.

## Open risks

1. **Acceptance item 1 stays partial** (the ruling, item 7): the configuration and the sampling rate cannot leave their defaults at the shipping shape. The PR says "Relates to #871".
2. **R821 S4 is not taken** because its two conditions conflict (Decisions). It needs a ruling if the one added line in the all-fabric top `.v` is acceptable.
3. **The firmware stage has no bound while a ring is held**, now stated in REBOOT_RESET.md section 8, as the processor states for its MAC.
4. **The split boot simulation pins no hash seed** (`tb/verilator/ctrl_split_boot/run.py`). With none it refused twice at `10b0fe93ef`, on the `csr.csv` comparison R822-F3 found in the REBOOT simulation (receipts/history-10b0fe93). It is outside this lane and no workflow runs it; a new issue for its owner should pin the seed as `ctrl_reboot/run.py` now does.
5. **Host load**: elaborate-gates-1 gate_19 ran `test_soc_timing_cuts` past the runner's 900 s wall clock (UNKNOWN, exit 92), as round 1 saw. Alone with no wall clock it passed in 1,712 s. This round changes no SoC path it builds (`sw/litex/milan_soc.py` is unchanged since round 1).
6. **The CPU simulation has no plant for the transmit gate**: in its scenario nothing would send between the DEPARTING and the port. Host B20 holds the DEPARTING 5 s with producers running, and the simulation's grader control proves its check.
