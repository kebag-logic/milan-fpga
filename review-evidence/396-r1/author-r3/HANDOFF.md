[A361] Issue #396 - Round 3 handoff

Status: round-3 desk work committed and ready for independent re-review.
All assigned gates and unchanged public script commands returned 0.
Bench acceptance items 3 and 4 remain open.

Initial head: `24d32d549fa7470318a93984403a92423a63fa25`
Final head: `8153576af6d739427b54f6c40299b0e57bc481ae`
Final tree: `1d174c6a4b647e00456846623993a658e894b716`
Commit subject: `Tighten release eligibility and correct post-cut timing`
The commit has no body or trailers.
Branch: `396-release-gates`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`
Physical working directory: `$LANES/396-release-gates`
Final porcelain is empty; all six changed files match HEAD byte-for-byte.
All four gitlinks are unchanged. See `final-integrity.json` for hashes.

Authority and public state

The issue body and every comment, all three assignments, both round-2 reports,
repository operating contract, contribution rules, documentation map,
requirements, quality policy, testing policy and relevant cited sources were
read. The round-3 decision supersedes the round-2 ADP expiry rule.
No unresolved design choice or assignment STOP condition remains in the desk work.

- [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855515133)
- [Round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854930205)
- [Initial desk assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5854692245)
- [Internal round-2 report](https://github.com/kebag-logic/milan-fpga/pull/586#issuecomment-5855513105)
- [External round-2 report](https://github.com/kebag-logic/milan-fpga/pull/586#issuecomment-5855194536)
- [Public takeover](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855545141)

Changes

| File:line | Change |
| --- | --- |
| REQUIREMENTS.md:262 | Recorded discontinuity, 0.5-second uncertainty bound plus observation resolution |
| REQUIREMENTS.md:285 | Separate cold hold; twenty-second ADP window from T0; restoration eligibility ceiling; continued boot evidence |
| docs/testing/TESTING.md:878 | Release prerequisites, shared profile rationale and canonical topology key |
| docs/testing/TESTING.md:915 | Numeric uncertainty result, required resolution, cold-hold provenance, corrected ADP formula and continuous boot capture |
| tb/tools/torture_campaign.py:3325 | Single restoration ceiling, cold-hold setting and validation |
| tb/tools/torture_campaign.py:3389 | Uncertainty and post-cut assertion contracts |
| tb/tools/torture_campaign.py:3504 | Restoration eligibility check |
| tb/tools/torture_campaign.py:3544 | Structured uncertainty parameters |
| tb/tools/torture_campaign.py:3571 | Separate cold hold, T0 ADP parameters and continued boot evidence |
| tb/tools/torture_campaign.py:4957 | Non-default timing, restoration requirements and snapshot checks |
| tb/tools/torture_campaign.py:5000 | 29/30/31/3600-second eligibility arms and invalid hold values |
| tb/tools/torture_campaign.py:5052 | Each required topology key on both roles, empty values and mixed shapes |
| tb/tools/torture_campaign.py:5092 | Event-correlated uncertainty contract |
| tb/tools/torture_campaign.py:5118 | Restart type edges and boot capture through next cut or campaign end |
| tb/tools/torture_campaign.py:5466 | Cold-hold CLI option and propagation |
| tb/tools/torture_release_mutants.py:19 | Nine defect injections with named behavioral failures and clean baseline |
| tests/features/torture_campaign_plan.feature:386 | Boundary and partial-topology scenarios |
| tests/steps/torture_release_steps.py:221 | Real CLI negative controls and timing checks |

Finding and suggestion disposition

These are executor fix claims, not reviewer verdicts or a completion ledger.

| Public finding or suggestion | Implemented result | Evidence |
| --- | --- | --- |
| Internal F1 / external F1 | Restoration bounds above 30 are ineligible; tighter bounds remain eligible | Boundary self-test, feature examples, both eligibility probes, new refusal-removal mutant |
| External F2 | `tu` clears within 0.5 seconds of its recorded discontinuity plus recorded resolution; no uncorrelated interval passes | Requirement, table, assertion, structured args, self-test, feature and two mutations |
| External F3 | T0 starts the full decoded ADP window; eight-second default cold hold is separate provenance | Non-default API 17 seconds and CLI 13 seconds, requirement and formula; ADP and hold mutations |
| Internal F2 / external F4 | Each topology key rule has a negative control; CRF-only and listener-only omissions reach real CLI eligibility | E10-E13/E15 and external R11/R12 all killed |
| Internal S1 / external S3 | Add Milan 5.6.2 alongside 5.6.3; require captured valid_time 10 | Standards receipt and timing tests |
| Internal S2 / external S1 | Explain why both areas retain the common paired-profile prerequisites | TESTING.md:875; existing behavior retained |
| Internal S3 | Document canonical `entity`; parser alias does not attest explicit topology | TESTING.md:888; alias refusal arm |
| Internal S4 | Pin `restore_requires`; reject boolean/negative restart observations as incomplete | R16/B04/B09 all killed |
| External S2 | Continuous UART/reset evidence continues through counter walk until next cut or campaign end | Requirement, table, plan, boot self-test and capture-shortening mutant |

Results

| Check | Result |
| --- | --- |
| Origin and initial head | Match |
| Public context | Issue, assignments, reports and public scripts read |
| Final planner checks | 49 tests passed |
| Final plan feature | 76 scenarios and 321 steps passed; none skipped |
| Full torture tier | 221 scenarios and 866 steps passed; 172 scenarios excluded by tags |
| New mutation controls | Nine killed; pristine baseline passed |
| Internal round-1 script, both public copies | Each: 42 killed, one informational survivor, one invalid anchor |
| Internal round-2 script | 48 killed, zero survived, two invalid anchors |
| External round-1 script, both public copies | Each: 21/21 killed |
| External round-2 script | 22/22 killed |
| Omission probe, both public copies | Each: 240 omissions across three topologies, zero accepted |
| Audit probe, both public copies | Real audit rejects D1-D6 |
| Attribution scripts | Identify failing checks for 21 external and seven required internal round-1 mutants |
| Eligibility probes | 31/600/3600-second bounds refused; tighter bounds accepted with other prerequisites |

The prior A08 survivor is the review's informational false-red-only control.
C13 is invalid because its old 480-second boot anchor is absent; current
derived-window mutations are killed. Internal round-2 R13/R19 are invalid
because the recorded decision replaced their ADP strings. Invalid mutations
are not counted as killed. The nine new controls include reinstating the old
pre-cut ADP formula and skipping missing ADP evidence; both fail the named
timing test.

The external round-2 probe's final arithmetic rows hardcode the obsolete
pre-cut subtraction formula instead of reading the emitted expression.
Those rows remain unchanged in the receipt and are not evidence about the
corrected T0 formula. The current expression and start event are pinned by
the planner self-test and the plan feature.

Public script provenance and reproduction

All fifteen public script files were extracted using `git show` from fetched
`396-review-evidence` revision `c8ba14ef462854d6338d131a17128b1916066344`.
Every file was compared byte-for-byte with its public blob before execution
and SHA-256 checked afterwards. `review-script-provenance.json` records paths
and hashes. Both rounds' duplicate copies were executed too.

The public gate runner ran unchanged against the physical worktree. Its exact
command was:

```sh
timeout 1800 bash /tmp/396-a361-review/R347-2/run_gates.sh $LANES/396-release-gates /tmp/396-a361-gates /tmp/396-a361-markdown/bin/python
```

The remaining public scripts ran sequentially under a foreground parent, with
1800-second per-script limits. `review-script-results.json` records all exact
commands and exit codes. Internal mutation scripts export committed HEAD;
external mutation scripts received `/tmp/396-a361-external-export`, a temporary
archive of this same head's `tb/tools`, `tests` and `scripts` trees. They
restored the exported planner's original SHA-256 after every script. None
mutated the candidate worktree. Exports and dependency installations stayed
under `/tmp`.

Gate table

All gates ran at the final head from `$LANES/396-release-gates`.
No gate command was piped. `$MDPY` below was
`/tmp/396-a361-markdown/bin/python`, installed from the repository's pinned
Markdown requirements with hash checking. Receipts are under `gates/` except
the new mutation receipt `round3-mutants.log`.

| Command | Exit code | Result |
| --- | --- | --- |
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 49 tests |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 76 scenarios / 321 steps |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 0 | 221 scenarios / 866 steps |
| `python3 -B scripts/check_feature_status.py --self-test` | 0 | 46/46 controls; zero findings |
| `python3 -B scripts/check_feature_status.py` | 0 | Zero findings |
| `python3 -B scripts/docs_check.py` | 0 | Zero findings; 23/23 scrub controls and 4/4 routing arms |
| `python3 -B scripts/check_doc_paths.py` | 0 | 850 cited paths resolve |
| `python3 -B scripts/check_doc_style.py` | 0 | 22 current documents |
| `python3 -B scripts/check_py_idiom.py` | 0 | No ratchet increase; zero overlong lines |
| `$MDPY -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | Zero findings; 339/339 arms |
| `$MDPY -B scripts/gen_toc.py --check` | 0 | 111 annotated pages |
| `git diff --check` | 0 | Clean |
| `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | 0 | Clean |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | 0 | Neither area has missing coverage |
| `python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json` | 0 | Three diagnostic repeats emitted |
| `python3 -B tb/tools/torture_release_mutants.py` | 0 | Nine named behavioral kills |

Initial checks found one overlong line, which was wrapped before commit, and
a missing pinned Markdown dependency, which was installed only in the temporary
environment. Their initial receipts are retained. The final runs above all pass.

Artifacts and limits

- `PR-BODY.md` is the full replacement body, begins with `[A361]`, says
  `Refs #396`, and includes Round 3. It has not been applied to the PR.
- `REVIEW-READY.md` is the exact final issue-comment body prepared for posting
  as the last public action. It names the final local head and reproducible
  evidence. Re-review remains the reviewers' responsibility.
- `standards-citation-check.md` records source clauses and concise facts;
  `standards-source-hashes.json` records the source document hashes. No source
  pages or standards text are included in this packet.
- No push, PR creation/edit, merge, hardware action, other checkout, firmware,
  RTL, builder or submodule edit was performed. Hosted CI and merge-candidate
  evidence remain future publication/merge work.
- Acceptance items 1, 2 and 5 have desk evidence. Items 3 and 4 require the
  shipping-image seven-day soak, 200 cold cuts, physical known-defect control,
  retained captures and resulting findings. The provisional restoration ceiling
  still needs the assigned manager ratification from #397/#75 measurements.

The authorized final action is to publish `REVIEW-READY.md` on issue #396 and
stop. No independent review approval, lens completion or physical acceptance
is claimed by this handoff.
