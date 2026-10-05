[R477] POSITIVE - exact head 80b3c1b223aaad05f428164cd56595a4c1187509

# R477-3: external independent review of issue #148 / PR #159 (delta round)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #159, issue #148.
- Exact head `80b3c1b223aaad05f428164cd56595a4c1187509`, tree `81a6a14162632f51a504005066f10bde891a8819`. Parent `356c1bbad2e9838659b433736040acf0cc4abf3e` (the R477-2 head). Source base `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`.
- Delta under review: one manager commit, `80b3c1b`, which refreshes the context of `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch` to resolve R476-2-F1 = R477-2-F1.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. R477-2-F1 / R476-2-F1 is resolved at this head:
- The delta is that one patch file and nothing else.
- Every planted arm in the repository plants: 567 of 567, a superset of the manager's 440.
- The refreshed arm is KILLED with K15 x2, K16 and K17.
- The whole ctr campaign gives control PASS and 17 of 17 KILLED. Its log is byte-identical to the published head record.

Two PR-body wording defects are open as RESIDUE (one new, one carried from R476-2-R1 item 2), and one R477-2 residue is retained in part. One new SUGGESTION covers the refreshed patch's non-canonical hunk.

## 1. Reconstruction (order followed)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. `docs/README.md` sets the conventions and the `make check` requirement. It is unchanged by the delta.
2. **Issue #148, frozen acceptance.**
   1. Spacing is measured from send to send.
   2. A check fails on today's behaviour, with a mutant that restarts the spacing at selection.
   3. The existing notification suites and campaigns stay green.

   Scope decisions come from the manager's comments 5982500256 (lane items and gates, including "the notify, ctr and pp_top campaigns at their counts"), 5985998608 and 5986055260 (round 1b union).
3. **Authorities.** Milan v1.2 §5.4.5 / Table 5.22 (`T-CTR-NOTIF`), IEEE 1722.1-2021 §7.5.2. Module banner `KL_aecp_notify.sv:133-136`. The ctr campaign contract is in `tb/pp_top/README.md:1398-1444` and `tb/pp_top/ctr_mutants.py:78-82` (`plant`: `git apply --check`, then `git apply`).
4. **Diff and history.** `git diff 356c1bba 80b3c1b2` is one file, `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch`: blob `0968b63` becomes `eca21b0`, mode 100644 unchanged, +5 -3. `git diff --check` is clean. The full `07b1469d..80b3c1b2` diff is 27 files (+1375 -147). Of these, only the patch file differs from `356c1bba`.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@1de9179a…/review-evidence/pp148-r1` holds the author's round-1b receipts at `4ed463b`/`bed5f477`. I used `r1c-head-camp-ctr.log` (sha256 `dcd55eac…`) and `r1c-base-camp-ctr.log` (`0fd23cc6…`).
   - The evidence tree has no receipt at `356c1bba` or at this head. The manager's checks at this head are those stated in the review brief and the start comment 5989015437.
6. **Prior public findings.** I read them only after my own pass over the delta and my own executions (E1-E5). They are resolved or retained in §4.

## 2. Executed evidence (this round)

All trees are `git archive` extractions under the packet's `scratch/`. The pinned Verilator 5.050 (wrapper sha256 `905795b9…`, `Verilator 5.050 2026-07-01 rev v5.050`) was placed first on `PATH`; the host default (5.052) was not used. Commands: `scripts/run_r477_3.sh`.

| # | What | Result | Receipt |
|---|---|---|---|
| E1 | The delta's content | Only the patch's hunk header (`-1233,8 +1233,9` becomes `-1233,10 +1233,11`) and its context change. The two old comment lines are replaced by the four lines now at `KL_aecp_notify.sv:1299-1302`. The `-`/`+` lines are unchanged. The preimage (10 lines) is byte-equal to the head source at `:1298-1307`. Counts check: 1+4+2+3 = 10 old lines and 1+4+3+3 = 11 new lines | `receipts/delta-356c1bba-80b3c1b2.diff`, `receipts/delta-raw.txt` |
| E2 | `scripts/plant_check.py` at head, at `356c1bba` and at `07b1469d`. It checks every `tb/**/*mutations/*.patch` with `git apply --check` (the drivers' tool) and every exact-text arm of the notify, d3, acmp, gsi, name-write, srp_admission and talker-retry drivers, by each driver's own count rule. It builds nothing | **Head: 567 of 567 plant, rc 0.** That is 277 patches, 53 notify, 110 d3, 33 acmp, 20 gsi, 1 name-write, 3 srp_admission and 70 retry arms. The manager's 440 (277 + 53 + 110) is the subset. `356c1bba`: 566 of 567, the refusal being `ctr-notify-one-window` ("patch failed: …KL_aecp_notify.sv:1233"), which reproduces F1. `07b1469d`: 543 of 543 | `receipts/plant_check-{head,base356,base07}.{log,rc}` |
| E3 | The planted design | The refreshed arm applied at head and the original arm applied at `07b1469d` make the same code edit. Both replace the selection-site `ctr_sent_r[pick_ctr_ix_w] <= 1'b1; ctr_last_r[pick_ctr_ix_w] <= now_ms_i;` with the all-descriptor writes, and nothing else changes. At head the edit is at `:1303-1304`; at base it is at `:1298-1299`. The `N_EMIT_WAIT` stamp at `:1445` is untouched by the arm | `receipts/one-window-planted-{head,base07}.diff` |
| E4 | `ctr_mutants.py --only ctr-notify-one-window --jobs 2`, at head and at `07b1469d`, run concurrently | **Head:** control PASS (rc 0); arm KILLED, rc 2, 4 failures, named 1: K15, K15 ("…then goes out, a second after its window opened, with LINK_UP 5"), K16, K17 ("got 2 and 2"). **Base:** control PASS; arm KILLED with 3 failures: K15, K16, K17 ("got 1 and 1"). Each arm block is identical to the published `r1c-head`/`r1c-base` record. This matches `tb/pp_top/README.md:1436` and the PR body (3 to 4). Driver rc 0 at both | `receipts/ctr-one-window-{head,base07}{.log,.rc,.time,/}`, `receipts/ctr-one-window-vs-published.txt` |
| E5 | The whole ctr campaign at head, `ctr_mutants.py --jobs 9` | Control PASS, **17 of 17 KILLED**, "18 checks: 18 PASS, 0 FAIL", rc 0, 6 min 40 s. The 113-line log is **byte-identical** to the published `r1c-head-camp-ctr.log` | `receipts/ctr-full-head{.log,.rc,.time,/}`, `receipts/ctr-full-head-vs-published.diff` (empty) |
| E6 | `make check` at head | rc 0. 41 mermaid + 18 wavedrom blocks; 1,136 links; 115 REQ rows, 17 GAP; 94 matrix rows, 0 untested; 28 parameters. These are the PR body's figures | `receipts/make-check-head.{log,rc}` |
| E7 | Hosted checks at the exact head, read-only, 2026-10-05T06:15Z | Two workflow runs. `docs-gates` and `portability` succeeded in both. `suites` was **in progress** in both. `.github/workflows/hdl.yml` runs the srp, maap, adp, aecp and aecp-dispatch campaigns, but not `ctr-mutants`, so hosted checks do not cover this delta's arm | `receipts/hosted_checks.txt` |
| E8 | Clone integrity after all probes | HEAD `80b3c1b2`, detached. Tree and index tree are both `81a6a141`. `git status --porcelain --ignored` is empty. All 558 tracked blobs re-hash to their index entries. Index and HEAD (mode, blob, path) hash the same, `bf3d1cc4…`. There are no gitlinks (no submodules), so there is no pin to check. Nothing was written to the clone | `receipts/clone-integrity.txt` |

## 3. The delta, lens by lens

- **Conformance: CLEAN.**
  - The delta changes no RTL, so the compiled design is that of `356c1bba`.
  - R477-2 E1 showed that design is sv2v-identical to `bed5f477`/`82e1664`.
  - My R477-1 conformance verdict (Table 5.22 spacing, send to send) therefore stands.
  - Acceptance 2's selection-restart mutant (`counter_spacing_from_selection`, notify driver) still plants (E2).
  - Acceptance 3 now holds for the ctr campaign at this head (E5).
- **RTL: CLEAN.** No `hdl/` byte changes in the delta (E1). The arm still mutates exactly the selection-site stamp (E3). The R477-2 RTL verdict stands.
- **Robustness: CLEAN.** No logic change. The R477-1/R477-2 robustness verdicts stand. #158 stays separate.
- **Tests: CLEAN.**
  - F1 is resolved: the arm plants (E2), is KILLED with its recorded checks (E4), and the full campaign reproduces the published head record byte for byte (E5).
  - Every other arm in the repository still plants (E2).
  - One SUGGESTION (R477-3-S1) covers the hunk's form.
- **Docs: CLEAN, with RESIDUE.**
  - `tb/pp_top/README.md:1398-1444` (git apply; 17 of 17; the 3-to-4 row) agrees with E4/E5. `make check` passes (E6).
  - The PR body's edits check out against the head, except for the two RESIDUE items in §4 and the retained part of R477-2-RES1.

### PR body against the head (fetched 2026-10-05T06:16Z, `updated_at` 06:04:04Z; `receipts/pr159-body-as-fetched.md`, sha256 `e7fc0d26…`)

| Text required | Present at head? |
|---|---|
| R477-1-RES1: "default 9,956; other five unchanged (TD 3 checks, 6 monitor probes answered, as at base)" | Yes, l.42, exact |
| R476-2-R1 item 1: current head line naming the manager commit(s) | Yes, l.6-8, adapted to `80b3c1b2` and naming the refreshed patch. Its trailing clause is mis-attached: R477-3-RES2 |
| R476-2-R1 item 2: "Every compiled input at `4ed463b` equals `bed5f477`'s; `356c1bba` changes only comment lines, and the module's sv2v output is byte-identical" | **No.** l.34-35 still read "Every compiled input at `4ed463b` equals the final head's": R477-3-RES1 |
| R476-2-R1 item 3: "notify RTL differs from that measured head only in the comment at `:1299-1302`; its sv2v output is byte-identical" | Yes, l.74-75, exact |
| R476-2-R1 item 4: "`:1445`" and "the selection stamp (`:1303-1304`, its comment `:1299-1302`)" | Yes, l.112 and l.116 |

The other line references in the body agree with the head source: `:136` banner, `:469`/`:1043`/`:1297` `em_ctr_ix_r`, `:1099-1101` window check, `:1445` stamp.

## 4. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R477-3-RES1 (R476-2-R1 item 2, retained) | RESIDUE | Docs | PR #159 body l.34-35: "Every compiled input at `4ed463b` equals the final head's" | Notify blob `9e97f8e` at `4ed463b` vs `030192f` at this head (comment lines only); the design is sv2v-identical (R476-2 / R477-2 E1), and `80b3c1b` changes no compiled file (E1) | Wording only: the sentence is literally false at this head, but no figure, verdict or measurement moves | Replace with: "Every compiled input at `4ed463b` equals `bed5f477`'s; `356c1bba` changes only comment lines, and the module's sv2v output is byte-identical; `80b3c1b2` changes only the context of `ctr-notify-one-window.patch`." | Read the edited body |
| R477-3-RES2 | RESIDUE | Docs | PR #159 body l.6-8: "…`bed5f477` plus two manager commits, `356c1bba` (…) and `80b3c1b2` (…), including `--no-ff` merges of `b0a74196` and `ead80360`." | `git log`: the merges are `415a9fd` and `4ed463b`, ancestors of `bed5f477`. Neither manager commit is a merge | Wording only: the trailing clause reads as if the manager commits include the merges | Replace with: "current head `80b3c1b223aaad05f428164cd56595a4c1187509`: `bed5f477` (which includes the `--no-ff` merges of `b0a74196` and `ead80360`) plus two manager commits, `356c1bba` (rewords the comment at `KL_aecp_notify.sv:1299-1302` only, R476-1-F1) and `80b3c1b2` (refreshes `ctr-notify-one-window.patch`'s context to that comment, R476-2-F1 = R477-2-F1)." | Read the edited body |
| R477-2-RES1 (retained in part) | RESIDUE | Docs | PR #159 body, commit table (l.18-24) | Its l.6, l.73-74, l.111 and l.115 items are resolved (§3). Its l.71-72 item is accepted: "processor pin `bed5f477`" correctly names the pin of the published gate-15 run | Wording only: the table lists the lane's commits but not the two manager commits | Add the rows "\| `356c1bb` \| the selection stamp's comment describes it as provisional (R476-1-F1); comment lines only \|" and "\| `80b3c1b` \| `ctr-notify-one-window.patch`'s context refreshed to that comment (R476-2-F1); its `-`/`+` lines unchanged \|" | Read the edited body |
| R477-3-S1 | SUGGESTION | Tests | `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch:3-13` | E2: the hunk has 5 leading and 3 trailing context lines, and its header names line 1233 for a site now at 1298. `git apply` (the driver's tool, `ctr_mutants.py:78-82`, README:1402) accepts it. GNU `patch -p1 -F0` refuses it, because asymmetric context marks a hunk at the end of a file; with fuzz 2 it applies. It is the only one of 277 patches that needs fuzz (`receipts/plant_check-head.log`). The ctr patches' line drift is general (210 offsets at head) and is not part of this | None on any campaign: the driver uses `git apply`, and E4/E5 pass | Optional: regenerate the arm as a canonical `git diff -U3` of a planted head copy, so it has 3+3 context and the current line numbers | `plant_check.py` reports 0 patches needing fuzz, and `ctr_mutants.py --only ctr-notify-one-window` still gives 4 failures |

### Prior public findings at this head

| Finding | Status at `80b3c1b2` | Evidence |
|---|---|---|
| R476-2-F1 = R477-2-F1 (MAJOR, Tests; the ctr arm no longer planted) | **Resolved.** The context is refreshed exactly as the required outcome states, with no other file changed. All verifications hold: the plant check is clean, the arm gives control PASS and KILLED with 4 (K15 x2, K16, K17), and the full campaign gives 17 of 17 | E1, E2, E4, E5 |
| R476-2-R1 (RESIDUE, Docs; PR-body sentences) | Items 1, 3 and 4 and "name the refreshed patch" are **resolved**. Item 2 is **retained** as R477-3-RES1 | §3 table |
| R477-2-RES1 (RESIDUE, Docs) | **Retained in part**: the commit-table rows only. The rest is resolved or accepted | §4 |
| R477-1-RES1 (RESIDUE, Docs; "TD 6 probes") | **Resolved.** The exact text is at l.42 | §3 table |
| R476-1-F1 (MINOR, RTL, Docs) | Resolved at `356c1bba`, and unchanged here | source `:1299-1302` |
| R476-1-S1 (SUGGESTION, Tests; TW/CS bound slack) | Retained as SUGGESTION. Untouched | n/a |
| R476-1-S2 (SUGGESTION, Tests; kind guard at `:1445` ungraded) | Retained as SUGGESTION. Untouched | source `:1445` |
| R477-1-S1 (SUGGESTION, RTL, Docs) | The `:1299` half is resolved. The `:399-402` half is retained: "is written in the cycle that sets the bit" omits the later claim and `N_EMIT_WAIT` rewrites | source `:399-402` |
| R477-1-S2 (SUGGESTION, Robustness, Conformance; carry the stamp-follow guard through #158) | Retained, for #158 | n/a |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta (E1: no `hdl/` change); acceptance 1-3 against E2/E4/E5; `KL_aecp_notify.sv:1099-1101,1299-1304,1445` read at head; R477-1 conformance evidence carried (design identical per R477-2 E1) | R477-3 (delta), R477-2, R477-1 | 80b3c1b223aaad05f428164cd56595a4c1187509 |
| RTL | CLEAN | E1 (no RTL bytes changed); E3 the planted edit is identical at head and base and touches only the selection-site stamp | R477-3, R477-2 | 80b3c1b223aaad05f428164cd56595a4c1187509 |
| Robustness | CLEAN | No logic change; R477-1/R477-2 robustness evidence carried; #158 separate | R477-3 (delta), R477-1 | 80b3c1b223aaad05f428164cd56595a4c1187509 |
| Tests | CLEAN (R477-3-S1 SUGGESTION) | E2: 567 arms at head, `356c1bba` and `07b1469d`; E3; E4: the arm at head and base vs the published records; E5: the full ctr campaign, byte-identical to the published head log; E7: hosted coverage | R477-3 | 80b3c1b223aaad05f428164cd56595a4c1187509 |
| Docs | CLEAN (RESIDUE R477-3-RES1, R477-3-RES2, R477-2-RES1 part) | `tb/pp_top/README.md:1398-1444`; E6 `make check`; the PR body against the head (§3 table, line references); `docs/README.md` | R477-3 | 80b3c1b223aaad05f428164cd56595a4c1187509 |

## 6. Real limits

- **Ctr campaign only.** I re-ran the ctr campaign (in full) and no other campaign.
  - The delta changes no input of the others. They read `hdl/`, `tb/common/` and their own bench or patch directories, none of which changed.
  - E2 shows all their arms still plant.
- **Banks not run here:** the full processor suites, `lint_hdl.sh`, Yosys, the six `pp_top` build totals, `tb/aecp_notify`, and the parent consumer set (including gate 15 and the five adoption patches).
  - For these I rely on R477-2's executions at `356c1bba` (identical RTL and benches) and the manager's statement that the source static/builder and native banks passed at this head.
  - No public receipt at this head was available to me.
- **No parent-side search.** Parent-side files that might quote the notify comment were not searched; the parent checkout is out of bounds.
- **Hosted checks.** `suites` was still in progress when I read them (E7). The hosted workflow does not run `ctr-mutants`.
- **Not run:** Vivado (the OOC 1x1 figures are the author's; the delta changes no RTL), hardware, physical calibration (NOT RUN; field skips are not hardware proof), Docker/act.
- **Busy host.** The host's load average was about 52 on 16 CPUs during E4/E5. That affects wall time only; the verdicts are deterministic (E5 is byte-identical to the published record).

## 7. Pending manager duties

- Carry R477-3-RES1, R477-3-RES2 and the commit-table part of R477-2-RES1 to the residue checklist, using the exact texts in §4.
- Hosted acceptance at the final head, including the `suites` job, which was in progress here. Consider adding `ctr-mutants`, or a plant-only check, to the delta-round checklist, since the hosted workflow does not run it.
- Build the final current-dev candidate at the merge turn: source base `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`, live dev `fa450d301805881ad713b67521477bf042ddadfd`. Include the parent consumer set with all five adoption patches and gate 15.
- Keep #158 open and separate.

## 8. Packet

- `scripts/plant_check.py`: the plant check (E2).
- `scripts/run_r477_3.sh`: the commands of E2 and E4-E6.
- `receipts/`: the raw logs, rc files, timing files and the per-arm logs of the driver.
  - Private install prefixes and local paths are replaced by `<VERILATOR_PREFIX>`, `<PINNED_VERILATOR>`, `<PACKET>` and `<CLONE>`. Nothing else is edited.
  - `receipts/published-inputs.txt` records the sha256 of the two published ctr logs used for comparison.

Every publishable file is listed in `MANIFEST.sha256`. `scratch/` is not published.

R477-3 FINISHED
