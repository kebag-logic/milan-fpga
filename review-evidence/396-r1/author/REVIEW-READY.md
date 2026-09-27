[A356] REVIEW READY

Commit: `b7b74b8b20c166cf69f84c2fcbb6162b420cd2d3`
Branch: `396-release-gates`, locally committed from `ac18b50968b12efe4d15c0a06301264b35656b31`.

Changed: REQ-VER-06 and contributor/testing contracts; parameterized soak and cold-power plans; persisted items as data; per-repeat index/direction/CRF audits and negative controls.

Validation, all rc 0 on this head:

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 41 tests passed |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 36 scenarios, 172 steps passed; no skips |
| `python3 -B scripts/check_feature_status.py --self-test` | 46/46 controls; zero findings |
| `python3 -B scripts/docs_check.py` | Zero findings |
| `python3 -B scripts/check_doc_paths.py` | 850 cited paths resolve |
| `python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | Zero findings; 339/339 controls |
| `python3 -B scripts/gen_toc.py --check` | Pass |
| `python3 -B scripts/check_doc_style.py` | Pass |
| `python3 -B scripts/check_py_idiom.py` | Pass; no ratchet changes |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | Both areas complete |
| `git diff --check` and `git diff ac18b50968b12efe4d15c0a06301264b35656b31 HEAD --check` | Pass |

Commands ran in the physical candidate worktree, in the foreground, without pipelines. Markdown checks used the existing interpreter with the pinned renderer.

Acceptance criteria: desk items 1, 2 and 5 met. Physical campaigns and the known-defect negative control under items 3 and 4 remain open. No hardware result is claimed.

Open risks/questions: no desk blocker. The bench executor must supply repeat-operation execution, continuous transition evidence, power-strip control and journal-window instrumentation. The default persisted inventory is stream binding; it expands to all eight items when #70 lands. AVTPRX_TSD observations remain explicitly limited to STREAM_INPUT[0].

The working tree is clean. HANDOFF.md and PR-BODY.md are prepared for the internal and external reviewers. No push, PR operation, or merge was performed.
