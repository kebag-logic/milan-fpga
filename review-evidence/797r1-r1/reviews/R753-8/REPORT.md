[R753] POSITIVE - exact head 06c89f1d48c73ec1977791f2a2c4f99579ae4853

Round R753-8 is the internal cleared-context review of PR #825 (issue #797, register reference). It is a delta review of exact head `06c89f1d48c73ec1977791f2a2c4f99579ae4853` (tree `40c99b22fcee5e4b9e182bef92c3512485d66168`) against round 7 at `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33`. Source base `1e80128f`; live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`, which is the PR's one merge base (`receipts/ls_remote.log`, `receipts/integrity.txt`).

**Why POSITIVE:** R753-7 F1 (MINOR, Conformance and Docs) is resolved by option (a). Every point of its verification holds at this head, and I confirmed each one myself. The delta adds no BLOCKER, MAJOR or MINOR. One RESIDUE (receipt-table wording) and one new SUGGESTION are recorded below, and the round-7 suggestions are retained as optional.

## Order of work

1. I re-read the contract (AGENTS.md sections 6 and 7, CONTRIBUTING's review bar), issue #797's frozen acceptance, and the inventory rule at `scripts/docs_inventory.py:20-38`.
2. Independent pass over `git diff 1de759d3..06c89f1d`, then my own probes.
3. Author receipts `review-evidence/797r1-r1/author-r8` at evidence commit `d0fabcdc0bb85e7cfd272b52485a6a0fc5a2b469`, verified by hash.
4. The PR body at the head, read through the GitHub API (`receipts/pr825.json`).
5. Only after that, the round-7 public reports: R753-7 (comment 6720354516) and R754-7 (comment 6720338707), copied to `receipts/prior_R753-7.md` and `receipts/prior_R754-7.md`.

## The delta

There is one commit, `06c89f1d`. It changes two files: `scripts/docs_inventory.json` (-111 lines) and `docs/DOCUMENTATION_AUDIT.md` (+2/-17). The commit message is one line with no trailers.

- **Data file** (`receipts/json_delta.log`, script `scripts/json_delta.py`):
  - `findings` goes from 65 to 50. Exactly 15 IDs are removed: D0-006, -007, -008, -014, -015, -016, -017, -018, -041, -042, -043, -044, -058, -059 and -060. None is added.
  - The 50 surviving entries are byte-identical to the parent's.
  - Everything outside `findings` (`verified_at`, `cited_at`, `verified_pages`, `judged`) is unchanged.
- **Generated page:**
  - The diff removes 15 Findings rows and rewrites the two page-table rows (`docs/DOCUMENTATION_AUDIT.md:313-314`). `REGISTER_MAP.md` now reads `stale | 1 finding(s): D0-057` and `REGISTER_MAP_CLASSES.md` reads `stale | 1 finding(s): D0-040`.
  - No other row moved, so no copy row of a kept ID lost its coverage.
- **Copy rows** (`receipts/prior_rows_removed_ids.log`, `receipts/also_fields.log`, `receipts/removed_quotes.log`, script `scripts/removed_quotes.py`):
  - At the parent, each removed ID had a row only on its own page. No copy row existed on any other page, which is the removal condition at `scripts/docs_inventory.py:27-28`.
  - Two removed entries carried `also` spellings: D0-058 had "**Nothing in this device persists a binding across a power cycle.**" and D0-059 had "is **not met by this build**". The first is D0-040's statement with its closing period, which normalisation strips. D0-040 still finds the same four history-page copies at the head (`docs/DOCUMENTATION_AUDIT.md:487-488,491-492`), so removing D0-058 does not stop any copy from being found.
  - The quotes of 14 of the 15 removed entries appear in no tracked Markdown file at the head.
  - The fifteenth, D0-018's quote (the `0x7C8–0x7D4` row), stays on `REGISTER_MAP_CLASSES.md:101` by design. Its correction, the `0x7D8` ETH_GUARD row with class **needed**, is at `:102`. That row agrees with the RTL: `hdl/common/csr/milan_csr.sv:897` (`A_ETH_GUARD = 'h7D8`), `:1731` (the magic write `32'h554E_4C4B` disarms, any other write re-arms) and `:2389` (readback).
- **Kept IDs:**
  - D0-040 has its own row plus 4 copies; D0-057 has its own row plus 7 copies.
  - This matches the PR body ("D0-040 on four, D0-057 on seven").

## R753-7 F1: its verification, point by point

| Verification as written | Result at `06c89f1d` | Receipt |
|---|---|---|
| `docs_inventory.py --check` rc 0 | rc 0, "docs/DOCUMENTATION_AUDIT.md is fresh" (533 lines) | `receipts/inv_check.log`, `.rc` |
| `docs_inventory.py --selftest` rc 0 | rc 0, 60 controls | `receipts/inv_selftest.log`, `.rc` |
| The "re-verify: quote not found" count drops by the removed entries | 19 → 5 in total; 16 → 2 on the two pages. 14 of the 15 removed IDs read "re-verify"; D0-018 read "on page" | count in the session, reproduced by the author's `receipts/lane/f1_verification.txt` |
| No row of a removed ID remains | Zero hits for each of the 15 IDs anywhere in the tree outside the data file, and zero inside it | `receipts/json_delta.log`, `receipts/removed_id_grep.log` |
| Each page is stale only through D0-040 or D0-057 | `:313` lists only D0-057; `:314` lists only D0-040. The five remaining re-verify rows are D0-001, -033 and -056 (other pages and lanes) plus D0-057 and D0-040 | `docs/DOCUMENTATION_AUDIT.md:473,494,515,529,530` |
| The PR body's Fixed sentence matches the ledger | Line 52 names 17 fixed statements: D0-006 to -008, -014 to -018, -040 to -044 and -057 to -060. That is the 15 removed plus D0-040 and D0-057, whose quotes are gone from these pages. Line 56 lists exactly the 15 removed. Line 57 names the two kept IDs and their copy counts. Line 58 drops D0-009, which dev removed in `859ab22a` (an ancestor of the head) | `receipts/pr825.json` |

F1 is **resolved**.

## Probes

- **P-A: restore all fifteen entries, then regenerate** (`scripts/probe_restore_all.sh`, `receipts/probe_restore_all.log`, run on a disposable clone of the exact head):
  - With the data file restored and the page not regenerated, `--check` gives rc 1.
  - After `--write`, `--check` gives rc 0, and the regenerated pair is byte-identical to the parent head.
  - So the regeneration is deterministic, and the head's pair is exactly the parent's pair minus the 15 entries.
  - It also shows that the gate does not enforce the removal rule itself. Round 7 caught the leftover entries by review, not by `--check`. That gate is dev's (#815), so this is a limit of the gate and not a defect in this lane (see S4).
- **Author plants P0 to P7** (`author-r8/receipts/plants/SUMMARY.txt`): all give the expected rc. P3 (restore D0-018 alone) and P4 (drop the kept D0-040) each exit 1, and the controls P0 and P7 exit 0. I verified them by hash and did not re-run them, because P-A covers the same failure direction.
- **Own gates at the head:**
  - `scripts/check_doc_style.py` rc 0 (25 current documents);
  - `scripts/docs_check.py` rc 0 (0 findings across 215 md files);
  - `git diff --check 1de759d3 HEAD` rc 0.
- **Consumers of the changed files:** only the docs workflow, `scripts/check_doc_style.py:39` and the `scripts/ci_events.py:1154-1155` step strings. Nothing under `tests/` reads them. So not re-running behave at this head, as the PR body says, is sound for this delta.

## Author receipts

- `author-r8/receipts/INDEX.md` lists 196 files. All 196 match in size and sha256, none is missing and none is unlisted (`receipts/author_r8_index_verify.log`). `receipts/HEAD.txt` names the exact head.
- `receipts/run/verify_docs_yml.md` reports 66 docs-workflow `run:` steps at rc 0 and 31 NOT RUN, each marked hosted-only. `verify_docs_yml.rc` = 0.

## Hosted evidence at the exact head (inspection only; the manager owns acceptance)

- All four `pull_request` runs at `06c89f1d` (rtl-fast, elaborate, rtl-full, docs) concluded `cancelled` (`receipts/hosted_runs.tsv`). Of 68 check runs: 43 were cancelled, 12 failed, 12 succeeded and 1 was skipped (`receipts/hosted_checks.tsv`).
- `docs-check` and `elaborate` failed at their "Require every gate exactly once" aggregate, with "dependent job failed, cancelled or skipped". Their shards had been cancelled (`receipts/hosted_failed_steps.log`, `receipts/hosted_docs_check_failed_tail.log`).
- `elaborate-gates-0` failed at "Install the pinned sv2v release" with exit code 22 (an HTTP error on the download), before any lane gate ran (`receipts/hosted_sv2v_failed_tail.log`).
- No hosted docs gate executed to completion at this head. These results are neither evidence against the delta nor acceptance evidence.

## Findings

### RES1 - RESIDUE - Docs - `review-evidence/797r1-r1/author-r8/receipts/run/verify_docs_yml.md:82` - the gate_41 log cell names a file that is not published

- **Evidence:** the row `docs-gates-2 | gate_41` names its log as `docs-gates-2__gate_41.log`. The published file is `docs-gates-2__gate_41.log.tail`, and `INDEX.md` lists it under that name. This is R754-7 RES2 again, carried from the round-7 handoff into the round-8 receipt table.
- **Impact:** wording in a receipt table only. The rc and the hashes are correct.
- **Exact fix:** in that cell, write `docs-gates-2__gate_41.log.tail` (a tail of the full log, whose sha256 the tail states). Fix the collector the same way, so later rounds do not repeat it.

### S4 - SUGGESTION - Robustness, Tests - `scripts/docs_inventory.py:25-28` (dev's gate, #815) - the removal rule depends on review alone

- **Evidence:** P-A. With the 15 fixed entries left in and the page regenerated, `--check` passes. The rule that a lane removes the entry it fixed is not something the gate can see.
- **Optional change, in a new Issue and outside this lane:** have `--check` or a review aid list each "re-verify: quote not found" entry that has no copy row on any page, so that leftover entries show up at the next gate run rather than at review.

### Comment rule

The delta adds no source comment. It removes data entries and regenerates a generated page, so it introduces no new bench-lane, lane, round, reviewer or comment-ID label.

## Prior findings at this head

| Item | State | Evidence at `06c89f1d` |
|---|---|---|
| R753-7 F1 (MINOR, Conformance and Docs) | **Resolved** | the table above |
| R754-7 S3 (SUGGESTION, Docs): the D0 owner should close the fixed rows | Resolved by the same change | `docs/DOCUMENTATION_AUDIT.md:313-314,529-530` |
| R754-7 RES2 (receipt-table gate_41 name) | Recurs in the round-8 receipts as RES1 | `author-r8/receipts/run/verify_docs_yml.md:82` |
| R753-7 S1 / R754-7 S1 (SUGGESTION): nothing notices a stale SoC extract | Retained, optional | `scripts/register_map_soc.json` and `scripts/gen_register_reference.py` untouched by the delta |
| R753-7 S2 / R754-7 S2 (SUGGESTION): the MAC_ADDR hold sits only in the design notes | Retained, optional | `REGISTER_MAP.md` and `register_descriptions.json` untouched |
| R753-7 S3 (SUGGESTION): the rewritten page inherits "Verified: D0" | Retained, optional | `verified_pages` still lists both pages (`receipts/json_delta.log`, non-entry content unchanged) |
| R753-7 RES1 / R754-7 RES1 (subject of `57264e30`) | Retained, residue checklist; no action possible | history |
| R753-6 S1, S2; R754-6 S1, S2; R753-5 S1; R754-4 S1, S2 | Retained, optional | files untouched by the delta |
| R753-3 RES2, R753-3 RES3, R754-3 R1 | Retained, residue checklist | pages untouched by the delta |

No prior BLOCKER, MAJOR or MINOR remains open.

## Lens results

```text
[R753] PASS Conformance - scripts/docs_inventory.json (65->50 findings), docs/DOCUMENTATION_AUDIT.md:313-314,473-533, PR #825 body lines 52-58,66 - F1 resolved against scripts/docs_inventory.py:22-28: each of the 15 removed entries is fixed and has no copy row; D0-040/D0-057 kept for 4/7 copies; Fixed sentence = ledger; D0-018 correction agrees with hdl/common/csr/milan_csr.sv:897,1731,2389
[R753] PASS RTL - git diff 1de759d3..06c89f1d (no file under hdl/, no generator, no gate); hdl/common/csr/milan_csr.sv:897,1731,2389 against REGISTER_MAP_CLASSES.md:102 - the ETH_GUARD class row that justifies removing D0-018 matches address, write rule and readback
[R753] PASS Robustness - receipts/probe_restore_all.log (stale data rc 1; regenerated equals parent bytes, rc 0), receipts/also_fields.log and receipts/removed_quotes.log (the D0-058 also-spelling is still covered by D0-040; no orphaned copy), author plants P0-P7 - S4 optional
[R753] PASS Tests - docs_inventory --selftest 60 controls rc 0, --check rc 0, check_doc_style rc 0, docs_check rc 0, git diff --check rc 0; author-r8 196/196 receipts hash-verified, 66 docs steps rc 0; no tests/ consumer of the changed files - S4 optional
[R753] PASS Docs - docs/DOCUMENTATION_AUDIT.md regenerated (fresh), PR #825 body Description/Round 8 rows, commit subject, author-r8 HANDOFF and receipts - RES1 residue only; prior S1-S3 retained optional
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/docs_inventory.json`; `docs/DOCUMENTATION_AUDIT.md:313-314,473-533`; `scripts/docs_inventory.py:20-38`; PR body lines 52-58 and 66; `hdl/common/csr/milan_csr.sv:897,1731,2389`; `REGISTER_MAP_CLASSES.md:101-102` | R753-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| RTL | CLEAN | the delta (no HDL); `milan_csr.sv` ETH_GUARD lines against the classes row | R753-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| Robustness | CLEAN (S4 optional) | P-A; copy-row and `also` analysis; author plants P0 to P7 | R753-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| Tests | CLEAN (S4 optional) | inventory `--check`/`--selftest`, `check_doc_style.py`, `docs_check.py`, `git diff --check`; author-r8 receipts (196 verified); consumer search | R753-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| Docs | CLEAN (RES1 residue; S1 to S3 optional) | `docs/DOCUMENTATION_AUDIT.md`; PR body; commit subject; author-r8 `HANDOFF.md` and `verify_docs_yml.md` | R753-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |

The delta touches only the inventory data and its generated page. The rest of the register-reference lane (generator, sweep, pages, notes, workflow, `ci_events.py`) is unchanged since `1de759d3`. Its round-7 coverage of RTL, Robustness and Tests (R753-7 and R754-7 at `1de759d3`, an ancestor of this head) still holds for those artifacts.

## Real limits

- I re-ran only the inventory, style, docs-check and diff-check gates. For the other docs-workflow steps at this head, I rely on the author's hash-verified receipts. Behave was last run at `1de759d3`, and nothing in `tests/` reads the changed files.
- The author plants were verified by hash, not re-run. My P-A probe covers the same direction.
- No builder export of my own; this delta does not touch the SoC extract.
- Hosted evidence at the exact head is not usable: all four runs were cancelled, and the aggregates failed on cancelled shards and a failed sv2v download. I did not open every failed job.
- No manager source bank ran at this head, and I infer none. Physical calibration was not run. Field skips are not hardware proof.

## Pending manager duties

- Re-run the hosted contexts at the exact head, and own hosted and act acceptance.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, against live dev `0a75aa77`, and link its receipts.
- Residue checklist: this round's RES1 (which carries R754-7 RES2), R753-7/R754-7 RES1, R753-3 RES2 and RES3, R754-3 R1.
- Optional suggestions: this round's S4 (a new Issue against dev's inventory gate); R753-7 S1 to S3 and R754-7 S1, S2; R753-6 and R754-6 S1, S2; R753-5 S1; R754-4 S1, S2.
- The external review at this head, and maintainer authorization for the merge.

R753-8 FINISHED
