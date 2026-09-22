[A168] FACTUAL VALIDATION RECEIPT

Head `65df1df50a80cd5f540a93d8f0cfabc97da3da75`, tree `da06c8609b7a574e3df121fbcb8a1fc8f207dcb7`; base `88e9276b2a220c716f64a843f7e1eb8f9265e896`. Every command below executed on this clean committed head. These are author measurements, not a review verdict or a candidate-merge validation. [Selected decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775771538); [exact synthetic renderer inputs/results](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775985191).

25 focused commands, every exit 0:

```sh
rtk proxy python3 -B scripts/gen_toc.py --selftest
rtk proxy python3 -B scripts/gen_toc.py --check
rtk proxy python3 -B scripts/gen_toc.py --verify-anchors
rtk proxy python3 -B scripts/gen_toc.py --sites
rtk proxy python3 -B scripts/check_em_dash.py --selftest
rtk proxy python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
rtk proxy python3 -B scripts/docs_check.py
rtk proxy python3 -B scripts/docs_check.py --selftest
rtk proxy python3 -B scripts/check_doc_style.py
rtk proxy python3 -B scripts/check_doc_style.py --selftest
rtk proxy python3 -B scripts/check_doc_paths.py
rtk proxy python3 -B scripts/check_py_idiom.py
rtk proxy python3 -B scripts/check_py_idiom.py --selftest
rtk proxy python3 -B scripts/check_hygiene.py --check
rtk proxy python3 -B scripts/check_hygiene.py --selftest
rtk proxy python3 -B scripts/measure_test_evidence.py --check
rtk proxy python3 -B scripts/measure_test_evidence.py --selftest
rtk proxy python3 -B scripts/measure_fail_fast.py --check
rtk proxy python3 -B scripts/measure_fail_fast.py --selftest
rtk proxy python3 -B scripts/check_todo_ownership.py
rtk proxy python3 -B scripts/check_todo_ownership.py --selftest
rtk proxy python3 -B scripts/measure_cohesion.py --selftest
rtk proxy python3 -B scripts/measure_control_flow.py --selftest
rtk proxy python3 -B scripts/ci_events.py --check
rtk proxy python3 -B scripts/ci_events.py --selftest
```

Key results: TOC selftest 754/754; Contents check 105 pages with navigation plus 17 below threshold; 144 existing fragment links reproduced; em-dash selftest 99 arms; base gate zero findings across nine added lines in one Markdown page, zero exemptions. docs_check zero findings over 163 Markdown files and 828 scrubbed text files. Python idiom long-function 9<=9 and long-module 10<=10, all other ratchets in budget; no budget file changed. CI contract 1505 items, selftest 1144 arms. All 27 decision sites read the shared character classes.

Preservation: all 707 prior arm inputs have identical blocks/headings/generated-navigation/refusal answers under base and head parsers. The #507 closer table module is byte-identical; its controls still execute. Only the old family-enumeration and site-count guards expand (eight to nine families, 25 to 27 sites). check_em_dash changes only its selftest integration; all gate decision functions are AST-identical. Exactly five changed files: CONTRIBUTING.md, scripts/gen_toc.py, scripts/gen_toc_cases.py, scripts/gen_toc_container_cases.py, scripts/check_em_dash.py. Every other tracked object, including the gitlinks, remains at the base. Initialized public submodule identities match the starting receipt.

AC4: no classification differences across all 163 tracked pages on EITHER original-base inputs or current-head inputs. Compared fields: blocks, line_kinds, headings with anchors, generated_block, refusals. No family-two heading was added.

Mutation sensitivity: 17 bounded source mutants in disposable parser/gate copies; each is caught by BOTH shipped selftests, with a named I437 failure. The original source bytes were never mutated. Table values are exit codes (1 for TOC test failure, 2 for em-dash selftest refusal), not passing gate verdicts:

| Mutation | gen_toc selftest | check_em_dash selftest |
|---|---:|---:|
| drop-context | 1 | 2 |
| forget-on-blank | 1 | 2 |
| blanket-indent | 1 | 2 |
| strict-column | 1 | 2 |
| fixed-column | 1 | 2 |
| characters-not-columns | 1 | 2 |
| no-code-padding | 1 | 2 |
| four-is-code-padding | 1 | 2 |
| empty-never-ends | 1 | 2 |
| empty-stays-empty | 1 | 2 |
| empty-uses-padding | 1 | 2 |
| lose-outer-column | 1 | 2 |
| stale-sibling-column | 1 | 2 |
| stale-context | 1 | 2 |
| no-lazy-hold | 1 | 2 |
| markers-in-blocks | 1 | 2 |
| no-ordinal-interruption-check | 1 | 2 |

Additional refusal controls: 25 independently spelled non-CR refused characters, each placed on the base and head side of a list-context page: 50 cases each produce two named findings and zero exemptions. The base cases explicitly report `mirrors no heading`; all name the offending code point/column. An invalid base revision also refuses. CR normalization remains covered by the unchanged #507 controls.

Outstanding manager bars: independent cold R237/R238 reviews, reviewer-owned lens coverage, full native/RTL/Yosys/processor bars, trusted-dev act replication, hosted checks, current candidate validation, merge authorization and post-merge containment. None was run or claimed here. No push, PR operation, Docker/act, hardware, install, other checkout edit or subagent occurred. There were no newly discovered product/parser defects outside the recorded limitations in these bounded tests; no neighboring fixes were taken.

Historical artifact limit: original R86-5 JSON/HTML paths are local-only in the public report; the 11 fresh F1 fixtures reconstruct its described family, not an attested archive row mapping. This distinction remains in the handoff and is not an acceptance-policy change.
