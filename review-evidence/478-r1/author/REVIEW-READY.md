[A156] REVIEW READY (author handoff; manager validation and publication pending)

Commit: `099e191137dd2797407fb8345a452bcc7a965608`
Actual base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`
Branch: `478-audio-unit-rate-bound` (clean, committed locally; not pushed).

Changed: `sw/builder/endstation_builder.py` adds the named L10 eight-rate maximum and cause-specific excess/duplicate refusals. `sw/builder/test_builder.py` adds gate 36a and the hand-built pp_shadow array/config drift check. `docs/ENDSTATION_BUILDER.md` documents the input contract.

Validation:

- Focused gates 36a, 32 and 25a/b/c pass. The original loader fails the distinct ninth-entry case. Independent in-memory mutations to maxima nine/seven and removal of duplicate rejection are caught.
- `python3 -u sw/builder/test_builder.py`: exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN`; only gate 11's physical calibration-report arm skipped because its report is absent.
- `python3 scripts/lint_rtl.py --check`: PASS, 90 <= ratchet 90.
- `python3 scripts/xvlog_gate.py --check`: PASS, zero parent findings and four existing donor findings at the ratchet.
- `python3 scripts/docs_check.py`, `python3 scripts/check_doc_paths.py`, `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/gen_toc.py --verify-anchors`, `python3 scripts/check_feature_status.py`, `python3 scripts/check_py_idiom.py`: PASS.
- `python3 scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8`: PASS, zero findings and 34/34 controls. `git diff --check`: PASS.

Acceptance: excess and duplicate lists fail for their specified causes; eight distinct unsorted entries pass `_load_clocking` unchanged; omitted-list defaults and current membership are preserved. All five configs build. Config-file and complete packed-image SHA-256 values are unchanged: arty_current advertises `[48000, 96000, 192000]`, and arty_4x4, arty_8ch, ax7101_8x8 and ax7101_1x1_tdm8 each advertise `[48000]`. The pp_shadow values/declared-length comparison passes and five independent drift controls fail. Its source and hand-built image are unchanged.

Open risks/questions: no unresolved implementation decision. Gate 11 calibration evidence is unavailable locally. Manager still owns latest-dev integration, full native/donor/behavior/Yosys gates, trusted act-first replication, hosted checks, R221/R222 reviews, candidate validation and publication. This is author evidence, not an approval or claim that the merge bar is complete. No complete parent sweep, full milan_dp, pp_shadow suite rerun, hardware operation, push, PR creation, candidate host-side act invocation or merge was performed.
