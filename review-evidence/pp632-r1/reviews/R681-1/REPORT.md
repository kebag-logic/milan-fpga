[R681] POSITIVE - exact head 51f88c7e14e7e2527c09ff9a23b93dd6b857fd50

# R681-1: internal cleared-context review of processor PR #199 (Relates to kebag-logic/milan-fpga#632)

- **Head:** `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50`, tree `438b7967df80fabeef960173e28bc1334de30cec`.
- **Base:** processor main `08023123ae2df5d802d20a9bb22cd063942845cd`, which is an ancestor of the head.
- **Commits reviewed:** three, each with a single parent:
  - `175a5a15033c399346d635677bbf16dd5f8926af`: the E_SINFO change, section NS and the two planted defects;
  - `0b0974604f770412abea610c3ac819858c7dc708`: the `decode.json` re-record;
  - `51f88c7e`: the D3S5 setup fix.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open.
  - One wording-only RESIDUE (R681-1-R1): a mis-abbreviated commit ID in the PR body.
  - Three optional SUGGESTIONs.
- **What this approves:** the processor source head only. It does not cover the current-dev merge candidate, the milan-fpga pin adoption, or the rest of issue #632.

## Reconstruction (public state only)

1. **Workflow.** This repository has no tracked AGENTS.md or CONTRIBUTING.md. I read the consuming repository's AGENTS.md and CONTRIBUTING.md (milan-fpga default branch `dev`), then this repository's `README.md`, `docs/README.md` and `Makefile` (`make check`).
2. **Issue and rulings.**
   - Issue #632's body is the media-clock phase work. This PR answers a finding raised on that issue's PR #770.
   - The acceptance comes from two rulings on milan-fpga PR #770:
     - [issuecomment-6306591168](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306591168): the gate compares the commanded value with the stored row (Milan v1.2 5.4.2.9, 5.4.2.10.2, 5.4.5.2; IEEE 1722.1-2021 7.5.2). A processor-level test and a planted defect restoring the GSI(3) compare are required.
     - [issuecomment-6312625146](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6312625146): option (b). The stored row once `RGN_DYNV` is valid, otherwise the integrator's GSI(3) word. Five words. The factory-row residue is recorded, not a finding.
   - The finding answered: R677-2-F1 ([issuecomment-6306520485](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306520485)).
   - The owner comments on #632 from 2026-10-21, and the author's REVIEW READY ([issuecomment-6316365497](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6316365497)).
3. **Requirements and interfaces.**
   - `docs/architecture/06_aecp_engine.md` §6.3 (row :522) and the notification trigger classes (:1180-1186).
   - `docs/architecture/02_interfaces.md` §4.3 and §4.4: the `gsi_*` face and the `aecp_pt_offset_o` / `_v_o` levels.
   - `docs/architecture/09_verification.md` :184 and :318.
   - REQ-NOT-002, the tag NS carries.
   - The `KL_aecp_dyn_state.sv` read and valid semantics (:201-262, :297, :339-340).
4. **Diff and history.** I read `git diff 08023123..51f88c7e` in full: nine files, +200/-16.
   - `0b097460..51f88c7e` changes no file under `hdl/`.
   - `175a5a15..0b097460` changes only the digest line of `tb/aecp_cmds/decode.json`.
5. **Executable evidence.**
   - I read the A659 packet at [`bf251ad3` review-evidence/pp632-r1](https://github.com/kebag-logic/milan-fpga/tree/bf251ad3ccc0af6a14069e1cd8d391010f36de41/review-evidence/pp632-r1):
     - HANDOFF rounds 3 and 3b;
     - `receipts/round3/notify_sinfo/` and `notify_sinfo_pp_0b097464/`;
     - `processor_51f88c7e/` (suites, gates and campaign rc files);
     - `scripts/round3b/`.
   - I then re-executed the claims below myself.
6. **Prior review findings on PR #199.** I read them after my own pass over the diff. There are none: the PR has no reviews, no review comments, and no prior-round findings. R677-2-F1 is resolved below at processor scope.

## Acceptance checks, each independently executed at the exact head

| # | Check | Result | Receipt |
|---|---|---|---|
| 1 | E_SINFO built only through the generator; ROM differs from main at 1859..1873 only; the SET response still echoes; the notification body is unchanged | **Holds.** Both trees' own `gen_ucode.py` emit 2048 words and 92 programs: main `a7b1af66…`, head `1f78804e…`. The differing words are exactly 1859..1873. Head words 1864..1873 equal main's 1859..1868 except the skip target (0x74c becomes 0x751). The three asserts pass at generation. `E_SINFOUNS` (480) and every other word are unchanged. NS checks every SET's SUCCESS response byte-exact (`unchanged_offset_step`, `push_step`) and every push byte-exact, including NS2's body carrying 0 | `receipts/rom_words.txt`; `pp_top_suite.log` (NS 20 checks, 0 failures) |
| 2 | Section NS covers: identical SET pushes nothing (NS4); changed SET pushes once (NS3, NS5); SET 0 on a never-set row pushes once (NS2); first SET equal to the factory value pushes nothing (NS1). Both planted defects KILLED | **Holds.** The `pp_top` default build passes NS with 20 checks; all seven builds total 10,741 of 10,741. Campaign of the 22 `--notify-only` controls: golden PASS, 22 of 22 KILLED. `stream_info_compare_applied` fails exactly NS4 and NS5. `stream_info_unset_arm_dropped` fails exactly NS1 and NS2. All 22 fail exactly the checks recorded in `tb/pp_top/README.md`, including the four re-measured rows (4, 4, 15 and 15). Four further reviewer probes, all KILLED: unset arm skips the gather (NS1); set arm falls into the gather (NS4, NS5); skip target off by one (NS1, NS4); valid test inverted (NS1, NS2, NS4, NS5) | `notify_22.{log,rc}`, `notify_22_failing_checks.txt`, `notify_22_results.json`; `extra_probes.{log,rc}`, `extra_probes_results.json` |
| 3 | D3S5 keeps its measured quantity honest (latency measured on a set row), and the 12 related D3 controls still fail their recorded counts | **Holds.** `primed` sets output 0 before `write_latency()`. The latency is therefore measured on the set arm, which is the arm the timed SET (4,000,002 ns) takes. The premise stays graded. Reviewer probe `r_d3s5_unprimed` (the old setup) reproduces "accepted at 315227, the WRITE's done at 315228". Probe `r_d3s5_primed_other` (priming output 1) fails the premise by the same one cycle. So the premise check is what catches an arm mismatch. The 12 controls: golden PASS, 12 of 12 KILLED, each failing exactly its recorded count (3, 2, 1, 18, 14, 2, 5, 2, 2, 1, 2, 1). `clear_wins_same_edge` fails only "D3S5 same edge", so the premise holds under it | `d3_12.{log,rc}`, `d3_12_failing_checks.txt`; `d3s5_probes.{log,rc}`, `d3s5_probes_results.json` |
| 4 | The `decode.json` re-record matches the ROM | **Holds.** The record holds `1f78804e…`, which equals the head ROM. A fresh `make -C tb/aecp_cmds record` (617,916 trials, 176 checks) leaves the file byte-identical. With main's record in place, the gate refuses ("swept from another ucode.hex … a7b1af66b72c, this tree's is 1f78804e448c"). `make check`: rc 0, AECP gate selftest 231 of 231, 31 commands, 231 tags. `tb/aecp_cmds/mutants.py`: 17 of 17 | `decode_json_rerecord.log`; `chk_gates.log` |
| 5 | No port, parameter or register-map change, and no other command's notification behaviour changes | **Holds.** The diff touches no `.sv`, `.svh`, script, workflow or `syn/` file. In `hdl/`, only `gen_ucode.py` changes. The entry stays `UPC_SINFO_C` = 1856 (`check_upc_map` PASS). The only references to `E_SINFO + n` are inside E_SINFO itself. Main's words 1869..1873 were unplaced fill. `aecp_commands.json` lists the SINFO entry under SET_STREAM_INFO alone. NP, ST, RN, CS, DN and WD pass unchanged. The campaigns pass: deadline and hazard (6 controls including the `pp_top` response budget, 61 of 61 arms killed) and dispatch (4 controls, 69 of 69) | `aecp_mutants.{log,rc}`, `aecp_dispatch_mutants.{log,rc}`, `chk_gates.log` |
| 6 | The `milan_dp` notify-leg receipts reproduce | **Reproduced** in a scratch milan-fpga clone at PR #770's head `3fdaea3d`, which differs from the measured `32fb8fc2` by one design document. The processor submodule was at pin `2cbed0a9`, with the head's E_SINFO block spliced in by my own script. The splice reproduces every recorded digest: pin generator `b1dd0f22…`, spliced `8e6a219f…`, pin ROM `518b900c…`, spliced ROM `f9954a76…`. The spliced ROM differs from the pin's at 1859..1873 only, and its E_SINFO slot equals the head ROM's. Results: `make notify` gives 441 checks, 0 failures; pushes 0, 1, 0, 1; GET reads 2,000,000 / 2,020,834 / 2,020,834 / 2,041,667. `gsi_mutants.py 9`: clean PASS, caught at step 3 (3 of 441). The same executable with the pin's ROM fails steps 3 and 4 (3 of 441), so the case is sensitive at the pin. A reviewer probe on the never-set CRF output row passes (456 checks, 0 failures): first SET of the factory 2,000,000 ns pushes nothing; SET 0 pushes once carrying 0, and GET then reads 0; SET 0 again pushes nothing; SET 2,000,000 pushes once. The scratch submodule was restored to its pin, clean | `mdp_notify_head.*`, `mdp_gsi_mutant9.*`, `mdp_notify_pinrom.*`, `mdp_factory_first_probe.*`, `milan_dp_submodule_applied.diff`, `milan_dp_factory_first_probe.diff`, `rom_words.txt` |

Other gates at the head, from a clean clone: `./scripts/lint_hdl.sh` rc 0; `check_m9_opcodes` (selftest and gate) PASS; `gen_matrix.py --check` OK (94 rows, 0 untested). Focused suites: `aecp_cmds` 176, `ucpu` 447, `dyn_state` 118 and `aecp_notify` 131, all 0 failing.

## Findings

### RESIDUE (wording only, carried to the residue checklist)

**R681-1-R1 - Docs - PR #199 body: the second commit is cited by a short ID that does not resolve.**

- **Where:** the PR body cites `0b097464` in the Status table (row 2) and opens the description paragraph with "**`0b097464`.**".
- **Evidence:** the commit is `0b0974604f770412abea610c3ac819858c7dc708`. Its 8-character abbreviation is `0b097460`, and `git rev-parse 0b097464` fails.
- **Impact:** wording only. The commit subject next to the ID and the author receipt README (which gives the full SHA) both identify it unambiguously. No measurement, test, code, generated artifact or conformance claim changes.
- **Exact fix:** in both places, replace `0b097464` with `0b097460`.
- **Related, outside this PR:** the same mis-abbreviation names the frozen milan-fpga evidence directory `notify_sinfo_pp_0b097464/`, and appears in the REVIEW READY comment. The directory is frozen, so no change there is requested.

### SUGGESTIONS (optional, no lens impact)

- **S1 (Docs).** `docs/architecture/02_interfaces.md` §4.3 and §4.4 (`:64`, `:422`) list the `gsi_*` consumers but not SET_STREAM_INFO.
  - On a never-set Stream Output row, SET_STREAM_INFO's push decision reads kind 0 selector 3 as the offset in force. That gives the integrator's answer a notification consequence before the first SET, which is where the recorded residue lives.
  - The omission predates this PR: main gathered the word on every row.
  - Consider one clause there linking 06 :522.
- **S2 (Docs).** `docs/architecture/06_aecp_engine.md:1182` says the unsolicited SET_STREAM_INFO carries "the presentation-time offset in force".
  - `E_SINFOUNS` serves the stored row, which is the offset as set. Row :522 now uses the as-set / in-use / in-force vocabulary.
  - Writing "the offset as set (the stored SEL_PTOFF row)" at :1182 would stop a reader from taking it for GET's applied word.
  - The line is pre-existing and outside the delta.
- **S3 (Tests).** NS grades the set arm only through rows a controller set; the restore path is not exercised.
  - A row valid by a saved-state restore takes the same arm through the same write port (`KL_aecp_dyn_state.sv:339-340`; restore writes carry the valid flag, `:71-73`).
  - An NS step after a restore (an identical SET pushes nothing) would grade the comment's "or a restore" claim directly.

## Prior findings at this head

| Prior | Status at `51f88c7e` | Evidence |
|---|---|---|
| Public findings on PR #199 | None exist (no reviews, review comments or prior-round reports) | the PR's comment and review lists at review time |
| R677-2-F1 (milan-fpga PR #770), processor half: the gate compared the commanded offset with GSI(3), the applied word | **Resolved at processor scope.** The gate compares like for like: the stored row once set, the factory word before (option (b), as ruled). An identical SET pushes nothing; a SET that changes the stored offset pushes once. The SET echo and the push body are unchanged. 06 :522 documents the compare, the reason and the residue. The planted defect restoring the GSI(3) compare is killed at NS4/NS5 here, and at step 3 of the consumer leg | checks 1, 2 and 6 above |
| R677-2-F1, milan-fpga half: the four-step `[NOTIFY]` case, its control, the doc scoping | Outside this PR. The consumer leg and its control are reproduced in check 6. The #770 doc and scope items belong to #770's own review | `mdp_*` receipts |

## Per-lens results

| Lens | Result | Artifact-specific evidence at `51f88c7e` |
|---|---|---|
| Conformance | CLEAN | Traced Milan v1.2 5.4.2.9 (echo), 5.4.2.10.2 (GET reads the offset in use), 5.4.5.1/5.4.5.2 and IEEE 1722.1-2021 7.5.2 (push only on a state change, carrying the response) through E_SINFO words 1856..1873, `E_SINFOUNS` and NS1-NS5. Option (b) is exactly the ruled form. The residue is recorded as ruled (06 :522, README NS, PR body). Consumer leg: 0, 1, 0, 1 pushes on the real datapath. Reviewer probe: a first SET equal to the factory value on a never-set row pushes nothing; SET 0 pushes once |
| RTL | CLEAN | ROM regenerated from both generators: 15 words differ, all inside the 32-word E_SINFO slot. Branch targets 0x748, 0x749 and 0x751 are checked by asserts. The valid read follows `KL_aecp_dyn_state.sv` semantics: an out-of-range index reads valid 0 and takes the pre-existing GSI(3) arm. Entry address and UPC map unchanged; no `.sv` file changed; lint rc 0 |
| Robustness | CLEAN | Never-set versus set rows on both outputs. SET of 0 on a never-set row (NS2), and SET 0 then a repeat at the consumer. Write-back of the applied value (NS5). Repeated identical SET (NS4). Out-of-range index falls to the pre-existing arm. Lock, locate-miss and STREAMING refusals precede the new words. The response budget holds: the `pp_top` budget control PASS, DL 64 checks. The face hold on the unset arm is unchanged from main; the set arm no longer depends on the face |
| Tests | CLEAN | NS: 20 checks, every SET and push byte-exact. Both ruled controls are killed at exactly their named checks, and four reviewer probes are killed. The D3S5 premise kills an unprimed or wrongly primed setup. All 22 notify and 12 D3 controls fail exactly their recorded counts; `aecp_cmds` 17 of 17; deadline/hazard 61 of 61; dispatch 69 of 69 |
| Docs | CLEAN (RESIDUE R1 only) | 06 :522 (compare, reason, residue); 09 :184 and :318; `tb/pp_top/README.md` D3S5 (:69-73), run list (:2484), section NS (:2661-2698) and mutation record (:2997-3003, :3029-3036), all matching measured results. Every PR-body file:line reference checked. Comment rule: the added lines carry no lane label, lane name, review round, reviewer ID or issue-comment ID (only issue and requirement IDs). `make check` rc 0 |

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | E_SINFO and `E_SINFOUNS` against Milan 5.4.2.9, 5.4.2.10.2, 5.4.5.1/.2 and IEEE 7.5.2; NS1-NS5; the consumer leg and reviewer probe | R681-1 | `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` |
| RTL | CLEAN | `gen_ucode.py:2434-2466`; ROM words 1856..1887 at main and head; `KL_aecp_dyn_state.sv` read and valid path; UPC map; lint | R681-1 | `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` |
| Robustness | CLEAN | Both arms on both outputs, 0 and write-back values, the out-of-range index, refusal ordering, the response budget | R681-1 | `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` |
| Tests | CLEAN | `tb/pp_top` (7 builds, 10,741); notify 22/22; D3 12/12; `aecp_cmds` 17/17; deadline/hazard 61/61; dispatch 69/69; six reviewer probes (4 NS, 2 D3S5); consumer leg, control 9 and a reviewer probe | R681-1 | `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` |
| Docs | CLEAN | 06, 09, `tb/pp_top/README.md`, the `notify_mutants.py` docstring, the PR body; `make check` (RESIDUE R1 carried) | R681-1 | `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` |

## Real limits of this round

- **No manager source bank** runs at this head, and none is claimed or inferred.
  - Not run by me: the full processor suite sweep (`run_suites.sh`), the SRP, MAAP and ADP campaigns, Yosys and elaboration guards, and the other 98 D3 controls.
  - For those, source-head execution evidence is the author's published receipts at `51f88c7e` (`processor_51f88c7e/`: suites rc 0, 1,030,329 checks; executed req-tags 231 lines, 14 suites; campaign rc files 0). I read them and did not re-run them.
- **My runs used the pinned simulator 5.050** (identity in `receipts/simulator_identity.txt`).
  - Up to four campaigns ran at once, each pinned to its own CPU set, within 16 jobs and the 12 GB cap.
  - Wall times are indicative only.
- **The consumer measurements are uncommitted.** They ran at milan-fpga `3fdaea3d` with the head's E_SINFO spliced, uncommitted, into submodule pin `2cbed0a9`, 1x1 shape only. The adopted pin (the fourth pin adoption) does not exist yet.
- **Hosted checks at the head, snapshot 2026-10-21T13:19Z.** `docs-gates` and `portability` succeeded (two runs each); `suites` was still in progress. No hosted acceptance is claimed (`receipts/hosted_checks_snapshot.tsv`).
- **Not checked:** composition with live dev `d77a8afd`. The current-dev merge candidate was not built here.
- **Physical calibration and bench proof: NOT RUN.** Simulation is not hardware proof.
- **Process note.** While listing PR #199's comments to find prior findings, before writing this verdict, I saw the opening paragraphs of the external reviewer's report, posted at 13:18Z. I read no further.
  - Every result here comes from my own executions and reading.
  - That report raised no finding I adopted or answered.
  - My RESIDUE and SUGGESTIONs came from my own pass over the diff.
- **Clone hygiene.** Two ignored `__pycache__` files that I created by importing the campaign drivers were removed. The review clone is then at exact head bytes: index blob IDs and modes equal the HEAD tree (680 entries), no untracked or ignored entries, and every worktree file hashes to its index blob. The head has no gitlinks (`receipts/clone_restore_check.txt`).

## Pending manager duties

- Carry R681-1-R1 to the residue checklist.
- Build and validate the current-dev merge candidate at the merge turn (source base `08023123`, live dev `d77a8afd`), and link its builder and native-bank receipts.
- Own hosted and act acceptance at the exact head; `suites` was still in progress at my snapshot.
- Sequence the fourth milan-fpga pin adoption carrying this head before PR #770 merges. Re-run the `[NOTIFY]` leg there with the committed pin, not a splice.
- The follow-up on #632, recorded by ruling and out of scope here: an applied offset that changes without a SET (IEEE 1722.1-2021 7.5.2 normal operation).

## Receipts and scripts (each listed in MANIFEST.sha256)

- `receipts/rom_words.txt`: the ROM digests and differing words at main, head, pin and pin+head, plus the E_SINFO slot side by side.
- `receipts/pp_top_suite.{log,rc,wall}`: `tb/pp_top`, seven builds.
- `receipts/notify_22.{log,rc,wall}`, `notify_22_results.json`, `notify_22_failing_checks.txt`.
- `receipts/d3_12.{log,rc,wall}`, `d3_12_results.json`, `d3_12_failing_checks.txt`.
- `receipts/chk_gates.{log,rc,wall}`: `make check`, lint, the UPC and M9 guards, `aecp_cmds`, `ucpu`, `dyn_state`, `aecp_notify`, `aecp_cmds/mutants.py`, `gen_matrix --check`.
- `receipts/decode_json_rerecord.log`.
- `receipts/aecp_mutants.{log,rc,wall}` and `receipts/aecp_dispatch_mutants.{log,rc,wall}`.
- `receipts/extra_probes.{log,rc,wall}` and `extra_probes_results.json`, from `scripts/sinfo_extra_probes.py`.
- `receipts/d3s5_probes.{log,rc,wall}` and `d3s5_probes_results.json`, from `scripts/d3s5_probes.py`.
- The consumer runs:
  - `receipts/mdp_notify_head.*`, `mdp_gsi_mutant9.*`, `mdp_notify_pinrom.*` (rc 1 expected: the pin's ROM) and `mdp_factory_first_probe.*`;
  - `receipts/milan_dp_submodule_applied.diff` (from `scripts/splice_sinfo.py`) and `receipts/milan_dp_factory_first_probe.diff` (from `scripts/sinfo_factory_first_probe.py`).
- `receipts/simulator_identity.txt`, `receipts/hosted_checks_snapshot.tsv`, `receipts/pr199_body_snapshot.md`, `receipts/clone_restore_check.txt`.
- `scripts/launch.sh`, `scripts/wait_rc.sh` and `scripts/chk_gates.sh`: the run harness.
- Host paths in the receipts are replaced by `<packet>`, `<review-clone>`, `<pinned-simulator-5.050>`, `<simulator-root>` and `<tmp-copy>`.

R681-1 FINISHED
