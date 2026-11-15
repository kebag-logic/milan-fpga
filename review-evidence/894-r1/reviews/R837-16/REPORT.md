[R837] NEGATIVE - exact head 07ed787ee0448be2360f97e8af01194a499003ee

# R837-16: delta re-review of PR #902 (issue #894), rounds 15 to 21, from `867faf1e` to `07ed787e`

Internal, cleared-context, independent review. Head `07ed787ee0448be2360f97e8af01194a499003ee`, tree `697298a1c8a5552b7ecd7f5790ccfbfeaa16cf13`. The review start is PR #902 issuecomment-6897154541.

The review covers the whole delta since round 14's `867faf1e` (R838-9 POSITIVE there): 11 commits and 8 files (`receipts/name_only_867faf1e.txt`). That is two Markdown documents, the harness README, two firmware headers and three harness Python files. Since `41ca9f87` the delta is `docs/design/SPLIT_CONTROL_MEMORY.md` alone (`receipts/name_only_41ca9f87.txt`).

**Verdict: NEGATIVE on one MINOR (Docs).** The PR body's final-pass paragraph says the hooks self-test "ran at the final head", a few sentences after it defines the final head as `07ed787e`. It last ran at `234bc149`. Every other lens is clean. R837-15-F1 and F2 are closed at their cause, and the four sweeps reproduce byte for byte at the head. Three wording residues and two suggestions are listed below.

## How the task was reconstructed

1. **The rules:** AGENTS.md (sections 5 to 7), and CONTRIBUTING.md's docs and em-dash gate rules.
2. **The scope:** issue #894's REVIEW READY for this head (issuecomment-6897091854) and its acceptance items 1 to 4 for round 21. These match the review brief's checks (1) to (4).
3. **The PR body:** the live body, which is byte-identical to the packet's `author-r21/PR-BODY.md` (121,964 B, sha256 `57ad272a…`).
4. **The diffs:** `git diff 867faf1e..07ed787e` in full, and the word diff `41ca9f87..07ed787e`.
5. **The "this PR writes" scope:** lines changed since the PR's GitHub base `cec88385`. That base is a descendant of the source base `66f71326`. Text that came in between the two, such as section 5 `:483`, is base-branch text (R837-15-S2).
6. **The evidence:** the public tree `471b48a4`, `review-evidence/894-r1/`.
   - `author-r21/`: 56 INDEX rows, each sha256 and size verified. The outer `MANIFEST.json` has 57 `author-r21/` entries, the INDEX included, all matching. Every fetched blob matched its git object id.
   - `author-r20/receipts/local-fe1fd541/`: 26 commands, rc 0.
   - The image receipts of rounds 12, 13, 14 and 16.
7. **Prior findings:** I read R837-14 (issuecomment-6894240714) and R837-15 (issuecomment-6896987271) only after my own pass.

## Findings

### R837-16-F1: MINOR (Docs)

- **Where:** the live PR #902 body, "The final pass, gate by gate" paragraph (body line 894). It reads: "The final head is `07ed787e`. … Round 13's own pass was at `234bc149`. After `ed0df35b` it changes only `tb/verilator/ctrl_service_hooks/hooks.py`, which no workflow job and no sweep suite reads: its one reader is lane part a's `hooks_selftest`, **which ran at the final head**."
- **Evidence:**
  - The paragraph defines "the final head" as `07ed787e`. The same body's gate table says the hooks self-test ran at `234bc149` ("Lane gates, part a (48) | `234bc149` | … the hooks self-test 28 of 28").
  - The published tree has `hooks_selftest.log` only for rounds 11 and 13 (`author-r13/receipts/lane/lane-234bc149/`).
  - Round 20's `harness_selftest` at `41ca9f87` is the CPU budget harness's `run.py --self-test`, not the hooks harness.
  - No commit after `234bc149` touches `tb/verilator/ctrl_service_hooks/` (`git log 234bc149..HEAD -- tb/verilator/ctrl_service_hooks` is empty). So the result carries by identity, but the sentence claims exact-head execution that did not happen.
  - The sentence has been carried since round 14's body (`author-r14/PR-BODY.md`: "The final head is `867faf1e`" … "which ran at the final head"). Each round renamed the final head, and that turned this clause false.
- **Authority:** AGENTS.md section 7 (exact-head evidence), and the Docs lens ("The PR and Issue contain enough evidence for another cold reviewer"). This is the same class as R837-15-F2: it misstates the head that a piece of evidence covers, so it is not wording only.
- **Impact:** a cold reviewer or the manager reads the hooks self-test as run at the merge candidate's source head, when it ran nine commits earlier and carries only by the identity of its inputs.
- **Required outcome:** the sentence names the head at which the hooks self-test ran, and says why it carries. For example: "its one reader is lane part a's `hooks_selftest`, which ran at round 13's final head, `234bc149`; no later commit touches `tb/verilator/ctrl_service_hooks/`". No other sentence in the body may use "the final head" for a head other than the one the paragraph defines.
- **Verification:**
  - Read the paragraph.
  - Grep the body for "final head" and check that every use either names `07ed787e`, or names its SHA and round (as body line 265 does; see R3).
  - `git log 234bc149..HEAD -- tb/verilator/ctrl_service_hooks` is empty.

## Residue (wording only; no lens made unclean; for the residue checklist)

- **R837-16-R1** (`docs/design/SPLIT_CONTROL_MEMORY.md:361`, `:363`, `:370`): the era in parentheses has two names, and the table's lead names the wrong column.
  - `:361` introduces the table as "Each image … at the merge of #810's `084cf7a8` into the tiers with #904's map checks and THE PACE". Its cells are now the head's figures, with that merge's in parentheses.
  - The header `:363` and `:370` call the parenthesised era "the ruling's head". `:2382` calls the same figures (125,200 B) "at the merge of #810's `084cf7a8`".
  - Every figure is correct: the head's match `rom-per-image.txt` and the image identity chain (below).
  - Exact fix:
    - `:361`: "…, at the head, with each figure at the merge of #810's `084cf7a8` into the tiers with #904's map checks and THE PACE in parentheses ([section 13](#the-tiers)):".
    - `:363` and `:370`: "(at the merge of `084cf7a8`)" instead of "(the ruling's head)".
- **R837-16-R2** (`docs/design/SPLIT_CONTROL_MEMORY.md:2003`, the 2026-11-05 record, sibling of R837-14-R1): "Once SRP's tick has counted more than `CTRL_LOOP_TX_AGE` (two) centiseconds while it is held, the next pass … was the build's alone".
  - `CTRL_LOOP_TX_AGE` is defined nowhere under `sw/` or `tb/` at the head, nor at `66f71326`. It was removed on 2026-11-06 (`a5f05f89`), before the PR's base. So the removed-constants sweep's stated reach ("defined at `66f71326`") correctly excludes it, and that claim stays exact.
  - The present tense still reads as a live rule. Exact fix: "Once SRP's tick had counted more than `CTRL_LOOP_TX_AGE` (two) centiseconds while it was held".
- **R837-16-R3** (PR body line 265, 13.3): "ran on a clean clone of the final head `234bc149`" and "ran at the final head". The SHA is given and the text sits under Round 13, so it is not misleading. But it is the only other place where "the final head" means a head other than `07ed787e`. Exact fix: "of round 13's final head `234bc149`" and "ran at that head".

## Suggestions (optional)

- **R837-16-S1 (Tests):** `rows_tiers.py:934-935` plants both interface legs at once and requires `len(tx_statements(...)) == len(POINTS)`. A defect that emitted two findings for one point and none for the other would satisfy the count. `flip_grade.py:172-184` already plants each leg alone and requires the refusal at its own point; my probe shows both controls catch a `tx_statements` that skips 8x8/2if. Optional: key the `rows_tiers` control on each point's finding, as `flip_grade`'s is.
- **R837-16-S2 (Docs/Tests, evidence):** the head's one-interface image sizes rest on two things:
  - `author-r12/receipts/images/rom-per-image.txt` at `fe0cef5b`: 111,024, 116,072, 124,528 and 129,624 B.
  - Round 13's statement that `c274b9f5` changed `ctrl_loop.o`, the ELF and the binary "at equal sizes". The binaries' sha256 differ between `30a01422` and `c274b9f5` for exactly the four one-interface images.

  No published receipt gives a size at `c274b9f5` or later. The cause makes equal sizes near-certain: `CTRL_LOOP_SLICE_US` went from 900 to 950 at one interface, and both fit RISC-V's 12-bit immediate. Even so, a `rom-per-image` line at the head would turn the inference into a receipt. The two-interface binaries are sha256-identical from `30a01422` through `b6f5c638`, so 112,312, 117,384, 125,792 and 130,920 B are proven by identity.
- **Retained, causes unchanged by this delta** (as R837-15 lists them; the delta since `fe1fd541` does not touch them):
  - R837-15-S1 (`:2275`) and S2 (`:483`): base text, known, not this PR's;
  - R837-14-S1's `:2300`;
  - R837-14-S3;
  - R837-10-S1, R837-10-S3, R837-7-S2 and R838-8-S1.
- **Known, not this PR's:** #916.

## Prior findings at this head (resolved after my own pass)

| Finding | State at `07ed787e` | Evidence |
|---|---|---|
| R837-15-F1 (`:370` gave the platform's 130,328 B and 744 B as current) | **Closed at cause** | `:370` reads "holds 130,920 B of `rom` in 131,072 at the head, 152 B before the granule its ledger's 60.0 holds (130,328 B and 744 B at the ruling's head)". This equals `:368`, `:2494` and body Status lines 59 and 125. Source: `rom-per-image.txt` `platform-8x8-2if … 130920`, with the 8x8/2if platform binary sha256-identical from `30a01422` to `b6f5c638` (`e4048efd…`). Arithmetic: 131,072 − 130,920 = 152, and 64 + 56 half-tiles = 60.0. The cause, section 5 outside the byte read, is closed by S3: `receipts/byte_scan_pr.tsv`, my own read, covers every section-5 sentence the PR writes. |
| R837-15-F2 (PR body named `41ca9f87` as the head and R837-14-F1 as unfixed) | **Closed at cause, but for F1 above** | Status, How-to (`# 07ed787e`), the final-pass sentence and the gate table name `07ed787e`. The R837-14-F1 row reads "Fixed in the tree at `fe1fd541` … round 20's packet, `receipts/local-fe1fd541/` (26 commands, rc 0)". Those receipts exist in the public tree: 26 rc lines, all 0. REVIEW READY issuecomment-6897091854 gives the full SHA. The final-pass paragraph's hooks clause is a further instance of the same class, not one of F2's four sites: R837-16-F1. |
| R837-15-R1 (`follow-context,,`) | **Closed** | 0 occurrences in the live body. |
| R837-15-R2 ("824 hits at the head") | **Closed** | Body 18.3 reads "Its 824 hits at `4ae887a1`". |
| R837-15-R3 (`:2006` "the head's behaviours") | **Closed** | `:2006` reads "Three of that head's behaviours were kept by where the work then stood, each found against its own trace". |
| R837-15-S3 (section-5 byte read), S4 (case-sensitivity) | **Taken** | `author-r21/receipts/s5-byte-sentences.tsv` (24 sentences). Body 19.2 item 3 reads "each matched case-sensitively as written". |
| R837-14-F1 (`:2382` 110,800 B as the head's) | **Still closed** | `:2382` gives 111,024 B, 55,152 B and 41.0 RAMB36, with 110,800, 110,576 and 40.5 as history. Arithmetic: 55 + 27 half-tiles = 41.0. |
| R837-14-F2 (sweep reach) | **Still closed** | 19.2's reach and limit text is unchanged since R837-15 closed it. The sweeps reproduce identically (below). |
| R837-14-R1 to R8, S1, S2; R837-13-F1 to F6, R1 to R4 | **Still closed** | `07ed787e` touches only `:335`, `:346-348`, `:363-370` and `:2006`, and reverts none of them. `:2304`, `:2310`, `:2382`, `:2197` and `:2246` read as R837-15 recorded them. |

## What I checked

### The code delta since `867faf1e` (round 16's `b6f5c638`, round 20's comment and docstring)

- **`ctrl_loop.h:371`:** `CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)`.
  - My `flip_grade.py --check --point 8x8/2if` gives the tx row at 98.49 ms, which rounds up to 99. At 1x1/1if the row is 33.38 ms, which rounds up to 34.
  - `rows_tiers.tx_statements(Path('.'))` returns `[]` (`receipts/gates/tx_statements.log`).
  - The constant's only firmware use is `ctrl_loop.c:203`, `_Static_assert(MBX_N_IF != 1u || …)`, so no object code changes. That agrees with round 16's 0 of 332 image files differing (`author-r16/receipts/identity/image-compare.txt`).
- **Comment-stripped code:** `aecp_mbx.h` is identical from `867faf1e` to the head. `ctrl_loop.h` differs in that one define alone (`scripts/code_tokens.py`, `receipts/code_tokens_867faf1e.txt`).
- **Tests delta:**
  - `rows_tiers.py:929-936` now requires a finding at both points with both legs planted, and none at the head.
  - `flip_grade.py:172-184` plants each leg alone and requires `CTRL_LOOP_TX_MS states 33 ms` at 1x1/1if and `states 98 ms` at 8x8/2if.
  - Mutation probe (`scripts/tx_leg_probe.py`, `receipts/tx_leg_probe.log`): with `tx_statements` patched to skip 8x8/2if, both controls escape by name (CAUGHT). At the head both escape nothing.
  - Self-tests on my clean clone: `rows_tiers.py` 1033 of 1033, `flip_grade.py` 585 of 585, `load_grade.py` 26 of 26.
- **`rows_grade.py:5,19-21` docstring:** history wording only. The method-docstring control is part of `flip_grade.py --selftest`, which passes.
- **Comment rule:** no new lane label, review round, reviewer ID or comment ID appears in the delta's source comments (`aecp_mbx.h:22-27,50`, `flip_grade.py:177-178`, `rows_tiers.py:929`).

### Present-tense bounds, figures, bytes, images and RAMB36 in every paragraph the PR writes

Rows, loads, pace and slice:

- My `flip_grade.py --check` (1x1/1if exit 0, 8x8/2if exit 1 by design) and `load_grade.py --check` (exit 0) are byte-identical to the author's round-21 receipts.
- **1x1/1if rows:** R4 13.10, first 14.66, last 127.21 (bound 130), R4L 188.48, ACMP 28.95, tx 33.38 and txL 48.43 ms.
- **8x8/2if:** the first queued notice is 20.93 ms.
- **Load:** 0.516 and 0.512.
- **Slice:** `tier_grid.py`'s choice, 950 us.
- **Where these are read:** FR_NFR 3.4.1 (`:383`, `:387`, `:390`), section 13, `aecp_mbx.h`'s comment, the harness README (`:188`, `:1490`) and the PR body's Status table. All agree, or give an older figure as history.

Bytes and RAMB36:

- `scripts/byte_scan.py` lists every sentence with a byte, KiB, RAMB36, tile, granule, spare or ledger figure, on a line changed since `cec88385`, plus every such sentence in the PR body (`receipts/byte_scan_pr.tsv`: 94 sentences). I read all of them:
  - section 5: 18;
  - section 13: 23;
  - sections 3 and 6: 3;
  - FR_NFR: 1;
  - PR body: 49.
- **Section 5's table, against `rom-per-image.txt` and the identity chain:** every present-tense cell is the head's, and every RAMB36 cell checks out at half-tiles of 2,048 B. The 1x1/1if fixture is 111,024 / 55,152 B, 55 + 27 half-tiles = 41.0. The 8x8/2if fixture is 125,792 / 113,168 B, 62 + 56 = 59.0. The 8x8/1if platform is 129,624 / 97,264 B, 64 + 48 = 56.0, its `sram` in 98,304.
- **`:335` and `:370` `ctrl_plat`:** 17,536, 19,008, 18,176 and 20,288 B. These equal the head's `sw/litex/ctrl_memory_ledger.py:35` and `ctrl_memory.py:263`.
- **`:361`'s 6,144 B:** this equals 16 × (576 − 192). `struct aecp_owed` is `alignas(64)` with 552 + 8 + 2 B (`aecp.h:263-268`), so a slot is 576 B against 192 B at 128 B.
- **`:2214`, `:2302`, `:2304`, `:2310`, `:2466`, `:2469`, `:2475-2476`:** history-framed, or code descriptions.
- **`:2482`, `:2494`, sections 3 and 6:** consistent with the head.
- **What the read found:** R1 (labels around correct figures). No present-tense superseded figure, byte count or RAMB36 statement.
- **Section 13 lines `:1996-2006`:** past tense, with the head's 34 and 99 ms and 49 ms beside the pre-tiers 44 and 176 ms. One tense residue remains (R2).

### The four sweeps' completeness claims

- I re-ran the author's round-21 scripts at the head: `constant_history`, `figure_sweep`, `figure_classify`, `removed_constants`, `removed_classify`, `retired_artifacts` and `retired_classify`. I read their I/O first; they only read git and write the named outputs.
- Every output is byte-identical to the published receipts (`receipts/sweeps-sha256.txt`):
  - 126 snapshots and 73 constants moved;
  - 828 hits: sweep 1 has 261 (137 historical, 58 beside the head's figure, 8 the head's own, 50 another quantity, 8 #916), and sweep 3 has 567 (315, 28, 7, 217);
  - 0 unclassified, and "current with a superseded figure: 0";
  - 10 constants gone, 8 lines naming one, current 0;
  - 1 file deleted, 15 lines naming it, current 0.
- These equal the REVIEW READY's 261, 567, 8 and 15, and body 20.6's split.
- Hits on the delta's lines (`:361`, `:2004`) are correctly classed.
- Each sweep's stated reach and limit is exact as stated. R2's `CTRL_LOOP_TX_AGE` sits outside sweep 2 by its stated reach, so the completeness claim stays true.

### Gates on a clean clone of `07ed787e` (0 changed paths after)

| Gate | Result |
|---|---|
| `docs_check.py` | rc 0: 0 findings, 219 md files |
| `check_em_dash.py`, base `66f71326` | rc 0: 0 findings, 2,393 lines, 28 pages |
| `check_em_dash.py`, base `867faf1e` | rc 0: 0 findings, 90 lines, 3 pages |
| `check_em_dash.py`, base `41ca9f87` | rc 0: 0 findings, 31 lines, 1 page |
| `check_doc_style`, `check_gptp_docs`, `check_doc_paths`, `check_archive` | rc 0 |
| `check_solution_docs`, `check_submodule_docs`, `check_feature_status` | rc 0 |
| `check_todo_ownership`, `check_hygiene`, `check_py_idiom` | rc 0 |
| `git diff --check 66f71326 HEAD` | rc 0 |
| `flip_grade.py --check` | 1x1/1if rc 0; 8x8/2if rc 1 by design |
| `load_grade.py --check` | rc 0 |
| `tier_grid.py --point 1x1/1if` | rc 0: 950 us chosen |
| `rows_tiers.py`, `flip_grade.py`, `load_grade.py` `--selftest` | rc 0: 1033/1033, 585/585, 26/26 |

The em-dash renderer was installed in a scratch-local virtual environment from `tools/markdown/requirements.txt` with `--require-hashes`. Host paths in those logs are redacted.

### Hosted evidence (inspected, not accepted; the manager owns it)

At read time, 22 check runs at the exact head (`receipts/hosted-check-runs.tsv`):

- 5 completed success: `bdd-conformance`, `changes`, `elaborate-gates-0`, `docs-check-no-git` and `docs-gates-0`;
- 4 in progress;
- 13 queued.

No completed failure.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_loop.h:371` against the tx rows (33.38 and 98.49 ms, rounded up); `FR_NFR.md` 3.4.1 `:380-394` against `flip_grade.py --check` and `load_grade.py --check`; `aecp_mbx.h:22-27,50`; section 5 `:265-273`, `:335-348`, `:361-372` against `rom-per-image.txt`, the image identity chain and `ctrl_memory_ledger.py:35` | R837-16 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| RTL | CLEAN | `receipts/name_only_867faf1e.txt`: no HDL, constraint or SoC file in the delta. `CTRL_LOOP_TX_MS`'s only firmware use, `ctrl_loop.c:203` (a 1x1-only `_Static_assert`). `receipts/code_tokens_867faf1e.txt`. `author-r16/receipts/identity/image-compare.txt` (0 of 332 differ) | R837-16 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| Robustness | CLEAN | No runtime path changes: `ctrl_loop.c:203` is compile-time only, the images are identical (r16 identity), and `aecp_mbx.h` code is unchanged. The 8x8/2if statement is held by `flip_grade.py:172-184` and `rows_tiers.py:929-936`, including the leg-skipped fault (`receipts/tx_leg_probe.log`) | R837-16 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| Tests | CLEAN | `rows_tiers.py:929-936`, `flip_grade.py:172-184`, `rows_grade.py:5,19-21`; the mutation probe; the three model self-tests (1033, 585, 26); the four sweeps reproduced byte-identically (`receipts/sweeps-sha256.txt`). S1 is optional | R837-16 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| Docs | UNCLEAN (R837-16-F1) | Live PR body (sha256 of the packet's `PR-BODY.md`, `57ad272a…`), Status, How-to, final pass and gate table; `SPLIT_CONTROL_MEMORY.md` sections 5 and 13 (`receipts/byte_scan_pr.tsv`, 94 sentences read); `FR_NFR.md` 3.4.1; harness README `:188`, `:1490`; the docs gates on a clean clone. R1 to R3 are residue | R837-16 | `07ed787ee0448be2360f97e8af01194a499003ee` |

## Real limits

- **No firmware image was rebuilt.**
  - The head's image sizes rest on `rom-per-image.txt` at `fe0cef5b` and on the sha256 identity tables of rounds 12 to 16.
  - The one-interface images carry round 13's "equal sizes" claim plus the immediate-width argument (S2).
  - From `b6f5c638` to the head, the code is unchanged by my comment-stripped comparison and the author's token-stream receipts.
- **No harness, campaign, sweep-suite, builder, Yosys, Vivado, act or hosted run was executed by me.** Round 13's measurements are carried as their receipts state.
- **Not executed or not shown here:**
  - no manager source bank runs at this head;
  - physical calibration NOT RUN;
  - field skips are not hardware proof;
  - 8x8/2if rows are reported only, by decision (#890).
- **Prior suggestions** that need code (R837-10-S1, R837-10-S3, R837-7-S2, R838-8-S1, R837-14-S3) are carried as R837-15 lists them. I did not re-derive them.

## Pending manager duties

- Route R837-16-F1 to the author, and carry R1 to R3 to the residue checklist.
- Hosted contexts at the exact head: 17 of 22 were queued or in progress when read.
- The current-dev merge candidate's builder and native banks at the merge turn. Source base `66f713267f201d1a00d7f711e04b3a996d804dee`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`.
- The external review, and merge authorization from the maintainer.

## Receipts and scripts

Listed in `MANIFEST.sha256`:

- **Scripts:** `scripts/byte_scan.py`, `scripts/code_tokens.py`, `scripts/tx_leg_probe.py`.
- **Receipts:**
  - `receipts/gates/*.log` and `*.rc`;
  - `receipts/byte_scan_pr.tsv`, and `receipts/byte_scan.tsv` (base `66f71326`, which includes base-branch text);
  - `receipts/code_tokens_867faf1e.txt`, `receipts/name_only_*.txt`;
  - `receipts/sweeps-sha256.txt`, `receipts/tx_leg_probe.log`;
  - `receipts/hosted-check-runs.tsv`, `receipts/clone-verify.txt`.

The review clone is at the exact head after the probes: 0 changed paths; the index's (mode, sha, path) equals HEAD's tree (sha256 `2b9aa980…`); the six gitlinks and checkouts are as recorded (`receipts/clone-verify.txt`). All probes ran on a separate disposable clone under `scratch/`, which is not published.

R837-16 FINISHED
