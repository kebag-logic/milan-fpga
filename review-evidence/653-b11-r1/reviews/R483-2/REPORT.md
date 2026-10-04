[R483] POSITIVE - exact head 6b83de0009673ce2c438985a0f9720f079a3715d

# R483-2: external re-review of PR #659 (Refs #653, bench lane B11), round 2

- **Head:** `6b83de0009673ce2c438985a0f9720f079a3715d`, tree `2f5399e4b187d30847191e13743b36cad9aeb63b`. Two commits on dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`: round 1 `6f76d612` and round 2 `6b83de00`. Live dev is still `6c22d3ca` (`receipts/clone_integrity.txt`).
- **Delta judged:** `6f76d612..6b83de00`, docs only. It touches `docs/findings/653_DISCONNECT_ORDER_BENCH.md` (+50/-13) and the page's row at `docs/findings/README.md:16` (+1/-1) (`receipts/delta_6f76d612_6b83de00.diff`). No HDL, test, script or gitlink change.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md (sections 6 and 6.1, and the PR template rule at :405);
  - `.github/PULL_REQUEST_TEMPLATE.md` and docs/README.md;
  - the #653 body and acceptance 1-4;
  - the lane comments on #653: the B11 assignment 5983239639, the round-2 assignment 5983716764 and REVIEW READY 5983801043;
  - the PR #659 body at the head;
  - the public evidence branch `653-b11-review-evidence`: round-1 author files at `980c5784`, and the round-2 author receipts `author-r2/round2/` at `9bb441d3`;
  - the upstream controller library source at the cited tag.
- **Role:** cleared-context external reviewer. No author contact, no GitHub write, no source edit.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR, MINOR or RESIDUE is open. Two optional SUGGESTIONs follow.

Every round-1 finding, mine and the internal reviewer's, is resolved at this head. The checks:

- **The library citation.** I fetched the upstream code it cites and re-read it there.
- **The new figures.** I recomputed them from the round-1 raw files and ran three planted controls against that recomputation.
- **Nothing measured moved.** No figure, per-cycle row, capture hash or tool hash changed from round 1.
- **The gates.** The docs gates pass at the head.

## Round-2 assignment items, checked

### 1. The library check (my R483-1 F2, the internal reviewer's R482-1 F1)

**The citation is right.** At page :226-238 the check is cited at tag `v4.3.1.1`, commit `6d61a92e`, `src/controller/avdeccControllerImpl.cpp:1611-1613`.
- `git ls-remote` peels tag `v4.3.1.1` (tag object `080ab851`) to commit `6d61a92e7f264c69f23cdc38f50d31114e567aa0` (`receipts/avdecc_ls_remote_tags.txt`).
- At that commit, :1611 is `if (lockedValue != unlockedValue && lockedValue != (unlockedValue + 1))` and :1613 is the `removeCompatibilityFlag(... Milan, "Milan 1.3 - 5.3.8.10", "Invalid MEDIA_LOCKED / MEDIA_UNLOCKED counters value on STREAM_INPUT: " ...)` call (`receipts/avdecc_v4.3.1.1_ControllerImpl_1600-1616.txt`).
- The file's SHA-256 is `5f70fbfa…`, the same as in the lane's `round2/library-check.txt`.

**"In the function that stores every counters update" holds.** The check sits in `ControllerImpl::updateStreamInputCounters`, which has four callers:
- the unsolicited-notification delegate, `avdeccControllerImplDelegateOverrides.cpp:787`;
- the enumeration and GET_COUNTERS result handlers, `avdeccControllerImplHandlers.cpp:528` and `:2484`;
- the virtual override, `avdeccControllerImplOverrides.cpp:3681`.

**"One check on a STREAM_INPUT's counter values" holds.** The tag has 76 `removeCompatibilityFlag` call sites (`receipts/avdecc_v4.3.1.1_compat_removals.txt`). 72 pass a literal clause and message, and four of those name STREAM_INPUT. The other four forward computed text from the misbehaving and Milan-downgrade helpers and from CONTROL value validation. Only `:1613` judges counter values:
- `ImplHandlers.cpp:524` and `:2479` are presence checks, "mandatory counters missing";
- `:5077` is a format rule.

**"The library's one other use of MEDIA_UNLOCKED" holds.** Under `src/`, `avdeccControllerImplHandlers.cpp:35`, the mandatory-counter list, is the only other one. The `include/` hits are the enum definition and the JSON name table.

**The stated condition (page :233-234, :240) is exact.** The Milan flag is removed only when MEDIA_LOCKED is neither MEDIA_UNLOCKED nor MEDIA_UNLOCKED + 1, and connection state is not an input. It therefore accepts 1/1 and 1/0, bound or not. It can flag neither order nor the CRF 1/0 window.

**The bench build is tied to the tag.** The copied header `avdeccVirtualControlledEntityInterface.hpp` hashes `3d09fa69…` at the tag, equal to `runs/build/build-3.txt` and to the page's hash table. The same receipt's describe line reads `v4.3.1.1` (`receipts/header_vs_tag.txt`).

**Every library update is one the check accepts (page :242-244).** Recomputed from `runs/s0b/s0b-probe.jsonl` and `runs/s1/s1-probe.jsonl`, the 69 DUT STREAM_INPUT counters updates are exactly 0/0 Connected ×23, 1/0 Connected ×23 and 1/1 NotConnected ×23 (`receipts/r2_recompute.txt`). All three are accepted, no update carried a compatibility event, and the Milan flag was present on every one.

**The acceptance row, headline and README now read as "no miscount".**
- Acceptance row 4 (:46) reads "No miscount flagged by the library; not a test of the order", and its evidence cell states the condition.
- The headline (:37-39) says the silence "is not evidence about the order".
- The README row (:16) carries the same qualification.

**The CRF section (:277-287) is right.**
- The 1/0 held in the window is the update delivered about 1,000 ms after the bind, while Connected.
- No counters update reached the library inside either window. R01 lasted 95.0 ms and R02 100.0 ms, and the next update carried 1/1/0 (`receipts/r2_recompute.txt`).
- Its closing sentence makes no tolerance claim.

**The conclusion is stated (:248-249).** It says the owner's flag cannot come from this library check and must come from the Hive application's own rules, which were not run. It also appears in Limits (:318-322) and in "read from source, not the installed binary" (:323-324).
- It holds beyond the build's tag. The condition is identical at `v4.3.0`, at current upstream `main` (`2fd57534`) and at `dev` (`a3a6292`), and at `v4.1.0` apart from its log text and its Milan 1.2 citation. None of them takes connection state as an input (`receipts/avdecc_check_across_refs.txt`).

### 2. The control interval (my R483-1 F1, the internal reviewer's R482-1 F2)

The page now reads (:260-261): "The UNBIND_RX command left 1,629.8 µs after the probe's own GET_COUNTERS answer, and its response 1,637.3 µs after it."

I recomputed both figures from the provided decoder's C0 output (`summary/decode/b11-a535-s0b-C0.decode.txt`). The time column reads the tap's two words swapped, so the true ns interval is ΔS / 2^32:
- own answer to UNBIND_RX command: **1,629.836 µs**;
- own answer to UNBIND_RX response: **1,637.340 µs**;
- command to response: 7.504 µs.

These agree with the grade's `own_rsp_to_cmd_us` 1629.8 and `cmd_to_rsp_us` 7.5, and with the lane's `round2/control-interval.txt`. The control still reads COUNTERS_FIRST against the probe's own answer and RESPONSE_FIRST against the unlock's push.

### 3. Identity row, PR body and the other residue

**Identity row (:64)** reads exactly as my R483-1 R1 asked: "Equal to the build's AEM image, except the three live-state fields below; the scripted gate reports FAIL on exactly those three".
- `identity/identity-verdict.txt` has exactly three FAIL lines: `aecp-STREAM_INPUT 0` at offset 78, `aecp-CLOCK_DOMAIN 0` at offset 71, and `get-clock-source`.
- These are the three values named at :67-69.
- This also answers the internal reviewer's S1.

**The PR body** (read at the head) now has the template's sections in order:
- Status, with the branch -> `dev`;
- Linked Issue / roles: `Refs #653` as the B11 assignment directs, the executor, and both reviewers;
- Description, Authoritative references (which add the upstream link), How to get into the same state, and How to validate, with commands and an expected-result table;
- Known limitations / out of scope, and Definition of Done.

It adds one "Round 2" section. The round-1 content is kept. This answers my R483-1 R2.

**The control-selection sentence** (:266-268) and its Limits line take the internal reviewer's S2 and my S1. My S2 was not taken, which is within its optional status. Every capture holds one UNBIND_RX command and one response.

### No measurement, figure or capture changed (`receipts/r2_controls_and_numbers.txt`)

- **Numeric tokens:** comparing round 1 with round 2, the page and README removed no numeric token.
- **Tokens added:** the tokens the page adds are the tag and line numbers (4.3.1.1, 1611-1613, 35), the pieces of the commit hash inside the URL, the counter pairs 0/0, 1/0 and 1/1, and 1,637.3.
- **Rows:** the 24 per-cycle rows, the 23 capture-hash rows and the 8 lane-file hash rows are byte-identical between `6f76d612` and `6b83de00`.

## Findings

### S1: SUGGESTION | Docs | `docs/findings/653_DISCONNECT_ORDER_BENCH.md:235-236` | The second library path has no commit link

`src/controller/avdeccControllerImplHandlers.cpp:35` is cited bare. The check it accompanies (:229) carries a pinned link.

A cold reader may take it for a path in this repository. The repository's path gate does not resolve it either way. Linking it at the same commit, `6d61a92e…#L35`, would make it checkable in one click. Optional.

### S2: SUGGESTION | Robustness, Docs | `docs/findings/653_DISCONNECT_ORDER_BENCH.md:318-322` | The library-version limit could be bounded

The page says the owner's library version is unknown.

The STREAM_INPUT check's condition is the same, with no connection-state input, at upstream `v4.1.0`, `v4.3.0`, `v4.3.1.1`, current `main` and current `dev` (`receipts/avdecc_check_across_refs.txt`). A clause saying so would show that the "must come from Hive" conclusion does not depend on which recent library version the owner ran. Optional.

## Prior public review findings on this PR: resolution at this head

| Finding | Severity | State at `6b83de00` | Evidence |
|---|---|---|---|
| R483-1 F1, control interval names the wrong event | MINOR | RESOLVED | page :260-261; `receipts/r2_recompute.txt` (1,629.836 / 1,637.340 µs); M1 control fails on a reverted figure |
| R483-1 F2, library check without receipt, and blind to the order | MINOR | RESOLVED | page :37-39, :46, :226-249, :277-287, :318-324; README :16; `receipts/avdecc_*`, `receipts/r2_recompute.txt` |
| R483-1 R1, identity row wording | RESIDUE | RESOLVED, as written | page :64; `identity/identity-verdict.txt` three FAIL lines |
| R483-1 R2, PR body not in template sections | RESIDUE | RESOLVED | PR #659 body at the head, template sections in order |
| R483-1 S1, the control does not exercise push selection | SUGGESTION | TAKEN | page :266-268 and Limits |
| R483-1 S2, decoder order takes the first response unfiltered | SUGGESTION | NOT TAKEN; optional, stands | one command and one response per capture (round-1 `decode_structure`) |
| R482-1 F1, library silence offered as order evidence | MINOR | RESOLVED; every required outcome is present | same as R483-1 F2; Limits :318-322 names the layer above the library as the only remaining source |
| R482-1 F2, control interval | MINOR | RESOLVED | same as R483-1 F1 |
| R482-1 S1, name the identity tool's aggregate FAIL | SUGGESTION | TAKEN | page :64 |
| R482-1 S2, the control does not exercise push selection | SUGGESTION | TAKEN | page :266-268 |

I read the prior findings only after my independent pass, and after a draft verdict and ledger were on disk. One wording difference: R482-1 F1 says the library has no other MEDIA_UNLOCKED use, while the page says it has one other, the mandatory-counter list at `ImplHandlers.cpp:35`. The upstream source supports the page. Its statement is the more precise one, so nothing is owed.

## Clean lenses (evidence at the head under review)

```text
[R483] PASS Conformance - docs/findings/653_DISCONNECT_ORDER_BENCH.md:37-46,:226-249,:260-261,:277-287 at 6b83de00; upstream avdeccControllerImpl.cpp:1605-1615 at 6d61a92e - #653 acceptance 1-4 wording against the per-cycle evidence, and the library check's condition, scope and callers against the tag's source
[R483] PASS RTL - receipts/clone_integrity.txt - 6c22d3ca..6b83de00 touches only two docs pages; no hdl/tb/syn/scripts path; four gitlinks equal to base; the round-2 delta makes no RTL claim (the :272-275 PR #655 statement is unchanged from round 1)
[R483] PASS Robustness - page :240-249, :277-287, :318-336; receipts/avdecc_check_across_refs.txt, receipts/r2_recompute.txt - claims bounded: the check cannot fire in either order or in the 1/0 window (and holds across upstream versions); no update fell inside either CRF window; limits for one controller, push cadence, source-not-binary and the unknown owner versions are stated
[R483] PASS Tests - receipts/r2_recompute.txt, receipts/r2_controls_and_numbers.txt - both control figures and the 69-update census recomputed from raw round-1 files; three planted controls fail as they should (reverted figure M1, a 2/0 update M2, an update inside the R01 window M3); the control sentence now limits its claim to the comparison
[R483] PASS Docs - page delta, docs/findings/README.md:16, PR #659 body; receipts/docs_gates.txt - 14 of 14 gates rc 0 at the head (docs_check, doc_style, gen_toc check and anchors, em-dash against 6c22d3ca (394 lines) and 6f76d612 (51 lines) and its selftest, doc_paths, ci_scope, baremetal check and selftest, feature_status, diff --check on both ranges); no table, hash or number regressed; the upstream link follows the precedent in docs/testing/MILAN_V12_AUDIT_2026-08-16.md:69
```

## Reviewer-owned lens ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page :37-46, :226-249, :260-261, :277-287; #653 acceptance 1-4; upstream `avdeccControllerImpl.cpp:1605-1615`, its callers, and all 76 compatibility-removal call sites at `6d61a92e`; `summary/o653-grade.json`; probe logs s0b/s1 | R483-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| RTL | CLEAN | `receipts/clone_integrity.txt`: name-status for both ranges, modes and blobs, gitlinks equal to base, no hdl/tb/syn/scripts path; round-2 delta carries no RTL claim | R483-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| Robustness | CLEAN | page :240-249, :277-287, :316-336; `receipts/avdecc_check_across_refs.txt` (v4.1.0, v4.3.0, v4.3.1.1, main, dev); CRF window census in `receipts/r2_recompute.txt` | R483-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| Tests | CLEAN | `scripts/r2_recompute.py` with `receipts/r2_recompute.txt` (12 checks, PASS); `scripts/r2_controls_and_numbers.sh` with `receipts/r2_controls_and_numbers.txt` (M1, M2 and M3 each rc 1; rows identical); control C0 decoder text and grade | R483-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |
| Docs | CLEAN | `docs/findings/653_DISCONNECT_ORDER_BENCH.md` delta (Contents :25, :37-39, :46, :64, :226-249, :260-268, :277-287, :318-324); `docs/findings/README.md:16`; PR #659 body against `.github/PULL_REQUEST_TEMPLATE.md`; `receipts/docs_gates.txt`; privacy and vendor-name precedent | R483-2 | `6b83de0009673ce2c438985a0f9720f079a3715d` |

## Real limits

- **Captures not re-read.** The 23 captures are not public. Round 2 changes no capture-derived figure, and the two control figures were re-derived from the provided decoder's published text and the grade JSON.
- **Library read from public source.** The check was read in the upstream source at the cited tag and at other public refs, not in the bench host's installed binary. The tie between the two is the describe line and the copied header's hash. Library versions older than `v4.1.0` were not read.
- **Hive not run.** The Hive application was not run by the lane or by this review, so acceptance 4 at the Hive layer stays open.
- **No bench or hosted runs.** No hardware, bench lock, Docker or act run was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted docs-check unfinished.** Hosted check-runs at the head were read twice (`receipts/hosted_checks.txt`). 7 succeeded: `rtl-fast`, `full-ci-gate`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability` and `docs-check-no-git`. 7 were skipped, including `verilator-suites` and `yosys-portability`, as expected for a docs-only head. `docs-check` was still in progress at 2026-10-04T20:08:25Z, and the combined status was pending.

## Pending manager duties

- Hosted acceptance at the exact head: confirm `docs-check` completes successfully. Own the act replica.
- Build and validate the final current-dev candidate at the merge turn. The source base and live dev are both `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`.
- Collect the parallel internal round's verdict. The merge bar needs two positive reviews and the complete ledger.
- S1 and S2 are optional, and no residue is carried.
- Keep #653 open: this PR refers to it, and acceptance 4 at the Hive layer is not tested.
- Merge only with explicit maintainer authorization.

## Receipts (all listed in `MANIFEST.sha256`)

- **Change scope:** `receipts/delta_6f76d612_6b83de00.diff` is the round-2 delta.
- **Upstream library check:** `scripts/avdecc_check_refs.sh` and `receipts/avdecc_check_across_refs.txt` read the check at five upstream refs. Also `receipts/avdecc_ls_remote_tags.txt`, `receipts/avdecc_v4.3.1.1_ControllerImpl_1600-1616.txt` and `receipts/avdecc_v4.3.1.1_compat_removals.txt`.
- **Header hash:** `receipts/header_vs_tag.txt`.
- **Recomputation:** `scripts/r2_recompute.py` and `receipts/r2_recompute.txt` cover the control intervals, the library-update census and the CRF windows.
- **Controls and numbers:** `scripts/r2_controls_and_numbers.sh` and `receipts/r2_controls_and_numbers.txt` hold the planted controls and the number and row comparison.
- **Docs gates:** `scripts/docs_gates.sh`, `receipts/docs_gates.txt` and `receipts/docs_gates/gate_01.log` to `gate_14.log`.
- **Hosted checks:** `receipts/hosted_checks.txt`.
- **Clone integrity:** `receipts/clone_integrity.txt` covers the clone at the exact head (index, status, modes, gitlinks) and the live dev tip.

R483-2 FINISHED
