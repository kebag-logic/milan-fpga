[A344] REVIEW READY

Commit: `054e59b41471ffbb3b4999a60c4cb04abcfc895f`
Branch: `565-8x8-clock` (local, unpushed, as assigned).

Changed: the 8x8 Milan/CPU declaration is 50 MHz with the build-contract/#565 basis and no closure claim. System, sample and audio clocks are unchanged. Refreshed the six-arm capture receipt and section 18, reconciled clock descriptions, and recorded per-arm configuration/ROM hashes. Capture gate and harness executable logic are unchanged.

Acceptance criteria:

- All clock consumers were derived and checked. Generated PLL divider changes 16 to 32; datapath timer divisor 100 to 50; system-cycle bridge watchdogs 3072 to 6144. Generated constraints are byte-identical and retain derived-clock handling. CPU clock selection and CDC remain enabled. The handoff and prepared PR body contain the complete before/after consumer table.
- Every generated artifact for each of the other four configurations is byte-identical: 11 files each, including the sweep fragment. The 8x8 configuration-specific gPTP image changes with `--clk-hz`; the three default ROM-ledger digests do not change, so no re-recording was needed.
- All 96 fresh captures pass. At 50 MHz, the 8x8 maxima are ON 24.30246 ms and OFF 24.26154 ms. Overall 24.30246 ms is below 24.5 ms, with 2.0163x margin against the 49 ms floor. The unchanged nominal hold remains 50 ms. The 1x1 overall maximum is 6.60642 ms; the labelled 100 MHz 8x8 overall maximum is 19.79024 ms. The STOP condition did not trigger.
- The 100 MHz comparison retains the selected configuration's 50 MHz gPTP image, as the existing harness specifies. It establishes capture timing only; no gPTP or physical timing claim is made.
- Read-only #231 report: baseline `ae729bbfd90934f4d56d3b02f1ffc652496b414d` uses the 8x8 100 MHz timer/integrated Milan clock. Its 68,136-LUT / -11.331 ns synthesis result and clock-derived ROM/parameters describe that recipe, and cannot be relabelled or rescaled to 50 MHz. Its standalone 10 ns constraint is separately fixed. No baseline file was edited.

Validation: every required command group returned rc 0:

- Complete builder bank in compiler-present and compiler-absent modes, through the supplied selector adapter; 851 target compiler calls in present mode.
- `python3 -B scripts/docs_check.py`, both normal and `GIT_DIR=/dev/null` modes.
- `python3 -B scripts/check_em_dash.py --base 831f94f4`, checked after the commit: 18 added lines in four Markdown pages, 339/339 self-test arms.
- `python3 -B scripts/check_doc_style.py`; `python3 -B scripts/gen_toc.py --check`; `python3 -B scripts/gen_toc.py --verify-anchors`; `python3 -B scripts/check_doc_paths.py`.
- `python3 -B scripts/check_nvm_capture.py`; `python3 -B scripts/lint_rtl.py --check`; `syn/yosys/ooc.sh timestamp_counter`; `git diff --check`.
- `scripts/run_all_suites.sh <log-dir> --shard 1/5`, `3/5`, and `4/5`, with generous foreground timeouts. These cover the default shape-reading CSR, datapath, NVM backend and NVM co-simulation suites. Chunk totals are 21 suites / 173891 checks, 12 / 14432, and 1 / 11206, all without failures or timeouts.

Declared omissions: the existing historical calibration report is absent in both builder modes; compiler instruments intentionally do not run in absent mode. Chunk 1 declares four optional external field-campaign/freshness skips. The no-Git docs mode skips Git inventory parity. These omitted arms contribute no evidence. The initial missing Markdown dependency was resolved by selecting the existing pinned environment, with no installation.

Handoff: `HANDOFF.md`, `PR-BODY.md`, raw capture logs, graded rows, command results and size/SHA-256 manifests are in the assigned output directory. All files are below 200 KB; large build evidence remains outside it. No hardware, submodule edits, push, PR creation/edit or merge was performed.

Open risks/questions: physical timing closure remains unmeasured; no new scope decision is open. Independent reviews remain pending.
