# HANDOFF: #797 D0 round 4 (R741-3 and R742-3 on PR #815), executor [A706d]

Status: **REVIEW READY** at head `8d8c2e366a2d49506b91a195de0094a440e7bc39`, tree `24d3429b66ec52b7fb48782fbb78d289abab668b`, local branch `797-d0-audit`, not pushed.

- Three commits on top of `808602e0`, no merge, no rebase, no amend, no force. PR #815 still points at `808602e0`.
- origin is `https://github.com/kebag-logic/milan-fpga.git`. The lane branched from dev `1e80128f`. `git merge-base --all origin/dev HEAD` gives the one base `1f29f189`, and `git ls-remote` read dev at `1f29f189` after the gates.
- `protocol-processor` show-toplevel and origin were verified before git commands inside it. Pins are unchanged: processor `a9e84b66`, gPTP `135afd04`.
- Reports: R741-3 and R742-3. Round 3 handoff: `../797-a706c/HANDOFF.md`.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6564104249
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6565033575

## Commits (one-line subjects, no body, no trailers)

| Commit | Answers | Subject |
|---|---|---|
| `2f87911f` | F1 | Cite the processor's top by file name and submodule in D0-063 to D0-065, so the derived source-list gate passes with its lines kept (#797) |
| `acc10192` | R742-3 F2, R741-3 R3 | Search past underscore emphasis, link syntax and a statement's closing punctuation, and record each tail-carrying quote's own sentence under also, so every copy form R742-3 planted gets a row (#797) |
| `8d8c2e36` | R741-3 R2, R742-3 R1 | Cite the PROBING_COMPLETED test at its own line in D0-064 and name the firmware file of nvm_commit() in D0-024 (#797) |

## Every finding and residue, with file:line and its verification

| Item | Change at the head | Verification |
|---|---|---|
| **F1 BLOCKER (shared).** The literal processor path made `scripts/pp_srcs.py --check` fail | `scripts/docs_inventory.json:476,477,483,484,490,491`: the six literals now read `protocol_processor_top.sv` in the `protocol-processor` submodule, with the same line numbers. `scripts/pp_srcs.py` and its `PROSE_OK` are not touched. The audit page was regenerated in the same commit | `receipts/gates/rtl-fast/verilator-lint__ci_step_8.log`, rc 0: "46 tracked source(s) derived; no build input carries a literal copy (self-test passed)". `receipts/verify/citations-at-head.txt`: 0 literals left, and exactly one path of that name in the submodule (`hdl/top/protocol_processor_top.sv`). Inventory gate rc 0: `receipts/gates/docsyml/docs-gates-0__gate_46.log`. Cited-path gate rc 0: `docs-gates-0__gate_43.log` |
| **R742-3 F2 MINOR.** Underscore emphasis | `scripts/docs_inventory.py:136` strips `_` that opens or closes emphasis, and keeps it inside a word. Arms `:891` and `:892` | `receipts/probes/r742-probe-e2e.txt`, "underscore emphasis": 1 row, stale. Mutants `underscore-emphasis-kept`, `inner-underscore-stripped`, `opening-underscore-kept`, `closing-underscore-kept`: KILLED (`receipts/probes/mutants-final-head.txt`) |
| **R742-3 F2.** One word as a Markdown link | `scripts/docs_inventory.py:137` `LINK_RE`, inline and reference form. `:367` applies it to a line or statement and `:381` to the whole page first, so link text wrapped over two lines is found with its line numbers kept. Arms `:893` and `:894-895` | Same receipt, "one word as a link": 1 row, stale. Mutants `needle-keeps-link-syntax`, `page-link-judged-per-line`, `reference-link-kept`: KILLED |
| **R742-3 F2.** A sentence ended differently from its recorded quote | `scripts/docs_inventory.py:372-374` `needle_of()` drops the closing `.,;:`, used at `:389`, `:403`, `:408`. Arm `:896` | Mutant `sentence-end-kept`: KILLED |
| **R742-3 F2.** A quote carrying the next clause's words | `scripts/docs_inventory.json` `also` at `:27` D0-002, `:51` D0-005, `:180` D0-024, `:190` D0-025, `:263` D0-035, `:273` D0-036 (two), `:354` D0-047, `:434` D0-058, `:444` D0-059, `:468` D0-062. The population was read from `tools/tail_census.py` and each quote's source line. Arms `:897` (the miss without `also`) and `:898` | `r742-probe-e2e.txt`: the D0-025, D0-035, D0-059 and D0-002 arms each give 1 row, stale. All nine planted arms give a row and a stale page; before this they gave 3 |
| **R742-3 F2.** Claim and behaviour agree | `scripts/docs_inventory.py:30-35` states what is normalised and what is not | `receipts/verify/citations-at-head.txt` prints the text. `r741-plant-probes.txt`: inline HTML, a backslash break and a paraphrase give no row, as the docstring says |
| **R741-3 R1.** PR body said "not pushed" | `PR-BODY.md`, Status and Known limitations: the sentence is gone and the hosted result is stated | That text; `gh run view 41349428937` read `rtl-fast cancelled` at `808602e0`, and `gh pr checks 815` lists `verilator-lint` and `docs-check` as failed |
| **R741-3 R2.** D0-064 citation one line short | `scripts/docs_inventory.json:484`: "(lines 3621-3622)" | `citations-at-head.txt` prints both lines; the status test is on 3622. No "(line 3621)" remains |
| **R741-3 R3.** "emphasis" meant asterisks only | `scripts/docs_inventory.py:32-33` and `PR-BODY.md` | F2 makes underscores normalised too, so the words are "asterisk and underscore emphasis", not the report's "asterisk emphasis". The arms above hold them to it |
| **R742-3 R1.** D0-024 line read as the wrong file | `scripts/docs_inventory.json:178`: "`nvm_commit()` (`sw/firmware/milan_baremetal/milan_baremetal.c` line 1405)" | `citations-at-head.txt` prints line 1405: `static int nvm_commit(const char *why)` |

**Suggestions.**

- Taken: R741-3 S2 in part. `:347` now refuses an `also` that normalises to nothing, with arm `:903` and mutant `nothing-left-accepted` KILLED. This round's normal form makes more strings normalise to nothing, such as `_` and `.`. `also: ["the"]` is still accepted, and it shows loudly in the diff.
- Not taken, because the assignment does not extend coverage:
  - R741-3 S1's HTML and backslash forms, and D0-013 wrapped before its `+` (246 planted forms, 2 not found, `r741-plant-probes.txt`).
  - R741-3 S3 and R742-3 S1, the surviving mutants. The reviewers' own scripts at this head report the same survivors: `no-nfkc`, `no-whitespace-collapse`, `held-not-updated`, `origin-rows-use-search`, and quote or ordered markers (`r741-mutants-final-head.txt`, `r742-mutants-final-head.txt`). Their patterns for the rewritten lines print `NOT APPLIED` or `NOT-APPLICABLE`; `mutants-final-head.txt` carries those at the new spelling.
  - R741-3 S4 and R742-3 S2, the second copy of D0-066's claim. `sw/trace/test_trace_roundtrip.py` is not a Markdown page. `findings/README.md` already records it for its owner.

**Real tree.** The generator and data changes add no row and remove none: 212 documents, 166 current, 25 stale, 21 obsolete; 65 recorded findings and 22 copy rows make 87 rows. The audit page differs from `808602e0` only in the D0-024, D0-063, D0-064 and D0-065 cells. `r742-probe-search.txt` and `r741-independent-search.txt` report wider-only hits, each a D0-040 or D0-058 statement on a page whose row of the other already holds those words. That is the designed "already held" rule.

**Module limit.** `scripts/docs_inventory.py` is 999 lines against the 1,000 limit of `check_py_idiom.py`. Room came from inlining `relative()` (`:431`, `:509`), and from packing comments, docstrings, `RULES`, `render()` lists and `fixture()` rows. A rendered-page diff before and after was empty. `ci/image/command-table.json:13701` carries the new digest, and `tools/walk_inventory_step.py` accepts it (`receipts/verify/walk-inventory-step.txt`, rc 0). `ci_tool_inventory.py --check` is not in `docs.yml` or `rtl-fast.yml` and was not run.

## Open decisions and limits

1. **Hosted CI has not run on this head; it is not pushed.** Protected contexts are still to be read after the push. The local replica was not run. No Vivado, sweep or hardware.
2. **Maintainer decision: what "Mark II default" names.** Unchanged from round 3: D0-001, D0-033, D0-056 and nine copy pages depend on it.
3. **The owner additions of 2026-10-30 are not applied**, as in round 3. The two scope-addition statements that do not match the code still need a decision (`findings/README.md`).
4. **An `also` spelling can be broader than the false claim.** D0-002's own clause, "clock-source selection now reaches the media plane's wrapper", is true on its own; the report's planted form requires it. A copy that continues differently gets a row for the area lane to judge. No page does this today.
5. **Sampling is not extended.** Round 2's read-only statements and dev's new lines on release-facing pages stay as round 3 states them.

## Generator and freshness gate

- Generator: `python3 scripts/docs_inventory.py --write`. Gate: `--check` (rc 1 stale or rule broken, 2 refused). Self-test: `--selftest`, 50 controls, each through `main(["--check"], fixture)` on a Git-initialised fixture.
- **Planted stale-page mutant, real tree.** `tools/probe_e2e.sh`, R742-3's script, appends one line to `docs/guides/BOARD_DEPLOYMENT.md` on a clone of the head. Every arm gives `--check` rc 1, then `--write` and `--check` rc 0 (`receipts/probes/r742-probe-e2e.txt`).
- **Generator mutants:** `tools/mutate_inventory.py` counted 45, killed 45; two equivalents are not counted and the hook-environment probe passes (`receipts/probes/mutants-final-head.txt`).
- **Named mutant, cross-page search disabled:** KILLED in the same receipt.

## Findings per area

Generated by `python3 scripts/docs_inventory.py --findings-dir findings` from a clone of the head; notes in `findings/README.md`.

| Area | Rows | Copy rows | File |
|---|---:|---:|---|
| reference (with integration) | 57 | 3 | `findings/reference.md` |
| overview and guides | 14 | 3 | `findings/overview-and-guides.md` |
| design | 6 | 6 | `findings/design.md` |
| testing and CI | 1 | 1 | `findings/testing-and-ci.md` |
| archive (recorded, not to be rewritten) | 9 | 9 | `findings/archive.md` |
| **total** | **87** | **22** | |

## Gates

All on clean clones of `8d8c2e36`, never piped. Runner and verifier: `receipts/gates/tools/`, copied from the assigned tools with this lane's paths (`run_docs_yml.py`, `verify_docs_yml.py`, `not_run.json`); `run_rtl_fast.py`, `select_rtl_fast.py` and `verify_rtl_fast.py` are their counterparts for `rtl-fast.yml`.

| Gate | Result | Receipt |
|---|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 65 steps rc 0, 31 not run with a stated reason, 0 bad; verifier rc 0 | `receipts/gates/docs-yml-table.md`, `receipts/gates/docsyml/` |
| Every step of `.github/workflows/rtl-fast.yml` that reads `scripts/` or `docs/` | 17 steps rc 0, 28 not run with a stated reason, 0 bad; verifier rc 0 | `receipts/gates/rtl-fast-table.md`, `receipts/gates/rtl-fast/` |
| `git diff --check` against the merge base `1f29f189` | rc 0 | `receipts/gates/lane/diffcheck.log`, `.rc` |

**How the selection was made.** `select_rtl_fast.py` takes a step whose own text names `scripts/` or `docs/`, or that runs a tracked file naming them. So the Yosys source-list steps and the firmware steps count, not only the `pp_srcs.py` step. `verify_rtl_fast.py` fails on any such step with neither an rc of 0 nor a reason.

**Attempts that failed before the logged pass, all kept in `receipts/gates/env-first-attempts/`.** Each failure is in my runner's environment, and each log shows its cause. None concerns the head's content.

| Step | Log's cause | What changed |
|---|---|---|
| `docs-gates-1` `ci_step_13`, then `gate_25_0` | Two parallel jobs shared one scratch `HOME` and raced on the RV32 SDK directory (`FileExistsError`); the builder leg then found no adopted SDK | Job rerun fresh after the SDK was installed |
| `docs-gates-0` `gate_13` | `wavedrom` missing from my scratch venv; `not_run.json` assumes the venv carries it, as the hosted step installs it | Installed `wavedrom==2.0.3.post3`, job rerun fresh |
| `firmware-boundary` `ci_step_9`, twice | `No module named 'migen'`, then `'litex'` | The LiteX interpreter put first on `PATH` for this job (`LITEX_BIN` in `run_rtl_fast.py`), job rerun fresh |
| `docs-gates-0` `ci_step_55` | "source dependency origin differs: third_party/tsn-c-stack". This is the hosted-context recorder the assigned list excludes as `ci_step_54`; the runner sets submodule origins to the local clones | Added to `not_run.json` under this workflow's id, with the reason. `receipts/gates/docsyml/docs-gates-0__DONE` therefore reads `failed 1`; the verifier's table is the tally |

The REVIEW READY comment says "four steps". This table has four rows, and the logs show five steps, because the `docs-gates-1` row holds two. Existing comments are not edited, so the count is corrected here.

**Other differences from the hosted run.**

- `/opt/verilator/bin` is the pinned Verilator's directory on this host; `run_rtl_fast.py` substitutes it in the step text.
- `changes/scope` runs in the workflow's replay form (`ACT=true`, base `refs/remotes/origin/dev` at `1f29f189`).
- Yosys 0.66 and the host's sv2v were on `PATH`; the install steps were not run.
- `docs-gates-2__gate_41.log` was over 200 KB, so it is a `.sha256.txt` record.

## Resources

Single Python processes and the gate jobs in parallel. `free -g` read available memory at 41 GB at its lowest; the unit's own peak was not sampled. Host load average reached about 180, shared with other lanes. No Vivado, sweep or hardware.

## Docs workflow gate table

| Job | Step | Name | rc | Log |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | `wire-accountability__ci_step_1.log` |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | `wire-accountability__ci_step_3.log` |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | `wire-accountability__ci_step_4.log` |
| wire-accountability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 | `docs-check-no-git__ci_step_1.log` |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | `docs-check-no-git__ci_step_2.log` |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | `docs-check-no-git__ci_step_3.log` |
| docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-0__ci_step_1.log` |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | `docs-gates-0__gate_1.log` |
| docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | `docs-gates-0__ci_step_5.log` |
| docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | `docs-gates-0__ci_step_7.log` |
| docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | `docs-gates-0__gate_7.log` |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | `docs-gates-0__gate_8.log` |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | `docs-gates-0__gate_9.log` |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | `docs-gates-0__gate_10.log` |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | `docs-gates-0__gate_11.log` |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | `docs-gates-0__gate_12.log` |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | `docs-gates-0__gate_13.log` |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | `docs-gates-0__gate_14.log` |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | `docs-gates-0__gate_15.log` |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | `docs-gates-0__gate_16.log` |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | `docs-gates-0__ci_step_21.log` |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | `docs-gates-0__gate_18.log` |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | `docs-gates-0__gate_19.log` |
| docs-gates-0 | ci_step_25 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | `docs-gates-0__gate_21.log` |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-0__ci_step_28.log` |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | `docs-gates-0__gate_24.log` |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | `docs-gates-0__gate_26.log` |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | `docs-gates-0__gate_27.log` |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | `docs-gates-0__gate_28.log` |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | `docs-gates-0__gate_29.log` |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | `docs-gates-0__gate_30.log` |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | `docs-gates-0__gate_31.log` |
| docs-gates-0 | gate_32 | Port contract gate | 0 | `docs-gates-0__gate_32.log` |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | `docs-gates-0__gate_33.log` |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | `docs-gates-0__gate_34.log` |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | `docs-gates-0__gate_35.log` |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | `docs-gates-0__gate_36.log` |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | `docs-gates-0__gate_37.log` |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | `docs-gates-0__gate_38.log` |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | `docs-gates-0__gate_39.log` |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | `docs-gates-0__gate_40.log` |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | `docs-gates-0__gate_43.log` |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | `docs-gates-0__gate_44.log` |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | `docs-gates-0__gate_45.log` |
| docs-gates-0 | gate_46 | Documentation inventory freshness gate | 0 | `docs-gates-0__gate_46.log` |
| docs-gates-0 | gate_47 | AEM store generator self-test | 0 | `docs-gates-0__gate_47.log` |
| docs-gates-0 | gate_48 | Sweep/build shape gate | 0 | `docs-gates-0__gate_48.log` |
| docs-gates-0 | gate_49 | Deploy shape gate | 0 | `docs-gates-0__gate_49.log` |
| docs-gates-0 | gate_50 | Entity shape gate | 0 | `docs-gates-0__gate_50.log` |
| docs-gates-0 | ci_step_53 | Fetch inventory dependencies | 0 | `docs-gates-0__ci_step_53.log` |
| docs-gates-0 | gate_51 | CI scheduling and evidence controls | 0 | `docs-gates-0__gate_51.log` |
| docs-gates-0 | ci_step_55 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context; this workflow's id for the step 829's list names ci_step_54. Tried once: it refuses on the runner's local submodule origin (env-first-attempts/docs-gates-0__ci_step_55.log) |
| docs-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-1__ci_step_1.log` |
| docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 | `docs-gates-1__ci_step_3.log` |
| docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs-gates-1__ci_step_5.log` |
| docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-1 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs-gates-1__ci_step_9.log` |
| docs-gates-1 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-1__ci_step_13.log` |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | `docs-gates-1__gate_25_0.log` |
| docs-gates-1 | ci_step_15 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-2__ci_step_1.log` |
| docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 | `docs-gates-2__ci_step_3.log` |
| docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs-gates-2__ci_step_5.log` |
| docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-2 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs-gates-2__ci_step_9.log` |
| docs-gates-2 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-2__ci_step_13.log` |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | `docs-gates-2__gate_25_1.log` |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | `docs-gates-2__gate_41.log` |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | `docs-gates-2__gate_42.log` |
| docs-gates-2 | ci_step_17 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-2 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check | ci_step_1 | Set CPU-derived job budgets | NOT RUN | this job has no local gate |
| docs-check | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only docs-check's hosted verify uses |
| docs-check | ci_step_6 | Require every gate exactly once | NOT RUN | verifies uploaded hosted receipts; this job's gates ran above |
| docs-check | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration, no local gate |
| ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | cancels a hosted run |

65 steps ran, 31 not run with a reason, 0 bad

## rtl-fast gate table

| Job | Step | Name | Reads | rc | Log |
|---|---|---|---|---:|---|
| changes | scope | Classify the change conservatively | direct | 0 | `changes__scope.log` |
| changes | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | direct | 0 | `verilator-lint__ci_step_7.log` |
| verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | direct | 0 | `verilator-lint__ci_step_8.log` |
| verilator-lint | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| bdd-conformance | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| yosys-tool | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | through syn/yosys/run.sh | 0 | `yosys-elaboration__ci_step_7.log` |
| yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | through syn/ooc/dp_srcs.py, syn/ooc/pp_resource_gate.py | 0 | `yosys-elaboration__ci_step_8.log` |
| yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | through syn/yosys/ooc_selftest.py | 0 | `yosys-elaboration__ci_step_9.log` |
| yosys-elaboration | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| publication-census | ci_packages_3 | Resolve exact package downloads 3 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| publication-census | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | through sw/firmware/gtest/tally_selftest.py | 0 | `firmware-unit__ci_step_7.log` |
| firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-unit__ci_step_9.log` |
| firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | through sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py | 0 | `firmware-unit__ci_step_11.log` |
| firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | through sw/firmware/gtest/fw_coverage.py | 0 | `firmware-unit__ci_step_12.log` |
| firmware-unit | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-control-mutants__ci_step_8.log` |
| firmware-control-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-aecp-mutants__ci_step_8.log` |
| firmware-aecp-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-srp-mutants__ci_step_8.log` |
| firmware-srp-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-boundary__ci_step_8.log` |
| firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | through sw/firmware/ctrl/test/ctrl_boundary.py | 0 | `firmware-boundary__ci_step_9.log` |
| firmware-boundary | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-verilator__ci_step_13.log` |
| firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | through sw/firmware/ctrl/test/ctrl_boundary.py | 0 | `firmware-verilator__ci_step_14.log` |
| firmware-verilator | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | ci_collect | Collect actual runtime evidence | direct | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_observe | Observe the first failed job | direct | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | direct | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | direct | NOT RUN | cancels a hosted run |

17 steps ran, 28 not run with a reason, 0 bad
