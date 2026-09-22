[A156] Author validation commands

Run from the implementation checkout. Shell commands use the RTK proxy.

```sh
rtk proxy python3 -c 'import sys; sys.path.insert(0, "sw/builder"); import test_builder as t; t.test_audio_unit_rates_loader_contract(); t.test_audio_unit_shipping_rates(); t.test_pp_shadow_audio_unit_rates_match_config(); t.test_builder_doc_key_map(); t.test_schema_12_keys_reach_the_image(); t.test_schema_12_refusals(); t.test_schema_11_configs_accepted_unchanged()'
rtk proxy python3 -u sw/builder/test_builder.py
rtk proxy python3 scripts/lint_rtl.py --check
rtk proxy python3 scripts/xvlog_gate.py --check
rtk proxy python3 scripts/docs_check.py
rtk proxy python3 scripts/check_doc_paths.py
rtk proxy python3 scripts/check_doc_style.py
rtk proxy python3 scripts/gen_toc.py --check
rtk proxy python3 scripts/gen_toc.py --verify-anchors
rtk proxy python3 scripts/check_feature_status.py
rtk proxy python3 scripts/check_py_idiom.py
rtk proxy python3 scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8
rtk git diff --check
```

The focused functions were invoked in one Python heredoc loop; the first command above is the equivalent compact invocation. The remaining Python arguments are the exact validation commands; logs are retained beside HANDOFF.md. The em-dash gate runs after the implementation commit because it compares committed HEAD against the base.

Additional evidence uses these retained standalone scripts:

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-author/check-rate-images.py
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-author/check-loader-mutations.py
```

The rate-image baseline was captured before the first repository edit at b17580b91deb11f3441dfc5d7f9fafe539d929b8. The mutation script changes loaded functions/constants in its own process and restores them; it writes no source file.
