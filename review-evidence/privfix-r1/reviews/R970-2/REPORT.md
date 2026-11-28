[R970] POSITIVE - exact head 0715cb206050c49a1745dd2d11e2fc0e1b74116b

# R970-2 external independent review: issue #1028 / PR #1029

- Head `0715cb206050c49a1745dd2d11e2fc0e1b74116b`, tree `14cac930093a39ae1e96881d63f774ad3a322b0e`, one commit on base `c1c428433539c8a4ab6c007c6d85a98df33d9472` (`dev-soft-core`, still the live tip at observation).
- Delta: 21 files, 33 lines added and 33 removed. 8 documentation pages, 2 scripts under `scripts/`, 5 tools under `tb/tools/`, 6 behave files under `tests/`.
- Round: R970-2, cleared context, reconstructed from AGENTS.md, CONTRIBUTING.md (sections 2.2 and 6), the issue body, the PR body, the diff and the public packet `review-evidence/privfix-r1/author` at archive commit `8a80a864`.
- Verdict: no BLOCKER, MAJOR or MINOR. Three RESIDUE items and four SUGGESTIONS, all listed below for one pass.

## Scope decisions read

- Issue #1028 body is the only scope source. It carries no maintainer or manager comment at observation.
- Frozen acceptance: (1) no bench-specific name in the touched files; (2) no behaviour change, ELFs and generated outputs byte-identical, touched tools' self-tests pass; (3) docs checks pass; (4) a follow-up pins `gptp-processor`.
- This PR is the `dev-soft-core` leg. Bullets 1 to 3 are judged here. Bullet 4, the `dev` leg (PR #1030) and the FPGA-gPTP change are outside this head.

## Prior public findings

None exist. At observation PR #1029 had 0 reviews, 0 review comments and 4 conversation comments, all review-start notices. Nothing to resolve or retain.

## What was checked, and the result

### Check 1: no behaviour change

- **Structure of the 9 touched Python files is identical.** With string constants masked, the base and head syntax trees are equal for every file (`receipts/ast_delta.sanitized.txt`, script `scripts/ast_delta.py`).
- **Exactly 5 non-docstring strings differ**; the other 7 differing strings are docstrings. Each of the 5 was traced to its consumers:

| String | Location | Consumer | Effect |
|---|---|---|---|
| mock boundary gateway, now `192.0.2.1` | `scripts/act_ci.py:15368` | `scripts/act_ci.py:4897-4902` requires a valid IPv4 only; the arm's assertion at `:15394-15403` reads no gateway text | none on the arm's verdict |
| planted remote-shell line, now `root@192.0.2.2` | `scripts/check_baremetal_only.py:1137` | rule at `:214-215` matches up to `root@` and never reads the host | none; probe M1 below |
| `--tap` help text | `tb/tools/avtp_wire_truth.py:185` | printed help only | none |
| `human_action` plan text | `tb/tools/torture_campaign.py:2989` | rendered as `DO:` text; two checks compare its first 24 characters, which are unchanged | none |
| fixture label `capture-tap` | `tb/tools/torture_campaign.py:6783` | echoed into `detail["devices"]` at `:1229`; never compared | none |

- **No pool-membership check exists for the gateway.** `address_pool` is used only at `scripts/act_ci.py:737`, `:4183`, `:14110` and `:14136`. `192.0.2.1` is already this file's fixture convention (`:13754`, `:14474`, `:14477`).
- **The non-Python files change comments and one title only.** `tb/tools/check_tu_on_wire.sh:20` is a comment, and `bash -n` passes. The three feature files change one description line, one comment and one scenario title. The old title appears nowhere else in the tree.
- **No wire or file-format literal changed.** The 28-octet record header handling, the kept FCS and `--tap` are untouched code.
- **HDL and clause numbers are untouched.** No path under `hdl/`, `sw/`, `syn/`, `configs/`, `avdecc/`, `ci/`, `litex/` or `third_party/` changed, and no gitlink changed. `pw1_w` occurs 3 times under `hdl/` at base and at head. The 10.a.b.c clause citations in the touched files are unchanged (`receipts/restore_and_scope_check.txt`, `receipts/scan_touched_head.tsv`).
- **ELF byte identity rests on two things.** The author's base and head build manifests are the same file, sha256 `467bc57b...013bb9`, 7,302 rows: 149 RV32 ELFs, 1,489 host ELFs, 5,664 other outputs. Independently, no build-input tree reads a touched file: the only references are comments (`receipts/build_input_closure.tsv`). I did not rebuild.
- **Generated outputs are fresh at head, run by me:** `gen_toc.py --check`, `docs/DOC_MAP.gen.py --check`, `gen_register_reference.py --check` (203 registers), `docs_inventory.py --check`, `ci_gate_workflows.py --check`, `generate_ci_evidence_pins.py --check`.
- **Touched-tool self-tests pass at head, run by me:** `avtp_wire_truth.py --self-test` OK, `torture_campaign.py --self-test` OK, `check_baremetal_only.py --check` 0 findings over 1,970 files, `--selftest` 867 arms. Behave: the three touched features 231 scenarios, the whole suite 511 scenarios and 2,346 steps, 0 failed (`receipts/gates-head/`).
- **`act_ci.py --selftest` was not run by me**; this round may not run it. Its evidence is the author's receipt (`selftest: PASS` at base and head) plus the static trace above.

### Check 2: wording and docs rules

- **Each sentence keeps its meaning.** A word-level diff of the 8 pages shows only the name replacements and the dash changes. In `docs/history/v1/traceability/milan-v12.md:183` the 12 dash replacements all sit in the page's own prose, none inside the quoted specification text.
- **No U+2014 on any of the 33 added lines** (`receipts/added_lines_charset.txt`). `check_em_dash.py --base c1c42843` reports 0 findings over 15 added lines on 8 pages, arms 339/339.
- **Docs gates pass at head, run by me with the pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1):** `docs_check.py` 0 findings over 226 pages and 1,972 scrubbed files, `check_doc_style.py` and its self-test, `check_doc_paths.py`, `gen_toc.py --check` and `--verify-anchors`, `docs_inventory.py --check`, `check_feature_status.py`, `check_gptp_docs.py`, `check_solution_docs.py`, `check_submodule_docs.py`. The hygiene, idiom, naming, TODO, test-evidence and fail-fast ratchets pass too.
- **In total 31 of the author's 32 gates were rerun, all rc 0** (`receipts/gates-head/summary.tsv`). The one not rerun is `act_ci.py --selftest`.
- **Comment rule holds.** No added line shows a lane label, review round, reviewer identity or issue-comment identifier.
- Two wording points and one PR-body point are RESIDUE below.

### Check 3: scan of the touched files

- **Clean except the stated exceptions.** My own scanner (`scripts/scan_touched.py`) finds no tap product or vendor name, no bench host label, no switch label, no home path and no serial shape in the 21 files.
- **Private-range address shapes remaining: 16.** 8 are IEEE clause numbers. 2 are the act-slot pool pins (`scripts/act_ci.py:14124`, `:14415`), which is the stated false positive and matches the author's count of 2. 6 are the tool's own mock Docker gateways (`172.18.0.1`, `172.30.0.1`), not bench addresses.
- **Tree-wide,** the tap product name, the two host labels and the switch label have 0 occurrences outside the HDL net.

### Probe

- **M1, rule mutation.** I narrowed the remote-shell rule at `scripts/check_baremetal_only.py:215` so it no longer skips options. The self-test then fails with `[runtime-remote-root-shell-with-options-caught] planted defect not caught`, rc 2. So the arm whose fixture changed still fails for the defect it claims (`receipts/probe_M1_baremetal_rule_mutation.txt`). The file was restored and verified.

### Author packet

- All 27 manifest entries match their published sha256; none is unlisted or missing (`receipts/author_packet_manifest_verify.txt`).
- The author's gate table (32 gates, base and head, all rc 0) agrees with my reruns on every figure I can compare: 15 added lines on 8 pages, 339 arms, 226 pages, 867 arms, 231 and 511 scenarios.

## Findings

No BLOCKER, MAJOR or MINOR.

### RES-1, RESIDUE, Docs: the indefinite article generalises one device's record format

- Where: `tb/tools/avtp_wire_truth_wire.py:216-217`, `tb/tools/check_tu_on_wire.sh:20`.
- Evidence: the base text named one product and said it writes a 28-byte record header. The head says "An inline capture tap writes a 28-BYTE RECORD HEADER" and "Use an inline capture tap ... and pass --tap". That now reads as true of every inline tap, which it is not.
- Impact: wording only. A docstring and a shell comment; no code, test, figure or generated artifact changes. The `--tap` help states the 28-octet format itself, so the option stays correctly described.
- Exact fix: write "The bench's inline capture tap writes a 28-BYTE RECORD HEADER" in the docstring, and "Use the bench's inline capture tap for stream traffic and pass" in the comment.
- Verification: read the two lines; rerun `avtp_wire_truth.py --self-test` and `bash -n`.

### RES-2, RESIDUE, Docs: one unwrapped line

- Where: `docs/testing/TESTING.md:1199`.
- Evidence: the line is 96 characters in a paragraph wrapped under 78. The same replacement in `docs/testing/RUNNING_TESTS.md:232-233` was rewrapped.
- Impact: cosmetic; the page renders the same and no gate reads it.
- Exact fix: break line 1199 as "(the two inline capture taps) and the controller bench host (the controller" / "and audio endpoint):".
- Verification: `check_em_dash.py --base` and `gen_toc.py --check` stay green.

### RES-3, RESIDUE, Docs: the PR body says "Closes" for one leg of the issue

- Where: PR #1029 body, line "Closes #1028 (on `dev-soft-core`)".
- Evidence: the issue also covers `dev`, FPGA-gPTP and a pin follow-up. The repository's default branch is `dev`, so the keyword has no machine effect on this PR.
- Impact: wording only; a reader may take the issue as finished by this merge.
- Exact fix: "Part of #1028 (the `dev-soft-core` leg)".
- Verification: read the body.

### S-1, SUGGESTION, Tests and Robustness: nothing stops the names returning

- Where: `scripts/docs_check.py:148-160` and `:292-304`.
- Evidence: the identity and local rule tables hold no rule for the tap product, the two host labels or the switch label. CONTRIBUTING.md section 6 describes how to add one: an assembled token, a planted fixture, and the scrub in the same commit.
- Outcome: a follow-up issue adds the rules. The acceptance does not ask for it, so it is optional here.

### S-2, SUGGESTION, Docs: bench detail outside the issue's five categories

- Powerstrip outlet numbers stay at `tb/tools/torture_campaign.py:2993` and `:3066`, and `tests/features/torture_campaign_plan.feature:279`.
- The private test repository's directory name is spelled at `docs/history/v1/tests/CONFORMANCE_TESTING_HOWTO.md:101` (6 occurrences on the page) and `tb/tools/torture_campaign.py:22`. `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:123` uses a placeholder for the same repository.
- Neither is a name the issue lists. Outcome: a manager decision on whether they belong in a follow-up.

### S-3, SUGGESTION, Docs: a docstring cites a page that does not exist

- Where: `tb/tools/avtp_wire_truth_wire.py:219-220` cites `docs/findings/BENCH_TOPOLOGY.md`, which is absent at head.
- The line is untouched by this delta, so it belongs in a separate issue.

### S-4, SUGGESTION, Docs: one more stale CI-image digest, as disclosed

- Where: `ci/image/tool-inventory.json`, `command-table.json`, `exec-audit-receipt.json`.
- Evidence: the inventory has 378 inputs; 168 are stale at base and 169 at head. The one added is `scripts/check_baremetal_only.py`. No workflow under `.github/` references `ci/image` (`receipts/ci_image_inventory_staleness.txt`).
- The PR body discloses this. Outcome: refresh at the next image regeneration.

## Lens results

```text
[R970] PASS Conformance - issue #1028 acceptance bullets 1-3 against receipts/scan_touched_head.tsv, receipts/ast_delta.sanitized.txt, receipts/gates-head/summary.tsv - no listed name in the 21 files, 5 non-docstring strings traced to consumers with no verdict or format effect, clause numbers and wire/file-format literals unchanged
[R970] PASS RTL - receipts/restore_and_scope_check.txt - 0 changed paths under hdl/ sw/ syn/ configs/ avdecc/ ci/ litex/ third_party/, 0 gitlink changes, pw1_w 3 occurrences at base and head; the lens has no artifact in this delta
[R970] PASS Robustness - scripts/check_baremetal_only.py:1132-1140, tests/features/wire_truth_avtp.feature:274, tb/tools/torture_campaign.py:6781-6786 - the caught arm, its near-miss clean arm and the no-offset negative scenario keep their verdicts; probe M1 shows the changed arm still fails on its defect
[R970] PASS Tests - receipts/gates-head/ (avtp_wire_truth, torture_campaign, baremetal_selftest 867 arms, behave_touched 231 scenarios, behave_full 511 scenarios), scripts/act_ci.py:15346-15403 read statically - every touched tool's self-test passes or, for act_ci, is traced; no assertion reads a changed string
[R970] PASS Docs - the 8 changed pages by word-level diff, receipts/added_lines_charset.txt, receipts/gates-head/{docs_check,em_dash,toc_check,toc_anchors,doc_style,doc_paths,docs_inventory}.log, PR #1029 body - meaning kept, 0 U+2014 on added lines, PR body figures match; RES-1 to RES-3 are wording only
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #1028 acceptance; scan, syntax-tree and gate receipts; clause citations in touched files | R970-2 | `0715cb206050c49a1745dd2d11e2fc0e1b74116b` |
| RTL | CLEAN | diff path list (no HDL, firmware, synthesis or submodule path), gitlinks, `pw1_w` count | R970-2 | `0715cb206050c49a1745dd2d11e2fc0e1b74116b` |
| Robustness | CLEAN | `scripts/check_baremetal_only.py:1132-1140`, `tests/features/wire_truth_avtp.feature:274`, `tb/tools/torture_campaign.py:6781-6786`, probe M1 | R970-2 | `0715cb206050c49a1745dd2d11e2fc0e1b74116b` |
| Tests | CLEAN | 4 tool self-test runs, the 3 touched features and the full behave suite rerun; `scripts/act_ci.py:15346-15403`, `:4897-4902` read statically; author gate receipts | R970-2 | `0715cb206050c49a1745dd2d11e2fc0e1b74116b` |
| Docs | CLEAN | 8 changed pages, 17 docs and generated-output gates and 7 ratchets rerun, PR #1029 body, added-line character set | R970-2 | `0715cb206050c49a1745dd2d11e2fc0e1b74116b` |

RESIDUE RES-1 to RES-3 leave no lens unclean. S-1 to S-4 are optional.

## Real limits

- **`act_ci.py --selftest` was not executed by me.** The changed fixture there is cleared by static trace and the author's receipt only.
- **No firmware rebuild.** ELF identity is the author's manifest pair plus my input-closure check. No LiteX SoC or bitstream was built by anyone.
- **The author's gate receipts are return codes, line counts and last lines,** not full logs. My reruns of 31 of the 32 carry full logs.
- **The packet is hash-consistent but I could not confirm a signature.** GitHub reports archive commit `8a80a864` as unsigned.
- **No manager source bank ran at this head,** and I claim none. No Verilator, Yosys, parent or processor bank was run; the delta has no RTL.
- **Hosted evidence at about 15:44Z was partial:** 29 runs completed with success, 1 skipped (physical gPTP, not hardware proof), 45 queued or in progress (`receipts/hosted_check_runs_head.tsv`). Executed and green at the exact head: `docs-check`, `docs-check-no-git`, `docs-gates-0..4`, `bdd-conformance`, `elaborate`, `elaborate-gates-0..4`, `split-cdc`, `wire-accountability`, `changes`. The Verilator and Yosys shards were mostly still queued.
- **Physical calibration NOT RUN.**
- **After the probe** the clone is at exact head: tree and index `14cac930...`, 1,997 tracked blobs rehashed with 0 mismatches, 0 mode changes, 6 gitlinks as recorded.

## Pending manager duties

- Build and validate the current-`dev` merge candidate (source base `c1c42843`, live `dev` `e275d795`) and link the receipts on the PR.
- Own hosted and local-replica acceptance once the queued contexts finish.
- Link the evidence packet from the PR or issue. At observation neither carries a link to it, nor a takeover or review-ready comment, so a cold reader of GitHub alone cannot reach the receipts.
- Keep issue #1028 open after this merge. Bullet 4 is not met: the pinned `gptp-processor` (`3ce71b76`) still shows a serial-shaped literal after `--ftdi-serial` in `docs/history/v1/BENCH_FIRSTLIGHT.md`. The `dev` leg and the FPGA-gPTP change are separate heads.
- Decide the author's disclosed open points: the act-slot pool literal, and the EUI-64 clock identities that remain in 12 files under `docs/findings/`, outside the touched set.
- Carry RES-1 to RES-3 to the residue checklist.
- A second independent positive review is still required before merge.

R970-2 FINISHED
