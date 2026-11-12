[R830] NEGATIVE - exact head bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb

# R830-2: external delta review of kebag-logic/milan-fpga PR #892 (issue #665), the tsn-c-stack pin move 70936b77 -> 715589c

Head `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb`, tree `32d7e5283d01e6ea541527d31974db62ee7c64b8`. That is six commits on round 1's `50e2a722` and fourteen on `dev-soft-core` `1d6bf555`.

- **Verdict: NEGATIVE.** One MINOR finding is open: N1, under Tests and Robustness.
- **Every named round-1 finding is closed**, each checked at its cause:
  - R830-1 F1 and F2;
  - R829-1 F1 and F2;
  - R830-1 F3 / R829-1 RES1.
- **Also recorded:** two retained RESIDUE items, from R829-1, and six SUGGESTIONs.
- **No BLOCKER or MAJOR** was found.
- **Conformance, RTL and Docs are covered clean at this head.**

N1 is small: one test and one plant. The redelivery's stop-at-decline condition, the half of the port contract's rule that keeps a declined command from being overwritten, can be deleted without any test failing. With it deleted, a command is silently never answered. That is the defect class this pin move exists to close.

## What was reconstructed, and from what

- **Contract:** AGENTS.md (sections 3 to 8) and CONTRIBUTING.md through its precedence rule.
- **Authority for this round:**
  - #665 issuecomment-6806698193: the round-2 ruling. Each finding is fixed as its Required outcome states, and R830-1 F1 needs "a test that fails without it".
  - issuecomment-6807277620: 41.0 RAMB36 accepted at the size fixture's 1x1/2if point; the 8x8/2if override re-keyed; `ACMP_MBX_PASS_MAX` 1,030 -> 2,754 acknowledged.
  - issuecomment-6811790762: 0.767 and 0.730 are recorded, not graded. The rule and the 0.75 ceiling go to #890, and S2b's sync owes item 4.
- **The author's public material:**
  - the two STOPs (issuecomment-6807249285, -6811703889);
  - REVIEW READY (issuecomment-6813799445);
  - the live PR body, which equals the packet's `PR-BODY.md` apart from a trailing newline.
- **Interface authority at the pin:** tsn-c-stack `docs/PORTING.md:74-117` ("ACMP owed bound", the redelivery rule and `bind_waiting`) at `715589c1`, and the loop contract `sw/firmware/ctrl/loop/ctrl_loop.h:14-55`.
- **Diff and history:**
  - `git diff 50e2a722..bfe7a9d6` (13 files), read in full;
  - `git diff 1d6bf555..bfe7a9d6` (25 files), for context;
  - every commit is one line with no trailers (`receipts/runs/diff-check-and-commits.txt`).
- **Author packet:** `review-evidence/tsnpin-r1/author-r2` at archive `35242f33a935cf336ba0c49f3a27d9b634da66d0` (branch `tsnpin-review-evidence`), fetched into a scratch repository. Sections read:
  - `HANDOFF.md` round 2;
  - `round2/gates-bfe7a9d6/verify.md` and its eleven SDK-step logs;
  - `round2/s2/*`, `round2/fixture-*`, `round2-load/*`.
  - The archive commit carries no signature header. Its identity is the fetched SHA, and the figures were checked against the files, not the summary.
- **Prior public findings:** my round-1 reports (R829-1, R830-1). They are resolved below. No other reviewer's report for this round was read.

## Prior findings: closed or retained, at their cause

| Finding | Status | Evidence at this head |
|---|---|---|
| **R830-1 F1** MINOR (all five lenses): kept-command later-command bound misstated; redelivery rule not met | **CLOSED** | See the four points below the table. |
| **R830-1 F2** MINOR Docs: S2 harness said the core drops what this pin keeps | **CLOSED** | `tb/verilator/ctrl_service_budget/README.md:553-557,576` and `scenario.py:827-828` are labelled "at tsn-c-stack `70936b77`", with the `715589c` behaviour stated. The round-1 verification grep hits only `README.md:554`, which is labelled. |
| **R830-1 F3** / **R829-1 RES1** RESIDUE: lane name in a new docstring | **CLOSED** | `sw/firmware/ctrl/test/acmp_owed_mutants.py:1` is exactly the given fix. |
| **R830-1 S1** SUGGESTION: the empty-kept guard is held by no test | **RETAINED as S1** | My plant `empty-kept-offered`, re-anchored on `acmp_mbx.c:159`, still escapes the acmp arm (`receipts/probes/adapter-mutants-summary.log`). |
| **R829-1 F1** MINOR Tests: the poll's "still owes" return unpinned at one owed frame | **CLOSED** | E3 (`test_acmp_mbx.cpp:1124-1156`) calls every poll directly and asserts no sleep. Plant `acmp-poll-owes-nothing-at-one` (R829's P6) is caught in my control campaign: `receipts/runs/fw-shard1.log:610`, "[ok] … 2 check(s) failed". |
| **R829-1 F2** MINOR Docs: the replica claimed the pinned SDK while using another GCC 14.3.0 build | **CLOSED** | See the three points below the table. |
| **R829-1 RES2** RESIDUE: PR body round-1 commit row "grows 144 to 152 B at every point" | **RETAINED as RES2** | Live PR body line 47 is unchanged. |
| **R829-1 RES3** RESIDUE: `MAILBOX_SPLIT.md` kept-command sentence omits the BIND_RX case | **RETAINED as RES3** | `docs/design/MAILBOX_SPLIT.md:582-583` was rewritten this round, but still names only "all eight owed". |
| **R829-1 S1** SUGGESTION: pin the BIND_RX-only-answered exception | **SUPERSEDED** | The exception is gone. The header now claims the bound with "a BIND_RX that is only answered between them included", and that case is untested (S2 below). |
| **R829-1 S2** SUGGESTION: refuse `__lshrdi3` in the portable `rv32` arm too | **RETAINED as S3** | `plat_arms.py:112` is untouched by the delta. |
| **R829-1 S3 / S4** | **SUPERSEDED** | By F2's closure and by the rule being met. |

**R830-1 F1, the evidence:**
- **The rule is implemented.** `acmp_mbx.c:157-175` (`redeliver`) offers the kept record, then up to `ACMP_MBX_REDELIVER_RECORDS` (19) waiting records in arrival order, until a decline. It runs from `on_poll` (`:181-190`) after a poll that sent, so before the next timer service. This matches `PORTING.md:88`.
- **The bound is restated.** `acmp_mbx.h:28-51` states n + 1 + f + r for every case. `:117-127` qualifies the A1 take bound while a command is kept.
- **My round-1 probe P1, re-run unchanged at this head** (`receipts/probes/control-no-plant.log:371-372`): the second command leaves in **pass 10** both with and without the two no-answer frames. At `50e2a722` it left in pass 11.
- **K4** (`test_acmp_mbx.cpp:1344`) pins that figure. Plant `acmp-redelivery-takes-no-waiting-record` is caught (`fw-shard1.log:628`).

**R829-1 F2, the evidence:**
- **The SDK steps ran.** The eleven "Install and verify the pinned RV32 SDK" steps at `bfe7a9d6` all have rc 0 (`round2/gates-bfe7a9d6/verify.md` rows 32, 67, 78, 149, 158, 165, 172, 179, 189, 214 and 228). Each log ends "SDK verified … `d42680e9…` … installer_sha256 `ffcc5433…`", "Buildroot 2021.11-18033-g83947c7bb6", "SDK cache hit: verified".
- **The installer is this head's.** `sha256sum scripts/ci_rv32_sdk.py` at this head is `ffcc5433d97209b00cac5155c61bc464a43a60fec49bce0330d81279e1df7cb4`.
- **My own install of the same archive** with the same installer: install rc 0, `--verify-only` rc 0, same identity (`receipts/sdk/`). The PR body's SDK statement is corrected.

## The brief's scope items

**(2) The redelivery and its RAMB36 effect, derived from the build.**
- **Build.** `ctrl_image.py --base 50e2a722` at this head on my pinned SDK (`receipts/runs/ctrl-image-vs-r1head.log`):
  - text grows by +128 B at both shapes (1x1: 35,784 -> 35,912; 8x8: 35,788 -> 35,916);
  - bss is unchanged;
  - the head figure equals the author's `round2/ctrl_image-redelivery-against-1d6bf555.log` (35,912).
- **Symbols** (`receipts/probes/adapter-symbol-sizes.txt`): `on_poll` 128 -> 244 B and `acmp_mbx_attach` 216 -> 228 B. These are the same as the author's fixture symbol diff. The fixture's extra `request` +12 B and `image_app` +8 B come from objects outside `ctrl_app`.
- **Banks.** I could not link the LiteX-runtime fixture (no runtime archives or migen here). Instead I applied the repository's own `ctrl_memory.banks` to the needs, building on the measured +144 B `rom` (`receipts/probes/bank-arithmetic.txt`):
  - 106,408 B -> 52 granules -> [64K, 32K, 8K];
  - 106,552 B -> 53 granules -> [64K, 32K, 8K, 2K];
  - with `sram` 57,808 B unchanged at [32K, 16K, 8K, 2K] (14.5), that is 40.5 -> **41.0**, 56 B over the 106,496 B granule edge.
- **Other points.** 8x8/1if leaves 88 B and 8x8/2if 480 B; both plans are unchanged.
- **Ledger.** `ctrl_memory.py:217` and `ctrl_memory_ledger.py:26` carry `ctrl_plat` 21,392 and 20,080, which agree with `SPLIT_CONTROL_MEMORY.md:97,296-311`.
- **Accepted** by issuecomment-6807277620.

**(3) The eleven pinned-SDK steps run and pass.** They do; see R829-1 F2 above.

**(4) S2 at both pins.** From `round2/s2/{base,head,final}-{1x1,8x8}.table.md` (rc 0 each):

| Point | At `70936b77` | At `715589c` |
|---|---|---|
| 1x1 | all four `backlog.owed_behind{0..3}` NEVER ANSWERED (≥ 362.723-362.726 ms) | answered at 94.958, 98.722, 102.820 and **104.568** ms |
| 8x8 | NEVER ANSWERED (≥ 370.364 ms) | answered at 120.289, 127.860, 133.109 and **138.526** ms |

- The `final` runs (snapshot taken after `bfe7a9d6` was committed) give tables identical to the `head` runs at `8ffcf2fc`.
- The `rom` bytes in the logs (104,984 and 120,352) are the head's ledger figures.
- Every answer is over the harness's 20 ms ceiling and within the 200 ms of Milan v1.2 Table 5.26. This is recorded, not graded.

**(5) The load figures.**
- **0.767 and 0.483** are in `round2-load/load_r2.md` / `load_r2.json`: `item.acmp` 165 us at 8x8 and 120 us at 1x1.
- **0.730 has no computing receipt in the packet.** It is stated in prose, and it is linear-consistent: the 0.063 term × 70/165 gives ≈ 0.731, and × 45/165 gives ≈ 0.721.
- **Nothing in this tree grades either figure.** `load_grade`, `flip_grade` and `poll_grade` are absent from `dev-soft-core` (`git grep`: no hits), and the PR body labels them "recorded, not graded".
- Per issuecomment-6811790762, #890 owns the proof (see S5).

**(6) Items handed to S2b's sync.**
- They are stated in the PR body (line 155) and in REVIEW READY:
  - the 8x8/2if fixture at 58.0 against 57.5 (122,984 B needs 61 granules, `bank-arithmetic.txt`);
  - the `__lshrdi3` hot-list entry;
  - the 1x1 ACMP poll at 10,974 measured against 6,500 stated.
- **None can land here.**
  - S2b's fixture arm, the hot list (`ctrl_split_hot.txt`) and `poll_grade.py` are not on this base (`git grep`: absent).
  - This PR's own 8x8/2if fixture keeps 57.5 with 480 B to spare.
  - Nothing on this base states a 6,500-cycle figure.

## Findings

### N1 — MINOR — Tests, Robustness — the redelivery's stop at a decline is held by no test; deleting it silently loses a command

**Where:** `sw/firmware/ctrl/acmp/acmp_mbx.c:166`, the `&& m->kept.len == 0u` term of the redelivery loop. Tests K1 and K4 to K7 (`test_acmp_mbx.cpp:1184,1344-1425`) and the plants in `acmp_owed_mutants.py:108-130`.

**Authority:**
- tsn-c-stack `PORTING.md:88`: the port offers waiting frames "until `acmp_rx` declines one", and `:100`: "Deliver no later ACMP frame before a kept one".
- `acmp_mbx.h:39-42`: "each until acmp_rx declines one, which it keeps".
- The round-2 ruling asks for the redelivery rule "with a test that fails without it".
- AGENTS.md section 6, Tests: each test can fail for the defect it claims to detect. Robustness: invalid ordering and repeated commands.

**Evidence:**
- **The plant.** `redelivery-past-a-decline` (`receipts/probes/redelivery-past-a-decline.patch`) drops that term.
  - The acmp arm passes every test: `receipts/probes/redelivery-past-a-decline.log`, "ESCAPED".
  - Every suite of `test_ctrl_firmware.py --require-rv32` passes on a planted copy of the head: `receipts/runs/plant-past-a-decline-full-suites.log`, `test_ctrl_firmware: PASS`, rc 0.
- **Why nothing catches it.** No test has a record still waiting behind a command the redelivery declines:
  - K1 has two commands, so the ring is empty after the decline;
  - K4 and K5 end on the decline;
  - K7's 19 records are malformed and never declined.
  - Branch coverage (42/42) is met because the term turns false in K4, but nothing observes the difference.
- **Reviewer probe P2** (`scripts/probe_p2.cpp`, inserted by `receipts/probes/p2/probe-p1-p2-insertion.patch`). Setup: the owed set full, then three GET_RX_STATEs (0x7101 kept, 0x7102 and 0x7103 waiting).
  - At the head it passes: order `6000…6007 7101 7102 7103` (`receipts/probes/p2/control-no-plant.log`).
  - With the plant it fails: order `6000…6007 7101 7103`, so **0x7102 is never answered** (`receipts/probes/p2/redelivery-past-a-decline.log`, "probes FAILED: …ProbeP2…").

**Impact:**
- A regression in this loop condition would overwrite the kept command with the next declined one. Its controller sees no response and its 200 ms timeout (Milan v1.2 Table 5.26) expires.
- That is the behaviour this pin move removes (S2: "never answered" at `70936b77`), and no gate would report it.
- The shipped code is correct. This is a verification gap.

**Required outcome:**
- A test in which the redelivery declines a command while at least one more record waits behind it. It asserts that every command is answered once, in arrival order, with nothing kept or owed after.
- A plant that drops the stop condition, named by that test in the control campaign.

**Verification:**
- Apply `receipts/probes/redelivery-past-a-decline.patch`. The new test must fail by name.
- The control campaign must rise from 585 to 586 caught.
- Probe P2 (or the new test) passes at the fixed head.

**Why not Conformance:** the code meets the rule (P1, P2 and K4 pass at the head). The ruling's literal bar, a test failing without the redelivery, is met by K4 and the five redelivery plants. The defect is in the depth of the tests, not in the behaviour.

### RES2 — RESIDUE — Docs — PR body round-1 commit row (retained from R829-1)

- **Where:** live PR body line 47, row "Ledger the platform's struct at its new size and state each point's plan".
- **Problem:** "`struct ctrl_plat` grows 144 to 152 B at every point" reads as a size change from 144 B to 152 B.
- **Exact fix:** "`struct ctrl_plat` grows by 152 B with one interface and by 144 B with two, at both shapes (round 1; the round-2 redelivery adds 8 B at the two-interface points)".

### RES3 — RESIDUE — Docs — `docs/design/MAILBOX_SPLIT.md:582-583` (retained from R829-1)

- **Problem:** the kept-command sentence leaves out the BIND_RX case of the owed bound.
- **Exact fix:** replace "A command that arrives with all eight owed is declined, not dropped:" with "A command that arrives with all eight owed, or a BIND_RX that arrives with fewer than two owed slots free, is declined, not dropped:".

### Suggestions (optional, non-blocking)

- **S1 [Tests]** (retained from R830-1 S1):
  - The guard `acmp_mbx.c:159` (`m->kept.len != 0u`) is still held by no test. The plant `empty-kept-offered` offers a zero-length record after every send with nothing kept, and it escapes.
  - The only effect is `rx_malformed` counting, plus wasted cycles in the poll.
  - Suggestion: K5 asserts `core()->rx_malformed` unchanged across its drain.
- **S2 [Tests]:**
  - `acmp_mbx.h:45-47` claims the bound with "a BIND_RX that is only answered between them included". K4 pins only frames that need no answer.
  - Suggestion: a K4 variant with an only-answered BIND_RX (unknown sink) between the two commands.
- **S3 [Tests]** (retained from R829-1 S2): refuse `__lshrdi3` in the portable `rv32` arm too, not only `platrv32` (`plat_arms.py:112`).
- **S4 [Docs]:**
  - The loop contract `ctrl_loop.h:18-21` describes a pass's receive service as "at most `CTRL_LOOP_RX_PER_PASS` records". The ACMP poll now takes up to 19 more acmp records. That is allowed under A2, as a module's stated poll cost, and stated in `acmp_mbx.h`.
  - Suggestion: one clause at item 3 saying a module's poll may take its own channel's records (THE KEPT COMMAND).
- **S5 [Docs, packet]:**
  - The 0.730 and 0.721 figures have no computing receipt; only the 0.767 column is in `load_r2.json`. The ruling gives the proof to #890.
  - `round2-load/acmp-item-split.txt` reports "heaviest less its nested handlers 14,291" at 8x8. That span covers `on_frame` only, which misses the kept record's direct `acmp_rx` call. It sits beside the 6,302 figure of `acmp-item-parts-8x8.txt`, which the 0.730 rests on.
  - Suggestion: label the split file's measure, or drop it, and publish the 0.730 column when #890 runs.
- **S6 [Tests, S2b's]:**
  - `scenario.py:833` keeps `may_drop=True` on the four commands behind the owed input, and `715589c` answers all four. That is right while the harness also records `70936b77`.
  - Suggestion for S2b, once only `715589c` is measured: drop the allowance so a lost answer fails the harness.

## Gates and probes I ran (scratch copies of the exact head, pinned SDK)

| Gate / probe | Result | Receipt |
|---|---|---|
| `ci_rv32_sdk.py --destination <scratch>` then `--verify-only` | rc 0 / rc 0; Buildroot 2021.11-18033-g83947c7bb6, archive `d42680e9…`, installer `ffcc5433…` | `receipts/sdk/` |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` (firmware-unit, `service_bounds` arm included) | PASS, rc 0 | `receipts/runs/fw-shard0.log` (`:67` service_bounds, `:110` acmp) |
| the same, `--shard 1/4` (firmware-control-mutants) | PASS: **585 of 585 caught**, the six new owed plants among them | `receipts/runs/fw-shard1.log` |
| `fw_coverage.py --selftest`, then `--check --jobs 4` | PASS (35 files); `acmp_mbx.c` 106/106 lines and 42/42 branches | `receipts/runs/fw-coverage.log:54` |
| `ctrl_image.py --base 50e2a722` | +128 B text at both shapes; symbols as above | `receipts/runs/ctrl-image-vs-r1head.log`, `receipts/probes/adapter-symbol-sizes.txt` |
| `docs/diagrams/submodule_boundaries.gen.py --check`; `scripts/check_submodule_docs.py` | OK (6 exact gitlinks) | `receipts/runs/docs-submodule*.log` |
| `scripts/check_py_idiom.py` (the gate `8ffcf2fc` failed); `scripts/check_cpp_idiom.py` | rc 0 / rc 0 | `receipts/runs/py-idiom.log`, `cpp-idiom.log` |
| `git diff --check 1d6bf555 HEAD`; commit messages | rc 0; 14 one-line commits, no trailers | `receipts/runs/diff-check-and-commits.txt` |
| Probe P1 (round 1's, unchanged) | second kept command in pass 10, with and without the gap | `receipts/probes/control-no-plant.log:371-372` |
| Probe P2 (new) | passes at the head; fails on `redelivery-past-a-decline` (0x7102 lost) | `receipts/probes/p2/` |
| Six reviewer plants on the redelivery, acmp arm | see below | `receipts/probes/adapter-mutants-summary.log` |
| `redelivery-past-a-decline` against every firmware suite | `test_ctrl_firmware: PASS` (escapes; N1) | `receipts/runs/plant-past-a-decline-full-suites.log` |

The six reviewer plants:
- **Caught:** `redelivery-before-the-send` (7 tests) and `redelivery-two-records` (K7).
- **Escaped:** `empty-kept-offered` (S1), `redelivery-past-a-decline` (N1), and `redelivery-continues-after-a-refusal`. The last is equivalent: `rx_resync` has already released the ring up to RX_HEAD, so no finding.

The clone was never built in. All runs used copies under the packet's scratch directory. One bytecode cache that my bank-arithmetic import created (`sw/litex/__pycache__/`, untracked) was removed. `receipts/restore-check.txt` shows:
- HEAD and tree exact;
- status empty with ignored files included;
- the index equal to the HEAD tree and the worktree equal to the index (contents and modes);
- all six gitlinks as recorded (`external` uninitialised, as at the start);
- every submodule clean.

## Lens results (all five applied at the exact head)

- **Conformance: CLEAN.**
  - Applied to `acmp_mbx.c:108-190` and `acmp_mbx.h:28-51,114-127,180-196`, against tsn-c-stack `PORTING.md:74-117` at `715589c1`.
  - The redelivery order, its trigger (an accepting poll, before timer service) and its stop all conform: P1 gives pass 10, P2 gives arrival order, and K4 to K7 pass.
  - `bind_waiting` covers the BIND_RX-declined-with-one-free case in the core (`PORTING.md:85-86,93`, and `:109`), so the header's "no timer probe is owed ahead of a waiting command" holds.
  - Each round-2 ruling item is met as stated. S2 shows the four commands answered within Table 5.26's 200 ms.
  - The load figures are recorded and not graded, as ruled.
- **RTL: CLEAN.** No HDL is in the diff. Applied to the firmware architecture and interfaces:
  - **Pass budget.** `ACMP_MBX_REDELIVER_MAX` = 52 + 19 × (36 + 52) = 1,724, with 19 = `MBX_CH_ACMP_RX_WORDS / 13`. It is an upper bound: at most a full ring, each record at most `ACMP_MBX_RX_RECORD_MAX`, and an EMPTY take costs less than the record it replaces.
  - **The restated pass bound** is `ACMP_MBX_PASS_MAX` 2,754. Every derived figure in `MAILBOX_SPLIT.md` (3 × / 9 × / 11 × / 22 × 2,754, 3,507 and 5,247 / 6,153) and in the two READMEs was re-computed and agrees. The `service_bounds` arm passes.
  - **Ceiling.** The documented owed-frame bound now exceeds the ceiling at 1 us per access. That is stated honestly, and the ruling acknowledged the 2,754.
  - **Buffer and reentrancy.** `l->frame` is reused only from the poll phase. Its only other user is the loop's receive service (`ctrl_loop.c:128-136`), and no path calls the loop re-entrantly.
  - **Sleep.** A pass that redelivers and ends owing nothing may sleep. That is safe, because the redelivery reaches every record waiting when the poll starts, and later records raise the RX level.
  - **RAMB36.** Derived as in item (2).
- **Robustness: UNCLEAN (N1).**
  - Clean within the lens:
    - a refused record during redelivery ends it, counted (K6, and `rx_resync` releases to RX_HEAD);
    - a full ring of the smallest records (K7);
    - a refused poll offers nothing (`acmp-kept-offered-on-a-refused-poll`, caught);
    - reset (K3);
    - one-owed-frame wake (E3);
    - redelivery with nothing kept (K5).
  - Not clean: the order and repeated-command case behind a decline (N1).
- **Tests: UNCLEAN (N1).**
  - Examined: E3 and K1 to K7 (`test_acmp_mbx.cpp:1124-1156,1184-1425`); the six new and four re-anchored plants (`acmp_owed_mutants.py`); 585 of 585 caught; coverage 106/106 and 42/42; six reviewer plants.
  - Not clean: N1. S1 and S2 are optional.
- **Docs: CLEAN.**
  - Examined:
    - `acmp_mbx.h`;
    - `MAILBOX_SPLIT.md:578-587,676-778` (every figure re-computed);
    - `SPLIT_CONTROL_MEMORY.md:94-97,293-312` (checked against the receipts and the bank arithmetic);
    - `sw/firmware/ctrl/README.md:387-442` and `maap/README.md:165`;
    - `tb/verilator/ctrl_service_budget/README.md:550-576` and `scenario.py:827-828`;
    - `coverage.ratchet`;
    - the live PR body, against the receipts.
  - The comment rule was checked: no lane, round, reviewer or comment ID appears in a new source comment of the delta.
  - Only residue remains (RES2, RES3). S4 and S5 are optional.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `acmp_mbx.c:108-190`, `acmp_mbx.h:28-51,114-127,180-196`; tsn-c-stack `docs/PORTING.md:74-117` at `715589c1`; probes P1 and P2 at the head; `round2/s2/*-{1x1,8x8}.table.md`; `round2-load/load_r2.{md,json}`; rulings -6806698193, -6807277620, -6811790762 | R830-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| RTL | CLEAN | `acmp_mbx.h:180-196` (pass terms), `ctrl_loop.c:121-160`, `ctrl_loop.h:14-55`, `mbx.c:363-401`, `MAILBOX_SPLIT.md:676-778` arithmetic, `fw-shard0.log:67` (service_bounds), `ctrl-image-vs-r1head.log`, `adapter-symbol-sizes.txt`, `bank-arithmetic.txt`, `ctrl_memory.py:217`, `ctrl_memory_ledger.py:26` (no HDL in the diff) | R830-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| Robustness | UNCLEAN (N1) | K3, K5 to K7, E3, `mbx.c:363-368`, reviewer plants and P2 (`receipts/probes/`) | R830-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| Tests | UNCLEAN (N1) | `test_acmp_mbx.cpp:1124-1156,1184-1425`, `acmp_owed_mutants.py`, `fw-shard0.log`, `fw-shard1.log` (585/585), `fw-coverage.log`, `plant-past-a-decline-full-suites.log`, `adapter-mutants-summary.log`, `p2/` | R830-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |
| Docs | CLEAN (RES2 and RES3 are residue) | `acmp_mbx.h`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md`, `sw/firmware/ctrl/README.md`, `maap/README.md`, `tb/verilator/ctrl_service_budget/README.md:550-576`, `scenario.py:827-828`, `coverage.ratchet`, the live PR body, `docs-submodule*.log`, `py-idiom.log` | R830-2 | `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` |

## Real limits

- **No manager source bank** ran at this head, and none is claimed or inferred.
- **Source-head execution evidence is the author's published gate receipts.** I read them; I did not re-run them. They cover:
  - every `run:` step of the four workflows (150 rc 0, 215 not run with a reason, 0 bad);
  - the AECP and SRP campaigns, firmware-boundary and firmware-verilator;
  - the sweep's `mbx` suite, `test_builder.py`, `behave`;
  - S2.
- **Not re-run here:** I re-ran only firmware-unit, firmware-control-mutants, coverage, the two docs gates and the two idiom gates.
- **The LiteX-linked fixture and platform images, S2's images and the load graders were not rebuilt.** There is no LiteX/migen or runtime archives here, and the graders are on S2b's branch. The RAMB36 effect is derived from my pinned-SDK build delta plus the repository's `ctrl_memory.banks`, not from a re-linked fixture.
- **Toolchain:** host GCC 16.2.1, GoogleTest 1.18 and Python 3.14.9 / PyYAML 6.0.3, against CI's ubuntu-24.04 and CPython 3.12 (`receipts/toolchain.txt`).
- **Hosted:** at capture (`receipts/hosted-check-runs.captured-at`), the exact head reported **no** check runs and no workflow runs (`receipts/hosted-check-runs.tsv` and `hosted-workflow-runs.tsv` are empty). No hosted context is evidence here; hosted and act acceptance are the manager's.
- **Hardware:** physical calibration NOT RUN, and field skips are not hardware proof.
- **Not assessed here:** 32x32 (S15's) and the #890 accounting rule.

## Pending manager duties

- **N1:** route the fix (one test, one plant) and a delta re-review of `test_acmp_mbx.cpp` / `acmp_owed_mutants.py`. The Tests and Robustness lenses must be re-covered at the new head. Conformance, RTL and Docs stay covered unless `acmp_mbx.c`/`.h` or the docs change.
- **Residue checklist:** RES2 and RES3.
- **#890:** the nested-receive accounting rule, its controls, and the 0.730 column receipt (S5).
- **S2b's sync onto this pin (item 4):**
  - the 8x8/2if fixture ledger (58.0 RAMB36);
  - drop the hot list's `__lshrdi3`;
  - restate `poll_grade.py`'s 1x1 ACMP item (10,974 cycles measured);
  - optionally S6.
- **S15:** rebuild 32x32 on this pin.
- **Merge turn:** validate the current-dev candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`) with the builder and native banks, link the receipts, and accept exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` evidence (none was reported at capture).

R830-2 FINISHED
