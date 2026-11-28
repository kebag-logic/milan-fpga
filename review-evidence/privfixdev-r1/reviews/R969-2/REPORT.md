[R969] POSITIVE - exact head e7974868ef362f521e59fb82446ff54a19886bfa

Round R969-2, internal independent review of PR #1030 (issue #1028), applied to `dev`.
Head `e7974868ef362f521e59fb82446ff54a19886bfa`, tree `fcccd1c14c1844b776c30d9c0bf4ae7f9d5ea593`, one commit on base `e275d7950ef3385753e6a15d2e191ba855b171ed` (the live `dev` tip).
Verdict basis: no BLOCKER, MAJOR or MINOR finding. Four SUGGESTIONs follow. No RESIDUE.

## Scope reconstructed

- The issue #1028 body is the frozen acceptance. It has no comments, so no maintainer or manager scope decision is recorded on the issue. It asks for four things:
  - no bench-specific name in the touched files;
  - no behaviour change: shipping ELFs and generated outputs byte-identical, and every touched tool's self-test passing;
  - the docs checks passing;
  - a follow-up `gptp-processor` pin (owned by the `dev-soft-core` lane, see Pending).
- The name classes in scope are: the capture-tap product, the bench host names, the AVB switch's label, private addresses and a debug-probe serial.
- Authorities read: AGENTS.md sections 3, 6 and 7; CONTRIBUTING.md section 6 (role naming, "No bench-identifying information"), 6.1 (em dash) and the Contents-separator rule; docs/README.md lines 138-140 (historical pages never define current behaviour).
- PR #1030 says it "Relates to #1028" and is the same change as PR #1029 (`dev-soft-core`, head `0715cb206050c49a1745dd2d11e2fc0e1b74116b`, base `c1c428433539c8a4ab6c007c6d85a98df33d9472`).
- Prior public review findings: none. The PR has 4 issue comments, all review-start notices (R969-1, R970-1, R969-2, R970-2). It has 0 reviews and 0 inline comments, and the issue has 0 comments. No prior finding needs resolving.

## Evidence

### Same change as #1029
- Both PRs touch the same 21 paths.
- `compare_changed_lines.sh` hashes each file's removed and added lines with offsets ignored. All 21 files are `SAME` (`compare_changed_lines.txt`).
- 17 of the 21 files are byte-identical between the two bases and between the two heads (`base_head_blob_compare.txt`).
- The other 4 differ between the branches before the change: BUILDING.md, REGISTER_MAP_CLASSES.md, RUNNING_TESTS.md and TESTING.md. Their edited lines are still identical.
- There is no file that only #1030 edits.

### Scan clean
- `scan_bench_names.py` builds its product, host and switch tokens from code points, so it does not carry the removed names itself.
- Over the whole tracked tree, those three classes go from 28 lines in 19 files at the base to **0 at the head** (`scan_counts.txt`). The other two of the 21 files are the two fixture addresses.
- The submodules have 0 hits. The commit message has 0 hits.
- In the touched files, the private-address class only hits two kinds of line (`scan_head.txt`):
  - IEEE clause numbers such as `10.7.6.2`;
  - `scripts/act_ci.py`'s Docker-default `172.18.0.1` and `172.30.0.1` stub gateways, and the slot pool `10.231.N.0/24`.
- The slot pool is a value the repository owns, not a bench address:
  - `scripts/act_ci.py:739` derives it, `return f"10.231.{self.number}.0/24"`;
  - `scripts/act_ci.py:14415` hands it to the slot daemon;
  - `docs/testing/CI_WORKFLOWS.md:2669` documents it.
  - So keeping it, as the PR body explains, is right, and changing it would be a behaviour change.
- Debug-probe serial: BUILDING.md:467 already uses the `<ax-ftdi-serial>` placeholder at the base. Nothing remains to change.

### No behaviour change
- Nothing changes under `hdl/`, `sw/`, `syn/`, `configs/`, `avdecc/`, `ci/` or any submodule.
- The build trees mention the changed files only in comments: `configs/endstation_ax7101_8x8.yaml:70`, `sw/litex/build.sh:30,45,56`, `sw/builder/test_builder.py:14551` and `syn/ooc/pp_resource_gate.py:391`. Firmware byte-identity therefore follows from the structure of the change.
- The author's firmware receipts corroborate it:
  - `dev-base.manifest.tsv` and `dev-head.manifest.tsv` are byte-identical (`cmp`);
  - each has 4,410 rows, which is 235 + 939 + 3,236;
  - both builds end `test_ctrl_firmware: BUILT`.
- `scripts/act_ci.py:15368`: the stub gateway changes from `<ip>` to `192.0.2.1`.
  - Production code only checks it is valid IPv4 (`scripts/act_ci.py:4896-4901`).
  - The arm's `check(...)` (`:15394-15402`) asserts the return code, the event list and the transcript strings, never the address.
- `scripts/check_baremetal_only.py:1137`: the fixture changes from `<ip>` to `192.0.2.2`. The detector regex at `:215` does not depend on the address.
- `tb/tools/torture_campaign.py:6783`: `"device"` is a fixture label. The arm asserts only the verdict `FAIL`.
- `human_action` text, argparse help text, docstrings and comments are not asserted anywhere (searched with `git grep`).
- The renamed behave scenario (`tests/features/wire_truth_avtp.feature:274`) has no outside reference.

### Gates I ran at the head (logs in `logs/`, every rc 0)
- Documentation:
  - `check_doc_style.py` and its `--selftest`;
  - `check_em_dash.py --base e275d795`: 0 findings over 15 added lines on 8 pages, 339/339 arms; and its `--selftest`;
  - `gen_toc.py --check` (152 pages);
  - `gen_toc.py --verify-anchors` (621 links);
  - `check_doc_paths.py`;
  - `docs_check.py` (0 findings, scrub self-test 23/23);
  - `docs_inventory.py --check`, `docs/DOC_MAP.gen.py --check`, `generate_ci_evidence_pins.py --check` and `check_feature_status.py`.
  - The pinned renderer came from `tools/markdown/requirements.txt` with `--require-hashes`, installed into a disposable venv.
- Code quality: `check_hygiene.py --check`, `check_py_idiom.py`, `check_sh_idiom.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check`, and `bash -n tb/tools/check_tu_on_wire.sh`.
- Tool self-tests:
  - `check_baremetal_only.py --check` (0 findings, 1,704 files) and `--selftest` (867 arms);
  - `avtp_wire_truth.py --self-test` (25 tests OK);
  - `torture_campaign.py --self-test` (123 tests OK).
- Behave: the three touched features, 231 scenarios and 921 steps passed.
- The same tool self-tests and behave also ran on an extracted base tree, with identical counts: 867 arms, 25, 123 and 231 (`base_gate_summary.txt`).
- Two gates did not run here because their tool was missing:
  - `gen_register_reference.py --check` (`wavedrom`);
  - `ci_gate_workflows.py --check` (`yaml`).
  - Their author receipts report rc 0 at base and head.

### Author packet
- `review-evidence/privfix-r1` at commit `8a80a864b336e65ff1a19d5118b889fecd897eeb` has 27 entries. All 27 match their `published_sha256`, and no file is unlisted (`verify_manifest.py`, `verify_manifest.txt`).
- The author's `dev-compare.txt` records 32 gates with rc 0 at base and head. The 32 include the `act_ci.py --selftest`, which I may not run here.
- The `privfixdev-r1` path named in the review brief does not exist at that commit. The packet is at `privfix-r1`.

### Hosted runs at the exact head
At snapshot (`hosted_check_runs.tsv`), 33 contexts had completed with success. Of the rest:
- 1 skipped: Physical gPTP, nightly and manual;
- 13 in progress;
- 10 queued.

The manager owns hosted and act acceptance. I make no claim about it.

## Findings

**S1 SUGGESTION, lenses Tests and Docs**, `scripts/act_ci.py:15368`.
- Evidence:
  - The arm stands in a slot-2 boundary (`slot = ReplaySlot(2)`). Its old gateway `<ip>` sat inside the slot-2 pool that `:739` derives.
  - The PR body keeps that same pool as repository configuration, yet rewrites this gateway as if it were a lab address. The new `192.0.2.1` lies outside the pool the stand-in models.
  - No assertion reads the address, so no test outcome changes.
- Impact: the fixture is less realistic. If a later change checks that the gateway lies in the slot pool, this arm will fail for an unrelated reason.
- Optional outcome: restore the slot-pool gateway, or note in the PR body that the stub address is deliberately outside the pool.
- Verification: `act_ci.py --selftest` still passes.

**S2 SUGGESTION, lens Docs**, `docs/integration/BUILDING.md:590`, `docs/testing/RUNNING_TESTS.md:233`, `docs/testing/TESTING.md:100,1123`.
- Evidence: the rewritten lines now name hosts by role ("controller bench host"). Beside them, the capture host is still named by its OS ("Ubuntu server").
- This is not a bench-specific name under the issue's classes, and `docs_check.py` does not flag it. CONTRIBUTING.md section 6 does prefer role names.
- Impact: inconsistent naming only.
- Optional outcome: in a follow-up on both lines of development, rename it to a role such as "the capture host".
- Verification: `docs_check.py` and `gen_toc.py --check`.

**S3 SUGGESTION, lenses Tests and Docs**, `scripts/docs_check.py:148` (`IDENTITY_RULES`).
- Evidence: CONTRIBUTING.md section 6 describes how to guard against a removed name returning: an identity-token rule assembled from code points, plus a planted `scrub_selftest` fixture. This change scrubs the tree but adds no rule.
- The issue does not require a rule, so this is not a conformance gap.
- Impact: nothing stops the removed tokens from coming back.
- Optional outcome: a follow-up issue that adds the rules and fixtures on both lines.
- Verification: the scrub self-test arm count rises and the tree stays at 0 findings.

**S4 SUGGESTION, lens Docs**, `docs/testing/RUNNING_TESTS.md:232` and `docs/testing/TESTING.md:1124`.
- Evidence: "the controller and audio endpoint on the controller bench host" repeats "controller". TESTING.md:1124 is 96 characters long, while the paragraph around it wraps at about 76.
- Impact: cosmetic only. Rendering is unaffected.
- Optional outcome: for example, "the controller and audio endpoint on their bench host", and rewrap.
- Verification: `check_doc_style.py`.

Comment rule: no added line brings a new lane label, lane name, review round, reviewer ID or comment ID. No added line contains U+2014.

## Lens results (each with its artifact)

- [R969] PASS Conformance -- issue #1028 acceptance vs `compare_changed_lines.txt`, `scan_counts.txt`, `scan_head.txt`, and `scripts/act_ci.py:739,14415` -- 21/21 files carry #1029's edited lines and there is no file only #1030 edits; the three name classes are at 0 at the head; the retained addresses are the repository's own slot contract; criterion 4 belongs to the `dev-soft-core` lane.
- [R969] PASS RTL -- `git diff --stat e275d795..e7974868` -- no path under `hdl/`, `syn/`, `configs/` or any submodule. Gitlinks are unchanged (`git submodule status`), and no build-tree file reads a changed file except in comments. The lens has no matching artifact in this delta.
- [R969] PASS Robustness -- `scripts/act_ci.py:4896-4901,15394-15402`, `scripts/check_baremetal_only.py:215,1137` and `tb/tools/torture_campaign.py:6783` -- every changed fixture value reaches only an address-agnostic validator or label. The base and head self-test counts are identical: 867 arms, 25, 123 and 231 scenarios.
- [R969] PASS Tests -- `logs/*.rc` and `base_gate_summary.txt` -- the touched tools' self-tests and the three touched behave features pass at the head with base-equal counts. The renamed scenario is unreferenced, and no assertion depends on the changed strings. S1 and S3 are optional.
- [R969] PASS Docs -- `logs/em_dash.log`, `logs/toc_check.log`, `logs/toc_anchors.log`, `logs/docs_check.log`, `logs/doc_style.log`, and the 8 page hunks. Meaning is kept on each page:
  - the historical pages stay historical, per docs/README.md:139;
  - REGISTER_MAP_CLASSES.md switches its whole Contents block to `--`, per CONTRIBUTING.md's separator rule.
  - S2 and S4 are optional.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #1028 acceptance; PR #1029 vs #1030 edited lines (21 files); tree-wide name scan; `scripts/act_ci.py:739,14415`; `docs/testing/CI_WORKFLOWS.md:2669` | R969-2 | e7974868ef362f521e59fb82446ff54a19886bfa |
| RTL | CLEAN | diff stat (no `hdl/`, `syn/`, `configs/` or submodule path); gitlinks unchanged; build-tree references are comments only | R969-2 | e7974868ef362f521e59fb82446ff54a19886bfa |
| Robustness | CLEAN | `scripts/act_ci.py:4896-4901,15368,15394-15402`; `scripts/check_baremetal_only.py:215,1137`; `tb/tools/torture_campaign.py:6783` | R969-2 | e7974868ef362f521e59fb82446ff54a19886bfa |
| Tests | CLEAN | baremetal selftest 867 arms; avtp_wire_truth 25; torture_campaign 123; behave 231 scenarios, base-equal | R969-2 | e7974868ef362f521e59fb82446ff54a19886bfa |
| Docs | CLEAN | 8 page hunks; em-dash, TOC, anchors, doc-style, doc-paths, docs_check, inventory and DOC_MAP gates | R969-2 | e7974868ef362f521e59fb82446ff54a19886bfa |

## Real limits

- `scripts/act_ci.py --selftest` was not run, because the brief forbids it. Its PASS rests on the author's receipt (`dev-compare.txt`) and my static reading of the one changed arm.
- `gen_register_reference.py --check` and `ci_gate_workflows.py --check` were not run, because `wavedrom` and `yaml` are not installed here. They rest on the author's receipts.
- I did not rebuild the firmware. Byte-identity rests on the structure of the change plus the author's identical base and head manifests, which I checked against the packet's hashes.
- The author packet's commit `8a80a864` is not GPG-signed (`%G?` = `N`). I verified hash integrity only.
- Behave ran on the three touched features only, not the whole 508-scenario suite. The full run rests on the author's receipt.
- No hardware or physical calibration was run. Field skips are not hardware proof.
- I ran no manager source bank and claim none.

## Pending manager duties

- Hosted exact-head contexts: 23 were not yet complete at snapshot.
- Act replication.
- The current-`dev` merge candidate (builder and native banks) at the merge turn.
- The second, external positive review.
- Acceptance criterion 4: the `gptp-processor` pin follow-up, through the `dev-soft-core` lane. #1028 closes there.
- Merge authorization.

Clone restored: `git ls-files -s` hash and `git submodule status` are identical to before the probes. The worktree is clean at `e7974868ef362f521e59fb82446ff54a19886bfa`, tree `fcccd1c14c1844b776c30d9c0bf4ae7f9d5ea593`.

R969-2 FINISHED
