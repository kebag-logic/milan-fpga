[A537] REVIEW READY

Commit: `3880c1eb6e2f927a07f98150d5b05a228f8f4efd` (round 2, local branch `661-pp-pin-ead80360`; not pushed by this lane, whose published head is still round 1's `42f65447`)
Branch: `661-pp-pin-ead80360`, three round-2 commits on round-1 head `42f654478c11bd8f2b070969d83140587190f276`, no rebase or amend: `e9b0334a`, `ba57a3bc` and the `--no-ff` merge `3880c1eb` of dev `fa450d301805881ad713b67521477bf042ddadfd` (#652 and #656; still the live dev tip). The merge commit's tree, `6bba0f2c`, equals `git merge-tree --write-tree` of its parents.

Changed:
- **R487-1 F1.** The adopted `available_index` rule is now stated, citing IEEE 1722.1-2021 Section 6.2.2.15: increment after each ENTITY_AVAILABLE, reset to 0 after an ENTITY_DEPARTING.
  - Places: `docs/design/SAVED_STATE_MATERIALIZATION.md:1036-1040`, `avdecc/gen_aemi_image.py:105-110` (comment) and `docs/reference/MILAN_COMPLIANCE_MATRIX.md:154`. The matrix's "divergence stays recorded" sentence is dropped.
  - A fifth stale statement of the same rule, found by R487-1's own verification grep, is also corrected: `sw/builder/test_builder.py:26237-26241` (comment).
  - `wt.adp.available-index-advances` (`tb/tools/avtp_wire_truth_checks.py`) exempts only an index of 0 on the ADPDU after an ENTITY_DEPARTING. Every other repeat still fails.
  - The new self-test `test_available_index_resets_after_departing` has four arms: a whole cycle passes; R487-1's probe DEP 0, AVAIL 0, 1 passes; DEP 5, AVAIL 0, 0 fails; AVAIL 4, DEP 5, AVAIL 5 fails.
  - Supporting changes: `build_adp_frame` takes a `message_type`, and the wire module names the two message types.
- **Dev merge.** Its only RTL is `KL_nvm_backend.sv`'s elaboration-time guard constant `N_NAME_MAX_C`.
  - Source lists are unchanged.
  - The resource gate's input digest, recomputed with its own `inputs()` at the merge head, differs from the record only through that file. With that file at its measured bytes, all three recorded `inputs_sha256` values reproduce exactly.
  - Builder outputs and packed images are byte-identical for all five configurations at `42f65447`, `ba57a3bc` and `3880c1eb` (55 files each).
  - No re-route was made.
- The processor change is still only the gitlink. No parent interface, firmware or SoC change beyond what dev brings.

Validation at `3880c1eb`, each command unpiped with its own log and rc:

| Command | Result | rc |
|---|---|---:|
| `make -C tb/verilator/milan_dp_gptp -j16 VERILATOR_JOBS=2` | physical 139 checks / 0 failures, simulation exit 0; `verify_abort.py` 6/0 + 20/0 + 14/0 = 40/0. The #656 exception is retired | 0 |
| Every shell step of `.github/workflows/docs.yml` | 49/49, each under GNU Make 4.3, including the whole builder bank (the same two NOT RUN arms as round 1; the merged NAME-capacity gate passes) | 0 |
| `(cd tb/tools && python3 avtp_wire_truth.py --self-test)` | 25 tests OK; three planted exemption defects each killed by the new test | 0 |
| `(cd tests && behave --no-capture -f plain)` | 404 scenarios / 1,968 steps | 0 |
| `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=2`; `make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=2` | fresh builds; verdict and count lines identical to round 1 | 0 / 0 |
| `make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=2 tdm8render-mutants` | #657 exception: 28 PASS / 4 FAIL over 32 controls, identical to round 1's base and head lists | 2 |
| `pp_srcs.py --check --selftest`; `check_rtl_source_lists.py` and `--selftest`; `pp_resource_gate.py check-baseline` and `check` of the three recorded endpoints; `audit_pp_descriptors.py` | pass | 0 |

The other round-1 evidence at `42f65447` is not re-run, as the round-2 assignment directs: the parent sweep, the processor and gPTP suites, Yosys, `pp_shadow`, `nvm_cosim`, LiteX, vendor syntax, the Vivado endpoints and capture.

Acceptance criteria: round-2 items 1 to 3 are met with the evidence above. The round-1 criteria stand. The PR body (PR-BODY.md, rewritten from the live body) carries `Closes #661`, `Closes #639`, `Closes #234`, `Relates to #629` and `Relates to #229`, with no host paths or account names.

Open risks/questions:
- R486-1 R2/R3/S1 and R487-1 S1/S2 are not acted on; they are the manager's residue list.
- `docs/reference/FR_NFR.md:173` (FR-DISC-01, "incrementing `available_index` on every state change") is a requirement row this lane may not reword. It is reported for a decision.
- The published branch needs the manager's push of `3880c1eb`.

Evidence packet: `2026-09-23/661-a537/HANDOFF.md` (Round 2 section), `PR-BODY.md`, `gate-results-r2.json`, `docs-results-r2.json`, `docs-steps-r2.tsv`, `resource-inputs-r2.json`, `builder-compare-r2.json` and `render-compare-r2.json`. Raw logs remain in the lane's validation storage and are represented by size and SHA-256.

This is author evidence, not a review verdict. No push, PR operation, merge, hardware access or bench operation was performed. Reviewers: internal [R486], external [R487].
