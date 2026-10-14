## Round 6

REVIEW READY at parent `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`.
Starting parent: `4c5d70b50230fbd5da347852d39daf7f23b3df0b`.
Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`, unchanged.
Assignment: issue #640 comment 6164557611.

The origin URL matches the assigned repository.
The branch reflog records creation from `e8454e2751d05b02ee8e5a571857589ab358ab86`.
The new commit directly follows the assigned starting parent.
Both worktrees are clean; the donor root matches its directory.
The repository-local identity was used without configuration changes.
The commit subject is one line, without body or trailers.

### Changes

| File:line at the new head | Change and finding |
|---|---|
| `docs/testing/CI_WORKFLOWS.md:1322` | R592-5-F1: describes `--expect` as the worker matrix size, six for Verilator and four for Yosys. |
| `docs/testing/CI_WORKFLOWS.md:1337` | Optional R592-5-S1: a seven-worker matrix with a stale total of six; the omitted shard example on line 1338 is 6/7. |
| `PR-BODY.md:16`, reproduction at 88, limitations at 142 | R593-4-D1: exact published-revision and checkout sentences; no-push/no-PR-edit claim explicitly describes the executor's implementation stage. |
| `PR-BODY.md:180` | Names the unpushed continuation and current checks separately from historical evidence. |

Only the documentation file changes in the repository: three lines replaced.
No RTL, generated artifact, workflow, test, Makefile or donor change occurred.
The existing O9 fixture at `scripts/ci_events.py:5256` expands six workers
by appending worker six, while retaining a literal denominator of six.
The optional example now describes that fixture accurately.

### Gate table

All commands ran in the foreground, without pipelines, under CPython 3.12.3.
The existing disk-scratch environment supplied the declared dependencies.
Logs remain under the lane's `round6` scratch directory.

| Command or check | Exit | Result and defect coverage |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | Zero findings across 207 Markdown and 1299 scrubbed text files. Built-in planted scrub controls pass 23/23 and routing controls 4/4; they detect forbidden identity/path text and invalid document routing. |
| `python3 scripts/ci_events.py --check` | 0 | 2175 contract items across four workflows and the policy document. Detects workflow/contract drift, including matrix/aggregate count mismatches. No new CI mutation run is claimed. |
| `python3 scripts/check_doc_style.py` | 0 | All 22 audience documents pass. Detects excessive prose length in its declared inventory; the changed CI policy is outside that inventory. |
| Direct count and scope audit | 0 | Documentation agrees with six/four matrix lengths, singleton totals, aggregate verifiers and contract literals; no stale `--expect 5` remains. This is an assertion audit, without a planted mutant. |
| `python3 scripts/check_em_dash.py --base 4c5d70b50230fbd5da347852d39daf7f23b3df0b` | 0 | Zero findings over the three added lines; 339/339 built-in controls pass, covering added em dashes and false navigation exemptions. |
| `git diff --check 4c5d70b50230fbd5da347852d39daf7f23b3df0b HEAD` and final source audit | 0 | Whitespace clean; only the authorized document changed; exact parent and donor identities, commit format and clean worktrees verified. No planted mutant. |

The three required checks ran on bytes committed unchanged at this head.
The em-dash check and source audit ran after the commit.
The documentation correction adds no behavior requiring a new test.
Previous table controls and their named defects remain in the Round 5 table.

### Primitive, resource and route evidence

No synthesized input changed; no synthesis or route ran this round.
The before/after mapping remains the historical M0s measurement, not a
new measurement of this head:

| Storage | Before | After |
|---|---|---|
| Tap and TX FIFO, each 256 beats | Each RAMB36 + RAMB18 | Each one RAMB36 |
| Ledger, 8 x 21 | 168 FF plus mux | 4 RAM32M + 1 RAM32X1D |
| Results, 8 x 89 | 712 FF plus mux | 16 RAM32M + 1 RAM32X1D |
| Timer, 8 x 32 | 256 FF plus mux | 5 RAM32M + 2 RAM32X1D |

| Historical M0s metric | Base `e8454e27` | M7 `49e1ce48` |
|---|---:|---:|
| LUT | 50267 | 49898 |
| FF | 54413 | 53220 |
| Slices | 15779 | 15773 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 25 |
| WNS / WHS, ns | +0.299 / +0.031 | +0.122 / +0.019 |

The historical route passed its then-current gate with every endpoint met.
The isolated plane saving remains 107-253 LUTs, below 500 (300-700),
plus 1149 FFs and one tile. These figures do not qualify the merged tree.
D7 still reserves acceptance re-recording for M9; none occurred here.
The post-merge daily area measurement remains assigned to integration.

### Delivery and evidence limits

One new parent commit: `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`,
`Align CI worker-count documentation with the matrix`.
No push, PR edit, merge, hardware access or donor mutation occurred.
The PR body records the observed published parent `4c5d70b5` and donor
`e4869fd0`, followed separately by the local Round 6 continuation.
Its exact publication sentences therefore describe existing published revisions.
The status should advance to the continuation when it is published.

All work was awaited. No simulation build or route ran.
The final source audit records service memory below the 9 GB ceiling.
No installed dependency, export or build tree entered the output directory.
Every output file remains below 200 KB.

This is implementation evidence, not a review verdict or merge clearance.
Corrected-head review and the repository's remaining integration gates still apply.
New issue REVIEW READY comment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6164684520

### Round 6 receipts

Original logs stay in disk scratch. Their sizes and SHA-256 identify the bytes.

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `ci-events.log` | 167 | `1d6cd17ae0e330d2f2cd96ed2860848271e3b99f2e7c13c6e5e9583312518a0b` |
| `count-audit.log` | 256 | `5ae75b8881fcb6bebb4dd73608601ea3d6abc62c8b1ea264d3027cea871fc9b7` |
| `doc-style.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs.log` | 128 | `afd69244ae6e7091eb4b64694f7d41e43df44ce57725a896bb48a551fdfd2584` |
| `em-dash.log` | 138 | `9822e83c45f37b2084bda59659283e7653d49ed1fcf4cfc6c41afbe1d0162a37` |
| `final-source-audit.log` | 390 | `48c3e14be4d487f907df99ce6da13d08ee0456516dba7c7615e85439da74dd13` |
| `output-audit.log` | 224 | `6f4e1e9ee4fc2e57498a02f9d942cb8c37d8a3f2f77ca1c7fb6cd077291ab3f7` |

The output audit confirms template sections, exact requested wording,
revision labels, neutral roles, privacy and the 200 KB file-size limit.
