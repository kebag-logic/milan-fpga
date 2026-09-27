[A346] REVIEW READY
Commit: 7c63e453142deb4d848c41594b2246afe32a792a
Branch: `565-8x8-clock` (local; not pushed)

Changed: `docs/integration/BAREMETAL_FIRMWARE.md:33,42` now distinguishes enforced profile checks from the declared 50 MHz target, cites both implementation files, and links #582. `hdl/ieee1722/aaf/README-parameters.md:37` explains the divider rationale without naming a board clock. Both assigned items are implemented in one text-only commit.

Validation: all commands returned rc 0:

- `python3 scripts/docs_check.py`
- `GIT_DIR=/dev/null python3 scripts/docs_check.py`
- `python3 scripts/check_em_dash.py --base 831f94f4`
- `python3 scripts/check_doc_style.py`
- `python3 scripts/gen_toc.py --check`
- `python3 scripts/gen_toc.py --verify-anchors`
- `python3 scripts/check_doc_paths.py`
- `python3 scripts/check_nvm_capture.py`
- `git diff --check`, also checked over the round 2 and full source deltas.

Acceptance criteria: both round 2 assignment items met. Only the two Markdown files changed; the capture receipt is byte-identical and passes its gate. The filesystem inventory mode skips its Git-parity self-test; that skip supplies no evidence.

Handoff: `HANDOFF.md` and the full replacement `PR-BODY.md` are prepared. The PR body has a Round 2 section; no PR edit was made.
Open risks/questions: no new implementation question. Independent re-review remains pending; enforcement and the assigned follow-ups remain with #582.
