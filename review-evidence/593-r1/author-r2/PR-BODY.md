[A377] Enforce recorded mr causes and tu timing in the release soak.

Closes #593

## Status

Ready for independent review at `68e801b2823f75e037152f7eb2ac4c5dcda5d919`.

## Description

The soak gate correlates each mr toggle and MEDIA_RESET increment with a recorded media-clock-source change, CRF disruption, or received CRF mr toggle. It checks the eight-PDU hold per stream and rejects GM-only causes. The tu check retains the last-discontinuity upper bound and adds the resolution-aware 0.25-second GM minimum. Missing evidence produces NOT RUN.

REQ-VER-06 and TESTING section 6d describe the evidence and timing windows, citing IEEE 1722-2016 4.4.4.3/4.4.4.7 and Milan v1.2 Annex B.1.1/B.1.2 and Tables 5.4/5.6.

## How to reproduce and validate

With the pinned Markdown dependencies installed, run:

```sh
python3 -B tb/tools/torture_campaign.py --self-test
python3 -B tb/tools/torture_release_mutants.py
python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress
python3 scripts/ci_scope.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py --self-test
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04
git diff 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD --check
```

All gates returned zero at the stated head: 75 planner tests, 106 killed mutations, and 87 feature scenarios. Documentation, source-fact, Python idiom and hygiene gates also passed.

## DoD

Assigned desk criteria are implemented and locally validated. Independent review and physical release campaign evidence remain separate obligations.

## Round 2

The corrected head is `68e801b2823f75e037152f7eb2ac4c5dcda5d919`.

- Correlate the `tu` rise with its first discontinuity. Grade every GM change against the complete interval history, including absent holds and changes at clear.
- Refuse resolution at or above the derived limits: `min(0.25, 0.5)` seconds for `tu`, and half the one-second counter-update ceiling for the two-sided `mr` cause window.
- Consume each cause at most once per stream. Require a recorded capture span covering the counter window, and classify counter decreases as resets.
- Pin the new behavior and assertion text with mutation controls. Document the PHC-step conflict in [#602](https://github.com/kebag-logic/milan-fpga/issues/602). Pending that decision, a PHC step alone remains no cause; a soak containing one fails on the current image.

All 35 assigned gate commands returned zero at this head. The planner passes 75 tests; the mutation driver kills 106 controls, including the 25 from PR #586. The plan feature passes 87 scenarios, and the torture tier passes 232. Builder scope, bare-metal boundary, documentation and whitespace gates pass.

The unchanged review mutation drivers kill 32/32 and 38/38 applicable controls, with no survivors. Four and six old anchors respectively were superseded; eight re-anchored or replacement controls are killed separately. The external probe meets all 21 cases with recorded capture spans supplied. The internal probe's only remaining mismatches are its two unassigned suggestions: counter under-counting and omitted GM provenance. Neither changes this round's acceptance criteria.

Independent re-review remains pending. This is desk evidence; physical release qualification remains separate.
