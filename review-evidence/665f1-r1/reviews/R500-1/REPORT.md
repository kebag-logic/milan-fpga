[R500] NEGATIVE - exact head 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e

# R500-1: internal cleared-context review of PR #669 (#665 lane F1)

- **Head under review:** `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e`, tree `a574cf75a8d3a233ad7dc6b31ca31fbf1f214848`.
- **Source base:** `fa450d301805881ad713b67521477bf042ddadfd`, an ancestor of the head. Eight one-line commits with no trailers. 32 files, +4,751 lines, nothing removed.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - the #665 body and its lane F1 assignment (comment 5993775541);
  - the bare-metal directive (5992455815) and the executor's TAKEN and REVIEW READY comments;
  - SAVED_STATE_FASTCONNECT.md sections 4.2, 6.1, 6.2 and 7;
  - SAVED_STATE_MATERIALIZATION.md sections 6.1, 6.2, 8.1, 8.4, 8.6 and 15.1;
  - the shipping writer `sw/firmware/milan_baremetal/milan_baremetal.c`;
  - `scripts/nvm_klj2.py`;
  - the capture receipt `tb/verilator/nvm_capture_cpu/measurements.json`;
  - the diff and its history;
  - the manager's public evidence tree `review-evidence/665f1-r1` at `38e93660`.

All five lenses were applied. **Six blocking or lens-uncleaning findings remain open, two of them MAJOR. Every lens is UNCLEAN, so the verdict is NEGATIVE.**

## Prior public findings

PR #669 has no earlier review findings: 0 reviews, 0 inline comments, and only the two review-start comments of R500-1 and R501-1. I read that state after my own pass. Nothing is carried forward, and nothing needs resolving or retaining.

## What was verified clean (evidence for the ledger)

- **Executor's gate, reproduced at the head:** `test_ctrl_nvm.py --require-rv32 --self-test` returns rc 0 (`receipts/gate_selftest.log`). It covers:
  - 5 shapes and 26 checks, 24 of them on both flash ports;
  - 46 of 46 planted defects caught;
  - RV32I bss of 4,000 B at 1x1 and 14,360 B at 8x8, stage 3,344 and 13,264, text 10,348 to 10,368. These equal the PR's figures.
  - The 3,126 power-cut count reproduces by arithmetic: (45 + 61 + 81 + 121 + 213) cases × 3 starts × 2 ports.
- **Verdict parity (section 6.2):** a reviewer fuzz of 3,500 structured mutations finds **0 mismatches** between the C codec as the boot judges a slot and `klj2_decode` over the bytes the slot holds.
  - The mutations cover header fields, record headers, reorder, drop and duplicate, N_REC, IMG_LEN, pad, the erased faces, an extra record, identity and payload_length.
  - Every refusal verdict class was reached except `VD_STALE` (boot has no prior accepted SEQ).
  - Evidence: `probe_parity_fuzz_{1x1,8x8}.txt`.
- **Boot order:**
  - the wrap-safe pick, A on a tie (as in the shipping writer);
  - re-stage and re-judge in RAM;
  - apply, then settle after the maps and before the names, then rollback to DEFAULTS, or CLOSED when the rollback fails;
  - CLOSED on an unproven model;
  - release at COMPLETE, BLANK or DEFAULTS only;
  - all read against FASTCONNECT 6.2 and 7, MATERIALIZATION 6.2 and 8.4, and `nvm_store.c:113-285`.
- **Write path:**
  - only the non-authoritative slot is erased or programmed (`nvm_store.c:423-441`, guarded, and policed by the model's protected slot in every power-cut case);
  - ascending pages, header first;
  - the authority moves only in `nvm_commit_done` after a full read-back (`nvm_store.c:499-537`);
  - DR2b (`nvm_store.c:346-357`);
  - DR5, blank before refused (`nvm_store.c:421-428`).
- **LiteSPI port:** `ls_open`, `ls_xfer`, `ls_close`, `ls_busy`, `ls_write_enable`, `ls_command` and the PHC read are the shipping writer's code (`milan_baremetal.c:84-98, 956-1013`), unchanged in substance. Program and erase only start, and both are refused outside the journal (`ls_in_journal`).
- **Byte identity:**
  - `milan_baremetal.c` is blob `1cebba0b` at both base and head;
  - no file under `hdl/`, `tb/`, `scripts/`, `sw/litex/`, `sw/builder/` or `configs/` changed;
  - no file outside `sw/firmware/ctrl_nvm/` references the module except the docs index row. Nothing links it.
- **Focused gates at the head, all rc 0:**
  - `docs_check.py`;
  - `check_em_dash.py --base fa450d30`: 0 findings over 208 added lines;
  - `gen_toc.py --check`;
  - `check_doc_paths.py`;
  - `check_cpp_idiom.py` and `check_py_idiom.py`;
  - `check_baremetal_only.py --check`;
  - `measure_test_evidence.py --check`;
  - `check_nvm_capture.py`;
  - `nvm_hosttest/test_nvm_firmware.py --self-test`.

  Logs are in `receipts/gate_*`. The em-dash and TOC gates ran under the pinned Markdown renderer environment.
- **Hosted, at the exact head:** `rtl-fast` concluded success. `rtl-full`, `docs` and `elaborate` were still in progress when observed, so they are not used as evidence here.

## Findings

### R500-1-F1: MAJOR. Lenses: Robustness, RTL, Tests

**Artifact.** `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:18-20,187-189`, with its consumers `nvm_store.c:302-309` (DR2a window), `nvm_store.c:305` (DR2c backoff), `nvm_store.c:445-455` (erase and program timeouts) and `nvm_flash.c:16`. Title: a backward PHC step freezes the write path for the length of the step.

**Authority and evidence.**
- The port's time is the fabric PHC, "held at the last value" on a backward step.
- A grandmaster restart moves domain time backwards by the grandmaster's whole previous uptime (`docs/design/PRESENTATION_TIME_WRAP.md:33`).
- The shipping writer re-arms on a backward step instead: `now < nvm_dirty_since` at `milan_baremetal.c:1327`, and `now < nvm_hb_last` at `milan_baremetal.c:941`.

The reviewed store runs over the reviewed LiteSPI port, with only the modelled PHC moved (`receipts/probe_time_step_1x1.txt`):

| Case | What happened |
|---|---|
| no step (control) | commits at 1.0 s |
| PHC 60 s back | `ok=0 erases=0 dirty=1` 10 s later; commits only at 61.0 s |
| PHC 30 min back | still `ok=0 erases=0 dirty=1` 10 min later |

- The same hold stops `nvm_wait`'s erase and program timeouts from firing.
- The same hold makes `nvm_flash_wait` loop forever on a hung device.
- Three forward steps during erase waits exhaust a healthy device's work set (`failed=3 exhausted=1`).
- No check covers time at all. The planted defect `time_not_held` survives all 26 checks (`receipts/mutant_time_not_held.txt`).

**Impact.** After any grandmaster change to a source with earlier time, a controller's changes stay out of flash for as long as the step: minutes to days. A power cut in that window loses them, and both DR2a's window and DR2c's backoff become unbounded.

**Required outcome.** The store's elapsed-time decisions (debounce, backoff, operation timeouts, the blocking wait) stay bounded across a PHC step in either direction. Examples: a monotonic counter as the time base, or re-arming on a backward step as the shipping writer does. The port contract and the README must state the behaviour.

**Verification.**
- `probe_time_step.py` reaches a commit about 1 s after the change in the backward cases.
- A suite check moves the PHC both ways.
- A planted defect for that check is caught.

### R500-1-F2: MAJOR. Lenses: Conformance, Robustness, Tests

**Artifact.** `nvm_store.c:594-609` (`nvm_store_changed` clears `attempts` and `exhausted` on every call), `nvm_store.c:499-517` (a later success clears `exhausted`, `first_failed` and `stale`), and `test/nvm_checks_write.py:177`. Title: DR2c is not met; an unchanged work set is re-armed and the alarm is not kept until reset.

**Authority and evidence.** DR2c (MATERIALIZATION section 15.1, line 2271, RULED) says: "at most three firmware transaction attempts per **unchanged** captured work set ... After exhaustion, keep the alarm until reset ... Automatic forgiveness risks clearing evidence of an abandoned change ... Measure error bursts and erase amplification."

The reviewed store runs over a device that drops every program (`receipts/probe_dr2c_1x1.txt`):

| Sequence | Result |
|---|---|
| exhaust | `failed=3 exhausted=1` |
| then one change call that leaves the value as it was (the suite's own `--touch` DR2b input) | `attempts=0 exhausted=0` |
| the same call every 5 s for 60 s | `failed=39 erases=39` against an unchanged work set |
| exhaust, then a healthy device and a new change | `exhausted=0 stale=0 first=0` |

- No status bit retains the exhaustion until reset.
- The suite asserts the opposite: `recovers_after_failure` requires `exhausted == 0` after a new change (`nvm_checks_write.py:177`).
- The executor's public reading (HANDOFF section 8, "a new change opens a new one") does not address either the identical-value case or the alarm.

**Impact.**
- On a failing medium, repeated identical SETs drive unbounded erase attempts.
- A later success, or any change call, erases the only evidence that a work set was abandoned. That is the forgiveness DR2c forbids.

**Required outcome.**
- The attempt budget resets only when the captured work set actually changes.
- An exhaustion alarm survives later changes and successes until reset.
- The check and its mutant assert both.

**Verification.**
- `probe_dr2c.py` shows at most 3 attempts per unchanged work set and the alarm still set after a success.
- The suite check is inverted accordingly.
- A planted defect that clears the alarm is caught.

### R500-1-F3: MINOR. Lenses: Conformance, RTL, Tests

**Artifact.** `nvm_store.c:289-296` with `nvm_store.c:600-604`. Title: DR2a's 1,000 ms first-dirty window is skipped for the next change after a change captured mid-capture.

**Authority and evidence.** DR2a (line 2269) requires the 1,000 ms firmware first-dirty window. `nvm_capture_begin` disarms the window, and a change made during the capture re-arms it with that change's time. If the running capture also takes that record, the window stays armed with a stale start once nothing is dirty.

Probe (`receipts/probe_dr2a_rearm_1x1.txt`, harness-only phase word):

| Case | Result |
|---|---|
| change Y while the capture runs; change Z 5 s after the commit | Z's erase starts about 2 ms after Z (`erase_starts_us=[1008274, 6055259]`, `ok=2`) |
| control: Y made before the capture | Z still `dirty=1` 50 ms later |

The `debounce` check does not cover a change during a capture.

**Impact.** Extra commits and erases under bursty traffic, against the coalescing that DR2a rules.

**Required outcome.** The window starts at the first change that is still dirty, and a change consumed by the running capture leaves no armed start.

**Verification.** The probe's case shows Z's erase at 1,000 ms or more after Z, and a check plus mutant cover a change during capture.

### R500-1-F4: MINOR. Lenses: Conformance, Docs

**Artifact.** `nvm_state.h:28-30`, `nvm_store.c:177-218` and `host/nvm_smodel.c:157-167`. Title: bindings are restored inside the D3 transaction and rolled back by a D3 abort, contrary to section 8.6, with no record of the deviation.

**Authority and evidence.** MATERIALIZATION section 8.6 (lines 1274-1277): "the unit of atomicity for a transport failure is the walk ... A D3 roll-back leaves a completed binding walk applied: its owners are the two stores and the map plane, never the listener or the binding manager". Section 8.1 step 4 says a binding-walk failure fails that walk whole and does not abort D3.

In this store:
- the binding group goes through the same `apply` walk;
- a fault on any later record calls `rollback()`, specified as "every restorable value back to its image default";
- the state model resets the bindings with everything else;
- a binding `apply` fault aborts the whole restore to DEFAULTS.

Neither the README, the PR, nor HANDOFF section 8 states this as a reading.

**Impact.** An unrelated D3 fault (a name, a map or the settle step) leaves the listener unbound for that boot, although the authority keeps the restored bindings. Fast connect is lost while the slot still holds them.

**Required outcome.** One of:
- the bindings keep section 8.1 and 8.6 semantics: outside the D3 roll-back, and a binding failure fails only the binding walk; or
- the deviation is published for a decision and stated in the state-port contract.

**Verification.** A check with an apply fault after the binding group shows the bindings still applied, or the published decision is cited in `nvm_state.h` and the README.

### R500-1-F5: MINOR. Lens: Tests

**Artifact.** `test/nvm_checks.py`, `test/nvm_checks_write.py` and `test/nvm_mutants.py`. Title: the suite cannot fail for several defects in the claims it rests on.

**Evidence.** Reviewer-planted defects were each graded by all 26 checks on every port at 1x1. A positive control, the lane's own `no_verify` seam, is caught by 3 checks (`receipts/mutant_control_no_verify.txt`).

| Planted defect | Checks reddened |
|---|---|
| `verify_skips_last_stretch` | 0 of 26 |
| `blankcheck_first_stretch_only` | 0 of 26 |
| `tie_picks_b` (the stated tie rule inverted) | 0 of 26 |
| `time_not_held` | 0 of 26 |
| `program_refusal_ignored` | 0 of 26 |

The first of these matters most. With the last page program dropped, the planted store reports a verified commit (`ok=1`, authority to seq 6). The next boot refuses that slot (`vd_a=4`) and falls back to seq 5: the change is silently lost while the store reported success. The reviewed store correctly fails the attempt (`receipts/probe_verify_tail_1x1.txt`).

Also:
- the model's `read-fail` fault is never armed by any check;
- `nvm_flash_wait` is never called by the store or the suite;
- the tie rule (A wins) follows the shipping writer, while section 7's literal pseudo-code `newer = (int32_t)(A.seq - B.seq) > 0` would offer B. It is stated in a code comment and never exercised.

**Impact.** The PR's central claim that "the authority moves only after a verified read-back" is graded only for faults in the first page.

**Required outcome.** Checks that fail for:
- a read-back or blank check that skips any stretch, including the trailer;
- the tie rule;
- the time behaviour;
- a refused program;
- a read failure at boot and at verify.

Each needs a planted mutant.

**Verification.** Rerun `probe_mutants.py` for each defect above: every one is caught.

### R500-1-F6: MINOR. Lens: Docs

**Artifact.** `sw/firmware/ctrl_nvm/README.md:135-136`. Title: the service-bound sentence overstates the CPU bound.

**Evidence.**
- "No call holds the loop longer than one 256-byte transfer on the 1x link". One such transfer is about 0.17 ms in the model.
- The same paragraph derives about 1.2 ms for the longest step: 1,158 B × 1.05 µs/B, the capture receipt's 8x8 rate. The arithmetic checks out against `measurements.json`.
- The suite's `CALL_BOUND_US` measures model link time only, and CPU work costs no model time (`nvm_checks_write.py:204` says "of link time"; the README does not).
- The byte bound also leaves out the owner's `latch()` cost and the per-step record walk (`nvm_store.c:370-371`, `nvm_rec_next`).
- The derived figure itself is honestly labelled DERIVED in the README and PR, and its margin against 24.5 ms is wide.

**Impact.** A reader takes a link-time bound as a CPU-time guarantee that the derived figure contradicts.

**Required outcome.** The sentence states that the bound is model link time, and the derived CPU figure lists what it excludes.

**Verification.** Re-read README section "The service bound".

### R500-1-S1: SUGGESTION. Lens: Tests

**Artifact.** `.github/workflows/docs.yml:233` and `scripts/ci_events.py:1018`.

The sibling gate `nvm_hosttest/test_nvm_firmware.py --self-test` runs in hosted CI. `ctrl_nvm/test/test_ctrl_nvm.py` runs in none, although it imports shared parent scripts (`nvm_klj2.py`, `nvm_shape.py`, `nvm_contract.py`, `flash_map`, `test_nvm_firmware.parity_cases`) that can change under it.

**Suggestion.** Wire it in under the CI-events contract, or record a follow-up Issue and the open risk in the PR.

## Seam with F0

The seam is credible as stated, with one condition:
- the five-call media port has no dependency on F0's files;
- the store's service and change hooks fit F0's bounded event loop;
- `plat/nvm_shape_gen.h` takes the same generated constants the shipping image publishes.

F0's REVIEW READY names F1's time as coming from `NOW_MS`. Whichever time source the seam lands on must not inherit F1's hold-on-backward-step behaviour (F1 above).

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3, F4) | FASTCONNECT 6.1/6.2/7 against `nvm_klj2.c:261-380`, `nvm_store.c:113-285` and `probe_parity_fuzz_*`; MATERIALIZATION 6.2, 8.1, 8.4, 8.6 and 15.1 (DR2a, DR2b, DR2c, DR3b, DR5) against `nvm_store.c:289-609` and `nvm_state.h`; the lane F1 items 1 to 6 against the PR and README | R500-1 | `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e` |
| RTL | UNCLEAN (F1, F3) | the write-path state machine `nvm_store.h:40-52` and `nvm_store.c:539-592` (every phase, default and error path, `busy<0`, timeouts); widths and wraps (`uint16_t` offsets against the 65,536 bound, the u32 sequence wrap, the u64 time deltas); time base `nvm_flash_litespi.c:171-191`; LiteSPI access `nvm_flash_litespi.c:59-169` against `milan_baremetal.c:956-1013` | R500-1 | `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e` |
| Robustness | UNCLEAN (F1, F2) | malformed and truncated containers (parity fuzz, 3,500 cases, 0 mismatches); the power-cut sweep (gate, 3,126 cases); media hang, stuck, drop and flip; read flip at re-stage; rollback fault; unproven model; PHC steps (`probe_time_step`); repeated identical changes (`probe_dr2c`) | R500-1 | `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e` |
| Tests | UNCLEAN (F1, F2, F3, F5) | `test/*.py`, `test/nvm_test.c`, `host/*.c`; the gate with self-test (rc 0, 46 of 46); 7 reviewer mutants (`receipts/mutant_*`); the vector round trip against `tb/verilator/nvm_backend/records_*` (1x1 3,336 B 0x6FEA9AD3, 8x8 13,256 B 0x01F55611) | R500-1 | `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e` |
| Docs | UNCLEAN (F4, F6) | `sw/firmware/ctrl_nvm/README.md`, the header comments, the `docs/README.md` row, the PR body, the REVIEW READY comment, the public HANDOFF; docs gates rc 0 (`receipts/gate_docs_check`, `gate_em_dash`, `gate_gen_toc`, `gate_doc_paths`) | R500-1 | `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e` |

## Real limits

- **No RV32 execution.** The RV32 arm gives sizes only. The per-step CPU time is not measured, and I did not measure it either. My judgement of the 1.2 ms figure is arithmetic against the capture receipt.
- **LiteSPI reads bypass the read-fault model.** The LiteSPI port reads the model's array through the memory map, so read faults reach only the direct model port. This is stated by the suite.
- **Probe seams are harness-only.** The PHC probe and the DR2a probe add script words and a PHC offset to the scenario runner and the command-master model. The store, the codec and both ports compile byte-identical.
- **Physical calibration NOT RUN.** No real LiteSPI timing, no real power cut, no hardware. Field skips are not hardware proof.
- **F0 is not on dev.** The seam is judged from the published text of both lanes.
- **Not run (out of scope for this review):** full parent, PP, gPTP, Yosys and builder banks, Docker, act and the host CI runner.
- **Clone state after the probes:**
  - HEAD and tree are as above;
  - the index was force-refreshed with no differences;
  - all 32 changed blobs hash-match;
  - the four gitlinks match the tree;
  - no untracked or ignored files remain.

## Pending manager duties

- Hosted `rtl-full`, `docs` and `elaborate` at the exact head.
- `act` acceptance.
- The current-dev candidate merge build.
- Carrying the executor's out-of-scope shipping-writer VD_REC/VD_LEN parity finding to its own Issue.
- R501-1's independent verdict.
- After fixes, a new round at the new head covering every lens again.

R500-1 FINISHED
