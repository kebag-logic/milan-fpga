[R867] NEGATIVE - exact head 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2

R867-2: internal independent review, delta round 2 of PR #947 for #946 / #665. The delta is `66c6edf3..9f4f3de0`, five one-line commits. Tree `9bdd0b0644d75354b43767e8453db2dc3649ea8b`, source base `cb96336d`. This is a source review. It does not authorize a merge, it does not validate the current-dev merge candidate, and it is not hardware qualification.

**Verdict: NEGATIVE.** Two MINORs are open, and both are cheap to fix:
- F-1, Tests: the new refusal gate's kind and type tests are never exercised at an index that has a context.
- F-2, Docs: the PR body's race argument states a mechanism the code does not have.

The round-1 MAJOR (R868-1-F1) is fixed:
- By my own reading of the core, ACMP and the wrap, the fix is correct. I found no interleaving that breaks the invariant.
- Its new tests fail by name on round 1's platform.
- All 26 planted defects are caught when I run them again.

R867-1 F-1, F-2 and F-3 and both prior RESIDUEs are resolved. There is no BLOCKER and no MAJOR. There are three RESIDUEs and three SUGGESTIONs.

## Findings

### F-1 MINOR — Tests — `sw/firmware/ctrl/test/test_plat_sinks.cpp:680-714` (S5) against `sw/firmware/ctrl/plat/ctrl_plat.c:170` — the new refusal gate's kind and type tests are never exercised at an index that has a context

- **Authority / evidence:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect" and "Tests do not merely reproduce implementation assumptions".
  - S5 claims that "a change of another kind writes no context". It is the R867-1 F-2 resolution's test. S5 uses only the ENTITY's SET_NAME and STREAM_OUTPUT **0**'s SET_STREAM_FORMAT. Index 0 has no receive-monitor context, so any defect keyed on the descriptor index is invisible there.
  - S6 to S10 use only STREAM_INPUT changes, so they cannot tell the gate's kind or type tests apart either.
  - I planted two defects through the PR's own harness (`scripts/sinkprobe.py`). All 10 Sinks tests still pass under each (`receipts/plant-one-type-dropped.log`, `receipts/plant-one-kind-dropped.log`):
    - `bool one = kind == AECP_CHANGE_FORMAT && (type == STREAM_INPUT || type == 6u);` (a STREAM_OUTPUT taken for a STREAM_INPUT);
    - `bool one = type == STREAM_INPUT;` (the kind test dropped).
  - I added one reviewer test, `RvOutputAndNameAtAContextIndex` (`scripts/rvprobe-test.patch`):
    - STREAM_INPUT 7 is bound.
    - STREAM_OUTPUT 7's SET_STREAM_FORMAT then waits, is acknowledged, and must answer SUCCESS and write no context.
    - SET_NAME of the bound STREAM_INPUT 7 must answer SUCCESS and write no context.
  - It passes at the head (`receipts/rvprobe-head.log`, 11 of 11).
  - It fails on each plant by name:
    - type plant: "RV output n's SET_STREAM_FORMAT is taken while input n is bound" (`receipts/rvprobe-type-plant.log`);
    - kind plant: "RV SET_NAME of input n writes no context" (`receipts/rvprobe-kind-plant.log`).
  - fw_coverage's 100 % branch figure does not show this, because index 0 evaluates both sides of the `&&`.
- **Impact:** The shipped code is correct. But the suite would not catch a plausible regression in the gate. Such a regression answers a legitimate waiting STREAM_OUTPUT SET_STREAM_FORMAT with ENTITY_MISBEHAVING whenever the same-index STREAM_INPUT is bound. That is an over-refusal that IEEE 1722.1-2021 7.4.9 does not allow. It also writes contexts on changes that move none.
- **Required outcome:** A Sinks case exercises the wrap's kind and type discrimination at an index that has a context, for example output n and SET_NAME of input n, with input n bound. The two defects above, or equivalents, are in `sink_mutants.py`, each caught by name.
- **Verification:** Both plants are caught by their named test in the control campaign. Sinks still passes at 8x8/1if and 1x1/1if.

### F-2 MINOR — Docs — PR #947 body, "Why it is race-free", line 61 — the race argument states a mechanism the code does not have

- **Authority / evidence:** The PR body says: "Every change the core keeps writes its contexts in the change port, before the core answers it, with no mailbox access between the change and the write."
  - `ctrl_plat.c:209-210` forwards the change to the face first. The face's publication makes mailbox writes, an F_COMMIT and F_STATUS busy polls (`aecp_face.c` publish; `mbx_face_commit`). The contexts are written only after that. In the immediate path, `sinks.applied(ctx)` then reads F_STATUS once more before the write.
  - This order is deliberate and tested. The plant `sink-change-before-commit` (`sink_mutants.py:72`) writes before forwarding, and S2 catches it as "written after the change's acknowledged commit".
  - What the argument actually needs is that no ACMP input (no BIND_RX) is processed between the applied port's bound check and the write. That does hold: the firmware is single-threaded, and those mailbox accesses are the face's own.
  - R868-1-F1 required the documented race argument to be true. This is a false technical premise inside that argument, not wording only. I was unsure enough about calling it wording that, by the owner's rule, it is MINOR.
- **Impact:** A later reviewer or maintainer who relies on the stated mechanism would reason from a property the firmware does not have. For example, they might conclude that the mailbox watcher's per-access checks bracket the write, or that the face's commit could be moved after the write.
- **Required outcome:** The PR body states the property the code has. For example: "with no ACMP processing between the applied port's bound check and the write; the only mailbox accesses between are the face's own publication and status reads, so no stream can be published meanwhile". The text in `ctrl_plat.c:137-147` and `plat/README.md:83` is already accurate and needs no change.
- **Verification:** The PR body's sentence matches `ctrl_plat.c:205-213` and the `sink-change-before-commit` plant.

### RESIDUE-1 — Docs — `sw/litex/ctrl_memory.py:254` — a lane name in a new source comment

The new comment line reads `#: named debt owed to S14 (#665). The`, and S14 is a lane name. This is a new instance in the reviewed delta. Exact fix: `#: named debt owed to the hybrid XIP work (#665 decision D3). The`. The `Ledgered` owner strings at lines 277-296 are data, not comments, and they follow the existing entries, so they are not counted.

### RESIDUE-2 — Docs — PR #947 body, Known limitations, line 131 — the follow-up ticket now exists but is not named

Change "a ticket of its own is proposed" to "it is #950". #950 is open and states exactly this scope: input 0, CRF and STREAM_OUTPUTs, refused with the clause's status.

### RESIDUE-3 — Docs — PR #947 body, line 61

F-2's rewording covers this RESIDUE if the author takes it. It is listed so that the manager's checklist has the location.

### S-1 SUGGESTION — Conformance — the status of a refused waiting change

A waiting change refused because its input was bound during the wait is answered ENTITY_MISBEHAVING at 100 ms. The change is undone, and the response reports the values in force.

- IEEE 1722.1-2021 7.4.9 names STREAM_IS_RUNNING for a bound input. That status tells a controller more, and #950's "refuses with the clause's status" could carry it for these inputs too.
- This is not a defect of this PR. ENTITY_MISBEHAVING is the core's documented timeout answer (`aecp.h`, `applied`). The response stays within the 9.3.2.6 bound. Changing the status is a core change that moves every CPU-budget image.
- The author's open point scopes this correctly.

### S-2 SUGGESTION — Robustness — `ctrl_plat.c:170` and `ctrl_plat_csr.c:93-104` — the `AAF_SUBTYPE` gate on the changed value

`ctrl_plat_csr_sink_context` decides which descriptor has a context from the first byte of its current format. The bound check runs on the undone (old) value, and the write runs on the done (new) value. So on an input whose format list mixes AAF and non-AAF formats, a change to a non-AAF format would leave the old AAF format in its context.

This cannot happen today: every shipped shape's AAF inputs advertise AAF formats only (`avdecc/aem_descriptors.py:133`, `FORMATS`). A builder rule or an assertion would keep it that way.

### S-3 SUGGESTION — Docs — `tb/verilator/ctrl_split_boot/README.md:137` — pre-existing stale figures

The line says "At this branch's head each boot reaches ready, at 26.370 ms (1x1, one interface), 66.017 ms (8x8, one) and 68.371 ms (8x8, two)". The lane's boot receipt at `9f4f3de0` gives 65.775 ms at 8x8/1if. This line predates the PR and the delta does not touch it, so it is not counted. It is #746-class upkeep.

## Prior findings, at this head

| Finding | My reading at `9f4f3de0` | Status |
|---|---|---|
| R868-1-F1 MAJOR: a BIND_RX settles while a SET_STREAM_FORMAT waits, and the change is done again onto the bound input | **The wrap:** `sink_applied` (`ctrl_plat.c:193-200`) answers false while `core->waiting` and the noted change moves a context whose ACMP sink is `bound`. **When `bound` is set:** at BIND_RX (`acmp.c:903`) and at restore (`acmp.c:1370`), before any probe. The stream_id is published only once settled (`acmp.c:221-237`), so `bound` is the earlier, conservative signal. **The core:** it calls the applied port during a wait only in `aecp_poll`'s waiting block (`aecp.c:906-918`). Its other three calls short-circuit on `waiting` or cannot be reached while waiting. `asynchronous()` is not reached while waiting, so `noted` cannot be overwritten. **Taken:** the core swaps and calls `aecp_note` → `sink_changed` with no port between, and the contexts are written before the held response is released. **Not taken:** the core answers ENTITY_MISBEHAVING at `AECP_WAIT_MS`, with the values in force. Any write on that path carries the value in force, and an LCTX RAM write has no side effect (`KL_avtp_rx_monitor_ctx.sv:719-723`). **Interleavings:** I found none that publishes a nonzero SID with context ≠ current format. I checked acknowledgement before or after the bind, an unanswered probe, the timeout, unbind before the acknowledgement, rebind and SET_CONFIGURATION. **Scope:** no mailbox, face, core, ACMP or RTL source changes. **Round 1's `ctrl_plat.c`:** S6 fails by name with "input 7: current 0205022000806000, context 0205022002006000", and S4, S5, S7 and S10 fail too (`receipts/sinks-r1-platform.log`). **Docs:** the race argument in `ctrl_plat.c`, `plat/README.md` and the PR body is true, apart from F-2's mechanism sentence. | **Resolved** |
| R868-1-R1 RESIDUE: lane names in new comments | `sim_ctxfmt.cpp:5` and the flash-model wording are fixed in `85363367`. | Resolved; one new instance is RESIDUE-1 |
| R867-1 F-1 MINOR: ROM ledger not raised | **Ledger:** `ctrl_memory.LEDGERED` holds `platform-8x8-two-interfaces` at 61.0 and a new `platform-8x8-one-interface` at 56.5, with symbols 13,594 / 18,240 B. Both cite the owner's rule of 2026-11-15 (#665 issuecomment-6892332745, which I read: "An image past its entry raises the entry to its measured size, at the next half tile, as named debt owed to S14"). **Links:** `boot_soc.PLATFORM_LEDGERED` and `plat_ledger.POINTS` take both entries, with a new control `product-override-not-taken`. **Tests:** `test_ctrl_memory.py` at the head has 0 failures (`receipts/test_ctrl_memory-head.log`). **Figures:** the author's `plat_ledger` receipt gives rom 131,656 / 133,224 B, equal to the figures in the README and SPLIT_CONTROL_MEMORY sections 3 and 5. The controls pass 8 of 8 on the lane and 9 of 9 on the composition. **Train:** the train's raise to 63.0 is a composition step (`merge/composition-ledger-raise.patch`). | **Resolved** |
| R867-1 F-2 MINOR: the poll's owed-flag clearing untested | The poll is removed, so no platform code runs on each pass. S5 runs 100 passes with the clock moved 2 s, and nothing is written. The plant `sink-every-pass-rewrites` is caught when I run it again. The kind/type gap is in new code and is F-1. | **Resolved** |
| R867-1 F-3 MINOR: follow-up tickets | #948 and #949 are open and named in the PR body. #950, the core's unchecked redo for input 0, CRF and outputs, is also open. | **Resolved**; RESIDUE-2 asks the PR body to name #950 |
| R867-1 R-1 RESIDUE: `sim_ctxfmt.cpp:5` | Fixed. | Resolved |

## The author's open points (item 5)

- **ENTITY_MISBEHAVING rather than STREAM_IS_RUNNING:** correctly scoped. It is the core's documented answer, it is bounded, and the response carries the values in force. See S-1 and #950.
- **The datapath's face copy during the 100 ms wait:** correctly scoped.
  - The face committed the change before the core undid it. The same exposure exists on the base, where the change was then kept for good.
  - W ends the exposure at the wait's bound. It affects `F_FMT_IN` and the map's channel clip, not the monitor's judgement. Known limitations states it.
- **Input 0, CRF and outputs keep the core's unchecked redo:** this is base behaviour, not introduced here, and outside #946's receive-context scope. It is ticketed as #950.

## Gates (item 6)

These come from the author's published receipts unless marked as mine.

- **Firmware gate** at `548324b5`: PASS, every suite with 0 failures, Sinks 10/10 at both shapes (`gates/lane-548324b5-firmware-gate.txt`). The diff confirms that `548324b5..9f4f3de0` changes only one docstring, in `ctrl_memory_ledger.py`.
  - **Mine:** Sinks at the head, 10/10 at both shapes (`receipts/sinks-head.log`).
  - **Mine:** the sink table run again, 26 of 26 caught (`receipts/sink-table-{1,2}of2.log`).
  - **Mine:** seven extra plants (`receipts/sink-extra.log`):
    - Caught: a redo flag set outside a wait, the immediate write removed, the bound check on the settled stream, and refusing every wait.
    - Escaped, but equivalent and harmless:
      - the redo flag never cleared, because every next applied call resets it;
      - the bound check on `published_bound`, because ACMP sets it in the same call as `bound`.
    - Escaped for real: the any-kind gate, which became F-1.
- **fw_coverage:** PASS, the changed files at 100 % after exclusions (author receipt). F-1 shows what branch coverage cannot see here.
- **Twin:**
  - The lane's captures are byte-identical to `cb96336d`'s: the split, fabric and report sha256 are equal.
  - The lane and the base each have the one owed row `split-talker-failed` and the same plant results: `byte-flip` refused and `srp-plus-k` escaping. So the lane's one escape equals the base's.
  - The composition has 0 findings and every plant refused.
- **Boot:** the lane at `9f4f3de0`, 8x8/1if with the override `platform-8x8-one-interface`, is ready at 65.775 ms. The composition is ready at 67.328 ms at 8x8 and at 27.936 ms at 1x1. All are within the 20 s bound.
- **CPU-budget images:** hash-equal to the train's recorded ones (1x1 `55484254e638ed7f`, 8x8/1if `175418f4b5b1a9d4`). Their sources do not change.
- **Release image:** by reading, the delta changes no all-fabric input. It touches the split platform, its tests, the ledger's LEDGERED entries and a test-bench comment. As in round 1, no release artifact hash was produced.
- **RTL:** the delta changes no HDL, and `sim_ctxfmt.cpp` changes in one comment line only. The avtp_rxmon suite receipt at `0f6c12ba` passes, CTXFMT 96/96 including [CF4]. The suite's inputs do not change after `0f6c12ba`.
- **Sweep and docs:**
  - The composition sweep runs 65 of 65 suites, with 0 in-suite failures and 4 declared external-generator skips.
  - The docs steps on the lane pass every step that dev-soft-core has.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat.c:131-213` against IEEE 1722.1-2021 7.4.9 (STREAM_IS_RUNNING on a bound input), 7.4.16 and 9.3.2.6, and Milan v1.2 Table 5.6 / 4.4.2.2; `aecp.c:445-520,895-934`; `aecp_commands.c:88-140`; `acmp.c:221-237,895-935,1360-1375`; S6-S10 outcomes; the scopes of #948, #949 and #950; owner's rule 6892332745 | R867-2 | `9f4f3de03f99dc8c7a72f5f8884f00df82c965d2` |
| RTL | CLEAN | No HDL in the delta. `KL_avtp_rx_monitor_ctx.sv:700-740`: the window write is a plain RAM write with no side effect, and a same-value rewrite cannot tear the PDU's FMT_LO/FMT_HI reads in M_PFRD2/3. `ctrl_plat_csr.c:70-104` is unchanged. The avtp_rxmon receipt is at `0f6c12ba`. | R867-2 | `9f4f3de03f99dc8c7a72f5f8884f00df82c965d2` |
| Robustness | CLEAN | Interleavings: acknowledgement before or after the bind, unanswered probe, timeout, unbind before the acknowledgement, rebind, SET_CONFIGURATION, lock expiry against a wait. A re-entrant change port (`sinks.redo` is captured before forwarding). The boot's open order (`ctrl_plat.c:342-377`). The refused path's same-value rewrite. S-2 is a latent case that no shipped shape reaches. | R867-2 | `9f4f3de03f99dc8c7a72f5f8884f00df82c965d2` |
| Tests | **UNCLEAN** (F-1) | `test_plat_sinks.cpp` S1-S10 and the Coherence watcher; `sink_mutants.py`, all 26 run again; seven extra plants; two escaping gate plants; the reviewer test `RvOutputAndNameAtAContextIndex`; round 1's platform failing by name; `test_ctrl_memory.py` at the head | R867-2 | `9f4f3de03f99dc8c7a72f5f8884f00df82c965d2` |
| Docs | **UNCLEAN** (F-2) | The `ctrl_plat.c:129-147` comment; `plat/README.md:78-84,118-145`; `SPLIT_CONTROL_MEMORY.md` sections 3 and 5 against `ctrl_memory.LEDGERED` and the plat_ledger POINT figures; `ctrl_split_boot/README.md:136-143`; PR body lines 51-73 and 112-140; the RESOLUTIONS table in HANDOFF-r2 | R867-2 | `9f4f3de03f99dc8c7a72f5f8884f00df82c965d2` |

## Real limits

- **Not run by me:** the full firmware gate (`--self-test`), fw_coverage, plat_ledger, the twin, the sweep, the boot simulation and the CPU-budget run.
  - Those figures are the author's published receipts.
  - I spot-checked them: the twin's lane-to-base hashes, the ledger's POINT lines and controls, the budget hashes, the boot's ready line and the RTL suite's lines.
- **Run by me:**
  - the Sinks suite at both shapes;
  - the sink plant table (26);
  - nine reviewer plants;
  - one reviewer test;
  - round 1's platform against round 2's tests;
  - `test_ctrl_memory.py`.
- **Verilator:** not run, because the delta has no HDL and the RTL receipt's inputs are unchanged.
- **Hosted CI:** not inspected.
- **Hardware:** physical calibration NOT RUN. The bench's stream, power-cycle and soak items at 8x8/1if were not run, and no hardware was used.
- **Clone state:** after the probes I confirmed that the clone equals the exact head (`receipts/clone-restore-check.txt`):
  - the worktree and the index equal HEAD, and the index tree is `9bdd0b06…`;
  - every submodule gitlink is equal, and every submodule is clean.
  - Before that check I removed one stray untracked directory, left by a failed first campaign launch with relative paths.

## Pending manager duties

- Validate the current-dev merge candidate (source base `cb96336d`, live dev `e275d795`) with the builder and native banks.
- Accept the hosted and act results for the exact head.
- Apply the composition step's ledger raise, the train's `platform-8x8-two-interfaces` from 62.5 to 63.0 (`merge/composition-ledger-raise.patch`). The step-12 composition must take the train's side of the ledger.
- On dev-soft-core alone, an 8x8/1if **product** SoC build is still held to 56 and would be refused at 56.5 (PR body, ROM). So the bench's 8x8/1if items need the train image.
- Run the bench's stream, power-cycle and soak items at 8x8/1if, which are #946's acceptance, before #946 closes.
- Carry RESIDUE-1 to RESIDUE-3 to the residue checklist.

R867-2 FINISHED
