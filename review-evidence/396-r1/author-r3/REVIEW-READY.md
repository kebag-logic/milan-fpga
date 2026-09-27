[A361] REVIEW READY

Refs #396. Round 3 desk acceptance items 1, 2 and 5 are ready for independent
re-review. Bench items 3 and 4 remain open.

Commit: `8153576af6d739427b54f6c40299b0e57bc481ae`
Tree: `1d174c6a4b647e00456846623993a658e894b716`
Branch: `396-release-gates`
This is a local commit; it has not been pushed, as assigned.

Changed: `REQUIREMENTS.md`, `docs/testing/TESTING.md`, the release planner,
its plan feature and steps, and a new round-3 mutation driver.

- One named provisional 30-second ceiling now governs eligibility; tighter
  bounds remain eligible and 31-second or larger bounds are refused.
- The requirement, evidence table, assertion and plan agree on `tu`: a recorded
  discontinuity starts the interval, which clears within 0.5 seconds plus
  recorded observation resolution. Uncorrelated uncertainty fails.
- The corrected ADP window starts at power-strip ON (T0). Captured valid_time
  must be 10 and is decoded in two-second units. Off time and pre-cut ad age
  are separate provenance. `power_off_hold_s` defaults to eight seconds and is
  tested at non-default API and CLI values.
- Negative controls independently omit CRF keys, listener shape and every
  required topology key. Text/test suggestions are included: shared-profile
  rationale, canonical entity key, restoration requirements, restart type
  edges, Milan 5.6.2 citation and continuous boot evidence until the next cut
  or campaign end.

Validation at this exact head, from `$LANES/396-release-gates`,
all foreground and rc 0:

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 49 tests passed |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 76 scenarios / 321 steps; none skipped |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 221 scenarios / 866 steps; 172 scenarios excluded by tags |
| `python3 -B tb/tools/torture_release_mutants.py` | Nine named behavioral kills; clean baseline passed |
| `python3 -B scripts/check_feature_status.py --self-test` | 46/46 controls; zero findings |
| `python3 -B scripts/check_feature_status.py` | Zero findings |
| `python3 -B scripts/docs_check.py` | Zero findings |
| `python3 -B scripts/check_doc_paths.py` | 850 cited paths resolve |
| `python3 -B scripts/check_doc_style.py` | Passed |
| `python3 -B scripts/check_py_idiom.py` | Passed |
| `python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | Zero findings; 339/339 arms |
| `python3 -B scripts/gen_toc.py --check` | Passed |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | No missing area coverage |
| `python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json` | Three diagnostic repeats |
| `git diff --check` | Clean |
| `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | Clean |

The Markdown parser gates used the pinned requirements in
`tools/markdown/requirements.txt` in a temporary environment.

All fifteen public script files from
[`396-review-evidence` at c8ba14ef](https://github.com/kebag-logic/milan-fpga/tree/c8ba14ef462854d6338d131a17128b1916066344/review-evidence/396-r1/reviews)
were run unchanged, including both rounds' duplicate copies, probes,
attribution scripts and the gate runner. Every command returned 0; public
blob comparisons and final SHA-256 checks confirm the scripts were unchanged.

| Public suite | Result |
|---|---|
| Internal round 1 | 42 killed, one informational survivor, one invalid anchor |
| Internal round 2 | 48 killed, zero survivors, two invalid anchors |
| External round 1 | 21/21 killed |
| External round 2 | 22/22 killed |
| Omission probes | Each: 240 omissions, zero accepted |
| Audit probes | Real audit rejects all six defects |

Required internal E10-E13/E15 and external R11/R12 all die; internal
R16/B04/B09 die too. A08 remains the prior informational control. C13 uses the
removed 480-second boot literal; internal R13/R19 use superseded ADP strings.
These invalid cases are not counted as kills. New controls reject reinstating
the old ADP formula and skipping missing ADP evidence. The external probe's
final arithmetic rows hardcode the obsolete formula; they do not evaluate the
new expression and are not evidence against the corrected T0 rule.

Acceptance: assigned desk items have implementation and reproducible evidence.
`HANDOFF.md` and the full replacement `PR-BODY.md`, including Round 3, are
complete in the assigned packet. The worktree is clean and all gitlinks are
unchanged. No firmware, RTL or builder change was made.

Open risks/questions: the restoration ceiling remains provisional pending
#397/#75 measurements and manager ratification. Shipping-image soak, cold cuts,
physical negative control and retained bench evidence remain open under items
3 and 4. This is desk evidence, not a review verdict or physical acceptance.
No PR edit, push or merge was performed; independent re-review and publication
remain pending.
