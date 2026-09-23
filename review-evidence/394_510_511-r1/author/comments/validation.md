Validation at `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` (submodules initialised at their gitlinks), every command exit 0:

```text
python3 -B scripts/docs_check.py                      0 finding(s), 164 md + 848 scrubbed files
python3 -B scripts/check_em_dash.py --base 759da623   0 finding(s) over 199 added lines in 11 pages
python3 -B scripts/check_feature_status.py --self-test   46/46; 0 finding(s)
python3 -B scripts/check_baremetal_only.py --check    OK, 0 findings
python3 -B docs/traceability/gen_module_matrix.py --check   up to date (69 modules)
python3 -B scripts/check_gptp_docs.py --with-submodule   OK (8 pages, donor checkout verified)
python3 -B scripts/check_doc_style.py                 OK (22 documents)
python3 -B scripts/gen_toc.py --check / --verify-anchors   OK / 154 fragment links
python3 -B scripts/check_doc_paths.py                 OK
python3 -B scripts/check_submodule_docs.py            OK (4 exact gitlinks)
git diff --check 759da623 HEAD                        clean
python3 -B sw/builder/test_builder.py                  ALL GATES PASS EXCEPT 1 NOT RUN
```

The builder arm that did not run is gate 11: it needs a local build report
that is not present. docs_check, the feature-status self-test, the em-dash
gate, gen_toc, the style gate and the gPTP docs gate also return 0 at each of
the six commits. The lane changes Markdown only: no RTL, firmware, builder,
configuration or test file.
