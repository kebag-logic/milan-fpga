[A623] REVIEW READY
Commit: 2e83841675e4e1439c413c9ca11b4a123898a60e (branch `748-elab-race`, five normal commits on `c48bfe38`; not pushed)
Changed (round 2 for PR #749; the workflow change itself is untouched):
- R637-1-F01: `scripts/ci_toolcache_isolation.py` `checks()` judges gate 23h and its negative control from the builder driver's own `--receipt`, not its exit code. It refuses by the check's name a check with NOT RUN rows (quoting the driver's reason), a check missing from the receipt, a missing receipt, and a non-zero exit. A step whose `run` is not text is now refused by name instead of crashing the control.
- R637-1-F02: every path argument is made absolute, and `--rev` is resolved to a commit, before any state is derived. A bad `--rev` is refused up front. The help, docstring and `docs/testing/CI_WORKFLOWS.md` say relative or absolute is accepted.
- R637-1-F03: `(#748; REQ-VER-04)` on the template comment, the control's docstring and both `scripts/ci_events.py` explanations. The generated workflows are byte-identical.
- R636-1-F2: `--gate-legs` runs both legs' "Elaboration gates" steps together before the final manifest. Every other step after the patch series is named with its reason. The report carries the planted and final manifest hashes.
Validation (native, CPython 3.12.3 planted, all through the CLI at the commit):
- Complete patched interpreter with `--work run` (relative) and with an absolute directory: ISOLATED, rc 0 both; both checks "ran and passed" in both legs; 0 of 6303 paths changed.
- `litex-boards` uninstalled after the patches, and the same without the patches: NOT ISOLATED, rc 1; both checks reported NOT RUN in both legs, refused by name, even though gate 23h exits 0.
- Available but unpatched interpreter: NOT ISOLATED, rc 1 (gate 23h fails, no receipt).
- `--shared` and the `dev` 9ef71772 workflow: NOT ISOLATED, rc 1, 9296 paths changed, one placement rc 1 each.
- `--gate-legs`: ISOLATED, rc 0 in 995 s. Leg 0 `ALL GATES PASS` (940 s); leg 1 `ALL GATES PASS EXCEPT 1 NOT RUN`, gate 11's calibration arm (408 s). Afterwards 0 of 6303 paths changed; the planted and final manifest sha256 are both 871f9aea2b89f393b82fcd49ecb9aa6797cd669a75e5b3d601d74a5aba678d36.
- `ci_gate_workflows.py --check` rc 0 and its self-test PASS; `ci_events.py --check` OK (2199 items) and `--selftest` PASS (5233 arms; the three #748 arms caught); `docs` gate set 46 of 46 run steps rc 0, tree clean afterwards.
Acceptance criteria: round-2 items 1 to 4 met, with evidence in the handoff. The per-job CI cost is unchanged from round 1 (the venv step, 2.3 to 2.6 s per leg).
Open risks/questions: the four-job act replay at this head and the hosted gates belong to the coordinating role. The PR body's inventory edit is kept.
