[R634] POSITIVE - exact head 71d5e08506168e88f52a998a05f1d43b4801d2a5

Issue #645 / PR #741, round R634-3. Internal independent re-reviewer, cleared context, single re-reviewer for this delta.

- Head: `71d5e08506168e88f52a998a05f1d43b4801d2a5`, tree `c104b0c1c98c9b106ce8dbb0789250499a60ba5d`.
- Previously reviewed head: `b2891a8f29598fff1865f855991ad4c1505e35a3`. At that head R634-2 was NEGATIVE for one MINOR (F1) and R635-2 was POSITIVE.
- Delta reviewed: `b2891a8f..71d5e085`, one commit, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` +3/-3.
- Range base: `f62602531d415d6c1cae1374a3cc2938faf54049`, which is also live `dev`.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6188583660 ("R634-2-F1. state the grouping the tool used and drop 'consecutive' ... Keep the printed ranges, and make the PR body bullet follow the page").

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open, and all five lenses are covered clean at the exact head.

- **R634-2-F1 is resolved at its cause.** The page's burst row now states the grouping the tool applies, and "consecutive" is gone from the page and the PR body. Under the stated rule, every printed burst figure reproduces from the published recorded data. Two probes check this: the round-2 probe, reused unchanged, and a new per-window probe.
- **Nothing else changed.** The repository delta is three lines of one Markdown page: the burst row (`:4890`) and two artifact-hash rows (`:4969`, `:4976`). The submodule gitlinks are unchanged.
- **Packet changes are wording only.** In the published lane packet, the only change from round 2 to round 3 is wording in `tools/summ_b17.py` (its docstring and the emitted row). That changes `summary/priming.md`. Every numeric summary is byte-identical.

One new RESIDUE and one SUGGESTION are listed below. Two RESIDUE items and two SUGGESTIONs from R634-2 were outside this round's assignment. They are retained unchanged for the manager's residue checklist.

## What was checked

1. **The page states the rule actually used.**
   - `:4890` now reads "Bursts of PDUs over 20 us late per cycle, grouped while less than 1 ms apart, 3 to 12 such PDUs each". This is the assignment's decision wording.
   - The tool's rule is `BURST_US, BURST_GAP_S = 20.0, 1e-3` in `tools/summ_b17.py:39`. Its `bursts()` function, `:70-80`, drops PDUs `late_us <= 20.0` and joins a PDU to the open burst while `s - last_s < 1e-3`. The docstring, `:17-18`, now says "while successive qualifying PDUs are less than 1 ms apart".
   - Page, tool and decision agree.
   - "consecutive" appears 0 times in the B17 section (`:4611-4979`), its index row (`:92`) and the live PR body. Receipt: `receipts/pr-741-body-raw.md`, plus the grep counts in this report.
2. **Every printed burst figure reproduces under the stated rule.** Both probes read the raw `cycles/cNN/{events,poll}.jsonl` and `summary/cNN.json` `late_pdus` of the published round-3 packet (`review-evidence/645-b17-r1/author-r3`, evidence branch commit `72e09cffa0e39748f30c78c6f5d161b44b15c768`).
   - `scripts/burst_definition_probe.py` is the R634-2 script, byte-identical (sha256 `f583e7da...`). Under rule A_1ms it gives:
     - bursts per cycle: 9 to 19 to the last poll, 11 to 24 to the capture's end;
     - bursts after the slip: 8 to 18 to the last poll, 10 to 23 to the capture's end;
     - 3 to 12 PDUs per burst;
     - a later, larger burst in 9 of 10 cycles.
     These are the page's ranges. Receipt: `receipts/burst-definition-probe-r3.json`.
   - `scripts/burst_window_probe.py` is new. It recomputes the following and matches all 12 printed values plus the under-10 us claim. Receipt: `receipts/burst-window-probe-r3.json`, `all_match: true`.
     - the further bursts after the last poll: 2 to 7;
     - PDUs per burst in each window separately: 3 to 12 to the last poll, and 3 to 12 to the capture's end;
     - peak after the slip: 27.1 to 30.1 us and 27.6 to 30.3 us;
     - the slipping burst's peak: 24.6 to 29.3 us;
     - the first burst inside the slip's interval: 10 of 10;
     - no recorded late PDU before the interval.
   - The per-cycle counts equal the author's `summary/bursts-round3.md` and the REVIEW READY table.
   - **Falsification sweep.** The same probe regroups the data at gaps from 187.5 us to 2 ms. Only 750 us and 1 ms reproduce every printed burst range. The consecutive rule (187.5 us) gives 12 to 24 and 11 to 23 to the capture's end, and 1.5 ms or more gives 11 to 23 and 10 to 22. So the figures are sensitive to the rule, and the stated rule is one that reproduces them.
3. **The PR body follows the page.**
   - The live PR body is byte-identical to the packet's `PR-BODY.md`. Receipt: `receipts/pr-741-body-raw.md`.
   - Line 31 reads "A burst groups PDUs more than 20 us late while less than 1 ms apart, with 3 to 12 such PDUs each".
   - Line 44 reads "Bursts use the same grouping stated above".
   - The figures there equal the page's.
   - The author's `tools/check_b17_page.py` was re-run here against the head page and the live PR body: 84 ok, 0 mismatches, rc 0. Receipts: `receipts/author-check-rerun-r3.txt`, `.rc`.
4. **Hashes and regeneration.**
   - All 14 evidence rows of the page's hash table (`:4966-4979`) match the round-3 packet in bytes and SHA-256, including round-3 `summ_b17.py` (20,127 bytes, `6e333555...`) and `priming.md` (964 bytes, `0aaef1c5...`). Receipt: `receipts/page-hashes-vs-r3-packet.txt`.
   - Re-running round-3 `summ_b17.py` on a scratch copy of the packet returns rc 0. It regenerates `priming.md`, `table.md`, `figures.json`, `cycles.json` and `counter-logs.sha256` byte-identical to the published files. Receipt: `receipts/summ-b17-rerun-r3.txt`.
   - All 12 lines of `priming.md` appear verbatim on the page. Receipt: `receipts/priming-table-vs-page.txt`.
   - Packet manifest: two of 119 entries do not verify. Both are publisher-side redaction carried unchanged from round 2:
     - `identity-resume/identity-verdict.json` is recorded in the evidence branch's `MANIFEST.json` as `path_redacted: true`, from `bc704fb3...` to `64fae695...`, with the same bytes in the round-2 packet.
     - `tools/__pycache__/ana_b17.cpython-314.pyc` was not published.
     All other entries verify. No delta impact.
5. **Gates at the exact head, run here.** All seven required docs gates return 0. Receipts: `receipts/gate-*.log|rc`.
   - `scripts/docs_check.py`
   - `scripts/check_doc_style.py`
   - `scripts/gen_toc.py --check` (pinned renderer from `tools/markdown/requirements.txt`, hash-locked, in a scratch venv)
   - `scripts/check_em_dash.py --base f6260253`: 0 findings over 370 added lines
   - `scripts/check_doc_paths.py`
   - `scripts/check_baremetal_only.py --check`
   - `git diff --check`

   These are the reviewer's re-runs. They are not a manager source bank.

## Findings

### R634-3-R1 RESIDUE: the packet locator still says "the second round's" files

- **Lenses:** Docs.
- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4647-4649`. It reads: "The second round's tools and summary, named in [B17: artifact hashes](#b17-artifact-hashes), are in the packet the manager holds."
- **Evidence:**
  - The hash table this sentence points to now names a round-3 `tools/summ_b17.py` (`:4969`) and a round-3 `summary/priming.md` (`:4976`).
  - Both rounds are now published on `645-b17-review-evidence`: `review-evidence/645-b17-r1/author-r2` (commit `5b67fa6b`) and `review-evidence/645-b17-r1/author-r3` (commit `72e09cff`).
  - This is the locator R634-2-S1 suggested naming, made stale by this delta's "round 3" label.
  - Purely prose: no figure, hash, verdict, test or claim changes.
- **Exact fix:** "The later rounds' tools and summaries, named in [B17: artifact hashes](#b17-artifact-hashes), are published on the same branch as `review-evidence/645-b17-r1/author-r2` (round 2, commit `5b67fa6b`) and `review-evidence/645-b17-r1/author-r3` (round 3, commit `72e09cff`)."

### R634-3-S1 SUGGESTION: say "successive" in the burst row

- **Lenses:** Docs.
- **Where:** `:4890` and PR body line 31.
- **Evidence:** The rule joins a PDU while it is under 1 ms after the previous qualifying PDU. A reader could instead take "less than 1 ms apart" to bound the whole burst's span. 5 of the 179 bursts span 1 ms or more, up to 1,370 us, so that reading would change counts.
- **Suggestion:** The wording is the maintainer's decision and reads correctly as written. Adding the tool docstring's word would close the other reading: "grouped while successive ones are less than 1 ms apart".

### Prior findings at this head

| Prior finding | Severity | Status at 71d5e085 | Evidence |
|---|---|---|---|
| R634-2-F1: burst definition does not reproduce two printed ranges | MINOR | **RESOLVED** | `:4890`; probe A_1ms reproduces 9-19, 11-24, 8-18, 10-23, 3-12, 9/10; window probe all 12 match; PR body lines 31 and 44; 0 "consecutive" |
| R634-2-R1: page-check and `figures.json` descriptions claim more than they cover | RESIDUE | **RETAINED** (not in this round's assignment) | `:4753-4755`, `:4975` unchanged; the 2 to 7 figure is correct (window probe); exact fix as in R634-2 |
| R634-2-R2 / R635-2-RES-1: the `RENDER_STAT` lower bound reads as a five-cycle contrast | RESIDUE | **RETAINED** (not in this round's assignment) | `:4824-4827` unchanged; exact fix as in R634-2 |
| R634-2-S1: name the published round 2 packet | SUGGESTION | Not taken; superseded by R634-3-R1 | `:4647-4649` |
| R634-2-S2 / R635-2-S3: the 32 s hold differs per cycle in c01 and c03 | SUGGESTION | Not taken (optional) | `:4759-4760` unchanged |
| R635-2-S1, R635-2-S2 | SUGGESTION | Optional; S2 as R634-3-R1 | none |
| R634-1-F1..F4, R635-1-F1, R635-1-RES-1/2, R635-1-S1..S4 | various | Resolved or taken at `b2891a8f` (R634-2, R635-2); the delta does not touch the lines they rest on | `git diff b2891a8f..71d5e085` |

## Lens results

| Lens | Result | Artifact | What was checked and against what |
|---|---|---|---|
| Conformance | PASS | assignment 6188583660; `:4890`; live PR body lines 31, 44; `receipts/burst-*-probe-r3.json` | The decision is met item by item: the grouping used is stated, "consecutive" is dropped, the printed ranges are kept, and the PR body follows the page. Every printed burst figure is reproduced under the stated rule. Slips, classes (all (c)) and "#645 stays open" are unchanged. |
| RTL | PASS | `receipts/clone-integrity.txt` (delta name-status; 6 gitlinks equal to `f6260253`) | The delta has no HDL, firmware, constraint or tooling file, and no submodule move. The RTL citations in the B17 section (`:4716-4717`, verified at `b2891a8f`) lie outside the changed lines. The prior RTL verdict holds, because nothing it depends on changed. |
| Robustness | PASS | `receipts/burst-window-probe-r3.json` (`gap_sweep_us`, `pdus_last` and `pdus_cap`) | The boundary behaviour of the stated rule was checked: strict `> 20 us`, strict `< 1 ms`, the per-window PDU range, and the gap sweep. A different rule changes the figures, and the stated one reproduces them. No bench, console or power action was taken (recorded data only). |
| Tests | PASS | `receipts/author-check-rerun-r3.txt` (84 ok, 0 mismatches); `receipts/summ-b17-rerun-r3.txt` (5 outputs byte-identical); two reviewer probes; `receipts/gate-*.rc` (7 of 7 rc 0) | The author check was re-run at this head against the live PR body. The summary tool regenerates the published table. The probes are independent of the author's check. R634-2-R1 is retained as RESIDUE. |
| Docs | PASS | `:4890`, `:4969`, `:4976`; `receipts/page-hashes-vs-r3-packet.txt` (14/14); docs gates | The changed row and both hash rows are correct against the round-3 packet. R634-3-R1 and the retained R634-2-R1/R2 are wording RESIDUE. R634-3-S1 is optional. |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6188583660; page `:4890`; PR body (live, byte-identical to packet); both burst probes | R634-3 | 71d5e08506168e88f52a998a05f1d43b4801d2a5 |
| RTL | CLEAN | delta name-status (one Markdown page); gitlinks unchanged from `f6260253`; prior RTL coverage at `b2891a8f` unaffected | R634-3 | 71d5e08506168e88f52a998a05f1d43b4801d2a5 |
| Robustness | CLEAN | gap sweep; per-window PDU ranges; threshold and gap strictness in `summ_b17.py:39,70-80` | R634-3 | 71d5e08506168e88f52a998a05f1d43b4801d2a5 |
| Tests | CLEAN (R634-2-R1 is RESIDUE) | `check_b17_page.py` re-run (84/0); `summ_b17.py` regeneration; two probes; 7 gates | R634-3 | 71d5e08506168e88f52a998a05f1d43b4801d2a5 |
| Docs | CLEAN (R634-3-R1, R634-2-R1, R634-2-R2 are RESIDUE; R634-3-S1 optional) | B17 section `:4611-4979`; hash table 14/14 against `author-r3`; docs gates | R634-3 | 71d5e08506168e88f52a998a05f1d43b4801d2a5 |

## Real limits

- **Recorded data only.** No bench, console, controller, tap or power access was made. Physical calibration was NOT RUN. Printed precision is not calibrated accuracy, and the lane's field skips are not hardware proof.
- **The raw tap captures were not available.** The `.pcap` files stay on the bench host. Burst figures were recomputed from the published `summary/cNN.json` `late_pdus`, which `tools/ana_b17.py` extracted from those captures. This round did not re-derive `late_pdus` from the captures.
- **No source bank was run.** These are the reviewer's own docs-gate re-runs, not a manager source bank. No builder, native, Verilator, Yosys, PP or gPTP bank ran here, and none applies to a Markdown-only delta.
- **Hosted contexts, as snapshotted at 09:19:53Z.** Receipt: `receipts/hosted-checks-snapshot.tsv`.
  - `rtl-fast`, `full-ci-gate`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `changes` and `wire-accountability` succeeded at this head.
  - `docs-check` was still in progress.
  - `verilator-suites`, `yosys-portability` and the firmware and shard contexts were skipped. Skipped is not executed.

## Pending manager duties

- Accept the hosted and act results at this head, including the `docs-check` result that was still in progress at the snapshot.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, from source base `f6260253` (also live `dev`), and link the receipts on the PR.
- Carry R634-3-R1, R634-2-R1 and R634-2-R2 to the residue checklist.
- Confirm the two-positive review bar. R635-2 was POSITIVE at `b2891a8f`, and this round is the single re-review of the delta under the owner's rule.
- Close-out: `Refs #645` (the issue stays open, every slip class (c)). Merge only with maintainer authorization.

## Receipts

All are listed in `MANIFEST.sha256`. Scripts:

- `scripts/burst_definition_probe.py` (R634-2, unchanged)
- `scripts/burst_window_probe.py` (new)

Usage for both: `python3 -I <script> <author_packet_dir>`, read-only.

The clone was restored and verified: HEAD and tree as above, `write-tree` equals the tree, `status --ignored` is empty (a gate-generated `scripts/__pycache__/` was removed), `diff-index` is empty, and the 6 gitlinks are equal to `f6260253`. Receipt: `receipts/clone-integrity.txt`.

R634-3 FINISHED
