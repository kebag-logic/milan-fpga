[R476] POSITIVE - exact head 80b3c1b223aaad05f428164cd56595a4c1187509

# R476-3 internal independent review: processor issue #148 / PR #159, delta round

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #159, branch `pp148-notify-spacing`.
- **Exact head:** `80b3c1b223aaad05f428164cd56595a4c1187509`, tree `81a6a14162632f51a504005066f10bde891a8819`. Both were verified in the isolated detached clone. The parent is `356c1bbad2e9838659b433736040acf0cc4abf3e`, the R476-2 head.
- **Source base:** `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`.
- **Review start:** PR #159 comment 5989014977.
- **Scope of this round:** the delta `356c1bba..80b3c1b2`, which is one manager commit. The lens verdicts from R476-1 (at `bed5f477`) and R476-2 (at `356c1bba`) stand unless this delta touches them.

**Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open.

- **The delta is what it claims to be.** It changes only the context lines of `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch`, and the hunk header becomes `@@ -1233,10 +1233,11 @@`. The `-`/`+` lines are unchanged.
- **The patched arm is unchanged.** Planted at this head, the patch produces a design that differs from the original planted at `bed5f477` only in the reworded comment.
- **R476-2-F1 = R477-2-F1 is resolved.** All 440 of 440 planting arms plant at this head; at `356c1bba` only 439 did.
- **The full ctr campaign re-ran at this head.** Control PASS and 17 of 17 KILLED, rc 0. All 19 records, including every failing-check line, are identical to the published head record. `ctr-notify-one-window` fails 4 checks: K15 x2 (named), K16 and K17.
- **Two wording-only RESIDUEs remain, both in the PR body.** R476-2-R1 is retained in part, because its item 2 was not applied. R476-3-R1 is new. Neither makes the verdict NEGATIVE.

## 1. Reconstruction (order followed)

1. **Contributor guidance.**
   - The repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head.
   - The conventions come from `README.md` and `docs/README.md`.
   - The mutation-campaign rules are in the `tb/pp_top` README §"GET_COUNTERS face controls" (`tb/pp_top/README.md:1398-1444`): an arm is a reviewed patch, applied with `git apply` to a scratch copy, and is KILLED only when its run completes, fails and prints its named check.
2. **Frozen acceptance and scope.** Issue #148's body sets three acceptance items:
   1. The spacing is measured send to send.
   2. A check is red on today's behaviour, with a selection-restart mutant.
   3. The existing notification suites and campaigns stay green.

   The manager comments set the rest of the scope. Comment 5982500256 sets the gates, including "the notify, ctr and pp_top campaigns at their counts". Comments 5985998608 and 5986055260 set the round-1b union. Comment 5988897133 is the manager's commit `356c1bba`.
3. **Authorities.**
   - Milan v1.2 §5.4.5, Table 5.22 (`T-CTR-NOTIF`), as the issue, 06 §7 and the RTL banner cite it.
   - The ctr campaign contract: `tb/pp_top/ctr_mutants.py:1-19,78-82` and `tb/pp_top/README.md:1398-1444`.
   - The delta changes no clause-bearing artifact.
4. **Diff and history.**
   - `git diff 07b1469d..80b3c1b2` covers 27 files.
   - `git diff bed5f477..80b3c1b2` covers 2 files: the comment in `KL_aecp_notify.sv` (`356c1bba`) and this patch.
   - `git diff 356c1bba..80b3c1b2` covers 1 file (§2).
5. **Public evidence.**
   - kebag-logic/milan-fpga `1de9179a`, `review-evidence/pp148-r1`: its `MANIFEST.json` lists 216 files. I fetched `author/evidence/round-1b/r1c-head-camp-ctr.log`, and its sha256 `dcd55eac…a178570` equals the manifest's `published_sha256`.
   - That tree holds no receipt at `356c1bba` or `80b3c1b2`.
   - The manager's checks at this head (plant check 440 of 440; `ctr_mutants --only ctr-notify-one-window` control PASS, KILLED with 4) are stated in the review assignment. No public comment carries them yet (§7).
6. **Prior public findings.** They are resolved or retained in §4.

## 2. What the delta is

`scripts/delta_identity.sh` checks the delta. Its output is `receipts/delta_identity.log` (rc 0):

| Check | Result |
|---|---|
| Files changed `356c1bba..80b3c1b2` | `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch` only, mode 100644 to 100644, blob `0968b634` to `eca21b0c`, numstat 5/3 |
| `git diff --check` | clean |
| Patch blob history | `0968b634` at `07b1469d`, `bed5f477` and `356c1bba`; `eca21b0c` at this head |
| `KL_aecp_notify.sv` blob | `030192f9` at `356c1bba` and at this head (untouched by this delta) |
| The patch's `-`/`+` lines, old vs new | identical (5 lines): `-` the two stamp lines; `+` `ctr_sent_r <= '1;` and the loop that stamps every `ctr_last_r[c]` |
| Hunk arithmetic | header `@@ -1233,10 +1233,11 @@`; counted 10 old and 11 new lines |
| Bytes | no CR; final newline present |
| Context against the head | the four context comment lines are exactly `KL_aecp_notify.sv:1299-1302` at this head |
| Planting outside a work tree | old patch at `bed5f477` and new patch at this head: both "Hunk #1 succeeded at 1298 (offset 65 lines)", rc 0 |
| Planted `bed5f477` vs planted head | they differ exactly as the unplanted files do (the 2-line to 4-line comment at `:1299`); comment-stripped, the planted files are identical |

The arm therefore plants the same design at this head as the reviewed arm did at `bed5f477`.

## 3. Executed evidence (this round)

All simulations used the pinned simulator wrapper:
- `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f`.
- It is exported as `VERILATOR` and inherited by `tb/pp_top/Makefile`'s `VERILATOR ?=`.

Every tree was a `git archive` extraction under `scratch/`. Nothing was written into the clone.

| # | What | Result | Receipts |
|---|---|---|---|
| E1 | `scripts/delta_identity.sh` | §2; rc 0 | `receipts/delta_identity.{log,rc}` |
| E2 | `scripts/plant_check.py`: every `tb/**/*.patch` through `git apply --check` with cwd at the extraction root (not a work tree), as every patch driver plants; plus every exact-text edit of `notify_mutants.py` and `d3_mutants.py`, applied in order, each old text required exactly once | **head 440 of 440**, rc 0: adp_engine 39, maap 27, aecp_dispatch 40, ctr 17, d3 110, pp_top/mutations 46, notify 53, srp_top 108. **`356c1bba` 439 of 440**, rc 1; the only refusal is `ctr-notify-one-window.patch` ("patch failed: hdl/aecp/KL_aecp_notify.sv:1233"). `bed5f477` 440 of 440. `07b1469d` 430 of 430 (four pp_top patches and six notify arms fewer) | `receipts/plant_check-{head,p356,pbed,pbase}.{log,rc}` |
| E3 | `ctr_mutants.py --jobs 2 --only ctr-notify-one-window` at this head | control PASS; arm rc=2, failures=4, named=1 **KILLED**: K15 x2 ("STREAM_INPUT 0 is pushed at once…", "…AVB_INTERFACE 0 then goes out…"), K16, K17 (got 2 and 2). "2 checks: 2 PASS", rc 0 | `receipts/ctr-only-head/` |
| E4 | full `ctr_mutants.py --jobs 6` at this head (`make ctr-mutants` arms, 17 + control) | control PASS, **17 of 17 KILLED**, "18 checks: 18 PASS, 0 FAIL", rc 0 | `receipts/ctr-full-head/` |
| E5 | `scripts/compare_ctr.py`: E4 against the published head record `r1c-head-camp-ctr.log` (round 1b, at `4ed463b`/`bed5f477` inputs) | **19 of 19 records identical**: every verdict line, every failure count and every FAIL line, including K14's "1018 ms" figures. rc 0 | `receipts/compare-ctr-full-vs-published.{log,rc}`, `receipts/published-r1c-head-camp-ctr.log` |
| E6 | the same `--only` run at `356c1bba` (reproduces the prior finding) | the driver raises `CalledProcessError` from `git apply --check` on the arm; rc 1, no tally | `receipts/ctr-only-356c1bba/` |
| E7 | the same `--only` run at base `07b1469d` | control PASS; arm KILLED with 3 failures (K15 x1, K16, K17 got 1 and 1). This matches the README row's "3 at `main` `07b1469d`, without K15's second" and its "into K17 (2 pushes, not 1)" | `receipts/ctr-only-base/` |
| E8 | PR body (fetched at review time, PR `updated_at` 2026-10-05T06:04:04Z) | §5 | `receipts/pr159-body-at-review.md`, `receipts/pr-body-excerpts.txt` |
| E9 | Hosted checks at the exact head, workflow `hdl`, push and pull_request runs | `docs-gates` success (both); `portability` success (both); `suites` **in progress** in both at 06:11:28Z. Snapshot only; the manager owns hosted acceptance | `receipts/hosted-checks.tsv` |
| E10 | Clone state and tools | §8 | `receipts/environment.txt` |

The campaigns ran inside the 12 GB unit. Memory reached the cap under page cache, with `oom_kill 0` throughout. Each arm's verdict depends on its own named checks, and every arm completed with a tally.

## 4. Prior public findings on this PR, at this head

| Finding | Status at `80b3c1b2` | Basis |
|---|---|---|
| R476-2-F1 = R477-2-F1 (MAJOR, Tests): `ctr-notify-one-window.patch` refused at `356c1bba`, so the ctr campaign aborts | **Resolved.** The PR-body sentence that R477-2-F1 also asked for is carried as RESIDUE under R476-2-R1 below | E1-E6. The patch was refreshed exactly as required (context only, header `-1233,10 +1233,11`, `-`/`+` unchanged). The plant check is 440 of 440. The full campaign gives 18 of 18 with records identical to the published head record. `git diff 356c1bba` touches only that patch |
| R476-1-F1 (MINOR, RTL, Docs): stale selection-stamp comment | Resolved at `356c1bba` (R476-2); unchanged here | `KL_aecp_notify.sv` blob `030192f9` unchanged; `:1299-1302` as R476-2 accepted |
| R476-2-R1 (RESIDUE, Docs; PR body) | **Retained in part.** Items 1, 3 and 4 and the "name the refreshed patch" note are applied. **Item 2 is not applied** | Detail and the exact fix are in §5. PR body lines 35-36 still read "Every compiled input at `4ed463b` equals the final head's" |
| R477-1-RES1 (RESIDUE, Docs; "TD 6 probes") | **Resolved** | PR body line 43 reads exactly "default 9,956; other five unchanged (TD 3 checks, 6 monitor probes answered, as at base)" |
| R477-2-RES1 (RESIDUE, Docs; PR body) | **Retained in part** | Resolved: the head line (l.7), "differs from that measured head only in the comment" (l.76), `:1445` (l.113), and "(`:1303-1304`, its comment `:1299-1302`)" (l.117). Retained (its own exact fixes stand): the commit table still has no row for `356c1bb`, nor now for `80b3c1b`; and l.73-74 "gate 15 passes with processor pin `bed5f477`" does not say at which pin gate 15 last ran |
| R476-1-S1 (SUGGESTION, Tests): no check holds the limiter at exactly 1,000 ticks | Retained (optional) | Untouched by the delta |
| R476-1-S2 (SUGGESTION, Tests): the kind guard at `:1445` is ungraded | Retained (optional) | Untouched |
| R477-1-S1 (SUGGESTION, RTL, Docs) | The `:1299` half was resolved at `356c1bba`. The `:399-402` half is retained (optional) | `:399-400` still reads "is written in the cycle that sets the bit" (`receipts/environment.txt`) |
| R477-1-S2 (SUGGESTION, Robustness, Conformance): carry the stamp follow to #158 | Retained, for #158 | Untouched |

## 5. Findings (this round)

### R476-2-R1 (retained in part) - RESIDUE - lens: Docs (PR body only)

- **Where:** PR #159 body, lines 35-36 (`receipts/pr-body-excerpts.txt`): "Validation is complete at base `ead80360` and head `bed5f477`. Every compiled input at `4ed463b` equals the final head's; documentation checks were repeated at `bed5f477`."
- **Authority / evidence:**
  - The final head is now `80b3c1b2`. Its `KL_aecp_notify.sv` differs from `4ed463b`'s in four comment lines (`356c1bba`), and the ctr arm patch differs in context lines (`80b3c1b2`). So the sentence is literally false at this head.
  - The defect is wording only. The comment-stripped notify source and its sv2v output are identical (R476-2), and the planted arm is the same design (§2). The re-run campaign reproduces every published record (E4, E5). No measurement, figure or verdict moves.
  - The body also does not state that the ctr arm was re-checked after `80b3c1b2` (R477-2-F1's PR-body clause).
- **Impact:** a reader may take the round-1b receipts to have been produced from byte-identical inputs. They were produced from semantically identical inputs.
- **Required outcome (exact fix):** replace the sentence "Every compiled input at `4ed463b` equals the final head's; documentation checks were repeated at `bed5f477`." with:

  > Every compiled input at `4ed463b` equals `bed5f477`'s; documentation checks were repeated at `bed5f477`. `356c1bba` changes only comment lines of `KL_aecp_notify.sv` (its sv2v output is byte-identical), and `80b3c1b2` changes only the context lines of `ctr-notify-one-window.patch`, which plants the same design: at `80b3c1b2` all 440 planting arms plant, and `ctr_mutants.py` gives control PASS and 17 of 17 KILLED, `ctr-notify-one-window` failing K15 x2, K16 and K17.
- **Verification:** read the edited body against this head.

### R476-3-R1 - RESIDUE - lens: Docs (PR body only)

- **Where:** PR #159 body, lines 6-9: "…current head `80b3c1b2…`: `bed5f477` plus two manager commits, `356c1bba` (…) and `80b3c1b2` (…), including `--no-ff` merges of `b0a74196` and `ead80360`."
- **Evidence:** the trailing "including `--no-ff` merges" now follows the list of the two manager commits, so it reads as if those commits included the merges. The merges are `415a9fd` and `4ed463b`, in `bed5f477`'s history. No figure is wrong.
- **Impact:** wording only.
- **Required outcome (exact fix):** move the clause to the branch sentence, so lines 6-9 read:

  > Branch `pp148-notify-spacing` from `main` `07b1469d`, including `--no-ff` merges of `b0a74196` and `ead80360`; current head `80b3c1b223aaad05f428164cd56595a4c1187509`: `bed5f477` plus two manager commits, `356c1bba` (rewords the comment at `KL_aecp_notify.sv:1299-1302` only, R476-1-F1) and `80b3c1b2` (refreshes `ctr-notify-one-window.patch`'s context to that comment, R476-2-F1 = R477-2-F1).
- **Verification:** read the edited body.

### Examined and accepted (not findings)

- **PR-body line references at this head:** `:136` (banner), `:469`, `:1043`, `:1297` (`em_ctr_ix_r`), `:1099-1101` (window check), `:1299-1302` (comment), `:1303-1304` (selection stamp) and `:1445` (`N_EMIT_WAIT` stamp). All are exact.
- **PR-body ctr row** ("1 control, 17 KILLED | same") holds at this head (E4).
- **The hunk header's start line (1233) against the actual position (1298).** `git apply` locates the exact context at offset 65, as it did for the original patch at `bed5f477`. Fifteen of the seventeen ctr patches plant at an offset; this is the campaign's existing practice, and `git apply` uses no fuzz.
- **README record.** `tb/pp_top/README.md:1419-1436` ("control PASS, 17 of 17 KILLED"; `ctr-notify-one-window` 4 at head, 3 at `main`) is reproduced at this head (E4, E7). No tracked file at this head still quotes the removed comment text (a search of the whole tree found none).

## 6. Lenses

- **Conformance - CLEAN.** The delta changes a verification patch only, with no RTL, clause claim or conformance figure. The R476-1 conformance verdict at `bed5f477` (spacing from the round's last send, Milan Table 5.22) stands, because RTL semantics are unchanged since then (R476-2; §2).
- **RTL - CLEAN.** No HDL file changes in this delta (`KL_aecp_notify.sv` blob `030192f9` at parent and head). The planted mutant RTL equals the reviewed arm's, comment aside (§2).
- **Robustness - CLEAN.** No logic change. The refreshed patch plants deterministically outside a work tree, with no fuzz. The driver's refuse-on-drift behaviour was demonstrated at `356c1bba` (E6), and it now passes at head (E3, E4).
- **Tests - CLEAN.**
  - R476-2-F1 is resolved: 440 of 440 arms plant (E2).
  - The ctr campaign is 18 of 18, identical record by record to the published head record (E4, E5).
  - The named arm fails K15 x2, K16 and K17 exactly as the README records, and 3 at base (E7).
- **Docs - CLEAN, with two RESIDUEs.**
  - The tracked docs and README agree with the head.
  - The PR body has two wording-only residues (§5), and R477-2-RES1's unapplied items are retained (§4).

### Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta diff (no clause-bearing artifact); R476-1 conformance reading of `KL_aecp_notify.sv` (send-to-send spacing, Table 5.22) carried unchanged | R476-1 (full), R476-2, R476-3 (delta) | `80b3c1b223aaad05f428164cd56595a4c1187509` |
| RTL | CLEAN | `KL_aecp_notify.sv` blob identity parent/head; planted-design comparison `bed5f477`/head (E1) | R476-1 (full), R476-2 (comment), R476-3 (delta) | `80b3c1b223aaad05f428164cd56595a4c1187509` |
| Robustness | CLEAN | patch bytes, hunk arithmetic, no-fuzz planting outside a work tree; driver refusal at `356c1bba` and success at head (E1, E3, E6) | R476-1 (full), R476-3 (delta) | `80b3c1b223aaad05f428164cd56595a4c1187509` |
| Tests | CLEAN | plant check at four revisions (E2); ctr `--only` at head, `356c1bba` and base (E3, E6, E7); full ctr campaign at head and its record comparison (E4, E5) | R476-1 (full), R476-2, R476-3 (delta) | `80b3c1b223aaad05f428164cd56595a4c1187509` |
| Docs | CLEAN (RESIDUE R476-2-R1 part, R476-3-R1; R477-2-RES1 part retained) | `tb/pp_top/README.md:1398-1444`; PR body at review time (E8); line references at head | R476-1 (full), R476-2, R476-3 (delta) | `80b3c1b223aaad05f428164cd56595a4c1187509` |

## 7. Real limits and pending manager duties

- **Delta round only.** I did not re-run the processor suites, lint, Yosys, the other nine campaigns, the parent consumer set, or the OOC area at this head. The delta changes none of their inputs except this ctr patch, which only the ctr campaign reads, and that campaign was re-run in full. For those gates I rely on the earlier rounds and on the manager's stated banks.
- **No public evidence at this head yet.** The public evidence tree (`1de9179a`) has no receipt at `356c1bba` or `80b3c1b2`, and no public comment carries the manager's head checks. *Manager duty:* publish the exact-head evidence (plant check, ctr run, banks) that the PR and the merge decision rely on.
- **Hosted checks.** At 06:11:28Z, `suites` was still in progress at the exact head in both runs; `docs-gates` and `portability` succeeded. The hosted workflow runs no ctr campaign. *Manager duty:* hosted/act acceptance at the exact head.
- **Merge-turn candidate.** Source validation is distinct from the final current-dev candidate. *Manager duty:* build it at the merge turn (source base `07b1469d`, live dev `fa450d301805881ad713b67521477bf042ddadfd`), including the parent adoption patch and gate 15 at the final pin.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **RESIDUEs to the residue checklist:** R476-2-R1 item 2 (updated exact fix in §5), R476-3-R1, and R477-2-RES1's commit-table row and gate-15 pin items.
- **Second review.** Merge still requires the other independent positive review. The concurrent R477-3 report was not posted and was not read.
- **Reading order disclosure.** At the start of this round I listed the PR's comments in one call. That listing displayed the opening portion (up to about 5,000 characters each) of the earlier R476-1, R476-2, R477-1 and R477-2 reports before my own delta pass. I read their findings sections in full only after I had finished the delta identity check, the plant check, the targeted arm run (E1-E3) and the PR-body line-reference check. The full campaign (E4) was still running at that point. The delta checks and every run above are my own.
- **Memory.** The campaign ran at `--jobs 6` to stay inside the 12 GB unit. The memory peak reached the cap under page cache, with no OOM kill.

## 8. Clone restoration

- All probes ran in `git archive` extractions under `scratch/`. `plant_check.py` refuses a git work tree, so nothing was written into the review clone.
- The clone is at exact head `80b3c1b2`, tree `81a6a141`, with HEAD detached.
- `git status --porcelain --ignored` is empty, and the worktree and index are clean.
- The index (mode, blob, path) and the HEAD tree hash the same: `bf3d1cc4…122c4`.
- The repository has no gitlinks (0 entries of mode 160000), so there is no submodule pin to check.
- **Receipt redaction:** the simulator's host install prefix in the build logs was replaced with `<SIMULATOR_PREFIX>`. No other edit was made to any receipt.

R476-3 FINISHED
