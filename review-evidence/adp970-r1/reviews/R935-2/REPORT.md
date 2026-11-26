[R935] POSITIVE - exact head f4833e16a07d07494277aba8dc7a5de19320c20b

# R935-2: internal cleared-context delta review of kebag-logic/milan-fpga PR #1015 (Relates to #970)

- **Head:** `f4833e16a07d07494277aba8dc7a5de19320c20b`, tree `acc0b819bec698855f98c81f52a4a04abcde6afd` (verified in the review clone).
- **Delta judged:** `0ad0e518..f4833e16` (rounds 3 to 5). The PR's own content is `4df125b8..f4833e16`, 23 files. `77f2dc55` is a two-parent merge of `dev-soft-core` `4df125b8` (#1016). The rest of `0ad0e518..4df125b8` is #1016's content, not this PR's.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR is open. Every prior finding is resolved at its root at this head. Four RESIDUE items and three SUGGESTIONs follow, each with its exact fix.
- **All five lenses applied:** Conformance, RTL, Robustness, Tests, Docs. Each is CLEAN at this head, with its evidence in the ledger below.

## Contents

- [1. Reconstruction](#1-reconstruction)
- [2. Prior findings, resolved or retained](#2-prior-findings-resolved-or-retained)
- [3. New findings at this head](#3-new-findings-at-this-head)
- [4. Per-lens results](#4-per-lens-results)
- [5. Reviewer-owned ledger](#5-reviewer-owned-ledger)
- [6. Executed evidence](#6-executed-evidence)
- [7. Real limits and pending manager duties](#7-real-limits-and-pending-manager-duties)

## 1. Reconstruction

- **Order read:** AGENTS.md; issue #970, its body and the rulings of 2026-11-22 and 2026-11-25 (the 2026-11-26 attribution comment as context only); the PR body; the diff and history; tsn-c-stack `a795471c..c3bff8f3`; the author packet `review-evidence/adp970-r2` at evidence commit `af092a85`.
- **Packet integrity:** all 28 `MANIFEST.json` entries match their published sha256. The evidence commit and the head commit are unsigned; GitHub reports `verified: false`, reason `unsigned`. So integrity rests on the manifest hashes, not on a signature.
- **Scope in force:** ruling item 2 of 2026-11-25. Each draw mixes a fresh sample, the entity ID and the interface. The draw is uniform (IEEE 1722.1-2021 6.2.4.2.2) over Milan's ranges: 0 to 2 s at a startup (Milan v1.2 5.6.3.5.2) and 0 to 4 s at LINK_UP (5.6.3.5.3). The declared discovery time stays 6.0 s.
- **Gitlink:** `third_party/tsn-c-stack` is `c3bff8f3`.
  - It is the merge commit of tsn-c-stack PR #40 (merged, `merge_commit_sha` `c3bff8f3`, closes stack issue 39), with parents `a795471c` and `95902060`.
  - Its tree `4064709b` equals `95902060`'s, the head the stack review covered.
  - Stack `main` is identical to `c3bff8f3` (compare: ahead 0, behind 0).
- **Other gitlinks** equal the base `4df125b8`: gptp-processor `3ce71b76`, protocol-processor `801ef228`, lwSRP `d1bb4f4e`, verilog-axis `48ff7a7e`.

## 2. Prior findings, resolved or retained

These were read only after my own pass over the diff. Each is judged at its root.

| Finding | Status at this head | Evidence |
|---|---|---|
| R936-1 F1 MAJOR (Conformance, RTL, Robustness, Tests, Docs): a qualified LINK_UP took no fresh sample | **RESOLVED** at the root, in the stack | See the details below the table. |
| R935-1 F1 MAJOR (Tests, Docs): two docs-workflow gates red | **RESOLVED** | `scenario.py` is 1,000 lines. No line over 120 columns in `scenario.py`, `adp_first_mutants.py`, `ctrl_mutants.py` or `hooks.py`. `check_py_idiom.py` gives `long module: 10 <= 10` and `over-long line: 0 <= 0`. With the pinned Markdown venv, `gen_toc.py --check` reports `TOC gate: OK` and CHANGELOG:13 carries the new section. All 31 gate groups I ran exit 0, including the no-git copy and the em-dash gate from `4df125b8` (`receipts/docs-gates2/summary.txt`). Hosted `docs-check-no-git` and `docs-gates-1` succeeded at this head; `docs-gates-0/2` were in progress at my snapshot. |
| R935-1 F2 MINOR (Docs, RTL): `rom` cost stated against older figures | **RESOLVED** | `SPLIT_CONTROL_MEMORY.md:755` states +264 / +272 / +264 / +256 B. My `plat_ledger.py` runs: head 127,832 / 129,624 / 141,944 / 143,688 B; `c34e7d8b` **and** `4df125b8` both 127,568 / 129,352 / 141,680 / 143,432 B. `sram`, tiles and `ctrl_plat` are equal at all three points. One label is stale (RES2, wording only). |
| R935-1 F3 MINOR (Tests): B25 could not fail for a coarse or late-wired clock | **RESOLVED** | B25 (`test_plat_boot.cpp:1346`) now boots with clock origins 1 us apart and requires three distinct generator states. In my campaign it catches each of these by its own words: `plat-clock-in-milliseconds`, `plat-clock-1024-us-granule`, `plat-clock-wired-after-release`, `seed-clock-not-wired`, and my own `r-plat-clock-high-word`. |
| R935-1 F4 MINOR (Docs, Conformance): handoff and title claimed a seed at each LINK_UP | **RESOLVED** | The claim is now true in code (R936-1 F1 above). The title "per host, interface and link-up" matches `adp.c`. The r2 REVIEW-READY, `FR_NFR.md:221-223`, CHANGELOG:117-130 and `SUBMODULES.md` no longer defer the LINK_UP sample. |
| R935-1 R1 RESIDUE (`FR_NFR.md:222`) | **RESOLVED** | The line now reads exactly as the stated fix ("H4 to H6 ... ; H7 holds the seed's terms"). |

**R936-1 F1 in detail:**

- **The fix lives in the stack.** `third_party/tsn-c-stack/src/adp.c:99-110` `leave_down()` takes one `ports->seed` sample. It seeds `mix(mix(rng ^ (mac + sample)) ^ id ^ iface<<24)`, with zero mapped to 1.
- **Where it is called:** from `adp_set_enable` at `:256` (a startup with the link up) and from `adp_link_change` at `:274` (a LINK_UP from DOWN).
- **What takes no sample:** the guard at `:269` returns before any sample on a duplicate or disabled LINK_UP. `adp_gm_change` (`:292`) and the DISCOVER and TMR_ADVERTISE paths draw without one.
- **Draw ranges unchanged:** `draw_ms` and the xorshift32 generator are untouched in `a795471c..c3bff8f3`.
- **The adapter only supplies the sample.** `sw/firmware/ctrl/adp/adp_mbx.c:51-64`: `port_seed` returns the wired clock, or NOW_MS where none is wired. Nothing under `sw/firmware/ctrl` writes `rng`.
- **Tests through the real adapter and platform:**
  - H9 (`test_adp.cpp:1020`): one read per qualified rise, the first rise after an enable included, and one at the startup draw. None at a duplicate or disabled LINK_UP.
  - H10 (`:1052`): the enable sample is fixed and the LINK_UP sample varies; this gives 915 distinct delays of 1,024.
  - B27 (`test_plat_boot.cpp:1365`): runs at both interface counts.
- **Plants that kill the old behaviour:**
  - `link-up-not-sampled` is caught by H9 and B27.
  - `link-up-sample-ignored` is caught by H10.
  - My own `r-base-pin-link-up` is caught by H10 and by B27 in both the 1-interface and 2-interface arms.

## 3. New findings at this head

None of these changes a measurement, figure, verdict, test, code path, generated artifact or clause claim, and none touches a privacy rule.

### RES1 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:1201-1205` - the #970 block splits a two-line test statement

- **Evidence:** the #1013 block ends "Parent tests accept 57 to 2047." (`:1199`) / "They refuse 0 and 55." (`:1207`). The new "Issue #970 adopts stack pin `c3bff8f3` ..." line and its table were inserted between those two lines. So "They refuse 0 and 55." now follows the #40 table, and its subject reads as the #40 change.
- **Exact fix:** move lines 1201-1205 (the "Issue #970 adopts ..." line, the blank line and its three table lines) to just after "They refuse 0 and 55.". The #1013 text then reads as before, and #970's block follows it.

### RES2 - RESIDUE - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:755` - "this change's own base `c34e7d8b`"

- **Evidence:** after `77f2dc55` the PR's base is `4df125b8`. The figures are right at both: my ledgers give identical `rom`, `sram`, tiles and `ctrl_plat` at `c34e7d8b` and `4df125b8`. Only the label is stale.
- **Exact fix:** replace "against this change's own base `c34e7d8b`" with "against `c34e7d8b` and this change's base `4df125b8`, which take the same figures".

### RES3 - RESIDUE - Docs - `sw/firmware/ctrl/test/adp_first_mutants.py:121` - a source comment names review activity

- **Evidence:** the comment reads `# #970, the reviews of PR #1015: each qualified rise samples, through the adapter and the platform`. It was new in `25aaf510`, inside the reviewed delta. The comment rule allows behaviour and reason with issue and requirement IDs, and no review rounds.
- **Exact fix:** `# #970 (IEEE 1722.1-2021 6.2.4.2.2; Milan v1.2 5.6.3.5.3): each qualified rise samples, through the adapter and the platform`.

### RES4 - RESIDUE - Docs - author packet `review-evidence/adp970-r2/author/REVIEW-READY.md` section 2, and the PR body's CPU-leg rows - the legs' base is described inexactly

- **Evidence, base images:** REVIEW-READY says the legs ran "against base `5de21ff3`, whose images and simulated hardware equal the merged base's". The PR body says only "against the base".
  - My loadable images at `c34e7d8b` and `4df125b8` have the same size and differ in exactly 3 bytes, all inside `adp_rx` (`receipts/image-identity.txt`, `receipts/image-diff-adp_rx.txt`).
  - Those bytes are #38's comparison: `li a4,56; bne` becomes `li a4,55; bge`.
  - The instruction count is the same, and the legs' 56-octet ENTITY_DISCOVER takes the same path. So no leg's figure changes; the sentence is inexact, not the measurement.
- **Evidence, log paths:** the packet also says "Logs: `receipts/r5/milan/`" and "`receipts/r5/attribution/`", but the published paths are `receipts/milan/` and `receipts/attribution/`.
- **Exact fix:**
  - REVIEW-READY: "against base `5de21ff3`, whose images equal the merged base's but for #38's one comparison in `adp_rx` (3 bytes, the same instruction count, a path no leg's probe takes differently)".
  - The log lines: `receipts/milan/` and `receipts/attribution/`.
  - PR body: "CPU budget legs against `5de21ff3`" in both rows.

### S1 - SUGGESTION - Tests - `sw/firmware/ctrl/test/test_adp.cpp:1052` (H10) - the distinct-delay floor is loose

- 1,024 uniform draws over 4,001 values give about 904 distinct values; 915 were observed.
- The floor is `>= 600`. That catches a constant or collapsed sample (`link-up-sample-ignored` gives 1), but not a sample that has lost a few of its low bits.
- A floor near 850 would also catch partial-entropy defects. This is optional, because the chi-square arm and B25/B27 already hold the platform's resolution.

### S2 - SUGGESTION - Docs - `sw/firmware/ctrl/adp/adp_mbx.h:23-26` - the comment breaks after "and seeds its"

- The THE DRAW comment breaks mid-sentence after "and seeds its". Reflowing the paragraph would read better.

### S3 - SUGGESTION - Conformance (outside the delta, for a separate issue if wanted) - the 16-bit draw step

- `draw_ms` (`adp.c:53-62`, unchanged here) maps `rng >> 16` by `(r16 * (max+1)) >> 16`.
- So each millisecond value receives 16 or 17 of the 65,536 inputs, about 6 % relative unevenness, which no 1,024-draw chi-square can see.
- This is pre-existing, unchanged by this PR, and not a finding against it. A 32-bit multiply-shift would remove it if the owner wants IEEE 1722.1-2021 6.2.4.2.2's "uniform" taken literally.

## 4. Per-lens results

```text
[R935] PASS Conformance — third_party/tsn-c-stack@c3bff8f3 src/adp.c:53-62,99-110,238-294; sw/firmware/ctrl/adp/adp_mbx.c:51-64; docs/reference/FR_NFR.md:199-223 — one fresh sample at each transition out of DOWN (startup with link up, qualified LINK_UP), none at duplicate/disabled LINK_UP, GM change, DISCOVER or TMR_ADVERTISE; seed = (mac + sample) mod 2^32 mixed with entity ID and interface (IEEE 1722.1-2021 6.2.4.2.2; ruling 2026-11-25 item 2); draw ranges 0-2 s / 0-4 s unchanged (Milan v1.2 5.6.3.5.2, 5.6.3.5.3); declared 6.0 s and the 4,311 ms sum unchanged; GM change still announced (G4 passes in the ADP slice, 84 checks); the gitlink is the merge commit c3bff8f3, tree-equal to the reviewed 95902060.
[R935] PASS RTL — git diff --stat 4df125b8..f4833e16 (no hdl/ file; gptp-processor and protocol-processor gitlinks unchanged); receipts/ledger-{head,4df125b8,c34e7d8b}.log; adp_mbx.h:123; MAILBOX_SPLIT.md:697 — no RTL in the delta; firmware contracts: the new adp_mbx_set_clock seam is file-scope, outside the ledgered struct; ADP_MBX_LAT_LINK 12 equals the measured C0 (12, bound 12); platform LINK_UP probe stays 11 accesses (the clock is not a mailbox access); rom +264/+272/+264/+256 B, sram, tiles and ctrl_plat unchanged at four points, all PASS; base images c34e7d8b and 4df125b8 differ only in #38's 3 bytes; CPU legs from the author's receipts: 1x1 75 paired, 0 misses; 8x8/1if 90 paired, the same 7 known misses on both sides, 0 over the share.
[R935] PASS Robustness — tsn-c-stack src/adp.c:108,243-283; test_adp.cpp:1020 (H9), :1052 (H10); test_plat_boot.cpp:1346-1411 (B25-B27), :350-353 — duplicate and disabled LINK_UP sample nothing; re-enable with link up samples once; link loss then rise samples afresh (H8, B27); a seed that mixes to 0 starts at 1 (A22, plant seed-left-at-zero caught); no clock wired falls back to NOW_MS and still spreads (H6, plant seed-fallback-constant caught); the clock seam is cleared at each modelled reset; another interface's generator is untouched by a rise (B27); cosim shutdown at 32 s holds for any draws (LINK at 50 ms + 4 s + 3 x (5 s + 4 s) = 31.05 s; a GM change or DISCOVER in WAITING only shortens a cycle).
[R935] PASS Tests — receipts/fw-gate.log (85 suite verdicts PASS, ADP slice 84, boot if1 59 / if2 60), receipts/draw-plants.log, receipts/fw-coverage.log — the full plant table (865) names every host test (0 unnamed); the 26 draw-table plants plus seed-left-at-zero are all caught by their named test's words; 4 of 5 reviewer plants are caught as named (r-clock-read-twice by H9; r-base-pin-link-up by H10 and B27 at both interface counts; r-plat-clock-high-word by B25 and B27; r-plat-clock-cached by B27). The fifth, r-base-pin-semantics, was caught by H9 as named; its second expectation, on H10, was this reviewer's plant-design error, since that plant keeps the LINK_UP sample, so H10 rightly passes. Coverage ratchet PASS, 40 files.
[R935] PASS Docs — receipts/docs-gates2/summary.txt (31 gate groups exit 0: docs_check, no-git docs_check + feature_status, em-dash from 4df125b8, doc_style, submodule_boundaries/docs, diagram_pngs, py_idiom, toc, docs_inventory and the rest); FR_NFR.md:220-223; MAILBOX_SPLIT.md:540-544,697; SPLIT_CONTROL_MEMORY.md:755; SUBMODULES.md:27,1201-1205,1251,1296; CHANGELOG.md:13,117-130; tb/verilator/mbx/README.md, ctrl_reboot/README.md:120 — each changed contract is stated and matches code and receipts (reboot 92.325 ms, cosim 33 s, LINK_UP 12); RES1-RES4 are wording only and carried as residue.
```

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | stack `src/adp.c:53-62,99-110,238-294` at `c3bff8f3`; `adp_mbx.c:51-64`; `FR_NFR.md:199-223`; #970 rulings; PR #40 merge state | R935-2 | `f4833e16a07d07494277aba8dc7a5de19320c20b` |
| RTL | CLEAN | diff stat (no HDL); gitlinks; `adp_mbx.h:123,161-164`; `ctrl_plat.c:135-140,401`; three ledgers; image identity; author CPU-leg receipts | R935-2 | `f4833e16a07d07494277aba8dc7a5de19320c20b` |
| Robustness | CLEAN | `adp.c:243-283`; H6/H8/H9/H10; B25-B27; `test_plat_boot.cpp:350-353`; `cosim_main.cpp:234-251` | R935-2 | `f4833e16a07d07494277aba8dc7a5de19320c20b` |
| Tests | CLEAN | `test_adp.cpp:857-1074`; `test_plat_boot.cpp:304-353,1343-1411`; `adp_first_mutants.py`; `ctrl_mutants.py:340-341`; my gate, plant and coverage receipts | R935-2 | `f4833e16a07d07494277aba8dc7a5de19320c20b` |
| Docs | CLEAN (RES1-RES4 carried) | CHANGELOG, FR_NFR, MAILBOX_SPLIT, SPLIT_CONTROL_MEMORY, SUBMODULES and its diagram/manifest, DOCUMENTATION_AUDIT, mbx and reboot READMEs; my docs-gates2 run | R935-2 | `f4833e16a07d07494277aba8dc7a5de19320c20b` |

## 6. Executed evidence

Every run below was against the exact head in the review clone, unless a base point is named. Receipts are under `receipts/`.

| Run | Result |
|---|---|
| `test_ctrl_firmware.py --require-rv32 --jobs 4` | PASS, 85 suite verdicts (`fw-gate.log`, `fw-gate.rc` = 0) |
| `scripts/draw_plants.py` (the repository's own `plant()`/`campaign()`; 27 table plants + 5 reviewer plants) | full table 0 unnamed; 27/27 table plants caught; reviewer plants as in section 4 (`draw-plants.log`) |
| `fw_coverage.py --check --jobs 8` | PASS, 40 files (`fw-coverage.log`) |
| `plat_ledger.py` at head, `4df125b8`, `c34e7d8b` | PASS at four points each; figures as in section 2 (`ledger-*.log`, rc 0) |
| Image identity, `objcopy -O binary` of each point's `ctrl_app.elf` | `image-identity.txt`, `image-diff-adp_rx.txt` |
| `scripts/docs_gates.sh`, run with the pinned Markdown venv | 31 of 31 exit 0 (`docs-gates2/`). A first run without the renderer failed 3 groups for missing packages only; it is superseded and not published. |
| Hosted check snapshot at head (read-only) | 15 success, 1 skipped, 43 queued or in progress (`hosted-checks-snapshot.tsv`); the manager owns acceptance |
| Restore check | HEAD and tree exact; 0 porcelain lines including submodules; index equals the HEAD tree in mode, blob and path; gitlinks as in section 1 (`restore-verify.txt`). Every disposable worktree I created was removed and pruned. |

## 7. Real limits and pending manager duties

- **Not re-run by this review:** the CPU budget legs, the split boot simulations, the co-simulation, the reboot simulation, the twin and its plants, the hooks self-test and the memory plan tests. For these I relied on the author's manifest-verified receipts. My own checks were the cosim's 32 s bound (by arithmetic), the reboot README figure against `reboot.log`, and the legs' base identity (RES4).
- **The legs' base `5de21ff3` was not built by me.** Its `rom` equality with `c34e7d8b` is from the earlier public round. My byte comparison covers `c34e7d8b` against `4df125b8`.
- **No manager source bank ran at this head, and none is claimed.** The current-dev merge candidate (source base `4df125b8`, live dev `e275d795`) and its builder and native banks are the manager's at the merge turn.
- **Hosted contexts:** exact-head `verilator-suites` and `yosys-portability`, and hosted/act acceptance, are pending and owned by the manager.
- **No hardware proof:** physical calibration was NOT RUN, and the bench re-run of the affected discovery scenarios (an acceptance item of #970, which this PR relates to and does not close) is not covered. Field skips are not hardware proof.
- **Residue to carry:** RES1-RES4 go to the residue checklist.

R935-2 FINISHED
