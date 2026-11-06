[R774] POSITIVE - exact head 3c22947861e5c057a6195ad46e1a379d67592559

External independent review, round R774-3, of kebag-logic/milan-fpga PR #841 (issue #839). The head is `3c22947861e5c057a6195ad46e1a379d67592559` (tree `03d9de984aa5c1796aae715abe50abe8e88cfee4`). The source base is `604899c08ff1cd1830e1dd08b733109ef852400c`. The delta judged in this round is `ba56827bbfe4acadb84ca220616a76ad74611e7d..3c22947861e5c057a6195ad46e1a379d67592559`: two commits, touching `tb/verilator/milan_dp/README.md` (+9/-6) and `tb/verilator/milan_dp/sim_boot_sa.cpp` (+3/-2).

The verdict is POSITIVE. R774-2 F1, the only open finding of the previous round, is resolved at its cause: the README's two lists now say exactly what `grade()` and `early_enable()` check. The two renamed checks say what they compare, and nothing else in the code changed. `bootsa` passes 67 of 67. `bootsa-mutants` passes 13 of 13: the clean control plus all twelve controls, each caught by every check it names. No RTL, harness logic, generated artifact or receipt figure changed. No new finding above SUGGESTION. There is no new RESIDUE.

## The three assigned checks

### (1) R774-2 F1: the README states exactly what the leg checks

**First-boot list.** `README.md:1183-1198` against `grade()` (`sim_boot_sa.cpp:759-830`). `grade()` is called once, at `:862`. That is after `probe_tx()` (`:861`) and before `pair_order()` (`:863-864`) and `early_enable()` (`:865-866`), with a single `reset()` before it (`:837`). So "every frame of the first boot (through the controller's and the listener's exchanges)" is exactly the `sent_` range it iterates (`:764`). The list is now in the code's order:

| README | Code | Match |
|---|---|---|
| :1186-1187 the processor offered a frame before the station MAC was written | :796-797 `pp_offered_early_` | yes |
| :1188 no all-zero source address | :768, :798 | yes |
| :1189 no CSR-addressed transmitter's frame before both halves | :773, :799-800 (`before_mac = !(wrote_lo_ && wrote_hi_)`, `:416`; gPTP excluded) | yes |
| :1190 each protocol's frames carry the station MAC | :769-772, :801-807 (all ten kinds, `other` included) | yes |
| :1191-1192 destination: own for MSRP, MVRP, gPTP, ADP, ACMP, MAAP; the controller's MAC for AECP | :774-775, :808-815; `protocol_da()` :178-189 | yes |
| :1193-1195 EtherType at 12-13 (16-17 behind a C-TAG) and AVTP subtype name a graded kind | :816-817; `classify()` :151-170 | yes |
| :1196-1197 MSRP, MVRP, gPTP, ADP, AECP, ACMP, MAAP, AAF sent; CRF where declared | :818-827 (`kCrfOutputDeclared`, :820) | yes |
| :1198 `A_TXARB_DIAG` clean | :828-830 | yes |

**"Grades instead" for the early-enable boots.** `README.md:1205-1215` against `early_enable()` (`sim_boot_sa.cpp:549-618`). "Instead" is accurate. None of `grade()`'s destination, EtherType or sent-and-graded checks run over these boots. Their checks are the ones below, and the stamp comparison runs in every boot (`README.md:1200-1203`; `grade_stamp()`, `sim_boot_sa.cpp:621-629`).

| README | Code | Match |
|---|---|---|
| :1207-1210 required sources offered while unwritten: MAAP + CRF (MAAP on), AAF + CRF (MAAP off), CRF where declared | :599-600, :603-604, :608-609 | yes |
| :1211 no frame of that source before the pair | :601, :605, :610 | yes |
| :1212-1213 MAAP, AAF, CRF after (AAF, CRF with MAAP off), CRF where declared | :602, :607 (AAF in both boots), :611 | yes |
| :1214-1215 no early CSR frame, no all-zero, all station MAC, `A_TXARB_DIAG` clean | :613-617 | yes |

**CRF condition.** `early_enable()` grades CRF only under `if (kCrfOutputDeclared)` (`:608`). `grade()` requires CRF only under the same condition (`:820`). The README now states it on both early-enable items that name CRF (`:1210`, `:1213`), and on the first-boot list (`:1197`).

The text applies option (a) of R774-2 F1's required outcome, using its exact replacement wording. **F1: resolved.**

### (2) The renamed checks say what they compare, and the legs still pass

- Word diff (`receipts/delta_scope.txt`): only the two label strings change. The AECP destination label becomes "every AECP frame's destination address is the controller's MAC". The comparison at `:774` is `s.da != kControllerMac` for AECP, so the label is true. The other six destination labels become "... is its protocol's"; they compare against `protocol_da()`, so these labels are true too. "every frame's EtherType (and, for AVTP, subtype) is a graded protocol's" counts `Kind::Other`, which `classify()` returns for an unknown EtherType or an unknown subtype under 0x22F0. That label is true. The computed values and the expected 0 are unchanged.
- `bootsa_mutants.py:62-73` match by substring (`:166`). `MSRP_DA` and `ADP_DA` already lacked the dropped parenthetical, so every named check still matches. The old labels appear nowhere else in the tree (`git grep`). No script, TESTING.md or CHANGELOG line reads them.
- `bootsa` (pinned Verilator 5.050 rev v5.050, identity checked): rc 0, "== bootsa: checks: 67   failures: 0 ==". Both renamed labels print with `got=0 exp=0` (`receipts/bootsa-run.log:50,53`). The figures match the author's round-3 receipts and round 2: 868 first-boot frames; 847 and 3 frames after the pair, 0 left while held; 93 control-lane frames and 3,556 octets compared, 0 changed.
- `bootsa-mutants`: the repository's own `bootsa_mutants.py` plants and verdict, run in parallel child interpreters by `scripts/run_bootsa_mutants_parallel.py`. The result is rc 0, "13 checks: 13 PASS, 0 FAIL": the clean control passes, and all twelve controls are caught by every check they name (`receipts/bootsa-mutants.log`).
- Falsification probe: the renamed AECP check is live. Under the "stamp lands on the destination" control, it fails with got=1, beside MSRP/MVRP/ADP/ACMP/MAAP (`receipts/probe-stamp-on-da.log:47-53`, 15 failures). The EtherType check stays `ok` under every control. It has no planted control (SUGGESTION S3 below); this is unchanged by the delta.

### (3) No RTL, harness logic or receipt figure changed

`receipts/delta_scope.txt` covers `git diff --stat` and `--name-status`. It shows two files, `M` only. Nothing under `hdl/`, `syn/`, `sw/`, `configs/`, `review-evidence/` or any submodule changed. The `sim_boot_sa.cpp` word diff is label text only, so no control flow, comparison or count changed. `git diff --check 604899c0..3c229478` has rc 0. The receipt figures are unchanged, as listed under (2).

**Comment rule.** No source comment is added in the delta. The added lines have no lane label, round, reviewer ID or comment ID (`receipts/delta_scope.txt` scan: none).

## Prior findings, resolved or retained at this head

| Finding | Status at 3c229478 |
|---|---|
| R774-2 F1 (MINOR, Docs) | **Resolved**: option (a) with the exact texts; line-by-line tables above |
| R774-2 S4 (SUGGESTION, Tests): stale "untouched" labels | **Taken**: both labels renamed to what they compare |
| R774-2 S1 (name every check a control fails), S2 (exported offsets for `0x108`/`0x10C`/`0x784`), S3 (`gen_boot_fw.py:112` spacing) | **Retained as optional SUGGESTIONs**, not in the round-3 assignment; unchanged at `sim_boot_sa.cpp:617,828,863-864` and `gen_boot_fw.py:112` |
| R774-1 and R773-1 findings | Resolved at R774-2 (ba56827b) and untouched by this delta, so they stay resolved |
| R773-2 findings | See "Other reviewer's round-2 items" after the ledger (read after this verdict and ledger were written) |

## New findings

There is no BLOCKER, MAJOR, MINOR or RESIDUE. The suggestions below are optional.

### S1 - SUGGESTION - Docs - "instead" sits after the stamp paragraph

- Where: `tb/verilator/milan_dp/README.md:1200-1205`.
- What: "In each early-enable boot it grades instead:" comes directly after the stamp paragraph, not after the first-boot list it replaces. A quick reader could take "instead" as replacing the stamp comparison. "in every boot" at `:1200` settles it, so this is not a defect.
- Optional fix: move the stamp paragraph (`:1200-1203`) below the early-enable list. Or write "In each early-enable boot it grades, in place of the first boot's list:".

### S2 - SUGGESTION - Docs - where the CRF parenthetical sits

- Where: `README.md:1209-1210`.
- What: "(CRF where the config declares ...)" follows the MAAP-off clause. It could be read as qualifying that boot only, while the code applies it to both boots (`sim_boot_sa.cpp:608`).
- Optional fix: "... MAAP and the CRF talker in the MAAP-on boot, the AAF talker and the CRF talker in the MAAP-off boot; in both, CRF only where the config declares the CRF Media Clock Output".

### S3 - SUGGESTION - Tests - the EtherType check has no planted control, and the AECP destination check is named by none

- Where: `sim_boot_sa.cpp:816-817` and `:808-815`; `bootsa_mutants.py:108-111`.
- What: none of the twelve controls fails the EtherType check. The AECP destination check fails under the stamp-on-destination control (probe, got=1), but no control names it.
- Optional fix: add the AECP destination label to that control's named list. Consider a harness-side negative (for example, an unknown subtype injected into the classifier's input) to show the EtherType check can fail. This is unchanged by the delta.

### S4 - SUGGESTION - Docs - prose and label wording

- Where: `README.md:1193` says "every frame is a known protocol's". The label now says "a graded protocol's".
- Optional fix: use one word for both. This is not a defect: the README describes the check and does not quote it.

## Per-lens results

```text
[R774] PASS Conformance — tb/verilator/milan_dp/sim_boot_sa.cpp:689-701,774,808-817 at 3c229478 — the renamed AECP label states the comparison the code makes (destination = kControllerMac, the MAC the leg's READ_DESCRIPTOR is sent from at :691); the other destination labels still compare protocol_da() (:172-189, its clause citations unchanged); no acceptance, clause claim or figure changed (receipts/delta_scope.txt); issue #839 acceptance 1-2 still met in simulation (receipts/bootsa-run.log 67/0), 3-4 per the maintainer record issuecomment-6655611611
[R774] PASS RTL — receipts/delta_scope.txt — no hdl/, syn/, configs/ or submodule path in ba56827b..3c229478, gitlinks verified (receipts/restore_check.txt); the RTL the R774-2 RTL lens covered at ba56827b is byte-identical here, and the 12 RTL controls rebuilt from this head's milan_datapath.sv are all caught (receipts/bootsa-mutants.log)
[R774] PASS Robustness — sim_boot_sa.cpp:549-618,759-830 at 3c229478 — the word diff changes no reset, ordering, config-dependent (kCrfOutputDeclared :608,:820) or bounded-retry path; early-enable boots MAAP on/off, 0 frames left while held, A_TXARB_DIAG 0 (receipts/bootsa-run.log:71-98)
[R774] PASS Tests — receipts/bootsa-run.log, receipts/bootsa-mutants.log, receipts/probe-stamp-on-da.log at 3c229478 — 67/0 clean; 13/13 (clean plus 12 controls caught by every named check after the rename, substring matching at bootsa_mutants.py:166); the renamed AECP check falsifiable (got=1 under the stamp-on-destination control); S3 optional
[R774] PASS Docs — tb/verilator/milan_dp/README.md:1183-1215 at 3c229478 — matched line by line against grade() :796-830 and early_enable() :599-617, including the first-boot range (:837-862) and the CRF condition (:608,:820); old labels absent from the tree; no comment-rule residue in the added lines; S1, S2, S4 optional
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_boot_sa.cpp:172-189,689-701,774,808-817`; issue #839 acceptance and decision record issuecomment-6655611611; `receipts/delta_scope.txt`; `receipts/bootsa-run.log` | R774-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| RTL | CLEAN | `receipts/delta_scope.txt` (no RTL path changed since R774-2's clean RTL lens at ba56827b); `receipts/restore_check.txt` (gitlinks); 12 RTL controls rebuilt from this head (`receipts/bootsa-mutants.log`) | R774-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| Robustness | CLEAN | `sim_boot_sa.cpp:549-618,759-830` word diff (label strings only); early-enable boot output `receipts/bootsa-run.log:71-98` | R774-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| Tests | CLEAN | `sim_boot_sa.cpp:808-817`; `bootsa_mutants.py:62-73,108-111,157-169`; `receipts/bootsa-run.log`, `receipts/bootsa-mutants.log`, `receipts/probe-stamp-on-da.log` | R774-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| Docs | CLEAN | `tb/verilator/milan_dp/README.md:1114-1239` (focus `:1183-1215`) against `sim_boot_sa.cpp:549-618,759-830,833-873`; tree-wide `git grep` for old labels; added-line comment-rule scan | R774-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |

## Other reviewer's round-2 items

I read the other reviewer's round-2 report (issuecomment-6672109925, at ba56827b) only after this verdict and ledger were written. Its items at this head:

| Item | Status at 3c229478 |
|---|---|
| R773-2 RES-1 (RESIDUE, Docs): the first list reads as covering every boot, and "also" | **Resolved**. Its outcome is met through R774-2 F1 (a)'s text, not RES-1's exact words. `:1183` now scopes the list to the first boot, and `:1205` drops "also" (it now reads "instead"). The intent is the same, and it matches the code (tables above). |
| R773-2 S1 (SUGGESTION, Tests): "untouched" parentheticals in check names | **Taken**. Both renamed. `bootsa_mutants.py` still matches (substring), and the controls pass 13/13. |
| R773-2 S2 (SUGGESTION, Docs): CRF's condition | **Taken** at `README.md:1210,1213` (see S2 above for an optional placement tweak). |
| R773-2 S3 (SUGGESTION, Tests): `gen_boot_fw.py:112` spacing | **Retained**, optional (same as R774-2 S3); the file is unchanged. |
| R773-2 S4 (SUGGESTION, Tests): PM2 is an equivalent mutant | **Unchanged**, informational. The delta touches no RTL, so the classification stands. |

Nothing in that report changes this verdict or ledger.

## What I ran

- I used the pinned simulator `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, after checking that `--version` prints `Verilator 5.050 2026-07-01 rev v5.050`.
- `make -C tb/verilator/milan_dp VERILATOR=<pinned> VERILATOR_JOBS=16 bootsa-build` (rc 0, `receipts/bootsa-build.log`), then `./obj_bootsa/Vmilan_dp_bootsa` (rc 0, `receipts/bootsa-run.log`).
- `python3 -I scripts/run_bootsa_mutants_parallel.py <clone>/tb/verilator/milan_dp <scratch> 6`, with `VERILATOR=<pinned> VERILATOR_JOBS=3` (rc 0, `receipts/bootsa-mutants.log`, 3 min 17 s). Each mutant is a child interpreter calling the repository's own `bootsa_mutants.run_mutant()`. Two earlier attempts of this wrapper were discarded and are not evidence. An in-process thread pool lost per-mutant output, because stdout redirection is not thread-safe. A process pool failed to start under the interpreter's default start method.
- Probe: the built stamp-on-destination executable rerun from `tb/verilator/milan_dp` (rc 1 as expected, `receipts/probe-stamp-on-da.log`).
- `git diff --check 604899c0..3c229478` rc 0. Scope, word diff and scan are in `receipts/delta_scope.txt`. The restore check is in `receipts/restore_check.txt`: HEAD, index tree `03d9de98…` equals the head tree, the worktree equals the index, nothing untracked, and the six gitlinks match HEAD.

## Real limits

- This is not a manager source bank. No full parent, PP, gPTP, Yosys or builder bank was run. Source-head execution evidence beyond my reruns is the author's published round-3 receipts (issue #839 REVIEW READY of round 3), whose figures my run reproduces.
- I did not re-run the docs workflow or the full sweep. I did not run hosted jobs or local act. Physical calibration was NOT RUN; simulation is not hardware proof.
- At the time of reading, the exact-head hosted contexts were mostly queued or in progress; completed ones are listed in `receipts/hosted_checks.txt`. No hosted result is claimed here.
- Lenses outside the delta carry their R774-2 verdicts by dependency: the delta changes nothing they depend on. I spot-checked them, but did not re-derive them in full.

## Pending manager duties

- Hosted acceptance at the exact head (rtl-fast, verilator-suites, yosys-portability), and act acceptance.
- The current-dev merge candidate (builder and native banks) at the merge turn, against live dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- Carry S1-S4 and the retained R774-2 S1-S3 to the author as optional.
- Post-merge containment and the Issue's closure and move to Done. A maintainer must authorize the merge.

R774-3 FINISHED
