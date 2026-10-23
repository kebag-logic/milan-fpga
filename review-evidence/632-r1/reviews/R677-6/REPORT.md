[R677] POSITIVE - exact head cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e

Round R677-6: the internal independent re-review of kebag-logic/milan-fpga PR #770 (#632, #764). The head is `cf1ca875` with tree `e4d84bf05d153298aeec0b15dc887aa16efef744`, one documentation commit on `24a292a0`. R677-5 reviewed `24a292a0` and was NEGATIVE with one MINOR, R677-5-F1.

R677-5-F1 is resolved at its cause. The delta changes one paragraph of one Markdown page and nothing else. All five lenses are CLEAN at this head. There is no open BLOCKER, MAJOR or MINOR. One RESIDUE in the PR body and one SUGGESTION are recorded below.

This is a source-review verdict. It is not merge authorization, it is not hosted or act acceptance, and it is not hardware proof.

## Scope and independence

- **Order of reading.** I read AGENTS.md, and the round-5 public record for the scope. Then the delta: `git diff 24a292a0..cf1ca875`, shown in full in `receipts/delta.diff`. Then the 2011, Cor1-2013, Cor2-2015, 2020 and Milan v1.2 texts. Then the pinned engine source. Only after my own pass did I read the PR body, FPGA-gPTP #87, the manager's fix note (issuecomment-6372658718) and the round-5 reports.
- **What I did not read.** No private author material, lane scratchpad or management directory, and no round-6 report from another reviewer.
- **Prior coverage that carries over.** My R677-5 coverage at `24a292a0` applies unchanged to every file other than `docs/reference/REGISTER_MAP.md`. The delta touches no other file (check 1).

## Check 1: the delta is confined to one paragraph

`receipts/delta_checks.txt` and `receipts/delta.diff`:

- `git diff --name-only 24a292a0 cf1ca875` lists one file, `docs/reference/REGISTER_MAP.md`, blob `49712714` -> `e6232070`, mode 100644 unchanged.
- The hunk is `@@ -1470,9 +1470,14 @@`, inside the 0x7DC section: 8 lines added, 3 removed, all of them prose.
- `git diff --stat` over `hdl syn configs tb scripts sw avdecc .github Makefile*` and every submodule path is empty.
- All six gitlinks are identical at `24a292a0` and `cf1ca875`: external `efeb541a`, gptp-processor `55680bff`, protocol-processor `93fb0b2d`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`.
- The commit message is one line with no trailers.
- The added lines contain no lane label, review round, reviewer ID or issue-comment ID.

No executable line and no gitlink changed.

## Check 2: R677-5-F1's required outcome, clause by clause

The paragraph is `docs/reference/REGISTER_MAP.md:1470-1480`. I checked it against the local texts, with SHA-256 sums and extract line numbers in `receipts/clause_lookup.txt`.

| Required outcome | Text at head | Lookup | Met |
|---|---|---|---|
| 1. Attribute the empty publication to 2020 10.3.11.2.1 d) together with 10.3.13.2.4 f) 5), labelled 2020 | `:1475-1477`: "That is the IEEE 802.1AS-2020 rule: 10.3.11.2.1 d) empties the port's receivedPathTrace, and 10.3.13.2.4 f) 5) copies it to pathTrace, appending thisClock only when it is not empty." | 2020 10.3.11.2.1 d): with no TLV, receivedPathTrace "is set to the empty array". 10.3.13.2.4 f) 5): on the SlavePort, receivedPathTrace "is copied to ... pathTrace, and, if it is not empty, thisClock is appended". The paragraph now gives each clause its own role: d) writes receivedPathTrace, not pathTrace, which was the defect in F1 | yes |
| 2. State that 2011 has no such rule and pathTrace keeps its previous value (10.3.10.2.1 d), 10.3.12.1.1), so the publication departs from the adopted edition | `:1477-1479`: "IEEE 802.1AS-2011 has no such rule: without a TLV, pathTrace keeps its previous value (10.3.10.2.1 d), 10.3.12.1.1). So the count-zero publication departs from the edition Milan v1.2 profiles." | 2011 10.3.10.2.1 d) writes pathTrace only when a TLV is present on a SlavePort. 10.3.12.1.1 sets it to {thisClock}. 10.3.12.1.4 i) applies only when this system is the grandmaster. No other clause writes pathTrace. Cor1-2013 restates 10.3.12.1.4 and does not change 10.3.10.2.1. Cor2-2015 changes only 11.2.15. Milan v1.2's normative [802.1AS] is 2011 with Cor1-2013 and Cor2-2015 | yes |
| 3. Link the public Issue that holds the gPTP owner's decision | `:1479-1480`: "The decision is open in FPGA-gPTP #87." | Mister-M-alt/FPGA-gPTP#87 is OPEN (`receipts/fpga-gptp-87.json`). Its title and body give the same two-edition analysis and ask the gPTP owner to decide. The reference form matches the page's other FPGA-gPTP references (#82 `:1051`, #85 `:1483`, #86 `:1489`) | yes |
| 4. No engine change | the gitlink is unchanged | `gptp-processor` is `55680bff` on both commits. In `hdl/top/KL_gptp_engine.sv:714-730` and `:976-981`, `path_append_w` is 0 when the received count is 0, so `pub_path_count_r` is 0. That is the count-zero behaviour the paragraph describes | yes |

The finding's verification steps all pass:

- `git grep -n '802.1AS-2020' docs/reference/REGISTER_MAP.md` returns only `:1475`, the labelled statement.
- The PR-wide added-line scan (`git diff -U0 e26f1816 cf1ca875`, excluding `docs/history`) still finds exactly one 802.1AS-2020 citation, this one (`receipts/added_line_scan_2020.txt`).
- The docs gates pass at the exact head (`receipts/gates/`):
  - rc 0: `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py` and its `--selftest`, `check_gptp_docs.py` and its `--with-submodule` run, and `check_submodule_docs.py`.
  - `check_em_dash.py --base e26f1816`: 0 findings over 1956 added lines.
  - `gen_toc.py --verify-anchors` (536 links) and `--check`: OK. Both ran on a venv whose `pip freeze` matches `tools/markdown/requirements.txt` exactly (`md-venv-freeze.txt`). The first attempt on the system interpreter stopped with rc 2 because the renderer was missing. That is an environment failure, not a gate result, and it is kept in `summary.txt`.

## Check 3: the PR body against the paragraph

`receipts/pr770_body_excerpts.txt`:

- The open question names FPGA-gPTP #87 ("Open question (published as FPGA-gPTP #87, not decided here)").
- The limits list names it too ("The decision is open in FPGA-gPTP #87 (R677-5-F1); this PR changes no engine behaviour").
- Both state the 2020 rule as 10.3.11.2.1 d) with 10.3.13.2.4 f) 5), and say 2011 keeps the previous value (10.3.12.1.1). The clause table maps 2020 10.3.11.2.1 d) to "no counterpart" in 2011.

No claim in the body contradicts the paragraph. The fix table and the evidence statements stop at `24a292a0`, which is R677-6-R1 below.

## Prior findings at this head

| Finding | Disposition at `cf1ca875` |
|---|---|
| R677-5-F1, MINOR, Conformance and Docs | **Resolved at cause.** All four required outcomes are met (check 2). The verification grep, the scan and the gates pass |
| R677-5-R1, RESIDUE, Docs | **Retained.** `tb/verilator/milan_dp/dynmap_mutants.py:29` and `:35` still carry the round labels. The file is unchanged by the delta, the lines come from dev, and #746 tracks them. It is not new residue |
| R678-5-S1, SUGGESTION, Tests and Docs (the dynmap campaign's fresh-clone prerequisite) | **Retained, optional.** The delta does not touch it |
| R677-4-S1 to S5, and the optional items carried in R678-4 | **Retained, optional.** Outside the delta. R678-5 recorded their dispositions and nothing here changes them |
| Every earlier BLOCKER, MAJOR and MINOR on this PR | **Unchanged.** Resolved at `24a292a0` per R677-5 and R678-5, and nothing in their scope changed since |

## Findings this round

### R677-6-R1 - RESIDUE - Docs - the PR body's fix record and evidence head stop at `24a292a0`

- **Where:** the PR #770 body.
  - The fix table runs to item 5 (`24a292a0`). There is no row for R677-5-F1 at `cf1ca875`.
  - The lead paragraph is headed "Round 8 at `24a292a0`".
  - The verification checklist reads "round 8 at `24a292a0`".
  - Item "4, the neighbour at `REGISTER_MAP.md:1471`" still says the page "names that as the rule IEEE 802.1AS-2020 10.3.11.2.1 d) states". That is the `546412d8` wording, now superseded.
- **Evidence:** `receipts/pr770_body_excerpts.txt`. The fix and its gates are recorded in the manager's PR comment (issuecomment-6372658718). No statement in the body is false for the head it names.
- **Impact:** A cold reader of the body alone does not see the head or the fix for the last round. No measurement, verdict, clause claim or code is affected. It is wording only.
- **Exact fix:**
  - Add a row: "6. R677-5-F1 | `cf1ca875` | `REGISTER_MAP.md:1470-1480` attributes the count-zero publication to IEEE 802.1AS-2020 10.3.11.2.1 d) with 10.3.13.2.4 f) 5), states that 2011 keeps the previous pathTrace (10.3.10.2.1 d), 10.3.12.1.1), so the publication departs from the adopted edition, and links FPGA-gPTP #87; the docs gates pass at `cf1ca875`".
  - Append "(superseded at `cf1ca875`, item 6)" to the item-4 neighbour row.
  - Name `cf1ca875` in the lead paragraph and the checklist as a one-page documentation commit on `24a292a0`.

### R677-6-S1 - SUGGESTION - Conformance, Docs - also name the own-grandmaster writer of the 2011 previous value

- **Where:** `docs/reference/REGISTER_MAP.md:1478`, "(10.3.10.2.1 d), 10.3.12.1.1)".
- **Evidence:** In 2011, {thisClock} can come from 10.3.12.1.1 or from 10.3.12.1.4 i). FPGA-gPTP #87 names both. The sentence is correct as written, and the page cites 10.3.12.1.4 i) two lines later, at `:1485`.
- **Optional outcome:** "(10.3.10.2.1 d); initial value from 10.3.12.1.1 or 10.3.12.1.4 i))". This does not affect the verdict or any lens.

## Applied-lens evidence

```text
[R677] PASS Conformance - docs/reference/REGISTER_MAP.md:1470-1480; receipts/clause_lookup.txt - each cited clause read in 802.1AS-2020 (10.3.11.2.1 d), 10.3.13.2.4 f) 5)), 802.1AS-2011 (10.3.8.21, 10.3.10.2.1 d), 10.3.12.1.1, 10.3.12.1.4 i)), Cor1-2013, Cor2-2015 and Milan v1.2 normative references; engine KL_gptp_engine.sv:714-730,:976-981 at gitlink 55680bff publishes count zero as stated; FPGA-gPTP #87 open with the same analysis
[R677] PASS RTL - receipts/delta_checks.txt - git diff --stat 24a292a0..cf1ca875 over hdl, syn, configs and all submodule paths is empty and every gitlink is unchanged; R677-5's RTL verdict at 24a292a0 covers an RTL tree identical to this head's
[R677] PASS Robustness - receipts/delta_checks.txt, receipts/delta.diff - the only changed blob is a Markdown page; no input-handling, reset, timeout or configuration path changed; R677-5's verdict at 24a292a0 carries over
[R677] PASS Tests - receipts/delta_checks.txt, receipts/gates/summary.txt - no test, harness or campaign file changed (tb and scripts diff empty); the gates that cover the changed page pass at the exact head; R677-5's executed legs at 24a292a0 cover a test and RTL tree identical to this head's
[R677] PASS Docs - docs/reference/REGISTER_MAP.md:1470-1480; receipts/gates/ (docs_check, check_doc_paths, check_doc_style +selftest, check_gptp_docs +--with-submodule, check_submodule_docs, check_em_dash --base e26f1816, gen_toc --verify-anchors/--check all rc 0); receipts/added_line_scan_2020.txt; receipts/pr770_body_excerpts.txt - R677-5-F1 resolved; PR body consistent; R677-6-R1 is RESIDUE (wording) and does not leave the lens unclean
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REGISTER_MAP.md:1470-1480`; the 802.1AS-2011, Cor1-2013, Cor2-2015 and 2020 texts and the Milan v1.2 normative references; `KL_gptp_engine.sv:714-730,976-981` @ `55680bff`; FPGA-gPTP #87. Other files carried from R677-5 | R677-6 | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| RTL | CLEAN | the delta's empty RTL scope and unchanged gitlinks; RTL tree identical to the one R677-5 covered | R677-6 (delta), basis R677-5 @ `24a292a0`, which nothing in scope touched since | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| Robustness | CLEAN | the delta (one Markdown blob); input, reset and timeout paths identical to those R677-5 covered | R677-6 (delta), basis R677-5 @ `24a292a0` | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| Tests | CLEAN | the delta's empty tb and scripts scope; docs gates at head; R677-5 executed evidence on an identical test and RTL tree | R677-6 (delta), basis R677-5 @ `24a292a0` | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| Docs | CLEAN (RESIDUE R677-6-R1 and SUGGESTION R677-6-S1 recorded) | `REGISTER_MAP.md:1470-1480`; docs gates at head; PR body excerpts; added-line scan | R677-6 | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |

## Real limits

- **No source bank at this head.** I ran no simulation, lint, Yosys, builder or campaign. The delta is one Markdown paragraph. Source-head execution evidence is the author's published receipts at `24a292a0`, and R677-5 reviewed those against an identical executable tree.
- **No published receipt for the manager's gates at `cf1ca875`.** The fix note (issuecomment-6372658718) says the gates pass. The evidence tree at `2e4361bf` has no receipt for `cf1ca875`: its `author-r8b/receipts/docs-gates/HEAD.txt` names `f1fda3f1`. My own runs in `receipts/gates/` reproduce the claim at the exact head. They are reviewer evidence, not the author's receipt.
- **Hosted checks.** Sampled at 2026-10-23T19:13:40Z (`receipts/hosted_checks_cf1ca875.txt`).
  - 8 completed with success: bdd-conformance, changes, docs-check-no-git, firmware-aecp-mutants, full-ci-gate, Prepare pinned Yosys, verilator-lint and wire-accountability.
  - 1 skipped: Physical gPTP, which runs nightly and manually only.
  - 36 were queued or in progress, so they are not evidence.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. The #764 bench method is a post-merge item.
- **Standards copies.** The clause texts are local licensed copies and are not redistributed. The receipt gives their hashes and extract line numbers. The file named `802.1AS-Cor1_2013.pdf` is not the corrigendum (it uses 2020 numbering), so I did not use it as a 2011 authority.
- **Clone integrity** (`receipts/clone_integrity.txt`). After the run the clone is at `cf1ca875`, tree `e4d84bf0`. The worktree and index equal HEAD, and all 1447 index entries match the HEAD tree in mode and blob. The REGISTER_MAP blob is `e6232070`, the submodules are at their gitlinks and clean, and the `scripts/__pycache__` my gate run created has been removed.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `e26f1816`, live dev `e5b480a385841f19420570bbba7c46da101d1303`) with the builder and native banks, and link the receipts on the PR.
- Accept the hosted and act runs at the exact head or at the candidate. 36 hosted contexts were still pending when I sampled.
- Publish the docs-gate receipts for `cf1ca875`, or cite this packet's receipts.
- Carry R677-6-R1 and R677-5-R1 (#746) to the residue checklist.
- Track the gPTP owner's decision in FPGA-gPTP #87.
- Get explicit maintainer authorization before any merge.

R677-6 FINISHED
