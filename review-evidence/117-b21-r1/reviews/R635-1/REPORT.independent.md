[R635] NEGATIVE - exact head 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b

Independent pass complete for R635-1. All five lenses applied before reading any other review findings. The final report expands these results and records the subsequent public-history check.

| Finding | Severity | All attributable lenses | Artifact | Result |
|---|---|---|---|---|
| R635-1-F1 | MAJOR | Conformance, Tests, Docs | docs/findings/117_AUDIO_CONTINUITY.md:865; tools/b21_restart.py in the pinned evidence | Restart acceptance excludes unmeasured steady output latency and starts at the response, so the reported relative times do not prove rebind-to-first-valid-sample under one second. |
| R635-1-F2 | MAJOR | Conformance, Robustness, Tests, Docs | docs/findings/117_AUDIO_CONTINUITY.md:1021; published tools/b21_grade.py:215 and :234 | Hash equality is treated as exact four-slot equality; a reproducible changed frame is reported fully matched. Independent exact replay nevertheless finds the actual recording equal. |
| R635-1-F3 | MINOR | Robustness, Tests | published tools/b21_grade.py:255 | Three inserted zero frames as the first discontinuity crash summary generation with KeyError instead of yielding the measured foreign/offset counts. |
| R635-1-F4 | MINOR | Tests, Docs | docs/findings/117_AUDIO_CONTINUITY.md:937 | Nine groups are described as positive; replay gives eight positive groups and one negative group. |

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #117 body and assignments; REQUIREMENTS.md:306; findings page:843; retained direction/restart media | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| RTL | CLEAN | source.diff; docs/design/TIME_SYNC.md:507; docs/reference/REGISTER_MAP.md:1878 and :2028; CSR polls; source-integrity.json | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| Robustness | UNCLEAN | probes.py and probe-results.json; McASP timing; restart silences, statuses and format reads | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| Tests | UNCLEAN | public tools/b21_grade.py, b21_mcasp_ana.py, b21_restart.py; replay and independent receipts | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| Docs | UNCLEAN | entire 622-line diff, public task and evidence, cited authorities, exact-head author gate receipts and local docs checks | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |

No source fixes, hardware access, public writes, other reviewer reports or private handoffs were used. The final report remains pending only its assembly and the public prior-finding audit.
