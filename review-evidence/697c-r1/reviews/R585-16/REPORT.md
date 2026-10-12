[R585] POSITIVE - exact head 5b4ea55160c5ee34263e24140f960c4f03d923bc

# R585-16: external independent review of issue #697 / PR #705, rounds 14 to 17

Exact head `5b4ea55160c5ee34263e24140f960c4f03d923bc`, tree `bfc159e4340d62df621848448dc3640d41f0eb1b`.
Source base `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`. Live dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, merged into the head.

This is a delta review of the commits on `8aaa2da7`:
- round 14: `d89898db`, `b62c1981`, `4a35f2f4`, `a8fe548a`;
- round 15: `44eef11f`;
- round 16: `516a69be`;
- round 17: `6e88cfb6`, then the merge of dev `c6bd08c6` (`5b4ea551`).

All five lenses were applied independently. There is no open BLOCKER, MAJOR or MINOR, so the verdict is POSITIVE.
- One RESIDUE: an over-broad sentence about what the stack's allowlist holds.
- One new SUGGESTION. The earlier optional items are retained.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md` (by reference from AGENTS.md) and `docs/README.md`.
2. Issue #697:
   - its body and frozen acceptance 1-5;
   - the round 14, 15, 16 and 17 assignments (6117713386, 6118625227, 6119960001, 6121496568);
   - the author's REVIEW READY comments 6118316100, 6119366539, 6120798872 and 6122601380.
   The round-12 scope ruling stands: adversarial code inside the proof's own modules is out of scope. No new requirement or interface clause is cited. The authority for the delta is the round-12 threat model plus the round 14-17 items.
3. `git diff c20c85bd..5b4ea551` and its history. The lane delta `8aaa2da7..6e88cfb6` was read line by line: `ctrl_build.py`, `ctrl_pin.py`, `ctrl_pin_env.py`, `ctrl_configs.py`, `ctrl_pin_store.py` and `sw/firmware/ctrl/README.md`. The merge `5b4ea551` was checked against an automatic merge.
4. Public executable evidence:
   - the live PR body;
   - the exact-head hosted check runs (run 38258540718);
   - the published probe scripts at `f1fb6dd1`, `review-evidence/697c-r1/reviews/` (each verified against its packet's `MANIFEST.sha256`).
5. Only after my own pass over the diff, my probes and a draft verdict: the prior public findings, chiefly R584-14 (6121475687) and R585-15 (6121148300).

## What the assignments ask, confirmed at this head

| Item | Result | Evidence |
|---|---|---|
| R14: every object the proof reads is checked against its id, failing closed | `ctrl_build.stored` (`ctrl_build.py:471-482`) reads `cat-file <type> <id>` as bytes and hashes `<type> <len>\0<bytes>` with the repository's object format. A mismatch is refused by its place. `pinned_tree` (`:485-504`) parses the commit and every tree itself, and no blob is read. A missing, corrupt, trailing-garbage, peeled-tag or commit-for-tree object fails closed. | `receipts/r584_12_store_probe_head_g2{43,56}.txt` (21 states each); `receipts/mutant_*_no_hash_check.log` (2 controls escape) |
| R14: R585-12's F1 refused by name before any build; F0 and F2 keep their verdicts | R585-12's `forge_probe.py`, unchanged: F0 REFUSED `src/adp.c`; F1 REFUSED `the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40`; F2 REFUSED `the pinned commit`. The same on both Gits. Three real entry points (`ctrl_build.py --stack-pin`, `maap_differential.py`, `aecp_arms.py`) exit 2 naming the forged tree, with 0 objects built. | `receipts/r585_12_forge_probe_head_g2{43,56}.txt`; `receipts/forged_entrypoints_head.txt` |
| R14: the helper passes `-c core.fsmonitor=false`, with a standing control | `ctrl_build.py:418`. Both repositories' checks now refuse `core.fsmonitor` by name first, so the setting is defence in depth. Mutant `no_helper_config`: 0 escape on either Git. | `receipts/mutant_summary_final.txt` |
| R15: local allowlist, through the helper, before any object read, refusing by name | `configured` (`:545-557`) runs at `:588`, before `rev-parse HEAD` and every `cat-file`. The probes cover promisor, partialClone, uploadpack, sshCommand, fsmonitor, hooksPath and helper keys: every one is refused by name with RAN=0. | `receipts/r584_12_store_probe_*`; `receipts/pins_head_*.log`; mutant `no_stack_allowlist`: 15 escape on 2.56.0 (on 2.43.0 Git recursed into its own promisor until the 300 s bound) |
| R15: `GIT_NO_LAZY_FETCH` set; honoured versions recorded | `ctrl_build.py:191`. Upstream source, sha256 checked against kernel.org: 2.43.0 and 2.44.0 have no `NO_LAZY_FETCH`; 2.45.0, 2.43.4 and 2.44.1 do. This matches `README.md:188-189`. | `receipts/git_no_lazy_fetch_versions.txt` |
| R16: superproject keys refused by name before the gitlink is read | `superproject_configured` (`:560-572`) runs at `:430`, before `ls-files --stage`. R585-14's two probes, unchanged, are REFUSED by name with RAN=0 on upstream 2.43.0 and on 2.56.0. The `actions/checkout` control is accepted. | `receipts/r585_14_sparse*_head_g2{43,56}.txt`; `receipts/pins_head_*.log` |
| R17: one parser, by section and variable, whatever the subsection | `parsed_key` (`:507-515`) takes the section as everything before the first dot and the variable as everything after the last. The subsection is `None`, `""` or its name, which is how Git's `parse_config_key` splits a key. `configuration` (`:518-532`) uses it for both repositories. `superproject_configured` tests `f"{section}.{variable}"` only, and `family` (`:535-542`) gives the stack's allowlist an empty subsection its own family `""`. | source; my own probe below |
| R17: R584-14's `superproject_spelling_probe.py`, unchanged, on upstream Git 2.43.0 | S2, S3 and S6-S9 are REFUSED naming the key, each with RAN=0. S0 and S5 give the same verdicts as R584-14's 516a69be receipt. Git 2.56.0 gives the same. R584-14's `stack_spelling_probe.py`: T0 ACCEPTED, T1 and T2 REFUSED by name, RAN=0. | `receipts/r584_14_superproject_spelling_head_git2{43,56}.txt`, `r584_14_stack_spelling_head_git243.txt` |
| R17: new controls fail under their mutant | Mutant `named_only`, round 16's match (a `remote` key refused only with a named subsection): exactly the three new superproject controls escape on both Gits, and on 2.43.0 Git runs the recorder. `sub_present_only`: the two subsection-less controls escape. `parser_empty_is_none` and `family_empty_is_named`: the `submodule "".active` control escapes. | `receipts/mutant_summary_final.txt` and per-mutant logs |
| R17: all earlier pin controls hold | 106 of 106 `[ok]`, census 0, figures 0, 4 of 4 figure controls. This holds on Git 2.56.0 and upstream 2.43.0. Hosted at the exact head (Git 2.55.0): `firmware-boundary` and `firmware-verilator` PASS with 106 pin controls and 0 misbehaved. | `receipts/pins_head_git2{43,56}_py314.log`; `receipts/hosted_firmware_boundary_summary.txt` |
| R17: texts claim only what the controls prove | "On any Git" and "whatever a Git version makes of it" are gone from the tree and the PR body. The counts match the code: 106, twenty-seven store controls, eight superproject, fourteen stack-key. One over-broad sentence about the allowlist remains: RES-1. | `README.md:175-189`, `:223`, `:244-261`; `ctrl_build.py:182-222`; `ctrl_pin.py:59-70`; `ctrl_pin_store.py:3-77`; live PR body |
| R17: R584-14-RES-1, R585-15-RES-1 and RES-2 applied | Applied. `README.md:189` carries R584-14-RES-1's text. `README.md:188` and `ctrl_build.py:188` say "updated 2.43.0". The PR body's Round 16 paragraph has no braces. The reference links name `5b4ea551…`. | source; live PR body |
| R17: the dev merge changes only the regenerated diagram; images equal dev's | The head's tree equals `git merge-tree 6e88cfb6 c6bd08c6` except the three conflicted diagram files. Of dev's 40 changed files, the head differs from dev only in the diagram files and in `SUBMODULES.md` and `CI_WORKFLOWS.md`, which both sides changed and which merged automatically. The diagram differs from dev only in the tsn-c-stack box. `submodule_boundaries.gen.py --check` and `--selftest`, `check_diagram_pngs.py` and `check_submodule_docs.py` (and their self-tests) pass. No `sw/`, `third_party/` or `configs/` file is in dev's delta. `ctrl_image.py --base c6bd08c6` gives `+0` in every section, and the ELF and `.img.bin` of both default shapes are byte-identical to dev's. | `receipts/merge_and_scope.txt`, `dev_delta_files.txt`, `docs_*.log`, `ctrl_image_base_dev.log`, `ctrl_image_elf_hashes.txt` |

### My own probes (independent of the earlier reviewers' scripts)

`scripts/spelling_probe.py` builds a sparse superproject from scratch. Its sparse directory holding the gitlink lacks its tree. Into its own configuration it writes 12 spellings that reach a recorder through `ext::` if Git fetches:
- no subsection;
- an empty subsection;
- a key with no value;
- upper case;
- an old-style `[remote.o]`;
- a dotted subsection;
- `partialclonefilter` alone;
- `extensions.partialClone` alone;
- an `includeIf gitdir` file;
- the work tree's own configuration.

The proof's read runs first, then a raw `ls-files` with the same Git. Results:
- At the head on upstream 2.43.0, all 12 are REFUSED naming the key, with RAN=0. The raw read starts the recorder in all 12 (RAN=1), so each is a live route.
- At `516a69be` on 2.43.0, the subsection-less, empty-subsection, include and work-tree spellings ran the recorder: 8 of 12, RAN=1. So the probe detects the defect when it is present.
- Git 2.56.0 gives RAN=0 at both heads, because of `GIT_NO_LAZY_FETCH`.

Receipts: `receipts/spelling_{head,old}_g2{43,56}.{log,json}`.

## Findings

### R585-16-RES-1 - RESIDUE - Docs - the allowlist is said to hold "no key that names a program", but an allowlisted key's value may name one

- **Artifact:**
  - `sw/firmware/ctrl/README.md:181`: "it holds Git's own bookkeeping only, and no key that names a program, a promisor remote or its transport."
  - `sw/firmware/ctrl/test/ctrl_build.py:199`: "None names a program or a store."
  - `ctrl_build.py:551-552`: "and no key of it names a program, a promisor remote or its transport."
- **Authority:** round-17 item 3, "the texts state exactly what is held".
- **Evidence:** `remote.<name>.url` is allowlisted and judged by key, not value. A clone whose `remote.origin.url` is `ext::<recorder> %S` is ACCEPTED at the pin with RAN=0, on Git 2.43.0 and 2.56.0. With the pinned `src/` tree missing, it is REFUSED "cannot read the pinned tree", again with RAN=0 (`receipts/allowlisted_value_g2{43,56}.log`). The key names a program, but no command of the proof contacts a remote, so Git never starts it.
- **Impact:** wording only. The behaviour the sentence is meant to state holds: Git starts no program and fetches nothing. No measurement, figure, verdict, test or code depends on the sentence. `stack_pin`'s docstring (`ctrl_build.py:578-579`) already says it correctly: "no key of it names a program Git starts or a remote it fetches from".
- **Exact fix:**
  - `README.md:181`: replace "and no key that names a program, a promisor remote or its transport." with "and no key that has Git start a program or declares a promisor remote or its transport while the pin is decided (a remote's or a submodule's `url` may name any transport, but no command of the proof contacts a remote)."
  - `ctrl_build.py:199`: replace "None names a program or a store." with "None has Git start a program or fetch while the pin is decided."
  - `ctrl_build.py:551-552`: replace "and no key of it names a program, a promisor remote or its transport." with "and no key of it has Git start a program, or declares a promisor remote or its transport, while the pin is decided."
- **Verification:** re-read the three places.

### R585-16-S1 - SUGGESTION - Docs, Robustness - a developer's blobless (`--filter`) superproject clone is refused by name, which no text says

- **Artifact:** `sw/firmware/ctrl/README.md:183-186`.
- **Evidence:** `git clone --filter=blob:none` writes `remote.origin.promisor=true` and `remote.origin.partialclonefilter=blob:none`. `stack_gitlink` on such a superproject is refused by those keys (`receipts/partial_clone_superproject.txt`). It fails closed and the hosted checkout is unaffected, which the exact-head hosted run confirms.
- **Suggestion:** one sentence saying that a superproject cloned with `--filter` cannot run the pinned gates until it is a full clone.

### Observation, not a finding

Git 2.56.0 itself crashes with SIGSEGV (rc -11) in a raw `ls-files --stage` of a sparse index whose sparse directory's tree object is missing. This happens even with no promisor configured. Under the proof the read yields no entry, and `stack_gitlink` refuses "is not one stage-0 gitlink", failing closed (`receipts/spelling_head_g256.log`, RAW lines). This is a Git defect outside this PR.

## Prior public findings at this head

| Finding | Status at `5b4ea551` | Evidence |
|---|---|---|
| R584-14-F1 (MINOR: subsection-less and empty-subsection promisor spellings pass the superproject check on Git without `GIT_NO_LAZY_FETCH`) | RESOLVED. R584-14's probe, unchanged: S2, S3 and S6-S9 are REFUSED by key with RAN=0 on upstream 2.43.0. My 12-spelling probe agrees. Three standing controls escape under round 16's match. | `receipts/r584_14_superproject_spelling_head_git243.txt`, `spelling_head_g243.log`, `mutant_*_named_only.log` |
| R584-14-RES-1 (README CVE-release wording) | APPLIED at `README.md:189` | source |
| R585-15-RES-1 (Ubuntu "updated" package) | APPLIED at `README.md:188`, `ctrl_build.py:188` | source |
| R585-15-RES-2 (stray braces in PR body) | APPLIED | live PR body |
| R585-14-F1 (superproject promisor, named remote) | Still RESOLVED: both of R585-14's probes are REFUSED by name with RAN=0 on 2.43.0 and 2.56.0 | `receipts/r585_14_sparse*_head_*.txt` |
| R584-12-F1 = R585-13-F1 (stack promisor transport) | Still RESOLVED: R584-12's 21 store probes give RAN=0, and toctou's plant does not land | `receipts/r584_12_store_probe_head_*.txt` |
| R584-11-F1 = R585-12-F1 (forged `src/` tree) | Still RESOLVED | `receipts/r585_12_forge_probe_head_*.txt`, `forged_entrypoints_head.txt` |
| R585-12-S1, R584-12-S1 = R585-13-S2 | Still RESOLVED: refused by key; escape under `no_superproject_check` and `no_stack_allowlist` | mutants |
| R585-14-S1 (`needle in detail`, `ctrl_pin.py:994`) | RETAINED SUGGESTION | source |
| R585-14-S2 (no control fails for `GIT_NO_LAZY_FETCH` or `core.fsmonitor=false` alone) | RETAINED SUGGESTION. Confirmed: `no_lazy_env`, `no_helper_config` and `no_defence_in_depth` each let 0 escape on both Gits | `receipts/mutant_summary_final.txt` |
| R585-14-S3 (unparsable stack configuration reported as "not its own checkout", now `ctrl_build.py:587`) | RETAINED SUGGESTION | source |
| R584-13-S1 (allowlist is Linux file-system shaped) | RETAINED SUGGESTION | source |
| R585-13-S1 (no standing control forges the root tree) | RETAINED SUGGESTION. The head refuses it: R584-12 `forged_root` | `receipts/r584_12_store_probe_head_*.txt` |
| R585-13-S3 ("cannot read the pinned tree" for a commit read, now `ctrl_build.py:477`) | RETAINED SUGGESTION | source |
| R584-11-S1, R584-9-S1, R585-2-S2 | RETAINED SUGGESTIONS, untouched by the delta | as tabled by R585-15 |
| R584-8-RES-1 and the other carried residue for #495 | RETAINED; not re-verified one by one | as tabled by R585-15 |

## Lens results

```text
[R585] PASS Conformance - issue #697 acceptance 1-5 and assignments 6117713386, 6118625227, 6119960001, 6121496568; sw/firmware/ctrl/test/ctrl_build.py:182-222, :412-430, :471-600; ctrl_pin_store.py; live PR body; receipts/r584_14_superproject_spelling_head_git243.txt, r585_14_sparse*_head_*.txt, r585_12_forge_probe_head_*.txt, merge_and_scope.txt, ctrl_image_elf_hashes.txt - every round 14-17 item is met at the head: hash-checked objects, allowlist before any object read, GIT_NO_LAZY_FETCH with versions verified from upstream source, superproject keys judged by section and variable before the index read, R584-14's probe REFUSED/RAN=0 on upstream 2.43.0, merge equal to dev except the regenerated diagram, images byte-identical to dev at both default shapes; acceptance 1-5 untouched (no moved path, pin 405dc683, lwSRP 08ee86e8 unchanged).
[R585] PASS RTL - receipts/merge_and_scope.txt; git diff --name-only 8aaa2da7..6e88cfb6 (6 files under sw/firmware/ctrl, no hdl/, tb/, Makefile, workflow or build flag); head vs dev c6bd08c6 (72 lane files; dev's tb/ and .sv changes byte-equal to dev); gitlinks at head - no RTL or interface contract changes in the delta; the merge carries dev's reviewed RTL/testbench files unchanged; the helper contract (GitRun.raw defaulted, bytes decoded with surrogateescape) holds for every caller; ctrl_configs.GATE gains ctrl_pin_store.py, a gate module, not a builder.
[R585] PASS Robustness - ctrl_build.py:471-572; receipts/spelling_{head,old}_g2{43,56}.log (12 spellings incl. upper case, old-style, dotted, valueless, includeIf, worktree), r584_12_store_probe_head_*.txt (missing, corrupt, trailing, tag-for-commit, commit-for-tree, alternate, deep forged tree), allowlisted_value_g2{43,56}.log, mutant_*_superproject_check_late.log - each malformed, forged, missing or re-spelled input fails closed by name with RAN=0 on upstream 2.43.0 and 2.56.0; check order is load-bearing on 2.43.0 (5 escape when the superproject check follows the index read).
[R585] PASS Tests - ctrl_pin_store.py:100-453; ctrl_pin.py:914-1000; receipts/pins_head_git2{43,56}_py314.log (106/106 [ok], census 0, figures 0); receipts/mutant_summary_final.txt (12 mutants x 2 Gits); receipts/hosted_firmware_boundary_summary.txt - every new mechanism has a standing control that fails under its mutant (round-16 match 3, named-or-empty 2, parser 1, family 1, superproject check removed 7, late 5 on 2.43.0, local scope only 1, hash check 2, allowlist 15); defence-in-depth settings alone 0 (R585-14-S2, retained).
[R585] PASS Docs - sw/firmware/ctrl/README.md:167-261; ctrl_build.py:182-222 and docstrings :425-600; ctrl_pin.py:1-140; ctrl_pin_store.py:3-77; live PR body (Status, Round 17, Known limitations, references); receipts/docs_*.log (docs_check 0, em-dash 0 over 435 lines vs c6bd08c6, py-idiom ratchets, diagram/PNG/submodule-doc checks and self-tests) - figures equal the code; no "any Git" claim remains; residues of R584-14 and R585-15 applied; one wording residue R585-16-RES-1 (no effect on coverage).
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #697 acceptance 1-5 and the round 14-17 assignments; `ctrl_build.py:182-222`, `:412-600`; `ctrl_pin_store.py`; live PR body; `receipts/r584_14_*`, `r585_14_*`, `r585_12_*`, `merge_and_scope.txt`, `ctrl_image_*` | R585-16 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| RTL | CLEAN | `git diff --name-only 8aaa2da7..6e88cfb6`; head vs dev `c6bd08c6` (72 files; dev's tb/.sv byte-equal); gitlinks; helper contract `ctrl_build.py:231-240`, `:412-422`; `ctrl_configs.py:74-76` | R585-16 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| Robustness | CLEAN | `ctrl_build.py:471-572`; `receipts/spelling_*`, `r584_12_store_probe_head_*`, `allowlisted_value_*`, `forged_entrypoints_head.txt`, `mutant_*_superproject_check_late.log` | R585-16 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| Tests | CLEAN | `ctrl_pin_store.py:100-453`; `ctrl_pin.py:914-1000`; `receipts/pins_head_*`; `receipts/mutant_summary_final.txt` and 48 per-mutant files; hosted `firmware-boundary`/`firmware-verilator` summary | R585-16 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |
| Docs | CLEAN (RESIDUE R585-16-RES-1 only) | `sw/firmware/ctrl/README.md:167-261`; `ctrl_build.py` comments and docstrings; `ctrl_pin.py:1-140`; `ctrl_pin_store.py:3-77`; live PR body; `receipts/docs_*.log` | R585-16 | `5b4ea55160c5ee34263e24140f960c4f03d923bc` |

## Real limits

- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts.
- Not run here:
  - the full `ctrl_boundary.py --require-rv32 --selftest`. A start was refused because this checkout has no lwSRP submodule and the host's toolchain is not the runner replica's (`receipts/boundary_without_verilator.log`, rc 2, nothing judged);
  - `firmware-unit`, coverage, the 506-plant mutation campaigns, the hook-rule campaign and the full 54-command docs job.
  The 106 pin controls were run alone through `scripts/run_pins.py`, which calls the head's own `pin_controls`, `proof_census`, `figures` and `figure_controls`.
- Images: only `ctrl_image.py`'s two default shapes were built, at the head and at dev `c6bd08c6` with the pinned RV32 SDK, and their ELF and `.img.bin` are byte-identical. The author's 35-image table was not re-derived. Dev's delta touches no `sw/`, `third_party/` or `configs/` file.
- Python was CPython 3.14.7 only. This host's CPython 3.12.3 has no `yaml`. Ubuntu's patched Git 2.43.0 was not exercised. Upstream Git 2.43.0 was built from `git-2.43.0.tar.xz` (sha256 `5446603e…76ec`, equal to kernel.org's `sha256sums.asc`).
- Mutant `no_stack_allowlist` on Git 2.43.0 printed 5 escapes, then Git recursed into a promisor that is the clone itself and hit the 300 s bound (rc 124). Its 2.56.0 run gives the full count of 15.
- Hosted at the exact head (snapshot `receipts/hosted_checkruns_head_snapshot.tsv`): 16 success, 1 skipped (Physical gPTP nightly), 6 in progress (`firmware-unit`, `elaborate`, four Verilator shards). Hosted and act acceptance belong to the manager.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- After the probes, the clone was verified (`receipts/checkout_integrity.txt`):
  - 1295 tracked files match their index blobs by bytes, mode and stage;
  - the index equals HEAD, and the status is clean;
  - all six gitlinks match HEAD, and the checked-out ones match their submodule HEADs;
  - the pin check passes.
  The only change to the clone is the initialised tsn-c-stack submodule at its gitlink.

## Pending manager duties

- Carry R585-16-RES-1 to the residue checklist with its exact fix, along with the retained #495 residue. R585-16-S1 and the retained suggestions are optional.
- Validate the current-dev merge candidate at the merge turn (source base `c20c85bd`, live dev `c6bd08c6`). The builder and native banks run there.
- Own hosted and act acceptance at the exact head. `firmware-unit`, `elaborate` and four Verilator shards were still running at the snapshot.
- The internal review R584-15 is running at the same head. Merging needs two positive reviews and the full completion bar.

R585-16 FINISHED
