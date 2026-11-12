[R829] POSITIVE - exact head 32b43973069ee2742f86c4f92adb5eb9ca6bdfb3

# R829-3: internal cleared-context delta review of PR #892 (issue #665), the tsn-c-stack pin move 70936b77 -> 715589c

- **Delta reviewed:** `bfe7a9d6..32b43973`, two commits.
  - `91224a0d` adds test K8 and the plant `acmp-redelivery-past-a-decline`.
  - `32b43973` makes two wording fixes, in `MAILBOX_SPLIT.md` and `SPLIT_CONTROL_MEMORY.md`.
- **Head and base:** tree `4b82e85895812b8094c877becd12cbfdd5f86585`. Source base `1d6bf555`.
- **Previous verdicts at `bfe7a9d6`:** R829-2 NEGATIVE (F1 Tests/Robustness, F2 Docs) and R830-2 NEGATIVE (N1 = F1). Both were MINOR only.
- **Authority for this round:** #665 issuecomment-6814546620 (round-3 ruling), items 1 to 3.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open.
- F1 (= N1) is closed, at its cause. I confirmed it with my own plant run and a second defect variant of my own.
- F2 is closed. Builder leg 0 ran on the pinned SDK at this head.
- Every named prior RESIDUE item is closed.
- Two new RESIDUE items are wording only. One SUGGESTION concerns the evidence packet, not the head.
- All five lenses are covered clean at this exact head.

## What was reconstructed, and from what

- **Contract:** AGENTS.md sections 3 to 8. CONTRIBUTING.md is the one authority over it.
- **Ruling:** #665 issuecomment-6814546620.
  - Item 1: a test in which a redelivered record is declined while another waits behind it, each command answered once in arrival order, with the `acmp_mbx.c:166` stop planted and caught by name. The campaign reads 586.
  - Item 2: re-run builder leg 0 on the pinned RV32 SDK and record its compiler line.
  - Item 3: wording-only residue is taken; suggestions are optional.
- **Interface authority at the pin:** tsn-c-stack `docs/PORTING.md:74-93` ("ACMP owed bound").
  - `:80-82`: all eight owed, or a BIND_RX with fewer than two free slots, is declined.
  - `:88`: the redelivery offers waiting frames "until `acmp_rx` declines one or none is left".
  - `src/acmp.c:75`, `:1139`: `OWED_BY_BIND 2u`; a BIND_RX needs `room(a, 2)`.
- **Code:** `sw/firmware/ctrl/acmp/acmp_mbx.c:108-190` (`on_frame`, `on_rx_ready`, `redeliver`, `on_poll`) and `acmp_mbx.h:227` (`struct ctrl_loop *loop`). Neither changed in this delta: `git diff --quiet bfe7a9d6 HEAD -- sw/firmware/ctrl/acmp` reports no change (`receipts/delta-and-anchors.txt`).
- **Diff and history:** four files, +44 −3.
  - Both commits have one-line subjects with no body and no trailers (`receipts/delta-and-anchors.txt`).
  - The gitlinks are unchanged; tsn-c-stack is at `715589c1`.
- **Author packet:** `review-evidence/tsnpin-r1/author-r3` at archive `f3fed3c2311d37545eeff2ae548b592bdf153cd3`. I fetched it into a scratch bare repository and read it by section: HANDOFF round-3 section, PR-BODY, `receipts/round3/**` (`gates-32b43973/{verify-combined.txt, logs, attempts, drivers}`, `gate-tools`, `builder-legs`), and the round-2 gate-19 logs for comparison.
- **Live PR body:** fetched read-only (`receipts/pr-body-live-at-review.md`). It is the packet's `PR-BODY.md` with one trailing blank line removed (`receipts/pr-body-vs-packet.diff`).
- **Prior public findings:** R829-2 (issuecomment-6814234862) and R830-2 (issuecomment-6814537327). I read them only after my own pass over the diff and receipts. They are resolved below.

## The assignment's checks

### (1) F1: the redelivery's stop at a decline, with a record waiting behind it

**K8** is at `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1427-1460`.
- **Setup:** the owed set is filled, and GET_RX_STATE 0x7901 to 0x7903 are offered on one interface with the egress paused.
- **Before the egress returns,** after 20 passes, it asserts:
  - exactly one decline (`busy_declined == 1`);
  - a kept record;
  - exactly one record taken (`rx_records == taken + 1`).
- **After the egress returns,** over `ACMP_MBX_KEPT_PASSES + 5` (14) passes:
  - the sent sequence must equal the eight owed frames (0x6000 to 0x6007), then 0x7901, 0x7902, 0x7903. Being an exact vector, it allows no duplicate, loss or reordering;
  - `busy_declined == 3`, nothing kept, nothing owed.

**The test matches the trace of the head's code.**
- **Pass 1:** the poll frees one slot. The kept 0x7901 is accepted. 0x7902 is taken and declined (busy 2), kept, and the loop stops on `m->kept.len == 0u`.
- **Pass 2:** 0x7902 is accepted. 0x7903 is declined (busy 3) and kept.
- **Pass 3:** 0x7903 is accepted.
- **Drain:** the 11 frames leave in 11 passes, within the test's 14.
- This is the rule at PORTING.md:88.

**The plant.** `acmp_owed_mutants.py:114-118` drops `&& m->kept.len == 0u` from `acmp_mbx.c:166`. The fixture string matches the head line byte for byte; the campaign's `plant()` refuses anything but exactly one occurrence. The plant names K8 and K8's failing words.

**My own probe** (`scripts/probe_k8.py` → `receipts/probe_k8.txt`, logs in `receipts/probe-logs/`).
- **Method:** the campaign's own `plant()` and arm builders, on copies of the tree. The clone itself is untouched.
- **The head, unmodified:**
  - `acmp` arm: PASS, 165 tests, 0 failures, K8 OK.
  - `acmpif2` arm: PASS, 38 tests, K8 OK.
- **The author's plant `acmp-redelivery-past-a-decline`:**
  - `acmp` rc 1, 1 check failed: `[FAIL] AcmpMailbox.K8ACommandTheRedeliveryDeclinesKeepsItsPlaceAheadOfTheNext: K8 the owed frames, then each command answered once, in arrival order`. `ctrl_mutants.caught()` is True.
  - `acmpif2` fails the same way.
- **My variant `rv-stop-after-take`:** the stop is moved after the take, so the record taken behind a decline is dropped without being offered.
  - K8 fails on both its order check and its "each command declined once, and nothing kept or owed after" check, in both arms.
  - So K8 holds the clause against more than the one spelling planted.

**The campaign on a clean clone.**
- **Log:** `receipts/round3/gates-32b43973/logs/rtl-fast__firmware-control-mutants__ci_step_9.log`.
  - Header: head `32b43973`, clone `<scratch>/gates/wf6/.../wt`.
  - `:632-633`: `[ok] mutant acmp-redelivery-past-a-decline (acmp): 1 check(s) failed`, first `[FAIL] ...K8...`.
  - `:1187`: `mutants: 586 of 586 caught`. The rc file reads 0, and `tree-after.txt` shows an empty status.
- **My own count:** at this head `len(ctrl_mutants.MUTANTS) == 586` and `unnamed_tests() == []`.
- **The other plants on the same loop line:** the author's subset log shows `acmp-redelivery-takes-no-waiting-record` (K4) and `-short-of-a-full-ring` (K7) still caught. The full campaign line covers them too.

**Result: CLOSED.**

### (2) F2: builder leg 0 on the pinned RV32 SDK

- **Driver:** `receipts/round3/gate-tools/leg0_pinned.sh`. It snapshots a clean clone of the head and sets `HOME=<scratch>/sdk/home` with the SDK at `$HOME/br-milan-rv32/host`. That is the path gate 1b looks up (`sw/builder/test_builder.py:4772-4774`, `Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"`). It runs `ci_rv32_sdk.py --verify-only` on that destination in the same script.
- **`builder-legs/sdk-verify-only.log`, rc 0:**
  - `SDK verified` with archive `d42680e9…` and release `riscv32-ilp32d--glibc--stable-2025.08-1`. Both match the pin at `scripts/ci_rv32_sdk.py:24-25`.
  - Version `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`.
- **`builder-legs/builder_leg0.log:4`, rc 0:** `[gate 1b] compiler argv[0]=<pinned-rv32-sdk>/bin/riscv32-linux-gcc version=riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`, then `ALL GATES PASS`.
  - The receipt `builder-leg0.json` names head `32b43973…`, tree `4b82e858…`, leg 0 of 2.
  - `tree-after-leg0.txt` is empty.
- **Leg 1:** rc 0, all gates but gate 11 (placed-build report), as in rounds 1 and 2.
- **The PR body:** the SDK paragraph (live line 61) and the gate table (line 147) now name the build gate 1b used. They also say that round 2's legs used the other GCC 14.3.0 build (Buildroot 2026.05). The remaining over-broad sentence is RESIDUE RES-A below.

**Result: CLOSED.**

### (3) The residue wording

- **R829-2 RES1 = R830-2 RES2** (PR body, round-1 commit row): CLOSED. Live line 47 reads: "`struct ctrl_plat` grows by 152 B with one interface and by 144 B with two, at both shapes (round 1; the round-2 redelivery adds 8 B at the two-interface points)". This is the requested text.
- **R829-2 RES2 = R830-2 RES3:** CLOSED.
  - `docs/design/MAILBOX_SPLIT.md:582-585` reads "A command that arrives with all eight owed, or a BIND_RX that arrives with fewer than two owed slots free, is declined, not dropped: the adapter keeps it and takes no later acmp record".
  - It is correct against PORTING.md:80-82 and `acmp.c:75,1139`.
- **R829-2 RES3:** CLOSED.
  - `docs/design/SPLIT_CONTROL_MEMORY.md:309` reads "the adapter's pointer to the loop it attached to (the redelivery takes records in that loop's buffer)".
  - The member is `acmp_mbx.h:227` (`struct ctrl_loop *loop;`), added in this PR (`git diff 1d6bf555..HEAD -- acmp_mbx.h`).
- **Comment rule:** the delta adds one source comment, `test_acmp_mbx.cpp:1427-1428`.
  - It states the behaviour and cites tsn-c-stack PORTING "ACMP owed bound", which exists at `docs/PORTING.md:74`.
  - It names no bench lane, lane name, review round, reviewer ID or comment ID. A grep of the added lines for such tokens has no hits.

### (4) `LITEX_SIM_TIMEOUT=3600` on `elaborate-gates-1`

- **It is a real runner setting.** `scripts/run_litex_sims.sh:73` documents "LITEX_SIM_TIMEOUT per-script wall clock in seconds (default 900)", and `:110` is `TMO="${LITEX_SIM_TIMEOUT:-900}"`. No workflow sets it, so hosted runs use 900 s.
- **It was used only for that job.**
  - `gate-tools/run_wf_tmo.py:83-86` is the only override, with its reason, written at the top of every step log of the job.
  - `drive_tmo.sh` runs that driver.
  - Of the logs at head, only the seven `elaborate__elaborate-gates-1__*` logs carry the override header.
  - Within that job only `run_litex_sims.sh` (gate 19) reads the variable.
- **It hides no failure.** `drivers/restarts.log` and the attempt logs show:
  - **Attempt 1:** rc 92, `simulations: 8 passed: 7 failed: 0 ... timed out: 1`. Only `test_soc_timing_cuts` was killed by the 900 s clock ("result UNKNOWN, not a failure").
  - **Attempt 2:** rc 92, 6 passed, 0 failed, 2 timed out (`test_retained_cdc_storage`, `test_soc_timing_cuts`).
  - **Attempt 3** (override): 1 passed, 7 failed.
    - Six of the failures carry `No space left on device` lines in the aggregate.
    - `test_ctrl_memory`'s own log ends `[FAIL] the planted ledgers arm raised OSError: [Errno 28] No space left on device` after every earlier check `[ok]`.
    - So all seven are disk-full, not test results.
  - **Attempt 4** (override, fresh clone): gate 19 rc 0, `simulations: 8 passed: 8 failed: 0 skipped: 0 timed out: 0`. Every other step of the job is rc 0.
- **No member that ran to completion ever failed for a test reason.** `test_ctrl_memory`, the member that reads `SPLIT_CONTROL_MEMORY.md`, passed at the default 900 s in attempts 1 and 2.
- **At `bfe7a9d6` and `8ffcf2fc`,** gate 19 passed 8/8 with no override (`round2/gates-*/logs/elaborate__elaborate-gates-1__gate_19.log`).
- **No timed-out member reads this delta's files.**
- **Conclusion:** the override is an honest, disclosed, job-scoped runner setting, and it is local evidence only. The hosted 900 s run remains the manager's to accept.

### (5) The 40 reused steps from `bfe7a9d6`

- **The reused jobs** (`verify-combined.txt`):
  - rtl-fast `verilator-lint`, `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc`;
  - rtl.yml `full-ci-gate`, `yosys-shards-{0..3}-4`, `yosys-tool`.
- **What their `run:` steps invoke:**
  - `lint_rtl.py`, `pp_srcs.py`;
  - `syn/yosys/run.sh` and the `syn/ooc`/`syn/yosys` selftests;
  - `sw/mailbox/publication_census.py`;
  - `make -C tb/verilator/milan_dp split-cdc`;
  - the yosys shards;
  - and in `full-ci-gate`, `ci_events.py --check` and `ci_scope.py --selftest`.
- **Content readers of the delta's files:** `git grep` over the repository finds no reader of `test_acmp_mbx.cpp` or `acmp_owed_mutants.py` among those inputs. It finds no content reader of either page either: `mailbox_emit.py:244` only emits a link, and the `hdl/` hits are comments.
- **One exception.** `rtl.yml/full-ci-gate` runs `python3 scripts/ci_scope.py --selftest` (`rtl.yml:85`). That selftest's `gated_files()` scans every tracked `.py` under `sw/` (`ci_scope.py:89-90,152-166`), and `acmp_owed_mutants.py`, changed here, is one of them. So the claim "none reads the four files" is not literally true for that one step.
- **The evidence has no gap.** The same command ran at this head, rc 0:
  - in rtl-fast `changes` (`rtl-fast.yml:48`; `logs/rtl-fast__changes__scope.log`, rc 0);
  - in elaborate's scope steps (`elaborate.yml:60,295`; `elaborate__elaborate-gates-{0,1}__scope`).
- **The scope decision is the same at both heads.** The step's own scope decision reads the changed-file list, not the files' contents. It is `rtl=true` either way, because `sw/` paths were already in `1d6bf555..bfe7a9d6`.
- **Classification:** a wording inaccuracy only, RESIDUE RES-B below.

## Findings

### RES-A — RESIDUE — Docs — live PR body line 61 (the SDK paragraph)

- **Problem:** the paragraph opens "Every RV32 build in this PR's figures and gates used the pinned SDK". Three sentences later it says round 2's builder legs ran the other GCC 14.3.0 build (Buildroot 2026.05). The disclosure is present and the claim at this head is true. Only the opening sentence is broader than the facts.
- **Exact fix:** "Every RV32 build in this PR's figures, and every gate at `32b43973`, used the pinned SDK, …".
- **Optional, same line and line 147:** "HOME at the pinned SDK's parent" → "HOME at the directory holding `br-milan-rv32/host`, the pinned SDK's install".

### RES-B — RESIDUE — Docs — live PR body lines 16 and 138; HANDOFF.md:57 (the reused-step claim)

- **Problem:** the text says the 40 reused steps' inputs are not touched, or that no reused step reads the four files ("whose inputs this round does not touch", "reaches none of them", "None reads the four files of this delta"). But rtl.yml `full-ci-gate`'s `ci_scope.py --selftest` scans every `.py` under `sw/`, `acmp_owed_mutants.py` included.
- **Why it is only wording:** the same selftest ran at the head, rc 0, in rtl-fast `changes` and in elaborate's scope steps. No result, gate or claim of correctness changes.
- **Exact fix:** after "taken from `bfe7a9d6`" (line 16) and after "reaches none of them" (line 138) add "; the one reused step that scans a changed file, `full-ci-gate`'s `ci_scope.py --selftest` (every `.py` under `sw/`), is the same command that ran at the head in rtl-fast `changes` and in elaborate's scope steps". Make the same change to HANDOFF.md:57.

### S-1 — SUGGESTION — evidence packet (not the head; no lens) — `author-r3/receipts/INDEX.md`

- **What I found:** `scripts/verify_index.py` → `receipts/verify_index.txt`. Of 2,035 rows, 1,900 match.
  - **21 rows mismatch.** All 21 are exactly the files that carry the `<home-path>` placeholder. Their sizes differ by 6 to 16 bytes. So a host-path redaction ran after the index was generated.
  - **114 rows are missing.** All of them are files inside the two withheld transient repository copies (`attempts/attempt2/.../tmp/retained-cdc-control-*`). Each copy is noted in place by an unlisted `*.WITHHELD.txt`.
- **Impact:** none on any claim. I read the receipts behind each claim directly. But a cold reviewer checking the index would see 135 failures.
- **Suggestion:** regenerate INDEX.md after the final redaction, and list the withheld paths as withheld, not by hash.

### Suggestions retained from prior rounds (optional; ruling item 3 leaves them untaken, no tree change)

- R829-2 S1 = R830-2 S3: `__lshrdi3` refusal in the portable `rv32` arm.
- R829-2 S2: `rv-bad-continues`, equivalent, needs no test.
- R829-2 S3 = R830-2 S1: the `acmp_mbx.c:159` guard; assert `rx_malformed` unchanged.
- R830-2 S2: a K4 variant with an only-answered BIND_RX.
- R830-2 S4: a `ctrl_loop.h` item-3 clause.
- R830-2 S6: the `may_drop` allowance, which is S2b's.
- R830-2 S5 is taken in the receipts:
  - `round2-load/load-split-8x8.txt` states 0.767, 0.730 and 0.721 with their item terms;
  - `acmp-item-split.txt:1` now says its measure leaves the kept record's direct `acmp_rx` in.

## Prior public findings: resolved at this head

| Item | State at `32b43973` | Evidence |
|---|---|---|
| R829-2 F1 MINOR Tests, Robustness (= R830-2 N1): the stop at a decline untested | **CLOSED** | K8 `test_acmp_mbx.cpp:1427-1460`; plant `acmp_owed_mutants.py:114-118`, same edit as R829-2's `rv-continue-after-decline` and R830-2's patch; caught by name in the clean-clone campaign (586/586) and in my probe, in both arms; a second variant of mine also caught (check 1) |
| R829-2 F2 MINOR Docs: builder leg 0 not on the pinned SDK | **CLOSED** | `builder_leg0.log:4` names Buildroot 2021.11-18033-g83947c7bb6; `sdk-verify-only.rc` 0 on that destination; PR body states round 2's build (check 2); wording remainder is RES-A |
| R829-2 RES1 = R830-2 RES2 | **CLOSED** | live PR body line 47 |
| R829-2 RES2 = R830-2 RES3 | **CLOSED** | `MAILBOX_SPLIT.md:582-585` |
| R829-2 RES3 | **CLOSED** | `SPLIT_CONTROL_MEMORY.md:309` |
| R829-2 S1–S3, R830-2 S1–S4, S6 | optional, retained | above |
| R830-2 S5 | taken (receipts only) | `round2-load/load-split-8x8.txt`, `acmp-item-split.txt:1` |
| Earlier rounds' items (R829-1, R830-1) | closed at `bfe7a9d6` by R829-2 and R830-2; nothing they rest on is touched by this delta | `acmp_mbx.c`/`.h`, the S2 harness and the ledgers are unchanged since `bfe7a9d6` |

## Lens results (all five applied at the exact head)

```text
[R829] PASS Conformance — docs/design/MAILBOX_SPLIT.md:582-585; test_acmp_mbx.cpp:1427-1460; acmp_mbx.c:157-175 — the new kept-command clause checked against tsn-c-stack PORTING.md:80-82,88 and acmp.c:75,1139 (BIND_RX needs two slots); K8's expected order and decline counts traced against PORTING.md:88's redelivery rule on the unchanged code; no protocol behaviour changed in the delta
[R829] PASS RTL — git diff bfe7a9d6..32b43973 (4 files: 2 firmware test files, 2 design pages; no hdl/, firmware source, gitlink or build change) and acmp_mbx.c:166 unchanged — no RTL, firmware source or interface contract in scope of the delta; the RTL verdict at bfe7a9d6 depends on nothing the delta changed
[R829] PASS Robustness — test_acmp_mbx.cpp:1427-1460 and receipts/probe_k8.txt — the ordering and backpressure case (a decline at the redelivery with a record waiting) is now pinned; both the planted removal and the reviewer's stop-after-take variant lose or reorder a command and are caught, in the 1-interface and 2-interface arms
[R829] PASS Tests — acmp_owed_mutants.py:114-118; gates-32b43973/logs/rtl-fast__firmware-control-mutants__ci_step_9.log:632-633,1187; receipts/probe_k8.txt — K8 passes on the head (165 and 38 tests, 0 failures) and fails by name on its plant; campaign 586 of 586 on a clean clone, with 586 entries and no unnamed test counted at the head; fw_coverage acmp_mbx.c 106/106 lines, 42/42 branches (firmware-unit log at head)
[R829] PASS Docs — MAILBOX_SPLIT.md:582-585; SPLIT_CONTROL_MEMORY.md:309; test_acmp_mbx.cpp:1427-1428 comment; live PR body (receipts/pr-body-live-at-review.md) lines 16, 47, 61, 138, 147 — the prior residue is closed with the given text; the new comment obeys the comment rule; RES-A and RES-B are wording only and carried as residue
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `MAILBOX_SPLIT.md:582-585`, `test_acmp_mbx.cpp:1427-1460`, `acmp_mbx.c:157-190` against tsn-c-stack `PORTING.md:74-93`, `acmp.c:75,1139` | R829-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| RTL | CLEAN | the delta's file list (no RTL or firmware source); `acmp_mbx.c`/`.h` unchanged since `bfe7a9d6`; gitlinks unchanged | R829-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| Robustness | CLEAN | K8; the plant and the reviewer variant in `acmp` and `acmpif2` (`receipts/probe_k8.txt`) | R829-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| Tests | CLEAN | K8; `acmp_owed_mutants.py:114-118`; head campaign log (586/586); firmware-unit and coverage receipts at head; table count at head | R829-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |
| Docs | CLEAN (RES-A, RES-B carried as residue) | the two design pages; the new comment; live PR body; HANDOFF round-3 section | R829-3 | `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` |

## Probes and receipts (listed in MANIFEST.sha256)

- **`scripts/probe_k8.py`** → `receipts/probe_k8.txt`, `receipts/probe-logs/*.log`.
  - It runs the clean `acmp`/`acmpif2` arms, then the author's plant and `rv-stop-after-take`, on campaign copies.
  - About 4.7 min of wall time, compile jobs 4.
- **`scripts/verify_index.py`** → `receipts/verify_index.txt` (the packet INDEX check, S-1).
- **`receipts/delta-and-anchors.txt`:** the delta stat, the raw commit messages, and the code and authority anchor lines quoted above.
- **`receipts/pr-body-live-at-review.md`** and **`receipts/pr-body-vs-packet.diff`:** the live PR body as read, and its difference from the packet copy.
- **`receipts/hosted-at-head.txt`:** at review time (2026-11-12T10:28Z) the head had 0 check-runs, 0 workflow runs and 0 status contexts. So this round inspected no hosted execution at the head.
- **`receipts/clone-restore-check.txt`** shows the clone after the probes:
  - HEAD `32b43973…`, tree `4b82e858…`;
  - empty status, including ignored and untracked files;
  - index equal to HEAD and the worktree equal to the index;
  - every gitlink at its recorded commit, and every submodule worktree clean.
- **What the probes touched:** they wrote only under the packet's `scratch/`, and Python ran with `-B`.

## Real limits

- No manager source bank runs at this head. Source execution evidence is the author's published receipts, which I verified by section, plus my own focused probes. I claim no source bank, and I infer none.
- I did not re-run the full control campaign, the builder legs, gate 19 or any LiteX simulation myself. Those rest on the author's clean-clone receipts, which I checked for head stamp, rc, tree state and content.
- I did not inspect the `behave` (508 scenarios) receipt; its log is over the packet's 200 KB limit and was not copied.
- The `elaborate-gates-1` evidence at this head ran with `LITEX_SIM_TIMEOUT=3600`. It shows no completion within the hosted 900 s clock under load, although `bfe7a9d6` passed at 900 s.
- The exact-head hosted contexts had not started when I looked.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The packet's INDEX is not self-consistent (S-1). I read the cited receipts directly.

## Pending manager duties

- Carry RES-A and RES-B to the residue checklist. Both are PR-body text, plus one HANDOFF line.
- **Hosted/act acceptance at the exact head.** This includes `elaborate-gates-1` gate 19 at the default 900 s, `verilator-suites` and `yosys-portability` after ready, and `rtl-fast` at this head.
- **The current-dev merge candidate** (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`): build and validate it at the merge turn, with the builder and native banks, and link the receipts on the PR.
- **Merge order per the ruling:** S2b merges this head before #810 merges.
- **Still owed elsewhere, not by this PR:**
  - S2b's sync owes the three items of #665 issuecomment-6811790762 item 4;
  - the 0.75 ceiling and nested-receive rule are #890's;
  - 32x32 is S15's.

R829-3 FINISHED
