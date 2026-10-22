[R683] POSITIVE - exact head 1098978f4a931a667e147b68a791520eb141c917

Round R683-2 is the internal cleared-context review of kebag-logic/milan-fpga PR #772 (Closes #771, the fourth pin adoption). It covers exact head `1098978f4a931a667e147b68a791520eb141c917`, tree `cad31d5084366583e8cd18c46e71ca6277c5d825`, and the round-2 delta `a97aea01..1098978f` (`b6fc1590`, `bbdd24d0`, `1098978f`). Source base `d77a8afd`.

I applied all five lenses to the delta, and checked each named prior finding at its cause. No BLOCKER, MAJOR or MINOR finding is open, so the verdict is POSITIVE. Three wording RESIDUE items and four SUGGESTIONs are listed below so the author can take them in one pass.

## Summary

- **Item 1 is case (a).** The production firmware follows processor #189, and only the walk's test adapter was stale.
  - The SRP delivery `sw/firmware/ctrl/app/ctrl_app_srp.c:90-100` sends a registered sink outside SETTLED_NO_RSV, whose kind differs, to `acmp_tk_kind_changed`.
  - `third_party/tsn-c-stack/src/acmp.c:1176-1187` refuses that call outside SETTLED_RSV_OK. Otherwise it sets `tk_failed` with no arc and calls `finish()`.
  - `finish()` (`:495-515`) notifies once when the Table 5.22 view changes. That view includes `registering_failed = talker_registered && tk_failed` (`:431-432`, compared at `:441-448`).
  - GET_RX_STATE sets REGISTERING_FAILED from the same field (`:891-892`).
  - This is exactly the adopted model at `protocol-processor/tb/acmp_listener/sim_main.cpp:404-408` and `:1179-1182`: in SOK, REGISTERING_FAILED follows the registered type, with no state change, frame or strobe (Milan v1.2 Table 5.39).
  - tsn-c-stack is unchanged (`70936b77` at base and head), and nothing under `sw/firmware/ctrl/app` changed since `d77a8afd`.
- **The walk adapter is correct, and the oracle is unweakened.**
  - `b6fc1590` changes only `drive()` (`sw/firmware/ctrl/test/acmp_walk.cpp:259-262`) and the header comment. A `tk_kind == 2` stimulus in SETTLED_RSV_OK now goes to `acmp_tk_kind_changed`, with the same NO_RSV / RSV_OK split as the production glue. Every other state keeps `acmp_tk_registered`.
  - `m.predict` and every comparison are untouched, and the model is still cut from the pinned processor.
  - My own runs at the head (`receipts-walk-probe.txt`):
    - `acmpwalk` 127/0 and `acmp` 130/0.
    - With only the new `drive()` branch removed from the checkout, `acmpwalk` returns to 127/1 with exactly the base's two `TK_REG_SOK` failures (`receipts-walk-revert-probe.txt`; file restored, blob `02afed8b` = HEAD).
  - Both planted controls are KILLED in `acmp` and `acmpwalk` on my runs:
    - `acmp-kind-lost`: walk "registered state" and "notified exactly when a Table 5.22 item moved"; `AcmpCore.KindChangesOnlyTheSettledView` "kind updates the reported view".
    - `acmp-kind-not-notified`: the walk's notification check alone, and `AcmpCore` "kind change notifies once".
  - A control of my own, `rev-kind-inverted` (`tk_failed = !failed`), is also KILLED in both arms.
- **Items 2 and 3 match the donor.** The FPGA-gPTP `55680bff` engine (`hdl/top/KL_gptp_engine.sv:117-122`, `:705-736`, `:973-990`) gives:
  - count 0: absent TLV;
  - 1 to 7 received entries: count + 1, ending with thisClock;
  - 8 or more: the first eight, count 8, no thisClock;
  - reset or self-master: `{thisClock}`, count 1.

  The `REGISTER_MAP.md`, `SUBMODULES.md` and `CHANGELOG.md` bound text and the five F3 places state this. The three `.sv` hunks are `//` comment lines only: 0 non-comment changed lines and an identical comment-stripped body (`receipts-sv-comment-only.txt`).
- **Item 4: the gate claims match the receipts.**
  - The published evidence tree `b6d9eaa1` checks against its publication `MANIFEST.json`: 393 files, 0 failures, 87 path-redacted. All 149 round-2 originals match the author's `round2/MANIFEST.sha256`. The `.gz` was not published; the text log was (`receipts-publication-verify.txt`).
  - Each figure in the PR body and REVIEW READY comment appears in a receipt at head `1098978f` with dirty=0:
    - sweep 63/63, 2,189,520 checks;
    - physical leg 209;
    - Yosys 58/58, 0 unjustified ties;
    - behave 406 / 1,977;
    - xvlog 0;
    - docs steps 44, with 42 rc 0 and 2 SKIP;
    - quick gates all rc 0;
    - firmware gate set: see the list under the prior-findings table.
  - The census rc 1 reproduces byte-identically on my run, and its inputs (`.github/`, `scripts/ci_*.py`) are unchanged since `d77a8afd` (`receipts-firmware-census-head.log`).

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

### R683-2-R1 — RESIDUE — Docs, Tests
- **Artifact:** `tb/verilator/gptp_shadow/sim_main.cpp:591-592` (the `announce_one_path` helper; in the PR diff, not in the round-2 delta).
- **Evidence:** the comment says "its served sequence is exactly `[GM]`". Since #85, the test it feeds expects count two ending with thisClock (`:929-932`). This is the same stale meaning R683-1-F3 removed from the five contract places.
- **Exact fix:** replace line 592 with `//! the absent-TLV spelling: it publishes [GM, thisClock], count two (FPGA-gPTP #85).`
- Wording only. No check changes.

### R683-2-R2 — RESIDUE — Docs
- **Artifacts:** `CHANGELOG.md:76` "(gPTP #86)" and `docs/reference/REGISTER_MAP.md:1482` "(FPGA-gPTP #86;".
- **Evidence:** next to "gPTP #82", "#84" and "#85", which are issue numbers, `#86` reads as an issue. It is the PR (`SUBMODULES.md:244` links `pull/86`).
- **Exact fix:** "(gPTP PR #86)" and "(FPGA-gPTP PR #86;".

### R683-2-R3 — RESIDUE — Docs
- **Artifact:** the PR #772 body, Known limitations, docs-check bullet.
- **Evidence:** "...2 skipped by rule. Two steps were skipped by rule." The sentence is repeated.
- **Exact fix:** delete "Two steps were skipped by rule."

### R683-2-S1 — SUGGESTION — Docs, Conformance
- **Artifacts:** "count one is ... before a peer is elected", at `KL_gptp_shadow.sv:637-638`, `KL_pp_shadow.sv:461`, `milan_datapath.sv:2156-2157`, `README.md:172` and `REGISTER_MAP.md:335-336`.
- **Evidence:** the donor also republishes `{thisClock}` after a departed peer, and whenever the local vector wins (`KL_gptp_engine.sv:121`, `:705-712`).
- **Suggestion:** "while this station is its own grandmaster (from reset, or after its peer is lost)" is more exact. The current text follows the assignment's wording and the parent's existing convention (`REGISTER_MAP.md:1051`), and is not false.

### R683-2-S2 — SUGGESTION — Tests
- **Artifact:** `sw/firmware/ctrl/test/srp_feedback.hpp:85-110`.
- **Evidence:** the composed-app swap tests install a `CHANGED` hook but never require that it fired. The author's probe (`case-a/probe-production-check.diff`) adds that assertion.
- **Context:** without it, a muted stack notification is caught on the composed path only indirectly, by `KindThenWithdrawalIsDeliveredInOrder` (stack-mute receipts), and directly by `AcmpCore` and the walk.
- **Suggestion:** commit the probe's two `EXPECT_FALSE(fk.hook)` lines.

### R683-2-S3 — SUGGESTION — Docs, Tests
- **Artifact:** `round2/firmware-gates/env.txt`.
- **Evidence:** the receipt records `clang --version` (host 23.1.1). The stack gate invokes `clang-18` by name (`third_party/tsn-c-stack/scripts/compiler_tokens.py:12`), so the REVIEW READY "Clang 18.1.3" is inferred from the PATH setup, not receipted. `ctrl_boundary` rc 0 shows the stack gate ran.
- **Suggestion:** record `clang-18 --version` in the env receipt.

### R683-1-S1 — SUGGESTION, retained (not taken)
`ucode.hex` Makefile prerequisites omit `aecp_commands.json` and `aecp_fields.json`. The round-2 delta does not touch them.

## Prior public findings at this head (read after my independent pass)

| Finding | Status at `1098978f` | Evidence |
|---|---|---|
| R683-1-F1 BLOCKER | RESOLVED at source. The hosted part of its verification is a manager duty. | Case (a) proven on the production path (above). The local firmware gate set at `CI_WORKFLOWS.md:3158-3172` ran at the head with the verified SDK (`--verify-only` receipted). See the list after this table. |
| R684-1-F1 MAJOR | RESOLVED | The stimulus goes through the production API; the oracle is unchanged. The registered-type and notification checks are retained, and the two adverse controls are KILLED (author receipts and my runs). The PR's DoD "Required local verification bar passes" is now supported by receipts. |
| R683-1-F2 MINOR | RESOLVED | `REGISTER_MAP.md:1480-1484`, `SUBMODULES.md:244` and `CHANGELOG.md:74-76` name the bound. This matches the donor at `KL_gptp_engine.sv:717-736`. |
| R683-1-F3 MINOR | RESOLVED | All five places state 0 = absent, 1 = `{thisClock}` (#82), and an explicit one-entry `[GM]` = count two (#85). Comment-only (receipt). `check_port_contracts`, `lint_rtl --check` and `pp_resource_gate.py check-baseline` rc 0 on my spot run (`receipts-spot-gates.txt`). One further stale test comment is R683-2-R1. |
| R683-1-R1 RESIDUE | RETAINED for the residue checklist | `hdl/milan/KL_pp_shadow.sv:1281` still opens "scratch only:". The author defers it, as the residue rule allows. |
| R683-1-S1 SUGGESTION | RETAINED, not taken | See above. |

Local firmware gate results for R683-1-F1:
- `tally_selftest --mutants`: 18 of 18.
- `test_ctrl_firmware --require-rv32 --self-test --lwsrp`: PASS; 66 tallies, 1,593 checks, 0 failures; control mutants 521 of 521; a further 358 AECP/SRP/lwSRP-pin `[ok]`, 0 escaped.
- `ctrl_boundary`: rc 0 under the LiteX interpreter. The host-python run was refused (rc 2, migen), which is disclosed.
- `test_ctrl_nvm`: 435 tests; 109 of 109 planted defects caught.
- `fw_coverage --selftest`: 29 of 29.
- `fw_coverage --check`: PASS, 30 files.
- The digest the capture pins is unchanged, because round 2 touches only `sw/firmware/ctrl/test/`.

## Lens results

[R683] PASS Conformance — `sw/firmware/ctrl/app/ctrl_app_srp.c:90-100`; `third_party/tsn-c-stack/src/acmp.c:431-448,495-515,891-892,1160-1187`; `protocol-processor/tb/acmp_listener/sim_main.cpp:400-408,1179-1182`; `gptp-processor/hdl/top/KL_gptp_engine.sv:117-122,705-736,973-990`; the delta's doc hunks — the production SOK swap was checked against Milan v1.2 Table 5.39 / 5.22 as the adopted model encodes them, and the path-count and bound text against the donor RTL. Case (a); no divergence.

[R683] PASS RTL — `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:634-643`, `hdl/milan/KL_pp_shadow.sv:457-466`, `hdl/milan/milan_datapath.sv:2153-2160`, `receipts-sv-comment-only.txt` — every changed line is a comment, and the comment-stripped files are identical to `a97aea01`. The `gsi_asp_chg_i` contract text now matches the comparator it describes. Lint, port contracts and baseline are rc 0. RTL logic is unchanged since R684-1's RTL lens at `a97aea01`, and the delta changes nothing that lens depended on.

[R683] PASS Robustness — `sw/firmware/ctrl/test/acmp_walk.cpp:259-262`, `ctrl_app_srp.c:90-100`, `acmp.c:1176-1187`, `receipts-walk-probe.txt` (the `rev-kind-inverted` control) — the new branch fires only in SETTLED_RSV_OK, and every other state keeps the refusing `acmp_tk_registered`, as in production. A same-kind call is idempotent ("same kind is idempotent" is graded and is killed by both controls). The inverted-kind defect is caught. The 8-or-more-entries bound case is documented.

[R683] PASS Tests — `sw/firmware/ctrl/test/acmp_walk.cpp`, `sw/firmware/ctrl/test/acmp_mutants.py:372-382`, `receipts-walk-probe.txt`, `receipts-walk-revert-probe.txt`, author `round2/case-a/*` and `round2/firmware-gates/text/ctrl_firmware.log` — the walk passes 127/0 at the head and fails 127/1 without the fix, so the fix is what turns the oracle green. Both new controls name live checks and are KILLED. 521 of 521. tsn-c-stack's own tests are unchanged.

[R683] PASS Docs — `docs/reference/REGISTER_MAP.md:332-338,1474-1484`, `docs/reference/SUBMODULES.md:244`, `CHANGELOG.md:69-76`, `README.md:168-176`, the live PR body (Validation, Known limitations, DoD), the REVIEW READY comment — the bound and the count meaning are stated, and every gate figure traces to a receipt. Only RESIDUE R1 to R3 and SUGGESTIONs S1 and S3 remain.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_app_srp.c:90-100`; `acmp.c:431-448,495-515,891-892,1160-1187`; processor `sim_main.cpp:400-408,1179-1182`; gPTP `KL_gptp_engine.sv:117-122,705-736,973-990`; delta doc hunks | R683-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| RTL | CLEAN | three `.sv` comment hunks; comment-stripped comparison vs `a97aea01`; lint, port-contract and baseline spot gates | R683-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| Robustness | CLEAN | `acmp_walk.cpp:259-262` state split vs production glue; idempotence check; reviewer inverted-kind control; bound documentation | R683-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| Tests | CLEAN | own `acmp`/`acmpwalk` runs: head, both controls, reviewer control, drive() revert; author control/production/gate receipts; 521/521 | R683-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| Docs | CLEAN (RESIDUE R1–R3 carried) | REGISTER_MAP, SUBMODULES, CHANGELOG, README, live PR body, REVIEW READY, publication manifest | R683-2 | 1098978f4a931a667e147b68a791520eb141c917 |

## Real limits

- I did not re-run the full firmware gate set, the sweep, Yosys, behave, xvlog, docs steps or the image builds. They rest on the author's published source-head receipts, which I checked by section and against the publication manifest.
- My own executions:
  - the `acmp` and `acmpwalk` arms, unplanted, with the two author controls, with one reviewer control, and with the test-side revert;
  - the firmware census;
  - five fast doc/RTL gates.
- My first test-side revert attempt is void and is marked in its receipt: the arms compile test sources from the checkout, not the planted copy. The valid revert was applied to the checkout and restored.
- On this host the `clang-18` wrapper under the tools directory now points to a missing path, so I could not re-run `ctrl_boundary`. Its PASS rests on the author's receipt.
- No manager source bank exists at this head, and none is inferred.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted acceptance at this exact head. At my snapshot (`receipts-hosted-checkruns-1098978f.tsv`, 18:06Z), `firmware-unit`, `firmware-control-mutants`, `firmware-srp-mutants`, `firmware-boundary`, `firmware-verilator`, the Verilator shards and Yosys were queued or in progress. `firmware-aecp-mutants`, `wire-accountability`, `verilator-lint`, `bdd-conformance` and `docs-check-no-git` had succeeded. Physical gPTP was skipped by its schedule. R683-1-F1's hosted verification is these contexts.
- The current-dev merge candidate (builder and native banks), and the external positive review.
- Open an Issue for `scripts/ci_events.py --firmware-census` rc 1. It is pre-existing on `d77a8afd` and out of this PR's scope.
- Carry R683-1-R1 and R683-2-R1 to R3 to the residue checklist.
- After merge: the donor-issue closures (keep processor #190's CRF step tracked), the identity gate, the #637 cold cycle and the soak. #76 follows #770.

Receipts and scripts are listed in `MANIFEST.sha256`. Clone restoration was verified by `receipts-integrity.txt`: index equals HEAD, 1,423 tracked blobs have their bytes and modes, and all six gitlinks are clean, including processor `93fb0b2d`, gPTP `55680bff` and tsn-c-stack `70936b77`.

R683-2 FINISHED
