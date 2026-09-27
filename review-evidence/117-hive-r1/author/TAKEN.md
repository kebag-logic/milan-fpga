[A373] TAKEN

Branch: `117-la-avdecc-enum`, base `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
Authoritative references: the [owner decision and assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858063707), REQUIREMENTS.md REQ-VER-05, and docs/findings/117_GPTP_SILICON_EVIDENCE.md.
Scope: prove the assigned running image on UART and AECP, repeat headless la_avdecc enumeration at least three times, record compliance verdicts, diagnostics, descriptors and provenance, and replace only the Hive entries and blocker B4. Other acceptance rows stay unchanged.
Validation: the assigned documentation gates, ci_scope self-test, bare-metal-only check and git diff whitespace check. Each bench action uses a bounded foreground command and its own bench lock.
Blockers: none identified; identity gate pending.
Review: independent reviewers assigned by the coordinator after this handoff; this operator supplies evidence only.
