[A156]

## Status

Author implementation committed at `099e191137dd2797407fb8345a452bcc7a965608` on `478-audio-unit-rate-bound`, based on `dev` `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. Manager integration, publication gates and independent reviews remain pending.

## Linked Issue / roles

Closes #478

Executor: A156. Internal cleared-context reviewer: R221. External reviewer: R222. Manager: A10.

## Description

The builder accepted AUDIO_UNIT rate lists longer than the processor can walk and lists containing duplicates. It now refuses both with cause-specific `ConfigError`; the eight-entry maximum is named beside `BASE_RATE_HZ` and cites donor L10.

Gate 36a covers a legal eight-entry loader boundary, a distinct ninth-entry refusal, duplicates, defaults/order and unchanged shipping rates. It also compares pp_shadow's deliberately hand-built `AU_RATES_C` values and declared length against the shipping YAML, with independent drift controls. The schema mapping documents the input contract.

## Authoritative references

- #478 [readiness decision](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770832729) and [assignment](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770949009).
- `protocol-processor/docs/architecture/07_memory_maps.md` section 3.1 L10, at donor pin `424c688fa2205b934a7689a58f2aa766420f2326`.
- Milan v1.2 Section 5.3.3.3; `REQUIREMENTS.md` REQ-VER-03/04.

## How to get into the same state

After manager publication, in an isolated checkout:

```sh
git fetch origin 478-audio-unit-rate-bound
git checkout 099e191137dd2797407fb8345a452bcc7a965608
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
python3 -c 'import sys; sys.path.insert(0, "sw/builder"); import test_builder as t; t.test_audio_unit_rates_loader_contract(); t.test_audio_unit_shipping_rates(); t.test_pp_shadow_audio_unit_rates_match_config()'
python3 sw/builder/test_builder.py
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/check_py_idiom.py
python3 scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8
```

Expected: rate boundary/refusal and drift controls pass; five shipped configs still build. The author full builder run exited 0 with one explicit gate 11 calibration-report skip. Detailed self-test evidence belongs in the companion PR comment; complete manager gates remain pending.

## Known limitations / out of scope

The eight-entry positive case tests `_load_clocking`; it does not broaden stream-format or runtime-rate support. All five packed shipping images and YAML files remain byte-identical. No donor, firmware, shipping config or pp_shadow source changed. The existing physical resource-calibration report was unavailable for gate 11.

## Definition of Done

- [x] Linked Issue implementation acceptance criteria are satisfied
- [x] New behavior has self-checking tests
- [x] Authoritative input documentation is updated
- [ ] Complete required local and hosted verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] All five lenses have clean reviewer-owned coverage at the integrated head
- [ ] Blocking findings are fixed and re-reviewed; no review remains in flight
- [ ] Candidate merge result is validated
- [ ] Authorized merge and post-merge containment are complete
