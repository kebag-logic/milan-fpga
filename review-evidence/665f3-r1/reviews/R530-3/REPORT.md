[R530] NEGATIVE - exact head abb3a78a12c29ff13ee7f71a00b387a6c91dc361

# R530-3: internal cleared-context review of PR #688 (issue #665, lane F3, round 4)

- **Head:** `abb3a78a12c29ff13ee7f71a00b387a6c91dc361`, tree `d85f5361950dbf3f8deff0d45f4cb4fe7ff1e7fd`. This is the published `665-f3-acmp` and the PR head, not a draft.
- **Delta reviewed:** `4f6216ab..abb3a78a`. That is the `--no-ff` merge `72597d22` of dev `d51b373a` (FC #685, #679, #677), plus nine commits. The full `021b9c1f..abb3a78a` range was read for context.
- **Assignment:** #665 comment 6034423349.
- **Verdict:** NEGATIVE, on one open MINOR (R530-3-F1). The round's MAJOR (R531-2-F1) is resolved at its root. So are R530-2-F1 and F3, and the three round-2 RESIDUE items. The linked image (R531-2-F2, R530-2-F2) is now reported, and it is a real link. However, the documented command refuses on the pinned RV32 SDK. The figures reproduce only on an unpinned local toolchain, and the docs attribute them to the pinned SDK.

## Findings

### R530-3-F1 | MINOR | Conformance, Tests, Docs | the linked-image measurement cannot be reproduced with the pinned SDK, and its toolchain is misattributed

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_image.py:70-71` and `:178-179`: it links `-march=rv32i -mabi=ilp32 ... -lgcc`.
  - `sw/firmware/ctrl/README.md:246`: "At lane F3 round 4, with the pinned SDK's GCC 14.3.0".
  - PR #688 body, line 54 ("the pinned SDK's GCC 14.3.0") and lines 177-179 ("every command exits 0 ... `ctrl_image.py` prints the table above").
  - `review-evidence/665f3-r1/author-r4/HANDOFF.md:133`: "Compiler: the pinned SDK's `riscv32-linux-gcc` (Buildroot 2026.05, GCC 14.3.0)".
- **Authority/evidence:**
  - **Acceptance.** Addition 6030870481 requires the linked image. R531-2-F2's verification requires "independently reproduce the link".
  - **The pin.** `scripts/ci_rv32_sdk.py` (the SDK every RV32 gate uses, `ARCHIVE_SHA256 d42680e9...`) pins the Bootlin `riscv32-ilp32d--glibc--stable-2025.08-1` archive. I extracted that exact archive (hash verified).
  - **The refusal.** With `MILAN_RV32_CC` pointing at it, `ctrl_image.py --base d51b373a...` exits 2: "can't link double-float modules with soft-float modules" (`receipts/ctrl-image.log`, `ctrl-image.rc` = 2).
  - **Why.** The pinned SDK has one multilib, and its `libgcc.a` is double-float ABI (ELF flags 0x4). The composition's objects need libgcc helpers (`__lshrdi3` in `adp.o` and `acmp.o`; `__udivdi3`, `__umoddi3` and `__muldi3` in the LiteSPI port; `__udivsi3`, `__umodsi3` and `__mulsi3` in the pool). So the base cannot link with the pinned SDK either (`receipts/rv32-toolchain-identity.txt`).
  - **Where the figures come from.** The published figures reproduce exactly, every section, total and object at both shapes plus the base deltas (`receipts/ctrl-image-local-toolchain.log`), with a different compiler: `$HOME/br-milan-rv32/host`, "Buildroot 2026.05" GCC 14.3.0, with a soft-float `libgcc` (sha256 `faef00ac...`). `fw_rv32.CANDIDATES[0]` picks it first when `MILAN_RV32_CC` is unset.
  - **Why nothing catches it.** That path is where CI installs the pinned SDK, but on the measuring host it holds a different build. The pinned archive's compiler reports "Buildroot 2021.11-18033-g83947c7bb6". No gate or workflow runs `ctrl_image.py` (`git grep`, same receipt), so nothing catches the refusal.
- **Impact:**
  - The acceptance evidence is a real link. But a cold reviewer, the manager or CI following the PR's "How to get into the same state" (the CI RV32 SDK) gets REFUSED, not the table.
  - The README, PR body and handoff state a provenance that is false.
  - The figures (32.1 % and 40.0 % of 128 KB) are correct for the toolchain that made them. The libgcc helpers in them are 2,704 bytes of text and 256 bytes of rodata at the shipping shape (from the link map). So no budget conclusion changes, which is why this is MINOR, not MAJOR.
  - It is not RESIDUE, because it concerns a measurement's reproducibility and provenance and a tool's behaviour.
- **Required outcome:** the documented command and the documented toolchain agree. Either:
  - `ctrl_image.py` links with the pinned SDK (for example, by supplying the soft-float arithmetic helpers the composition needs and reporting them apart like the C-runtime stand-ins), and the published figures are regenerated with it; or
  - the README, PR body and handoff name the toolchain actually used, with its identity (version string and libgcc hash), and state that the pinned SDK cannot link the image. The manager then records a public disposition for the acceptance item.

  Either way, whatever toolchain is named must reproduce the published table.
- **Verification:** with a fresh extraction of the pinned archive, and `MILAN_RV32_CC` set to it, `python3 sw/firmware/ctrl/test/ctrl_image.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` exits 0 and prints the published table. Otherwise the docs' named toolchain prints it, and no text claims the pinned SDK.

### R530-3-R1 | RESIDUE | Docs | the PR title still says "stacked on #685"

- **Where:** PR #688 title: "Mark II F3: bare-metal ACMP core on the mailbox (stacked on #685)".
- **Evidence:** #685 is merged into dev `d51b373a`, which this head merges. The PR's base is `dev`, and its body says "the diff against `dev` is lane F3's alone". The title is wording only.
- **Exact fix:** retitle to "Mark II F3: bare-metal ACMP core on the mailbox".

No other finding.

## Prior public review findings at this head (read after my own pass)

I read R530-2's and R531-2's reports (evidence branch commit `48786159`, `reviews/R530-2/REPORT.md` and `reviews/R531-2/REPORT.md`) after my independent pass. I extracted R531-2's `independent_timers.cpp` and its runner beforehand, as the assignment required, without reading the report.

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R531-2-F1 MAJOR, TMR_NO_RESP from the clock after the accepted send | RESOLVED | See the note below the table. |
| R531-2-F2 MINOR, linked image absent | RESOLVED as to the report. Reproducibility on the pinned SDK is RETAINED as R530-3-F1 | Both shapes, with the base delta. Sections, totals and static objects reconcile with the ELF's section headers and symbol table (`ctrl-image-local-toolchain.log`). It is a real `_start` -> `main` link at `--gc-sections` into `image.ld`'s 128 KB region; stubs and stand-ins are disclosed. |
| R530-2-F1 MINOR, two interface mix-ups escape | RESOLVED | See the note below the table. |
| R530-2-F2 MINOR, linked image not reported | RESOLVED as to the report. RETAINED as R530-3-F1 for reproducibility | As for R531-2-F2. |
| R530-2-F3 MINOR, stale 0.92 us | RESOLVED | `MAILBOX_SPLIT.md:925-927` gives 0.89 us and 0.44 us, "the table's access times for T_svc", and they equal `:666-667`. I recomputed every row: 3,036, 11,132, 22,264 and 9,108 are 3, 11, 22 and 9 x 1,012, and each access time is 10 ms (or 20 ms) over the bound, rounded down as stated. |
| R530-2-R1, R2, R3 RESIDUE | RESOLVED | The exact texts are in `MAILBOX_SPLIT.md` (open item, contents line) and in the PR body (Status, Known limitations). |
| R530-2 S1 to S3 SUGGESTION | Unchanged; S2 declined by the assignment | No lens effect. |
| R531-1-F1 to F5, R530-1-F1 to F5, R1 | Still RESOLVED | Their planted defects are in the 354-defect table, all caught at this head, and their tests pass (A24, A26 to A29, B7, N7, `acmpif2` 19 of 19). R531-1-F2's immediate-send remainder is closed by R531-2-F1 above. |

**R531-2-F1 evidence.**

- **The fix** (`acmp.c:659-712`).
  - `no_resp_from_send` invalidates the entry's cached clock and arms TMR_NO_RESP from a fresh read. Both the immediate path (`send_probe`, `SENT`) and the owed path (`probe_left`) use it.
  - The owed path holds the timer with no deadline.
  - LOST keeps its from-the-attempt timer and counts the loss.
- **Expiry** (`acmp.c:1090-1114`): expiry tests deadlines at the latest read.
- **R531-2's four tests:** 4 of 4 at the head (`r531-timers-head.log`). At `4f6216ab`, the two immediate-send tests fail (`r531-timers-4f6216ab.log`).
- **My seven moving-clock probes** (`scripts/r530_timer_probes.cpp`) pass at the head (`r530-timer-probes-head.log`). They cover:
  - an owed duplicate settling at 199 ms and timing out only at 200 ms;
  - two duplicates in one expiry, each from its own send;
  - the 32-bit wrap inside a send;
  - the lost-probe policy;
  - a re-bind while owed;
  - an unbind while owed.

  With the head's tests and the pre-fix `acmp.c`, exactly the immediate-send probes fail, 2 of 7 (`r530-timer-probes-prefix-acmp.log`). The five kept behaviours pass on both.
- **My six planted defects** (`r530-mutation-probes.log`) are all caught by named A1, A10, A23, A27, A28 or A30 tests. One expected-equivalent defect survives: a lost probe re-reading the clock, where no send happened.
- **Kept behaviour and campaigns.**
  - FIFO order, the sequence ID and the single duplicate are kept: A30 asserts the exact copy and the sequence_id. My two-sink probe checks the per-sink sequence IDs.
  - The ctrl campaign is 354 of 354, including A30's three new defects and the 12 re-planted ones.
- **Access cost.** It is +1 `NOW_MS` per probe sent at once. That gives 35 (C5), a pass of 1,012 (996 + 16) and the four backlog bounds above.
  - BIND reads the clock only after its probe (`acmp.c:776-807`), so 51 and 76 stand.
  - The C-path tests pass. The planted extra-clock-read defects are caught.

**R530-2-F1 evidence.**

- **New checks.** Q22 and Q23 are in `suite.hpp:1562-1613`, run by `run_bound_timing`. The suite grows from 380 to 382 checks at one interface and to 384 at two interfaces.
- **Planted defects.** The full `mutants.py` run (four controls) catches 147 of 147 (`mbx-mutants-full.log`). Among them:
  - `rx-bound-verdict-of-the-presented-interface` (one interface, two interfaces, both adapters) fails Q22 by name;
  - `rx-bound-live-reads-interface-0-owed` (two interfaces, both adapters) fails Q23 by name.
- **My own interface mix-ups** (`r530-mbx-mutants.log`, `r530-mbx-mutants-if1.log`). These are caught:
  - liveness reading interface 0's `BOUND_EN` (Q13);
  - comparing interface 0's identities (Q13);
  - the host's entry index ignoring the interface (R1);
  - an index with no table not refused, at one interface (Q13);
  - the X13 form through AXI4-Lite at two interfaces (Q22).

  Two survivors are equivalent, not gaps:
  - `if_r` latched on every accepted byte: `rx_if_i` is held for the frame, and `if_r` changes only on `take_w`, `KL_mbx_rx.sv:529-530`;
  - the no-table refusal removed at two interfaces: the 1-bit index has no out-of-range value there.

## What each lens examined

### Conformance

- **TMR_NO_RESP.** I checked it against Milan v1.2 5.5.3.5.3 steps 5-7 and 5.5.3.5.16 steps 1-2, as cited by the assignment, the code and the round-2 ruling: the timer starts once the probe is sent, for the initial probe and for its exact duplicate. A response at 199 ms is accepted, and the timeout comes only at the full interval (R531-2's tests and mine).
- **Ordering.** Response-before-notification ordering is unchanged; the owed-FIFO tests pass.
- **Acceptance (assignment 6034423349).**
  - Items 1, 2, 3 and 5 are met.
  - Item 4 (6030870481) is reported, but not reproducibly on the pinned SDK (F1).
- **Scope and defaults.**
  - Scope holds: `git diff 4f6216ab HEAD -- hdl sw/litex configs sw/builder constraints syn` is empty.
  - The default build is unchanged in this round.
  - The submodule gitlinks equal dev's.

**Unclean (F1).**

### RTL

- **No RTL in this round.** The mailbox RTL is byte-identical to round 3 (the `hdl` diff is empty), so +357 LUT / +86 FF stands.
- **Bound term's interface indexing** (`KL_mbx_rx.sv:235`, `:302-310`, `:460`, `:529-530`). Probed with eight reviewer defects at one and two interfaces (above).
- **Firmware timer arithmetic.**
  - `due()` uses a signed 32-bit difference (`acmp.c:300-303`); deadlines are `now + 200` modulo 2^32 (wrap probe P3).
  - After a send, the cached clock is invalidated, which bounds the expiry loop: a probe's deadline lies 200 ms past the read used for the due test.
- **Past deadlines.** A deadline re-armed after the clock moved mid-loop may already be past. Both the RTL (`KL_mbx_evt.sv:10-12`, "an armed slot whose deadline has passed") and the model (`mbx_model.c:147`, signed `>= 0`) expire it at once, so there is no wedge.
- **Resources.** The block-RAM effect of the composition was reproduced at 42,100 and 52,472 bytes of 131,072, measured off-pin (see F1).

**Clean.**

### Robustness

- **Timer paths.** Owed, lost, re-bound, unbound, duplicate-owed and wrap paths, with a clock that moves inside each send (my P1 to P6; R531-2's queued control).
- **Re-entry.** The #678 guard: both `reentry_*` arms pass, 122 tests each. A23 catches the owed-path timer-kind defect.
- **Interfaces.** Out-of-range and no-table indices refused (Q13). Back-to-back frames on different indices (Q22). Copy-owed gating per interface (Q23).
- **Configuration.** Feature-disabled and configuration-dependent behaviour: `acmpif2` 19 of 19, and `run-if2` on both adapters plus the model.

**Clean.**

### Tests

- **Gates.**
  - The ctrl gate passes with `--require-rv32` (pinned SDK): 13 arms, `acmp` 81, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 19, `reentry_*` 122 each.
  - The campaign catches 354 of 354 (12 slices, no ESCAPED line and no unnamed test).
  - Coverage: `--check` holds 17 files at 100 % after exclusions (`acmp.c` 734/734 lines, 342/342 branches); `--selftest` 28 of 28.
- **Mailbox suite** (`make all`): 382 and 427 checks; 384 and 429 at two interfaces; the model 369; co-simulation 32; 5 of 5 quick arms. `mutants.py` catches 147 of 147 with four controls.
- **Store and RTL gates.**
  - `test_ctrl_nvm.py --require-rv32`: 435 tests, 5 shapes.
  - `test_nvm_firmware.py --self-test`: OK.
  - `lint_rtl.py --check --self-test`: 90 <= 90.
  - `gen_mailbox.py --check --crosscheck` and `--selftest`.
- **Sensitivity.**
  - A30 fails on the pre-fix behaviour: the campaign's three new defects, plus my six.
  - Q22 and Q23 fail on X13 and X17.
- **Merge.**
  - `git merge-tree` of `4f6216ab` and `d51b373a` reproduces exactly the six conflicted files, and `72597d22` differs from the mechanical merge only in those files (`merge-tree-recompute.txt`, `merge-resolution-vs-markers.diff`).
  - Each resolution keeps both sides: #677's `reentry_*` arms, `--jobs` and `assert.h`; F3's ACMP arms, `--slice`, `unnamed_tests` and the `acmp*` ratchet rows; dev's `adp.c` ratchet row 204/204.
  - The re-graded counts are true: 13 arms, and 15 exclusion rows, which I counted in the table.

**Unclean (F1):** the image tool is run by no gate and refuses on the pinned SDK.

### Docs

- **Checked against source and receipts:**
  - `MAILBOX_SPLIT.md:546-549`, `:638`, `:648-654`, `:665-679`, `:723-728` and `:922-930`;
  - `acmp.c`, `acmp.h:41-44` and `acmp_mbx.h:44-57`, `:63-144` header comments;
  - `sw/firmware/ctrl/README.md` (contents, ACMP module, host test with 254 F3 defects counted from the table, Linked size), `sw/firmware/gtest/README.md` and `tb/verilator/mbx/README.md` (Q22/Q23 rows, the planted-defect table, "Q18 to Q23 are the RTL's alone": 382 - 369 = 13 and 384 - 369 = 15);
  - the PR body and title, and the author-r4 handoff.
- **Docs-workflow gates pass.** `docs-gates.log` has 35 commands. 31 pass under the plain interpreter, among them `docs_check.py`, the idiom checks, `ci_events.py --check`, `fw_rv32_selftest.py --require-rv32` and `tally_selftest.py`. The four renderer commands pass under the pinned renderer (`docs-gates-md-venv.log`): `check_em_dash.py --base d51b373a` and `--base 021b9c1f`, and `gen_toc.py --check`, `--verify-anchors` and `--selftest`.

**Unclean (F1):** the README, PR body and handoff name the pinned SDK for figures it cannot produce. R530-3-R1 is RESIDUE.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R530-3-F1) | `acmp.c:659-712`, `:776-807`, `:1090-1114`, `:1159-1177` against Milan v1.2 5.5.3.5.3 steps 5-7 and 5.5.3.5.16 steps 1-2; assignment 6034423349 items 1-5; #665 6030870481; scope diffs | R530-3 applied; not clean | `abb3a78a12c29ff13ee7f71a00b387a6c91dc361` |
| RTL | CLEAN | empty `hdl` diff `4f6216ab..HEAD`; `KL_mbx_rx.sv:235`, `:302-310`, `:460`, `:529-530` under eight reviewer defects; `acmp.c:110-119`, `:300-310`, `:661-665`; `KL_mbx_evt.sv:10-12`; `mbx_model.c:147`; `acmp_mbx.h:119-144` | R530-3 | `abb3a78a12c29ff13ee7f71a00b387a6c91dc361` |
| Robustness | CLEAN | `scripts/r530_timer_probes.cpp` P1-P6; `r531-timers-*.log`; `reentry_*` arms; Q13, Q22 and Q23 at one and two interfaces; `acmpif2` | R530-3 | `abb3a78a12c29ff13ee7f71a00b387a6c91dc361` |
| Tests | UNCLEAN (R530-3-F1) | `test_acmp.cpp:1788-1876`; `acmp_review_mutants.py:70-100`; `suite.hpp:1562-1613`; `mutants.py:375-388`; `ctrl_image.py`; every `camp-slice-*.log`; `mbx-mutants-full.log`; `mbx-make-all.log`; coverage, store and lint receipts; `merge-*` receipts | R530-3 applied; not clean | `abb3a78a12c29ff13ee7f71a00b387a6c91dc361` |
| Docs | UNCLEAN (R530-3-F1) | `MAILBOX_SPLIT.md:546-549`, `:638-679`, `:723-728`, `:922-930`; `sw/firmware/ctrl/README.md:24-28`, `:70-73`, `:165-190`, `:225-261`; `gtest/README.md:164-170`, `:228-235`, `:360-363`; `mbx/README.md:73-104`, `:250-258`; PR #688 body and title; `author-r4/HANDOFF.md:128-136`; docs-gate receipts | R530-3 applied; not clean | `abb3a78a12c29ff13ee7f71a00b387a6c91dc361` |

## Real limits

- **Clause text.** No copy of Milan v1.2 or IEEE 1722.1 is in the repository. I checked the TMR_NO_RESP clauses by the numbers and wording the assignment, the code and the round-2 ruling cite, not against the standard's text.
- **Image toolchain.** The linked image was reproduced only with the unpinned local toolchain, because the pinned SDK refuses it (F1).
- **Markdown renderer.** `check_em_dash.py` and `gen_toc.py` ran with a pre-existing virtual environment. Its name equals the first 12 hex digits of the sha256 of `tools/markdown/requirements.txt`, and its renderer packages match the pins. The plain-interpreter run of those four commands refused for the missing renderer only (`docs-gates.log`, rc 4).
- **Not run, by assignment:**
  - out-of-context area and Vivado, `xvlog_gate.py` and Yosys (no RTL changed in this round);
  - the builder bank and the parent, PP and gPTP banks;
  - `act` and `act_ci`.

  Also not run: the `lwsrp` arm (no lwSRP checkout).
- **Hosted evidence** at inspection (`hosted-check-runs.txt`):
  - executed and successful: `rtl-fast`, `firmware-unit`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `changes`, Yosys shards 0 to 3, and Verilator shards 0 and 3;
  - still in progress: Verilator shards 1, 2 and 4;
  - not yet reported: the `verilator-suites` and `yosys-portability` aggregates;
  - skipped: physical gPTP (nightly and manual).

  None of the hosted jobs runs `ctrl_image.py`.
- **No hardware.** Physical calibration was NOT RUN. The access time (A4) is unmeasured, so the backlog bounds remain conditional on 0.89 us (acmp ring) and 0.44 us (adp ring) per access or less. Field skips are not hardware proof.

## Pending manager duties

- Rule on R530-3-F1, and carry R530-3-R1 to the residue checklist.
- Build and gate the candidate merge against live dev. The head descends directly from `d51b373a`, so if dev has not moved, the candidate tree is this head's tree `d85f5361`.
- Own hosted acceptance (the remaining Verilator shards and both aggregates) and `act`.
- Obtain the external review. An executor's verdict counts for neither positive.
- Physical calibration and the A4 access-time measurement belong to the F2 to F5 bench pass.
- This verdict carries no merge authorization.

## Reproduction

These commands were run from the clone at the head. `$PACKET` is this directory. Every script is under `scripts/` and every log, with its rc, is under `receipts/`.

- **Gate and campaign.**
  - `MILAN_RV32_CC=<pinned SDK>/bin/riscv32-linux-gcc python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 [--self-test --slice K/12 --jobs 1]`.
  - `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` and `--selftest`.
- **Image.** `python3 sw/firmware/ctrl/test/ctrl_image.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`, run with the pinned SDK (refuses) and with `MILAN_RV32_CC=$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc` (reproduces). The identities are in `rv32-toolchain-identity.txt`.
- **Timer probes.**
  - `scripts/run_r530_probes.py <tree> <work> scripts/r530_timer_probes.cpp r530-probes`, at the head, at `4f6216ab`, and on the head with `4f6216ab`'s `acmp.c`.
  - R531-2's runner, copied verbatim as `scripts/r531_2_run_timer_probes.py <tree> <dir>`, with `<dir>/scripts/independent_timers.cpp` being `scripts/r531_2_independent_timers.cpp`.
- **Planted defects.** `scripts/r530_mutation_probes.py <tree> <work>`; `scripts/r530_mbx_mutants.py <tree> <work>` and `scripts/r530_mbx_mutants_if1.py <tree> <work>`, with `VERILATOR` set to the pinned 5.050 and `<tree>` a `git archive` of the head.
- **Mailbox suite.** `make -C tb/verilator/mbx VERILATOR=<pinned 5.050> all` and `python3 -B tb/verilator/mbx/mutants.py --jobs 4`, in a `git archive` copy of the head.
- **Docs and merge.**
  - `scripts/docs_gates.sh`.
  - `git merge-tree --write-tree --name-only 4f6216ab d51b373a`, then `git diff <that tree> 72597d22`.

After the probes I removed the interpreter caches the runs created. The index equals `HEAD`'s tree: same blob ids, modes and stage 0. `git diff HEAD` is empty after a full refresh. The four submodules are checked out at their gitlinks, which equal dev's.

R530-3 FINISHED
