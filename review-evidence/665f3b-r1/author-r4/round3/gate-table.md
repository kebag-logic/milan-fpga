| Gate | Command | Result | Planted control / proof |
|---|---|---|---|
| ci-events-check | `python3 scripts/ci_events.py --check` | rc 0 | ci-events-controls: 3064 arms over 2169 contract items |
| ci-events-controls | `python3 scripts/ci_events.py --selftest` | rc 0 | 3064 workflow/policy mutations and negative controls |
| doc-path-controls | `python3 "$EVIDENCE/round3/doc_path_controls.py" --repo .` | rc 0 | Three disposable tracked fixtures; expected statuses 0, 1, 1 |
| doc-paths | `python3 scripts/check_doc_paths.py` | rc 0 | doc-path-controls: valid passes, missing path and past-end anchor fail |
| doc-style-controls | `python3 scripts/check_doc_style.py --selftest` | rc 0 | Positive and refusal style fixtures |
| doc-style | `python3 scripts/check_doc_style.py` | rc 0 | doc-style-controls: documented positive/negative fixtures |
| docs-controls | `python3 scripts/docs_check.py --selftest` | rc 0 | 23 scrub and 4 routing arms |
| docs | `python3 scripts/docs_check.py` | rc 0 | docs-controls: 23 scrub and 4 routing arms |
| em-dash-controls | `python3 scripts/check_em_dash.py --selftest` | rc 0 | 339/339 planted controls |
| em-dash | `python3 scripts/check_em_dash.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c` | rc 0 | 339/339 embedded controls; separate em-dash-controls also passes |
| evidence-controls | `python3 scripts/measure_test_evidence.py --selftest` | rc 0 | 105/105 controls; inactive mutations and unexplained readers refused |
| evidence-readers | `python3 scripts/measure_test_evidence.py --check` | rc 0 | evidence-controls: 105/105 controls |
| gate-read-inventory | `python3 "$EVIDENCE/round3/gate_read_inventory.py" --repo .` | rc 0 | Exact eight-page set; no missing/stale entry; classifier reader/removal controls above |
| hygiene-controls | `python3 scripts/check_hygiene.py --selftest` | rc 0 | 35/35 controls |
| hygiene | `python3 scripts/check_hygiene.py --check` | rc 0 | hygiene-controls: 35/35 controls |
| integrity | `python3 "$EVIDENCE/round3/integrity.py" --repo .` | rc 0 | Direct raw-blob/mode and parent/changed-path identity check; no synthetic control claimed |
| python-controls | `python3 scripts/check_py_idiom.py --selftest` | rc 0 | 54/54 scanner, population and ratchet checks |
| python-idiom | `python3 scripts/check_py_idiom.py` | rc 0 | python-controls: 54/54 checks |
| scope-after | `python3 scripts/ci_scope.py --selftest` | rc 0 | 109 checks; removal of each gate-read page is caught; independent scan still names each removed page; 16 reader spellings |
| scope-classification | `python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md` | rc 0 | New page case and table-removal mutation in scope-after |
| service-bounds-portable | `python3 "$EVIDENCE/round3/service_bounds.py" --repo . --out "$WORK/portable-bounds"` | rc 0 | Same 38 controls through the published portable runner |
| service-bounds | `python3 "$WORK/bounds.py"` | rc 0 | 38/38 stale-value/deletion controls; 47 total checks |
| source-controls | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 | 50/50 controls |
| source-lists | `python3 scripts/check_rtl_source_lists.py` | rc 0 | source-controls: 50/50 controls; source removals from each consumer |
| toc-controls | `python3 scripts/gen_toc.py --selftest` | rc 0 | 1501/1501 rendering controls |
| toc | `python3 scripts/gen_toc.py --check` | rc 0 | toc-controls: 1501/1501 controls |
