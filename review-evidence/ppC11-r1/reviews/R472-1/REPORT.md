[R472] NEGATIVE - exact head 91cef52b3c56cc69f66966b004782a69d2940a46

# R472-1: internal independent review of processor PR #156 (lane C11; issues #27, #70, #75, #71 acceptance 1 and 3)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #156, branch `c11-docs-gates`.
- Exact head `91cef52b3c56cc69f66966b004782a69d2940a46`, tree `1033d92b04474001548689b20e1e0e4fe13a7966` (both checked in the review clone, `receipts/clone_integrity.log`).
- Source base `c050d97153dd0480ae741102c1647eeda9b7f273`. Diff reviewed: `c050d971..91cef52` (5 commits, 28 files, +783 / -131).
- Cleared context. Reconstructed from public state only, in this order: the parent's AGENTS.md §6 and CONTRIBUTING.md (this repository has neither), docs/README, the bodies and comments of issues #27, #70, #75 and #71 (including the lane-opening scope comment on #27), the authorities they cite (02, 01 F01.5, 08 F08.1, 09 §7/§8, the integrator guide, 00 REQ-REU-002/003 and REQ-DOC-001, `protocol_processor_top.sv`, `KL_pp_side_port.sv`, `KL_pp_nvm_port.sv`, `KL_acmp_talker.sv`), the diff and its commits, and then the public evidence: the PR body, the published lane evidence at `kebag-logic/milan-fpga@4a3ae4a1/review-evidence/ppC11-r1` (MANIFEST.json, HANDOFF.md, PR-BODY.md), and the exact-head hosted check runs.
- Prior public review findings on PR #156: **none**. The PR carries two review-start comments and no reviews or review comments. Issues #27, #70, #75 and #71 carry no findings either. Nothing to resolve or retain.

Verdict: **NEGATIVE**. Two MINOR findings are open: F1 (the ID gate misses an ID with no row when it is written as a braced list) and F2 (the figure gate's self-test claims more than it plants). Both are small and cheap to fix. Everything else in scope checked out. The architecture pages now match the landed ports. The three `hdl/`/`tb/` edits change comments only. The word-stream history is verbatim and its permalinks resolve. Rule 5 is untouched. The PNGs are gone. 09 §7 matches the Makefile and CI. The CI change is sound, and the hosted docs-gates job passed at the exact head.

## Findings

### F1: MINOR (Conformance, Robustness, Tests, Docs): `make ids` passes a braced list whose member is a hyphenated ID with no row

- **Where:** `scripts/check-ids.py:39` (`BRACES = re.compile(r"-\{([A-Z0-9, ]+)\}")`) and `scripts/check-ids.py:103-104`. When the brace pattern does not match, the use falls through to `elif text.startswith("-", end): ... "family"`. The claims are at `docs/README.md:88-89` ("a braced list (`T-ACMP-{CMD, DELAY}`) a row for each member") and `docs/architecture/09_verification.md:124`.
- **Authority and evidence:** #70 acceptance 1 is "a make check target fails when a P- or T- ID used under docs/, hdl/ or tb/ has no row in F01.5 / F08.1". A planted use was appended to `08_timing.md` in a disposable clone: `T-NVM-{RS-DEADLINE, RS-TYPO}`. `T-NVM-RS-TYPO` has no F08.1 row, yet `check-ids.py` passes with rc 0 and "OK". This is plant I5 in `receipts/gate_probes.log`. The brace class has no `-`, so the list is read as the family `T-NVM`. Any `T-NVM-…` row then satisfies it, and no member is checked. The hyphen-free control `T-MRP-{JOIN, TYPO}` is caught (I6). The same fallback reads any `<ID>-<lowercase>` continuation as a family: the issue's own stray `P-TX`, written as `P-TX-shaped`, passes (I7). Hyphenated members are a natural shorthand in this registry, which has multi-segment siblings such as `T-NVM-RS-DEADLINE` / `T-NVM-RS-AGGREGATE` and `T-BUDGET-AECP-TYP` / `-WC`. No use at the head has this form (`receipts/ids_forms_head.log`: every lenient-form use at the head is a real family or `P-…-1`), so the tree passes today for the right reason.
- **Impact:** the gate is documented as fail-closed on any P-/T- ID without a row, and on each member of a braced list. One plausible notation passes a missing row silently, which is the drift #70 exists to stop.
- **Required outcome:** treat a use as a family only for the documented forms, `-*` and a hyphen at the end of a line. Brace members may contain hyphens, and each one is checked. Any other `-{…}` or `-<text>` continuation is either parsed as an ID or fails closed. Add self-test cases for a hyphenated braced member with no row and for an ID followed by a lowercase hyphenated suffix.
- **Verification:** at the fixed head, plants I5 and I7 of `scripts/gate_probes.py` must give rc 1. Every other plant must keep its expected rc. `make check` stays rc 0 on the tree.

### F2: MINOR (Tests, Docs): the figure gate's self-test does not plant three faults that 09 §7 says it plants

- **Where:** `scripts/check-figures.py:173-189` (`SELFTEST_CASES`) against `docs/architecture/09_verification.md:125`, which says "…has an `<svg>` root and a `viewBox`, carries no `<image>` or `<foreignObject>` … The self-test plants each fault and must see it caught".
- **Authority and evidence:** under the AGENTS.md §6 Tests lens, each new test must be able to fail for the defect it claims to detect. I mutated the script and ran the mutant's own `--selftest` (`receipts/gate_probes.log`, mutants section). Eight of 11 mutants are killed. Three survive with selftest rc 0:
  - MF8: `<foreignObject>` is no longer checked.
  - MF9: a root that is not an SVG-namespace `<svg>` is accepted.
  - MF10: an empty hand-authored inventory is accepted.

  The production code handles these cases correctly today (plants G2, G3 and G6 are caught on the real tree). Only the self-test, the regression guard that `make check` runs first, misses them. So 09 §7 states a verification property that does not hold. That is a test claim, not wording.
- **Impact:** a later edit that drops any of those three checks keeps `make figures` and CI green, although 09 §7 says the self-test would catch it.
- **Required outcome:** add self-test cases for `<foreignObject>`, a non-SVG-namespace root, and an inventory section with no listed SVG. Alternatively, make the 09 §7 row state exactly which faults the self-test plants.
- **Verification:** rerun `scripts/gate_probes.py`. MF8, MF9 and MF10 must be KILLED (selftest rc 1), and `make figures` must stay rc 0 on the tree.

### R1: RESIDUE (Docs; wording only): 02 §2 rule 2 says the top has "no FIFO"

- **Where:** `docs/architecture/02_interfaces.md:105`: "the top has one clock and no FIFO".
- **Evidence:** the sentence is about the dual-clock MAC FIFOs, and the ownership it states is correct. Read literally, though, it contradicts 03 §2, which lists the top's per-engine dispatch FIFOs. Fixing it changes no measurement, figure, test, code, artifact or clause claim.
- **Exact fix:** "the top has one clock and no dual-clock FIFO".

### Suggestions (do not affect the verdict)

- **S1 (Tests/Robustness, CI):** `.github/workflows/hdl.yml:21` installs `wavedrom` unpinned. This line predates the PR, and the hosted run resolved `2.0.3.post3`. `wavedrom-check` compares renders byte for byte, so a new wavedrompy release could fail CI with no change in the source. Pin `wavedrom==2.0.3.post3`. Mermaid CLI is pinned at the top level (11.16.0), but its transitive dependencies float because there is no lockfile. Consider one if reproducibility matters.
- **S2 (Tests):** the `ids` self-test also misses three behaviours the code has. These are mutants MI5 (any tail, not just a numeric one, accepted after a real stem), MI8 (an empty master table accepted) and MI9 (a duplicate row accepted), all of which survive the self-test. Today the production code is right on each: plants I12, I15 and I16 are caught. Add planted cases for them. The 09 §7 `ids` row claims only that strays are planted, so this is not a finding.
- **S3 (Docs):** `02_interfaces.md:623` says `nvm_dev_req_o` is "held until `nvm_dev_gnt_i`". That matches the RTL port comment (`KL_pp_nvm_port.sv:157`), and the deadline that withdraws an ungranted request is stated a few lines below in the same section. "held until `nvm_dev_gnt_i` or withdrawn at the deadline (below)" would make the table complete on its own.
- **Observation, out of scope:** `docs/guides/integrator.md:216-217` uses short names `wr_done_i` and `wr_ready_i` for `resp_mem_wr_done_i` and `resp_mem_wr_ready_i`. This predates the PR, the file is a guide rather than an architecture page, and the PR does not touch these lines (`receipts/port_names_02_integrator.log`).

## Acceptance, item by item

| Issue | Item | Result | Evidence |
|---|---|---|---|
| #27 | architecture pages show only landed ports | met | All 151 distinct `*_i`/`*_o` names on `docs/architecture/*.md` are ports declared in `hdl/` (`receipts/port_names_arch_head.log`, rc 0); the scanner fails on a planted `rx_err_i` (`port_names_planted.log`). In 02, every name is a port of `protocol_processor_top` (`port_names_02_integrator.log`). The 02 §3 table (8 signals), §7 `host_*` table (7) and §8 `nvm_dev_*` table (15) match the top's declarations in name, direction and width (`protocol_processor_top.sv:286-295`, `:566-589`), and the top wires them to `KL_pp_nvm_port` (`:2907-2921`) and `KL_pp_side_port` (`:4644-4650`) |
| #27 | RX shows no backpressure | met | 02 §3 says "RX has no backpressure"; F02.3 is redrawn with `rx_valid_i`/`rx_data_i`/`rx_last_i` only (source and SVG checked; rendered and inspected). No `rx_ready`/`rx_err`/`rx_sof` remains on architecture pages or guides except the guide's "There is no `rx_ready`" |
| #27 | word-stream history discoverable | met | `docs/history/02-class-a-word-stream.md`. The paragraph, table and both waveform sources are verbatim from base (`receipts/history_verbatim.log`). The three permalinks at `c050d971` resolve on GitHub to the same blob ids as the local base, and the `#3-class-a--packet-streaming` slug matches the base heading (`history_permalinks.log`). It is linked from 02 §3, docs/README §1 and the root README |
| #27 | links and diagrams valid | met | `make check` at the head: links 1,152 OK, wavedrom 18 fresh, lint 41 Mermaid + 18 WaveDrom OK, figures OK (`receipts/make_check_head.log`, rc 0). F02.3, F02.4 and F02.7 were rendered and inspected. Their timing matches the RTL: TX stall holds the byte (`protocol_processor_top.sv:4536-4610`); the side port accepts in IDLE and its strobe comes at least one cycle later (`KL_pp_side_port.sv:128-219`) |
| #27 | extra: 02 §7 `host_*`, §8 `nvm_dev_*` | met | as above. The APB mapping sentence agrees with the RTL's own mapping comment (`KL_pp_side_port.sv:52-59`) |
| #70 | 1: a make target fails on any P-/T- ID without a row | **partly**: see F1 | Plants I1-I4 and I8-I16 behave as expected: strays in docs, RTL comments, new untracked tb files, SVGs and the history page are caught; deleted rows, duplicate rows and unfindable or empty tables fail. Plant I5 (a braced member with a hyphen) is missed |
| #70 | planted control | met | The executor's controls (HANDOFF §3), plus my own I1-I16 |
| #70 | 2: MAAP rows; 02 §4.2 carries no values | met | F01.5 rows at `01_overview.md:183-184`. Defaults equal the RTL (`KL_acmp_talker.sv:140` = 1024, `:180` = 10 000), and neither is a top parameter. 02 §4.2 has no 1024 / 10 s / 1800 / 15 s / 500 / 600 / 30 s value left (grep). The third stray had zero uses at base (I13 reproduces the base's 39 uses of 3 IDs) |
| #70 | 3: docs/README §2 = 09 §8 | met | Both say that `make check` enforces `ids` and `params` and nothing more, and that the value scan is still to add (`docs/README.md:83-96`, `09_verification.md:158-162`, `:398-400`) |
| #70 | 4: in docs-gates CI | met | `hdl.yml` docs-gates runs `make check`. The hosted run at the exact head (job 111475936324) printed the `ids` lines (`receipts/hosted-docs-gates-111475936324.log`) |
| #75 | 1: CI runs make check, Mermaid CLI pinned | met | `npm install --prefix "$HOME/mermaid-cli" @mermaid-js/mermaid-cli@11.16.0`; the hosted log shows `mmdc --version` = 11.16.0 and `lint: 41 mermaid + 18 wavedrom blocks checked, OK`. The job has no other network step, and the pip line predates the PR (S1) |
| #75 | 2: hand-authored SVG is a listed class with its rule | met | `docs/README.md` §3, the "Hand-authored SVG" and "Nothing else" bullets; `docs/diagrams/README.md` |
| #75 | 3: five PNGs removed | met | `git ls-files` has 0 `.png`. No reference to them remains (grep; the only `.png` strings are the gate's own self-test fixtures and the scratch-render command) |
| #75 | `make figures` refuses unlisted files | met | Plants G1-G9 are all caught (PNG, foreignObject, non-namespaced root, a file in src/, a nested dir, missing inventory, a missing draw.io export, an unlinked figure, a stray txt). Self-test strength: F2 |
| #75 | 4: 09 §7 matches CI | met | The 09 §7 table lists exactly the Makefile `check` prerequisites (lint, wavedrom-check, links, matrix, modmatrix, params, ids, figures, stale), and CI runs `make check` |
| #71 | 1: integrator §3, RX FIFO complete FCS-good frames | met | `integrator.md:135-146`, anchor `rx-frame-atomic`; §1 points there |
| #71 | 3: REQ-REU-003 cells name the integrator as FIFO owner | met | `00_MILAN_COMPLIANCE_REVIEW.md:531` |
| #71 | rule 5 untouched (the #81/#84 lane's) | met | 02 §2 rule 5 is byte-identical at base and head (extracted and diffed) |
| scope | hdl/tb edits comment-only | met | `receipts/comment_only.log`, rc 0. Comment-stripped preprocessed sources are identical at base and head: `verilator -E -P` (pinned 5.050, wrapper sha256 `905795b9…e92f`) for `KL_pp_trace_ring.sv` (51 lines, `fabfdf23…`) and `KL_pp_tx_slots.sv` (204, `6ee60459…`); `g++ -fpreprocessed -dD -E -P` for `tb/tx_slots/sim_main.cpp` (477, `90f51caa…`). These match the executor's published hashes. The fourth touched file, `tb/tx_slots/README.md`, is documentation |
| scope | CI change sound | met | Pinned top-level install into `$HOME`, `.bin` appended to `GITHUB_PATH`, no global or privileged write, no secrets, no `curl \| sh`. The existing `lint-diagrams.sh` puppeteer config supplies `--no-sandbox`, and the hosted job succeeded |

## Lens results

| Lens | Result | Artifact examined at the head | Against |
|---|---|---|---|
| Conformance | **UNCLEAN** (F1) | each issue's acceptance list (table above); 02 §3/§7/§8 tables against the `protocol_processor_top.sv` declarations; F01.5 rows against `KL_acmp_talker.sv` defaults | #27/#70/#75/#71 bodies and the #27 scope comment |
| RTL | CLEAN | the three comment-only edits (preprocessed identity); `KL_pp_side_port.sv:128-219` (accept, strobe, `rdata` zero rules) against F02.7 and the 02 §7 table; `protocol_processor_top.sv:4536-4610` (TX stall, frame-atomic shim) against F02.4; `KL_pp_nvm_port.sv:60-177` against the 02 §8 device-face table (op codes 0/1/2, ERASE length 0, one-cycle done/err, informational busy); `lint_hdl.sh` 41/41 OK; tb/tx_slots 95/95 PASS; `gen_matrix --check` OK | existing module and interface contracts; no RTL behaviour change (scope) |
| Robustness | **UNCLEAN** (F1) | `check-ids.py` and `check-figures.py` under 25 fault plants (`receipts/gate_probes.log`); the lenient-form inventory at the head (`ids_forms_head.log`); missing, empty and duplicate master tables; untracked and ignored files | the gates' documented fail-closed contracts (docs/README §2/§3, 09 §7) |
| Tests | **UNCLEAN** (F1, F2) | both self-tests under 22 single-behaviour mutants (16 killed, 6 survive: MF8, MF9, MF10 → F2; MI5, MI8, MI9 → S2); `make check` rc 0 locally and in the exact-head hosted docs-gates job | AGENTS.md §6 Tests lens; 09 §7 claims |
| Docs | **UNCLEAN** (F1, F2; R1 is residue) | 02, 01 F01.2 note and F01.5, 03 §2/§8, 07 §5.5, 09 §7/§8, docs/README §1-§3/§6, the diagrams README, the HDL and integrator guides, the history page, the root README, 00 REQ-REU-002/003 and REQ-DOC-001; three redrawn waveforms rendered and inspected; F01.2 drawio placement of the FIFOs inside the MAC clock-domain boxes, which confirms the new note | AGENTS.md §6 Docs lens; docs/README single-source and figure rules |

## Ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue acceptance lists; 02 §3/§7/§8 vs `protocol_processor_top.sv`; F01.5 vs `KL_acmp_talker.sv`; 00 rows | R472-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| RTL | CLEAN | comment-only proof; `KL_pp_side_port.sv`, `KL_pp_nvm_port.sv`, top TX shim vs F02.4/F02.7/§8 tables; lint 41/41; tx_slots 95/95 | R472-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| Robustness | UNCLEAN (F1) | 25 gate plants; lenient-form inventory | R472-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| Tests | UNCLEAN (F1, F2) | 22 self-test mutants; local `make check`; hosted docs-gates log | R472-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |
| Docs | UNCLEAN (F1, F2) | every changed doc; history verbatim and permalinks; rendered waveforms | R472-1 | 91cef52b3c56cc69f66966b004782a69d2940a46 |

## Commands and receipts (all in the foreground, each with its own log and rc)

| Receipt | rc | Result |
|---|---:|---|
| `receipts/make_check_head.log` | 0 | lint 41+18; wavedrom 18; links 1,152; matrix 115/17; modmatrix 94/0; parameters 28/28/28; ids selftest 9, ids 488 files / 91 IDs; figures selftest 10, figures 3/18/5; stale (wavedrom 2.0.3.post3 in a scratch venv; Mermaid CLI 11.16.0) |
| `receipts/lint_hdl_head.log` | 0 | 41 `LINT OK` (pinned Verilator 5.050) |
| `receipts/tx_slots_head.log` | 0 | 95 checks, 95 PASS (the suite whose harness comment changed) |
| `receipts/gen_matrix_head.log` | 0 | 94 rows, 0 untested |
| `receipts/comment_only.log` | 0 | 3 compiled files identical after preprocessing |
| `receipts/port_names_arch_head.log` / `_base.log` / `_planted.log` / `port_names_02_integrator.log` | 0 / 0 / 1 / 1 | head clean; the planted name is caught; the guide's pre-existing short names are noted out of scope |
| `receipts/ids_forms_head.log` | 0 | lenient forms at the head: 6 families and 2 `-1` uses, all legitimate; a naive independent scan finds no other ID without a row |
| `receipts/gate_probes.log` | 0 | 25 plants, 24 as expected (I5 is F1); 22 mutants, 6 survive (F2, S2); the probe clone is restored clean after each step |
| `receipts/history_verbatim.log`, `history_permalinks.log` | n/a | verbatim; 3/3 blob ids match |
| `receipts/hosted-docs-gates-111475936324.log`, `-111475927418.log`, `hosted_check_runs.tsv` | n/a | exact-head hosted docs-gates success (pull_request and push events); portability success; suites in progress at 2026-10-04T16:24Z |
| `receipts/clone_integrity.log` | n/a | after the probes, the review clone is at HEAD = exact head; index tree = `1033d92b…`; worktree and index equal HEAD; 0 blob-hash mismatches over 513 tracked files (496 × 100644, 17 × 100755); this repository has 0 gitlinks and no `.gitmodules`, so there is no submodule gitlink to verify; the one ignored entry, the reviewer's own `scripts/__pycache__/`, was removed |

Scripts: `scripts/comment_only.sh`, `scripts/port_names.py`, `scripts/ids_forms.py`, `scripts/gate_probes.py`. Every probe ran in a disposable clone under `scratch/`, never in the review clone. Redaction: one local install prefix (`receipts/REDACTIONS.txt`).

## Real limits

- I did not run the full processor suite bank (`run_suites.sh`), Yosys, the parent consumer set of 17, the builder or the mutation campaigns. They were not permitted, and they are not needed for a change that the comment-only proof shows leaves RTL and testbench behaviour unchanged. I rely on the manager's published source banks for those.
- Hosted evidence: I inspected the docs-gates and portability jobs at the exact head, both executed and successful. The suites job was still running when I looked. I did not run act or Docker.
- Physical calibration: NOT RUN. It does not apply to a docs/scripts/CI change, and no hardware was used.
- The `*_i`/`*_o` port check accepts any port declared anywhere under `hdl/`. That is the criterion this assignment set. For 02 I also checked each name against the top itself.
- My plants cover the forms listed above. They do not prove the ID gate complete for every notation.

## Pending manager duties

- Carry F1 and F2 to the executor. Re-review is required at the fixed head.
- Carry R1 to the residue checklist (exact fix above).
- Build and validate the final current-dev candidate at the merge turn: source base `c050d971` onto live dev `fea346e7`. That includes the parent consumer set with the processor gitlink at the candidate and coordination with PRs #154 and #155 and the #81/#84 lane (for any new T-ID rows).
- Accept the hosted and act results, including the exact-head suites job that was in progress.
- Close #71 only once the #81/#84 lane delivers acceptance 2. This PR says "Relates to #71".

R472-1 FINISHED
