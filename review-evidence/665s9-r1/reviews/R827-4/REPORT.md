[R827] POSITIVE - exact head 2155eb9666693c0404aadb34ac4dad10a2466e24

Internal independent review, round R827-4, of PR #889 (issue #870, S9 of #665). Exact head `2155eb9666693c0404aadb34ac4dad10a2466e24`, tree `ea03711b42313e28662ea623301a0c5b2c435b37`. This is a delta review of `a69fc0f5..2155eb96`. Prior head `a69fc0f5` was reviewed POSITIVE by R827-2 and NEGATIVE by R827-3 on composition finding F1.

The verdict is POSITIVE. The delta answers F1: gate 23o now holds the split recipe's `nvm_split.json` byte for byte against the all-fabric build's, and on the composed candidate a split recipe that changes that file fails the gate. This round adds no MINOR, MAJOR or BLOCKER and no RESIDUE. It adds one SUGGESTION (N1).

## 1. The delta and the composition

- **The diff** (`delta.diff`) is one line: `sw/builder/test_builder.py:23852-23853`. `RECIPE_SHAPE_ARTIFACTS` gains `"nvm_split"`. It is the only change in `a69fc0f5..2155eb96`. The tuple is referenced at three places, all inside gate 23o (`:23852`, `:23878`, `:23922`). No other gate, script or document reads it.
- **The composed candidate** (`receipts/composition_identity.txt`) is dev-soft-core `8b1bdfaf` merged with `2155eb96` in a disposable clone. The merge is clean. Its tree `d5cf412b` differs from R827-3's candidate tree `63b2a160` (`8b1bdfaf` + `a69fc0f5`, reproduced here by `git merge-tree`) in this one line only. Everything else R827-3 measured at its candidate is therefore unchanged, byte for byte. The submodule gitlinks are the same in head and candidate. The PR's base is `dev-soft-core`.
- **On S9's own tree** (`receipts/gate23o_head.log`), `build()` writes no `nvm_split` path in either placement, so the new label is absent on both sides. The gate's presence check treats that as equal, and gate 23o passes.
- **On the composed tree** (`receipts/gate23o_composed.log`, `receipts/probe_counterfactual_composed.log` arm A), all 9 labels are written in both placements for all 5 configs, and gate 23o passes.

## 2. Prior finding F1 (R827-3), checked at its cause

F1 (MINOR, Tests and Docs) said gate 23o does not hold `nvm_split.json` in the composed tree. Its verification was the probe's PLANT reading "caught", with gate 23o and `test_builder.py --require-rv32` staying green.

| Check | Where | Result |
|---|---|---|
| The R827-3 probe, unchanged (sha256 `93b09832…47bd0`, the same as R827-3's manifest), on the composed candidate | `receipts/probe_composed.log` | FACT: equal for 5/5 configs. PLANT: **gate 23o FAILED (caught)** for every config ("the recipe's nvm_split is not the all-fabric build's") |
| Counterfactual: the same plant with the prior head's 8-label tuple, in memory | `receipts/probe_counterfactual_composed.log` B | PASSED (not caught). The new label is what catches it |
| Presence plant: the split recipe alone writes no `nvm_split` path | same file, D | caught |
| Unplanted gate 23o, head tuple | same file, E; `gate23o_composed.log` | PASSED |
| Gate 23o at 2155eb96 (S9's tree) | `receipts/gate23o_head.log` | PASSED, rc 0 |
| `test_builder.py --require-rv32` | see below | Not rerun in full (builder bank). Covered by delta isolation plus the published receipt |

The probe's own FIX-CHECK arm appends the label a second time, so its line counts 10 labels. That is an artifact of the probe, which was written for the prior head. It does not affect the PLANT arm.

**`--require-rv32`.** The author's published receipt at the prior head, `author-r4/receipts/r4/gates/test-builder.log`, has sha256 `daff52bc…4c15`, which equals the evidence `MANIFEST.json` entry's `published_sha256`. It records `python3 sw/builder/test_builder.py --require-rv32`, `ALL GATES PASS EXCEPT 2 NOT RUN`, `rc=0` (`receipts/evidence_spotcheck.txt`). The delta changes nothing outside gate 23o, and gate 23o passes at the head and on the candidate. So the rest of that receipt carries to `2155eb96`.

No execution receipt exists for `2155eb96` itself, from the author or the manager. The full run at the merge candidate is a manager duty (section 6).

**Docs half of F1.** `docs/design/MAILBOX_SPLIT.md:1608-1610` cites gate 23o for "Its shape artifacts are the all-fabric build's byte for byte". That statement is now true at the candidate. The gate's header comment (`test_builder.py:23841-23849`) states the same contract.

**F1: Resolved.**

## 3. This round's findings

### N1 - SUGGESTION - Tests, Docs - `sw/builder/test_builder.py:23922` (gate 23o's summary line)

- **Evidence.** The summary prints `len(RECIPE_SHAPE_ARTIFACTS)`, the size of the tuple, not the number of artifacts actually compared. On S9's own tree it now reads "writes the all-fabric build's 9 shape artifacts byte for byte", but `build()` writes 8 of them there (`receipts/gate23o_head.log`: absent `['nvm_split']`). On the composed candidate, which is every tree the PR lands in, 9 is true (`gate23o_composed.log`). The both-absent presence rule (`:23880`) is the same rule the gate already applied to the other labels.
- **Impact.** None on any landed tree. A branch-only receipt overstates its count by one, and a future label that both placements stop writing would still be counted as compared. In the composed tree gate 39 separately requires the 1x1 build to write `nvm_split.json`.
- **Optional outcome.** Count the labels present on both sides in the summary, or name the absent ones.

### Comment rule and wording

The delta adds no source comment, prose or PR text. It has no new RESIDUE and no bench lane label, round or reviewer ID in source.

## 4. Prior public findings on this PR, at this head

| Finding | Severity, lenses | Status at 2155eb96 |
|---|---|---|
| R827-3 F1: gate 23o does not hold `nvm_split.json` | MINOR, Tests, Docs | **Resolved** (section 2) |
| R827-3 S1: area-plan ledger stage figures dated KLJ2 (`MARK_II_AREA_PLAN.md:1051-1060`) | SUGGESTION, Docs | Retained. The figures are unchanged at head |
| R827-3 S2: `ctrl_split_boot` map-stability refusal depends on the hash seed | SUGGESTION, Tests | Retained as a new-Issue suggestion. Not in the delta |
| R827-1 F1, R828-1 F1, R827-1/R828-1 F2 (U0), R827-1/R828-1 R1 | MINOR / RESIDUE | Resolved before this round. The delta does not touch them |
| R827-1 S1 | SUGGESTION | Taken |
| R827-1 S2: FSM default in `KL_mbx_rx.sv` | SUGGESTION, RTL, Robustness | Retained on #495 |
| R828-1 S1 / R828-2 S-C; R828-2 S-A / R827-2 N1; R828-2 S-B / R827-2 S-a; R828-2 S-D / R827-2 N4 | SUGGESTION | Retained. The delta does not touch them |
| R828-2 RES-1 / R827-2 N3: the PR body's expected final builder line (PR body line 99, "prints `ALL GATES PASS`"; the receipts print `ALL GATES PASS EXCEPT n NOT RUN`) | RESIDUE, Docs | Retained, still present. Fix: name each NOT RUN row |
| R828-2 RES-2: provenance claim covering 3 of 9 reports | RESIDUE, Docs | Retained, fix as published |
| R827-2 N2: gate 23p docstring omits the bound-bitstream control (`test_builder.py:23727`, unchanged) | RESIDUE, Docs | Retained. Exact fix: "gate 23p - the identity gate passes the two real images and a copy of the split one that binds its bitstream, and fails every planted one by its kind." |

## 5. Lens results and ledger

```text
[R827] PASS Conformance — delta.diff; receipts/probe_composed.log (FACT 5/5); receipts/gate23o_composed.log — #870 scope "the configs keep their shape; the recipe sets control.placement: split": the split SoC's NVM record space (read by milan_soc.py --ctrl-mailbox) is now held to the all-fabric build's, and it is equal at all 5 configs; no acceptance criterion's evidence changes (composed tree differs from R827-3's by this line only)
[R827] PASS RTL — delta.diff; receipts/composition_identity.txt — no hdl/ or generated RTL file in the delta; composed tree d5cf412b = R827-3's 63b2a160 except test_builder.py:23853, so R827-3's RTL coverage at a69fc0f5 (KL_mbx, KL_mbx_rx, native bank at its candidate) is unaffected
[R827] PASS Robustness — receipts/probe_counterfactual_composed.log (D, E); receipts/gate23o_head.log — a split recipe missing the nvm_split path is refused by the presence arm; with the artifact absent on both sides (S9 tree) the gate stays green, not crashing
[R827] PASS Tests — sw/builder/test_builder.py:23852-23853, :23878 at 2155eb96; receipts/probe_composed.log (PLANT caught); receipts/probe_counterfactual_composed.log (B not caught at the 8-label tuple, C caught); receipts/evidence_spotcheck.txt (--require-rv32 rc 0 at a69fc0f5, receipt hash matches the manifest) — the new label can fail for the defect it targets; N1 is a SUGGESTION
[R827] PASS Docs — docs/design/MAILBOX_SPLIT.md:1608-1610; sw/builder/test_builder.py:23841-23849 at 2155eb96 (and in the composed tree) — the page's and the gate header's "shape artifacts byte for byte" claim is now enforced for nvm_split.json; no doc enumerates the labels; no new comment or residue
```

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta; #870 scope; recipe FACT 5/5 on the composed tree; composition identity | R827-4 | `2155eb9666693c0404aadb34ac4dad10a2466e24`, composed with `8b1bdfaf` in tree `d5cf412b54aa3e0c87781495eb5c289ac6d76649` |
| RTL | CLEAN | delta (no RTL); composed-tree identity to R827-3's candidate apart from one test line | R827-4 (R827-3's RTL evidence at ancestor `a69fc0f5`, untouched since) | `2155eb9666693c0404aadb34ac4dad10a2466e24` |
| Robustness | CLEAN | presence plant D; both-absent run on S9's tree | R827-4 | `2155eb9666693c0404aadb34ac4dad10a2466e24` (+ `d5cf412b`) |
| Tests | CLEAN | gate 23o at head and on the composed tree; R827-3 probe; counterfactual B/C; published `--require-rv32` receipt at `a69fc0f5` | R827-4 | `2155eb9666693c0404aadb34ac4dad10a2466e24` (+ `d5cf412b`) |
| Docs | CLEAN | `MAILBOX_SPLIT.md:1608-1610`; gate 23o header and summary | R827-4 | `2155eb9666693c0404aadb34ac4dad10a2466e24` (+ `d5cf412b`) |

## 6. Real limits and pending manager duties

- **This round did not rerun `test_builder.py --require-rv32` in full**, at the head or at the candidate, because that is the builder bank. It ran gate 23o alone, at both trees, and two in-memory probes. Its conclusion that the rest of the receipt carries over rests on delta isolation: the tuple is read only by gate 23o, and the candidate tree is one line from R827-3's. **Manager duty:** run the builder and native banks on the current merge candidate and link the receipts.
- **No manager source bank ran at this exact head, and none is claimed.** No published execution receipt for `2155eb96` exists. The `--require-rv32` evidence is the author's receipt at `a69fc0f5`.
- **The composed candidate is a local disposable merge** (commit `95c4fc57`, made under a throwaway identity). Only its tree id `d5cf412b` is meaningful. Live dev `fa6c094b` has diverged from dev-soft-core `8b1bdfaf` (ahead 370, behind 247). The final candidate against the live base is the manager's to build and validate at the merge turn.
- **Hosted CI.** A snapshot at the head (`receipts/hosted_checkruns_snapshot.tsv`) shows 7 completed success, 1 skipped (Physical gPTP), and the rest queued or in progress. Hosted and act acceptance are the manager's.
- **No hardware evidence.** Physical calibration was not run, and skips are not hardware proof.
- **This clone is unmodified** (`receipts/restore_verify.txt`): HEAD `2155eb96`, tree `ea03711b`; 0 status lines; worktree and index match HEAD; index (mode, blob, path) equals the HEAD tree; submodule gitlinks as tracked.

R827-4 FINISHED
