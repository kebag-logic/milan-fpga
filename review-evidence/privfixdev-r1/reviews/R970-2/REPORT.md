[R970] POSITIVE - exact head e7974868ef362f521e59fb82446ff54a19886bfa

# R970-2 external independent review: issue #1028 / PR #1030 (`dev`)

- Head `e7974868ef362f521e59fb82446ff54a19886bfa`, tree `fcccd1c14c1844b776c30d9c0bf4ae7f9d5ea593`, one commit on base `e275d7950ef3385753e6a15d2e191ba855b171ed`.
- Live `dev` was still `e275d795` at 15:53Z on 2026-11-28, so the source base is the live base.
- Review start: https://github.com/kebag-logic/milan-fpga/pull/1030#issuecomment-7241661696
- No open BLOCKER, MAJOR or MINOR. Three RESIDUE items and four SUGGESTION items are listed below, each with its exact fix.
- One classification needs a maintainer's eye before this verdict is relied on: S3.

## What the change is

21 files, 33 lines removed and 33 added: 8 documentation pages, 2 scripts, 5 files under `tb/tools/`, 6 files under `tests/`.
It replaces the capture-tap product name, two bench host names, the switch's model label and two fixture addresses with role wording and RFC 5737 addresses.
No path under `hdl/`, `sw/`, `syn/`, `configs/`, `avdecc/` or `ci/` changes, and no submodule gitlink moves (`receipts/clone-integrity.txt`).

## The three points asked of this round

### 1. Same edits as PR #1029

`receipts/compare-1029-vs-1030.txt`: both PRs touch the same 21 paths, and in every one of the 21 the sequence of removed and added lines is identical.
There is no `dev`-only file in this PR, so there is no `dev`-only edit to judge.
PR #1029 was compared at head `0715cb206050c49a1745dd2d11e2fc0e1b74116b`.

### 2. No behaviour change

- `receipts/delta-semantics.masked.txt` (`scripts/delta_semantics.py`): every Python file was compared as an AST and as a token stream at base and head. The differences are 6 docstrings, 5 string constants and 2 comments. Non-string or structural differences: 0.
- The 5 string constants are: the `--tap` help text (`tb/tools/avtp_wire_truth.py:185`), one operator instruction (`tb/tools/torture_campaign.py:2989`), one self-test fixture label (`tb/tools/torture_campaign.py:6783`), and two self-test fixture addresses (`scripts/act_ci.py:15368`, `scripts/check_baremetal_only.py:1137`).
- The fixture label is passed through to the `devices` detail only (`tb/tools/torture_campaign.py:1229`); no verdict reads it.
- The remote-shell rule matches on `root@` and ignores the host (`scripts/check_baremetal_only.py:215`), so the arm still fires on the new address.
- The mock gateway only has to be a valid IPv4 address (`scripts/act_ci.py:4897-4902`), and the arm's assertion does not read it (`scripts/act_ci.py:15397-15402`).
- `tests/steps/torture_plan_steps.py:716` and `tb/tools/torture_campaign.py:6992` compare the first 24 characters of the operator instruction. Those 24 characters are unchanged.
- The retitled scenario (`tests/features/wire_truth_avtp.feature:274`) is named nowhere else in the tree.
- The shell file changes one comment line (`tb/tools/check_tu_on_wire.sh:20`); `bash -n` passes.
- Firmware: the author's base and head build manifests for `dev` are byte-identical, 235 RV32 ELFs, 939 host ELFs and 3,236 other outputs, 4,410 rows (`receipts/packet-verification.txt`). This round did not rebuild.

### 3. Meaning kept under the docs rules, and the scan

- Gates rerun by this round at the head, all rc 0 (`receipts/gates/`, `scripts/run_gates.sh`): `docs_check.py` (0 findings, 215 pages and 1,706 text files), `check_doc_style.py`, `check_em_dash.py --base e275d795` (0 findings over 15 added lines on 8 pages, arms 339/339), `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `docs_inventory.py --check`, `gen_register_reference.py --check`, `DOC_MAP.gen.py --check`, `check_feature_status.py`, `check_todo_ownership.py`, `check_hygiene.py --check`, `check_py_idiom.py`, `check_sh_idiom.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`.
- Where the author's packet records the same gate, the result agrees (32 gates, 0 failing at base and at head).
- Each changed prose line was read in context. On the Markdown lines the only edits besides the names are U+2014 to `--`: 16 characters on 5 lines, none inside a quoted specification sentence.
- `docs/reference/REGISTER_MAP_CLASSES.md:37-39` moves the whole Contents block to `--`; `gen_toc.py --check` accepts it.
- Scan, reviewer-derived (`receipts/scan-removed-tokens.txt`, `scripts/scan_removed_tokens.py`): 11 tokens occur on a removed line and on no added line. 10 of them have 0 lines at the head across every tracked text file. The eleventh is an ordinary English adjective that sat in a hyphenated compound with the product name (305 lines at base, 304 at head).
- Scan, author's: 2 hits at the head, both the act-slot address pool pins. They are at `scripts/act_ci.py:14124` and `:14415`, and they pin the launcher's own pool (`scripts/act_ci.py:739`). That value is a design constant of the tool and identifies no bench. Changing it would change launcher behaviour, which the issue's second criterion forbids. I accept the two as not bench-specific; the public decision is a manager duty (below).
- The other private-range literals left in `scripts/act_ci.py` are stock container-bridge gateways in mocks (`receipts/scan-addresses.txt`). They identify no bench.
- The remaining locations in that receipt are IEEE clause numbers and one register range that have the shape of an address. The receipt gives locations only, so it repeats no retained literal.
- Comment rule: 0 added lines carry a lane label, a review round, a reviewer ID or an issue-comment ID (`receipts/delta-comment-rule.txt`).

## Acceptance criteria of issue #1028

| criterion | at this head | evidence |
|---|---|---|
| No bench-specific name in the touched files' current content | met, as the issue defines the term (bench hardware, hosts, the switch, private addresses, a probe serial); S3 names something outside that definition | `receipts/scan-removed-tokens.txt`, `receipts/scan-addresses.txt` |
| No behaviour change; shipping ELFs and generated outputs byte-identical; every touched tool's self-test passes | met | `receipts/delta-semantics.masked.txt`, `receipts/packet-verification.txt`, `receipts/gates/` |
| Docs checks pass (paragraph style, ASCII dash) | met | `receipts/gates/doc_style.log`, `receipts/gates/em_dash.log` |
| A follow-up pins `gptp-processor` to the FPGA-gPTP commit carrying the same change | not part of this PR; still owed | gitlink `gptp-processor` is `1616fc8f` at base and head |

## Findings

No BLOCKER, MAJOR or MINOR.

### W1 - RESIDUE - Docs - the tap's record format now reads as a property of every inline tap

- Where: `tb/tools/avtp_wire_truth.py:7` and `:185`, `tb/tools/avtp_wire_truth_wire.py:216`, `tb/tools/check_tu_on_wire.sh:20`.
- Evidence: the old text tied the 28-octet record header and the kept FCS to one named product. The new text says "an inline capture tap" writes them. That is true of the bench's tap and not of inline taps in general.
- Impact: a reader with a different tap could pass `--tap` and get offsets 28 octets out. Wording only: no code, test or figure changes.
- Exact fix: write "the bench's inline capture tap" in those four places. `tb/tools/avtp_wire_truth_selftest.py:621` already uses the definite form.
- Verification: reread the four lines; `avtp_wire_truth.py --self-test` and `bash -n` still pass. The same four lines are in PR #1029.

### W2 - RESIDUE - Docs - the PR body's list of what changed omits one operator instruction

- Where: PR #1030 body, "Only prose, help text, docstrings, comments, one behave scenario title and fixture labels change."
- Evidence: `tb/tools/torture_campaign.py:2989` is the `human_action` of the switch power-cycle step. The checklist prints it (`tb/tools/torture_campaign.py:6310`), so one line of tool output changes.
- Impact: none on any test or verdict. The sentence is incomplete.
- Exact fix: add "and one operator instruction in the torture plan" to that sentence.
- Verification: reread the PR body.

### W3 - RESIDUE - Docs - the public thread does not link the evidence it rests on

- Where: PR #1030 and issue #1028 threads at 15:53Z.
- Evidence: the PR carries four review-start notices and no other comment; the issue carries none. The author packet is public at commit `8a80a864`, path `review-evidence/privfix-r1`, and nothing on the PR or the issue links it. There is no `REVIEW READY` comment naming the commit and the commands. The path `review-evidence/privfixdev-r1` does not exist at that commit.
- Impact: a cold reader cannot get from the PR to the receipts. No measurement or claim changes.
- Exact fix: one PR comment linking `https://github.com/kebag-logic/milan-fpga/tree/8a80a864b336e65ff1a19d5118b889fecd897eeb/review-evidence/privfix-r1` and stating the head it covers.
- Verification: the link opens and its `MANIFEST.json` verifies (`scripts/verify_packet.py`).

### S1 - SUGGESTION - Docs - a table row that no longer says anything

- Where: `docs/integration/BUILDING.md:591`.
- The row now reads "a second bench host: retired; it holds no bench role". Without the name it tells a reader nothing. Dropping the row loses no information.

### S2 - SUGGESTION - Docs - one docstring line grew past its neighbours

- Where: `tb/tools/torture_campaign.py:3101`, 82 columns. The idiom gate passes. Rewrapping keeps the block even.

### S3 - SUGGESTION - Conformance, Docs - a private repository name remains in two touched files, outside this issue's list

- Where: `docs/history/v1/tests/CONFORMANCE_TESTING_HOWTO.md:95`, `:97`, `:101`, `:346`, `:375` and `tb/tools/torture_campaign.py:22`. None of these lines is in the delta, and all six are at the base.
- Authority: `CONTRIBUTING.md:409-411` says the private bench suite is never referenced by an external name. `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:120-124` already uses a placeholder for the same repository.
- Why this is not a MINOR here: issue #1028 defines its bench-specific names as bench hardware, hosts, the switch, private addresses and a probe serial. A repository name is none of those, the author's rule list does not carry it, and `docs_check.py` passes at base and head. The name also stands in the public body of issue #247.
- This classification is mine. If the maintainer reads the first acceptance criterion as covering this name, it is a MINOR under Conformance and Docs, those two lenses are not clean, and this verdict does not stand.
- Recommended: a public maintainer decision, and if the name is to go, a new Issue that also adds the token to `scripts/docs_check.py` as `CONTRIBUTING.md:706-711` describes.

### S4 - SUGGESTION - Docs - a docstring cites a page that is not in the tree

- Where: `tb/tools/avtp_wire_truth_wire.py:220` cites `docs/findings/BENCH_TOPOLOGY.md`. No tracked file has that name. The line is at the base and is not in the delta; it sits four lines below a changed line.

## Mutation probes (Tests, Robustness)

Each mutation was planted in a disposable copy and run beside an unmutated control (`scripts/apply_mutations.py`, `scripts/run_probes.sh`, `receipts/probes/`).

| probe | mutation | control | mutated |
|---|---|---|---|
| M1 | `check_baremetal_only.py`: the remote-shell rule stops tolerating options before `root@` | PASS, 867 arms | rc 2, arm `runtime-remote-root-shell-with-options-caught` reports the planted defect not caught |
| M2 | `avtp_wire_truth_wire.py`: the reader ignores the tap record header | self-test OK; 37 scenarios pass | self-test fails 2 tests; scenario at `wire_truth_avtp.feature:274` fails |
| M3 | `torture_campaign.py`: a stream-scoped capture source no longer convicts alone | self-test OK | self-test fails `test_cross_side_growth_bites_every_way` |

So the arm, the scenario and the check whose fixtures this change rewrote can each still fail for the defect they claim.
Behave at the head: the three touched features pass 231 scenarios, the whole suite 508 (`receipts/gates/behave_touched.log`, `behave_full.log`).

## Prior public findings on this PR

None exist. At 15:53Z PR #1030 had 0 reviews, 0 inline comments and four review-start notices, and issue #1028 had 0 comments. There is nothing to resolve or retain.

## Lens results

```text
[R970] PASS Conformance — issue #1028 acceptance list against receipts/scan-removed-tokens.txt, receipts/delta-semantics.masked.txt, receipts/gates/em_dash.log, receipts/compare-1029-vs-1030.txt — criteria 1 to 3 met at e7974868; criterion 4 is a follow-up outside this PR
[R970] PASS RTL — receipts/clone-integrity.txt and the 21-path list of e275d795..e7974868 — no path under hdl/, sw/, syn/ or configs/ and no gitlink changes; tb/tools/check_tu_on_wire.sh:20 is a comment
[R970] PASS Robustness — scripts/check_baremetal_only.py:215 and :1137, scripts/act_ci.py:4897-4902 and :15368, tb/tools/avtp_wire_truth_wire.py:212-238 — the rewritten fixtures still reach the refusal paths they exercise (probes M1, M2)
[R970] PASS Tests — receipts/probes/ (M1 to M3 with controls), receipts/gates/behave_full.log, tests/steps/torture_plan_steps.py:716 — every touched test still fails for its defect; 508 scenarios and 867 arms pass
[R970] PASS Docs — the 8 changed pages read in context, receipts/gates/docs_check.log, doc_style.log, em_dash.log, toc_check.log, toc_anchors.log — role wording per CONTRIBUTING.md section 6, no U+2014 on added lines, Contents blocks fresh
```

## Reviewer-owned ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #1028 body; `CONTRIBUTING.md:684-711`; `receipts/scan-removed-tokens.txt`; `receipts/scan-addresses.txt`; `receipts/compare-1029-vs-1030.txt`; `receipts/packet-verification.txt` | R970-2 | `e7974868ef362f521e59fb82446ff54a19886bfa` |
| RTL | CLEAN | path list of `e275d795..e7974868`; gitlinks in `receipts/clone-integrity.txt`; `tb/tools/check_tu_on_wire.sh:20` | R970-2 | `e7974868ef362f521e59fb82446ff54a19886bfa` |
| Robustness | CLEAN | `scripts/check_baremetal_only.py:215`, `:1137`; `scripts/act_ci.py:4897-4902`, `:15368`; `tb/tools/avtp_wire_truth_wire.py:212-238`; `tb/tools/torture_campaign.py:1108-1150`; probes M1 to M3 | R970-2 | `e7974868ef362f521e59fb82446ff54a19886bfa` |
| Tests | CLEAN | `receipts/probes/`; `receipts/gates/behave_touched.log`, `behave_full.log`, `baremetal_selftest.log`, `avtp_wire_truth.log`, `torture_campaign.log`; `tests/features/wire_truth_avtp.feature:274`; `tests/steps/torture_plan_steps.py:716` | R970-2 | `e7974868ef362f521e59fb82446ff54a19886bfa` |
| Docs | CLEAN | the 8 changed pages at their changed lines; `receipts/gates/docs_check.log`, `doc_style.log`, `em_dash.log`, `toc_check.log`, `toc_anchors.log`, `doc_paths.log`, `docs_inventory.log`; PR #1030 body | R970-2 | `e7974868ef362f521e59fb82446ff54a19886bfa` |

RESIDUE W1 to W3 leave no lens unclean under the owner rule of 2026-10-02. S1, S2 and S4 are optional. Conformance and Docs are clean only on the S3 classification stated above.

## Limits of this review

- `scripts/act_ci.py --selftest` was not run by this round, by rule. Its pass at this head rests on the author's receipt and on hosted job `docs-gates-2` (job 141015709874, success, head `e7974868`), whose step at `.github/workflows/docs.yml:761` runs it.
- The author's scan rule list is private. Only its totals are published, so the two retained hits were located by this round's own address scan and not by rerunning the author's rules.
- GitHub reports the packet commit `8a80a864` and the head commit as unsigned. The packet was verified by git blob id and by its own `MANIFEST.json` (27 entries, 0 mismatches), not by a signature.
- Firmware byte identity is the author's measurement. This round checked that the two manifests are identical and that no firmware source is in the delta. No LiteX, bitstream, parent, protocol-processor, gPTP, Yosys or builder bank ran.
- The scoped Verilator was not used: the delta carries no RTL and no simulation source.
- Hosted evidence at 15:53Z: the `docs` workflow (run 46156988749) had every job completed and successful, and `bdd-conformance` in `rtl-fast` (run 46156988763) succeeded. `rtl-fast`, `rtl-full` and `elaborate` were still running or queued. `Physical gPTP (nightly and manual)` was skipped, and a skip is not evidence.
- No manager source bank ran at this head, and none is claimed. No hardware was used; physical calibration NOT RUN.
- PR #1029 was examined only for line identity with this PR. FPGA-gPTP was not reviewed.
- The author's figure of 168 stale inventory inputs out of 378 was not reproduced. This round's count for `ci/image/command-table.json` is 42 of 148 tracked records stale at base and 43 at head (`receipts/ci-image-snapshot-staleness.txt`). The one record this delta makes stale is `scripts/check_baremetal_only.py`, as the PR body says. No workflow under `.github/workflows/` names those snapshots.

## Pending manager duties

- Build and validate the current-`dev` merge candidate and link its receipts on the PR.
- Accept the hosted and local-replica contexts once the in-flight runs finish.
- Record publicly the decision to keep the two act-slot pool pins (`scripts/act_ci.py:14124`, `:14415`).
- Get S3 decided publicly; open a new Issue if the name is to be removed.
- Carry W1, W2 and W3 to the residue checklist. W1 applies to PR #1029 as well.
- Deliver the follow-up of acceptance criterion 4, and do not let issue #1028 close before it lands.
- Refresh the `ci/image` snapshots at the next image refresh.
- A second independent positive review is still required before merge.

## Packet contents

- `scripts/`: `delta_semantics.py`, `scan_removed_tokens.py`, `verify_packet.py`, `apply_mutations.py`, `run_probes.sh`, `run_gates.sh`.
- `receipts/`: the files named above, with one log and one rc file per gate and per probe.
- `MANIFEST.sha256` lists every publishable file. Host paths in two probe logs are replaced by `$PACKET`.
- `scripts/run_gates.sh` records the gate commands as one runner; the round ran them in three batches with the same arguments.
- The clone was left at the exact head: worktree, index and gitlinks equal `e7974868` (`receipts/clone-integrity.txt`).

R970-2 FINISHED
