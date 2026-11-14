# R841-1 commands (run from the review clone at 4958ca4f630da1f715bdcd78113b798bbe332b81)

`<clone>` is the detached review clone, `<packet>` this packet, `<venv>` the pinned LiteX venv.

| receipt | command | result |
|---|---|---|
| gates/shape-selftest | `python3 scripts/check_sweep_shape.py --self-test` | rc 0 |
| gates/board-variants | `python3 scripts/board_variants.py` | rc 0 |
| gates/board-variants-selftest | `python3 scripts/board_variants.py --selftest` | rc 0, 6 controls |
| gates/gate1e | `python3 sw/builder/test_builder.py --gates test_qspi_owner_transition_completed_write_prefixes` | rc 0 |
| gates/timing-grade | `python3 sw/builder/test_timing_grade.py <venv>/python3` | rc 0 |
| gates/build-dryrun | `bash sw/litex/build.sh ax7a200t --dry-run` | rc 0 |
| gates/diff-check | `git diff --check b7d69295 HEAD` | rc 0 |
| gates/docs-inventory | `python3 scripts/docs_inventory.py --check` | rc 0 |
| docs-gates/* | `check_doc_style`, `check_doc_paths`, `check_diagram_pngs`, `check_hygiene --check`, `check_py_idiom`, `check_sh_idiom`, `check_solution_docs`, `check_deploy_shape --self-test`, `docs_check` | rc 0 each |
| docs-gates/em_dash | `check_em_dash.py --base b7d69295` | rc 2: pinned renderer not installed here (not a finding); added lines carry 0 U+2014 (em_dash_added_lines.txt) |
| probes/flash_layout_regen | `python3 docs/diagrams/flash_layout.gen.py <scratch>/flash_layout` | all four svg/drawio byte-identical to the committed ones |
| probes/ax7101_base_vs_head | `scripts/elaborate.sh` (build.sh dry-run argv without `--build`) for ax7101 at b7d69295 and at the head, then `scripts/compare_elab.py` | 15 of 22 in-scope files byte-identical; .v, csr.*, headers differ only in generated-on lines; flashboot_layout.json gains flash_device/flash_jedec_id |
| probes/ax7101_verilog_body | normalised Verilog body hashes | ax7101 base == ax7101 head == ax7a200t head |
| probes/ax7101_vs_ax7a200t_head | soc.h, Tcl, init, xdc diff between the two recipes at the head | only the part (Tcl x3) and the AEM offset (soc.h, ROM init) differ; xdc identical |
| probes/layout_from_soch_vs_main | `layout_from_soch.py` over each head elaboration's soc.h | images and flash device equal main()'s layout for both dies |
| probes/probe_200t_update | `python3 -I scripts/probe_200t_update.py <clone> <scratch> <venv>/python3` | rc 0, 6 arms as expected |
| probes/probe_200t_update_under_K9 | the same probe with mutant K9 planted in a disposable copy | rc 1: the update arm fails |
| probes/mutants | `python3 -I scripts/mutants.py <disposable copy> <venv>/python3` | 5 killed, 4 survived (K3, K4, K7, K9) |
| probes/litex_sim_test_gptp_tx_timestamp | `scripts/run_litex_sims.sh <logs> --only test_gptp_tx_timestamp` (leg 0's only member) | PASS, 576 s |
| hosted-checks | `gh api .../commits/<head>/check-runs` (read only) | first read: 58 success, 1 skipped (nightly physical), 2 in progress; second read (17:21:30Z): 59 success, 1 skipped, 1 in progress, 6 queued. No failure at either read; the manager owns hosted acceptance |
| restore-check | git index/tree/gitlink verification after the probes | exact head restored |
