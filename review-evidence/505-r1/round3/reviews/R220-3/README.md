# R220-3 receipts - PR #505 / issue #407, exact head 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7

Review clone: `$VALIDATION_STORAGE/reviews/r220-505-r3`, detached at the head above.
Scratch: disposable `git archive` copies and a sparse clone of the public
`505-review-evidence` branch under `/tmp/r220-3-scratch`, removed at exit.
Every Python command ran with `-B` and `PYTHONDONTWRITEBYTECODE=1`.
Shell commands ran through `rtk` (the `rtk proxy` form where raw output was needed).

## Layout

| Path | Content |
|---|---|
| `REPORT.md` | The review report (first line is the verdict). |
| `logs/00-entry-state.log` | Entry state: HEAD, tree, parents, clean status, `git ls-files -s` hash, submodules, `git diff --raw` from ad624931 and from base. |
| `logs/01-ci-events-check-head.log` | `python3 -B scripts/ci_events.py --check` at the head. |
| `logs/02-ci-events-selftest-head.log` | `python3 -B scripts/ci_events.py --selftest` at the head. |
| `logs/03-doc-gates-head.log` | docs_check, check_em_dash (base b17580b9, base ad624931, selftest), gen_toc (selftest, verify-anchors, check), check_doc_paths, check_doc_style (+selftest), check_feature_status (+self-test), traceability matrix, check_archive (+selftest), check_baremetal_only (check, selftest), DOC_MAP, `git diff --check` from b17580b9 and from ad624931. |
| `logs/04-docs-check-no-git.log` | The `docs-check-no-git` body on a `.git`-less archive copy of the head. |
| `logs/05-ci-scope.log` | `ci_scope.py` answer for the PR's changed-file set. |
| `logs/p1-content-gap-census.{json,log}` | Probe p1 at the head: content levers on every `run:` step of the four workflow files through the tree's own `check()`. |
| `logs/p1b-content-gap-census-base.{json,log}` | The same probe at base b17580b9 (detection control). |
| `logs/p2-cli-sha-pin-edits.log` | Probe p2: the F3 edits and one carrier control through the real `--check` CLI on archive copies of the head. |
| `logs/p3-ac5-diagnostic-identity.log` | Probe p3: the head's diagnostic for the AC5 edit versus the archived act receipt lines; the published AC5 verifier; PR #506 state. |
| `logs/p4-checker-ast-delta.log` | Probe p4: `ci_events.py` AST delta 6af65a15 to head and ad624931 to head, with reachability from `check()`. |
| `logs/p5-f1-f2-nonregression.log` | Probe p5 output: carrier arm composition at the head, the AC5 arm, docs-check steps 41-43 records, `git grep "pinned yet"`. |
| `logs/p6-residue-claims-grep.log` | `git grep` for residue/tracker claims at the head and at base. |
| `logs/98-integrity-pre-report.log`, `logs/99-exit-integrity.log` | Clone integrity before writing the report and at exit (probe p9). |
| `probes/` | p1-p6 and p9 sources. The p3, p5 and p6 logs record their exact command on their first line. |
| `receipts/` | Public-state snapshots: issue #407 and #439 bodies and comments, PR #505 view and comments (entry and final), PR reviews, hosted check runs at the head, remote refs, and `public-evidence-blobs.txt` (blob ids and re-hash result of every archived evidence file read). |

## Reproduce

```sh
C=$VALIDATION_STORAGE/reviews/r220-505-r3; H=5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7
S=$(mktemp -d); mkdir -p "$S/head" "$S/base" "$S/p2"
git -C "$C" archive "$H" | tar -x -C "$S/head"
git -C "$C" archive b17580b91deb11f3441dfc5d7f9fafe539d929b8 | tar -x -C "$S/base"
python3 -B probes/p1_content_gap_census.py --root "$S/head" --out p1.json
python3 -B probes/p1_content_gap_census.py --root "$S/base" --out p1b.json
bash probes/p2_cli_sha_pin_edits.sh "$C" "$H" "$S/p2"
python3 -B probes/p4_checker_ast_delta.py "$C" 6af65a151663e1301f1983a6c9d22650a0b35da9 "$H"
python3 -B probes/p4_checker_ast_delta.py "$C" ad62493186576144f9fa1568babad012bc9ad8ca "$H"
python3 -B probes/p5_f1_f2_nonregression.py "$S/head"
bash probes/p6_residue_claims_grep.sh "$C"
git clone --filter=blob:none --no-checkout --branch 505-review-evidence \
  https://github.com/kebag-logic/milan-fpga.git "$S/evidence"
git -C "$S/evidence" sparse-checkout set review-evidence/505-r1
git -C "$S/evidence" checkout 11bc477524657ae0863f1b014c995904fc377471
bash probes/p3_ac5_identity.sh "$S/evidence" "$S/p2" "$C"
bash probes/p9_integrity.sh "$C" "$H"
```

p3 compares the `FAIL` line of p2's `c1-carrier-or-true` run with
`ac5-act/01.log:1902` and `ac5-act/02.log:37` of the public evidence branch,
then runs `python3 -B ac5/verify_receipts.py <archive-root>`.
