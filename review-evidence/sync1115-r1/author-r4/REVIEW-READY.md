[A787] REVIEW READY

Commit: `c10c549e`, parent `6ceed753` (local; nothing pushed; the manager pushes).

Round 4 fixes R854-001 from PR #934 issuecomment-6932841237. The harness records each timer callback's owning interface and application at expiry, from its argument and the participant-creation binding. The grader uses that owner for the opportunity, first MRPDU, LeaveAll, late/absent output and service row. Missing or unresolved ownership is reported and fails. No firmware, product RTL, configuration, pin or numeric bound changes.

Validation:
- Clean-head harness self-test: rc 0, 876 checks, all 258 mutants caught, including the original eight and four new owner mutants.
- The supplied overlap fails on the actual MSRP participant at its original 1,180 ms opportunity (191 ms). Clean reordered overlap passes. Both applications and both interfaces have skipped, late and absent controls; the supplemental full matrix passes all 24 cases.
- Eleven 8x8/1if phases rerun with owners recorded: 22 save-held/save-starved groups, 44 LeaveAlls sent, none skipped, late, absent, unresolved or unowned; every probe row within its bound. Worst rows: LeaveAll 1.64360 ms, periodic 2.96879 ms, join 1.86217 ms, against unchanged 20 ms. The 49 ms conformance bound is unchanged.
- The required 1x1/1if valid-destinations leg exits 0. All 26 rerun traces equal their earlier executions after removing only the added owner records; all thirteen rebuilt firmware ELFs match their earlier images byte for byte. Seed clones use the exact head's harness; their MAC changes remain harness-only experiments.
- Clean-head docs jobs: 63 executed steps rc 0, 34 NOT RUN with explicit reasons, zero bad steps.

Open limits: every 8x8 phase leg retains rc 1 on two known #914 STATED polls-base costs; the extra 8x8 valid-destinations leg retains rc 1 on nineteen build/slice costs. They are not whole-leg passes. #898 still owns the 305 us paced SET_CONFIGURATION and CTRL_LOOP_TX_MS 35; neither changes here. #919's PHY gap and the earlier #929/#916 exclusions remain. Earlier image, route and full-gate evidence retains its recorded source heads; #818's timing floor is +0.030 ns setup / 0 ns hold, best of three.

R854-001 has an author fix pending independent re-review. R853-1 has published no findings at this handoff. The manager owns the push, evidence publication, composed-head acceptance and review completion; this is not merge approval.

The sanitized round-4 packet contains HANDOFF-r4.md, PR-BODY.md, this REVIEW-READY text, the receipts and a generated INDEX.md.
