[A201] TAKEN

Branch: `437-container-paragraph-scopes`, clean starting head `e4906bfca65c61e7e109e3532ac1b2dd5b4c0096` (tree `f5d2e8c022d39684f458f7d2d0ee97b350533353`). Sole author per the [assignment](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5795309062). Manager A10; R237 and R238 review the next head.

Authoritative references: #437 with acceptance 1 as amended 2026-09-23 14:15 and the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5794734885); #516 and its owner-decision comment; [R237-3](https://github.com/kebag-logic/milan-fpga/pull/515#issuecomment-5794524773) and [R238-2](https://github.com/kebag-logic/milan-fpga/pull/515#issuecomment-5794587304) with every earlier round on PR #515; the [container-walk decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791031813); CONTRIBUTING 5 and 6.1; CODE_QUALITY rule 12; CommonMark 0.31.2 sections 4.6, 4.7, 5.1, 5.2 and 6.6.

Interpreted scope:
- First merge live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70`. A dry-run merge is conflict-free; the only shared path is CONTRIBUTING.md (dev edits section 2, this lane 6.1).
- Remove the rendered-comment emulation: `gen_toc_html.py`, the rendered-comment flag in `blocks()`, the prose-comment end rule and the `<!-->` closure change. Comments are then read as at the base: open until `-->`, and not ended with their container. The container walk stays: the type-7 gate, and a fence or raw HTML block ends with its container.
- State the unclosed-raw-HTML-comment family in the walk docstring and CONTRIBUTING 6.1 as a directed limitation owned by #516, with its direction and boundary. Its fixture shapes keep their recorded renderings, marked as the limitation.
- Fix R237-3 F2 (an item holding only a link reference definition), R237-3 F4 (an arm for the quote's end at a blank line), R238-2 F2 (an arm for the type 3-5 end marker; the HTML-stage properties leave with the stage) and the escape inventory of R237-3 F3 / R238-2 F3 outside the removed emulation. Each finding is recorded as resolved or moved to #516.
- Acceptance 2 to 5 unchanged; no ratchet widened.

Validation plan: `gen_toc.py --selftest`, `--check`, `--verify-anchors`; `check_em_dash.py --selftest` and `--base <merge-base>`; `docs_check.py` and its selftest; `check_doc_style.py`; `check_py_idiom.py`; `git diff --check`. GitHub `gfm` renders of new shapes and of base/head differences over the fixtures and the reviewers' published shapes. A named mutation per new property. At most 8 jobs.

Blockers: none.
