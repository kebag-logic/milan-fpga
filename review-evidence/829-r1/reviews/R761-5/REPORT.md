[R761] POSITIVE - exact head 4871df3f6eed1cbc5a399e18372b60a04cb32387

# R761-5: composition review of issue #829 / PR #831, merge-train candidate

Candidate `4871df3f6eed1cbc5a399e18372b60a04cb32387`, tree `2b2118dfc57f2625850838e13ca25c63d7196fd7`.
Parents: live dev `503bc97cd4f24ad07596c17e7188f2024617972d` and PR head `b9628c8963d436af0dccebb205a5241ece5d9e93`.
Scope: composition acceptance only. The PR source head already carries two independent POSITIVE source reviews, R761-4 and R762-4, both at `b9628c89`.

## Verdict basis

The composed tree introduces no defect beyond the reviewed sources.

- **The candidate is a pure merge.** Recomputing the merge of dev `503bc97c` with head `b9628c89` gives tree `2b2118df`, the candidate's own tree. No conflict was resolved and nothing else was edited (`receipts/composition-check.log`).
- **One predecessor.** The PR's base is `1f29f189`. Since then dev's first-parent line has gained one merge: PR #828 (#640, Mark II charter). It changes 23 files, all Markdown docs, and no code, test, workflow, registry or submodule.
- **Two files are changed by both:** `REQUIREMENTS.md` and `docs/design/GPTP_PLANE.md`. Their hunks are disjoint:
  - In `REQUIREMENTS.md`, #828 rewrites the ownership text in sections 1, 4 and 7. The PR adds the MII figure to the egress scope note, now at `REQUIREMENTS.md:207-208`.
  - In `GPTP_PLANE.md`, #828 rewrites lines 6-7. The PR changes the delay formula and adds `### The 100 Mb/s MII shape` at `GPTP_PLANE.md:275-377`.
- **No semantic conflict.** #828 limits fabric gPTP ownership to "until F6". It also states that "the PHC and timestamps stay in fabric, on both ports" in both regimes (`REQUIREMENTS.md:156-159`, `GPTP_PLANE.md:6-7`). The PR changes only timestamp and egress-correction RTL and the matching docs, which stay in fabric before and after F6. None of the PR's added lines makes an ownership or placement claim that #828 has since qualified (`receipts/independent-pass-before-prior-findings.md`).
- **#828's area rows for modules this PR changes are not falsified.** #828 adds measured rows for `KL_gptp_gmii_launch` (192 LUT), `u_txret` (218) and `u_gptp_shadow` (5,194) at `docs/design/MARK_II_AREA_PLAN.md:112,117,175`. These are dated measurements pinned to source commit `40b77bbd`, which is not on dev (`MARK_II_AREA_PLAN.md:77-80`). The PR's GMII-shape change gates the observer on `gmii_tready_i`. That does not falsify a dated measurement, and no gate reads those figures.
- **Cross-references hold.**
  - The PR's added lines cite no requirement ID, and #828 removes no requirement ID.
  - The PR's only new cross-page anchor, `GPTP_PLANE.md#the-100-mbs-mii-shape` from `tb/verilator/gptp_txts/README.md:70`, resolves.
  - The code that names the two shared docs is `test_builder.py:28483`, `gptp_txts/sim_main.cpp:77`, `milan_dp/sim_gptp.cpp:102`, `check_tap_purity.sh:83`, `torture_campaign.py:3213` and `DOC_MAP.gen.py:114`. All of these are comments or labels; none parses the doc contents.
  - Builder gate labels `1g` and `1h` are unique in `test_builder.py`.

## Gates run on the candidate

These are the gates that read the files both PRs change: docs, TOC/anchors, em-dash, the gPTP doc gate, style, paths, CI-event contract, source lists. Every one exits 0 (`receipts/gates-summary.txt`, with one `.log` and `.rc` per gate).

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings, 213 md + 1438 text files |
| `scripts/gen_toc.py --check` | OK, 152 pages |
| `scripts/gen_toc.py --verify-anchors` | 582 cross-page fragment links reproduced |
| `scripts/check_em_dash.py --base 503bc97c` (the candidate's parent) | 0 findings over 149 added lines in 6 pages |
| `scripts/check_em_dash.py --base 1f29f189` (the PR's base) | 0 findings over 2064 added lines in 27 pages |
| `scripts/check_em_dash.py --selftest` | PASS, 339 arms |
| `scripts/check_gptp_docs.py` | OK, 8 pages |
| `scripts/check_doc_style.py` / `check_doc_paths.py` / `check_hygiene.py` | OK / OK, 1085 paths / 0 |
| `scripts/ci_events.py --check` / `--selftest` | OK, 2199 items / PASS, 5258 arms |
| `scripts/check_solution_docs.py` / `check_feature_status.py` | OK / 0 findings |
| `scripts/check_rtl_source_lists.py` / `check_soc_sources.py` | OK, 112-file closure, 4/4 lists / OK, 46 modules |

The Markdown renderer these gates need was installed into a disposable venv, from `tools/markdown/requirements.txt` with `--require-hashes`. `ci_events.py` imports a sibling module, so it was run without isolated mode, as CI runs it.

## Signed local CI packet

This is `review-evidence/829-r1/local-ci/b9628c89` at `e3b459be` (`receipts/packet-verify.txt`, `receipts/composition-check.log`, `tools/composition_check.sh`).

1. **Signer key.** `allowed_signers` holds exactly one key, principal `milan-local-ci`, ED25519 fingerprint `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`. That is the required key.
2. **Signature.** `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` reports a Good signature and exits 0. The `manifest.json` sha256 is `4f0c72cc9e1bdd58671d1ef70c4f4d0aa188383e95c16cd43538abdfeffac193`, as stated.
3. **Subject.**
   - Candidate `4871df3f6e…` with parent `503bc97c` and tree `2b2118df`, all matching.
   - Head `b9628c89…` with tree `a829a5d0`, which matches `git rev-parse b9628c896^{tree}`.
   - The act runner is at `503bc97c`, live dev. Result: `success`.
4. **Coverage.** All 47 coverage entries are `ok: true`:
   - 46 by act. Every act job they name, including the 19 Verilator and 4 Yosys shards, is `success`.
   - 1 `not-run`: `rtl/physical-gptp`. Its reason is that it runs only on schedule or manual dispatch, so act shows it skipped. Its act status is `skipped`.
   - Act's exit code is 0. Banks `full-native` (5 commands) and `manager-builder` (48 commands) all exit 0.
5. **Workflow definitions.** All four workflow sha256 values recorded for the candidate and the head match `.github/workflows/{docs,elaborate,rtl-fast,rtl}.yml` at both commits.

## Findings

**No BLOCKER, MAJOR or MINOR.** The composition adds no new finding.

### Residue carried from the source reviews (wording only; no effect on the verdict or any lens)

The candidate merge adds no source comment, so it adds no comment-rule residue. Each residue below is still open at this head. Its bytes are unchanged; only line numbers shifted where #828 edited the same file.

| ID | Lenses | Path at candidate | Defect | Exact fix |
|---|---|---|---|---|
| R761-4-RES1 = R762-4-R1 | Docs | `sw/builder/test_builder.py:18313-18314` (blob `71aed6cf`, identical to `b9628c89`) | "The gate's keeps fail if no earlier source defines it any more" names only the keeps. With the macro gone, a cut control fails first. | The two source rounds gave different fixes. Take one: "The gate's controls fail if no earlier source defines it any more." This is accurate whichever control trips first. |
| R762-3-R1 = R761-3 RES1 | Docs | `README.md:287`, also `:229` and `:258` (they were `:281`, `:223` and `:252` at `b9628c89`; #828's hunk at line 56 adds 6 lines) | The builder gates row says `python3 + pyyaml`. Line 258 calls the repo gates "pure Python, seconds". Gates 1g and 1h need the pinned `sv2v` front end. | `:287` becomes `python3 + pyyaml + the pinned sv2v (gates 1g, 1h)`. `:258` becomes `# 4 · run the repo gates (the lint one wants verilator; the builder gates want sv2v)`. `:229`'s "why" cell adds "; the builder's gates 1g and 1h read the datapath through it". The fix already stated at R762-3 also suffices. |
| R761-3 RES2 | Docs | `syn/ooc/dp_srcs.py:70` (blob `ceb94845`, identical) | "Used by" omits gate 1h. | `Used by syn/ooc/milan_datapath_ooc.tcl, syn/ooc/pp_shadow_ooc.tcl and sw/builder/test_builder.py (gate 1h).` |

### Suggestions (no effect on coverage)

- **R761-5-S1, Docs, `README.md`.** This is the one carried residue file that #828 also edits. Fixing the README residue above in the PR that next edits `README.md` would stop its line references from drifting again.
- **Carried unchanged:**
  - R761-4 S1 (four workers for gate 1h) and S2 (hosted cost in the PR body).
  - R762-4-S1 (`elaborate-gates-1` above its projected bound, `docs/testing/CI_WORKFLOWS.md:3079`; blob `617dc60a`, identical at the candidate).
  - R762-3-S1 and R762-3-S2 (`.github/ci-templates/docs.yml:164-166`, blob `3f4938d5`, identical).
  - R761-3 S1, S2 and the remaining S3 cases.
  - The R761-2 / R762-2 / R761 / R762 suggestions that are tracked for their own Issues.

## Prior public findings at this head

I read these after writing `receipts/independent-pass-before-prior-findings.md`. My sources were R761-4 and R762-4 at `e3b459be`, `review-evidence/829-r1/reviews/`.

| Finding | Disposition at `4871df3f` | Evidence |
|---|---|---|
| R762-3-F1 (MINOR, Tests, Docs) and the macro case of R761-3 S3 | **Stay closed** | `test_builder.py` blob `71aed6cf` is identical at the head and the candidate; #828 touches no code |
| R761-4-RES1 / R762-4-R1 | **Retained, residue** | Above |
| R762-3-R1 / R761-3 RES1 | **Retained, residue**, lines shifted +6 | Above |
| R761-3 RES2 | **Retained, residue** | Above |
| All the suggestions listed above | **Retained, suggestions** | Their artifacts are blob-identical at the candidate, apart from `README.md` |
| R761-1 F1-F7, R762-1 F1-F8 and R1-R4, R761-2 F1, R762-F9, R762-F4 | **Stay closed** | The composition touches none of their artifacts |

## Lens results

| Lens | Does the composition touch its scope? | Result |
|---|---|---|
| Conformance | **Yes.** It composes normative text in `REQUIREMENTS.md` | PASS. #828's ownership clauses (`REQUIREMENTS.md:156-159`, sections 1 and 7) and the PR's egress scope note (`:207-208`) are consistent: timestamps are fabric-retained in both regimes. #829's acceptance is unaffected because no code changed. |
| RTL | **No.** The predecessor has no `hdl/`, `syn/` or `sw/` change; the merge is pure | PASS by the source reviews. `hdl/` blobs are identical to `b9628c89`. #828's dated area rows on these modules are checked above. |
| Robustness | **No** | PASS by the source reviews. No code path or configuration changed. |
| Tests | **No test changed.** Readers of the shared docs were checked | PASS. Code that names the two shared docs only does so in comments. The signed act and bank runs on the candidate all succeed. |
| Docs | **Yes.** It touches `GPTP_PLANE.md`, `REQUIREMENTS.md`, the README line shift, TOC and anchors | PASS. The 16 gates above are green. The MII section and #828's "until F6" header are coherent. The only drift is the residue line shift. |

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REQUIREMENTS.md:156-159,207-208`; `GPTP_PLANE.md:6-7,275-377`; #828 diff `1f29f189..503bc97c`; `receipts/independent-pass-before-prior-findings.md` | R761-5 (composition); R761-4 and R762-4 (source) | `4871df3f6eed1cbc5a399e18372b60a04cb32387` |
| RTL | CLEAN | Merge-tree identity in `receipts/composition-check.log`; predecessor file list (docs only); `MARK_II_AREA_PLAN.md:77-80,112,117,175` | R761-4 and R762-4 at `b9628c89`, an ancestor whose RTL scope nothing has touched since; R761-5 confirms the composition | `b9628c8963d436af0dccebb205a5241ece5d9e93` (source), `4871df3f6eed1cbc5a399e18372b60a04cb32387` (composition) |
| Robustness | CLEAN | As for RTL; no code delta in the composition | R761-4 and R762-4; R761-5 confirms the composition | `b9628c8963d436af0dccebb205a5241ece5d9e93` (source), `4871df3f6eed1cbc5a399e18372b60a04cb32387` (composition) |
| Tests | CLEAN | Signed manifest coverage, 47/47 ok (`receipts/composition-check.log`); readers of the shared docs; `test_builder.py` blob identity; gate labels 1g/1h | R761-5 (composition); R761-4 and R762-4 (source) | `4871df3f6eed1cbc5a399e18372b60a04cb32387` |
| Docs | CLEAN, 3 residues carried | `receipts/gates-summary.txt` and the per-gate logs; `GPTP_PLANE.md:275`; `tb/verilator/gptp_txts/README.md:70`; `README.md:229,258,287`; `test_builder.py:18313-18314`; `syn/ooc/dp_srcs.py:70` | R761-5 | `4871df3f6eed1cbc5a399e18372b60a04cb32387` |

## Real limits

- No simulation, synthesis or builder bank was rerun here. The composition changes no code, and the signed packet covers execution. I verified the packet's signature, subject, coverage and workflow hashes; I did not re-execute it.
- `rtl/physical-gptp` is not run (schedule-only job). Physical calibration has NOT been run; field skips are not hardware proof. 100 Mb/s physical calibration stays open under #583.
- I did not inspect the hosted runs at the exact head. Hosted and act acceptance belong to the manager.
- #828's area figures are measurements at `40b77bbd`. Whether the PR's observer gate moves the GMII-shape LUT count is not measured here. No claim in the tree depends on that.

## Pending manager duties

- Rebuild the current-dev merge candidate at the merge turn if dev moves past `503bc97c`. This verdict covers tree `2b2118df` only.
- Publish the builder and native bank receipts for the final candidate on the PR.
- Carry the three residues above to the residue checklist.
- Hosted exact-head contexts on the final candidate.

## Restore check

The clone was never modified. HEAD and tree are `4871df3f…`/`2b2118df`; `git status --porcelain` is empty; the index and worktree match HEAD. Six submodule gitlinks are recorded; the five initialized ones are checked out at their gitlink, and `external` is uninitialized (`receipts/restore-verify.txt`).

R761-5 FINISHED
