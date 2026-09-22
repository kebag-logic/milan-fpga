[A156] Committed author handoff for #478

Implementation head: `099e191137dd2797407fb8345a452bcc7a965608`
Actual parent/base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`
Branch: `478-audio-unit-rate-bound`
Checkout: `$CANDIDATE`
State: clean, one local commit ahead of the issue-linked remote branch. No push, PR creation, review launch, rebase or merge performed. No other source checkout changed.

## Changed files

| File | Change |
|---|---|
| `sw/builder/endstation_builder.py` | `MAX_AUDIO_UNIT_RATES = 8` next to `BASE_RATE_HZ`, citing donor section 3.1 L10; separate excessive-length and duplicate `ConfigError` checks after existing integer conversion. |
| `sw/builder/test_builder.py` | Gate 36a: legal eight-entry loader boundary, distinct ninth-entry refusal, duplicate and normalized-duplicate refusals, existing defaults/membership/order, five shipping image rate lists, and the pp_shadow declaration drift gate with five independent controls. Registered in the normal full runner. |
| `docs/ENDSTATION_BUILDER.md` | Authoritative schema mapping row 8 documents the bound, uniqueness, defaults/order/current membership and gate 36a. |

Commit: `fix(builder): enforce AUDIO_UNIT rate-list contract` (one line, no trailers).

## Acceptance mapping

| Requirement | Evidence |
|---|---|
| More than eight entries refused, naming cause and L10 | `test_audio_unit_rates_loader_contract`: nine distinct values through `load_config`; diagnostic requires the key, eight-entry walk and L10. Original loader failed this gate by accepting the ninth entry. |
| Duplicates refused by cause | Same gate tests `[48000, 96000, 48000]` and `[48000, "48000"]`; requires duplicate-specific `ConfigError`. |
| One named maximum with provenance | `endstation_builder.py:1200`; comparisons and bound diagnostic use `MAX_AUDIO_UNIT_RATES`. |
| Eight entries accepted; defaults and order retained | Eight distinct unsorted values with 48000 last pass `_load_clocking` unchanged; omitted-list defaults tested at all three existing base rates. Empty and missing-current lists retain their existing refusal. This boundary tests the specified loader contract, without widening stream-format or runtime-rate support. |
| Five shipped configs remain valid and rates unchanged | Full builder gate 1 builds all five. Gate 36a decodes their AUDIO_UNIT words from packed images. Before/after SHA-256 checks match both all config bytes and all complete packed AEM images. |
| Hand-built pp_shadow list cannot drift silently | The normal builder runner compares literal `AU_RATES_C` values and declared array length against `endstation_arty_current.yaml`. Independent changed-value, reordered-value, declared-length, shortened-initializer and commented-declaration controls are each refused. The C++ image remains hand-built and unchanged. |
| Changed input contract documented | Schema mapping row 8; focused gate 32 and documentation checks pass. |

## Author validation

All commands below ran from the author checkout through `rtk proxy` (Git through `rtk git`). Source content was unchanged between these checks and the final commit; the em-dash gate ran on the committed head. See [VALIDATION-COMMANDS.md](VALIDATION-COMMANDS.md) for the complete focused invocation.

| Command / scope | Result | Log |
|---|---|---|
| Focused Python invocation of gates 36a, 32, 25a/b/c | PASS; seven test functions | `focused.log` |
| `python3 -u sw/builder/test_builder.py` | Exit 0: `ALL GATES PASS EXCEPT 1 NOT RUN`. Gate 11's physical resource-calibration report is absent; no other arm skipped. Available LiteX elaborations ran. | `builder-full.log` |
| `python3 scripts/lint_rtl.py --check` | PASS: 90 findings <= ratchet 90, 17 waived, zero justified lint-off pragmas | `lint.log` |
| `python3 scripts/xvlog_gate.py --check` | PASS: zero parent findings; four existing pinned-processor findings match the ratchet. Analyzed 72 parent files and 48 processor files. | `xvlog.log` |
| `python3 scripts/docs_check.py` | PASS: zero findings; scrub 23/23, routing 4/4 | `docs_check.log` |
| `python3 scripts/check_doc_paths.py` | PASS: 824 cited paths resolve | `check_doc_paths.log` |
| `python3 scripts/check_doc_style.py` | PASS | `check_doc_style.log` |
| `python3 scripts/gen_toc.py --check` | PASS | `gen_toc--check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | PASS: 145 cross-page links reproduced | `gen_toc--verify-anchors.log` |
| `python3 scripts/check_feature_status.py` | PASS: zero findings | `check_feature_status.log` |
| `python3 scripts/check_py_idiom.py` | PASS: no new violations; all ratchets satisfied | `check_py_idiom.log` |
| `python3 scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8` | PASS: zero findings, 34/34 controls | `em-dash.log` |
| `git diff --check` | PASS | No output |
| `python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-author/check-loader-mutations.py` | PASS: raising maximum to nine, lowering it to seven, and removing duplicate rejection each fail gate 36a independently; no source mutation | `loader-mutations.log` |
| `python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/478-author/check-rate-images.py` | PASS: five complete images and config files match the pre-edit baseline | `rate-image-comparison.log` |

Environment: Python 3.14.7, Verilator 5.052. Public submodule pins were initialized by the manager and left unchanged: protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused SSH-only `external` submodule remains uninitialized.

## Five-config evidence

All AUDIO_UNIT rate offsets remain 144. Counts remain three for arty_current and one for each other config. Full image hashes below are identical before and after the change; `baseline-rates.json` and `after-rates.json` also include the config-file hashes.

| Config suffix | Advertised rate words | Packed AEM image SHA-256 |
|---|---|---|
| `arty_current` | `[48000, 96000, 192000]` | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `arty_4x4` | `[48000]` | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `arty_8ch` | `[48000]` | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `ax7101_8x8` | `[48000]` | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `ax7101_1x1_tdm8` | `[48000]` | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |

## Remaining manager work

- Integrate the latest live `dev` if it moved, including any #407 merge, then validate the resulting tree. This author kept the assigned base throughout.
- Publish the branch and draft PR, using [PR-BODY.md](PR-BODY.md). Publish [REVIEW-READY.md](REVIEW-READY.md) as evidence, not a review verdict.
- Run the complete native bar, including the parent sweep, required donor/behavior suites and Yosys; trusted act-first replication from a separate clean live-dev checkout; and all required hosted contexts on the publication head. None of those broader results is claimed by this author.
- Resolve the availability of the existing gate 11 calibration report if that evidence is required for the manager's validation. Its skip is explicit, not a pass.
- Obtain independent R221/R222 reviews and the reviewer-owned five-lens ledger on the integrated head. Then complete candidate validation, authorized merge and post-merge containment.

No pp_shadow source, Makefile, image or local suite artifact changed, so the conditional pp_shadow suite rerun was not invoked. No complete parent `run_all_suites`, expensive full `milan_dp`, hardware operation, or candidate host-side `act_ci.py` was invoked. No unresolved implementation decision remains; remaining items are the manager's publication/review/validation bar.

## Public record

- [Readiness decision](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770832729)
- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770949009)
- [A156 TAKEN](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770966362)
- [A156 implementation details and focused evidence](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5771001703)
- [A156 REVIEW READY author evidence](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5771061894)
