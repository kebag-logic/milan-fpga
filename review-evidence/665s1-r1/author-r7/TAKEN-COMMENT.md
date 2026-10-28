[A680h] TAKEN
Branch: 665-s1-faces (PR #795), at the round-6 head `424b1489`
Authoritative references: assignment issuecomment-6447669608 (merge round); rulings 6421238472 and 6425357821 still in force; reviews R701-6 and R702-6 (POSITIVE at `424b1489`)
Interpreted scope: merge `origin/dev-soft-core` (`6660a1a0`, S2 / PR #792) into `665-s1-faces` as one merge commit, no rebase. Resolve the conflict in `sw/firmware/ctrl/test/ctrl_configs.py` by keeping both sides: S2's harness classifications and S1's entries, each with its reason. No other change.
Validation plan: the hosted rtl-fast `firmware-boundary` steps run locally as the workflow runs them; the firmware self-test in four shards as separate units; `fw_coverage.py --check`; `test_builder.py --require-rv32`; the linked images at four points (caps per ruling 6425357821); S2's harness self-test; the docs gates; the bare-metal scope gate; `cd tests && behave`. All rc 0, then REVIEW READY with the merge head.
Blockers: none
