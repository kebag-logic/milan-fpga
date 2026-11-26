[R941] NEGATIVE - exact head 079c4fa1514be460949ddc28ae3277ea1873cb48

Internal independent review R941-2 of #1009 / PR #1017 (step 1 of ruling 3: the binding class's 100 ms first-dirty
window on the whole-commit save). Head `079c4fa1514be460949ddc28ae3277ea1873cb48`, tree
`be2122cbd487361b4ed8a99ff283565c1bec3eb2`, base `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. This is a
delta round: `85569e24..079c4fa1` is one commit, a comment in `sw/firmware/ctrl_nvm/nvm_store.h`. It also covers the
round-2 author packet (`review-evidence/p1win-r2`, evidence commit `e2d4a1d3`). All five lenses were applied.

Verdict: the delta is correct and compiles to the same tokens. The round-2 packet closes the identity and publication
part of R942-1-F2: a clean clone of the head, `results.json` and `table.md` bound by hash, exit 0. Two MINOR findings
are open at the root of that evidence:
- **F1.** Ruling 3's "notice 140 ms" item has no row in the published run.
- **F2.** The board summaries count 47 power cuts, but the PR accounts for 44.

Conformance, Tests and Docs are left unclean. RTL and Robustness are clean. There are two RESIDUE items and three
SUGGESTIONs.

## The delta (independent reading)

`nvm_store.h:29-31`: "plus that many centiseconds for each step of its save after the window" becomes "plus
CTRL_LOOP_STEP_AGE + 1 centiseconds for each step of its save after the window".
- This is the right antecedent. It is the pace the paragraph states at `:22-23`, the one
  `tb/verilator/ctrl_service_budget/save_window.py:30-31` derives the bound from ("at least once every
  CTRL_LOOP_STEP_AGE + 1 ticks"), and the one in the harness README's `save_window.bound_ms` sentence (`README.md:113`).
- The changed lines carry no lane label, lane name, review round, reviewer ID or issue-comment ID.
- Nothing in the tree reads this comment's text. `nvm_mutants.py:508` anchors on a `#define` line elsewhere in the
  header.
- Line count is unchanged (220 lines). Stripped of comments by the preprocessor with line markers kept, the header is
  byte-identical at `85569e24` and `079c4fa1` (`receipts/delta-preprocess.txt`, `scripts/delta_preprocess.sh`). So no
  translation unit's token stream or line table changes. This supports the PR's statement that the split-target
  campaign run at `85569e24` stands for this head.

## Round-2 evidence, checked at its root

| Claim (PR body / packet) | Check | Result |
|---|---|---|
| Packet integrity | 26 entries of `MANIFEST.json` and 25 of `author/MANIFEST.txt` re-hashed (`scripts/check_packet.py`, `receipts/check_packet.txt`) | 0 mismatches; no entry path-redacted; `author/PR-BODY.md` equals the live PR body apart from its `[A844]` lead line |
| Full run tied to the head | `full-run/*-identity.txt` | head `079c4fa1…`, tree `be2122cb…`, 0 status entries before and after, gitlinks equal `git ls-tree HEAD` (external `efeb541a` uninitialised, as in the review clone), command `run.py --point <pt> … --jobs 16 --record-budget-findings` (fresh build, no `--reuse-build`), rc 0; started 21 s after the head's commit time; `results.json`/`table.md` hashes equal the identity's and both manifests' |
| 113 groups, no refusal, the seven `backlog-owed` misses, one 8x8 pass owed to #977 | `results.json` both points | 113 groups, 0 refusals, 7 misses, 0 share misses (the 8x8 pass is in the OWED registry, `srp-bound`), 0 save misses |
| "Every figure equals round 1's run to the microsecond" | round-1 `gates.txt` regrade sections against round-2 verdict lines (`receipts/r1-r2-figures.txt`) | 37 of 37 lines at 1x1 and 40 of 40 at 8x8/1if identical |
| 1x1 `backlog-owed` rows within 0.05 ms of the base | round-1 `baseowed` section | differences 0.047 to 0.049 ms |
| 8x8/1if rows under `egress_ledger.py` | `8x8-1if-egress-ledger.txt` | every row 0.19 to 0.35 ms under its figure, rc 0 |
| Bind groups, burst, `save-burst`, `save-flight`, STEPS | verdict lines | the PR's table and prose figures match, e.g. 891.169 / 394.959 ms in capture, 646.392 / 306.463 ms burst with 2 / 4 saves, 1,353.998 / 1,097.438 ms and 650.995 / 147.073 ms, longest store pass 1.158 ms, step 0.793 ms |
| Load: 0.512 (1x1) and 0.744 (8x8/1if) | re-ran `load_grade.py --check` at the head (`receipts/load-grade-check.txt`) | 0.512 HELD at 0.70; 8x8/1if 0.744 against the flip check's 0.75 (see S1); RESULT PASS, rc 0 |
| Gate receipts at the head | `receipts/gate-*.txt` | every one: head `079c4fa1`, tree `be2122cb`, 0 status entries, rc 0. Store 170 plants, harness 321 mutants, split-target 79 checks, coverage PASS (`nvm_store.c` 513/513, 317/326), firmware 17 tests, memory, platform ledger (+0 findings), docs |
| LUT attribution | `receipts/lut-attribution.txt` | synth +23 / +19 LUT, place +159 / -9, ROM bank cells 34 / 31 at base and head, Verilog identical but for date and paths, ROM init files the only differing inputs: all as the PR states. The 8x8 post-synthesis difference sits in `KL_mbx`/`KL_mbx_cdc`/`milan_datapath`, not in the ROM (RES1) |
| Board: 144 and 32 readings under 800 ms | `board/summary-*.txt` | 8x8: 108 changes, max 0.5999 s, brackets 31.7-33.1 ms; 1x1: 24 changes, max 0.3354 s; cut holds 36 / 8, max 0.6026 / 0.3301 s; none within 10 ms (the PR says so) |
| Board: 44 cuts, each idle at the bind, durable before power-off, at least 250 ms before the last frame | same | the 36 + 8 graded lines all PASS, all idle at the bind, least margin 1.271 s, power off 1.469-1.674 s. **But the summaries count 38 and 9 power cuts** (F2) |
| Firmware ELF identity | identity files; harness reuse rule | `ctrl_app.elf` `57c023af…` (8x8/1if) and `f4bbbb4d…` (1x1), built fresh at the head. Not rebuilt here (the harness's SoC export needs a LiteX install, which this session does not have). The delta is shown token-neutral (above). The round-1 ELF digests are not published, so the PR's "byte-identical to it" has no public receipt (RES2) |

## Findings

**R941-2-F1 MINOR - Conformance, Tests, Docs - `review-evidence/p1win-r2/author/full-run/1x1-results.json` and
`8x8-1if-results.json` (`notices: []`); `tb/verilator/ctrl_service_budget/run.py:882`, `README.md:344-346`; PR body
"The full service-budget run at both points" - ruling 3's "notice 140 ms" is not measured by the published run.**
- Authority/evidence:
  - Ruling 3 item 3 requires "the full service-budget run at both points: notice 140 ms, ACMP 30 ms, …".
  - The 140 ms is the owner's bound on the last queued notice (`docs/reference/FR_NFR.md:416`; `CTRL_LOOP_QUEUED_MS`
    130 at both shapes, `ctrl_loop.h:368,377`). The harness holds it, and the retried notice's 20 ms, through
    `notice_window.py`'s `notice.retried` and `notice.queued` rows.
  - Those groups run only under `--variant answering-later` (`run.py:882`; README:344) and `answering-every-port`
    (README:346). The author's command names no variant. Both published runs record `notices: []` and no
    retried, queued or talker notice row (`receipts/check_packet.txt`).
  - The `notice-retried-<k>` groups exercise the path this PR changes: a SET_NAME save in flight, then a BIND_RX of
    STREAM_INPUT 0 during it (`notice_window.py:14-19,108-110`). That BIND_RX now opens the binding class's window.
  - The harness self-test's notice checks run on synthetic logs (`selftest_notice.py:1-9,30-35`), not the head's
    firmware.
  - R942-1-F2 said "Full notice <=140 ms and ACMP <=30 ms rows are not published for inspection: F2 retains that
    requirement". R941-1 narrowed F2 to the default run on the reading that it held those rows. At the root, the
    default run does not hold the notice rows.
- Impact: an acceptance item of ruling 3 has no executed evidence at this head, on a path the change touches. The
  PR's "every group" reads as covering it. A cold reviewer cannot confirm the notice bounds survive the new window.
- Required outcome: one of these.
  - From a clean checkout of the head, run the notice arms at both points: `run.py --point <pt> --variant
    answering-later` and `--variant answering-every-port`, with `talker-notices` if the manager reads "notice" to
    include it. Publish each run's identity (as `full-run/*-identity.txt`), `results.json`, `table.md` and rc, and
    state the worst retried and queued notice in the PR.
  - Or obtain a public manager ruling that names the artifact that holds "notice 140 ms" for step 1, and state it in
    the PR.
- Verification: the arms' `results.json` show measured `notice.retried`/`notice.queued` rows, `notice_misses` empty,
  rc 0, at head `079c4fa1` (or its successor) with 0 status entries. Or the ruling and the PR sentence exist.

**R941-2-F2 MINOR - Conformance, Tests, Docs - `review-evidence/p1win-r2/author/board/summary-8x8.txt:6`,
`summary-1x1.txt` "(2) power cuts"; PR body "On the board" - three power cuts are not accounted for.**
- Authority/evidence:
  - Ruling 3 item 3 requires, per cut, that the store is idle at the bind and the saved state reads as durable before
    power is lost.
  - The PR states "at every one of the 44 cuts (36 at 8x8/1if, 8 at 1x1/1if)".
  - The summaries count "power cuts: 38, durable readings in holds: 36" at 8x8 and "power cuts: 9, durable readings in
    holds: 8" at 1x1. The 36 + 8 per-cut lines all PASS. The other 2 + 1 cuts have no line and no stated reason.
  - The grader is not in the repository, so a cold reviewer cannot tell whether they followed a bind.
- Impact: if any of the three followed a bind, the per-cut claim is unshown for it. If none did, the PR's "44 cuts"
  is a miscount of what ran.
- Required outcome: the published summary or a note beside it identifies each of the three cuts (scenario, input,
  whether a bind preceded it, and why it has no hold reading). The PR then states the total that ran and the 44 that
  are graded. Any cut that followed a bind and has no durable reading is reported as such.
- Verification: the counts reconcile (38 = 36 + 2, 9 = 8 + 1) with a stated reason per cut.
- This is MINOR rather than RESIDUE because it may hide an unshown per-cut result.

**R941-2-RES1 RESIDUE - Docs, RTL - PR body "Memory and fit", the LUT paragraph; `receipts/lut-attribution.txt`
"per instance" - the attribution says more than the receipt shows.**
- Evidence: the paragraph sets "the last, partial bank … its contents count in LUTs" directly before "After synthesis
  the head has 23 LUTs more at 8x8/1if". It ends "starting from netlists that differ only in ROM contents".
- The receipt shows something else. At 8x8 the post-synthesis difference is in 9 instances, the largest `KL_mbx` +40,
  `KL_mbx_cdc` -25 and `milan_datapath` +25, none of them the ROM. At 1x1 it is in 2 instances of the CPU's hierarchy.
- The conclusion stands, because the netlist inputs are identical but for ROM contents. No figure or verdict changes.
- Exact fix: replace "starting from netlists that differ only in ROM contents." with "starting from synthesized
  netlists whose only differing input is the ROM contents (after synthesis 9 instances differ at 8x8/1if, the largest
  `KL_mbx` +40 and `KL_mbx_cdc` -25, and 2 at 1x1/1if, in the CPU's hierarchy, +19)."

**R941-2-RES2 RESIDUE - Docs - PR body "The full service-budget run at both points": "and the firmware is
byte-identical to it".**
- Evidence: round 1 published no ELF digest of its run, so this clause has no public receipt. The figures' identity
  does have one (`receipts/r1-r2-figures.txt`).
- Exact fix: either append "(round 1's `ctrl_app.elf` sha256 `<8x8>` and `<1x1>`, as this run's identity files
  record)", or replace the clause with "and its verdict lines are identical to round 1's".

**R941-2-S1 SUGGESTION - Docs - PR body "0.744 at 8x8/1if (0.76)"; `flip_grade.py:63`.** The tree's gate for
8x8/1if is the flip check's 0.75. Ruling 3 says 0.76. The load meets both. Consider "0.744 at 8x8/1if (the flip
check's 0.75; ruling 3's 0.76)".

**R941-2-S2 SUGGESTION - Docs - `receipts/gate-store.txt`.** The gate prints 656 tests over five shapes, but the PR
says "five shapes, 128 tests each" (640). Consider naming the other 16 (the RV32 arm's binary) or publishing the
per-binary tally.

**R941-2-S3 SUGGESTION - Tests - the size fixture's arms.** The round-2 receipts re-run every other gate at the head.
The arms are still round 1's at `8a4ad2c4`. Their inputs are unchanged since then, so this is completeness only.

## Prior public findings, resolved or retained at this head

| Finding | Disposition |
|---|---|
| R942-1-F1 MINOR, the routed LUT excess has no attribution | **Resolved** (R941-1). Round 2 adds the post-synthesis counts R941-1-S1 asked for, and they confirm no design input but ROM contents differs. Wording residue only: RES1 |
| R942-1-F2 MINOR (narrowed by R941-1 to the full service-budget run) | **Resolved for the default run:** clean-clone identity, `results.json`/`table.md`/rc published and hash-bound, every recorded exception as on the base (above). **Retained in its notice part as R941-2-F1:** the published run holds no notice row, which R942-1 named as part of F2 |
| R941-1-RES1 RESIDUE, "that many centiseconds" lost its antecedent | **Resolved** by `079c4fa1`, with exactly the prescribed text (`nvm_store.h:29-30`) |
| R941-1-S1 SUGGESTION, post-synthesis counts; 8x8 two-interface fit | Counts **done** (`lut-attribution.txt`). Whether ruling 2's two-interface fit binds step 1 remains a manager decision (not routed; its ledger entry 64.5 unchanged, `gate-plat.txt`) |
| R941-1-S2 SUGGESTION, gate receipts naming the base or a dirty tree | **Done** for every gate at the head with 0 status entries. The size-fixture arms remain round 1's (S3) |

## Lens results

```text
[R941] PASS RTL - diffstat c34e7d8b..079c4fa1 (no HDL, SoC or gateware path); nvm_store.h:22-31 delta (comment only, token-neutral: receipts/delta-preprocess.txt); receipts/lut-attribution.txt (Verilog and init-file comparison, ROM bank cells, synth/place counts); PR routed table against round-1 images.txt - no open finding beyond RES1's wording
[R941] PASS Robustness - nvm_store.h delta (no behaviour change, so R941-1's coverage of test_nvm_window.cpp:149-271 and the in-flight phases stands); board summaries' 44 graded cuts (idle at the bind, durable, least margin 1.271 s); results.json save groups (save-starved/second within stated worst cases at both points) - no open finding
```
- Conformance: UNCLEAN (F1, F2).
- Tests: UNCLEAN (F1, F2).
- Docs: UNCLEAN (F1, F2), with RES1, RES2 and S1-S2 carried.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R941-2-F1, R941-2-F2 | ruling 3 items 3-4 against both full-run `results.json`, identity, egress ledger, families; `load_grade.py --check` re-run; `notice_window.py:14-19,108-110`, `run.py:352-359,882`; FR_NFR.md:416; board summaries | R941-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| RTL | CLEAN | delta and its preprocessed identity; `lut-attribution.txt`; routed table; no HDL/SoC/gateware path in the lane | R941-2 (delta; R941-1 at 85569e24 for the unchanged code) | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Robustness | CLEAN | delta (no behaviour change); save groups in both runs; board cut lines | R941-2 (delta; R941-1 at 85569e24 for the unchanged code) | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Tests | UNCLEAN: R941-2-F1, R941-2-F2 | gate receipts at the head (store, harness self-test, split-target, coverage, firmware, memory, platform ledger, docs, load); round-1/round-2 verdict-line identity; `selftest_notice.py` (synthetic only) | R941-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Docs | UNCLEAN: R941-2-F1, R941-2-F2 (RES1, RES2 carried) | `nvm_store.h:22-50`; live PR body against `author/PR-BODY.md` and every receipt; packet README and manifests | R941-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |

## Limits

- **Physical calibration NOT RUN.** No hardware was touched. The board figures are the author's published summaries,
  regraded by a grader that is not in the repository. Field skips are not hardware proof.
- The 8x8 Talker-Failed case on input 0 (being re-run) is context only. Its result was not examined.
- Not re-run here: the full service-budget runs, the gates other than `load_grade.py --check`, the routed images and
  the split-target campaign. The budget ELF was not rebuilt: the harness's SoC export needs a LiteX install this
  session does not have. The ELF identity rests on the author's identity files plus this round's proof that the delta
  changes no compiled token.
- Hosted contexts at the exact head were all `queued` when observed (`receipts/hosted-checks-observed.tsv`), so none
  had executed. No manager source bank is claimed or inferred.
- The ruling's "ACMP 30 ms" is read here with the seven `backlog-owed` egress-hold rows (61.6-64.8 ms, the ACMP row
  61.862 / 63.003 ms) as the recorded exception. Both prior rounds accepted that on the base's equal figures. Every
  other ACMP row is at most 8.291 ms.

## Pending manager duties

- F1: the notice arms at both points at the head, or a ruling naming what holds "notice 140 ms". Then a re-review of
  Conformance, Tests and Docs.
- F2: the three unaccounted power cuts.
- The board acceptance the PR lists under "Before it lands": the 8x8 input-0 case, the boot comparison, and a
  decision on the 10 ms reading resolution that ruling 3 requires (brackets are 31.7-37.1 ms).
- Carry RES1 and RES2 to the residue checklist.
- Decide whether ruling 2's two-interface fit binds step 1.
- The current-dev merge candidate (source base `c34e7d8b`, live dev `e275d795`): builder and native banks, hosted and
  local-replica acceptance, merge authorization.

R941-2 FINISHED
