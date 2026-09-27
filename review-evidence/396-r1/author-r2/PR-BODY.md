[A359]

Refs #396

## Status

Desk acceptance items 1, 2 and 5 are ready for independent re-review at
`24d32d549fa7470318a93984403a92423a63fa25`. Bench acceptance items 3 and 4 remain open.

## Description

Define REQ-VER-06: seven continuous days with bidirectional AAF/CRF streams,
plus 200 cold cuts split into 160 idle and 40 journal-commit cuts.
Add parameterized soak and power plans, a declared persisted-item inventory,
and independent per-repeat index, direction and CRF coverage audits.
Document the required exact-image evidence and the distinction between desk
validation and physical release acceptance.

## Round 2

Implement the [recorded timing decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854930205):

- T0 is the host timestamp of the power-strip ON command. The first post-cut
  advertisement must beat the last captured pre-cut advertisement's expiry,
  derived from that PDU's own `valid_time` in two-second units.
- Each persisted binding must resume valid AVTP automatically within the
  provisional `restore_bound_s=30`, including both directions and CRF.
  The manager ratifies this bound from #397 and #75 measurements.
- After automatic restoration succeeds, an additional controller reconnect
  must reach first valid AVTP less than one second after CONNECT_RX success.
- Boot observation is `restore_bound_s + boot_margin_s`, with a default
  five-second margin. The margin cannot extend a passing deadline.
  The single-boot assertion rejects #366's repeated BIOS pass even if streaming
  eventually recovers; incomplete observations cannot pass.

Correct the release assertion and requirement citations against extracted
Milan v1.2, IEEE 1722-2016 and IEEE 1722.1-2021 source pages. Separate the
sequence and uncertainty fields, asCapable clause, binding persistence,
advertising, automatic restoration and controller reconnect authorities.

`release_eligible` requires a sampling interval no greater than 60 seconds,
the stream-binding inventory and explicit complete topology, in addition
to the area's duration or count/phase minimums. Default fixtures and partial
CLI overrides remain diagnostic. AAF indices overlapping CRF are refused.
The flag judges configured prerequisites; it does not prove physical coverage,
measured results, descriptor provenance, or ratification of the timing bound.

Expand negative controls across every repeat, both devices, both descriptor
kinds and independent AAF/CRF directions. Test non-default interval, total,
restoration bound and margin, phase-specific snapshot policy, commit-count
eligibility and the repeated-boot control.

## Reproduction and validation

```sh
python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json
python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power
python3 -B tb/tools/torture_campaign.py --self-test
python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_py_idiom.py
git diff --check
git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check
```

Use both candidate-specific topology specifications from served descriptors
for bench planning. Install the pinned Markdown requirements for the document
gates. All 12 required gates returned 0 at the head above.

| Validation | Result |
|---|---|
| Planner self-test | 47 tests passed |
| Plan feature | 68 scenarios / 297 steps passed; none skipped |
| Feature-status controls | 46/46 passed; zero findings |
| Documentation, source quality, area coverage and whitespace | Passed |
| Unchanged internal mutation script | 42/44 killed; all seven required mutants killed |
| Unchanged external mutation script | 21/21 killed |
| Unchanged omission probe | 240 omissions across three topologies; zero accepted |
| Unchanged audit probe | Real audit rejects all six planted defects |

The internal A08 survivor is the prior report's informational false-red-only
control. C13 is invalid because its old 480-second source anchor no longer
exists; it is not counted as killed. A separate current-contract mutation
hardcoding the derived boot observation to 60 seconds fails both test suites.
The four public scripts were verified byte-identical to the evidence branch.

## Definition of done

- [x] Recorded release decisions appear in the normative requirement and plan.
- [x] Both areas observe every index, both directions and CRF.
- [x] Each repeat detects missing counter targets and independent AAF/CRF directions.
- [x] Required desk gates and requested mutation controls pass.
- [ ] Shipping-image soak and cold-cycle campaigns, with retained evidence.
- [ ] Physical known-defect negative control and findings.
- [ ] Manager ratification of the provisional restoration bound.
- [ ] Independent re-review of this head.

The bench executor supplies the power-strip and journal-window instrumentation.
No physical release result is claimed. Desk validation does not discharge
#70, #117, or the open bench acceptance items.
