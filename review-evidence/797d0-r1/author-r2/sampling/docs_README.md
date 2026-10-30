# Sampling ledger: docs/README.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 51 | item | Summaries never override normative requirements. | - | policy: AGENTS.md section 2 authority order |
| 61 | row | \| Trace clocks, resets, and crossings \| [Clock-domain guide](litex/CLOCK_DOMAINS.md) \| | path 1 | ok: docs/litex/CLOCK_DOMAINS.md exists |
| 72 | row | \| Follow a stream's media clock \| [Media-clock following, implemented](design/MEDIA_CLOCK_FOLLOWING.md) \| | path 1 | ok: docs/design/MEDIA_CLOCK_FOLLOWING.md:6 implemented (fixed in round 1) |
| 73 | row | \| Review the firmware saved-state store \| [Saved-state store, F1](../sw/firmware/ctrl_nvm/README.md) \| | path 1 | ok: sw/firmware/ctrl_nvm/README.md:2 '#665 F1' |
| 74 | row | \| Review the firmware AECP owner and its evidence \| [AECP core and adapters, F5](../sw/firmware/ctrl/aecp/README.md) \| | path 1 | ok: sw/firmware/ctrl/aecp/README.md:4 'Lane F5' |
| 75 | row | \| Review saved-state snapshot ownership \| [Snapshot ownership, implemented](design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md) \| | path 1 | ok: docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:6 'ACCEPTED, AND IMPLEMENTED' |
| 78 | row | \| Review the firmware mailbox \| [Packet mailbox split, F0](design/MAILBOX_SPLIT.md) \| | path 1 | ok: docs/design/MAILBOX_SPLIT.md:2,4 F0 implemented |
| 79 | row | \| Review the split placement's firmware memory \| [Split control memory, M8a-1](design/SPLIT_CONTROL_MEMORY.md) \| | path 1 | ok: docs/design/SPLIT_CONTROL_MEMORY.md:3 'M8a-1 implemented' |
| 116 | sentence | They never become universal guarantees. | - | policy: guidance |
| 120 | sentence | The implementation remains Milan-oriented. | - | ok: docs/reference/MILAN_COMPLIANCE_MATRIX.md verdict 'not fully compliant' |
| 122 | sentence | It is not fully Milan-compliant. | - | ok: same as line 120 |
| 128 | item | Review open Issues before planning delivery. | - | policy: guidance |
| 134 | item | Use the [historical v1 index](history/v1/README.md). | path 1 | ok: docs/history/v1/README.md exists |
| 135 | item | Historical pages never define current behavior. | - | policy: archive rule (scripts/check_archive.py) |
| 136 | item | Every historical page names its successor. | - | ok: scripts/check_archive.py:31 requires a 'Current successor' banner; gate b004 rc 0 |
| 145 | item | Never add an em dash; see [the rule](../CONTRIBUTING.md#61-the-em-dash-rule). | path 1 | policy: CONTRIBUTING.md 6.1; scripts/check_em_dash.py |
| 147 | item | Regenerate every committed render. | - | policy: CONTRIBUTING.md generated-file rule |
