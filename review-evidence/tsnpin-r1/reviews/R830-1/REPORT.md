[R830] NEGATIVE - exact head 50e2a722ef2671b3f5b017f97b1c7d41705c4f32

# R830-1: external review of kebag-logic/milan-fpga PR #892 (issue #665), the tsn-c-stack pin move to 715589c

Head `50e2a722ef2671b3f5b017f97b1c7d41705c4f32`, tree `895066febbe99d8a88c9152a2432aeab908e9dc9`, eight commits on `dev-soft-core` `1d6bf555`.

- **Verdict: NEGATIVE.** Two MINOR findings are open: F1, attributable to all five lenses, and F2, a Docs finding.
- **Also recorded:** one RESIDUE (F3) and one SUGGESTION (S1).
- **No BLOCKER or MAJOR** was found.

## What was reconstructed, and from what

- **Contract:** AGENTS.md, then CONTRIBUTING.md through its precedence rule.
- **Issue #665:**
  - the issue body, which has no lane-specific acceptance;
  - the lane's TAKEN (issuecomment-6792567545) and REVIEW READY (issuecomment-6804604273);
  - the #859 round 4 ruling, item 1 (issuecomment-6746289265): the pin move is its own lane;
  - the tsn-c-stack PR #34 round 2 ruling, item 3 (issuecomment-6789256216): the parent consumer bar is deferred to this lane;
  - the S2b comments that name the +132 B effect (issuecomment-6778599191, item 5) and the 0.75 ceiling (issuecomment-6798230066, #890).
- **Interface authorities at the moved pin:**
  - tsn-c-stack `docs/PORTING.md` "ACMP owed bound" (lines 74-117);
  - tsn-c-stack `docs/REQUIREMENTS.md` ACMP-12;
  - the loop contract in `sw/firmware/ctrl/loop/ctrl_loop.h` (A1 to A4, THE BOUND).
- **Diff and history:** `git diff 1d6bf555..50e2a722` (23 files) and every commit.
- **Author's packet:** `review-evidence/tsnpin-r1` at archive `8561308e` (HANDOFF, PR body, receipts).
- **Prior public review findings:** the PR thread carried none when this round started. The only other review activity is the parallel internal round's start notice, so nothing needs resolving or retaining.

## Scope checks (the brief's items 1 to 5)

| Item | Result | Evidence |
|---|---|---|
| 1. `715589c` is tsn-c-stack `main` and a fast-forward of `70936b77`; nothing edited in the submodule | **Holds.** `ls-remote main` = `715589c1…`. `merge-base --is-ancestor 70936b77 715589c1` rc 0. `715589c1` is PR #34's merge commit, and the merge commits of PRs #28, #29, #30 and #33 are all in the range. The submodule worktree is clean, ignored files included. | `receipts/pin-check.txt` |
| 2a. #28's adapter: offers each frame, keeps it on decline, `acmp_rx_ready` a hint | **Partly.** Every record goes to `acmp_rx`, and a declined one is kept and offered again after an accepting poll (`acmp_mbx.c:111-165`). After that poll, though, the adapter offers *only* the kept record. The port contract's redelivery rule has it offer every waiting frame (**F1**). | `scripts/probe_p1.cpp`, `receipts/probes/` |
| 2b. #29's hot-list entry | The hot list (`ctrl_split_hot.txt`, `ctrl_hot.py`) **is not on this base** (`git ls-files`: absent). In its place, the `platrv32` arm refuses `__lshrdi3` (`plat_arms.py:158-159`), and plant `wire-put-be-shifts-64-bits` is caught. S2b still owes the hot-list entry at its sync. | `receipts/runs/fw-shard1.log`, author `rv32/` receipts |
| 2c. ACMP sizing for #33 | One mask word at 16 sinks. The coverage ratchet and the ledger (`sram` +144 to +160 B) agree with that layout. | `coverage.ratchet`, `SPLIT_CONTROL_MEMORY.md:296-310` |
| 3. Consumer bar at the pin | Every firmware gate runnable here passes (table below). Ledger at 1x1, 8x8/1if and 8x8/2if: no RAMB36 plan moves in either image, `rom` +304 to +400 B, and `__lshrdi3` leaves every image. The **+132 B over-granule effect belongs to S2b's `answering-every-port` arm**, which is not on this base (`git grep`: none). There is **no 32x32 shape** on this base. | author `ledger/*-table.md`, checked equal to `ctrl_memory_ledger.py:26` and `SPLIT_CONTROL_MEMORY.md:94` |
| 4. S2 at the moved pin, recorded against the old | rc 0 at both points and both pins. "An ACMP command behind the owed input" goes from never answered to 104.915 ms (1x1) and 137.688 ms (8x8). `load_grade.py` and `flip_grade.py` are **not on this base**, so the ~0.72 / 0.75 flip read belongs to S2b and #890. | author `s2/compare-*.md`, `s2/*/run.rc` (all 0) |
| 5. Docs and census naming the old pin | The pins table, the adoption table, the diagram (its gate passes) and every stack link have moved. The remaining `70936b77` mentions are the before-figures and `ci/image/exec-audit-receipt.json`, which is an audit receipt of a recorded tree. One stale behavioural description remains (**F2**). | `receipts/runs/docs-submodule-*.log` |

## Findings

### F1 — MINOR — Conformance, RTL, Robustness, Tests, Docs — the kept command's later-command bound is wrongly stated, and the redelivery rule is not met

**Where:**
- `sw/firmware/ctrl/acmp/acmp_mbx.c:155-165` (`on_poll`);
- `sw/firmware/ctrl/acmp/acmp_mbx.h:40-47` and `:118-121`.

**Authority:**
- tsn-c-stack `docs/PORTING.md:88-89` at `715589c`: "After each `acmp_poll` that accepts an owed frame, the port offers its waiting ACMP frames in arrival order … until `acmp_rx` declines one … This is the redelivery rule the bound below assumes."
- `:92`: "Offering fewer waiting frames … can leave a slot free at timer service after **a frame that needs no answer** or a BIND_RX that is only answered, and a timer probe owed there delays each later kept command one pass."
- ACMP-12 (`docs/REQUIREMENTS.md`) points to that contract for "the redelivery order".

**What the adapter does and states:**
- After an accepting poll it offers only the kept record. The records behind it wait for a later pass's receive service, which runs after that pass's timer service.
- `acmp_mbx.h:40-47` names one exception, a kept BIND_RX that is only answered. For every other case it states: "Otherwise a kept command's response leaves in pass n + 1 + f + r after the room returns."

**Reviewer probe P1** (`scripts/probe_p1.cpp`, run by `scripts/run_acmp_arm.py` on a scratch copy of the head):
- Setup:
  - eight owed frames, with the egress held;
  - two GET_RX_STATE commands for sink 1;
  - two PROBE_TX_RESPONSEs between them, which are frames that need no answer;
  - sink 0's TMR_NO_RESP retry, falling due in the third pass after the room returns.
- Control run, without the two frames: the second command leaves in **pass 10** (n + 1 + f, n = 8, f = 1), and the probe is counted lost.
- Run with the two frames: the retry probe takes the slot freed in pass 2, and the second command leaves in **pass 11** (`receipts/probes/probe-p1-acmp-arm.log:361-362`).
- So the header's figure for that case is wrong.

**Related gaps:**
- The PR's open question and the header name only the BIND_RX case, so the decision request does not show the whole deviation.
- `acmp_mbx.h:118-121` still states, without condition, that every acmp record "is taken by pass ACMP_MBX_RX_PASSES (10)". While a command is kept, the ring is deliberately not taken (`:36`, `on_rx_ready`). That bound now holds only under A3.
- No test covers a later kept command behind records that need no answer while a timer probe is due. K1 uses back-to-back GET_RX_STATEs only, so the stated bound is not pinned for that case.

**Impact:**
- Each interleaving of this kind lets one timer probe slip one pass ahead of each later kept command.
- The contract's egress-hold budget (`PORTING.md`, "Budget the egress hold … (ACMP_OWED_MAX + 1 + f + r) * p ms") is computed from the bound the adapter states but does not keep.
- At 8x8 the measured passes are milliseconds long. The timeout is 200 ms (Milan v1.2 Table 5.26), and S2 already measures 137.688 ms for the gap-free case.
- The core has no defect. The deviation is in the parent adapter only.

**Required outcome, one of:**
- (a) A maintainer decision, recorded publicly, that accepts one-record redelivery. In that case:
  - `acmp_mbx.h` states the kept-command bound as a figure for every case the contract names, no-answer frames included;
  - the A1 take bound at `:118-121` is qualified for the kept state;
  - a test pins the later-command figure with interleaved no-answer frames and a due timer probe, and a plant that breaks it is caught.
- (b) The contract's redelivery rule implemented within a stated per-pass budget, with the same test. The author's reason for not doing so is `ctrl_loop.h` A1.

**Verification:** re-run probe P1 at the new head. It must either assert the header's stated figure, or show pass 10 under the contract rule. The new test must fail on its plant.

### F2 — MINOR — Docs — the S2 harness still says the core drops the commands this pin keeps

**Where:**
- `tb/verilator/ctrl_service_budget/README.md:553-555` and `:575`;
- the comment at `tb/verilator/ctrl_service_budget/scenario.py:827-828`.

**Evidence:**
- At the merged head these lines say, in the present tense: "The ACMP core drops the commands it cannot owe … `room()` counts a busy drop … the core takes the commands behind and never answers them."
- The README does not name the pin it measured at.
- At `715589c` the core declines those commands (ACMP-12), and this PR's adapter keeps and answers them. The PR's own S2 record shows "never answered -> answered after 104.915 / 137.688 ms".
- The PR body says the harness READMEs "record measurements at the old pin; their owners re-measure". The README itself does not say so.

**Impact:**
- A cold reader at the merged head is told the opposite of what this PR ships.
- The harness's `may_drop=True` allowance for those probes is still justified by a comment that no longer holds.

**Required outcome:** either the README finding and the scenario comment state that they were measured at tsn-c-stack `70936b77` and that `715589c` keeps the command (citing the PR's at-both-pins record), or the owner lane's update (S2b, #810) lands in the same train before this merges. The manager decides which.

**Verification:** at the merge candidate, `git grep -n "drops the commands\|busy drop\|may never be answered" -- tb/verilator/ctrl_service_budget` shows either the pin label or no hit.

### F3 — RESIDUE — Docs — a lane name in a new source docstring

- **Where:** `sw/firmware/ctrl/test/acmp_owed_mutants.py:3`, a new file in this delta: `"""acmp_owed_mutants.py - lane F3's planted defects of the ACMP owed frames (#665).`
- **Rule:** no lane names in source comments (owner 2026-10-15). The existing instances in `acmp_mutants.py:3` and `acmp_review_mutants.py:3` are #746's.
- **Exact fix:** `"""acmp_owed_mutants.py - the planted defects of the ACMP owed frames (#665).`

### S1 — SUGGESTION — Tests — one adapter guard is held by no test

- **Where:** `test_acmp_mbx.cpp:1147-1197` (K1) and `acmp_mbx.c:160`.
- **Evidence:** I planted two defects of my own (`scripts/adapter_mutants.py`, `receipts/probes/adapter-mutants-summary.log`):
  - `kept-offered-before-the-poll` is caught by K1 and K2;
  - `empty-kept-offered` drops the `m->kept.len != 0u` guard, so every accepting poll offers a zero-length record. It **escapes** every existing test; only the reviewer probe fails.
- **Effect:** the core counts the empty record in `rx_malformed`, which no firmware path reads (`git grep`: tests only).
- **Suggestion:** K1 asserts that `rx_malformed` is unchanged across its drain.

## Gates I ran at the exact head

Runs are on the reviewed clone unless marked as a scratch copy. The clone was restored afterwards (`receipts/restore-check.txt`).

| Gate | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` (firmware-unit) | PASS | `receipts/runs/fw-shard0.log` |
| the same, `--shard 1/4` (firmware-control-mutants) | PASS: **579 of 579 caught**, the 9 adapter plants and `wire-put-be-shifts-64-bits` among them | `receipts/runs/fw-shard1.log` |
| the same, `--shard 2/4` (firmware-aecp-mutants) | PASS: 139 `[ok]`, 0 escaped (the author's count at this head) | `receipts/runs/fw-shard2.log` |
| the same, `--shard 3/4` (firmware-srp-mutants) | PASS: 280 `[ok]`, 0 escaped (the author's count at this head) | `receipts/runs/fw-shard3.log` |
| `fw_coverage.py --selftest`, then `--check --jobs 4` | PASS (35 files) | `receipts/runs/fw-coverage-check.log` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (firmware-verilator), on Verilator 5.050 with its identity checked | PASS: 1019 sources, 0 findings | `receipts/runs/boundary-only-verilator.log`, `receipts/toolchain.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (firmware-boundary) | **refused by the environment**: `test_ctrl_memory.py` needs `migen`, and this host has no LiteX interpreter. The author's receipt is PASS over 3258 sources. | `receipts/runs/boundary-without-verilator.log` |
| `sw/litex/test_ctrl_memory.py` | **not run** (no `migen`); the author's receipt only | `receipts/runs/litex-test-ctrl-memory.log` |
| `submodule_boundaries.gen.py --check`; `check_submodule_docs.py` | OK (6 exact gitlinks) | `receipts/runs/docs-submodule-*.log` |
| `git diff --check 1d6bf555 HEAD`; commit messages | rc 0; every commit is one line with no trailers | this report |
| Probe P1, on a scratch copy | the second kept command leaves in pass 11 with the gap, and in pass 10 without it (F1) | `receipts/probes/probe-p1-acmp-arm.log` |
| Two adapter plants, on a scratch copy | 1 caught, 1 escaped (S1) | `receipts/probes/` |

`receipts/runs/RC-NOTE.txt` states which rc files were derived from their logs' verdict lines.

## Lens results (all five applied at the exact head)

- **Conformance: UNCLEAN (F1).**
  - Applied to `acmp_mbx.c:111-165` and `acmp_mbx.h:28-51`, against `PORTING.md` "ACMP owed bound" lines 74-117 and ACMP-12 at `715589c`, with probe P1.
  - Clean within the lens: the pin identity; decline-not-drop and arrival order (K1, and `on_rx_ready` gating the ring); a BIND_RX waiting for two slots with no probe lost (K2); `__lshrdi3` absent (the `platrv32` arm); sizing at 16 sinks.
- **RTL: UNCLEAN (F1).**
  - No HDL is in the diff (`git diff --stat`). The lens was applied to the firmware architecture and interface contracts:
    - the loop's per-pass budget and THE BOUND (`ctrl_loop.c:121-160`, `ctrl_loop.h:20-60`);
    - the adapter's pass bounds and `ACMP_MBX_PASS_MAX`;
    - the kept buffer's size against `mbx_rx_take`'s refusal (`mbx.c:387`, 128 B).
  - No RAMB36 plan moves (ledger receipts).
- **Robustness: UNCLEAN (F1).**
  - Clean within the lens:
    - backpressure: the egress held for 20 passes, and a refused poll offers nothing;
    - reset during a kept command (K3, `acmp_mbx_init`'s `memset`);
    - repeated declines (K2);
    - an oversized record, which the driver refuses;
    - the owed-set drain (`acmp.c:1302-1324` is the only decrement of `owed_count`, so no kept command can strand the ring).
  - Not clean: interleaved records with a timer probe due (F1).
- **Tests: UNCLEAN (F1).**
  - Examined: K1 to K3 (`test_acmp_mbx.cpp:1147-1248`); the eight K plants and nine adapter plants in `acmp_owed_mutants.py`; the re-anchored plants in `acmp_review_mutants.py` and `ctrl_mutants.py`.
  - The four campaigns re-run here: 579 of 579, 139 and 280, all with 0 escaped.
  - Not clean: the stated later-command bound is untested (F1). S1 is one escape of my own plants.
- **Docs: UNCLEAN (F1, F2).**
  - Clean within the lens: `SUBMODULES.md`, the diagram, the four READMEs, `MAILBOX_SPLIT.md:579-586`, the ledger tables in `SPLIT_CONTROL_MEMORY.md:94` and `:296-310` (checked against the receipts), and the PR body's limitation statements (checked against the tree).
  - Not clean: F1's header statements and F2. F3 is residue.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `acmp_mbx.c:111-165`, `acmp_mbx.h:28-51,118-121`, tsn-c-stack `docs/PORTING.md:74-117` and ACMP-12 at `715589c`, probe P1, `plat_arms.py:111-160`, `receipts/pin-check.txt` | R830-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| RTL | UNCLEAN (F1) | `ctrl_loop.c:121-160`, `ctrl_loop.h:20-60`, `acmp_mbx.h:96-195`, `mbx.c:387`, `ctrl_memory.py:217`, `ctrl_memory_ledger.py:26`, author ledger receipts (no HDL in the diff) | R830-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| Robustness | UNCLEAN (F1) | K1 to K3, `acmp.c:305-360,1103-1160,1302-1324` at `715589c`, probe P1, two adapter plants | R830-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| Tests | UNCLEAN (F1) | `test_acmp_mbx.cpp:1118-1248`, `acmp_owed_mutants.py`, `acmp_review_mutants.py`, `ctrl_mutants.py`, `fw-shard0..3.log`, `fw-coverage-check.log`, `adapter-mutants-summary.log` | R830-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| Docs | UNCLEAN (F1, F2) | `SUBMODULES.md`, `submodule_boundaries.*`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md`, `sw/firmware/ctrl/README.md`, `maap/README.md`, `gtest/README.md`, `acmp_mbx.h`, `tb/verilator/ctrl_service_budget/README.md:553-575`, `scenario.py:827-828`, the PR body | R830-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |

## Real limits

- **No manager source bank** ran at this head, and none is claimed or inferred.
- **The rest of the source-head execution evidence is the author's published receipts at `50e2a722`.** I read them; I did not re-run them. They cover:
  - the full sweep;
  - every `run:` step of `docs.yml`, `rtl-fast.yml`, `elaborate.yml` and `rtl.yml` (139 rc 0, 226 not run with a reason; I found no non-zero rc file);
  - the `test_builder.py` legs, `behave` and `test_ctrl_nvm.py`;
  - the S2 harness runs.
- **Not run, by the brief:** the full parent and builder banks, Docker/act and the host `act_ci`.
- **Not runnable on this host:** the non-Verilator `firmware-boundary` form and `sw/litex/test_ctrl_memory.py`. There is no LiteX/`migen` interpreter here, so the ROM/RAM ledger was not re-measured. Its figures are the author's receipts, checked equal to `ctrl_memory_ledger.py` and `SPLIT_CONTROL_MEMORY.md`.
- **Interpreter:** the campaigns ran under an existing read-only Python 3.14 interpreter carrying PyYAML 6.0.3. CI pins CPython 3.12 (`receipts/toolchain.txt`).
- **Hosted runs:** the snapshot at this head (`receipts/hosted-checks-snapshot.txt`) shows the firmware, Verilator and Yosys jobs queued or in progress. It is not evidence; hosted and act acceptance are the manager's.
- **Hardware:** physical calibration NOT RUN, and field skips are not hardware proof.
- **32x32:** not assessed. There is no such shape on this base; it is S15's.

## Pending manager duties

- **F1:** decide the redelivery deviation: either accept one-record redelivery with a correct stated bound, or require the contract rule.
- **F2:** decide its path: a pin label in this PR, or S2b's update in the same train.
- **At S2b's (#810) sync onto this pin:**
  - drop the hot list's `__lshrdi3` entry;
  - re-measure the 8x8/2if `answering-every-port` arm's `rom`. It was 132 B over its granule with tsn-c-stack#32 alone, and this PR's adapter adds +304 to +400 B of `rom` on this base's images;
  - re-grade the 8x8/2if flip check at this pin, with the kept-command adapter, against #890's 0.75 ceiling.
- **S15:** rebuild 32x32 on this pin (#859 round 4 ruling).
- **Merge candidate:** validate the current-dev candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`) with the builder and native banks, and link the receipts on the PR.
- **Hosted evidence:** accept the exact-head `rtl-fast`, `verilator-suites` and `yosys-portability` evidence when it completes.
- **Residue:** carry F3 to the residue checklist.

R830-1 FINISHED
