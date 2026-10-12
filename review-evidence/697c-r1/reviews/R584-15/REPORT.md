[R584] POSITIVE - exact head 5b4ea55160c5ee34263e24140f960c4f03d923bc

Round R584-15, internal cleared-context review of PR #705 for issue #697.
Head `5b4ea55160c5ee34263e24140f960c4f03d923bc`, tree `bfc159e4340d62df621848448dc3640d41f0eb1b`.
This is a delta review of rounds 14 to 17: `8aaa2da7..6e88cfb6` (seven lane commits) and the merge of dev `c6bd08c6`.
All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
There is no open BLOCKER, MAJOR or MINOR.
One RESIDUE (PR-body wording) and one SUGGESTION are recorded.

## Reconstruction

- Authorities: AGENTS.md, CONTRIBUTING.md, docs/README.md.
- Issue #697: its acceptance, the owner decisions (6074086970, 6074093506, 6074191062), the lane assignment (6091228902) and the pin ruling (6092176555). Also the round-12 scope ruling (6114400461) and the round 14 to 17 assignments (6117713386, 6118625227, 6119960001, 6121496568).
- The diff `c20c85bd..5b4ea551`, the history `8aaa2da7..5b4ea551`, and the published evidence branch `697c-review-evidence` at `f1fb6dd1`.
- I made my own pass over the delta before reading prior findings. I then read R584-14 (6121475687) and R585-15 (6121148300) to settle what they carry.

## What each round asked, confirmed at this head

| Item | Result | Evidence |
|---|---|---|
| R14-1: every object read is checked against its id and fails closed | Met. `stored` (`ctrl_build.py:471-482`) hashes `<type> <len>\0<raw>` from `cat-file` for the pinned commit and every tree `pinned_tree` walks (`:485-504`). No blob is read; files are hashed from their own bytes (`:437-464`). A tag served for the commit, a commit served for a tree, a deep forged tree, an alternate-store forgery, a corrupt object and a missing object are all refused. | `receipts/prior_probes/store_probe.*.txt` |
| R14-1: R585-12 `forge_probe.py` F1 refused by name before any build; F0 and F2 keep their verdicts | Met on both Gits. F1 is refused as `the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40`. F0 is refused by `src/adp.c`. F2 stays refused, now named by the forged pinned commit. Three entry points exit 2 with 0 objects built. | `receipts/prior_probes/forge_probe.*.txt`, `forged_entrypoints.*.txt` |
| R14-2: `-c core.fsmonitor=false` with a standing control | Met (`ctrl_build.py:196`, `:418`). Both repositories also refuse `core.fsmonitor` by name, so removing the helper setting lets 0 controls escape (M10). It is stated as defence in depth (R585-14-S2, retained). | `receipts/mutants/M10-*.log` |
| R15-1: stack allowlist runs through the helper before any object read and refuses by name | Met. `configured(stack)` (`:588`) runs after `rev-parse --show-toplevel` and before `rev-parse HEAD` and every `cat-file`. It refuses every key whose family is outside `STACK_CONFIG` (`:204-207`). | 15 stack controls `[ok]`; M09 lets 15 escape on 2.56.0 |
| R15-2: `GIT_NO_LAZY_FETCH=1`, with the honouring versions recorded | Met (`:191-192`). From the upstream sources: v2.45.0 reads it (`environment.c` sets `fetch_if_missing = 0`), and so do v2.39.4, v2.42.2, v2.43.4 and v2.44.1. v2.43.0 and v2.44.0 do not. The README (`:188-189`) states exactly this. | source reading (Limits) |
| R15-3: R584-12 `store_probe.py` ends in refusal with RAN=0 | Met on upstream 2.43.0 and on 2.56.0. `lazy_uploadpack_fail`, `lazy_uploadpack_serve`, `lazy_ssh` and `lazy_toctou` are each refused by key with `RAN=0`. The toctou plant does not land. | `receipts/prior_probes/store_probe.*.txt` |
| R16-1: superproject keys refused before the gitlink is read; actions/checkout keys pass | Met. `superproject_configured(root)` (`:430`) runs before `ls-files --stage` (`:431`). The `actions/checkout` control is accepted, and hosted `firmware-boundary` passed on a real checkout at this head. | M07 on 2.43.0: 5 escape, Git running the recorder |
| R16-2: R585-14's two probes end in refusal with RAN=0 on upstream 2.43.0 | Met on both Gits. | `receipts/prior_probes/sparse_gitlink*.txt` |
| R17-1: one parser splits section, subsection (absent, empty or named) and variable the way Git does; the superproject is judged by (section, variable) | Met. `parsed_key` (`:507-515`) has Git's `parse_config_key` split: first dot, last dot, and the subsection between them. `superproject_configured` (`:568-570`) tests `f"{section}.{variable}"` only. Git 2.43.0 declares a promisor only through `extensions.partialclone` (`setup.c`) and `remote.*.promisor` / `remote.*.partialclonefilter` (`promisor-remote.c`), with `xmemdupz(name, namelen)` naming a missing subsection `""`. All three are refused for every subsection. | Git 2.43.0 source; probes below |
| R17-2: R584-14 `superproject_spelling_probe.py` re-run unchanged on upstream 2.43.0 | S2, S3 and S6-S9 end REFUSED naming the key with `RAN=0`. S0 and S5 keep their 516a69be verdicts (refused by name, `RAN=0`). S1 (check removed) is ACCEPTED with `RAN=1`, so the probe can fail. Same verdicts on 2.56.0. | `receipts/superproject_spelling_head_git2.43.0.txt`, `..._git2.56.0.txt` |
| R17-2: new controls fail under their mutant | Met on both Gits. M01 (round 16's named-only match): the 3 new superproject controls escape. On 2.43.0 Git runs the recorder; on 2.56.0 they escape by their words. M02 (subsection required): 2 escape. M03 (empty subsection passes): 1 escapes. M04 (parser reads empty as none) and M05 (family reads empty as named): `submodule "".active` escapes. | `receipts/mutants/M01-M05*.log` |
| R17-2: all earlier pin controls hold | 106 pin controls, 0 misbehaved, census 0, figures 0, 4 figure controls. This holds on upstream 2.43.0 + CPython 3.12.3 and on 2.56.0 + CPython 3.14.7, and inside both boundary self-tests. | `receipts/pin_controls_head_*.log`, `boundary_*.log` |
| R17-3: the texts claim only what the controls prove | Met. README `:175-189`, `ctrl_build.py:182-222` and `:507-572`, `ctrl_pin.py:59-70` and `ctrl_pin_store.py:3-77` state the allowlist, the six (section, variable) pairs and the two defence-in-depth settings. "On any Git" is gone from the tree and the PR body. The counts (27 store, 17 environment, 8 superproject, 14 refused plus 1 accepted stack controls) match the run. | figure check 0; my count of `receipts/pin_controls_head_*.log` |
| R17-3: R584-14-RES-1, R585-15-RES-1/2 applied | Applied with their exact texts: README `:188` and `:189`, `ctrl_build.py:188`, and the PR body's Round 16 paragraph. | live PR body |
| R17-4: the merge of dev `c6bd08c6` | A three-way audit of every path against base `c20c85bd` finds 66 lane-only paths and 35 dev-only paths, each with its own side's blob in the merge. Six paths changed on both sides. `git merge-tree --write-tree 6e88cfb6 c6bd08c6` reproduces the head tree except the three conflicted diagram files (`.drawio`, `.png`, `PNG_MANIFEST.json`). The generator's `--check` and `--selftest`, `check_diagram_pngs.py` and `check_submodule_docs.py` pass at the head. The merge differs from dev only in the lane's 72 paths. | `receipts/merge_audit.txt`, `receipts/docs/*` |
| Images equal dev's | I built all 5 `ctrl_image` shapes three ways: at the head, as the head's `--base c6bd08c6`, and with dev `c6bd08c6`'s own builder in a disposable dev tree. Each set is byte-identical (`8c27ee19…`, `b7976d5c…`, `b119b2b5…`, `5a4086ce…`, `acb380ee…`), with `+0` in every section. These equal the author's table. I did not rebuild the 30 SRP and AECP images (Limits). Their inputs are unchanged since `8aaa2da7`, apart from pin-proof test modules, and dev changed no `sw/`, `configs/` or `third_party/` path. | `receipts/ctrl_image_elf_compare.txt`, `image_inputs_since_516a69be.txt`, `dev_side_paths.txt` |
| Round-12 scope ruling | Applied. No finding below needs code inside the proof's own modules. | - |

My own further spellings (`probes/r584_15_spelling_probe.py`), each over an `ext::` program that would serve the tree:
- `[Remote] Promisor`;
- the legacy `[remote.x]`;
- a dotted subsection `"a.b"`;
- a value-less `promisor`;
- an included file;
- an `includeIf "onbranch:"` file;
- the work tree's own file;
- an empty-subsection `partialCloneFilter`;
- `extensions.partialClone` with a named remote.

Each is REFUSED naming its key with `RAN=0` on both Gits. The route keys alone (`url.*.insteadOf`, `protocol.ext.allow`) start nothing. With the check removed, 2.43.0 runs the program (`RAN=1`).

## Findings

### R584-15-RES-1 - RESIDUE - Docs - PR body still says the head is unpublished

- **Artifact:** PR #705 body, `## Round 17`, "Open, for the manager", item (d): "the head is not pushed, so no hosted run exists at it."
- **Evidence:** the PR head is `5b4ea551`. Hosted runs exist at it: `rtl-fast`, `firmware-boundary`, `firmware-unit` and `firmware-verilator` succeeded, and two Verilator shards were still running when listed (`receipts/hosted_check_runs_at_head.tsv`).
- **Impact:** wording only. No measurement, figure, verdict, test, code or claim depends on it.
- **Exact fix:** replace that item with "(d) the head was pushed after this section was prepared; its hosted runs are the manager's to accept."
- **Verification:** re-read the item.

### R584-15-S1 - SUGGESTION - Tests, Robustness - a store control can hang instead of ending in a verdict

- **Artifact:** `ctrl_pin_store.py:393-395` (`checked` calls `stack_pin` in-process) and `ctrl_pin.py:986-996`.
- **Evidence:** under mutant M09 (the stack allowlist not called) on upstream Git 2.43.0, 7 controls escape. The run then stops making progress in a lazy self-fetch from a promisor remote that is the clone itself, with `git-upload-pack` children piling up, until my 590 s and 420 s caps (`receipts/mutants/M09-*.g243.stream.log`). At the head every control ends in its verdict, so this matters only when a regression reaches it.
- **Impact:** the self-test would end at the job's timeout rather than with a named `[ESCAPED]` line.
- **Suggested outcome:** give each store control's read a bounded time, as the proof runs already have (`PROOF_RUN_TIMEOUT_S`), and report a timeout as an escape.

## Prior public findings at this head

| Item | Disposition | Evidence |
|---|---|---|
| R584-14-F1 (MINOR: subsection-less and empty-subsection promisor spellings pass the superproject check) | RESOLVED. The probe re-ran unchanged on upstream 2.43.0 with every required verdict, and the new controls escape under M01-M03. | `receipts/superproject_spelling_head_git2.43.0.txt`, `receipts/mutants/M01-M03*` |
| R584-14-RES-1 | APPLIED, `README.md:189` | source |
| R585-15-RES-1 | APPLIED, `README.md:188`, `ctrl_build.py:188` (its `:186` part takes R584-14-RES-1's text, as directed) | source |
| R585-15-RES-2 | APPLIED, PR body Round 16 paragraph | live PR body |
| R585-14-F1, R584-11-F1 = R585-12-F1, R584-12-F1 = R585-13-F1 | Still RESOLVED; their probes print refusals with `RAN=0` | `receipts/prior_probes/*` |
| R585-14-S1 (`needle in detail`, `ctrl_pin.py:994`) | RETAINED SUGGESTION | source |
| R585-14-S2 (no control fails for either defence-in-depth setting alone) | RETAINED SUGGESTION; M10 and M11 escape 0 on both Gits | `receipts/mutants/M10*`, `M11*` |
| R585-14-S3 (unparsable stack configuration reported as "not its own checkout", now `ctrl_build.py:585-587`) | RETAINED SUGGESTION, fails closed | source |
| R584-13-S1 (allowlist holds what Git writes on Linux) | RETAINED SUGGESTION, fails closed | `ctrl_build.py:204-207` |
| R585-13-S1 (no standing control forges the root tree), R585-13-S3 ("cannot read the pinned tree" for a commit read, now `ctrl_build.py:477`) | RETAINED SUGGESTIONS; `store_probe` `forged_root` is refused at the head | `receipts/prior_probes/store_probe.*` |
| R584-11-S1, R584-9-S1, R585-2-S2, R584-8-RES-1 and the residue carried for #495 | RETAINED; outside this delta, not re-verified one by one | - |

## Lens results

```text
[R584] PASS Conformance - ctrl_build.py:425-434,507-572 and Git 2.43.0 setup.c:550-575, promisor-remote.c promisor_remote_config; receipts/superproject_spelling_head_git2.43.0.txt, r584_15_spelling_git2.43.0.txt, ctrl_image_elf_compare.txt, merge_audit.txt - round 17 items 1-4 against #697 comment 6121496568, round 14-16 items against 6117713386/6118625227/6119960001, acceptance 3 (images) for the 5 ctrl_image shapes against dev c6bd08c6's own build
[R584] PASS RTL - git diff c6bd08c6..5b4ea551 and c20c85bd..6e88cfb6 over hdl/, syn/ and the processor and axis gitlinks (0 paths); tb/verilator/mbx/Makefile pin prerequisites held by receipts/boundary_only_verilator.log (6 boundary, 106 pin, 4 figure controls, 0 misbehaved, scoped Verilator 5.050) - no RTL, CDC or interface change at this head; the bench's targets refuse a poisoned stack before compiling
[R584] PASS Robustness - ctrl_build.py:471-504 (fail-closed object reads), :545-572 (unknown scope, empty subsection and value-less keys); receipts/prior_probes/store_probe.*.txt (tag-for-commit, commit-for-tree, corrupt, missing, alternates, toctou), r584_15_spelling_*.txt (case, legacy subsection, include, includeIf, worktree) - malformed, missing and substituted objects and every key spelling tried, on two Gits
[R584] PASS Tests - ctrl_pin_store.py:297-451, ctrl_pin.py:983-996; receipts/mutants/M00-M13 on Git 2.43.0 and 2.56.0, pin_controls_head_*.log, boundary_without_verilator.log (2822 compiled sources of 3049 invocations, 105/106/4, 0 misbehaved) - each new control fails under its mutant; R584-15-S1 is a suggestion only
[R584] PASS Docs - sw/firmware/ctrl/README.md:165-261, ctrl_build.py:179-222, ctrl_pin.py:59-70, ctrl_pin_store.py:3-77, PR #705 body (Status, Rounds 14-17, Known limitations); receipts/docs_summary.txt (74 of 76 docs commands rc 0, em-dash against c6bd08c6 clean) - figures equal the run's counts, the residue fixes are applied, R584-15-RES-1 is residue only
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_build.py` pin proof; Git 2.43.0 promisor sources; spelling probes; merge audit; 5 image shapes against dev | R584-15 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| RTL | CLEAN | RTL and processor paths (none changed); mailbox bench pin prerequisites in the Verilator boundary run | R584-15 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| Robustness | CLEAN | object-store and configuration edge cases on two Gits; my 11 spellings | R584-15 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| Tests | CLEAN | 106 pin controls on two Gits and two Pythons; 14 mutants on two Gits; both boundary self-tests | R584-15 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| Docs | CLEAN (RESIDUE R584-15-RES-1 to the checklist) | README, docstrings, PR body; 76 docs commands | R584-15 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |

## Real limits

- I did not rebuild the 30 SRP and AECP images. Their runtime archives need picolibc, compiler-rt and LiteX sources. Identity for them rests on two things: their inputs are unchanged since `8aaa2da7` apart from pin-proof modules, and dev changed no image input. The 5 `ctrl_image` shapes were rebuilt and compared.
- I did not verify the Ubuntu `2.43.0-1ubuntu7.3` / `-1ubuntu7` statement or the hosted runner's Git 2.55.0. The upstream tags were checked from source.
- Two of the 76 docs commands did not complete. `gen_hdl_reference.py --selftest` refused because its separately pinned parser is not installed here. `sw/builder/test_builder.py` (a builder bank) hit my 580 s cap while passing. The PR touches neither file.
- Firmware-unit's suites, the full Verilator sweep, Yosys and the builder banks were not run. Act was not run. Physical calibration was NOT RUN, and nothing here is hardware evidence.
- Deviation: one docs-command batch was first launched with a wrapper that dropped the interpreter word. Through its shebang, the candidate's `scripts/act_ci.py --selftest` then ran once on the host. It stopped at a PyYAML refusal inside its offline self-test. No container was listed afterwards, and the clone's tracked state was verified unchanged (`receipts/checkout_integrity.txt`). It gives no evidence and is not cited.
- My boundary run counted 3049 and 926 recorded invocations, where the author's published counts are 3053 and 930. The compiled-source counts are equal (2822 and 829). The difference is in invocations recorded on this host. Findings and controls are identical.

## Pending manager duties

- Accept the hosted exact-head contexts. `verilator-suites` and `yosys-portability` were not yet concluded when listed: shards 1/5 and 4/5 were in progress.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and run act through the audited-install bootstrap this PR's `act_ci.py` manifest change needs.
- Carry R584-15-RES-1 to the residue checklist.
- Obtain the external review for this head.

R584-15 FINISHED
