| gate | command | rc | seconds |
|---|---|---|---|
| markdown-renderer-lock | `python3 -c "import cmarkgfm, html5lib, importlib.metadata as m; print(m.version(\"cmarkgfm\"), m.version(\"html5lib\"))"` | 0 | 0.1 |
| docs-check | `python3 scripts/docs_check.py` | 0 | 7.1 |
| feature-status | `python3 scripts/check_feature_status.py` | 0 | 1.1 |
| feature-status-selftest | `python3 scripts/check_feature_status.py --self-test` | 0 | 1.1 |
| em-dash | `python3 scripts/check_em_dash.py --base d385b38e5282b395ca55d49d135e46a93f56a340` | 0 | 2.6 |
| em-dash-selftest | `python3 scripts/check_em_dash.py --selftest` | 0 | 2.6 |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.1 |
| doc-style-selftest | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.0 |
| toc-selftest | `python3 scripts/gen_toc.py --selftest` | 0 | 0.8 |
| toc-verify-anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.7 |
| toc-check | `python3 scripts/gen_toc.py --check` | 0 | 5.3 |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.1 |
| baremetal-check | `python3 scripts/check_baremetal_only.py --check` | 0 | 25.2 |
| baremetal-selftest | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 5.6 |
| doc-map-check | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.4 |
| doc-map-selftest | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.4 |
