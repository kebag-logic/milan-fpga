[A356]

Refs #396

## Status

Desk acceptance items 1, 2 and 5 are ready for review.
Bench acceptance items 3 and 4 remain open.

## Description

Define REQ-VER-06: seven continuous days with bidirectional AAF/CRF streams,
plus 200 cold cuts split into 160 idle and 40 journal-commit cuts.
Add parameterized soak and power plans, a data-driven persisted-item list,
and independent per-repeat index, direction, and CRF coverage audits.
Document required evidence and the distinction between desk and physical results.

## How to reproduce

```sh
python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json
python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power
```

Use the candidate's actual topology overrides for bench planning.
Reduced diagnostic profiles cannot qualify a release.

## How to validate

```sh
python3 -B tb/tools/torture_campaign.py --self-test
python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
git diff --check
```

All required gates returned 0.
The planner passed 41 tests; the plan feature passed 36 scenarios and 172 steps.
Feature-status controls passed 46/46 with zero findings.
Additional documentation, coverage, and source-quality checks also passed.

## Definition of done

- [x] Recorded release decisions appear in the normative requirements.
- [x] Both areas observe every index, both directions, and CRF.
- [x] Missing-index, missing-direction, and missing-CRF controls fail their audits.
- [x] Required desk gates pass.
- [ ] Shipping-image soak and cold-cycle campaigns, with retained evidence.
- [ ] Physical known-defect negative control and findings.
- [ ] Independent reviews.

The bench executor still supplies power-strip and commit-window instrumentation.
These desk results do not discharge #70, #117, or physical release acceptance.
