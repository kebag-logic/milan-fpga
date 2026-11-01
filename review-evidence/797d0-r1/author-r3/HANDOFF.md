# HANDOFF: #797 D0 round 3 (R741-2 and R742-2 on PR #815), executor [A706c]

Status: **REVIEW READY** at head `808602e08daee5e86ae21026bbaf2f9114db077a`, local branch `797-d0-audit`, not pushed.

- Seven commits on top of `3e6d92c1` (one merge, six on top), no rebase, no amend, no force.
- origin is `https://github.com/kebag-logic/milan-fpga.git`. The lane branched from dev `1e80128f`; dev `1f29f189` is merged and is still the live tip. `git merge-base --all origin/dev HEAD` gives the one base `1f29f189`.
- `protocol-processor` and `gptp-processor` show-toplevel and origin were verified before git commands inside them. Merged pins: processor `a9e84b66`, gPTP `135afd04`.
- Assignment: issuecomment-6525276746 (D0 round 3). Reports: R741-2, R742-2. Round 2 handoff: `../797-a706b/HANDOFF.md`.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6562932764
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6563763608

## Open decisions and limits

1. **Maintainer decision: what "Mark II default" names.** D0 records it as contradicting the build (`--ctrl-mailbox` is off by default). `REQUIREMENTS.md:27` is normative, and R741-2 calls either reading defensible. All 13 pages now carry one judgement, so one answer settles them. If it names the design placement, delete D0-001, D0-033 and D0-056: nine pages return to current, and the other four keep other findings.
2. **The rule finds the same statement, not a paraphrase.** Probe p07 shows the limit. The six `also` spellings on D0-001 are hand-collected by `git grep`; a new paraphrase is caught only once recorded.
3. **Removing an entry removes its copy rows.** The page says to remove an entry only once no copy row remains. No gate enforces that.
4. **The owner additions of 2026-10-30 13:33 and 13:40 are not applied** (style-gated and diagram columns, "current only when that count is zero"). They are not in this assignment, and R741-2 left the decision with the manager.
5. **Sampling is not extended.** Round 2's 823 read-only statements stay read-only. Dev's new lines on release-facing pages were not checked statement by statement: I read the deltas of eight small pages (`README.md`, `REQUIREMENTS.md`, `SYSTEM_INTEGRATOR`, `INTEGRATION_GUIDE`, `PORTING_GUIDE`, `BOARD_DEPLOYMENT`, `MILAN_FEATURE_STATUS`, `MILAN_COMPLIANCE_MATRIX`) and did not read those of `BUILDING`, `BAREMETAL_FIRMWARE`, `SUBMODULES` and the gPTP guides. The page keeps "checked at dev `1e80128f`" for statements and adds "cite source lines at dev `1f29f189`" for citations.
6. **Not run:** hosted CI, the local `act` replica (it needs a pushed head), builder and source banks. No Vivado, sweep or hardware.
7. **`ci_tool_inventory.py --check` refuses**, at this head and at live dev, on the same unrelated stale digest (`sw/builder/endstation_builder.py`). The same walker on the inventory step alone accepts this head. So `ci/image/tool-inventory.json` is not regenerated.
8. The reviewers' optional suggestions are not taken: R741-2 S1 (its mutant `parser-cells-ignore-escapes` still survives), S2, S3 and R742-2 S1.

## Commits (one-line subjects, no body, no trailers)

| Commit | Subject |
|---|---|
| `97c7c485` | Merge dev 1f29f189 into 797-d0-audit, keeping both docs/README.md rows and regenerating the audit through its generator (#797) |
| `859ab22a` | Move the findings' source lines to the merged tree, drop D0-009 now #70 publishes the PHY link on every path past nvm_boot(), and restate D0-017 and D0-062 against dev 1f29f189 (#797) |
| `6c00c5ab` | Record the GET_STREAM_INFO ownership contradiction and the supplied trace producer as D0-063 to D0-066, and narrow D0-035 and D0-027 to their source lines, with the lines in each correction (#797) |
| `4c8b4654` | Search every recorded contradiction, normalised, across every inventoried page, so each page carrying it gets its own finding row and renders stale, with the README and requirements-page copy planted as a self-test arm (#797) |
| `624c7c43` | Arm the cross-page search against a longer word, two spellings on one page and a statement holding a recorded one, each killing its mutant (#797) |
| `c2b687d6` | Search a page for the statement's text before its word-boundary pattern, drop the redundant blank-line marker, and grade the two-spellings arm on the second copy's real line (#797) |
| `808602e0` | Plant the requirements-page copy as a wrapped block quote, so a search that keeps each line's marker fails the arm (#797) |

## Disposition

| Item | Result |
|---|---|
| Merge of dev | One conflict, `docs/README.md`: kept dev's new REBOOT row and this lane's "implemented" media-clock row. The audit was regenerated inside the merge commit. |
| R742-2 F1 (MAJOR) | D0-063 (`INTEGRATION_GUIDE.md:60`), D0-064 (`:64`). The page renders stale. D0-063's correction gives each word and flag its writer. |
| R742-2 F2 | D0-035: two rejection predicates; the length bounds the copy only. |
| R742-2 F3 | D0-027: the round-trip tests the supplied producer, and the shipping image does not link it. |
| R741-2 F1 | The gate rule below. `REQUIREMENTS.md:27` gets its row from the search, not from a hand-recorded entry. |
| Sampling (item 4) | Every correction added or changed cites its lines in the correction cell. `receipts/citations-round3.txt` prints each cited line at this head. |

Added beyond the assignment's letter, each because the same evidence required it:

- **D0-065, `INTEGRATION_GUIDE.md:65`:** "the processor's four fields" is the same miscount as `:60`.
- **D0-066, `VERIFICATION_DEVELOPER.md:25`:** "Shipping trace producer" is the sentence behind R742-2 F3, and it was unrecorded.
- **D0-009 removed:** #70 (PR #816) now polls the PHY on every path past `nvm_boot()`, including a refused record set (`milan_baremetal.c:1099-1102`, `:1671`, `:1676`). The finding's claim is no longer true at the merged tree.
- **D0-017 restated:** its correction leaned on D0-009. It now says a CSR identity mismatch returns before the poll is armed (`:1900-1903`).
- **D0-062 restated:** the route it pointed at has moved to the #787 re-pin record (+0.365 ns, 63 slices free, processor `a9e84b66`).
- **D0-038 restated:** #814 renamed the call to `add_staged_sdram`.
- **28 citations moved:** the merge moved their lines with the text unchanged (`receipts/moved-citations.txt`, tool `tools/moved_citations.py`). The three "TEXT DIFFERS" lines there are D0-026, D0-038 and D0-062, reread by hand.

The GET_STREAM_INFO logic is the same at `f65c8ff7` (R742-2's lines 3573-3585) and at the merged pin `a9e84b66` (lines 3628-3643). Only the line numbers moved.

## Changes (file:line, reason)

| File:line | Change | Reason |
|---|---|---|
| `scripts/docs_inventory.py:32` | docstring: the cross-page rule and its limit | R741-2 F1 |
| `scripts/docs_inventory.py:137-138` | what a copy may differ by | "normalised" |
| `scripts/docs_inventory.py:160-162` | `Finding.also`, `Finding.origin` | recorded other spellings; a copy row names the recording page |
| `scripts/docs_inventory.py:354` | `load_data` validates `also` (rc 2) and reads `cited_at` | a malformed entry refuses |
| `scripts/docs_inventory.py:373` | `normal_form()`: NFKC, line markers, emphasis and code spans, whitespace, case | the search's normal form |
| `scripts/docs_inventory.py:379` | `flatten()`: the page on one line with line offsets, so a wrapped copy matches and a blank line breaks it | `REQUIREMENTS.md` wraps its statements |
| `scripts/docs_inventory.py:389` | `carried_line()`: whole words only, returns the first line | no match inside a longer word |
| `scripts/docs_inventory.py:400` | `copies()`: one row per finding and other page | the gate rule |
| `scripts/docs_inventory.py:488` | `build()` adds the copies before the status rule | each carrying page renders stale |
| `scripts/docs_inventory.py:566` | a copy row says where the statement is recorded | a cold reader can tell copies from records |
| `scripts/docs_inventory.py:841-908` | `plant_copy()`, `in_order()`, `copy_controls()`: 12 arms; 42 controls in all | the README and requirements-page arm |
| `scripts/docs_inventory.py:278` | `relative()` is now `posixpath.relpath`, and the docstring is rewrapped | keeps the module at the 1,000-line limit of `check_py_idiom.py`; the rendered page is unchanged by it |
| `scripts/docs_inventory.json` | `cited_at`; D0-001 `also` and correction; D0-017, 027, 035, 038, 057, 062 restated; D0-009 removed; D0-063 to D0-066 added; 28 moved citations | above |
| `docs/DOCUMENTATION_AUDIT.md` | regenerated by `python3 scripts/docs_inventory.py --write` only | generated page |
| `docs/README.md` | merge resolution, both sides kept | merge |
| `.github/ci-templates/docs.yml:423-435` | step comment names the cross-page rule | the comment states what the gate catches; `.github/workflows/docs.yml` regenerates unchanged |
| `ci/image/command-table.json:13701` | script sha256 `8340fe0b51cc2f81df7a086da4d9e2821cc028dc7cfbd4b15edaa8f439591833` | the command table pins the script's bytes; no new subprocess form |

Audit at this head: 212 documents, 166 current, 25 stale, 21 obsolete. 65 recorded findings and 22 copy rows make 87 rows.

## Generator, gate rule and freshness gate

- Gate: `python3 scripts/docs_inventory.py --check` (rc 1 stale or rule broken, 2 refused). Self-test: `--selftest`, 42 controls, each through `main(["--check"], fixture)` on a Git-initialised fixture.
- **Rule:** each recorded statement and each `also` spelling is searched, normalised, across every inventoried page. Each other page carrying it gets a row, then the status rule applies. A copy row leaves when its page is fixed.
- **Decision, archive pages:** a copy on an archive page gets a row and keeps `obsolete` (9 rows on 8 pages, 2 of them on `PROTOCOL_TRACEABILITY.md`). The status rule already leaves obsolete pages as they are, and a frozen archive is not rewritten. The page says so.
- **Planted stale page in the real tree** (`receipts/mutants/probe-cross-page.txt`, p01): one added line on `docs/guides/README.md` gives `--check` rc 1.
- **Other real-tree probes in that receipt:** p02, the README statement wrapped onto `SYSTEM_INTEGRATOR.md`: rc 1, then `--write`, rc 0, one row, stale. p03, the `REQUIREMENTS.md` row deleted by hand: rc 1. p04, marked current by hand: rc 1 with the status-rule message. p06, the requirements sentence reworded: rc 1, then `--write`, rc 0, row gone, page current. p07: the paraphrase limit.
- **Named mutant, cross-page search disabled:** `--selftest` KILLED and `--check` CAUGHT (`receipts/mutants/mutants-final-head.txt`). Probe p05: a generator with the search disabled regenerates a page that passes its own `--check`, and `--selftest`, the workflow's next command, exits 1.
- **All generator mutants** (`tools/mutate_inventory.py`): 36 counted, 36 killed, with two earlier mutants equivalent and not counted. The hook-environment probe passes.
- **Reviewers' scripts rerun at this head:** R741-2 `probe_gate2.sh`, 11 of 11 expected (`receipts/mutants/r741-probe-gate2-final-head.txt`). R741-2 `mutate_selftest2.py`, 12 killed, with the same three survivors its report names (`receipts/mutants/r741-mutants2-final-head.txt`). R742-2 `probe_inventory.py`, rc 0 (`receipts/mutants/r742-probe-inventory2-final-head.txt`).
- **Command table:** `tools/walk_inventory_step.py` accepts this head (`receipts/walk-inventory-step-final-head.txt`). The full check's refusal is identical at this head and at dev (`receipts/ci-tool-inventory-check.txt`, `receipts/ci-tool-inventory-check-at-dev.txt`).

## Findings per area

Generated by `python3 scripts/docs_inventory.py --findings-dir findings`; notes in `findings/README.md`.

| Area | Rows | Copy rows | File |
|---|---:|---:|---|
| reference (with integration) | 57 | 3 | `findings/reference.md` |
| overview and guides | 14 | 3 | `findings/overview-and-guides.md` |
| design | 6 | 6 | `findings/design.md` |
| testing and CI | 1 | 1 | `findings/testing-and-ci.md` |
| archive (recorded, not to be rewritten) | 9 | 9 | `findings/archive.md` |
| **total** | **87** | **22** | |

## Gate table (head `808602e0`, all rc 0, never piped)

The same 96-command list as rounds 1 and 2, run by `tools/run_gates.sh` with the pinned Markdown renderer, wavedrom and pyslang in a scratch venv. Dev did not change `.github/` between `1e80128f` and `1f29f189`. The list covers docs_check, doc style, em-dash, doc paths, TOC and anchors, the bare-metal scope gate and the no-git forms. Logs over 200 KB are replaced by a `.sha256.txt` record. Not run: the RV32 SDK install, the compiler-absent firmware controls and the end-station builder legs. No Vivado.

| # | rc | time | command | log |
|---:|---:|---:|---|---|
| a001 | 0 | 0s | `git rev-parse HEAD && git status --short \| wc -l` | receipts/head-808602e0/a/001.log |
| a002 | 0 | 0s | `python3 scripts/gen_hdl_reference.py --selftest` | receipts/head-808602e0/a/002.log |
| a003 | 0 | 2s | `d=$(mktemp -d) && python3 scripts/gen_hdl_reference.py --output "$d/ref"; rc=$?; rm -rf "$d"; exit $rc` | receipts/head-808602e0/a/003.log |
| a004 | 0 | 8s | `python3 scripts/docs_check.py` | receipts/head-808602e0/a/004.log |
| a005 | 0 | 2s | `python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"` | receipts/head-808602e0/a/005.log |
| a006 | 0 | 3s | `python3 scripts/check_em_dash.py --selftest` | receipts/head-808602e0/a/006.log |
| a007 | 0 | 0s | `python3 scripts/check_doc_style.py` | receipts/head-808602e0/a/007.log |
| a008 | 0 | 0s | `python3 scripts/check_doc_style.py --selftest` | receipts/head-808602e0/a/008.log |
| a009 | 0 | 0s | `python3 scripts/check_gptp_docs.py` | receipts/head-808602e0/a/009.log |
| a010 | 0 | 1s | `python3 scripts/check_gptp_docs.py --selftest` | receipts/head-808602e0/a/010.log |
| a011 | 0 | 0s | `python3 docs/DOC_MAP.gen.py --check` | receipts/head-808602e0/a/011.log |
| a012 | 0 | 1s | `python3 docs/DOC_MAP.gen.py --selftest` | receipts/head-808602e0/a/012.log |
| a013 | 0 | 0s | `python3 docs/diagrams/timesync_chain.gen.py --check` | receipts/head-808602e0/a/013.log |
| a014 | 0 | 0s | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | receipts/head-808602e0/a/014.log |
| a015 | 0 | 0s | `python3 scripts/check_solution_docs.py` | receipts/head-808602e0/a/015.log |
| a016 | 0 | 4s | `python3 scripts/check_solution_docs.py --selftest` | receipts/head-808602e0/a/016.log |
| a017 | 0 | 0s | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | receipts/head-808602e0/a/017.log |
| a018 | 0 | 1s | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | receipts/head-808602e0/a/018.log |
| a019 | 0 | 0s | `python3 scripts/check_submodule_docs.py` | receipts/head-808602e0/a/019.log |
| a020 | 0 | 0s | `python3 scripts/check_submodule_docs.py --selftest` | receipts/head-808602e0/a/020.log |
| a021 | 0 | 0s | `python3 scripts/gen_wavedrom.py --selftest` | receipts/head-808602e0/a/021.log |
| a022 | 0 | 1s | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | receipts/head-808602e0/a/022.log |
| a023 | 0 | 0s | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | receipts/head-808602e0/a/023.log |
| a024 | 0 | 0s | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | receipts/head-808602e0/a/024.log |
| a025 | 0 | 1s | `python3 scripts/check_diagram_pngs.py` | receipts/head-808602e0/a/025.log |
| a026 | 0 | 7s | `python3 scripts/check_diagram_pngs.py --selftest` | receipts/head-808602e0/a/026.log |
| a027 | 0 | 1s | `python3 scripts/check_feature_status.py --self-test` | receipts/head-808602e0/a/027.log |
| a028 | 0 | 1s | `python3 docs/traceability/gen_module_matrix.py --check` | receipts/head-808602e0/a/028.log |
| a029 | 0 | 1s | `python3 scripts/check_gptp_docs.py --with-submodule` | receipts/head-808602e0/a/029.log |
| a030 | 0 | 0s | `make -C gptp-processor docs` | receipts/head-808602e0/a/030.log |
| a031 | 0 | 0s | `python3 scripts/measure_control_flow.py --selftest` | receipts/head-808602e0/a/031.log |
| a032 | 0 | 0s | `python3 scripts/measure_cohesion.py --selftest` | receipts/head-808602e0/a/032.log |
| a033 | 0 | 27s | `python3 scripts/check_baremetal_only.py --check` | receipts/head-808602e0/a/033.log |
| a034 | 0 | 6s | `python3 scripts/check_baremetal_only.py --selftest` | receipts/head-808602e0/a/034.log |
| a035 | 0 | 2s | `python3 scripts/check_nvm_record_space.py` | receipts/head-808602e0/a/035.log |
| a036 | 0 | 40s | `python3 scripts/check_nvm_record_space.py --self-test` | receipts/head-808602e0/a/036.log |
| a037 | 0 | 1s | `python3 scripts/check_nvm_capture.py` | receipts/head-808602e0/a/037.log |
| a038 | 0 | 0s | `python3 scripts/check_soc_sources.py` | receipts/head-808602e0/a/038.log |
| a039 | 0 | 1s | `python3 scripts/check_soc_sources.py --selftest` | receipts/head-808602e0/a/039.log |
| a040 | 0 | 1s | `python3 sw/litex/iob_pack_selftest.py` | receipts/head-808602e0/a/040.log |
| a041 | 0 | 2s | `python3 scripts/check_rtl_source_lists.py` | receipts/head-808602e0/a/041.log |
| a042 | 0 | 3s | `python3 scripts/check_rtl_source_lists.py --selftest` | receipts/head-808602e0/a/042.log |
| a043 | 0 | 1s | `python3 scripts/measure_naming.py --check` | receipts/head-808602e0/a/043.log |
| a044 | 0 | 0s | `python3 scripts/measure_naming.py --selftest` | receipts/head-808602e0/a/044.log |
| a045 | 0 | 3s | `python3 scripts/check_port_contracts.py` | receipts/head-808602e0/a/045.log |
| a046 | 0 | 3s | `python3 scripts/check_port_contracts.py --selftest` | receipts/head-808602e0/a/046.log |
| a047 | 0 | 2s | `python3 scripts/measure_fail_fast.py --check` | receipts/head-808602e0/a/047.log |
| a048 | 0 | 2s | `python3 scripts/measure_fail_fast.py --selftest` | receipts/head-808602e0/a/048.log |
| a049 | 0 | 2s | `python3 scripts/check_todo_ownership.py` | receipts/head-808602e0/a/049.log |
| a050 | 0 | 2s | `python3 scripts/check_todo_ownership.py --selftest` | receipts/head-808602e0/a/050.log |
| a051 | 0 | 9s | `python3 scripts/measure_test_evidence.py --check` | receipts/head-808602e0/a/051.log |
| a052 | 0 | 8s | `python3 scripts/measure_test_evidence.py --selftest` | receipts/head-808602e0/a/052.log |
| a053 | 0 | 1s | `python3 scripts/check_hygiene.py --check` | receipts/head-808602e0/a/053.log |
| a054 | 0 | 0s | `python3 scripts/check_hygiene.py --selftest` | receipts/head-808602e0/a/054.log |
| a055 | 0 | 1s | `python3 scripts/check_sv_idiom.py` | receipts/head-808602e0/a/055.log |
| a056 | 0 | 0s | `python3 scripts/check_sv_idiom.py --selftest` | receipts/head-808602e0/a/056.log |
| a057 | 0 | 2s | `python3 scripts/check_cpp_idiom.py` | receipts/head-808602e0/a/057.log |
| a058 | 0 | 2s | `python3 scripts/check_cpp_idiom.py --selftest` | receipts/head-808602e0/a/058.log |
| a059 | 0 | 5s | `python3 scripts/check_py_idiom.py` | receipts/head-808602e0/a/059.log |
| a060 | 0 | 5s | `python3 scripts/check_py_idiom.py --selftest` | receipts/head-808602e0/a/060.log |
| b001 | 0 | 0s | `python3 scripts/check_sh_idiom.py` | receipts/head-808602e0/b/001.log |
| b002 | 0 | 0s | `python3 scripts/check_sh_idiom.py --selftest` | receipts/head-808602e0/b/002.log |
| b003 | 0 | 0s | `python3 scripts/check_doc_paths.py` | receipts/head-808602e0/b/003.log |
| b004 | 0 | 1s | `python3 scripts/check_archive.py` | receipts/head-808602e0/b/004.log |
| b005 | 0 | 0s | `python3 scripts/check_archive.py --selftest` | receipts/head-808602e0/b/005.log |
| b006 | 0 | 0s | `python3 scripts/gen_toc.py --selftest` | receipts/head-808602e0/b/006.log |
| b007 | 0 | 5s | `python3 scripts/gen_toc.py --verify-anchors` | receipts/head-808602e0/b/007.log |
| b008 | 0 | 6s | `python3 scripts/gen_toc.py --check` | receipts/head-808602e0/b/008.log |
| b009 | 0 | 2s | `python3 scripts/docs_inventory.py --check` | receipts/head-808602e0/b/009.log |
| b010 | 0 | 1s | `python3 scripts/docs_inventory.py --selftest` | receipts/head-808602e0/b/010.log |
| b011 | 0 | 0s | `python3 avdecc/gen_aem_store.py --self-test` | receipts/head-808602e0/b/011.log |
| b012 | 0 | 13s | `python3 scripts/check_sweep_shape.py --self-test` | receipts/head-808602e0/b/012.log |
| b013 | 0 | 0s | `python3 scripts/check_deploy_shape.py --self-test` | receipts/head-808602e0/b/013.log |
| b014 | 0 | 65s | `python3 scripts/check_entity_shape.py --self-test` | receipts/head-808602e0/b/014.log |
| b015 | 0 | 0s | `python3 scripts/ci_gate_workflows.py --check` | receipts/head-808602e0/b/015.log |
| b016 | 0 | 12s | `python3 scripts/ci_gate_workflows_selftest.py` | receipts/head-808602e0/b/016.log |
| b017 | 0 | 1s | `python3 scripts/ci_case_receipts_selftest.py` | receipts/head-808602e0/b/017.log |
| b018 | 0 | 0s | `python3 scripts/ci_make_cases_selftest.py` | receipts/head-808602e0/b/018.log |
| b019 | 0 | 0s | `python3 scripts/ci_maap_cases_selftest.py` | receipts/head-808602e0/b/019.log |
| b020 | 0 | 0s | `python3 scripts/ci_capture_cases_selftest.py` | receipts/head-808602e0/b/020.log |
| b021 | 0 | 8s | `python3 scripts/ci_suite_pieces_selftest.py` | receipts/head-808602e0/b/021.log |
| b022 | 0 | 2s | `python3 scripts/ci_suite_collect_selftest.py` | receipts/head-808602e0/b/022.log |
| b023 | 0 | 1s | `python3 scripts/ci_fail_fast_selftest.py` | receipts/head-808602e0/b/023.log |
| b024 | 0 | 5s | `python3 scripts/ci_runtime_evidence_selftest.py` | receipts/head-808602e0/b/024.log |
| b025 | 0 | 0s | `python3 scripts/ci_install_cache_selftest.py` | receipts/head-808602e0/b/025.log |
| b026 | 0 | 1s | `python3 scripts/generate_ci_evidence_pins.py --check` | receipts/head-808602e0/b/026.log |
| b027 | 0 | 0s | `python3 scripts/ci_workflow_plan_selftest.py` | receipts/head-808602e0/b/027.log |
| b028 | 0 | 0s | `python3 scripts/ci_manifest_selftest.py` | receipts/head-808602e0/b/028.log |
| b029 | 0 | 0s | `python3 scripts/ci_events.py --check` | receipts/head-808602e0/b/029.log |
| b030 | 0 | 178s | `python3 scripts/ci_events.py --selftest` | receipts/head-808602e0/b/030.log.sha256.txt |
| b031 | 0 | 0s | `python3 scripts/check_wire_accountability.py --self-test` | receipts/head-808602e0/b/031.log |
| b032 | 0 | 66s | `python3 scripts/act_ci.py --selftest` | receipts/head-808602e0/b/032.log |
| b033 | 0 | 31s | `d=$(mktemp -d) && install -m 0555 scripts/act_ci.py "$d/act_ci.py" && python3 -I "$d/act_ci.py" --selftest --worktree "$PWD"; rc=$?; rm -rf "$d"; exit $rc` | receipts/head-808602e0/b/033.log |
| b034 | 0 | 8s | `d=$(mktemp -d) && git archive HEAD \| tar -x -C "$d" && (cd "$d" && python3 scripts/docs_check.py && python3 scripts/check_feature_status.py); rc=$?; rm -rf "$d"; exit $rc` | receipts/head-808602e0/b/034.log |
| b035 | 0 | 3s | `d=$(mktemp -d) && git archive HEAD \| tar -x -C "$d" && (cd "$d" && python3 scripts/docs_inventory.py --check); rc=$?; rm -rf "$d"; exit $rc` | receipts/head-808602e0/b/035.log |
| b036 | 0 | 3s | `d=$(mktemp -d) && git clone -q --no-recurse-submodules "$PWD" "$d/c" && (cd "$d/c" && git checkout -q "$(git -C "$OLDPWD" rev-parse HEAD)" 2>/dev/null; python3 scripts/docs_inventory.py --check); rc=$?; rm -rf "$d"; exit $rc` | receipts/head-808602e0/b/036.log |

## Resources

Single Python processes, the gate lists and mutant shards. MemAvailable read 55 GB at the start and 52 GB at the end; it was not sampled in between. No Vivado, no sweep, no hardware.
