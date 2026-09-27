[A377] Enforce recorded mr causes and tu timing in the release soak.

Closes #593

## Status

Ready for independent review at `95bea7cf82fcf7cf034c156ef7aa6800ee769e05`.

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

All gates returned zero at the stated head: 66 planner tests, 44 killed mutations, and 86 feature scenarios. Documentation, source-fact, Python idiom and hygiene gates also passed.

## DoD

Assigned desk criteria are implemented and locally validated. Independent review and physical release campaign evidence remain separate obligations.
