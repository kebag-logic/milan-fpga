[R969] POSITIVE - exact head 0715cb206050c49a1745dd2d11e2fc0e1b74116b

# R969-2: internal independent review of PR #1029 (issue #1028)

- Reviewer: R969 (internal role, cleared-context independent session), round R969-2.
- Exact head `0715cb206050c49a1745dd2d11e2fc0e1b74116b`, tree `14cac930093a39ae1e96881d63f774ad3a322b0e`, one commit on source base `c1c428433539c8a4ab6c007c6d85a98df33d9472` (`dev-soft-core`).
- Commit message: one line ("Remove bench-specific names from documentation and tools"), no body, no trailer.
- Delta: 21 files, 33 lines changed. 8 Markdown pages, 2 CI scripts, 5 tools under `tb/tools/`, 6 behave files. Nothing under `hdl/`, `sw/`, `syn/`, `configs/`, `avdecc/` or `ci/`, and no gitlink.
- Previously reviewed head: none with published findings. R969-1, R970-1 and R970-2 posted only start notices on the PR. The PR has no review objects and no inline comments, and the issue has no comments. So there was no prior finding to resolve or retain, and this round judges the whole delta.

Verdict: POSITIVE. All five lenses are covered clean at the exact head. There is one RESIDUE (wording only) and four SUGGESTIONs. Nothing at MINOR or above.

## How the task was reconstructed

1. AGENTS.md and CONTRIBUTING.md. The rules that apply are section 6 (bench equipment named by role; no hostnames, bench subnets or USB serials; the deny-list extension path) and section 6.1 (the em-dash rule for added lines, with Contents separators switched per block).
2. docs/README.md map.
3. Issue #1028 body: the task and its four acceptance items. The issue has no comments and no further scope decision.
4. PR #1029 body and the hosted check state at the exact head.
5. The diff `c1c42843..0715cb20`, read in full.
6. Public evidence at `8a80a864b336e65ff1a19d5118b889fecd897eeb:review-evidence/privfix-r1`, verified by hash.
7. My own probes, listed below.

Frozen acceptance from #1028:
- A1: no bench-specific name in the touched files' current content.
- A2: no behaviour change. Shipping ELFs and generated outputs are byte-identical, and every touched tool's self-test passes.
- A3: the docs checks pass (paragraph style, ASCII dash).
- A4: a follow-up pins `gptp-processor` to the FPGA-gPTP commit carrying the same change.

A4 is a separate follow-up and not this PR's deliverable. It is listed under pending duties.

## Evidence examined and probes run

All receipts are in this packet. Removed tokens are never spelled in any receipt or script: tokens are assembled from code points, and removed literals are shown only as sha256 prefixes, as CONTRIBUTING section 6 asks of the deny-list.

### Author packet integrity (`packet_verify.txt`, `scripts/verify_packet.py`)
- 27/27 files match `MANIFEST.json` `published_sha256`. None is unlisted and none is missing.
- The evidence commit carries no git signature (`%G?` = N). Integrity rests on the committed hash manifest.

### Firmware byte identity (author receipts, re-verified)
- `dsc-base.manifest.tsv` and `dsc-head.manifest.tsv` are byte-identical: 149 rv32-elf, 1,489 host-elf and 5,664 other = 7,302 entries, matching the PR body's counts.
- The build tails read `test_ctrl_firmware: BUILT` (`--build-only`).
- The `dev` tree manifests are also identical (235/939/3,236). That belongs to PR #1030 and is noted for context only.

### Author gate receipts
- `gates/dsc-compare.txt`: base2 against head, 32 gates, 0 changed and 0 failing.
- `gates/last-lines.txt` verdict lines agree with my own reruns below.

### Structural no-behaviour probe (`ast_delta.txt`, `scripts/ast_delta.py`)
Every touched Python file parses to an identical AST at base and head once string constants are masked. The constant count is the same at base and head in every file. The only changed constants are:
- the act_ci self-test mock gateway (now `192.0.2.1`);
- the check_baremetal_only fixture (`ssh -p 2222 root@192.0.2.2 reboot`);
- the `--tap` help string;
- the `human_action` text;
- the fixture label `capture-tap`;
- docstrings.

No identifier, option, wire literal, file-format literal or control flow changed. Specifically, the 28-octet header, `--tap` and `ether[40:2]` are unchanged in text.

### Token scan (`scan_*.txt`, `scripts/scan_tokens.py`)
- Base, the 21 touched files: 34 hits over 7 token classes (tap product 20, host A 2, host B 5, switch model 5, the two old fixture addresses 1 each). This matches the author's stated pre-fix count of 34.
- Head, the 21 touched files: 0.
- Head, the whole tracked tree (2,003 files): 0.
- The HDL net `pw1_w` at `hdl/ieee1722/aaf/KL_render_queue.sv:557` is untouched and excluded by word boundary.
- A separate broader scan of the touched files kept only the stated false positives:
  - the act-slot pool literals `scripts/act_ci.py:14124` and `:14415`, plus production `:739`, which is outside the diff;
  - Docker's default bridge `172.18.0.1` fixtures;
  - the `10.a.b.c` IEEE clause numbers;
  - OS and image labels.

### Remote-shell detector probe (`remote_shell_probe.txt`, `scripts/remote_shell_probe.py`)
- `REMOTE_ROOT_SHELL_RE` (`scripts/check_baremetal_only.py:214-215`) is address-agnostic. The head fixture still fires, so arm `[R]` keeps its meaning.
- The controls behave as expected: the near-miss-clean arm and a non-root login do not fire.

### act_ci fixture analysis (static only; the act_ci self-test was not run, per brief)
- The mock gateway reaches only the IPv4 server-bind check (`scripts/act_ci.py:4896-4902`). `192.0.2.1` is a valid IPv4 address, so that check passes.
- The arm's assertion (`scripts/act_ci.py:15394-15403`) checks rc, the slot events, the namespace, endpoint and CPU ranges, none of which depends on the address.
- No containment or range check on the gateway exists in the file (searched for `is_private`, `subnet_of` and `ip_network(`).
- The author's head receipt records `act_ci_selftest: selftest: PASS`.

### torture_campaign fixtures
- `"device": "capture-tap"` is a display label, copied into detail only (`tb/tools/torture_campaign.py:1229`). The asserted verdict `FAIL` (`:6782-6786`) does not read it.
- The `human_action` prefix assertions (`torture_campaign.py:6992`, `tests/steps/torture_plan_steps.py:716`) compare `[:24]`. Base and head share the same 24-character prefix, "Power off the AVB switch".

### Renamed behave scenario
- `tests/features/wire_truth_avtp.feature:274` is referenced nowhere else in the tree.
- It runs and passes inside the touched-feature set.

### My gate reruns at the exact head (`gates-head/SUMMARY.tsv`, `scripts/run_gates.sh`)
All rc 0. Renderer gates used the pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1, matching `tools/markdown/requirements.txt`).

| Gate | Result |
|---|---|
| `check_em_dash.py --base c1c42843` | 0 findings over 15 added lines in 8 pages |
| `check_em_dash.py --selftest` | 339 arms |
| `check_doc_style.py` | OK |
| `docs_check.py` | 0 findings, 226 md + 1,972 text files |
| `gen_toc.py --check` and `--verify-anchors` | OK, 759 links |
| `check_doc_paths.py` | OK |
| `docs_inventory.py --check` | OK |
| `DOC_MAP.gen.py --check` | OK |
| `gen_register_reference.py --check` | OK |
| `check_hygiene.py --check` | OK |
| `check_py_idiom.py` | over-long 0 |
| `bash -n tb/tools/check_tu_on_wire.sh` | OK |
| `avtp_wire_truth.py --self-test` | OK |
| `torture_campaign.py --self-test` | OK |
| `check_baremetal_only.py --check` | OK |
| `check_baremetal_only.py --selftest` | 867 arms |
| behave, 3 touched features | 231 scenarios passed |
| behave, full suite | 15 features, 511 scenarios passed |

### Added-line checks
- No added line carries U+2014.
- No added line carries a lane label, review round, reviewer ID or issue-comment ID, so no comment-rule RESIDUE.

### CI-image snapshot claim
- `ci/image/tool-inventory.json` records the base digest of `scripts/check_baremetal_only.py` (`c720ca99...`). The head blob is `a0e91a2a...`.
- 168 of 378 recorded inputs were already stale at the base, which confirms the author's count.
- No file under `.github/` references the inventory, command table or exec-audit receipt. The PR body's disclosure is accurate.

### Hosted state (`hosted_checks_snapshot.tsv`, inspection only)
- At snapshot time: 32 completed/success (including docs-check, docs-gates-0..4, bdd-conformance and full-ci-gate), 7 in progress and 36 queued (firmware and verilator jobs).
- 1 completed/skipped: Physical gPTP, nightly/manual. That is a skipped context, not hardware proof.
- The manager owns hosted and act acceptance.

## Findings

### RES-1: RESIDUE (lens Docs)
- **Location:** `docs/testing/TESTING.md:1199`.
- **What it is:** the reworded line `(the two inline capture taps) and the controller bench host (the controller and audio endpoint):` runs to 96 columns. Its paragraph (`:1196-1198`) is wrapped at 76 or fewer.
- **Authority/evidence:** the page's own paragraph wrapping. The style gate passes, so this is layout only.
- **Impact:** none on any measurement, test, claim or privacy rule. It is purely the paragraph's shape in source.
- **Required outcome (exact fix):** rewrap lines 1198-1199 as:
  - `the build box (UART, JTAG and the external CSR transport), the Ubuntu server`
  - `(the two inline capture taps) and the controller bench host (the controller`
  - `and audio endpoint):`
- **Verification:** `check_doc_style.py` and `check_em_dash.py --base <merge-base>` stay at 0.

### SUG-1: SUGGESTION (lenses Tests, Docs)
- **Location:** `scripts/docs_check.py` `IDENTITY_RULES`.
- **What it is:** nothing stops the removed tokens from coming back. Base `docs_check.py` passed with all 34 hits present, so no current rule covers these tokens.
- **Authority:** CONTRIBUTING.md section 6 (`CONTRIBUTING.md:608-614`) names a code-point-assembled identity rule plus a planted `scrub_selftest` fixture as the normal way to extend the list. #1028's frozen acceptance does not require a guard, so this is optional.
- **Outcome:** a follow-up issue adding the tap product and vendor, the two host labels and the switch model as identity rules, each with a planted fixture.
- **Verification:** the scrub self-test arm count rises, and a planted line fails the gate.

### SUG-2: SUGGESTION (lens Docs)
- **Locations:** `docs/integration/BUILDING.md:591`, `docs/testing/RUNNING_TESTS.md:233`, `docs/testing/TESTING.md:100` and `:1198`.
- **What it is:** these lines name the capture host "Ubuntu server", by its operating system rather than by its role. Also, CONTRIBUTING's canonical role phrase is "the bench AVB switch" (`CONTRIBUTING.md:595`), and the delta writes "the AVB switch".
- **Why this is not a finding:** "Ubuntu server" is not a hostname, and the issue text itself uses "the AVB switch".
- **Outcome (optional):** "the capture host" and "the bench AVB switch", for uniform role naming.

### SUG-3: SUGGESTION (lens Docs)
- **Location:** `docs/testing/RUNNING_TESTS.md:232`.
- **What it is:** "the controller and audio endpoint on the controller bench host" repeats "controller". The meaning is intact, and the label matches the BUILDING.md table.
- **Outcome (optional):** "the controller bench host (controller and audio endpoint), the inline capture taps on the Ubuntu server."

### SUG-4: SUGGESTION (lens Docs)
- **Location:** `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:123`.
- **What it is:** the cell now points at a directory in the private test repository plus a description, because the old filename carried the host labels. A reader there has to recognise the script by its description.
- **Outcome (optional):** if the private script is ever renamed neutrally, cite the new name. No change is needed in this PR.

### Wording residue checked and accepted
- The fixture label "inline-tap" (feature title and step docstring) sits beside "inline capture tap" in prose. Both are unambiguous.
- The Contents block of `REGISTER_MAP_CLASSES.md:39-41` moved wholly to `--`, as section 6.1 requires. The `~700–900` en dash on `:41` is U+2013 and outside the rule.
- The history-page edits change only the names and dashes on the touched lines. No historical claim, figure, date or verdict moved, as checked by reading every hunk.

## Lens coverage (applied this round, exact head)

The clean results, in findings format:

- **[R969] PASS Conformance** — artifacts: #1028 acceptance items A1-A3, `scan_head_touched.txt` (0/7 classes), `scan_head_tree.txt`, `packet_verify.txt` firmware lines, `ast_delta.txt`, `gates-head/SUMMARY.tsv`, `docs/history/v1/traceability/milan-v12.md:183`, `docs/history/v1/NXN_ARCHITECTURE.md:652`.
  - A1 is met.
  - A2 is met: ELFs identical; touched-tool self-tests pass, by the author's receipt for act_ci and by my rerun for the rest.
  - A3 is met.
  - No Milan or IEEE clause reference, register value or wire/file-format literal changed. Clause numbers 5.3.7.3, 5.3.7.2 and 5.5.2.7, and the CSR values, are byte-identical apart from the em-dash to `--` substitution.
- **[R969] PASS RTL** — artifacts: `git diff --stat c1c42843..0715cb20` (no path under `hdl/`, `syn/`, `configs/`, `sw/`), `hdl/ieee1722/aaf/KL_render_queue.sv:557` (`pw1_w` unchanged), the gitlinks of all six submodules equal to HEAD's tree, and the firmware manifests base==head.
  - No RTL, constraint, generated SoC input or firmware source is in scope, so there is nothing to apply the clock, reset, CDC or width checks to, and the byte-identity receipt confirms no build-input drift.
- **[R969] PASS Robustness** — artifacts: `scripts/act_ci.py:4896-4902` and `:15394-15403`, `scripts/check_baremetal_only.py:214-215` and `:1136-1140` with `remote_shell_probe.txt`, and `tb/tools/torture_campaign.py:1229`, `:6782-6786`, `:6992`, `tests/steps/torture_plan_steps.py:716`.
  - Each changed fixture literal still drives the same accept or refuse path.
  - The new addresses are valid IPv4. The detector does not depend on the address.
  - The label is display-only.
  - The 24-character prefix assertions are unchanged.
  - No negative, boundary or failure path lost its trigger.
- **[R969] PASS Tests** — artifacts: `gates-head/behave_touched.log` (231 scenarios), `gates-head/behave_full.log` (511), `gates-head/torture.log`, `gates-head/avtp_wire_truth.log`, `gates-head/baremetal_self.log` (867 arms), `ast_delta.txt`, and `tests/features/wire_truth_avtp.feature:274` (renamed scenario, no dangling reference).
  - No assertion, step text or arm expectation changed, so no test was weakened.
  - The renamed scenario still runs.
  - SUG-1 is optional.
- **[R969] PASS Docs** — artifacts: the 8 touched pages read hunk by hunk, plus `gates-head/em_dash.log`, `doc_style.log`, `docs_check.log`, `toc_check.log`, `toc_anchors.log`, `docs_inventory.log`, `doc_map.log`, `register_reference.log`, and the PR body.
  - Every neutral phrase keeps its sentence's meaning.
  - The ASCII-dash rule holds.
  - The PR body is accurate on scope, false positives and snapshot staleness, and it is free of the removed tokens.
  - RES-1 is RESIDUE only. SUG-2 to SUG-4 are optional.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1028 A1-A3; scans; AST delta; firmware manifests; history rows `milan-v12.md:183`, `NXN_ARCHITECTURE.md:652` | R969-2 | 0715cb206050c49a1745dd2d11e2fc0e1b74116b |
| RTL | CLEAN | diff stat (no `hdl/`/`syn/`/`configs/`/`sw/`), `KL_render_queue.sv:557`, six gitlinks, firmware base==head | R969-2 | 0715cb206050c49a1745dd2d11e2fc0e1b74116b |
| Robustness | CLEAN | `act_ci.py:4896-4902,15394-15403`; `check_baremetal_only.py:214-215,1136-1140` and probe; `torture_campaign.py:1229,6782-6786,6992`; `torture_plan_steps.py:716` | R969-2 | 0715cb206050c49a1745dd2d11e2fc0e1b74116b |
| Tests | CLEAN | behave touched 231 and full 511; tool self-tests; baremetal 867 arms; AST delta; renamed scenario | R969-2 | 0715cb206050c49a1745dd2d11e2fc0e1b74116b |
| Docs | CLEAN (RES-1 RESIDUE carried) | 8 pages by hunk; em-dash, style, docs_check, toc, anchors, inventory, doc-map, register-reference gates; PR body | R969-2 | 0715cb206050c49a1745dd2d11e2fc0e1b74116b |

## Real limits
- **act_ci self-test:** I did not run `scripts/act_ci.py --selftest`, which the brief forbids. Its head PASS is the author's receipt. My coverage of that file is the static analysis plus the AST probe.
- **Packet integrity:** no cryptographic signature exists on the packet. I verified it by its committed hash manifest only.
- **Firmware identity:** this rests on the author's base and head manifests, which I re-verified but did not rebuild. No LiteX SoC or bitstream build was done by anyone. That build is not needed for a change that touches no build input, but it is outside the evidence.
- **Hosted checks:** they were still running at snapshot time. I made no hosted or act acceptance claim. No manager source bank runs at this head, and none is claimed or inferred.
- **Physical calibration:** NOT RUN. The Physical gPTP context is a skip, not hardware proof.
- **Scope:** the review covers only this PR (`dev-soft-core`). The `dev` sibling (#1030) and the FPGA-gPTP change were not reviewed.
- **Clone state after probes:** clean.
  - `git status --porcelain` is empty, and `HEAD`/tree are the exact values above.
  - The index's `(mode, blob, path)` set equals `HEAD`'s tree.
  - All six gitlinks equal the recorded commits.
  - The only out-of-tree side effect is a `FETCH_HEAD` for the evidence commit.

## Pending manager duties
- Build and validate the current-dev merge candidate (source base `c1c42843`, live `dev` `e275d795`) with the builder and native banks, and link the receipts.
- Accept the hosted contexts at the exact head, including the firmware and verilator jobs still queued at snapshot, and the act replica.
- Decide on the act-slot Docker pool literal (`scripts/act_ci.py:739`, `:14124`, `:14415`): accept it as a stated false positive, or open a separate issue to make it configurable.
- Own the follow-up that satisfies #1028 A4, the `gptp-processor` pin bump to the FPGA-gPTP commit that removes the debug-probe serial. A serial is still present in the currently pinned submodule's history page, and the bump runs the RTL gates.
- Make the out-of-scope decision on the clock identities carrying a vendor OUI on the #117 evidence page (author HANDOFF decision 2). It is not in #1028's list and not in this diff.
- Close #1028 by hand once all three lanes and A4 land. The PR targets `dev-soft-core`, which is not the default branch, so `Closes #1028` will not fire.
- Schedule the next CI-image refresh for the `ci/image` snapshot digests.
- Carry RES-1 to the residue checklist.

R969-2 FINISHED
