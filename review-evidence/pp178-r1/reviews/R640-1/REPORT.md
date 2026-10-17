[R640] POSITIVE - exact head ebc3b6bcd6e2c789c1c80c9e285193628567ea33

# R640-1 independent review: PR #180 (Closes #178, Closes #179), SET_CONFIGURATION micro-program E_SCFG

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #180, branch `178-179-set-configuration`
- Exact head `ebc3b6bcd6e2c789c1c80c9e285193628567ea33`, tree `8e0a529be44ab7bef20f3418e682908c500f70a7`
- Source base `22c139a4323bc96c779d13e3f6774480c5fb9b75` (processor main); delta `22c139a4..ebc3b6bc`: 16 files, +302 / -23, three commits (6c9daad, c7ac345, ebc3b6b)
- Role: internal independent reviewer, cleared context, round 1. Public review start: PR #180 comment 6241652092.

## Verdict

POSITIVE. Both behaviours are implemented in E_SCFG only, as the frozen acceptance requires. Each one is reproduced as a defect on the base generator and graded at the exact head. Every new check (NP1a, NP1c, NP10, NP10b, SC1, SC2, SC3) has a planted mutant that fails it, and I re-ran all ten arms at the exact head. The ROM moved only through `gen_ucode.py`, and the ROM digest record moved only through its generator. The ROM word diff is confined to E_SCFG's words. There is one RESIDUE (a stale RTL comment that the delta made inaccurate) and two SUGGESTIONs. No MINOR, MAJOR or BLOCKER is open.

## Scope reconstructed

Neither AGENTS.md nor CONTRIBUTING.md exists in the processor repository. The conventions come from `docs/README.md`: ID registries, single-source rules, spec citation, Milan-wins/Δ convention, and `make check` as the documentation gate.

Frozen acceptance, from the issue #178 body, the issue #179 body and the owner's comments on both:

1. #178: a SET_CONFIGURATION to the current index answers SUCCESS with no unsolicited notification (Milan v1.2 5.4.5.2: notify only "if the command modifies the state", to all registered controllers except the requester). A real change still notifies once.
2. #179: an out-of-range `configuration_index` answers NO_SUCH_DESCRIPTOR carrying the current index (IEEE 1722.1-2021 7.4.7.1, 7.4.7.2, Table 7-141; Milan v1.2 5.4.2.5). STREAM_IS_RUNNING keeps precedence. The owner corrected "testbench item A3" to the SET_CONFIGURATION items W18d/W18d2. A3 is READ_DESCRIPTOR and stays unchanged.
3. Suite cases for each behaviour, each with a planted mutant. The microcode is regenerated only through `gen_ucode.py`, and the ROM digest records only through their generators.
4. The compliance review records both decisions with the clauses. The READ_DESCRIPTOR behaviour for a missing CONFIGURATION index is reported, not changed.
5. Processor gates at base and head, plus the parent consumer gates on a scratch parent.
6. STOP on any register-map, port or parameter change. The change stays confined to E_SCFG, because sibling lanes #176/#177 touch the same engine.

## Findings

### R640-1-F1: RESIDUE (lenses: Docs, RTL). Stale arm description in the engine's µPC constant comment

- Location: `hdl/aecp/KL_aecp_engine.sv:877-882` (an unchanged line in a file outside the delta, made inaccurate by the delta).
- Evidence: at this head, E_SCFG's range check branches to `E_SCFGNSD` (`hdl/aecp/ucode/gen_ucode.py:1986`). The ROM word diff (`pub/receipts/rom-word-diff.txt`) shows word 1459's target moving from 0x5e9 (1513, E_SCFGBAD) to 0x611 (1553, E_SCFGNSD). `UPC_SCFGBAD_C` (1513) is now entered only from dispatch on `cmd_r.cdl < 16` (`KL_aecp_engine.sv:3508`). The comment still calls E_SCFGBAD "SET_CONFIGURATION's out-of-range arm" and says the refusal is "like the other two arms" (there are now four refusal arms).
- Impact: wording only. The comment misnames the arm; no compiled text, ROM word, test, figure or claim depends on it. `scripts/check_upc_map.py` passes (61 constants, 90 entry points).
- Required outcome (exact fix): on line 877, replace `SET_CONFIGURATION's out-of-range arm.` with `SET_CONFIGURATION's truncated-command arm (cdl < 16, BAD_ARGUMENTS); an index with no CONFIGURATION answers NO_SUCH_DESCRIPTOR through E_SCFGNSD, which E_SCFG's range check reaches inside the ROM (issue #179).` On line 882, replace `like the other two arms.` with `like the other three arms.`
- Verification: `grep -n "out-of-range arm" hdl/aecp/KL_aecp_engine.sv` returns nothing, and `python3 scripts/check_upc_map.py` still passes.

### R640-1-S1: SUGGESTION (lens: Tests). Pin the documented lock-before-index order

- Location: the `docs/architecture/06_aecp_engine.md:500` chain ("lock → index < configurations_count, else NO_SUCH_DESCRIPTOR") and the PR body's order table (rows 3 and 4).
- Evidence: E_SCFG runs `CHECK_LOCK` before the range check (`gen_ucode.py:1974-1986`). The only lock refusal check, W19g (`tb/pp_top/sim_main.cpp:7996`), uses an in-range index. No check sends an out-of-range index to an entity locked by another controller. IEEE 7.4.7.2 does not order the two refusals, so either answer conforms. This is not an acceptance item.
- Suggested outcome: a check in the style of W17n, where a foreign controller sends SET_CONFIGURATION(count) to a locked entity and gets ENTITY_LOCKED carrying the current index, with a mutant that swaps the order.

### R640-1-S2: SUGGESTION (lenses: Docs, Conformance). Δ registration for the notification narrowing

- Location: `docs/00_MILAN_COMPLIANCE_REVIEW.md:596` (§8 item 12, "Milan wins (§5.5.2.1)") and `docs/architecture/06_aecp_engine.md:532` ("narrowed by it").
- Evidence: `docs/README.md` §4 asks for every Milan-over-IEEE point to be tagged Δn in F01.4. F01.4 (`docs/architecture/01_overview.md:132-150`) has no row for Milan 5.4.5.2. The repository's existing 5.4.5.2 requirement, REQ-NOT-002 (`00:467`), is likewise recorded as a Milan requirement without a Δ, so the PR follows established practice. The behaviour and clauses match the frozen acceptance.
- Suggested outcome: either add a Δ row for "unsolicited notification only when the command modifies the state" and cite it from 06 §6.4 and 00 §8 item 12, or cite REQ-NOT-002 in place of "Milan wins".

No prior-round public review findings exist on this PR, so none needed resolving or retaining. A concurrent reviewer's report for this same round was posted while this review was running. To keep this review independent, it was not read before this verdict and ledger were written.

## Evidence by lens

### Conformance

- #178: the SUCCESS path skips `NOTIFY_ENQ` when the narrowed index in force equals the commanded index (`gen_ucode.py:2007-2009`). NP1a (index from the image's ENTITY, store unset) and NP1c (index from the dynamic store) grade SUCCESS byte-exact with no push to either controller. NP1 and NP1b still grade exactly one unsolicited response at the other registered controller when the index changes. The existing controls `enq_dropped_configuration` and `requester_not_excluded` hold the change side and the requester exclusion.
- #179: an index >= `configurations_count` lands in E_SCFGNSD (`gen_ucode.py:2073-2076`). It answers NO_SUCH_DESCRIPTOR (status 2) at cdl 16 carrying the current index, through the same overlay `_scfg_cur` and body `E_SCFGEMT` as the other refusals (7.4.7.1, "the old value if it fails"; Table 7-141). The dispatch order is unchanged (`KL_aecp_engine.sv:3508-3510`): cdl < 16 gives BAD_ARGUMENTS, then any bound/streaming gives STREAM_IS_RUNNING (Milan 5.4.2.5), then E_SCFG. NP10 grades STREAM_IS_RUNNING ahead of a missing index; SC1 grades index = count and SC2 grades 0xFFFF; W18d and W18d2 are updated to NO_SUCH_DESCRIPTOR.
- Compliance record: 00 §8 items 12 and 13 carry the clauses given in the issues (IEEE 7.4.7, 7.4.7.1, 7.4.7.2, Table 7-141; Milan 5.4.5.2, 5.4.2.5) and the owner decision of 2026-10-17. `aecp_commands.json` gains NO_SUCH_DESCRIPTOR in SET_CONFIGURATION's status set. F06.14 was regenerated, and the `aecpcmd` gate holds it against the ROM.
- READ_DESCRIPTOR observation (BAD_ARGUMENTS for `configuration_index` >= `configurations_count` on ENTITY/CONFIGURATION reads, although IEEE 7.4.5.1 says the field is ignored on receipt for those types): out of scope. Issue #179 explicitly makes it report-only and the PR changes no READ_DESCRIPTOR word (ROM diff). The PR body and 00 §8 item 13 report it accurately. It is a candidate for its own issue.

### RTL

- No RTL file changed. The delta is ROM content plus the command table, so there is no register-map, port or parameter change; the STOP condition was not triggered.
- Root cause verified against the µCPU: `COMPARE` narrows only `ra` to the format (`KL_aecp_ucpu.sv:224`) and compares the low 32 bits of `rb` whole (`:228`, `:236`). The base word `COMPARE ra=12, rb=6` therefore compared the 16-bit index with the image lane's `{configurations_count, current_configuration}` and never matched. The fix `COMPARE ra=6, rb=12` narrows r6, and r12 is `{48'd0, desc_ix_r}` for SET_CONFIGURATION (`KL_aecp_engine.sv:1588`), so a 32-bit compare of r12 is exact.
- ROM confinement (`pub/receipts/rom-word-diff.txt`, generated with `gen_ucode.py` at base and head): only word 1459 (the range-check target), word 1475 (the compare operands) and words 1553..1565 (the new arm, which previously held the generator's deterministic fill) differ. No other program word moved. `place()` asserts against overlap (`gen_ucode.py:436-447`). The µPC map gate passes with 90 entry points.

### Robustness

- E_SCFGNSD is straight-line (13 words, no loop). It clears the status that CHECK_ARG set before the overlay, as the two sibling arms entered from a checking op do, so the overlay's miss guard behaves the same. Its deadline-kill behaviour matches those siblings.
- Boundaries graded at head: index = count (SC1, W18d2), 0xFFFF (SC2, W18d), bound entity (NP10), truncated (W3c, W20f), image versus stored index source (NP1a, NP1c). The refusals were checked for no store write, no NVM mark, no notification and no unsolicited frame (SC1/SC2 effects, NP10b), and GET_CONFIGURATION is unchanged afterwards (SC3).
- Independent probes (my own edits, `scripts/probe.py`), each isolating one path:
  - `never_notify` (NOTIFY_ENQ always skipped): only NP1 and NP1b fail, so a real change is still graded as notifying.
  - `store_arm_misread`: only NP1c fails.
  - `image_arm_misread`: only NP1a fails.
  - `base_generator_sections` (base `gen_ucode.py` in the head bench): NP1a fails (one push at the other controller), and SC1/SC2 fail with status 7. Both defects reproduce on the base.
  - `range_bad_default` (full default run): W18d, W18d2, SC1 and SC2 fail with status 7. Partial receipt: the 590 s window ended before the final tally.

### Tests

- Full `tb/pp_top` at exact head, all seven builds: `10492 checks: 10492 PASS, 0 FAIL`, rc 0 (`pub/raw/pp_top-full-head.log`). This matches the author's count (+22 over base: NP +6; SC +8 in each of the two builds that run AX).
- New arms re-run at exact head with the repository drivers:
  - Notify, `--only` the five new arms: the golden passes, `5 of 5 KILLED by their named checks`, rc 0.
  - Dispatch, `--only` the five new arms: the control passes, all five KILLED, rc 0.
  - Per-arm failure counts match the `tb/pp_top/README.md` rows exactly: compare_whole_lane 1, unchanged_notifies 2, running_route_dropped 1, success_reserved_dirty 4, refusal_notifies 1; range-bad-arguments 2, nsd-zero-body 2, nsd-stores 5, nsd-notifies 3, refusal-short-body 4.
  - Every new check has a killing mutant: SC1 (range-bad-arguments, nsd-notifies, refusal-short-body), SC2 (nsd-zero-body), SC3 (nsd-stores), NP1a/NP1c (compare_whole_lane, unchanged_notifies, success_reserved_dirty), NP10 (running_route_dropped), NP10b (refusal_notifies).
- ROM consumers at head:
  - `tb/aecp_cmds` run: `585760 trials swept; 176 checks: 176 PASS, 0 FAIL`, rc 0. This holds `decode.json`, whose only change is the generated ucode digest `a3b62cab...`, equal to my regeneration.
  - `tb/ucpu`: `437 checks: 437 PASS`, rc 0.
  - `gen_matrix.py --check`: rc 0.
- Author's published receipts (parent evidence repository, review-evidence/pp178-r1, commit 1c1b15df) agree with my runs. Their base-ROM NP receipt reports 77 checks where the exact head gives 76. That receipt predates commit ebc3b6b, which folded NP10's separate premise check into NP10. The failing line is identical, and I reproduced it at the exact head.

### Docs

- `make check` at exact head, in a scratch clone: rc 0. Links 1195, ids 583 files, and `aecp commands: 31 commands, 84 entries walked and observed, F06.14 41 rows, OK`. These match the author's figures.
- The 06 §6.4 chain, the four SET_CONFIGURATION notes, the §9 command summary row, the 09 §8.1 current_configuration row and the tb/pp_top README sections (SC, NP1a/NP1c/NP10, mutation rows with provenance) are consistent with the ROM and the checks.
- Comment rule: the added source comments cite issues #178/#179 and clauses only. No bench lane labels, lane names, review rounds, reviewer IDs or comment IDs were added ("lane" in `gen_ucode.py`'s new comment means a 64-bit data lane). The one stale comment is F1.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #178/#179 bodies and owner comments; `gen_ucode.py` E_SCFG/E_SCFGNSD/E_SCFGEMT; dispatch order `KL_aecp_engine.sv:3508-3510`; `aecp_commands.json`; 00 §8 items 12-13; F06.14; NP1a/NP1c/NP10/SC1-SC3/W18d results | R640-1 | ebc3b6bcd6e2c789c1c80c9e285193628567ea33 |
| RTL | CLEAN (RESIDUE F1 recorded) | µCPU compare semantics `KL_aecp_ucpu.sv:221-239`; r12 justification `KL_aecp_engine.sv:1588`; base/head regenerated ROMs and word diff; `place()` overlap assert; µPC map gate | R640-1 | ebc3b6bcd6e2c789c1c80c9e285193628567ea33 |
| Robustness | CLEAN | E_SCFGNSD status handling and overlay; boundary checks; 5 independent probes (never_notify, store_arm_misread, image_arm_misread, base_generator_sections, range_bad_default) | R640-1 | ebc3b6bcd6e2c789c1c80c9e285193628567ea33 |
| Tests | CLEAN | full tb/pp_top (10492/10492); 10 new mutant arms re-run (10/10 killed, counts match README); tb/aecp_cmds; tb/ucpu; gen_matrix; author receipts cross-checked | R640-1 | ebc3b6bcd6e2c789c1c80c9e285193628567ea33 |
| Docs | CLEAN (RESIDUE F1 recorded) | `make check` (rc 0); 00 §8; 06 §6.4/§9/F06.14; 09 §8.1; tb/pp_top/README.md; PR body; comment-rule scan of added source lines | R640-1 | ebc3b6bcd6e2c789c1c80c9e285193628567ea33 |

## Real limits

- No specification PDFs were available to this review. Clause wording was checked against the owner's quotations in the frozen issue bodies, not against the documents.
- Not run here, by rule: `scripts/run_suites.sh` (the full processor bank), lint/Yosys/elaboration-guard banks, and any parent gate. Every other campaign was taken from the author's published receipts at base and head and not re-executed: all notify/dispatch arms outside the ten new ones, and the aecp, ctr, gsi, name-write, maap, adp, name_state, acmp and d3 campaigns.
- `range_bad_default` was cut by the 590 s window before its final tally. Its failing lines are recorded, but it is a partial receipt. One base-generator run was discarded because two simulator instances shared its tree and log. The clean replacement is `base_generator_sections`.
- At the exact head, the hosted contexts show docs-gates and portability completed successfully (two runs each) and suites still in progress (two runs). I made no hosted acceptance claim. Physical calibration was NOT RUN, and no field or hardware proof is implied.
- The author's scratch-parent evidence is at parent `7d79ffb2`, not live dev `e9cbb676`. Two parent gates fail identically at base and head for reasons outside this delta. `check_submodule_docs` fails on the moved pin record. `measure_test_evidence` fails on three unexplained DUT-source readers already on processor main (`tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py`, `tb/elab_guards/mutants.py`), none of which PR #180 touches. The author's published patch adds those dispositions.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base 22c139a4, live dev e9cbb676) on the builder and native banks, and publish the receipts. No manager source bank ran at this head, and none is claimed.
- At the parent pin move: add the three test-evidence dispositions and update the submodule pin record and diagram, so that `measure_test_evidence` and `check_submodule_docs` pass. Record the new ucode digest `a3b62cabe2cb091383f999bf58b830ff2d3ab63cd8699b95d2529dbf4d02bcb3` in the parent ROM ledger through its generator.
- Merge ordering with sibling PR #182 (#177): it also adds 00 §8 item 12 and changes `tb/aecp_cmds/decode.json`, `tb/pp_top/sim_main.cpp`, `aecp_dispatch_mutants.py` and the tb/pp_top README. Whichever merges second must renumber its §8 item, along with the "review §8 item 12/13" references in 06 §6.4. It must also re-record `decode.json` through `make -C tb/aecp_cmds record`.
- Carry R640-1-F1 (RESIDUE) to the residue checklist with its exact fix.
- Hosted/act acceptance, including the in-progress `suites` contexts at the exact head.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`, with paths relative to the packet root. Host paths in logs are redacted to `$PACKET`, `$CLONE`, `$VALIDATION_TOOLS` and `<container layer>`. The simulator identity is Verilator 5.050 rev v5.050, wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`. After the probes, the review clone was verified byte-identical to the exact head (`pub/receipts/clone-integrity.txt`): HEAD, tree and index tree are `8e0a529b...`, the worktree is clean with no untracked or ignored files, there are no blob mismatches, and the repository has no gitlinks.

R640-1 FINISHED
