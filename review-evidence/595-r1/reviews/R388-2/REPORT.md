[R388] POSITIVE - exact head 11e4e1f2876c99e8f136d869c70674e077ddcf94

# R388-2: internal independent re-review of PR #614 / issue #595

- **Head under review:** `11e4e1f2876c99e8f136d869c70674e077ddcf94`, tree `b78b64a0b7fd34797c7e06ece302675f7045cf49`. Parent `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8` (the round-1 head); source base `1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a`.
- **Role:** internal reviewer, cleared context, own detached clone. Round R388-2. The delta is one commit (executor [A419]), `44d3ae3b..11e4e1f2`.
- **Authorities read, in order:**
  - AGENTS.md.
  - Issue #595 body (acceptance 1-5, not-in-scope).
  - Round-1 assignment 5867362523 and round-2 assignment 5868165203 (manager decisions).
  - [A419] TAKEN 5868179065 and REVIEW READY 5868526411.
  - PR #614 body, and the review-start comment 5868544790.
  - `scripts/pp_srcs.py` (`pp_sources`, `PROSE_OK`, `check`) and `.github/workflows/rtl-fast.yml:108-109`.
  - The public evidence tree `review-evidence/595-r1` at `a3c8a9a1` (round-1 author packet), and my own round-1 packet as read-only input.
- **Delta scope:** `git diff 44d3ae3b..11e4e1f2` touches three files: `sw/builder/test_declarations.py` (+9/-3), `docs/ENDSTATION_BUILDER.md` (1 line) and `sw/builder/README-parameters.md` (1 line).
  - The delta leaves these paths untouched: `endstation_builder.py`, `test_builder.py`, `scripts/`, `configs/`, `hdl/`, `avdecc/`, `sw/litex`, `sw/firmware`, `tb/`, `syn/`, `.github/` and every gitlink (`receipts/delta_scope.txt`).
  - The commit message is one line with no trailers.

## Verdict

POSITIVE. Round-1 finding F1 is resolved at this head.
- The declaration suite now finds `pp_adp_pkg` through the derived processor source list. It adds no `PROSE_OK` exception.
- `scripts/pp_srcs.py --check --selftest` returns 0 both locally and in the hosted `rtl-fast / verilator-lint` job on this exact head.
- My removed-derivation control makes the check fail again. My probes also show the new derivation follows a moved package and refuses a duplicate, untracked or missing package.
- The independent `ADP_ENTITY_CAPS_C` read is kept, and it still bites.
- The taken suggestion S2 is applied.
- Refusal behaviour and all five configurations' artifacts are byte-identical to round 1 and to the base.
- No MINOR, MAJOR or BLOCKER finding is open. Every lens was applied at this head and is clean.

## Findings

No new finding in this round.

### Prior public findings, resolved or retained at this head

| ID (round) | Severity | Lenses | Status at `11e4e1f2` | Evidence |
|---|---|---|---|---|
| R388-1 F1 | MAJOR | Tests, RTL | **Resolved** | See "Assignment point (1)" below. |
| R389-1 F1 (same defect) | MAJOR | Tests, RTL | **Resolved** | Same evidence: `pp_srcs` check at `11e4e1f2` gives 0 findings (`receipts/pp_srcs_base_r1_head.txt`), and hosted `verilator-lint` step 7 succeeded (`receipts/hosted_verilator_lint.txt`). |
| R388-1 S2 | SUGGESTION | Docs | **Resolved (taken)** | `docs/ENDSTATION_BUILDER.md:883` now reads "Hexadecimal declarations require YAML strings." `sw/builder/README-parameters.md:70` now reads "EUI-48 YAML string". |
| R388-1 S1 = R389-1 S1 | SUGGESTION | Robustness | **Retained, out of scope** | Lenient quoted-MAC shape (signs, whitespace, unpadded or short separated groups). This is pre-existing and unchanged at this head (`receipts/edge_probe_vs_round1.txt`). The manager recorded it for the #495 checklist (assignment 5868165203). Being a suggestion, it does not affect coverage. |

## Assignment points

### (1) F1: derived package source

**Code.** `sw/builder/test_declarations.py:15-16` imports `pp_sources` from `scripts/pp_srcs.py`.
- `:233-237` reads every derived source and keeps those that declare `package pp_adp_pkg;` (`^\s*package\s+pp_adp_pkg\s*;`, multiline). It asserts exactly one.
- `:238-240` keeps the round-1 independent regex read of `ADP_ENTITY_CAPS_C` and its single-match assert.
- `git grep` finds no literal submodule path in the file (`receipts/delta_scope.txt`).
- `scripts/pp_srcs.py` is unchanged against both the base and the round-1 head. `PROSE_OK["sw/builder/test_declarations.py"]` still lists only its three pre-existing literals, so no exception was added.

**Gates at the exact head.**
- `python3 scripts/pp_srcs.py --check --selftest` returns 0. It derives 45 sources and reports 7 permitted-prose files (`receipts/pp_srcs_check_head.txt`).
- `python3 sw/builder/test_declarations.py` returns 0 (`receipts/test_declarations_head.log`).
- The same check run over the git blobs of each commit gives 0 findings at base `1fa2357f`, 1 at `44d3ae3b` and 0 at `11e4e1f2` (`receipts/pp_srcs_base_r1_head.txt`).

**Controls.** Each ran on a disposable copy of the exact head under `scratch/` (`scripts/derivation_probes.sh`, `receipts/derivation_probes.txt`). Each arm restores the copy to clean.

| Arm | Change | Result |
|---|---|---|
| C0 | none | `pp_srcs --check --selftest` rc 0; suite rc 0; the shipped derivation lines, executed verbatim, give `caps=0x0000C588` from 45 sources. |
| C1 (removed-derivation control) | Round-1 literal read restored in place of the derivation | `pp_srcs --check` **rc 1**: `sw/builder/test_declarations.py: names submodule source(s) literally that are not permitted prose: protocol-processor/hdl/adp/pp_adp_pkg.sv`. The suite alone still passes (rc 0), so only the source-list gate detects the regression, which is the gate that now covers it. Restored: both rc 0. |
| C2 | Package `git mv`-ed inside the submodule to `common/pp_adp_pkg_moved.sv` | The derivation follows it (`caps=0x0000C588`); `pp_srcs --check` rc 0. The round-1 literal would have raised on the missing path. |
| C3 | Second tracked file declaring `package pp_adp_pkg;` | The derivation and the suite fail with `expected one pp_adp_pkg in derived processor sources`. |
| C4 | Package untracked (`git rm --cached`, file left on disk) | Fails with the same assert. The derivation is tracked-only, as `pp_sources` documents. |
| C5 | Package declaration renamed | Fails with the same assert. |
| C6 | `ADP_ENTITY_CAPS_C` removed from the package | Fails at the single-match assert. That assert is pre-existing and carries no message; not a finding. |
| C7 | The test's caps perturbed by one bit (`^ 1`) | Suite **rc 1**: the builder refuses `entity.entity_capabilities 0x0000C589 diverges from ADP_ENTITY_CAPS_C = 0x0000C588`. |

C7 shows the independent read still drives the capabilities round-trip, and that it is not the builder's own parser (`gen_aemi_image.adp_entity_capabilities_declaration`, `endstation_builder.py:3716`).

**Import context.** `test_builder.py` imports `test_declarations` in its `__main__` block, and `test_builder.py:315` already puts `scripts/` on `sys.path`.
- `scripts/` and `sw/builder`, `sw/litex` and `avdecc` share no module names, so the new `sys.path` entry shadows nothing.
- Running gate 40's entry point under the builder's import order returns rc 0, and `pp_srcs` resolves to `scripts/pp_srcs.py` (`scripts/builder_import_context.py`, `receipts/builder_import_context.txt`).
- `sw/litex/milan_soc.py:521-536` already calls `pp_sources()` at import, so the new dependency on a git-tracked, checked-out submodule adds no environment requirement the builder bank lacked.

### (2) Summary lines

Both summary lines now say "YAML string":
- `docs/ENDSTATION_BUILDER.md:883`: "Hexadecimal declarations require YAML strings."
- `sw/builder/README-parameters.md:70`: "EUI-48 YAML string".

The surrounding quote instructions (`:885`, `:889`, and README `:159-167`) remain accurate guidance, and they match the refusal text.

The pinned Markdown gates, run with the pinned environment (Python 3.14.7, PyYAML 6.0.3), all return rc 0 at head (`receipts/doc_gates_head.txt`):
- doc style and its self-test;
- em-dash with `--base 1fa2357f` (21 added lines) and with `--base 44d3ae3b` (2 added lines);
- TOC `--selftest`, `--check` and `--verify-anchors`;
- doc paths;
- `docs_check`, both with git and with `GIT_DIR=/dev/null`.

### (3) Refusal behaviour and artifacts unchanged

**Refusal behaviour.**
- The 39-case edge probe at head is byte-identical to my round-1 head receipt. At base it is byte-identical to my round-1 base receipt (`receipts/edge_probe_vs_round1.txt`).
- My 14 round-1 mutants, re-run on a head copy, are all killed, with the unmutated and restored controls at rc 0 (`receipts/mutants_head.txt`). They include the three assigned rule mutants: M1 the `int(str(v), 16)` reread, M5 integer acceptance, and M7 scalar `formats`.

**Artifacts.** The five tracked configurations were built from disposable base and head trees (`receipts/artifact_compare.txt`, `receipts/artifacts_vs_round1.txt`, `receipts/model_fragment_vs_round1.txt`):
- The 50 CLI artifacts have identical sha256 values, and `diff -r` finds no difference.
- The 20 paired descriptor-image and normalized-config hashes are identical at base and head.
- The 5 sweep fragments are identical at base and head.
- Every hash equals my round-1 receipts. Those were cross-checked in round 1 against the executor's public inventory (70 artifacts plus 5 config files, 0 mismatches).

**Config files.** The five config-file sha256 values are unchanged.

### Hosted `rtl-fast / verilator-lint` at this head

The job was executed, not skipped (`receipts/hosted_verilator_lint.txt`):
- job `108897257968`, run `36412921320`, `head_sha` `11e4e1f2876c99e8f136d869c70674e077ddcf94`;
- conclusion **success**;
- step 6 "Run the ratcheted whole-tree lint gate" succeeded;
- step 7 "Prove protocol-processor source lists are derived" succeeded. This is the step that failed at `44d3ae3b`.

Other contexts at the 11:06:34Z snapshot (`receipts/hosted_checks_snapshot.txt`) are listed under "Real limits".

### Other static gates at head

`python3 scripts/check_py_idiom.py`, `measure_naming.py --check` and `check_hygiene.py --check` all return rc 0 (`receipts/python_static_head.txt`).

## Lens results

```text
[R388] PASS Conformance - sw/builder/endstation_builder.py:1443-1446,3181-3200,3307-3309,3664-3704 (unchanged 44d3ae3b..11e4e1f2, receipts/delta_scope.txt); receipts/edge_probe_vs_round1.txt, artifact_compare.txt, model_fragment_vs_round1.txt - issue #595 acceptance 1-5 and both assignments: string rule, list rule, suite pins, five configs byte-identical (50+20+5 hashes) and equal to round 1, docs state the rule; round-2 items (1)-(3) met
[R388] PASS RTL - scripts/pp_srcs.py:54-79,87-113,130-193 and sw/builder/test_declarations.py:15-16,233-240 at 11e4e1f2; receipts/pp_srcs_check_head.txt, pp_srcs_base_r1_head.txt, derivation_probes.txt C1-C5, hosted_verilator_lint.txt (step 7 success on exact head) - derived-submodule-source contract restored with no PROSE_OK change; no HDL, generated SV or gitlink change (delta_scope.txt, clone_integrity.txt)
[R388] PASS Robustness - sw/builder/test_declarations.py:233-240 derivation under move/duplicate/untracked/renamed/missing-constant faults (receipts/derivation_probes.txt C2-C6); receipts/edge_probe_head.txt 39 malformed/boundary spellings unchanged from round 1 - each fault gives a named assertion, none passes silently; S1 retained as out-of-scope suggestion
[R388] PASS Tests - sw/builder/test_declarations.py at 11e4e1f2 (rc 0), receipts/mutants_head.txt 14/14 killed with controls rc 0, derivation_probes.txt C1 (removed-derivation control rc 1) and C7 (independent caps read bites), builder_import_context.txt rc 0, pp_srcs --check --selftest rc 0 - the repository regression is green again and the new code can fail for the defects it claims
[R388] PASS Docs - docs/ENDSTATION_BUILDER.md:883-891, sw/builder/README-parameters.md:70,159-167 at 11e4e1f2; receipts/doc_gates_head.txt (pinned gates rc 0) - S2 taken, summary lines match the loader (resolved YAML type, not quoting); PR body and REVIEW READY state the round-2 change and its controls
```

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #595 acceptance 1-5, assignments 5867362523 and 5868165203. `endstation_builder.py` (unchanged in the delta). Edge-probe, mutant and artifact/model/fragment identity receipts, `receipts/delta_scope.txt`. | R388-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| RTL | CLEAN | `scripts/pp_srcs.py` contract, `test_declarations.py:15-16, 233-240`, base/r1/head blob check, controls C1-C5, hosted `verilator-lint` step 7 on the exact head. No HDL, generated-SV or gitlink change. | R388-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| Robustness | CLEAN (S1 retained as suggestion) | Derivation fault arms C2-C6. 39-case edge probe identical to round 1. | R388-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| Tests | CLEAN | Suite rc 0, 14/14 mutants killed, C1 removed-derivation control, C7 caps bite, builder import context, `pp_srcs --check --selftest` rc 0. | R388-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| Docs | CLEAN | `docs/ENDSTATION_BUILDER.md:883-891`, `sw/builder/README-parameters.md:70, 159-167`, pinned Markdown gates rc 0, PR body and REVIEW READY. | R388-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |

## Real limits

- **Banks not run.** I did not run the full parent, protocol-processor, gPTP, Yosys or builder banks; the assignment forbids them. The full `test_builder.py` bank result at this head is the manager's evidence, not mine.
- **Verilator not used.** The delta contains no HDL and the lint result is read from the hosted job, so I did not use the scoped Verilator binary or verify its identity. There were no Docker, `act` or host `act_ci` runs.
- **Hosted contexts still running.** At the snapshot (2026-09-28T11:06:34Z), `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shards 0-4 were still in progress.
  - `docs-check` and `elaborate` run the builder bank that imports `test_declarations`.
  - Already succeeded: `verilator-lint`, `bdd-conformance`, `changes`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate` and Yosys shards 0-3.
  - "Physical gPTP (nightly and manual)" was skipped. Skipped contexts are not evidence.
- **Round-2 evidence not yet public.** At my fetch, `595-review-evidence` (tip `259d0709`) holds only the round-1 author packet (`a3c8a9a1`, head `44d3ae3b`) and the two round-1 reviews. The [A419] round-2 packet and the manager's exact-head bank receipts, cited in the assignment, were not yet public. This verdict rests on my own reproductions listed above, not on those claims.
- **PyYAML version.** PyYAML resolution was checked only against 6.0.3.
- **Hardware.** Physical calibration was not run. Field skips are not hardware proof.
- **Candidate merge not validated.** This is a source-base review. I have not validated the current-dev candidate merge (live dev `7a7582f0`, with a possible #577 / PR #612 builder collision).
- **Clone integrity after probes.** All probes ran on copies under `scratch/`. The clone still has HEAD `11e4e1f2…`, tree `b78b64a0…`, a clean status, and no worktree or index diff (`receipts/clone_integrity.txt`).
  - The six relevant blobs match `HEAD:` with their modes (`scripts/pp_srcs.py` 755, the rest 644).
  - Gitlinks: external `efeb541a` (not initialized in this clone, as before), gptp-processor `5dce647a`, protocol-processor `16be6768`, third_party/verilog-axis `48ff7a7e`. Each checked-out submodule is clean at its gitlink.

## Pending manager duties

- Publish the [A419] round-2 packet and the exact-head bank evidence.
- Hosted and `act` acceptance on the exact head, including the still-running `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shard contexts.
- The external review (R389-2).
- Validate the current-dev candidate merge, including any #577 / PR #612 integration.
- File S1 against the #495 checklist as decided.
- Explicit maintainer merge authorization, then post-merge containment.

R388-2 FINISHED
