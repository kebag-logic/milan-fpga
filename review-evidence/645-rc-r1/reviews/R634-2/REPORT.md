[R634] POSITIVE - exact head fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c

# R634-2: internal cleared-context re-review of PR #742 (#645 bind round), round 2

- **Head:** `fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c`, tree `77e1321b1c9684e8899a85710296eb75af7ddf48`, source base `f62602531d415d6c1cae1374a3cc2938faf54049`.
- **Delta reviewed:** `2639eecf..fb5dd3da`, two commits.
  - `e0960932` changes the harness: `sim_main.cpp` constants and comments.
  - `fb5dd3da` changes the docs: `MEDIA_CLOCK_FOLLOWING.md`.
  - `hdl/` is byte-equal to `2639eecf` (`git diff --quiet 2639eecf fb5dd3da -- hdl`). `sim_main.cpp` is identical between the two commits, so every author campaign ran the head harness.
- **Verdict:** POSITIVE.
  - All five lenses were applied and are CLEAN at this head.
  - All prior findings (R634-1-F1, R635-1-F1, R634-1-F2, R634-1-S1) are resolved at their cause.
  - Open items: one RESIDUE (provenance wording) and two SUGGESTIONs. None leaves a lens unclean.
- **Scope of this review:** a source-head review. It is not a manager source bank and not the current-dev merge candidate. Physical calibration was NOT RUN; field skips are not hardware proof.

## What was verified, and how

1. **Author packet integrity.** I read `review-evidence/645-rc-r1/` at `512c59ba`.
   - All 2,828 `MANIFEST.json` entries match their published sha256, and no unlisted file is present.
   - In `author-r2/MANIFEST.sha256`, 28 lines fail. All 28 are path-redacted entries (`receipts/author-packet-verify.txt`, `scripts/verify_manifest.py`).
   - The live PR body equals `author-r2/PR-BODY.md` apart from one trailing newline.

2. **F1, the window, derived independently from B17's summaries.** I wrote my own script and did not reuse the author's.
   - Inputs: `645-b17-review-evidence` at `bdb96b66`, `c01..c10.json`; hashes are in `receipts/inputs.txt`.
   - Upper bound: each slip record's own `tap_lateness_max_us`. There is exactly one listed burst inside every slip interval, at both 5 ms and 50 ms grouping, so taking the minimum over bursts cannot under-bound.
   - Lower bound: the largest listed lateness after the slip interval, minus 1e6/48000 us.
   - Result: window **9.426667 .. 24.565 us, both edges from c05**. The other nine cycles' lower bounds are 6.742 to 9.238 us and their upper bounds 24.968 to 29.309 us, so every cycle contains the window (`receipts/b17_window_independent.txt`).
   - The harness takes the value from its replay table, `sim_main.cpp:180-181`: `kB17[4]` is `{5, 7.854, 0.0938, 24.565, 30.260}` (`:165`). The window test at `:1316-1317` is strict on both edges.
   - The 10 us listing threshold is used as a bound nowhere. "since nothing that late slipped it" is gone from the design, the harness and the PR body, and a tree-wide search for the old bound and counts finds nothing stale.
   - Simulation sanity check of the later-burst argument, on dev's datapath, B17 cycle 5 (`receipts/cycle5_bound_check.txt`):
     - all 36 binds whose head-measured lowest margin is above 9.427 us slip exactly one frame;
     - the no-lateness bind at 9.12 to 9.28 us slips two frames, which B17's cycle 5 did not.
   - This also answers R635-1-F1's cycle-1 counterexample: cycle 1's own bound is 7.858 us, not 9.427 us.

3. **The reclassification and every restated `sweep-bind` count.** I cross-checked independently (`scripts/bind_grid_crosscheck.py`; `receipts/crosscheck-16.txt`, `-32.txt`, `-dense.txt`, `early-detail.txt`).

   **16-phase `sweep-bind`, 320 binds:**
   - Head: 32/32 runs rc 0. 177 binds inside (the 8 that moved are `bind_j5_p05`'s, lowest edge 9.440 us) and 143 outside.
   - The 177 in-window binds all move `SLIP_LB` by +0 with one arm, one settle recentre and one render recentre.
   - On dev's datapath, all 177 slip exactly one frame (+2 dups, one event) at the first burst and nothing else.
   - Outside on dev: 43 slip one frame, 99 two frames and one a frame and a pair (+3).
   - Head early slips: 6, phases 0.8125 and 0.875, 0 to 5 us of lateness, 0.129 to 2.127 ms after the first PDU. All 6 are identical on dev, in kind and time to the microsecond.
   - Head frames slipped after the ring acts: 0.
   - Firing: 2,047.02 to 2,048.02 ticks after the arm. Post-recentre margins: empty side at least 3.479 ticks, full side at least 4.884 (`receipts/fix16-post-recentre-margins.txt`).
   - Dev labels only 171 of the 177 inside, by its own longer measuring interval. The design and the PR body correctly class by the head's labels.

   **32 phases, 0 to 5 us:**
   - In the window, 1 of 151 binds dups one pair: cycle 7, phase 0.84375, 0.127 ms after its first PDU.
   - Out of the window, 19 of 169 binds slip one frame, at phases 0.78125 to 0.875, up to 2.503 ms after the first PDU.
   - All 20 early slips are identical on dev.

   **128 phases of cycle 7, with and without lateness:**
   - In the window, 2 of 140 binds dup one pair: phases 0.890625 and 0.9296875, both with lateness, 0.127 and 0.252 ms after the first PDU.
   - Out of the window, 6 of 116 binds slip, up to 2.877 ms after the first PDU.
   - All 8 early slips are identical on dev.

   **Margins of the binds that slipped early:** every out-of-window slipping bind had a lowest margin of 3.52 us or less. The in-window dups had lowest margins of 19.04, 17.44 and 18.24 us.

   **Falsification reruns at this head.** I built the harness myself with pinned Verilator 5.050 (`receipts/simulator-identity.txt`), on the head and on dev `f6260253`'s datapath (sha256 `553be35d...`, equal to the author's). I reran `fix16/bind_j5_p05`, `fix32/bind_j5_p27` and `base32/bind_j5_p27`. All three are byte-identical to the published logs in every RESULT and slip line, with the same rc (`receipts/spotcheck-compare.txt`, `receipts/runs/`).

4. **F2, the stated limit.**
   - `MEDIA_CLOCK_FOLLOWING.md:1346-1370` states the in-window one-pair dup as pre-existing on dev and not removed by the arm, with incidence, phases and timing exactly as measured above. It restates the out-of-window slips over the 32-phase and dense grids, gives the margins, and links #743.
   - The test-plan row (`:1653`) scopes the no-`SLIP_LB` claim to the leg's and `sweep-bind`'s phases and points finer grids to #743.
   - The PR body's Round 2 and Known-limitations sections say the same.
   - #743 is OPEN. Its 1/141 and 2/132 are the same three dups under the old 10 us classification, and the PR body says so.

5. **S1, the area headline.** The PR body cites `AREA_BUDGET.md:124`: 50,013 LUT, 11,973 over NFR-RES-01's 38,040, and +3 LUT is 0.025 % of that gap. The row is at line 124 at this head and on live dev `65617779`.

6. **Gates.** I reran four at this head, each rc 0: `check_doc_style.py`, `check_doc_paths.py`, `check_cpp_idiom.py` and `git diff --check f6260253 fb5dd3da` (`receipts/gate-*`).
   - `check_em_dash.py` and `gen_toc.py` refuse here because the pinned Markdown renderer is not installed, and installing it is outside my allowance. Instead:
     - the author's receipts show both rc 0 at this head (`author-r2/r2/gates/`);
     - a direct scan of the delta's 62 added lines finds no em or en dash and no non-ASCII character.
   - Author receipts at this head: `follow_ring` default rc 0, 96 checks / 0 failures (b8 48, pullin 18, bind 30), settle control PASS at four rates; `make mutants` 15/15, each control caught by its named check.

7. **Checkout restored.** HEAD and the index tree are `77e1321b`, `git status` is empty, there are no untracked files, and the six gitlinks equal the head tree (`receipts/checkout-integrity.txt`). My builds and runs wrote only under the packet's `scratch/`.

## Prior findings at this head

| Finding | Status at fb5dd3da | Evidence |
|---|---|---|
| R634-1-F1 = R635-1-F1 (10 us lower bound unsupported) | RESOLVED | Supported bound 9.427 us derived in source from cycle 5's row. The 10 us listing threshold is never a bound. Counts restated from a both-datapath rerun and cross-checked above. |
| R634-1-F2 (in-window one-pair dup missing from the limit) | RESOLVED | The limit text, test plan and PR body describe it as pre-existing on dev, not removed by the arm, with incidence and phases. Out-of-window slips restated over 32 and 128 phases. #743 is linked and OPEN. |
| R634-1-S1 (area headline) | RESOLVED | The PR body cites `AREA_BUDGET.md:124`. |

## Findings

### R634-2-R1 RESIDUE (Docs, Conformance): "from its own `c05.json`" omits the read that shows the 30.260 us burst slipped nothing

- **Where:**
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1286-1290`: "(its `c05.json`) ... and the cycle's 30.260 us later burst then slipped nothing".
  - The PR body, "B17's window" paragraph and Round 2: "from its own `c05.json`".
  - `MEDIA_CLOCK_FOLLOWING.md:1277-1278`: "The 10 to 23 later bursts, up to 30.3 us, slipped nothing."
- **Evidence:**
  - Cycle 5's 30.260 us PDU came 37.503 s after its bind, but `c05.json`'s last `SLIP_LB` poll is at 31.837 s. Restricted to bursts its own polls observed, `c05.json` alone supports only 8.490 us.
  - That this burst slipped nothing rests on `c06.json`. Its first read comes 43.883 s after cycle 5's bind and reads 218, equal to cycle 5's last value, and cycle 6's unbind comes later, at 45.864 s.
  - The same holds for cycle 8's 6.742 us bound: its burst came at 37.013 s, and cycle 9's first read is still 224.
  - For cycles 1 to 9, the next cycle's first read covers every listed PDU with `SLIP_LB` unchanged. Cycle 10's 43 PDUs after its last poll (peak 26.298 us) have no following read in the summaries.
  - Receipts: `receipts/b17_later_burst_observed.txt`, `receipts/b17_poll_continuity.txt`.
- **Why RESIDUE:**
  - Every bound and count is unchanged and verified: 9.427 us still holds with the cross-cycle read.
  - The harness takes no file citation, and no code, test or classification changes.
  - Only the evidence attribution in prose is incomplete.
- **Exact fix:**
  - In the design and the PR body, replace "(its `c05.json`)" / "from its own `c05.json`" with "(its `c05.json`, with `c06.json`'s first `SLIP_LB` read, 218 and unchanged, 43.9 s after cycle 5's bind; the 30.260 us burst came at 37.5 s, after cycle 5's last poll)".
  - At `:1278`, change "slipped nothing" to "slipped nothing through each cycle's last poll and, for cycles 1 to 9, the next cycle's first read".
- **Verification:** the text matches `receipts/b17_poll_continuity.txt`.

### R634-2-S1 SUGGESTION (Tests): make the published bound script check its premise

`author-r2/r2/b17_bound.py` assumes that "every burst after the slip interval ... slipped nothing" without checking that a `SLIP_LB` read covers it. It also groups bursts at 5 ms, giving 10 to 22 later bursts, while the design's "10 to 23" follows B17's 0.2 ms rule.

Optional: add the poll-coverage and next-cycle continuity check (as `scripts/b17_poll_continuity.py` does), and state the grouping. No figure changes.

### R634-2-S2 SUGGESTION (Docs): restore the #640 budget comparison in the PR body

Item 3 of the design round asks for the area delta "against NFR-RES-01 and the #640 budget". The PR body's Area bullet gives only NFR-RES-01. The round-1 REVIEW READY gave 0.05 % of the #640 plan's 6,373-LUT margin (`AREA_BUDGET.md:328`; 3/6,373 = 0.047 %).

Optional: add that clause. The measurement itself is public and unchanged.

## Reviewer ledger (round R634-2)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (R1 is RESIDUE) | Issue #645 acceptance; design round 6187595500; round 2 assignment 6193474559 items 1 to 3; B17 `c01..c10.json` at `bdb96b66` with an independent derivation (`receipts/b17_window_independent.txt`, `b17_poll_continuity.txt`); `sim_main.cpp:56-68`, `:160-181`, `:1316-1317`, `:1343-1372`; `MEDIA_CLOCK_FOLLOWING.md:1264-1370`, `:1653`; PR body | R634-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| RTL | CLEAN | `hdl/` byte-equal to `2639eecf` (R634-1 RTL CLEAN; R635-1 PASS RTL at `2639eecf`; nothing in scope changed since). Head and dev-datapath harnesses built here from `hdl/milan/milan_datapath.sv` and `f6260253`'s copy; reruns identical to published logs (`receipts/spotcheck-compare.txt`) | R634-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| Robustness | CLEAN | Window edges: 9.440 us binds hold on the head; dev's cycle-5 behaviour either side of 9.427 us (`receipts/cycle5_bound_check.txt`); the arming-window residual at 16, 32 and 128 phases on both datapaths (`receipts/crosscheck-*.txt`, `early-detail.txt`), now stated as pre-existing and owned by #743; 0 slips after the ring acts across 896 head binds | R634-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| Tests | CLEAN | `sim_main.cpp` diff (constexpr derivation from `kB17[4]`, strict window test, `--any-phase` grading at `:1363-1368`); author campaigns `fix16/base16/fix32/base32/fixdense/basedense` cross-checked; three reruns byte-identical; author `fr_default` 96/0 and `fr_mutants` 15/15 at this head | R634-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |
| Docs | CLEAN (R1 is RESIDUE; S2 optional) | `MEDIA_CLOCK_FOLLOWING.md:1273-1370`, `:1653`; `TESTING.md:347`, `:624` (unchanged, still accurate); `TIME_SYNC.md:386`; PR body (equal to `author-r2/PR-BODY.md`); `AREA_BUDGET.md:124`; gates in `receipts/gate-*` and the author's `r2/gates` | R634-2 | fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c |

## Real limits of this review

- **Spot reruns only.** I reran 3 of the 640 published head and dev runs, plus two builds. The rest are the author's published receipts, which I cross-checked by parsing, not by re-execution.
- **Suites not re-executed.** The `follow_ring` default and `make mutants` are author receipts at this head. The other suites, lint, xvlog, Yosys, the builder and area were not rerun by anyone in round 2: the RTL is unchanged and their round-1 receipts stand.
- **Two gates not run here.** `check_em_dash.py` and `gen_toc.py` could not run in this environment (renderer not installed). I rely on the author's rc 0 receipts plus my direct scan of the added lines.
- **Simulation only.** B17's bounds are inferences from 0.5 s polls and a >10 us listing. The window is a bench-derived modelling bound, not a measured margin. Physical calibration and the bench repeat were NOT RUN.
- **The dup stays in the tree.** The in-window one-pair dup is pre-existing on dev and is not fixed by this PR. It is owned by #743, as ruled in 6193474559, and this review did not investigate its mechanism.
- **Hosted checks were still running.** At my snapshot (`receipts/hosted-checks-snapshot.tsv`), the exact-head checks were 13 completed/success, 1 skipped and 13 in progress. This is not hosted acceptance.

## Pending manager duties

- Carry R634-2-R1 to the residue checklist (design text and PR body wording).
- Exact-head hosted acceptance: `rtl-fast`, `verilator-suites`, `yosys-portability`, and the projected `follow_ring` wall clock against the hosted window.
- The current-dev merge-candidate validation, with builder and native banks, against live dev `65617779018f41d7e55d1b1ac189ef882bff6367`.
- The external re-review (R635-2).
- Merge only with explicit maintainer authorization.
- After the merge: the B17 bench repeat, which is #645's acceptance. Read any `SLIP_LB` +1 dup within a bind's first 42.7 ms against #743.

R634-2 FINISHED
