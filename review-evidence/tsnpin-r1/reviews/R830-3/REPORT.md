[R830] POSITIVE - exact head 32b43973069ee2742f86c4f92adb5eb9ca6bdfb3

# R830-3: external delta review, issue #665 / PR #892 (dev-soft-core tsn-c-stack pin 70936b77 -> 715589c)

- **Head:** `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3`, tree `4b82e85895812b8094c877becd12cbfdd5f86585`. The PR head ref matches it, and the PR is not a draft.
- **Delta:** `bfe7a9d6..32b43973`, two commits (`91224a0d`, `32b43973`), four files, +44/-3:
  - `sw/firmware/ctrl/test/test_acmp_mbx.cpp`: new test K8.
  - `sw/firmware/ctrl/test/acmp_owed_mutants.py`: new plant.
  - `docs/design/MAILBOX_SPLIT.md:582-585` and `docs/design/SPLIT_CONTROL_MEMORY.md:309`: wording.
- **Ruling answered:** round-3 ruling, #665 issuecomment-6814546620, items 1 to 3.
- **Author packet:** archive `f3fed3c2`, an ancestor of the live `tsnpin-review-evidence` tip `4214fab9`.
- **Verdict:** POSITIVE.
  - No BLOCKER, MAJOR or MINOR finding is open.
  - Three RESIDUE items (wording only) and three SUGGESTIONs are recorded below.
  - Every prior round-2 finding is closed at its cause.

## Ruling items checked against code and receipts

### (1) F1 / N1: the redelivery's stop at a decline. CLOSED

- **The test.** K8, `test_acmp_mbx.cpp:1427-1460`, `K8ACommandTheRedeliveryDeclinesKeepsItsPlaceAheadOfTheNext`:
  - The owed set is full, then three GET_RX_STATEs (0x7901 to 0x7903) arrive on one interface.
  - Before the egress returns it asserts one decline, a record kept, and exactly one record taken (`:1440`).
  - After the egress returns it asserts the exact wire order: the eight owed frames, then 0x7901, 0x7902, 0x7903, each once (`:1457`).
  - It also asserts three declines in total, with nothing kept or owed after (`:1458`).
- **Why it can fail.** With the stop removed, the third command's decline overwrites the kept second one in `on_frame` (`acmp_mbx.c:117-119`). 0x7902 is then never sent. K1 cannot see this, because its ring is empty after the decline.
- **The plant.** `acmp_owed_mutants.py:114-118`, `acmp-redelivery-past-a-decline`, rewrites exactly the `acmp_mbx.c:166` loop guard without `&& m->kept.len == 0u`.
- **Reviewer probe** (`probe_k8.py`, `receipts/probe_k8.log`). It drives the repository's own arm and campaign machinery; builds and planted copies are kept in scratch.
  - Clean `acmp` arm: 165 tests passed, K8 OK.
  - Clean `acmpif2` arm: 38 tests passed, K8 OK. The test also passes at two interfaces.
  - The author's plant is caught by K8, by name: "K8 the owed frames, then each command answered once, in arrival order".
  - The two plants on the same loop line still catch theirs: `acmp-redelivery-takes-no-waiting-record` by K4 and `acmp-redelivery-short-of-a-full-ring` by K7.
- **Reviewer-own plants:**
  - `rv-stop-checked-after-take`, the same defect spelled differently: caught by K8.
  - `rv-past-decline-and-drop`, which goes on past a decline but drops later records instead of overwriting: caught by K8 (2 checks).
  - `rv-past-decline-drops-later`, a guard in `on_frame` alone: ESCAPED. It is **equivalent** at the head. `on_frame` never runs with a record kept, because `on_rx_ready` (`acmp_mbx.c:124-128`) and the stop itself prevent it. That escape is the only reason the probe exits rc 1 (`receipts/probe_k8.rc`). It is not a test gap.
- **Campaign count.**
  - The author's clean-clone control campaign, `rtl-fast__firmware-control-mutants__ci_step_9.log`, is stamped with this head and tsn-c-stack `715589c1`.
  - It reads `mutants: 586 of 586 caught` and `test_ctrl_firmware: PASS`, with 586 `[ok] mutant` lines. Line 632 is `[ok] mutant acmp-redelivery-past-a-decline (acmp): 1 check(s) failed`.
  - My probe loads a mutant table of 586 at the head.
  - The delta adds exactly one `Mutant(` entry and removes none, so the count rises from 585 to 586.

### (2) F2: builder leg 0 on the pinned RV32 SDK. CLOSED

- **The SDK verification.** `round3/builder-legs/sdk-verify-only.log` (rc 0) names:
  - archive sha256 `d42680e9…b78f`, release `riscv32-ilp32d--glibc--stable-2025.08-1`;
  - installer sha256 `ffcc5433…f1e7cb4`.
- **Matches the head.** These equal `scripts/ci_rv32_sdk.py:24-25` and the file's own sha256 at the head (`ffcc5433…`). They also equal the cache key in `rtl-fast.yml:922`.
- **The run setup.** `gate-tools/leg0_pinned.sh` sets HOME to the SDK's parent. Gate 1b's compiler is home-relative (`test_builder.py:4773`), so it resolves to the pinned SDK.
- **The leg 0 log** (`builder_leg0.log`):
  - Line 1 is stamped with the head.
  - Line 4: `[gate 1b] compiler argv[0]=<pinned-rv32-sdk>/bin/riscv32-linux-gcc version=riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`.
  - It ends `ALL GATES PASS`. The rc is 0, the tree is clean after, and `builder-leg0.json` names this head and tree.
- **The superseded round-2 legs.** They named `(Buildroot 2026.05)`, and the PR body now says so.
- **Leg 1** is unchanged from round 2: all gates but gate 11, which needs a placed build's report.
  - Its two `disabled-writer … console cases; FAIL` lines also appear in round 2's leg 1 log.
  - The delta does not touch them.

### (3) Residue wording. CLOSED

- **R830-2 RES2 / R829-2 RES1.** Live PR body line 47 carries R830-2's exact text: "grows by 152 B with one interface and by 144 B with two … the round-2 redelivery adds 8 B at the two-interface points".
- **R830-2 RES3 / R829-2 RES2.** `MAILBOX_SPLIT.md:582-583` carries the exact fix.
  - The fix is true to the core: `acmp.c:1139` asks `room(a, OWED_BY_BIND)` for a BIND_RX, with `OWED_BY_BIND 2u` at `acmp.c:75`, and `room` is `owed_count + frames <= ACMP_OWED_MAX` at `:352`.
  - So a BIND_RX is declined with fewer than two slots free, and any other listener command at all eight owed.
- **R829-2 RES3.** `SPLIT_CONTROL_MEMORY.md:309` carries the exact fix. The field is `struct acmp_mbx.loop`, at `acmp_mbx.h:227`.

### (4) The `LITEX_SIM_TIMEOUT=3600` override on `elaborate-gates-1`. HONEST; it hides no failure

- **It is the runner's own setting.** `scripts/run_litex_sims.sh:73` documents it, `:110` defaults it to 900, and `:200` applies it with `timeout -k 10 "$TMO"`.
  - Exit 92 means "KILLED BY THE WALL CLOCK - result UNKNOWN … re-run it uncontended" (`:67-68`).
- **Where it is set.** `gate-tools/run_wf_tmo.py:83-86` sets the variable alone and names it in every step log's header.
  - Among the 110 head step logs, the `env override` header appears only in the 7 steps of `elaborate-gates-1`. That job is the only one the `drive_tmo.sh` driver ran.
- **Attempt 1** (900 s): 7 PASS and `test_soc_timing_cuts` TIMEOUT; `failed: 0`, rc 92.
- **Attempt 2** (900 s): 6 PASS and 2 TIMEOUT (`test_retained_cdc_storage`, `test_soc_timing_cuts`); `failed: 0`, rc 92.
- **Attempt 3** (3600 s): 7 FAIL, each on `No space left on device` (run_litex_sims.sh line 200 writing its log, and an `OSError` writing the rc). This is a host fault, not a test result, and it is disclosed.
- **Attempt 4** (3600 s): `simulations: 8 passed: 8 failed: 0 skipped: 0 timed out: 0`, rc 0. Every other step of the job is rc 0.
- **No failure hidden.** No 900 s attempt reported a FAIL. `test_ctrl_memory`, the member that reads `SPLIT_CONTROL_MEMORY.md` (`sw/litex/test_ctrl_memory.py:103`), passed at 900 s in attempts 1 and 2 and again in attempt 4.
- **Limit.** `test_soc_timing_cuts` has no pass under the default 900 s at this head on this host. It reads none of the delta's files. The hosted `elaborate` run under its default clock is the manager's.

### (5) The 40 steps reused from `bfe7a9d6`. Reuse sound; the claim is one step too strong (RES1)

- **What was reused.** `verify-combined.txt` gives 110 rc 0 at the head and 40 rc 0 at `bfe7a9d6`, from:
  - rtl-fast's `verilator-lint`, `yosys-tool`, `yosys-elaboration`, `split-cdc` and `publication-census`;
  - `rtl.yml`'s `full-ci-gate`, `yosys-shards` 0 to 3 and `yosys-tool`.
- **The receipts.**
  - All 110 head rc files are 0, and every head log carries the head stamp.
  - All 40 reused rc files under `round2/gates-bfe7a9d6` are 0.
- **What those steps read.** Most read RTL and syn inputs only: `lint_rtl.py`, `pp_srcs.py`, `syn/yosys/run.sh`, `syn/ooc/*`, `make -C tb/verilator/milan_dp split-cdc`, and `publication_census.py`, which loads the datapath and its includes.
- **The exception.** `rtl.yml/full-ci-gate` runs `scripts/ci_scope.py --selftest`.
  - That selftest scans every `.py`, `.sh`, `.mk` and Makefile under `tests tb syn sw hdl avdecc` for documentation-path spellings (`ci_scope.py:89-91`, `:163`).
  - So it does read `sw/firmware/ctrl/test/acmp_owed_mutants.py`.
- **Re-run at the head.** The plant's added lines carry no documentation path. I re-ran the gate's two content checks at the head, as the workflow runs them:
  - `ci_scope.py --selftest`: `selftest: PASS`, rc 0 (`receipts/ci_scope_selftest_head.log`).
  - `ci_events.py --check`: `ci_events: OK (2271 contract item(s) …)`, rc 0 (`receipts/ci_events_check_head.log`).
- **Result.** No evidence gap remains. The PR-body sentence is recorded as RES1.

## Findings

### RES1: RESIDUE (Docs). PR body gate paragraph and gate table, live lines 138 and 142

- **Text:** "this round's delta (two firmware test files and two design pages) reaches none of them", and in the REVIEW READY comment "None of them reads this delta's four files".
- **Evidence:** `rtl.yml/full-ci-gate`'s `ci_scope.py --selftest` reads `acmp_owed_mutants.py` (`ci_scope.py:89-91`). It passes at the head when re-run (`receipts/ci_scope_selftest_head.log`).
- **Impact:** wording only. No count, figure or rc changes, and the step is now proven at the head.
- **Exact fix:** after "reaches none of them" add: "except `rtl.yml`'s `full-ci-gate`, whose `ci_scope.py --selftest` scans every Python file under `sw/` for a documentation path; the new plant adds none, and that step passes at the head".

### RES2: RESIDUE (Docs). `tb/verilator/ctrl_service_budget/scenario.py:312`, docstring "ACMP's rows (MAILBOX_SPLIT.md:649-661)"

- **Evidence:** the delta adds one net line at `MAILBOX_SPLIT.md:583`, so the "ACMP service latency" heading moves from 649 to 650 and its table from 658-670 to 659-671.
- **Pre-existing drift:** the other line anchors in that directory into the page (`:499-506`, `:506`, `:757-762` in `scenario.py`, `grade.py` and `build.py`) were already off at `bfe7a9d6`. That is not this delta's doing; only the shifted 649 start is.
- **Impact:** comment only.
- **Exact fix:** "ACMP's rows (MAILBOX_SPLIT.md, section ACMP service latency)". Or `MAILBOX_SPLIT.md:650-671` if line anchors are kept.

### RES3: RESIDUE (Docs). PR body line 61, "Every RV32 build in this PR's figures and gates used the pinned SDK"

- **Evidence:** the same paragraph then says that round 2's builder legs ran the Buildroot 2026.05 build. Those legs are superseded, so the sentence is true of the current evidence, but its first words read as all-time.
- **Exact fix:** "Every RV32 build in this PR's figures, and in its gates at this head, used the pinned SDK".

### S1: SUGGESTION (Tests). K8, `test_acmp_mbx.cpp:1442-1458`

- K8 pins the order and the counts, but not each answer's pass (n+1, n+2, n+3 after the room returns), interface, or `GET_RX_STATE_RESPONSE`/SUCCESS status. K1 pins all of these at `:1214-1222`.
- Adding them would hold the bound `acmp_mbx.h` states for a command kept behind another kept one.

### S2: SUGGESTION (Docs/Tests). `acmp_mbx.c:111-120`

- The invariant "`on_frame` never runs while a record is kept" is what makes the reviewer plant `rv-past-decline-drops-later` equivalent. It is held jointly by `on_rx_ready` and the redelivery's stop.
- One clause in the THE KEPT COMMAND comment, or a debug assertion, would make the overwrite impossible to reintroduce silently from a third caller.

### S3: SUGGESTION. Prior-round suggestions retained, not re-examined except where noted

The delta does not change their scope.

- **R830-2 S1 = R829-2 S3:** the empty-kept guard at `acmp_mbx.c:159`. K8 adds no `rx_malformed` assertion, so it still applies.
- **R830-2 S2:** an only-answered BIND_RX between the commands of K4.
- **R830-2 S3 = R829-2 S1:** `__lshrdi3` in the `rv32` arm.
- **R830-2 S4:** a `ctrl_loop.h` item-3 clause.
- **R830-2 S6:** S2b's `may_drop`.
- **R829-2 S2:** equivalent; no test owed.
- **R830-2 S5:** taken in the receipts. `round2-load/load-split-8x8.txt` lists 0.767 / 0.730 / 0.721, and `acmp-item-split.txt:1` now states that it leaves the kept record's direct `acmp_rx` in.

**Comment rule:** the delta's new source lines name no bench lane label, lane name, review round, reviewer ID or comment ID.
- K8's comment cites tsn-c-stack PORTING "ACMP owed bound".
- "K8" is the file's own test-group label, as K1 to K7 are.

## Prior public findings: resolved or retained at this head

| Prior finding | Status | Evidence at `32b43973` |
|---|---|---|
| R830-2 N1 MINOR (Tests, Robustness) = R829-2 F1 | **CLOSED** | K8 + `acmp-redelivery-past-a-decline`; caught by name in my probe and in the author's 586/586 campaign |
| R829-2 F2 MINOR (Docs): leg 0's compiler | **CLOSED** | `round3/builder-legs/builder_leg0.log:4` names the pinned Buildroot 2021.11 build; SDK verify rc 0 |
| R830-2 RES2 = R829-2 RES1 | **CLOSED** | PR body line 47 |
| R830-2 RES3 = R829-2 RES2 | **CLOSED** | `MAILBOX_SPLIT.md:582-583` |
| R829-2 RES3 | **CLOSED** | `SPLIT_CONTROL_MEMORY.md:309` |
| R830-2 S1 to S4, S6; R829-2 S1 to S3 | retained (optional) | S3 above |
| R830-2 S5 | taken (receipts) | S3 above |

## Lens coverage

| Lens | Result | Artifact examined at `32b43973` | What was checked, against what |
|---|---|---|---|
| Conformance | PASS | `acmp_mbx.c:157-175`; `test_acmp_mbx.cpp:1427-1460`; `acmp.c:75,350-352,1139`; ruling 6814546620 | Ruling item 1 (test + plant + 586) and item 2 (leg 0 on pinned SDK) met. The redelivery still meets tsn-c-stack PORTING's "until `acmp_rx` declines one", now with a test that fails without the stop. The BIND_RX wording is true to `room(OWED_BY_BIND)`. |
| RTL | PASS | `git diff --stat bfe7a9d6..32b43973 -- hdl sw/firmware/ctrl/acmp third_party tb syn sw/litex scripts .github` (empty); `receipts/integrity.txt` gitlinks; `round2/gates-bfe7a9d6` 40 rc files | The delta touches no RTL, firmware source or gitlink. The adapter, the core pin and the reused RTL/Yosys/CDC/census steps (rc 0 at `bfe7a9d6`) are unchanged inputs, so the prior RTL verdict holds. |
| Robustness | PASS | K8 (`:1427-1460`); `receipts/probe_k8.log` plants | Invalid-ordering path: a decline during redelivery with records waiting. Caught by K8 in two spellings of the defect and in a drop variant. The one escape is equivalent by the `on_rx_ready` + stop invariant. |
| Tests | PASS | `test_acmp_mbx.cpp:1427-1460`; `acmp_owed_mutants.py:114-118`; author `…firmware-control-mutants__ci_step_9.log:632,1187-1188`; `receipts/probe_k8.log` | K8 passes in `acmp` (165) and `acmpif2` (38) and fails by name on its plant. K4 and K7 still catch their same-line plants. The campaign reads 586/586 on a clean clone, the table is 586 at the head, and exactly one entry was added. |
| Docs | PASS (RES1 to RES3 wording) | `MAILBOX_SPLIT.md:582-585`; `SPLIT_CONTROL_MEMORY.md:309`; live PR body lines 47, 61, 138-147; REVIEW READY 6820785811 | The three ruled wording fixes are in place, exactly. The SDK, override and reuse disclosures were checked against receipts (items 2, 4, 5). Remaining defects are wording-only residue. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `acmp_mbx.c:157-175`, K8, `acmp.c:75,352,1139`, ruling items 1 to 3 | R830-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| RTL | CLEAN | empty RTL/source/gitlink diff `bfe7a9d6..32b43973`; gitlinks in `receipts/integrity.txt`; 40 reused rc 0 | R830-3 (prior RTL verdict carried: inputs unchanged since `bfe7a9d6`) | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| Robustness | CLEAN | K8; probe plants (`receipts/probe_k8.log`) | R830-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| Tests | CLEAN | K8, `acmp_owed_mutants.py:114-118`, author campaign log 586/586, `receipts/probe_k8.log` | R830-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| Docs | CLEAN (RES1 to RES3 to the residue checklist) | `MAILBOX_SPLIT.md:582-585`, `SPLIT_CONTROL_MEMORY.md:309`, PR body, REVIEW READY | R830-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |

## Real limits

- **No source bank run at this head.** I ran no full parent, PP, gPTP, Yosys, builder, Verilator or LiteX bank.
  - What I executed myself: the `acmp` and `acmpif2` arms; a six-plant campaign (three author plants, three of mine); and `ci_scope.py --selftest` and `ci_events.py --check`.
  - Everything else is the author's published receipts at this head, spot-checked: rc files, head stamps, the SDK hash and named log lines.
  - I did not re-run the full 586-mutant campaign. Its count rests on the author's clean-clone log and on my table-size and diff count.
- **No manager source bank** runs at this head. None is claimed or inferred here.
- **The packet has no cryptographic signature.** "Signed" here means the evidence commit `f3fed3c2`, archive "Archive A767 round 3 packet", which is not GPG-signed (`%G?` = N).
  - Its ancestry from the live evidence branch tip is verified.
  - The blob ids of the files I relied on are in `receipts/packet-files.txt`.
- **One LiteX member unproven at 900 s.** `test_soc_timing_cuts` has no pass under the default 900 s clock on this host at this head; it passed only under 3600 s.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Reviewer host differs from CI.** My probes used the host gcc/g++ 16.2.1 and GoogleTest 1.18.0, the same as the author's campaign log, not the hosted Ubuntu toolchain.
- **Other reports.** I did not read the R829-3 report at this head before writing this verdict and ledger.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`), with its builder and native banks. Link those receipts on the PR.
- Own hosted and act acceptance at the exact head, including:
  - `elaborate`'s LiteX aggregate under its default clock;
  - the exact-head `verilator-suites` and `yosys-portability` contexts, telling executed jobs apart from skipped contexts.
- Carry RES1 to RES3 to the residue checklist.
- Track the ruled S2b sequencing (S2b's sync owes the three items of issuecomment-6811790762 item 4) and the merge authorization. Two independent positive reviews are required.

## Receipts (listed in MANIFEST.sha256)

- `probe_k8.py`: the portable probe. Usage: `python3 -I probe_k8.py <repo-root> <work-dir>`.
- `receipts/probe_k8.log`, `receipts/probe_k8.rc`: clean arms and the six-plant campaign. rc 1 comes only from the equivalent plant, as explained above.
- `receipts/ci_scope_selftest_head.log`, `receipts/ci_events_check_head.log`: full-ci-gate's checks at the head.
- `receipts/integrity.txt`: HEAD, tree, index tree, an empty `status --porcelain --ignored`, ls-files/ls-tree digests, gitlinks and clean submodules after the probes.
- `receipts/packet-files.txt`: blob ids of the author packet files examined, and the evidence-branch ancestry.

R830-3 FINISHED
