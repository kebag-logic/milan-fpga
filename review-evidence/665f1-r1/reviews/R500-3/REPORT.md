[R500] NEGATIVE - exact head 9412006bd58c002835bb06d46045c53098cc59a5

# R500-3: internal cleared-context review of PR #669 (#665 lane F1), round 3

- **Head under review:** `9412006bd58c002835bb06d46045c53098cc59a5`, tree `ba76ab7618f8d97c681d0e33f7b2d2128c6169aa`. It equals the PR's published head; the PR is ready, not draft.
- **Round 3:** five commits on `7f8dc1b1`:
  - `da35570a`: code and suite;
  - `ce78be4a`: the FASTCONNECT section 7 tie edit;
  - `716d3213`: the module page;
  - `e2000ef9`: a `--no-ff` merge of dev `28f9666f`;
  - `9412006b`: the 2,213 us cumulative call bound.
- **Bases:** the source base is `fa450d301805881ad713b67521477bf042ddadfd`, and live dev is `28f9666feab2b2ba287643c63ed3a16b1e0bb863`.
- **Reconstructed from**, in the public order:
  - AGENTS.md and CONTRIBUTING.md, then docs/README.md;
  - the #665 body, the lane F1 assignment (5993775541), the round-2 assignment (5996009284), and the decisions and round-3 assignment (5997929153);
  - the executor's TAKEN and REVIEW READY for round 3 (5998087724, 5999002886), and the PR body;
  - FASTCONNECT sections 6.2, 7 and 9.2; MATERIALIZATION sections 8.1 and 8.6; the shipping writer's `nvm_pick_slot`; `sw/litex/milan_soc.py`; the five `configs/endstation_*.yaml`;
  - `git diff fa450d30..9412006b`, the lane diff against live dev, and the round-3 history;
  - the public evidence at `38e93660` `review-evidence/665f1-r1`, which holds round-1 (`215c3c0b`) material only and is historical, not exact-head evidence;
  - the exact-head hosted check list.
- **Prior public findings** (R500-1, R501-1, R500-2, R501-2) were read only after my independent pass over the diff, my probes and my draft findings.

All five lenses were applied. Decision 1, decision 2, R501-2-F2 and R500-2-F1 to F4 are resolved at this head, and I verified each one independently (below).

One new MAJOR finding is open, so the verdict is NEGATIVE. The LiteSPI flash port does not compile at the system clock of three of the five shipped shapes. The suite's clock stand-ins hide this. Because the finding is attributable to all five lenses, every lens is UNCLEAN.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R500-3-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | The on-chip port cannot be built at the Arty shapes' 83,333,000 Hz clock, and the gate's 100 MHz stand-in reports those shapes OK |
| R500-3-R1 | RESIDUE | Docs | "a ready master costs one timer read" is true of the model, not of the chip |
| R500-3-S1 | SUGGESTION | Robustness, Docs | HELD has one exit, a reset that reads the slot cleanly. A slot that never reads cleanly therefore ends persistence for good. Decision 2 holds the writer even when a commit would be safe |
| R500-3-S2 | SUGGESTION | Robustness | HELD with changes outstanding reports `dirty=1` but `stale=0` |
| R500-1-S1 | SUGGESTION, retained | Tests | the lane gate still runs in no hosted workflow |

## Round-3 assignment (5997929153), item by item

| Item | At this head | Evidence |
|---|---|---|
| Decision 2 (R501-2-F1) | RESOLVED | See "Decision 2" |
| Decision 1 (R501-2-F3) | RESOLVED | See "Decision 1" |
| R501-2-F2: nominal and cumulative bounds separated, the every-wait case added, the PR maximum corrected | RESOLVED | See "Service bound" |
| R500-2-F1 to F4, and S1 | RESOLVED | See "Prior public findings" |
| `--no-ff` merge of dev | RESOLVED | `receipts/merge_check.log` |

### Decision 2

Code: `nvm_store.c:135-208`, `:237-248`, `:330-350` and `:392-417`.

- **The three-read rule.** `nvm_slot_check` gives a slot at most `NVM_READ_TRIES` = 3 reads.
  - OK returns on the first read. Its CRC-32 covers the SEQ at offset 8, because `nvm_klj2_check` re-parses the header from the same buffer (`nvm_klj2.c:366-379`).
  - A read the port fails leaves `prev` unchanged and does not count as a verdict.
  - Any other verdict, BLANK included, returns only when it equals an earlier verdict.
  - Otherwise the slot is UNREAD: its verdict is `VD_LEN` and its `unread` bit is set.
- **Re-stages.** A re-stage gets three tries. A slot that never re-stages to OK under its picked SEQ is marked UNREAD, and the other slot is offered. The loop is bounded because each pass removes one OK slot.
- **No SEQ from unvalidated bytes.** `st.seq` is taken only from a re-staged, CRC-checked container, or is 0 when no slot was accepted.
- **HELD.** Any `unread` bit sets `NVM_P_HELD` after release. In HELD:
  - `nvm_step` does nothing;
  - `nvm_store_changed` still marks the change and publishes `dirty`;
  - `nvm_store_commit_now` refuses.
- **The `authority_unknown` check** (`nvm_checks_write.py:469-541`):
  - it covers both orientations at SEQ 1, 5, 0x80000000 and 0xFFFFFFFF;
  - it runs four faults: three failed reads (held), two failed reads, an unreported flipped bit, and an aliased read that reads blank;
  - each case runs on through a clean reboot, a change, a commit and another clean reboot, and compares the restored payload each time.
- **The generation-restart control `unread_not_held` fails on the loss itself.** I re-ran it to print every finding (`receipts/probe_mutant_unread_not_held.log`): 35 findings.
  - At every SEQ, in both orientations, the assertions on the committed change and on the restored payload fail ("clean reboot: state of records ... differs from the slot").
  - So the check catches the lost commit itself, not only through its direct "not held" assertion.
- **The other planted defects.** `read_not_retried`, `refusal_unconfirmed`, `blank_unconfirmed`, `restage_not_retried` and `fallback_restage_unchecked` are all caught (`receipts/selftest_1x1.log` lines 24-29).

**The manager's question: a slot whose every read fails.** My probe `scripts/probe_held.py` runs three cases (`receipts/probe_held.log`, rc 0):
- A valid and B dead;
- A valid at 5 and B valid at 6 but dead;
- A dead and B blank.

Each case runs three faulted boots and then a clean one. Every faulted boot:
- returns from boot and releases AECP exactly once;
- keeps the service loop stepping for 50 s of model time (500,000 calls), with 20 changes and 20 console commits;
- erases and programs nothing, and refuses all 20 console commits;
- reports `phase=HELD`, the `unread` bit, `read_faults=3` and `dirty=1`;
- applies the readable slot where there is one.

So HELD does not deadlock the device, and it reports the condition.

**Reset is the only exit.** The hold repeats on every faulted boot. The first clean boot ends it and commits, at the next SEQ when a slot was accepted, else at SEQ 1. Decision 2's text ("until every slot has been read without a media fault, persistence is refused") permits this. Its consequence for a slot that never reads cleanly is R500-3-S1.

### Decision 1

- **The page.** FASTCONNECT section 7 reads `newer = (int32_t)(A.seq - B.seq) >= 0 ? A : B`, cites 5997929153, and says that slot A is offered on equal sequences.
- **The store and the shipping writer agree.** The store's `nvm_pick` (`nvm_store.c:216`) and the shipping writer's `nvm_pick_slot` (`milan_baremetal.c:1339`) both use `>= 0`.
- **The oracle.** `newer_wins` adds ties at 7 and at 0xFFFFFFFF, with distinct payloads, and expects A.
- **The control.** `tie_picks_b` is caught ("seq A 0x7 B 0x7: chose 1, want 0").
- **No other authority disagrees.** No other page, script or HDL in the tree states a tie rule (git grep).

### Service bound

- **The per-call deadline.** `LS_CALL_US` = 2,000 us is checked every 64 not-ready status reads, counted over the whole call (`plat/nvm_flash_litespi.c:81-109`).
- **The nominal and cumulative figures, per port, all five shapes** (`receipts/probe_port_maxima_*.log`).

  | Port | No stall taken | Stalled |
  |---|---:|---:|
  | Model | 168 us | none |
  | LiteSPI | 210 us | 2,189 us, or 2,190 us at `endstation_arty_4x4` |

  These equal the PR body and the README.
- **The measured-master table.** Every row reproduces at 1x1 and 8x8: 539, 859, 1,859, 2,189, 2,009, 210, 333 and 170 us (`receipts/probe_master_table_*.log`). At 4x4 each row is 1 us higher, and the README scopes its table to 1x1 and 8x8.
- **The bound against an adversarial sweep.** `scripts/probe_bound_sweep.py` ran 4,455 slowed-master patterns the suite does not run:
  - TX, RX and drain stalls;
  - counts from 1 to 999,999, five skips and nine poll lengths from 64 to 4,095;
  - in the program, erase and program-wait phases.

  The worst call was 2,190 us, within `CALL_BOUND_US` = 2,213, and nothing hung (`receipts/probe_bound_sweep.log`).
- **The 41,970 us figure.** `call_deadline_ignored` really produces `max_call_us=41970 > 2213` (`receipts/probe_mutant_call_deadline_ignored.log`). Its first-listed failure, `protected=3`, comes from the test's static `--protect-auth`: under the defect, an early slow commit lands in A, and later attempts target B. It is not a store write into a live authority.
- **The derived CPU figure.** The README and the PR body call the CPU figure "a floor only, compared with nothing".

## Findings

### R500-3-F1: MAJOR. Lenses: Conformance, RTL, Robustness, Tests, Docs

**Artifact.**
- `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:66-68`: `LS_TICKS_PER_US (CONFIG_CLOCK_FREQUENCY / 1000000u)` and `_Static_assert(CONFIG_CLOCK_FREQUENCY % 1000000u == 0u, ...)`. The same integer is used at `:93` and `:250`.
- `sw/firmware/ctrl_nvm/host/stubs/generated/soc.h` and `test/rv32/generated/soc.h`: `#define CONFIG_CLOCK_FREQUENCY 100000000` for every shape.
- `README.md:70-72`, `:77`: "`CONFIG_CLOCK_FREQUENCY`, 100 MHz".
- `README.md:15-17` and `:303-317`, and the PR body's per-shape claims.

**Title.** The on-chip flash port cannot be built for the three Arty shapes, and the gate's clock stand-in reports those shapes OK.

**Authority and evidence.**
- **The shapes' clocks.** `configs/endstation_arty_current.yaml:107`, `endstation_arty_4x4.yaml:66` and `endstation_arty_8ch.yaml:101` ship `sys_clk_hz: 83333000`; the two AX7101 shapes ship 100,000,000.
  - `sw/builder/endstation_builder.py:4834-4835` passes `--sys-clk-freq 83.333e6` for them, and `configs/generated/sweep_opts_arty.sh` shows it.
  - LiteX emits `CONFIG_CLOCK_FREQUENCY` as that integer, and `timer0` counts that clock.
- **The compile probe.** `scripts/probe_arty_clock.sh` builds the port with the RV32 arm's own flags, against the suite-generated shape header for `endstation_arty_current`. The result (`receipts/probe_arty_clock.log`):
  - at 100,000,000 the port compiles (rc 0);
  - at 83,333,000 it fails with `error: static assertion failed: "a whole number of clocks per us"` (rc 1).
- **The stand-ins hide it.** Both clock stand-ins fix 100 MHz, so for all five shapes the suite and the RV32 arm print "OK across 5 shape(s)" and report bss and text (`receipts/suite_endstation_arty_*.log`). At the clock those shapes ship, the port does not exist.
- **The authorities.** Lane assignment item 1 asks for an on-chip SPI flash controller implementation. The #665 body says the firmware "must port". The README says that exit 0 "means every check passed on every shipped shape, both flash ports". AGENTS section 6, Tests: "Tests do not merely reproduce implementation assumptions."
- **When it came in.** The assertion arrived in round 2 (`c1fb42a5`). No prior public finding names it.

**Impact.**
- When F0's switch links the store into an Arty image, the build fails. Three of the five shipped shapes have no on-chip saved-state port.
- The obvious local fix, dropping the assertion, makes the integer ticks-per-us 83. The time base then runs 0.4 % fast, and the deadline becomes 166,000 ticks rather than 166,666.
- The static-size table and the per-shape LiteSPI results for the Arty shapes describe a build that cannot be made at their clock.

**Required outcome.**
- The port's time base and per-call deadline are exact for every shipped shape's `CONFIG_CLOCK_FREQUENCY`. For example, ticks convert to microseconds through the clock in hertz, in 64 bits, with no whole-MHz assumption. Alternatively, an owner decision restricts the port to whole-MHz clocks, and the shapes it cannot serve are stated.
- The host suite and the RV32 arm build the port at each shape's own `sys_clk_hz`, taken from its config, not at a fixed 100 MHz.
- The clock-dependent checks hold at 83.333 MHz: `time_base`'s wrap window, which assumes 42.9 s, and the deadline checks.
- A planted defect fails the gate at an Arty shape, for example the whole-MHz assertion restored, or a truncating ticks-per-us.
- The README states the clock per shape.

**Verification.**
- `scripts/probe_arty_clock.sh <checkout> <scratch> <rv32-gcc>` gives rc 0 at 83,333,000, after `scripts/gen_shape_header.py` writes the shape header.
- The lane gate's per-shape output shows the Arty shapes built and run at 83,333,000 Hz, with every check green and the new planted defect reddened.

### R500-3-R1: RESIDUE. Lens: Docs

- **Artifact:** `sw/firmware/ctrl_nvm/README.md:96-97`: "So a ready master costs one timer read, and a master that stops being slow just before the deadline lets the call finish at the ready pace."
- **Why it is only wording:** it holds in the model, where status reads show readiness at once. On chip, each byte's link time leaves RX status reads not ready, so a healthy call also reads `timer0` about once per 64 such reads. It changes no figure, test or bound.
- **Exact fix:** "So a master that shows readiness at every first status read, as the host model does, costs one timer read; on chip, each byte's link time makes some RX status reads find it not ready, so a healthy call reads `timer0` about once per 64 of those. A master that stops being slow just before the deadline lets the call finish at the ready pace."

### R500-3-S1: SUGGESTION. Lenses: Robustness, Docs

**Artifact.** `nvm_store.c:410-416`, `README.md:174-183` and the PR's "Known limitations".

**Observation.** HELD's only exit is a reset whose boot reads every slot cleanly. Two kinds of slot never do:
- a slot with a permanent read fault;
- a slot whose reads disagree every boot.

The second is plausible on this board. `sw/litex/milan_soc.py:2704-2713` records memory-mapped reads that "CRC differs per read" on one placement. Flash cells left marginal by a power cut inside a program or erase can also read differently from one read to the next. For such a slot the device keeps serving but never persists again, and only the status reports it. The module page says "until reset" but not "never, while the slot stays unreadable".

**Analysis for the manager.** The generation restart in R501-2-F1 needs both of these:
- no slot is authoritative;
- the UNREAD slot survives the commit.

When one slot is accepted, the commit target is always the other slot (`nvm_target_slot`), which is then the UNREAD one. It is erased and rewritten at the accepted SEQ + 1, so no container is left surviving above the new one. A hold limited to the no-authority case would therefore keep decision 2's safety and avoid the permanent loss in the one-slot-readable case. Decision 2 as written refuses persistence in both cases, and the code follows it.

**Suggestion.**
- State the permanent consequence in the README and the PR.
- Put the narrower hold to the owner as a possible decision change.

### R500-3-S2: SUGGESTION. Lens: Robustness

**Observation.** In HELD, a change raises `dirty=1`, but `stale` stays 0 (`receipts/probe_held.log`). The README defines `stale` as a failed commit's claim, and decision 2's report is the `unread` bit plus the phase. Neither is wrong.

**Suggestion.** When the status is mapped onto FASTCONNECT 9.2's `nvm_backed`/`nvm_stale` at integration (F0/F5), state how HELD with outstanding changes is presented.

### R500-1-S1, retained: SUGGESTION. Lens: Tests

`test_ctrl_nvm.py` is still in no workflow under `.github/`. The executor lists it as carried.

## Prior public findings: resolved or retained at this head

| Prior finding | At this head |
|---|---|
| R501-2-F1 MAJOR, the generation restart after a transient read fault | RESOLVED: decision 2 is implemented, `authority_unknown` gives the required verification, and the control fails on the loss itself (above) |
| R501-2-F2 MINOR, nominal and cumulative bounds | RESOLVED: the per-call deadline; 250 us asserted per nominal call and 2,213 us per call overall; the every-wait case in `port_deadline`; the PR's figures scoped and re-measured by me on all five shapes; a 4,455-pattern sweep within the bound |
| R501-2-F3 MINOR, the tie rule | RESOLVED by decision 1: the page, store, oracle and control are aligned |
| R500-2-F1 MINOR, the binding walk skipped on an unproven model | RESOLVED. `nvm_restore` runs the slots, the binding walk, the model check and the D3 walk, which is MATERIALIZATION 8.1 steps 3 to 8. `model_unproven_closes` asserts the bindings applied, `bind_terminal` COMPLETE, CLOSED and nothing released. `bindings_skipped_unproven` and `model_ready_ignored` are caught |
| R500-2-F2 MINOR, the derived bound is not a bound | RESOLVED, as R501-2-F2 |
| R500-2-F3 MINOR, the fallback re-stage and the DR2a boundary untested | RESOLVED: `fallback_restage` and the `debounce` boundary case; `fallback_restage_unchecked` and `taken_off_by_one` are caught ("erase 1704 us after it") |
| R500-2-F4 MINOR, DR2b leaves `stale` set | RESOLVED: `nvm_heal()` runs at a DR2b suppression (`nvm_store.c:509`); `recovers_after_failure` ends `stale=0`; `dr2b_keeps_stale` is caught |
| R500-2-S1 SUGGESTION, a failed fallback stays `VD_OK` | RESOLVED: both slots `VD_LEN` and UNREAD (`fallback_restage`) |
| R500-1-F1 to F6, R501-1-F1 to F4 | Resolved at round 2 by both round-2 reviews; nothing regresses here. The 80-defect self-test, which includes their planted defects, is green at this head |
| R500-1-S1 SUGGESTION | RETAINED (above) |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Decisions 1 and 2 and round-3 items 1-5 against `nvm_store.c:135-417`, `nvm_klj2.c:255-380`, FASTCONNECT 7 as amended, MATERIALIZATION 8.1, `milan_baremetal.c:1335-1339`; lane item 1's on-chip port against `configs/endstation_*.yaml` clocks (`probe_arty_clock.log`) | R500-3 | `9412006bd58c002835bb06d46045c53098cc59a5` |
| RTL | UNCLEAN (F1) | No HDL in the lane diff. The write-path FSM, `nvm_store.c:421-745` (HELD and OFF terminal, every fail exit to IDLE); the boot read and re-stage loops and their bounds; the SEQ wrap at 0xFFFFFFFF; `plat/nvm_flash_litespi.c` deadline, wrap-safe `timer0` difference and clock assumption; no gitlink change against live dev | R500-3 | `9412006bd58c002835bb06d46045c53098cc59a5` |
| Robustness | UNCLEAN (F1) | Permanent read failure on either slot across three boots (`probe_held.log`); 4,455 slowed-master patterns (`probe_bound_sweep.log`); the power-cut sweep (3,126 cases in the gate); read fail, flip and alias at every boot read; the 83.333 MHz configuration (`probe_arty_clock.log`) | R500-3 | `9412006bd58c002835bb06d46045c53098cc59a5` |
| Tests | UNCLEAN (F1) | `test/*.py`, `test/nvm_test.c`, `host/*`; the gate per shape at rc 0, 40 checks each (`suite_*.log`); 80 of 80 planted defects (`selftest_1x1.log`); full findings of `unread_not_held` and `call_deadline_ignored`; per-port maxima on five shapes; the clock stand-ins `host/stubs/generated/soc.h`, `test/rv32/generated/soc.h` | R500-3 | `9412006bd58c002835bb06d46045c53098cc59a5` |
| Docs | UNCLEAN (F1; R1 is RESIDUE) | `sw/firmware/ctrl_nvm/README.md` (the 29/7/4 check split, the static-size table and the bound table re-measured), the FASTCONNECT 7 edit, the `docs/README.md` row, header comments, PR body; docs gates at rc 0: `docs_check`, `check_em_dash --base 28f9666f` (0 findings over 415 lines), `gen_toc --check` and `--verify-anchors`, `check_doc_paths`, `git diff --check` | R500-3 | `9412006bd58c002835bb06d46045c53098cc59a5` |

## Other evidence at this head, all rc 0

- `nvm_hosttest/test_nvm_firmware.py --self-test`
- `check_nvm_capture.py`
- `check_nvm_record_space.py`
- `check_cpp_idiom.py` and `check_py_idiom.py`
- `check_baremetal_only.py --check`
- The merge: `git diff 716d3213..e2000ef9` is byte-identical to `git diff 510fae60..28f9666f` (sha256 `6945c246…4b23`).
  - Its only path is `docs/findings/653_DISCONNECT_ORDER_BENCH.md`.
  - `9412006b` touches four lane files.
  - `milan_baremetal.c` is blob `1cebba0b` at base, dev and head.
  - Against live dev the lane changes 32 files.

## Real limits

- **The Arty clock.** Only the compile is shown. Arty runtime behaviour at 83.333 MHz is untested, because the port cannot be built there.
- **CPU time is not measured.** Nothing executes the RV32 build. Every call figure here is model time.
- **LiteSPI read faults.** LiteSPI reads are memory-mapped, so read faults reach the model port only. The decision-2 checks are model-port checks, as the suite states.
- **Read instability.** The suite and my probes model permanent and counted faults, not cells that read differently from one read to the next.
- **Physical calibration NOT RUN.** There is no hardware, real power cut or real LiteSPI timing here. Field skips are not hardware proof.
- **Hosted checks.** `receipts/hosted_checks.tsv` holds a snapshot at 2026-10-05T17:05:55Z on the exact head:
  - success: `rtl-fast`, the four Yosys shards, `yosys-elaboration`, Verilator shard 3/5, `verilator-lint`, `full-ci-gate`, `docs-check-no-git`, `changes`, `bdd-conformance` and `wire-accountability`;
  - in progress: Verilator shards 0, 1, 2 and 4, `docs-check` and `elaborate`;
  - skipped, not executed: "Physical gPTP (nightly and manual)".

  None of these is used as evidence here; the manager owns hosted and act acceptance.
- **Not run:** the full parent, PP, gPTP, Yosys and builder banks, Docker, act and the host CI runner.
- **The two defect-detail logs** (`probe_mutant_*.log`) exited 0 in the session, and no `.rc` file was kept for them.
- **Clone state** (`receipts/integrity.log`, rc 0):
  - 1,041 superproject blobs, with their bytes and modes, match tree `ba76ab76`, and so does the index;
  - protocol-processor `ead80360` (558 blobs), gptp-processor `5dce647a` (104) and verilog-axis `48ff7a7e` (214) match their gitlinks;
  - nothing is untracked or ignored. The bytecode caches the runs created were removed. No tracked file was edited; planted copies and builds lived only under `scratch/`.
- **Redaction.** One compiler path in `probe_arty_clock.log` was rewritten to `<checkout>`.

## Pending manager duties

- Hosted and act acceptance at the exact head, and the final current-dev candidate build: source base `fa450d30`, live dev `28f9666f`.
- Route R500-3-F1 to the executor. Put R500-3-S1's narrower-hold question to the owner if it is wanted. Carry R500-3-R1 to the residue checklist.
- Carry the executor's open items: the shipping writer's VD_REC/VD_LEN parity gap; #671; the lane gate in a hosted workflow.
- Obtain R501-3's independent verdict, and after fixes a new round at the new head covering every lens.

## Reproduction

From an exact detached checkout, with this packet as `$PKT` and a scratch directory `$S`:

```sh
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 $PKT/scripts/gen_shape_header.py "$PWD" endstation_arty_current $S/clk83
sh $PKT/scripts/probe_arty_clock.sh "$PWD" $S/clk83 <rv32-gcc>
python3 $PKT/scripts/probe_held.py "$PWD" $S/held
python3 $PKT/scripts/probe_port_maxima.py "$PWD" $S/pm <config-stem>
python3 $PKT/scripts/probe_master_table.py "$PWD" $S/mt <config-stem>
python3 $PKT/scripts/probe_bound_sweep.py "$PWD" $S/sweep endstation_ax7101_1x1_tdm8 14
python3 $PKT/scripts/probe_mutant_findings.py "$PWD" $S/mut <defect-name>
python3 -B $PKT/scripts/verify_integrity.py "$PWD" 9412006bd58c002835bb06d46045c53098cc59a5
```

The scripts read the checkout and write only under the scratch directory given. Every published receipt is listed in `MANIFEST.sha256`.

R500-3 FINISHED
