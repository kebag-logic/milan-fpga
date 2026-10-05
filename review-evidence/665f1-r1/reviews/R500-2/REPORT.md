[R500] NEGATIVE - exact head 7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11

# R500-2: internal cleared-context review of PR #669 (#665 lane F1), round 2

- **Head under review:** `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11`, tree `86236b61ec36ed252d6f91d698f2784302ef3743`. It equals the PR's published head.
- **Shape of the round:** `215c3c0b` (round 1), then:
  - `c1fb42a5` (code and suite);
  - `7725bcfa` (module page);
  - `7f8dc1b1`, a `--no-ff` merge of dev `510fae60`.
- **Source base:** `fa450d301805881ad713b67521477bf042ddadfd`. Live dev is `510fae60b26bef1db138de5cf2ac72b17b5011a5`.
- **Reconstructed from**, in the public order:
  - AGENTS.md and CONTRIBUTING.md, then docs/README.md;
  - the #665 body, the lane F1 assignment (5993775541), the bare-metal directive (5992455815) and the round-2 assignment (5996009284);
  - the executor's TAKEN (round 2) and REVIEW READY (round 2) comments;
  - SAVED_STATE_FASTCONNECT.md sections 6.2, 7, 9.2 and 9.4, and SAVED_STATE_MATERIALIZATION.md sections 6.3, 8.1, 8.6 and 15.1, at the head, including the dev merge's amendments to both;
  - the diff `fa450d30..7f8dc1b1` and its history;
  - the PR body, and the exact-head hosted check list.
- **Prior findings:** R500-1 and R501-1 were read only after this round's verdict and ledger were drafted.

All five lenses were applied. Every round-1 finding of both reviews is resolved in code, and the 24 new planted defects are real. **Four new MINOR findings remain open, so every lens is UNCLEAN and the verdict is NEGATIVE:**

| ID | Severity | What is wrong |
|---|---|---|
| R500-2-F1 | MINOR | The binding walk is skipped on an unproven model. |
| R500-2-F2 | MINOR | The derived service bound is not a bound. |
| R500-2-F3 | MINOR | Two round-2 claim paths survive planted defects. |
| R500-2-F4 | MINOR | A DR2b suppression leaves `stale` set with nothing un-durable. |

None of the four is wording only.

## Round-2 assignment (5996009284), item by item

| Item | Verdict at this head | Evidence |
|---|---|---|
| 1. Time base | RESOLVED | See "Time base" below. |
| 2. Strict DR2c | RESOLVED | See "DR2c" below. |
| 3. Boot judges the RAM copy | RESOLVED in code; one path untested (R500-2-F3) | See "Boot judgment" below. |
| 4. Bounded LiteSPI waits | RESOLVED in code; the stated bound is wrong (R500-2-F2) | See "Bounded waits" below. |
| 5. DR2a after a mid-capture change | RESOLVED in code; the boundary is untested (R500-2-F3) | See "DR2a" below. |
| 6. Bindings outside the D3 transaction | RESOLVED for faults and roll-back; ordering against the model check is open (R500-2-F1) | See "Bindings" below. |
| 7. A planted defect per claim | MOSTLY | All 24 new planted defects are real (next section). Two reviewer plants on round-2 claim paths survive (R500-2-F3). |
| 8. README bound stated as derived | PARTIAL | The three figures are now separated, but the derived figures do not bound anything (R500-2-F2). |
| 9. `--no-ff` merge of dev | RESOLVED | See "The dev merge" below. |

**Time base (item 1).**
- `ls_now_us` reads `timer0` only and accumulates it into 64 bits (`plat/nvm_flash_litespi.c:202-223`). No store or port code reads the PHC; only the host model keeps one, so the tests can step it.
- `nvm_flash_wait` is gone.
- The `time_base` check is LiteSPI-only. It steps the PHC by -60 s and by +60 s in four places: the window, the backoff, a hung erase (3,500 ms) and a hung program (50 ms). It also runs a window across the 42.9 s wrap.
- Both of its planted defects are real:
  - `phc_time`: "PHC -60000 ms in the window: erase None";
  - `clock_not_accumulated`: "erase 451365 us after the change".
- My own plant `half_backoff` is caught by `time_base` as well ("retry 501605 us").

**DR2c (item 2).**
- The code paths are `nvm_store.c:398-427`, `:463-480` and `:675-685`.
- The five planted defects fail for their defect (`receipts/mutant_detail.log`):

| Planted defect | Result |
|---|---|
| `budget_rearmed_by_change` | `failed=39` |
| `budget_rearmed_by_capture` | `failed=62` |
| `commit_now_overrides_exhaustion` | `withheld=0 failed=11` |
| `commit_now_ignores_backoff` | retry 183,703 us after the failure |
| `success_forgives_exhaustion` | `abandoned=0` |

- My plants `four_attempts`, `half_backoff` and `exhausted_sticks` are all caught.
- The exhaustion record matches D3 6.3 and FASTCONNECT 9.2 as amended at this head: the firmware has no alarm of its own, and `nvm_alarm` belongs to the producer.

**Boot judgment (item 3).**
- `nvm_slot_check` (`nvm_store.c:125-163`) judges the second read of a slot. The CRC, the records and the SEQ all come from the stage bytes.
- `nvm_stage_slot` (`:179-188`) re-judges the pick with its CRC and requires the pick's SEQ.
- Its planted defects are real:
  - `select_on_unchecked_reread`, R501-1-F1's probe: "the older slot's flipped word displaced the newer";
  - `stage_seq_unchecked`: "published 0x5, staged 0x5" against slot 0's 0x6;
  - `slot_read_fail_ignored`.
- No check covers the fallback pick's own re-judgment (R500-2-F3).

**Bounded waits (item 4).**
- `ls_ready` and the drain in `ls_open` give up after `LS_POLL_MAX`, and `ls_window` always releases chip select (`plat/nvm_flash_litespi.c:65-124`).
- The model withholds readiness, and a firmware still spinning after 1,000,000 reads counts as hung.
- The lane's planted defects are real: `xfer_unbounded` and `open_unbounded` both give `ls_hung=1`, and `stall_ignored` gives first verdict 13 in place of 12.
- My plants `cs_kept_on_stall`, `busy_stall_as_busy` and `poll_max_16x` are caught. The last one reads `max_call_us=2630 > 1000`.

**DR2a (item 5).**
- The code is `nvm_store.c:338-346` and `:657-673`.
- The planted defect `capture_leaves_window_armed` is real: "erase 1703 us after it".
- The boundary record is untested (R500-2-F3).

**Bindings (item 6).**
- The binding walk is its own unit (`nvm_store.c:213-230`), and a D3 roll-back passes `NVM_W_D3` only (`:234-240`). This matches D3 8.1 steps 4-5 and 8.6.
- All four planted defects are real. Two examples:
  - `d3_rollback_takes_bindings`: `sm_unbinds=1`, and "records 0x20, 0x21 differ";
  - `binding_fault_aborts_d3`: terminal 3.

**The dev merge (item 9).**
- `git diff 7725bcfa..7f8dc1b1` is byte-identical to `git diff fa450d30..510fae60`: sha256 `1687d3b6…93a3` on both (`receipts/merge_check.log`).
- The merge-base is `fa450d30`.
- No path under `sw/firmware/ctrl_nvm/`, and not `docs/README.md`, is in the merge's delta.
- Against live dev, the lane changes 31 files: everything under `sw/firmware/ctrl_nvm/` plus the `docs/README.md` row.
- `milan_baremetal.c` is blob `1cebba0b` at both base and head.

## The new planted defects are real

`receipts/gate_full.log` reproduces the gate at the head with rc 0 in 168 s:
- 5 shapes, 37 checks each (29 on both ports, 5 on the model port only, 3 on LiteSPI only);
- 69 of 69 planted defects caught;
- RV32 bss 3,144 / 4,032 / 5,436 / 7,996 / 14,392 B and text 10,981 to 11,001 B, equal to the README table.

Round 2 adds 24 planted defects to round 1's 46 and retires one, `attempts_kept`, which encoded the re-arming R500-1-F2 rejected: 46 + 24 - 1 = 69. Each of the 24 new ones fails for the defect it names. Its first failure text is in `gate_full.log` lines 15, 28-30, 41-44, 47, 52-56, 59-60, 62-64 and 75-79, with full detail for eight of them in `receipts/mutant_detail.log`.

The self-test counts a defect as caught only when every check it names turns red. A planted copy that does not build, or a runner that crashes, refuses the whole gate (exit 2); neither is counted as a catch (`test_ctrl_nvm.py:100-115`, `nvm_bench.py:122-129,168-181`).

## Prior public findings: resolved or retained at this head

| Prior finding | At this head |
|---|---|
| R500-1-F1 MAJOR, the PHC holds on a backward step | RESOLVED (item 1 above) |
| R500-1-F2 MAJOR, DR2c re-armed, alarm forgiven | RESOLVED (item 2 above) |
| R500-1-F3 MINOR, DR2a window left armed | RESOLVED in code; the boundary case is RETAINED as part of R500-2-F3 |
| R500-1-F4 MINOR, bindings inside the D3 transaction | RESOLVED; a related ordering defect is new, R500-2-F1 |
| R500-1-F5 MINOR, claims with no planted defect | RESOLVED for the five listed: `verify_skips_last_stretch`, `blankcheck_first_stretch_only`, `tie_picks_b`, time, `program_refusal_ignored`, plus read failures at boot, blank check and read-back. Two new survivors are R500-2-F3 |
| R500-1-F6 MINOR, the service-bound sentence | RESOLVED as to separating model time from CPU time; the derived figures are RETAINED as R500-2-F2 |
| R500-1-S1 SUGGESTION, the lane gate is in no hosted workflow | RETAINED as a suggestion; the executor lists it as an open risk |
| R501-1-F1 MAJOR, selection on an unchecked re-read | RESOLVED (item 3); R501-1's own probe shape is now a check |
| R501-1-F2 MAJOR, console bypasses DR2c | RESOLVED (item 2) |
| R501-1-F3 MAJOR, PHC clamp | RESOLVED (item 1) |
| R501-1-F4 MAJOR, unbounded SPI waits | RESOLVED as to boundedness. Its required "documented bound must state its actual assumptions and include failure paths" is RETAINED as R500-2-F2 |

## Findings

### R500-2-F1: MINOR. Lenses: Conformance, RTL, Tests, Docs

**Artifact.**
- `sw/firmware/ctrl_nvm/nvm_store.c:300-305`: the model check returns CLOSED before `nvm_choose` (`:314`) and `nvm_walk_bind` (`:325`) run.
- `test/nvm_checks.py:463-469`: `model_unproven_closes` asserts `sm_applies == 0`.
- `README.md:102-103` and `nvm_state.h:17-23`.

**Title:** an unproven entity model skips the binding walk that D3 8.1 runs before the image check.

**Authority and evidence.**
- MATERIALIZATION 8.1 orders the binding walk (step 4) and its drained terminal (step 5) before step 6: "An image it still cannot validate ends the restore CLOSED: nothing can be judged against it." It also says "A CLOSED terminal holds AECP and the enable until a reset, and does not take the listener's faces back."
- Section 8.6 places the same refusal at the D3 walk: "An image the restore cannot prove before pass 0 ends it CLOSED (cause 7)."
- At the head (`receipts/probes.log`): `--not-ready` on a golden slot gives `terminal=4 sm_applies=0 bind_terminal=0`, with 2 binding records in the shape.
- The reviewer plant `bindings_before_model_check` runs the binding walk before the model check. Only `model_unproven_closes` reddens (`applied=2`), so that check encodes the deviation.
- The README cites "D3 section 8.1 step 6" for an order that step 6 does not have.

**Impact.** With an unproven image, the saved listener bindings are never restored for that power cycle. The authority restores them and leaves the listener serving at CLOSED. The state port's two-walk contract is broken on this path.

**Required outcome.** One of:
- the binding walk runs on this path, as in 8.1 step 4, with the model check gating the D3 walk only; or
- the deviation is published for an owner decision and stated in `nvm_state.h` and the README.

Either way, the check asserts what was decided, and a planted defect fails it.

**Verification.** `--not-ready` on a golden slot shows:
- the bindings applied and `bind_terminal` COMPLETE;
- terminal CLOSED;
- `releases=0`.

Alternatively, the decision is cited.

### R500-2-F2: MINOR. Lenses: Conformance, Robustness, Tests, Docs

**Artifact.**
- `sw/firmware/ctrl_nvm/README.md:81-87` and `:219-227`, and the PR body's "The service bound";
- `plat/nvm_flash_litespi.c:54-57`, `:65-74`, `:96-104` and `:115-124`;
- `test/nvm_checks_write.py:388-391`.

**Title:** the derived service bound is not a bound.

**Authority.**
- The #665 rule: "Each protocol states its firmware service-latency bound per response path and tests it".
- Round-2 assignment items 4 ("each service step stays bounded") and 8 ("the README states the service bound as derived, with its assumptions").
- R501-1-F4's required outcome: "The documented bound must state its actual assumptions and include failure paths."

**Evidence.**
1. **The arithmetic does not meet its own inputs.** The README says "A stalled wait adds its 4,096 reads; at an assumed 0.5 us per CSR read ... that is at most 2 ms". The stall alone is 4,096 × 0.5 us = 2.048 ms. The 262 bytes, with at least four CSR accesses each, add at least 524 us at the same rate. That is at least 2.57 ms under the README's own assumptions.
2. **The bound is per wait, not per call.** The README says "a master that is slow but moving never trips it". A page program makes two waits per byte.

   | Slow-master case (`receipts/probes.log`) | Longest call, model time |
   |---|---|
   | Every TX (or RX) wait withheld 4,000 reads | 41,970 us, and the commit still succeeds |
   | Every wait withheld 4,095 reads | 42,961 us |

   That is 42 times the 1,000 us the README says every run holds. At the README's own 0.5 us per read, the same call is about 262 × 2 × 4,095 × 0.5 us ≈ 0.54 s.

   The suite's slow case withholds only two waits (`"tx:2:0:4000"`, longest call 529 us). The README describes it as "a command master slow by 4,000 reads a wait".
3. **A floor cannot sit inside a ceiling.** The capture figure of about 1.2 ms is stated as "a floor, not a ceiling". The page still concludes that "Both sit well inside the 24.5 ms".

**Impact.** No figure in the module page or the PR bounds a service call on the CPU, which the #665 rule asks for. A degraded but moving master can hold the single event loop for about half a second per program call, with no failure reported.

**Required outcome.**
- The stated bound follows from the code's actual limits: waits per call × `LS_POLL_MAX` × a stated cost per read, plus the per-byte work. Alternatively, the port caps the total no-progress reads per call, so the stated figure holds.
- The arithmetic matches its inputs.
- The capture figure is not placed inside 24.5 ms unless an upper figure supports it.
- The slow-master check either grades the per-call bound with every wait slowed, or the README describes what it actually exercises.

**Verification.**
- Re-read the README's "The service bound".
- Rerun `probes/r500_2_probes.py` and compare the every-wait slow-master case with the stated bound.

### R500-2-F3: MINOR. Lens: Tests

**Artifact.**
- `nvm_store.c:283-284`, the fallback pick's re-stage judgment;
- `nvm_store.c:666`, `r.id >= nvm.cursor.id`;
- `test/nvm_checks.py:293-385`, `test/nvm_checks_write.py:107-139` and `test/nvm_mutants.py`.

**Title:** two round-2 claim paths are guarded by code that no check can fail for.

**Authority.**
- Round-2 item 7: "each claim the suite rests on gets a planted defect that fails".
- AGENTS section 6, Tests: "Each new test can fail for the defect it claims to detect."
- README:117-118: "A slot that does not read back as it was judged gives way to the other".
- README:165: "A change the running capture has yet to reach is taken by that capture and opens no window".
- R500-1-F3's verification: "a check plus mutant cover a change during capture".

**Evidence** (`receipts/probes.log`, `receipts/demos.log`).
- The plant `fallback_restage_unchecked` drops the fallback's re-judgment and SURVIVES all 18 boot checks on both ports.
  - Demonstration: both re-stage reads return one flipped bit.
  - The head ends BLANK and applies nothing.
  - The plant applies the older slot COMPLETE, and record 0x8f differs from that slot's bytes. Corrupted bytes are applied: the item-3 invariant.
- The plant `taken_off_by_one` (`>` for `>=`) SURVIVES `debounce`.
  - Demonstration: a change hits the record the capture examines next, and a second change follows 5 s after the commit.
  - On the head, the second erase starts 1,001,703 us after the second change.
  - On the plant, it starts 1,703 us after it. That is R500-1-F3's defect, back at the boundary record.

**Impact.** A regression on either path brings back a round-1 defect with every check green.

**Required outcome.**
- A boot check that fails when the fallback slot is applied without its re-judgment, for example with both re-stage reads faulted.
- A DR2a case whose change hits the record the capture examines next.
- Each with a planted defect in `nvm_mutants.py`.

**Verification.**
- `probes/r500_2_probes.py` reports both plants CAUGHT.
- The gate's self-test reddens both.

### R500-2-F4: MINOR. Lenses: Conformance, Robustness, Tests, Docs

**Artifact.**
- `nvm_store.c:413-419`: the DR2b suppression clears the in-flight set and leaves `stale`;
- `nvm_store.c:575-576`: `stale` clears only inside `nvm_commit_done`, and only when nothing is dirty;
- `README.md:178-179` and `nvm_store.h:94`.

**Title:** `stale` stays set after every change is durable.

**Authority.**
- FASTCONNECT 9.2: "`nvm_stale` clears when `nvm_backed` is true again AND `nvm_dirty` is 0 -- that is, when the writer is live and nothing the outage left outstanding is still un-durable". It adds: "The rule clears the STATE, not just the view."
- D3 6.3: "A later successful commit clears `nvm_stale` under section 9.2's condition."
- README:178: "`stale` follows FASTCONNECT section 9.2".

**Evidence** (`receipts/stale.log`, both ports).
1. The first attempt fails.
2. The retry commits (`ok=1`) while a same-value change call is outstanding.
3. That call's capture is suppressed by DR2b (`skipped=1`).
4. The store ends `stale=1 dirty=0 pending=0` and idle.

The control without the repeated call ends `stale=0`. No check covers this path.

**Impact.** An ordinary repeated SET during a retry leaves the store reporting a loss, although every change is in a verified slot. It stays that way until some later unrelated commit, which is the stuck latch 9.2 rejects.

**Required outcome.**
- `stale` clears whenever 9.2's condition holds, including after a DR2b suppression leaves nothing outside a verified slot. Alternatively, the README states and justifies the deviation.
- A check and a planted defect cover it.

**Verification.** `probes/r500_2_stale.py` shows `stale=0` on both ports in the repeated-change case.

### R500-2-S1: SUGGESTION. Lens: Robustness

**Artifact.** `nvm_store.c:283-284`.

**Evidence.** When the fallback's re-stage also fails, the boot ends BLANK, but that slot's published verdict stays `VD_OK` (`receipts/demos.log` on the head: `terminal=2 vd_b=0`).

**Suggestion.** Mark the slot `VD_LEN` there, as the first pick is marked, so the status says why neither slot was applied.

### R500-1-S1, retained: SUGGESTION. Lens: Tests

`test_ctrl_nvm.py` still runs in no hosted workflow. Wire it in under the CI-events contract, or track it in an Issue.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F4) | FASTCONNECT 6.2, 7, 9.2 and 9.4, and MATERIALIZATION 6.3, 8.1, 8.6, 15.1 and the merge's amendments, against `nvm_store.c:125-685`, `nvm_klj2.c:255-380`, `nvm_state.h` and `nvm_store.h`; round-2 items 1 to 9 against the code, the README, the PR body and the REVIEW READY | R500-2 | `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11` |
| RTL | UNCLEAN (F1) | no HDL in the lane diff. The write-path state machine `nvm_store.c:601-655` (every phase, `busy<0`, the timeouts, the DR2b, DR2c and withheld exits); the boot walk order `:291-334`; the 64-bit time and `timer0` wrap arithmetic, `plat/nvm_flash_litespi.c:202-223`, against the model `host/litespi_model.c:220-259` and LiteX timer semantics; the bounded waits `:65-124`; `nvm_slot_check` widths (`img_len` against the stage) | R500-2 | `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11` |
| Robustness | UNCLEAN (F2, F4) | PHC ±60 s and the wrap (`time_base`); stalled, slow and dead masters (`port_stall` plus `probes.log`); read flip, alias and fail at every boot read; double re-stage faults (`demos.log`); repeated identical changes and console tries (`dr2c_*`, `stale.log`); the power-cut sweep (gate) | R500-2 | `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11` |
| Tests | UNCLEAN (F1, F2, F3, F4) | `test/*.py`, `test/nvm_test.c`, `host/*.c`; the gate at rc 0 with 69 of 69 planted defects; the 24 new defects' failure text (`gate_full.log`, `mutant_detail.log`); 9 reviewer plants, 7 caught and 2 survivors (`probes.log`); the README's model-time figures re-measured at 1x1 and 8x8 (`figures.log`: 167/168, 210 and 164 us) | R500-2 | `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11` |
| Docs | UNCLEAN (F1, F2, F4) | `sw/firmware/ctrl_nvm/README.md` (the static-size table and its 37/29/5/3 counts verified), the header comments, the `docs/README.md` row, the PR body; docs gates at rc 0 (`receipts/gates/`: `docs_check`, `em_dash` against both bases, `gen_toc --check` and `--verify-anchors`, `doc_paths`, `diff_check`) | R500-2 | `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11` |

## Other evidence at the head, all rc 0

- `nvm_hosttest/test_nvm_firmware.py --self-test`
- `check_nvm_capture.py`
- `check_nvm_record_space.py` and its `--self-test`
- `check_cpp_idiom.py` and `check_py_idiom.py`
- `measure_test_evidence.py --check`
- `check_baremetal_only.py --check`

The logs are in `receipts/gates/`. The em-dash and TOC gates ran under the existing pinned Markdown renderer environment. The default interpreter has no renderer and refuses with rc 2, which is not a finding.

## Real limits

- **CPU time is not measured.** Nothing executes the RV32 build. My statements on CPU time are arithmetic against the README's own stated costs.
- **LiteSPI and read faults.** LiteSPI reads are memory-mapped, so the model's read faults reach the direct port only. The suite states this.
- **Physical calibration NOT RUN.** No real LiteSPI timing, no real power cut, no hardware. Field skips are not hardware proof.
- **Hosted checks are in flight.** At exact head `7f8dc1b1`, `receipts/hosted_checks.tsv` holds a snapshot:
  - success: the four Yosys shards, Verilator shard 3/5, `verilator-lint`, `full-ci-gate`, `docs-check-no-git`, `changes`, `bdd-conformance` and `wire-accountability`;
  - skipped context, not executed: "Physical gPTP (nightly and manual)";
  - still in progress: Verilator shards 0, 1, 2 and 4, `yosys-elaboration`, `elaborate` and `docs-check`.

  None of these is used as evidence.
- **Not run (out of scope):** the full parent, PP, gPTP, Yosys and builder banks, Docker, act and the host CI runner.
- **Clone state after the probes** (`receipts/integrity.log`, rc 0):
  - all 1,041 superproject blobs and their modes match the head's tree;
  - the index equals tree `86236b61`;
  - the gitlinks match at protocol-processor `ead80360` (558 blobs), gptp-processor `5dce647a` (104) and verilog-axis `48ff7a7e` (214);
  - nothing is untracked or ignored. The bytecode caches the runs created were removed.
- **Disposable copies.** Planted copies and builds lived only under `scratch/`.

## Pending manager duties

- **Hosted and act acceptance** at the exact head, and the final current-dev candidate build: source base `fa450d30`, live dev `510fae60`.
- **Decisions the executor raised, to carry:**
  - the tie rule: FASTCONNECT 7's pseudo-code offers B on equal sequences, while the store and the shipping writer offer A;
  - an Issue for the SEQ-1 loss after a transiently refused slot. The same shape arises when both re-stages fail: the next commit erases the newer slot and writes SEQ 1 (see R500-2-S1);
  - the shipping writer's VD_REC/VD_LEN parity gap;
  - the lane gate in a hosted workflow.
- **The other review.** R501-2's independent verdict.
- **After fixes,** a new round at the new head that covers every lens again.

## Reproduction

From the root of an exact checkout, with the packet directory as `$PKT`:

```sh
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 $PKT/probes/r500_2_probes.py <scratch>
python3 $PKT/probes/r500_2_demos.py <scratch>
python3 $PKT/probes/r500_2_stale.py <scratch>
python3 $PKT/probes/r500_2_figures.py <scratch>
python3 $PKT/probes/r500_2_mutant_detail.py <scratch> budget_rearmed_by_change budget_rearmed_by_capture success_forgives_exhaustion d3_rollback_takes_bindings binding_fault_keeps_preloads binding_fault_aborts_d3 commit_now_overrides_exhaustion slot_read_fail_ignored
python3 -B $PKT/probes/r500_2_integrity.py .
```

The probes read the checkout and write only under `<scratch>`. Every published receipt is listed in `MANIFEST.sha256`.

R500-2 FINISHED
