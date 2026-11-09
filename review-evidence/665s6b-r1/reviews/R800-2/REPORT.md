[R800] POSITIVE - exact head a88772f1cf0c3c3b269294bd4ceaf436646ca5a1

# R800-2: external delta review of PR #861 (#665 S6b, the two-placement `milan_dp` twin)

- **Head under review:** `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1`, tree `f8114fa174c093957ad04c6a07e4431675557883`. The PR is ready for review, and its head matches this one.
- **Delta reviewed:** `git diff e69d243a..a88772f1` (my R800-1 head to this head). It has five commits and 22 files, +113/-78. No file under `hdl/` changed, and no gitlink changed (`receipts/clone-integrity.txt`). Code that the delta does not touch keeps its R800-1 lens verdict. The full source range `6584b7bf..a88772f1` was used for the comment-rule scan.
- **Authority:** the [A10] ruling issuecomment-6727748772 on #665 says "This round is text and one plant. No grade, ledger row or owed row changes." Its items are:
  1. no lane labels or comment IDs in source;
  2. Table 7-2 at `test_aecp.cpp:437` and `aecp_mutants.py:408`, with the PR body corrected;
  3. the split-cdc plant count;
  4. a LeaveAll-omission plant, refused by the grade with its words.

  Done means `make twin` exits 0 with only ledger and owed rows, `make twin-plants` refuses every plant, and every `run:` step passes on a clean clone. Out of scope: R800-1 SUG-1 and R799-1 S2-S4.
- **Verdict:** POSITIVE. All five lenses are covered clean at this head. There is one RESIDUE (wording only) and one SUGGESTION, and no BLOCKER, MAJOR or MINOR.

## What was executed at this head

All runs used a clean clone of the committed head, with the five submodules the legs read at their gitlinks (`scripts/clean_tree.sh`, `receipts/clean-tree.txt`). Verilator is the pinned 5.050; its identity was checked with `--version` (`Verilator 5.050 2026-07-01 rev v5.050`).

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp twin` | rc 0, `twin: 0 finding(s)`. The only notes are 1 `[TAIL]` (ADP), 6 `[LEDGER]` and 6 `[OWED]`, the same rows by name as at R800-1. Per-protocol counts are unchanged. No note carries `issuecomment`, `ruling` or `S2b`. | `receipts/make-twin.txt` |
| the captures | `fabric.json` `fa6a5a12…`, `split.json` `ee143865…` and `report.json` `41e234b1…` are byte-identical to the author's round-6 receipt. The first two are also identical to my R800-1 captures, so the simulated behaviour is unchanged. | `receipts/captures-sha256.txt` |
| `make -C tb/verilator/milan_dp twin-plants` | rc 0: 40 lines `REFUSED`, 0 `ESCAPED`, from 20 plants × 2 controls. `leave-all-omission` is refused in both controls by `[MRP] split MSRP Domain value 06030002: nothing at ms 27910 (a LeaveAll) is not an Applicant's message: from AA, QA, Table 10-3's txLA! sends JoinMt or Mt`. Its planted capture is byte-identical to the author's (`04cf6cca…`). | `receipts/make-twin-plants.txt` |
| probe: grade mutants against all 20 plants (`scripts/probe_grade_mutants.py`, mine) | PASS (see Tests below) | `receipts/probe_grade_mutants.txt` |
| probe: the planted frame's structure (`scripts/probe_omission_frame.py`, mine) | PASS (see Robustness below) | `receipts/probe_omission_frame.txt` |
| comment-rule scan: my R800-1 script, unchanged (sha256 `b3742b25…f869`, as in R800-1's MANIFEST) | empty for both `e6d27f3a..HEAD` and `6584b7bf..HEAD` | `receipts/comment-rule-scan.txt` |
| a wider scan of added lines, Markdown included | no source comment, docstring or printed string carries a comment ID, ruling ID or lane label. The remaining hits are Markdown design pages, which the owner rule does not name, and the word "ruling" at `census_split.py:212`. | `receipts/broad-scan.txt` |
| `git grep 'Table 7\.1'`, plus lines 437 and 408, plus the PR body | both lines cite Table 7-2. The PR body cites Table 7-2 and no longer lists a leftover. | `receipts/table-7-2.txt` |
| `python3 -B scripts/ci_events.py --check` (R799-1 F2's verification) | rc 0: `ci_events: OK (2271 contract item(s) …)` | `receipts/ci-events-check.txt` |
| hosted check runs at this head (read-only snapshot) | 44 success, 1 skipped, 11 in progress, none failed. `split-cdc`, `firmware-unit` and `firmware-aecp-mutants` succeeded; `publication-census` was still running. | `receipts/hosted-checks-a88772f1.tsv` |

The author's published round-6 receipts (`review-evidence/665s6b-r1/author-r6` at evidence commit `50cf8d3c`) were spot-checked rather than re-run:
- **CI replay table:** of its 744 step rows, 546 have rc 0, 113 are skipped by their `if:`, and 85 are `not run`. None has a non-zero rc. Each `not run` row names its reason: an APT solver step, a from-source Verilator or Yosys build replaced by the pinned host tool, or a GitHub-API-only step.
- **Disclosed first attempts:** `union-capture_coherence`'s first attempt failed on the replay tool's own clone check, because two drivers started the same instance in the same second. The full sweep's first launch hit a missing TMPDIR. Both are disclosed, and both passed when re-run (`ci/again-capture_coherence.txt`).
- **split-cdc:** `gates/make-split-cdc.txt` shows the 12 planted arms and `checks: 13 failures: 0`. `split_cdc_check.py` is unchanged since `e69d243a`.

After the probes, the review clone was checked (`receipts/clone-integrity.txt`):
- `git status --porcelain --ignored` is empty;
- HEAD and tree are as above;
- the index tree equals HEAD's, so blobs and modes match;
- the six gitlinks are unchanged.

The clean clone also has no tracked change. The probes ran on copies under the packet's scratch.

## Findings

### RES-1 RESIDUE: the README's owed table names a different owner from the one the rows now print

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/README.md:1376` and `:1377`. In the "Owed to" column of `stream-output-0-notices` and `split-talker-failed`, the README says "the SRP adapter round after S2b". The two `[OWED]` notes now print `owed to the SRP adapter entry that takes MAAP's allocation (#665)` (`twin_compare.py:461` `SRP_ROUND`; `receipts/make-twin.txt`).
- **Evidence:** the author's handoff (§2) keeps the README text on purpose, because "docs may name lanes". The other three owed rows' README entries (`#858`, and the #857 and #860 rows) already match what they print. The paragraph under the table also describes the cause as "until an SRP adapter entry takes MAAP's range". So the README states the same owner in two different wordings, and the table is the one that does not match the program.
- **Impact:** wording only. No row, predicate, value, cause or verdict changes. A reader searching for the printed owner in the README will not find it.
- **Exact fix:** in both cells, write "the SRP adapter entry that takes MAAP's allocation (#665)". A design page may name a lane, so "(the SRP adapter round after S2b)" may be kept as a parenthesis.
- **Verification:** `grep -n "SRP adapter entry that takes MAAP's allocation" tb/verilator/milan_dp/README.md` prints both rows.

### RES-2 RESIDUE: one edited Makefile comment line was not re-wrapped

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/Makefile:949` (120 columns): "# out a declared attribute and the LeaveAll declarations; the fabric's for its owed defects gone (#857, #858, #860), and". Its neighbours wrap at 74-78 columns.
- **Impact:** formatting only. No gate measures it; the file already had 134 lines over 79 columns at `e69d243a`.
- **Exact fix:** re-wrap the paragraph at lines 941-950 to the width of its neighbours.

### SUG-1 SUGGESTION: cite the owning issue for the REBOOT hold

- **Lenses:** Docs.
- **Where:** `sw/mailbox/census_split.py:66-69`: "The REBOOT carrier is not built yet; until it is, the hold is documented here."
- **Possible outcome:** name the issue that owns the carrier, as `docs/design/MAILBOX_SPLIT.md:1176` and `:1874` do (`#787`). The line states its behaviour and complies as written, so this is optional.

### Earlier findings

I read the PR thread only after my own pass. My draft verdict from before that read is kept as `receipts/draft-verdict-before-prior-findings.txt`. The thread holds R799-1 (NEGATIVE at `e69d243a`), my R800-1 (POSITIVE at `e69d243a`), the start notices, and one later round at this head. I did not read that later round's report.

| Prior finding | State at `a88772f1` | Evidence |
|---|---|---|
| R800-1 RES-1: lane labels and comment IDs in new source comments | **Resolved** | My unchanged scan is empty on both ranges. The four runtime "owed to" strings that RES-1 set aside were cleaned too: `#857/#858/#860 (a release-image defect)`, and the `SRP_ROUND` text. The README cell those strings left behind is RES-1 above. |
| R800-1 RES-2: "Table 7.1" at `test_aecp.cpp:437` and `aecp_mutants.py:408`, and an incomplete PR-body list | **Resolved** | `receipts/table-7-2.txt` |
| R800-1 SUG-1: a non-LeaveAll frame that omits an attribute is not read as its tx! | Out of scope by the ruling; kept as a suggestion, unchanged | `twin_mrp.py:269-289` is unchanged except for its docstring |
| R799-1 F1 (MINOR): the same Table 7.1 citations | **Resolved** | as RES-2 |
| R799-1 F2 (MINOR): split-cdc said "four planted raw crossings" | **Resolved**. Both lines state twelve plants: `CI_WORKFLOWS.md:437-442` gives 4 raw crossings, 5 held-bus takes, 2 resets and 1 level-clocked primitive, and the template's lines 318-324 say the same. This matches `split_cdc_check.py:258-301` `PLANTS` (12 entries). `ci_events.py --check` passes. | `receipts/ci-events-check.txt` |
| R799-1 R1 (RESIDUE): the comment rule, 43 lines | **Resolved** for source. The author's receipt `scans/r799-list-scan.txt` re-runs R799-1's scan with empty output, and my own scan agrees. | `receipts/comment-rule-scan.txt` |
| R799-1 S1: no plant guards the LeaveAll-omission arm | **Resolved** by `leave-all-omission`. Both named mutants are caught, as are four more of mine. | `receipts/probe_grade_mutants.txt` |
| R799-1 S2-S4 | Out of scope by the ruling | — |

## Lenses

### Conformance: CLEAN

```text
[R800] PASS Conformance — twin_plants.py:201-223, twin_compare.py:86-87, twin_mrp.py:72-77 (TXLA), README.md:1322-1325 at a88772f1 — the plant against IEEE 802.1Q-2018 Table 10-3 txLA! and the ruling
```

- **The plant tests what Table 10-3 forbids.** It removes the declared Domain's VectorAttribute from a LeaveAll frame and keeps the Domain Message's own LeaveAll vector. At that LeaveAll the Domain is in AA or QA (Registrar MT). Table 10-3's txLA! row gives AA sJ→QA and QA sJ, neither bracketed. With the opportunity's rLA! taken first, both go to VP, whose txLA! is s. So the only legal messages are JoinMt or Mt. The grade's words say exactly this.
- **The other ruling items hold.** Item 2 (Table 7-2) and item 3 (twelve plants) are met, as shown above. Item 1 is met for source.
- **Rows, predicates, values and causes are unchanged.** No `Row(`, `GradeRow(` or `lambda` line changed in `twin_compare.py` (`receipts/clone-integrity.txt`, last line). Only the owner strings of four rows changed, and only in wording. The captures and the `[LEDGER]` and `[OWED]` rows are the same as at R800-1.
- **"Done means" holds.** `make twin` exits 0 with only ledger and owed rows. `make twin-plants` refuses all 20 plants. The `run:` steps pass on clean clones according to the author's replay, which I spot-checked.

### RTL: CLEAN

```text
[R800] PASS RTL — git diff e69d243a..a88772f1 -- hdl protocol-processor gptp-processor third_party (empty); tb_split_top.sv:61; Makefile:37-40,864-960 — no RTL, gitlink or build-rule change
```

The only change under `tb/` that touches an HDL file is the `//!` comment at `tb_split_top.sv:61`. In the Makefile, the `split` rule is the same at `:869-870`, and the `twin-plants` recipe is unchanged apart from `leave-all-omission` added to `TWIN_CAPTURE_PLANTS`. `split-cdc` (12 plants) and `split_cdc_check.py` are unchanged since R800-1 covered them, and the hosted `split-cdc` passed at this head. R800-1's RTL coverage is not affected.

### Robustness: CLEAN

```text
[R800] PASS Robustness — twin_plants.py:201-223; receipts/probe_omission_frame.txt; scripts/probe_omission_frame.py — the plant's frame surgery and fail-closed path
```

- **The plant yields a well-formed MRPDU.** I rebuilt the expected planted frame on my own: walk the MSRPDU's Messages, take the Domain Message at octet 180 (`0404 000f`), remove its `0001 06030002 6c` VectorAttribute (NumberOfValues 1, no LeaveAll, one ThreePackedEvents octet `0x6c`, JoinMt), and lower its AttributeListLength from 15 to 8.
- **Only that frame changes.** The planted capture equals that reconstruction byte for byte. Both frames decode, and the LeaveAll types are still [1, 2, 3, 4]. The other attribute events (the two Talker Failed JoinMt) are unchanged. Exactly one frame of the capture differs, and no other split MSRP frame at ms 27910 carries the Domain, so the omission is not an MRPDU split across frames.
- **The plant fails closed.** If no matching frame exists, it raises `SystemExit("plant leave-all-omission: no split MSRP LeaveAll frame …")` and does not plant silently.
- **Nothing else in scope changed.** No other input-handling code changed in the delta.

### Tests: CLEAN

```text
[R800] PASS Tests — receipts/make-twin-plants.txt (40/40 REFUSED); receipts/probe_grade_mutants.txt; scripts/probe_grade_mutants.py — the new plant against grade mutants, each run with a regenerated baseline against all 20 plants
```

Six one-line mutants of `twin_mrp.py` change how an attribute omitted from a LeaveAll frame is read or judged. Each was run through `make twin`'s comparison and both controls of all 20 plants:

| Mutant | `make twin` | Caught by the 19 earlier plants | Caught by `leave-all-omission` |
|---|---|---|---|
| `txla-qa-bracketed` (QA's txLA! sJ made `[sJ]`) | rc 0 | none | yes (self rc 1, between rc 1) |
| `txla-aa-sends-nothing` (AA's txLA! sJ made `[s]`) | rc 0 | none | yes |
| `omitted-read-as-tx` (an omission read as a non-LeaveAll tx!) | rc 0 | none | yes |
| `txla-every-cell-optional` | rc 0 | `srp-plus-k`, self control only | yes |
| `omitted-attribute-unread` (a LeaveAll frame's omission not observed) | rc 0 | `srp-plus-k`, self control only | yes |
| `nothing-always-allowed` | rc 0 | `srp-plus-k`, self control only | yes |

- **The new plant closes a real gap.** The first three mutants pass `make twin` and every earlier plant, and only the new plant catches them. The two table mutants are R799-1's, re-run independently.
- **It fails on its own words.** Both controls exit 1 under each mutant. Under `omitted-read-as-tx` the grade still produces a finding, but with tx! words rather than the plant's txLA! words.
- **The head is clean.** At the head, all 20 plants are refused and `make twin` exits 0.
- **Other changes in scope.** `PLANT_WORDS` and `SELF_WORDS` gain the plant ("MSRP"). No existing test or plant was weakened; no other plant's words changed.

### Docs: CLEAN (RES-1 and RES-2 recorded as RESIDUE)

```text
[R800] PASS Docs — tb/verilator/milan_dp/README.md:110,1322-1325,1407,1433; docs/design/MAILBOX_SPLIT.md:1544; docs/testing/CI_WORKFLOWS.md:431-442; .github/ci-templates/rtl-fast.yml:318-324; Makefile:40; the PR body — counts, the new rule and the plant row against the code
```

- **The counts agree with the code.** Every "twenty plants" agrees with `TWIN_*PLANTS` (3 + 11 + 6). The README's plant table has 20 rows, and the new row's words equal `PLANT_WORDS["leave-all-omission"]`. No "nineteen" referring to the twin remains.
- **The split-cdc docs agree with the leg.** The policy page and the template state the leg's 12 plants.
- **The rewrites keep their meaning.** Every rewritten comment still names its issue (#665, #857, #858 or #860), a clause (for example Milan v1.2 5.4.5.2 and Table 5.22 in `twin_decode.py:189-190`, or 4.2.7.2.2 in `twin_grades.py:22`), or the behaviour itself (for example "a row no stimulus reaches is unproven", and "so it lengthens no existing job").
- **The PR body agrees with the head.** It states Table 7-2, twelve split-cdc plants, the twentieth plant, and 40 of 40.
- **Design pages.** `MAILBOX_SPLIT.md` and the README keep linked comment IDs. The owner rule names source comments, and both the ruling and the author leave design pages out, so they are not a finding here.
- **Residue:** RES-1 and RES-2 are wording only.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `twin_plants.py:201-223`, `twin_compare.py:86-87,461,491,531,553`, `twin_mrp.py:72-77,153-171,269-289`, README `:1322-1325`; the [A10] ruling issuecomment-6727748772; `receipts/make-twin.txt`, `make-twin-plants.txt`, `table-7-2.txt`; R800-1 coverage of the untouched code | R800-2 | `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1` |
| RTL | CLEAN | `git diff e69d243a..a88772f1` (no `hdl/` and no gitlink change), `tb_split_top.sv:61`, `Makefile:864-960`, `clone-integrity.txt`, hosted `split-cdc` success, R800-1 RTL coverage | R800-2 | `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1` |
| Robustness | CLEAN | `twin_plants.py:201-223` (frame surgery, fail-closed exit), `receipts/probe_omission_frame.txt` | R800-2 | `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1` |
| Tests | CLEAN | `receipts/make-twin-plants.txt` (40/40), `receipts/probe_grade_mutants.txt` (6 mutants × 20 plants), `twin_compare.py:68-120`, `Makefile:951-955` | R800-2 | `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1` |
| Docs | CLEAN (RES-1, RES-2 RESIDUE) | `tb/verilator/milan_dp/README.md`, `docs/design/MAILBOX_SPLIT.md:1544`, `docs/testing/CI_WORKFLOWS.md:431-442`, `.github/ci-templates/rtl-fast.yml:318-324`, the PR body, `receipts/comment-rule-scan.txt`, `receipts/broad-scan.txt` | R800-2 | `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1` |

## Real limits

- **Not re-executed here:** the census, `split-mutants`, `split_parallel.py`, the firmware suites, the builder and the full Verilator sweep. The delta touches none of them except in comments and docstrings, and R800-1 ran them at `e69d243a`. For this head they rest on the author's round-6 receipts, which I spot-checked, and on the hosted checks that had passed when I took the snapshot.
- **No manager source bank ran at this head, and none is claimed.** The current-dev merge candidate (source base `6584b7bf`, live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`) was not built or validated by this review.
- **Hosted evidence is a read-only snapshot.** 11 runs were still in progress, `publication-census` among them, and 1 was skipped by its `if:`.
- **Physical calibration NOT RUN.** This is simulation and host evidence only; field skips are not hardware proof.
- **The mutant probe reuses the head's planted captures.** The mutants edit only the grade code, not the plant makers. It regenerates each mutant's unplanted baseline.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR.
- Own hosted and act acceptance at the exact head, including the in-progress `publication-census` and Verilator shards.
- Carry RES-1 and RES-2 to the residue checklist.
- Merge only with explicit maintainer authorization.

R800-2 FINISHED
