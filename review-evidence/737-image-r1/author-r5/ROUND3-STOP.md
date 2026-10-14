[A615] STOP - PR #738 round 3
Head: `18f2df92b13cb3f4036b073ed76940187bf10487` (unchanged, clean branch; origin agrees).

The round-three ruling (6167899804, item 1.2) requires refusing a followed script importing `socket`, with an exception only for reviewed installer scripts. The unchanged workflow directly runs `python3 scripts/act_ci.py --selftest` at `.github/workflows/docs.yml:391`; `scripts/act_ci.py:60` imports `socket`. The script is already bound in the inventory inputs. Its port allocator at line 4852 uses sockets, and its self-test calls it at line 7209. This validation runner is not a tool installer.

Applying the import rule literally therefore refuses the existing required workflow. Exempting it would expand the published exception; changing or removing its test is outside this lane. AGENTS.md section 2 requires a public decision for this conflict.

Decision requested: may the closed table declare reviewed non-installing validation scripts with network imports, and what binding is required for that exception?

A read-only AST/source probe confirms the import, workflow call and exact inventory hash. HANDOFF.md and PR-BODY.md now contain Round 3 STOP sections; round3-policy-conflict.json records the evidence. No source edit, commit, push, workflow/test change or cold rebuild occurred. The two previous builds remain round-two evidence, not a new round-three manifest. All round-three fixes and rebuilds remain pending this decision.
