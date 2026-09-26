[A330]

# Round 2 handoff for issue #567

Assignment: https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786

Executor: [A330]. Independent reviewers: [R326] internal and [R327] external.

Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.
Branch: `567-pp-pin-0922e434`.
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Starting head: `1912c0472635ea174f1a2e2de2f3c96d09f55e9b`.
Final local head: `c9484ac8e86cb33d1120471530f9e1762bd4af1f`.
Commit subject: `Record unchanged ROM digests for processor pin 0922e434`.
The commit contains one subject line, no body, and no trailers.

## Result and scope

The repository recorder added exactly two rows for processor `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.
Both digests equal the corresponding `990f96526bb89356c963a260ebbdcf2a77e6623a` rows.
All 37 pre-existing rows, including the current gPTP row, and the header are unchanged.
No ledger content was edited manually.
The final commit changes only `syn/yosys/rom_digests.tsv`: two insertions, no deletions.
The working tree is clean.

The processor HDL tree is `d8879608b8fae8c06a505d7d5d485a97903a5766` at both pins.
`git -C protocol-processor diff --stat 990f9652 0922e434 -- hdl/` is empty.
The ROM inputs are unchanged; re-recording is required because the ledger keys include the exact processor pin.
The public Round 2 decision corrects the original acceptance 2 wording.

## Ledger diff

```diff
diff --git a/syn/yosys/rom_digests.tsv b/syn/yosys/rom_digests.tsv
index cc1a8e0c..ea2488fe 100644
--- a/syn/yosys/rom_digests.tsv
+++ b/syn/yosys/rom_digests.tsv
@@ -4,6 +4,8 @@
 # ooc.sh refuses to price the design either way. A pin bump re-records with
 #   ./ooc.sh --record-rom-digests
 # and that diff is reviewed with the bump. Columns: pin<TAB>image<TAB>sha256.
+0922e43408f891fc0b84a84691df86b4fd0f1c0d	ltn_rom.hex	23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956
+0922e43408f891fc0b84a84691df86b4fd0f1c0d	ucode.hex	23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144
 09f9bf3846511f8388d995126502ed92eaa65213	ltn_rom.hex	23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956
 09f9bf3846511f8388d995126502ed92eaa65213	ucode.hex	23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144
 0c208442c67213c04bde0eb75ec0f649eb09890b	ltn_rom.hex	23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956
```

## Digest comparison

| Image | SHA-256 at `990f9652` | SHA-256 at `0922e434` | Result |
|---|---|---|---|
| `ltn_rom.hex` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | MATCH |
| `ucode.hex` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | MATCH |

## Gate results

| Gate / command | rc | Evidence |
|---|---:|---|
| `cd syn/yosys && ./ooc.sh --record-rom-digests` | 0 | `record-rom-digests.log`; generated two new rows |
| Compare both new rows with the previous pin and prove existing rows unchanged | 0 | `digest-comparison.tsv`; both MATCH, 37 existing rows retained |
| `cd syn/yosys && ./ooc.sh KL_pp_shadow` | 0 | `ooc-pp-shadow.log`; normal ledger-reading path and full processor-wrapper synthesis |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | `rtl-fast-yosys.log`; 3 tops, 3 PASS, 0 FAIL |
| `python3 -B scripts/docs_check.py` in the candidate worktree | 0 | `docs-git.log`; 0 findings, 23/23 scrub controls, 4/4 routing controls |
| `python3 -B scripts/docs_check.py` in a metadata-free export of the final head | 0 | `docs-no-git.log`; 0 findings, 22/22 scrub controls, 4/4 routing controls |
| `python3 -B scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | `em-dash.log`; 0 findings, 339/339 controls |
| `git diff --check` | 0 | `diff-check.log`; clean working tree |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD` | 0 | `diff-check-base.log`; complete branch diff clean |
| `git diff --cached --check` before commit | 0 | Staged ledger passed before the one-line commit |

The two synthesis runs tested the exact source and ledger bytes subsequently committed at the final head.
The documentation and whitespace checks ran after that commit.
All commands ran in the foreground, without piping a gate to another process.
Synthesis commands had a 3,600-second timeout; documentation commands had a 1,800-second timeout.

The normal OOC run validates all three generated ROMs against their owning-pin rows, then hashes the consuming copies before and after synthesis.
Its processor-wrapper result is LUT 60,855; LUTRAM 6,136; total LUT 66,991; FF 30,187; RAMB36 15; RAMB18 4; DSP 6; CARRY4 2,104.
The three-top elaboration command is the command at `.github/workflows/rtl-fast.yml:186`.
Its `--no-structural` flag follows that job's command; the log explicitly records that structural checks are skipped in that worker.
These are local scoped results. The full hosted workflow, independent review, and merge gates remain pending.

## Environment and reproducibility

Local synthesis used Yosys 0.66 and the verified CI-pinned sv2v v0.0.12 archive.
The archive SHA-256 is `ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00`.
`tool-versions.txt` records the complete local build strings.
The local Yosys binary is a distribution build; this is not a claim of an identical hosted build.
Both synthesis scripts selected `/usr/lib/libjemalloc.so.2`.
An exported shell function selected the isolated converter because the scripts prepend the user's local binary directory.
The setup, with `VALIDATION_TOOLS` pointing to the temporary tool directory recorded in `toolchain-location.txt`, was:

```sh
sv2v() { "$VALIDATION_TOOLS/sv2v" "$@"; }
export VALIDATION_TOOLS
export -f sv2v
```

The first em-dash attempt returned 2 because the system environment lacked the required `html5lib` renderer dependency.
That refusal is preserved in `em-dash-attempt-1.log`; it was not counted as a pass.
The repository's hash-locked `tools/markdown/requirements.txt` was installed in a temporary virtual environment.
The final successful em-dash command selected that environment's Python through PATH.
No tracked file or requirement changed to obtain the pass.

The no-Git documentation mode used `git archive` of the final head, extracted under a temporary directory with no Git metadata.
It ran the actual `python3 -B scripts/docs_check.py` entry point and reported `filesystem walk (no git)`.
The export was removed after the command completed.
The inventory-parity control is explicitly skipped in this mode because it requires Git metadata; it is not counted among the 22 executed scrub controls.
Both documentation modes examined 166 Markdown files and 884 scrubbed text files.
Toolchains and source exports stayed outside the output directory.

## Prior pin change and remaining review context

The existing commit `1912c0472635ea174f1a2e2de2f3c96d09f55e9b` advances the processor from `990f9652` to `0922e434`.
Processor PR 118 records the October MVU waiver and unsupported-command response checks, including the locked case.
Processor PR 119 adds the integration parameter inventory and its checker.
The parent commit updates the pin references, adoption notes, changelog, diagram master and renders, and PNG manifest.
The processor HDL and parent RTL are unchanged across the pin adoption.
Round 1 validation remains public on [the prior handoff](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845135353); those broader checks were not repeated in this ledger-only round.

Inherited prose at `CHANGELOG.md:44` and `docs/reference/SUBMODULES.md:53,57` still describes an unchanged ledger and an unresolved acceptance decision. Those statements are superseded by the public Round 2 decision and this commit. They were left untouched because the assignment explicitly requires the ledger-only delta. Independent review must account for this documentation consistency gap; this handoff does not claim full issue completion.

No push, PR creation or edit, merge, other checkout, delegation, or hardware action was performed.
`PR-BODY.md` is a prepared artifact only.
