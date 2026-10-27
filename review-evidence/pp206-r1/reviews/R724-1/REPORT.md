[R724] NEGATIVE - exact head e9272b5635e76bf12a69376d59fd21d059cae320

# R724-1: external independent review of processor PR #208 (issue #206)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #208, issue #206
- Exact head `e9272b5635e76bf12a69376d59fd21d059cae320`, tree `0482079467bc4e40ebac7997441c9569b4cc4a8f`
- Base: processor main `097a79875f20c27f0a5987a193c165c5086f3cf5`; reviewed delta `git diff 097a7987..e9272b56` (two commits, `9abb41f`, `e9272b5`; 9 files, +291/-14)
- Public evidence read: milan-fpga `2d5d308a45c997a29a2fac945cae4d2b838bdd33:review-evidence/pp206-r1` (1,012 files, every file's sha256 equal to its MANIFEST.json `published_sha256`, none redacted)
- Round: R724-1, cleared context, external reviewer. Resumed once after a memory stop of the review unit (not a review failure); every receipt cited below was produced by this round after the resume, or is a pre-stop receipt re-checked against the same head.

## Verdict

NEGATIVE. The RTL change is correct and conformant, the four required cases and the pass-through mutant behave as claimed, the docs rows are updated, the parent idiom gates pass, and no port, parameter or register-map line changed. One MINOR test finding (R724-1-F1) is open: a gate that clears more than the three Table 5.9 flags survives the entire processor-top suite, so check (2) "every other GET_STREAM_INFO flag unchanged" is not guarded by any test at this head. It leaves the Tests and Robustness lenses unclean.

## Findings

### R724-1-F1 - MINOR - Tests, Robustness

- **Where:** `tb/pp_top/sim_main.cpp:1474` (the harness integrator's STREAM_INPUT flags word is `0x80000000 | type<<8 | index`), `tb/pp_top/sim_main.cpp:2055` (section GI's settled-gate mode adds only `0x52000000`), `tb/pp_top/gsi_internal.hpp:622-633` and `:649` (`gate_expected` / `gate_frame`); gate under test `hdl/top/protocol_processor_top.sv:3583`.
- **Authority:** issue #206 "Required": clear STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID (mask `0x52000000`) in selector 0, nothing else; review check (2): every other GET_STREAM_INFO field and flag unchanged; docs `06_aecp_engine.md:464` and `docs/guides/integrator.md` §8: BOUND (`0x04000000`), MSRP_ACC_LAT_VALID (`0x20000000`) and MSRP_FAILURE_VALID (`0x08000000`) stay integrator-owned.
- **Evidence (reviewer-run, exact head):** while an input is unsettled, the only selector 0 flags any harness answer carries are STREAM_FORMAT_VALID, the three gated flags, STREAMING_WAIT (section GI's `gsi_fold_sw`) and tag bits. So the byte-exact checks grade only those bits:
  - `R-mask-overclears-format` (mask `~0xD2000000`, also clearing STREAM_FORMAT_VALID) is killed: 61 GI failures (`receipts/reviewer_probes_2.log`).
  - `R-mask-overclears-bound` (mask `~0x56000000`, also clearing BOUND while unsettled) **survives**: section GI 6,373 checks, 0 failures (`receipts/reviewer_probes.log`). It also survives the full `make -C tb/pp_top run`: rc 0, 10,317 + 20 + 178 + 292 + 56 + 3 + 6 = 10,872 checks, 0 failures (`receipts/full_suite_mutants/R-mask-overclears-bound-full.{redacted.log,rc}`).
  - `R-mask-overclears-acclat` (mask `~0x72000000`, also clearing MSRP_ACC_LAT_VALID) **survives** in the same way: GI 6,373 / 0, full suite rc 0, 10,872 / 0 (`receipts/reviewer_probes_2.log`, `receipts/full_suite_mutants/R-mask-overclears-acclat-full.{redacted.log,rc}`).
- **Impact:** the RTL at this head is right (the mask is exactly `0x52000000`; RTL lens clean). The release guard is the gap. A later edit that also clears BOUND makes every bound-but-probing input (PROBING_ACTIVE, PROBING_PASSIVE, which is the #790 state itself) read as unbound to a controller. Such an edit would pass the processor-top suite, the GSI mutant driver and `make check`. The parent `[GSI]` cases that would see a real integrator's BOUND land only with the pin adoption (milan-fpga #790), not at this head. The PR text "each response grades the processor's gate alone" and "checked byte-exact" is true only for the bits the harness claims.
- **Required outcome:** in section GI's settled-gate mode, the harness integrator also claims the other integrator-owned flags in every STREAM_INPUT flags word. At least BOUND, MSRP_ACC_LAT_VALID and MSRP_FAILURE_VALID; preferably every bit outside `0x52000000` that the processor does not own. `gate_expected` keeps them in both settled and unsettled bodies, so a mask that clears anything but `0x52000000` fails a named check. Add a matching arm to `settled_gate_mutations()` (for example, the mask widened by BOUND) with its required failing check.
- **Verification:** `TMPDIR=<scratch> python3 scripts/reviewer_probes.py <clone> <base top> <out> <verilator> 4 R-mask-overclears-bound R-mask-overclears-acclat` must report both variants with `run_rc` 1 and named `GI GATE` failures. `python3 tb/pp_top/gsi_mutants.py --only <the new arm> ...` must kill the new arm by its named check, with golden and restored PASS. The full `make -C tb/pp_top run` must still pass.

### R724-1-S1 - SUGGESTION - Tests

- **Where:** `hdl/top/protocol_processor_top.sv:3585` keeps selector 4's failure-code byte `[15:8]` while unsettled; no test step has a non-zero failure code while pbsta is not PROBING_COMPLETED.
- **Evidence:** `R-sel4-fail-code-dropped` (selector 4 zeroed whole while unsettled) survives section GI (6,373 / 0) and the full suite (rc 0, 10,872 / 0; `receipts/full_suite_mutants/R-sel4-fail-code-dropped-full.{redacted.log,rc}`).
- **Impact / outcome:** Table 5.9 ties msrp_failure_code to MSRP_FAILURE_VALID (registering a Failed Talker), not to settled. This round did not establish whether the listener can register a Failed Talker attribute while probing (for example, in the REPROBE state with the old stream still published). If it can, add a step there that keeps the failure code. This does not affect the verdict.

### R724-1-W1 - RESIDUE - Docs (wording only)

- **Where:** `tb/pp_top/README.md:511-512`: "Premise checks read the binding view at each step."
- **Fact:** `gate_view` runs at RESET, PROBING, SETTLED, REPROBE, PASSIVE-STALE and UNBOUND, not at PROBING-SENT, REPROBE-SENT or SETTLED-AGAIN (`tb/pp_top/gsi_internal.hpp:694-741`).
- **Exact fix:** "Premise checks read the binding view at RESET, PROBING, SETTLED, REPROBE, PASSIVE-STALE and UNBOUND."

## Lens results

### Conformance - CLEAN

- Milan v1.2 5.4.2.10.1 / Table 5.9 and IEEE 1722.1-2021 7.4.16.2. `gsi_settled_w` (`protocol_processor_top.sv:3563`) is "in-range index and `gsi_status_w[7:5] == PB_COMPLETED_C`". `gsi_status_w` is the same `lstn_gsi_status_r[sink]` byte that selector 7 returns as pbsta/acmpsta (`:3575`), so the flags and the probing_status field share one status source, as check (1) requires. While unsettled, selector 0 clears `0x52000000` (STREAM_ID_VALID `0x40000000`, STREAM_DEST_MAC_VALID `0x10000000`, STREAM_VLAN_ID_VALID `0x02000000`), selector 2 answers 0, and selector 4 `[63:16]` (stream_dest_mac) answers 0. The stream_vlan_id was already gated by selector 6 and now reads the same wire. PROBING_COMPLETED = 3 (Milan 5.3.8.5 / Table 5.5) matches `gate_expected`'s `pb == 3`.
- Executed: on the head, section GI's GATE steps all pass (`receipts/gsi_mutants/golden-run.log`; full suite below). The head's tests over the base RTL fail 82 lines, 32 of them `GI GATE` (`receipts/reviewer_probes/base-rtl-run.log`), identical line-for-line to the first arm's 82 (compared by this round).
- Out-of-range inputs: `gsi_status_w` is 0, so the gate clears them too. This is documented in `06_aecp_engine.md` §6.2 and consistent with Table 5.9, because such an input is never settled.

### RTL - CLEAN

- The change is confined to the `gsi_answer` comb block and one new wire (`:3532`, `:3554-3588`). There are no new state elements and no change to `gsi_req_o` / `gsi_wait_i`, so selectors 0, 2 and 4 still request and wait. The STREAM_OUTPUT path is untouched (the gate sits inside `if (gsi_input_w)`). Selector 4's failure-code byte is preserved.
- Check (6): no port, parameter or register-map change. The port list ends at `:826`, and every changed line is at `:3529` or later. No `input`/`output`/`parameter`/`localparam` line is added or removed anywhere in the diff (`receipts/diff-097a7987-e9272b56.patch`). No register-map file is touched.
- Comment rule: the added source comments cite issue #206, milan-fpga #790 and Milan / IEEE clauses only. A scan of every added line for bench lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs found none; `A8`/`A15` and `F05.3` are pre-existing state-machine action and figure labels. No RESIDUE.
- Area is the author's measurement only (KL_pp_shadow +664 LUT / +12 FF); this round did not re-run synthesis.

### Robustness - UNCLEAN (R724-1-F1)

- Reviewer mutants, each built in its own temporary copy, all on the pinned simulator (identity checked: wrapper `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, `--version` = `Verilator 5.050 2026-07-01 rev v5.050`):

| Variant | Edit | Result |
|---|---|---|
| R-mask-sid-only | mask `~0x40000000` | killed, 22 `GI GATE` fails |
| R-mask-wrong-lane | mask in `[63:32]` | killed, 22 `GI GATE` fails |
| R-status-wrong-field | settled from acmpsta bits | killed, 834 fails, 20 `GI GATE` |
| R-settled-ge-passive | settled = pbsta >= 1 | killed, 10 `GI GATE PASSIVE-STALE` fails |
| R-gate-hits-format | also zero selector 1 | killed, 61 GI fails |
| R-mask-overclears-format | mask `~0xD2000000` | killed, 61 GI fails |
| R-gate-leaks-to-output | zero STREAM_OUTPUT selector 2 | survives GI-only (expected); killed by the full suite: `G2: STREAM_OUTPUT[1] Milan response byte-exact`, 1 failure (`receipts/R-gate-leaks-to-output-full.{diff,redacted.log,rc}`) |
| R-mask-overclears-bound | mask `~0x56000000` | **survives** GI and the full suite (F1) |
| R-mask-overclears-acclat | mask `~0x72000000` | **survives** GI and the full suite (F1) |
| R-sel4-fail-code-dropped | selector 4 zeroed whole | survives GI and the full suite (S1) |

- Check (2) for STREAM_OUTPUT is therefore guarded: R-gate-leaks-to-output is killed. For settled inputs it is guarded too: settled-gate-closed is killed. For the other integrator flags of an unsettled input it is not (F1).

### Tests - UNCLEAN (R724-1-F1)

- Check (3), the four cases: PROBING / PROBING-SENT (probing before the first answer), PASSIVE-STALE (T-ACMP-NOTK to PROBING_PASSIVE with the stale identity still published, premise-checked), SETTLED / SETTLED-AGAIN, and RESET / UNBOUND are present (`gsi_internal.hpp:694-741`), each graded by name and byte-exact. REPROBE adds the timeout-with-talker case. All fail on the base RTL (above).
- Check (3), the mutant: the six settled-gate arms ran on the head driver, `--jobs 4`, rc 0 (`receipts/settled_arms.log`, `receipts/settled_arms/`). Each arm was killed by its named check, including `settled-gate-removed` (the pass-through restored, `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero`), with golden and restored PASS. The author's full 29-arm campaign at this head (public evidence `author-r1/a691c/receipts/campaigns/gsi-e9272b5/results/results.json`) agrees. This round confirmed that `mutations()` at `e9272b5` returns the same 29 arms, in the same order, as at `9abb41f`, and that `mutations()` is 100 lines.
- Full processor-top suite at the exact head tree (`make -C tb/pp_top run`): rc 0, 10,872 checks, 0 failures (`receipts/pp_top_full_head.{redacted.log,rc}`). This equals the PR's 10,872.
- `make check` at the exact head (git clone of the head, tree `04820794`): rc 0 (`receipts/make_check_head.{log,rc}`). Two earlier attempts failed on this round's own environment (a PATH without the diagram linter, then an archive without git metadata). They are not head defects and are not cited as results.
- Open: F1 (other-flag preservation ungraded); S1 (suggestion).

### Docs - CLEAN

- Check (4): the GET_STREAM_INFO rows are updated consistently with the RTL: `06_aecp_engine.md` §6.2 (new paragraph), F06.12 flags text (`:460`), F06.13 owner rows and the coherence paragraph, `02_interfaces.md` §4.4 row, `docs/guides/integrator.md` §8, and `00_MILAN_COMPLIANCE_REVIEW.md` REQ-AEM-010. Each states the mask, the zeroed fields, that the rule uses the same pbsta, and that there is no port change. `tb/pp_top/README.md` documents the steps and the six arms, matching `gsi_mutants.py`. `make check` (links, matrices, IDs, figures, staleness) passes.
- One wording RESIDUE (W1); it does not leave the lens unclean.

## Parent consumer gate (check 5)

- Reviewer-run in a scratch worktree of milan-fpga dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`. The #202 source-stream-ID wiring patch was taken from public evidence `origin/pp202-review-evidence:review-evidence/pp202-r1/author-r6/parent-src-stream-id-wiring.patch` (sha256 `ff5068d295872d1f872b89890ff76f9bb1d3fd0738ad650282dbe45d9e171275`, equal to the assignment's) and applied. The `protocol-processor` gitlink was staged at the head, and gptp-processor was populated at its pin `55680bff`. `git submodule status` showed both at their pins (`receipts/parent_idiom/<rev>/STATE.txt`).

| Gitlink | check_py_idiom.py | --selftest | check_cpp_idiom.py | --selftest |
|---|---|---|---|---|
| `e9272b56` (head) | rc 0, `long function: 9 <= 9` | rc 0 | rc 0 | rc 0 |
| `9abb41f9` (first commit) | rc 1, `long function 10 > ratchet 9`; `--list` blames `protocol-processor/tb/pp_top/gsi_mutants.py` | rc 0 | rc 0 | rc 0 |
| `097a7987` (base) | rc 0, `9 <= 9` | rc 0 | rc 0 | rc 0 |

- This reproduces the author's idiom receipts and confirms that the second commit is what makes the Python idiom gate pass. The remaining parent gates (sweep shards, `milan_dp` `[GSI]` 461 checks with identical lines at base and head, the parent GSI mutants 11/11, OOC area, other static scanners) are the author's published receipts at `9abb41f`/`e9272b5`, read but not re-run (a full parent bank is outside this round's allowance).

## Hosted evidence (observed, not accepted here)

- Exact-head check runs, read at the time in `receipts/hosted_check_runs_e9272b56.json`. Two check suites: `docs-gates` success ×2, `portability` success ×2, `suites` success ×1, and one `suites` still `in_progress`. These are executed jobs; no skipped context is counted as a pass. The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `protocol_processor_top.sv:3529-3590`; issue #206 clauses; GI GATE expectations; base-RTL failure transcript | R724-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| RTL | CLEAN | full RTL diff, port list `:98-826`, comment-rule scan of every added line, `receipts/diff-097a7987-e9272b56.patch` | R724-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| Robustness | UNCLEAN (F1) | 10 reviewer mutants (GI and full suite), 6 author arms re-run | R724-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| Tests | UNCLEAN (F1) | `gsi_internal.hpp`, `sim_main.cpp` harness, `gsi_mutants.py`; full pp_top suite; `make check`; parent idiom gates | R724-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |
| Docs | CLEAN (W1 residue) | `06_aecp_engine.md`, `02_interfaces.md`, `integrator.md`, `00_MILAN_COMPLIANCE_REVIEW.md`, `tb/pp_top/README.md`, PR body | R724-1 | e9272b5635e76bf12a69376d59fd21d059cae320 |

## Real limits

- No manager source bank exists at this head, and none is claimed or inferred. This round's executions are focused: section GI, the full `tb/pp_top` suite, `make check`, the GSI mutant arms, reviewer mutants, and the parent idiom gates. The full processor sweep (`scripts/run_suites.sh`), `check-req-tags.py` over a sweep, lint, and every parent gate other than the two idiom scanners and their selftests are the author's receipts only.
- Physical calibration NOT RUN; no hardware, field or board evidence. Skipped contexts are not proof.
- Synthesis/area not re-run. The failure-code reachability question in S1 is open.
- The parent worktree used the published wiring patch with gptp-processor at its dev pin. The current-dev merge candidate (source base `097a7987`, live dev `97aab1d0`) is distinct and is the manager's to build.

## Pending manager duties

- Builder and native banks on the current-dev merge candidate at the merge turn, with their receipts linked on the PR.
- Hosted/act acceptance for the exact head, including the `suites` run that was still `in_progress` when this round read it.
- Carry W1 and the retained R723-1-RES-01 to the residue checklist.
- At the parent pin adoption (milan-fpga #790): the `[GSI]` cases and the parent `gsi_mutants.py` arm.

## Prior public review findings

No review finding was posted on PR #208 or issue #206 before this round started. The PR then held only the two "review started" notices. The parallel internal round R723-1 (POSITIVE, posted 2026-10-27T10:03:25Z) was read only after the verdict, findings and ledger above were written. Its findings are resolved or retained at this head as follows:

- **R723-1-RES-01 (RESIDUE, `docs/architecture/06_aecp_engine.md:397`, a 133-column line in the reflowed paragraph): RETAINED as RESIDUE.** This round confirmed the line is 133 columns and comes from this delta (`git blame`: `9abb41f`). One correction to its verification: line 401 (126 columns) is pre-existing (`1e0c83d`) and lies inside the quoted `awk` range. The check should read `awk 'NR>=394 && NR<=400 && length > 90'`.
- **R723-1-SUG-01 (SUGGESTION, STREAM_OUTPUT unchanged is pinned only by `G2: STREAM_OUTPUT[1] ... byte-exact`): RETAINED as SUGGESTION.** This round's R-gate-leaks-to-output matches it exactly: GI-only survives, and the full suite kills it by that one G2 check.
- **Divergence on check (2):** R723-1 records check (2) as holding, citing the full suite and the output probe. This round's R-mask-overclears-bound and R-mask-overclears-acclat show that the "every other flag unchanged" half is not guarded for an unsettled input's integrator-owned flags. That is R724-1-F1, which stays open as MINOR. R723-1's own decode of the #790 bench capture (`0xd6000006`: the three gated flags plus STREAM_FORMAT_VALID and BOUND) shows a real integrator sets BOUND in exactly the state the gate acts on.
- **Fact for the record:** R723-1 states that the #202 wiring patch is not public. It is published on milan-fpga branch `pp202-review-evidence` at `review-evidence/pp202-r1/author-r6/parent-src-stream-id-wiring.patch`, with sha256 `ff5068d2…1275`. This round's parent idiom gates ran with it applied (section "Parent consumer gate").

## Receipts

- Listed in `MANIFEST.sha256`. The portable scripts are `scripts/reviewer_probes.py` (section-GI reviewer mutants, built through the head's own `gsi_mutants.check_variant`), `scripts/full_suite_mutant.sh` (one edit, full `make -C tb/pp_top run`) and `scripts/parent_idiom.sh` (parent idiom gates at one gitlink).
- Full-suite transcripts embed a local toolchain path. They are published as `*.redacted.log` copies, with that path replaced by `<home-path>` and no other byte changed. The raw transcripts and the compile-only `*-build.log` files stay local. Each variant's `build_rc` is in its JSON line.
- `receipts/gsi_mutants.log` and `receipts/gsi_mutants/golden-run.log` come from a first full-driver launch at this head that the memory stop interrupted after its golden PASS. Only that golden result is cited. The settled-gate arms were re-run to completion in `receipts/settled_arms/`.
- `receipts/reviewer_probes.log` (base-rtl, R-mask-sid-only, R-mask-overclears-bound) is from the first probe launch at this head. `receipts/reviewer_probes_2.log` holds the rest. The clone was verified unchanged at the end (`receipts/clone_restore.txt`).

R724-1 FINISHED
