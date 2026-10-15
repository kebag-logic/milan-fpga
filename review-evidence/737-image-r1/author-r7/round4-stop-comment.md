[A615] STOP - PR #738, round 4
Head: e6b86814e6844ef61ba46a867a0fdbfbb925cceb (local and origin/737-ci-image agree).

Assignment 6170435035 requires refusing interpreter program text, shell functions and reached Makefiles with `$(shell)`, while preserving the current inventory and leaving workflows unchanged. Those requirements conflict on the existing head:

- `.github/workflows/elaborate.yml:230` and `:321` execute `python3 -c 'import pythondata_cpu_vexiiriscv as p; print(p.data_location)'` in command substitutions.
- `scripts/run_all_suites.sh:124` and `scripts/run_litex_sims.sh:112` define functions; workflows call these scripts at `rtl.yml:220` and `elaborate.yml:315`.
- `tb/verilator/milan_dp/Makefile:149`, already bound in the inventory, uses `$(shell python3 ...)`.

A read-only probe with CPython 3.12.3 and the checksum-authenticated parser confirms these literal forms. Probe rc 0; source worktree clean. They cannot be assigned to runtime-assembled-command residue under item 7.

Please record a public decision: authorize migration of existing unsupported forms in the appropriate lane, or amend the refusal rule with explicit reviewed support for existing forms. AGENTS.md sections 2 and 4 require publishing this conflict rather than privately changing the acceptance contract.

HANDOFF.md and PR-BODY.md now contain Round 4 STOP sections and the source evidence. No source edit, commit, push or rebuild; recipe/lock unchanged. Both round-three NEGATIVE reviews remain unresolved. Round-three image evidence remains historical. Stopping as instructed.
