[R617] POSITIVE - exact head a70e38804cb16435c089d024c58e8c3fb4d39ff6

Independent pass completed before reading either prior review comment/report.
No open BLOCKER, MAJOR or MINOR found within issue #35's amended scope.

The binding authorities are the issue body and public scope comments
6104916029, 6105366046 and 6105869522. The last permits speculative writes
through the flagged byte, requires none afterward, and requires an accepted
successor to expose only its own fields. The contract does not require
buffering a whole frame or zero total writes on late errors.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance and scope rulings; parser header/port and lines 632/652; 284-position required sweep; before/on/after oracle; successor field comparisons | R617-2 independent | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| RTL | CLEAN | Full parser and engine bank-write/event-selection paths; base-to-head diff and seven-commit history; normalized round-one/head code identity; published parent tie-off/equivalence/ROM receipts | R617-2 independent | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| Robustness | CLEAN | SOF-clear precedence, direct EOF error term, gaps, reset, adjacent refusals, extended seven-message-type probes, padding, path-bearing Announce, counter rollover | R617-2 independent | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| Tests | CLEAN | Parser 337/337; clean control plus eight mutants with all required named failures; extended probe 36129/36129; docs/contract/lint exit zero; mutation verdict and Makefile integration | R617-2 independent | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |
| Docs | CLEAN | README and all current role guides; source-evidence anchors; parser README/header/port; PR acceptance item 2; documentation checks and selftests | R617-2 independent | a70e38804cb16435c089d024c58e8c3fb4d39ff6 |

Exact-head local receipts: receipts/local/{parser.log,mutations.json,edges.log,
docs-contract-lint.log}; full raw mutant build/run logs and return codes kept.
The extended probe covers 4080 refused frames plus clean controls, 1136
zero-gap ordered type pairs and 65536 flagged runts crossing counter wrap.

Limits: parser-level behavior and static consumer mapping, not an independent
engine error-injection campaign. No parent/full source bank, synthesis,
implementation, hardware or physical calibration was run. The pinned public
raw gate bundle identifies round-one head 5b4ce397, not this head. Exact-head
full donor gates are reported in the author's public round-two comment and
PR body; those reports are not relabeled as independently rerun banks.
No source workflow runs/check runs were returned for this head. Manager
candidate construction, builder/native banks, hosted acceptance, required
independent approvals and adoption remain merge-turn duties.

Checkout audit: 105 tracked entries, bytes and executable modes equal HEAD;
index equal tree; no nested submodule gitlinks; clean worktree. Probe changes
exist only under packet scratch. Prior public findings reconciliation follows
this independent verdict.
