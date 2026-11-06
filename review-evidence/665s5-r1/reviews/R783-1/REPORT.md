[R783] NEGATIVE - exact head eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65

# R783-1: issue #665 lane S5 / PR #844, internal cleared-context review

- **Head:** `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65`, tree `883f71864feecfd59543c9c94e5c4f6835019238`. The diff runs from `5b5f4336` (dev-soft-core at the branch point) and has 8 one-line commits with no trailers.
- **Delta:** the new `tb/verilator/ctrl_service_hooks/` (README, `hooks.py`, `hooks_build.py`, `hooks_selftest.py`, `hooks_soc.py`, `run.py`) and one entry in `sw/firmware/ctrl/test/ctrl_configs.py`. No `hdl/` file, no firmware source, and no file of the CPU budget harness or the split boot harness is touched.
- **Verdict:** NEGATIVE. Two MINOR findings are open, F1 (Tests) and F2 (Conformance). Neither one changes a published figure.
- **The measurement is sound.** Every figure in the README matches the published receipts. 52 rows were re-measured in the reviewer's own builds, and every one matches cycle for cycle.
- **Counts:** two RESIDUE items (comment rule) and six SUGGESTIONs.

## Reconstruction (public state only)

- **Workflow:** AGENTS.md, CONTRIBUTING.md (one-line commits, PR template, "self-test results go in a PR comment").
- **Scope:** issue #665. The lane assignment is issuecomment-6513150371 and the executor's takeover comment is 6513247351.
- **Bound:** ruling 6495692075. T_svc is 20 ms. The bound is min(T_svc, the family's 10 % ceiling): 18 ms for SRP and 20 ms for every other family.
- **Clock:** owner decision 6514866239. The split CPU runs at 100 MHz on `sys`. The Milan clock is unchanged. S5 grades at the product clock, and its 50 MHz figures become history.
- **Other rulings:**
  - 6634982529: item 1 is the composed burst in the SRP row's scope; item 2 is the 6,490-cycle layout swing.
  - 6630265194: the retried notice is S2b's.
  - 6674728988: S2b round 17.
  - 6505997821: 59.0 RAMB36 at the ledgered 8x8 point.
  - 6508196970: the earlier clock correction.
- **Requirements:** FR_NFR.md 3.4.1 and 3.4.2 (all eight hook rows) and NFR-SCOUT-03.
- **Interfaces read:**
  - `hdl/milan/mailbox/KL_mbx.sv` (face-window accept and timeout) and `KL_mbx_rx.sv` (token buckets);
  - `sw/litex/milan_soc.py` (CPU clock wiring);
  - `tb/verilator/ctrl_service_budget/{split_soc,grade,scenario,build}.py`;
  - `sw/firmware/ctrl_nvm/test/nvm_bench.py` (`CONFIG_CLOCK_FREQUENCY`).
- **PR #844 body.** Prior public review findings on #844: none. At this head the PR carries only the two review-start comments, so no earlier finding needs to be resolved or kept.
- **Public evidence:** `review-evidence/665s5-r1` at `c30339bc`: receipts for the runs, plants, history, merge and gates.

## Findings

### F1: MINOR (Tests). The `counters-late` plant cannot fail: unplanted, its catch rule already matches

- **Where:**
  - `tb/verilator/ctrl_service_hooks/run.py:300-305`, the plant verdict. A plant counts as caught when *any* finding of its group starts with its words.
  - `hooks.py:203-206`, the `counters-late` plant, which runs in group `hooks-counters` with the words `LATE H-COUNTERS`.
- **Authority:** AGENTS.md section 6 Tests ("Each new test can fail for the defect it claims to detect"). Assignment item 5: "Each hook gets a planted late service and a planted ordering defect, and each must fail."
- **Evidence:**
  - Unplanted, `hooks-counters` already produces `LATE H-COUNTERS: counters.all.if0: 27.581 ms` at 1x1 on the answering arm at 100 MHz. That is the ALL-push miss the README reports (`receipts/plant_controls.out`).
  - The reviewer turned the plant into a no-op in a scratch clone: its spin was replaced by a comment, and nothing else changed. The real plant flow (`run.py --plant counters-late`) then printed `PLANT counters-late caught: LATE H-COUNTERS: counters.all.if0: 27.581 ms` and exited 0 (`receipts/noop_counters_late.log`).
  - Every row was equal to the unplanted run to the cycle (`receipts/noop_vs_unplanted.out`).
  - The other 15 plants' rules match nothing unplanted in their groups (`receipts/plant_controls.out`).
- **Impact:**
  - The published receipt does show the plant working: `counters.first` takes 81.8 ms planted against 5.64 ms unplanted. That holds only because `counters.first` happens to be the first row.
  - The gate itself cannot tell a working plant from one that applies but never executes.
  - Self-test probe P5 shows the catch rule is not covered by the self-test either (`receipts/probes.out`).
- **Required outcome:** an unplanted or no-op `counters-late` must print `ESCAPED` and exit 1, and the real plant must still be caught. For example:
  - the plant names the path it delays and is caught only by that path;
  - or the catch rule excludes findings the unplanted run of the same group also produces.
- **Verification:** re-run the no-op probe (`scripts/` and the receipt command above). It must print ESCAPED with rc 1. `--plant counters-late` must still be caught by `counters.first`.

### F2: MINOR (Conformance). A file outside the lane's frozen file scope was edited without a recorded decision, and it conflicts with active lane S4

- **Where:** `sw/firmware/ctrl/test/ctrl_configs.py:218-223`, one new `OUTSIDE` entry for `hooks_build.py`.
- **Authority:**
  - Assignment item 4 (6513150371): "Files. `tb/` and the test READMEs".
  - The executor's takeover comment: "This lane edits only `tb/` and test READMEs."
  - AGENTS.md section 2: a conflict is published and needs a decision, not a private interpretation.
  - AGENTS.md section 4: frozen scope.
- **Evidence:**
  - The file is a shared firmware-test gate configuration that both active parallel lanes also edit. PR #810 lists it at `d930ea98`, and PR #812 lists it at `4d9b901c`.
  - `git merge-tree` of this head with #812's head `4d9b901c` gives `CONFLICT (content): Merge conflict in sw/firmware/ctrl/test/ctrl_configs.py`.
  - The same trial merge onto dev-soft-core `a68536fa` and onto #810 `d930ea98` is clean.
  - The edit is disclosed in REVIEW READY and the PR body. No decision was asked for, and it is not among the open questions.
- **Impact:**
  - The lane departs from its frozen file scope without a ruling.
  - Whichever of #812 and #844 merges second must resolve a conflict in a file neither lane is assigned.
  - The edit is a classification entry, not firmware instrumentation. The STOP rule on firmware and RTL is not breached.
- **Required outcome:** one of these:
  - a public maintainer decision that accepts the entry and says which lane resolves the #812 conflict;
  - or the harness stops naming the firmware tree by text, so that the boundary gate passes without the entry.
- **Verification:** a link to the decision; or `ctrl_boundary.py --require-rv32 --selftest` (both modes) passing at a head without the entry.

### RESIDUE (owner comment rule 2026-10-15; wording only, no figure or verdict depends on it)

- **R1:** `tb/verilator/ctrl_service_hooks/hooks.py:445`. The docstring says "S2's groups wait as long as their paths take unplanted", which names a lane. Fix: replace "S2's groups" with "the CPU budget harness's groups".
- **R2:** `tb/verilator/ctrl_service_hooks/run.py:4`. The module docstring (also the `--help` description) reads "The F2-F5 timing hooks on the target core", which names lanes. Fix: "The control-plane timing hooks on the target core (#665)".

### SUGGESTIONS (optional)

- **S1 (Tests): self-test precision gaps.** Reviewer probes on a scratch copy (`receipts/probes.out`, `receipts/probes/`) escaped the self-test in six places. Each real rule is written correctly; the self-test simply does not pin it. Add a synthetic case for each:
  - H-DISC counts a PROBE_TX on another interface (P2);
  - H-SRP accepts an SR_DOMAIN published before the Domain record (P3);
  - H-MAAP lets one gate publication cover every later report (P9);
  - the summary picks the best path (P1);
  - the loaded fan-out group is dropped (P4);
  - the ALL push ends at its first descriptor (P12).
- **S2 (Robustness):** `run.py:306-308` only prints `ORDERING not applied` on a full run and still exits 0. Consider failing when a check that can apply on the run's arm applied to nothing. The idle arm's H-COUNTERS is the only by-construction case.
- **S3 (Docs/Tests): the "on `sys`" label is imprecise.**
  - At this base the CPU stays on its `milan` clock input. Under `--cpu-clock sys` that domain is simply clocked at 100 MHz (`hooks_soc.py:223,238`).
  - `build.json`'s `milan_hz` records the configuration's 50 MHz, not the simulated domain's 100 MHz.
  - Record the simulated domain frequency, and word the label as "CPU at the sys frequency, on this base's CPU clock input".
- **S4 (Docs): FR_NFR still states 10 ms at this base.** At this head and at dev-soft-core `a68536fa`, FR_NFR 3.4.1 still reads "Proposed project budget: T_svc = 10 ms", and NFR-SCOUT-03 says the same. The 20 ms and min(T_svc, C) text arrives with #810. The README's grading cites the ruling correctly. One sentence saying so would spare a cold reader the apparent conflict.
- **S5 (Tests):** no hosted or repository gate runs `run.py --self-test`, and none runs the CPU budget harness's either. A follow-up issue could register both.
- **S6 (Robustness):** `--plant` silently overrides `--point`, `--arm` and `--cpu-clock` (`run.py:250-252`). Refuse conflicting flags instead.

## The five checks of the brief

1. **The clock: met in effect.**
   - Every graded run has `cpu_clock sys`, `cpu_hz 100000000` and `sys_hz 100000000`, at both points and on both arms (`receipts/check_digests.out`, `check_receipts.out`).
   - The harness clocks the base's CPU clock input at 100 MHz (`hooks_soc.py:215-238`).
   - Nothing else in this SoC is on that domain:
     - `with_milan=False`;
     - the mailbox, its millisecond tick (`split_soc.py:174-200`), timer0 and the CSR window are on `sys`;
     - the firmware's `CONFIG_CLOCK_FREQUENCY` is the system clock (`nvm_bench.py:153-158`).
   - So no Milan-derived timing exists to change. The CPU-to-bus crossing that remains is disclosed (README Limits). See also S3.
2. **The bounds: met.**
   - Every row of the four runs is graded at 20 ms, or 18 ms for SRP, plus its W. Its verdict is ms <= bound. No bound is relaxed, and the held push is graded from its eligibility, as the H-COUNTERS row reads (`check_receipts.out`, 124 checks, 0 mismatches).
   - The README's tables match the receipts exactly:
     - run counts;
     - the worst path alone and under load per hook, point and arm;
     - misses;
     - ordering applied, undecided and findings;
     - the H-COUNTERS path table;
     - the History tables (`check_history.out`, 16 rows).
   - Alone, every hook fits except H-COUNTERS' ALL push: 27.58 ms at 1x1 and 218.71 ms at 8x8.
   - Under the composed load every hook misses at both points and on both arms, with one exception: H-DISC at 1x1 on the answering arm, 14.03 ms, within its bound. That exception is in the README and confirmed by the receipt and by the reviewer's own re-measurement. The brief's summary omits it.
   - The misses are reported, not re-graded.
3. **Composed windows, aging group and mutants: met.**
   - `refilled_ms()` is 180 ms, against a longest refill from empty of 160 ms (MAAP, 8 x 20 ms; `KL_mbx_rx.sv:597-631`, one token per refill period).
   - The aging group binds and answers one interface at a time (`hooks.py:428-432`).
   - Each of the eight ordering checks, the held push, the bounds, the clock labels, the narrow rule, the supersede rule, the aging rule and the bucket rule has a mutant caught by name. The self-test reproduced 22/22 and 31/31 (`selftest_head.log`).
   - The precision gaps are in S1. The plant verdict gap is F1.
4. **Files and plants: firmware, RTL and shared harness met; file scope not met (F2).**
   - No firmware, RTL or S2/S3 harness file is edited.
   - Plants copy the firmware tree into the build directory (`hooks_build.py:116-123`), and `run.py:245` refuses a build directory inside the checkout.
   - The plant receipts show "tree: 0 changed".
   - The reviewer's scratch clones and this review clone stayed clean (`verify_clone.out`).
   - The out-of-scope `ctrl_configs.py` entry is F2.
5. **The receipts back every figure: met.**
   - The recorded input digests of the four runs equal this head's bytes, and so do the firmware and configuration tree digests (`check_digests.out`). Only the README changed between the measured commit `fa925043` and the head.
   - Re-measured in the reviewer's own clean builds at this head, with pinned Verilator 5.050:
     - 52 rows at 1x1 on the answering arm: `hooks-counters`, `backlog`, `backlog-owed`, `hooks-load-counters` and `backlog-adp`;
     - every row is equal to the author's in ms, CPU cycles and verdict;
     - this includes `counters.all` 27.581 ms, `counters.loaded` 20.761 ms, the composed H-DISC 14.030 ms, the owed ACMP command 77.837 ms, the four never-served commands and the composed SRP 68.053 ms (`repro_vs_author.out`).

## Note for the manager's ruling: who owns the composed-load misses

S5 is a measurement lane, and on this firmware base the measured misses are correctly measured results. The lane should report them; closing them is someone else's work. The base is `5b5f4336` with no S2b cuts. The ownership splits as follows:

- **SRP under the composed burst, timer-driven MRPDUs and retried notices:** S2b round 17 items 1 to 3 (6674728988), together with the composed-burst scope ruling 6634982529 item 1.
- **The ACMP commands behind the owed one, never served:** the egress-held rows that 6495692075 leaves with tsn-c-stack #26.
- **The ADP, AECP, NOTIFY and MAAP composed misses:** the pre-cut figures that S2b's per-pass work bounds address. The firmware budget levers are ruled under D4.

The natural follow-up is the executor's own open question: re-run the same four commands on S2b's merged head.

- The portable self-test already passes on a trial merge of this head with #810 `d930ea98` (`selftest_merged_s2b.log`).
- That trial merge has not been built.
- #810 moves the CPU onto `sys` and adds a refusal for a CPU still on `milan`, so `hooks_soc.py`'s clock handling will need re-checking then.

S5's acceptance "each hook within its bound" therefore stays open on #665. The PR correctly says "Relates to #665". The executor's second question, whether the ALL push is one path or graded per descriptor, is the maintainer's to settle. The harness grades it as the 3.4.2 row reads: event to last push, one path.

## Lens ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issue #665 assignment 6513150371 and the rulings listed above; FR_NFR.md:330-410 (3.4.1, 3.4.2, NFR-SCOUT-03); `hooks.py:40-79,121-245` (bounds, normative timeouts, eight hooks and obligations); `run.py:67-153`; `ctrl_configs.py:218-223`; the published `runs/*/results.json`; trial merges against #810 and #812 | R783-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| RTL | CLEAN | No `hdl/` change in the diff. Test gateware in `hooks_soc.py:84-177` checked against `KL_mbx.sv:503-530`: CsrFile ack and read timing; window answer at `wait_cycles-1`, accepted ahead of the timeout; `busy` drops at the answer, so the waited counter re-arms per request. CPU clock wiring `milan_soc.py:3070-3080` with `with_milan=False`; mailbox ms tick `split_soc.py:174-200` | R783-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| Robustness | CLEAN | `hooks_build.py:104-123,154-164,240-252` (unique anchors, stale-build refusal); `run.py:241-282` (refusals, regrade staleness); `hooks.py:635-666` (undecided rule, 1040 ms); never-served and starved paths fail (`run.py:71-76`); `refilled_ms` against `KL_mbx_rx.sv:597-631`; trial merges onto dev-soft-core and #810 pass the self-test. Suggestions S2 and S6 only | R783-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| Tests | UNCLEAN (F1) | `hooks_selftest.py` (22 checks, 31 mutants, reproduced); 12 reviewer probes (`receipts/probes.out`); the catch rule of all 16 plants against unplanted receipts (`plant_controls.out`); the no-op `counters-late` plant through the real flow (`noop_counters_late.log`); 52 rows re-measured | R783-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| Docs | CLEAN (RESIDUE R1, R2) | `tb/verilator/ctrl_service_hooks/README.md` (every results, findings and history figure recomputed from receipts; cited rulings opened); PR #844 body; REVIEW READY 6676840432; comment-rule scan of every new `.py` file | R783-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |

## Real limits of this review

- **Not run by the reviewer, so it rests on the published author receipts and their digests:**
  - the full point runs: 8x8 at all, and the other groups at 1x1;
  - 15 of the 16 plants, and the planted `counters-late`;
  - the firmware self-test shards, the S2 harness, `test_builder.py`, the TSN boundary gate, the 98 docs and CI gates, and behave;
  - the 50 MHz history runs.
- **No manager source bank exists at this head, and none is claimed or inferred.**
- **Hosted checks on the head were mostly queued or in progress at review time.** A snapshot is in `receipts/hosted_check_runs.tsv`: 9 succeeded, 1 skipped, 38 pending. A skipped context is not an executed job.
- **The answering arm is a labelled test datapath, not the real face.** The idle arm never answers a window.
- **Ends are mailbox commits.** No wire, egress or network time is measured.
- **Physical calibration NOT RUN.** No hardware was used, and field skips are not hardware proof.
- **The layout swing (6,490 cycles) is the ruling's figure**, not one measured here.
- **The review clone was not modified.** Fetching the evidence commit and the #810 and #812 heads added objects only.
  - Head, tree, index (1,496 regular files rehashed, 0 differ; modes 1448 x 100644 and 48 x 100755) and the six gitlinks were verified at the end (`verify_clone.out`).

## Pending manager duties

- Rule on F2: accept the `ctrl_configs.py` entry and name the lane that resolves the #812 conflict, or require that it be removed.
- Rule on the composed-load ownership note above, and on the executor's two open questions: re-measure on S2b's head, and ALL push as one path or per descriptor.
- Merge-order dependency: FR_NFR's 20 ms text lands with #810 (see S4).
- Merge-turn validation of the current dev-soft-core candidate: builder and native banks, and hosted/act acceptance.
  - The trial merge onto `a68536fa` is textually clean.
  - The trial merge onto dev `cc204c6f` conflicts only in files outside this diff.
- Self-test evidence in a PR comment (CONTRIBUTING; DoD box unchecked) when the evidence is published.
- Carry RESIDUE R1 and R2 to the residue checklist.

R783-1 FINISHED
