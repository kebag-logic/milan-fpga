[A360] REVIEW READY

Commit: `55079500483970ee244f12fa4c94401783f3df6f` (local, unpushed)
Branch: `587-8x8-baseline-50mhz`
Measured input tree: `63fe4fb0164d798d44a6476001dc8b887cdd4609`

Changed: the baseline page now records the declared 50 MHz integrated 8x8 results beside labelled 100 MHz history. Added complete 50 MHz input/report hashes, boundary/load evidence and resource rankings. No RTL, configuration, tooling or submodule edits.

| Measurement | Historical 100 MHz | Declared 50 MHz | Delta |
|---|---:|---:|---:|
| Default whole LUTs | 68,136 | 68,047 | -89 |
| Default whole WNS ns | -11.331 | -1.708 | +9.623 |
| Attribution wrapper LUTs | 29,489 | 28,955 | -534 |
| Attribution wrapper internal WNS ns | -10.846 | -1.700 | +9.146 |

The separate attribution whole-design total is 69,923 LUTs. Both synthesis commands and all unchanged public boundary/load probes returned rc 0. Both clocks report 20.000 ns; clock-derived timer parameters bind 50 MHz. Source and image rehashing passed, with zero missing-ROM diagnostics. The attribution dynamic-state probe has zero external-only loads; the wrapper's 518-cell residual and load stems are recorded.

Validation at this head, all entrypoints rc 0, foreground and without pipelines, from `$LANES/587-8x8-baseline-50mhz`:

```text
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 -B scripts/docs_check.py
env GIT_DIR=/dev/null python3 -B scripts/docs_check.py
python3 scripts/check_em_dash.py --base 63fe4fb0
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
git diff --check
git diff --check 63fe4fb0 HEAD
```

The pristine control passes and all 28 maintained mutants are killed. Both documentation inventories contain 901 text files with zero findings; no-Git mode omits only Git inventory parity. The 339 em-dash controls, 179 anchors and 848 cited paths pass.

Acceptance items 1-3 are met. The [#229 reference comment](https://github.com/kebag-logic/milan-fpga/issues/229#issuecomment-5847400261) is updated and verified. HANDOFF.md contains file:line changes, the full clock comparison, hashes, versions and gate table; PR-BODY.md is prepared in the assigned packet. All packet files are under 200 KB; large reports/checkpoints remain outside it with SHA-256 and sizes recorded.

Open limits: 50 MHz still exceeds capacity by 4,647 LUTs and has negative synthesis WNS. Existing constraint warnings and 46/86 ports without input/output delays remain. No placement, routing or hardware claim. The 1x1 figures are unchanged. Worktree and initialized submodules are clean. No push, PR creation/edit, merge or other checkout was performed. Independent reviews by [R350] and [R351] and publication remain pending.
