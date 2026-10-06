[R515] POSITIVE - exact head 41bc9dac031526c1fd637ff1e801d3c6dc1260b4

Round R515-2. External independent delta review of issue #667 / PR #680.
Tree: `1a233401c2f5d585b7a0a2d1a7db16daff6d29b6`.

R515-1-F1 is resolved by the public baseline clarification and the accurate
published-head qualification in the PR body. No open finding remains from
this review. All five lenses were applied to this delta; the other R515-1
results stand at the same, unchanged head. This is source review approval,
not final merge-candidate validation or physical verification.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue
body and public scope decisions, REQUIREMENTS.md and linked timing/interface
authorities, then the requested `423ac5d9..41bc9dac` diff and history.
The startup delta and inherited render changes were examined before reading
the prior public R515-1 finding. Published source evidence was then checked.
No other reviewer's report or private author material was used.
Primary-clause conclusions from R515-1 are retained; this delta changes
neither a protocol requirement nor its interpretation.

After this verdict and ledger were written, the public findings inventory
was refreshed: zero submitted reviews, zero inline comments, and only the
[R515-1 report](https://github.com/kebag-logic/milan-fpga/pull/680#issuecomment-6016173689)
carrying a prior finding. Its sole finding F1 is explicitly resolved below.
The inventory is retained in `receipts/pr-findings-inventory.json`.

**Resolved finding: R515-1-F1 | previous severity MAJOR | Conformance, Tests, Docs**

- **Artifact:** PR #680, final manager note headed “#657 equality at the
  published head”; issue ruling 6016181662; exact raw epoch receipts in
  `receipts/prior/receipts/epoch-{base,head,dev}-run.log`.
- **Authority/evidence:** [Ruling 6016181662](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6016181662)
  clarifies [ruling 6012843714](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6012843714):
  after the manager's merge, use merge-parent dev
  `bd884631684ccf5060339efa92263d5c3e5c262c` for equality. The ruling explicitly
  accepts the already measured clean-leg equality. Git confirms that this
  is the head's second parent. Rehashing the immutable public R515-1 raw
  receipts confirms the table below and four identical failure lines across
  all three inputs. Every recorded executable return code is 1.
- **Impact at R515-1:** The original 32-run comparison named the original
  source base and author head; it could not establish equality between the
  original base and published merge head. The public clarification resolves
  that baseline ambiguity without changing measurements or tests.
- **Required outcome, now met:** The baseline has a public disposition.
  The PR names the published head, merge parent, exact byte count, check
  count, failures and digest. It labels the `423ac5d9` versus `5d6164a2`
  comparison as predating the merge. The earlier 32-run comparison remains
  historical source evidence, not a newly executed campaign at `41bc9dac`.
- **Verification:** `scripts/verify_delta.py` returns 0 after independently
  comparing raw bytes, manifests, source closure, commit parents and actual
  tracked files. `scripts/snapshot_public.py` returns 0 and retains the
  current public decision and PR wording. See `receipts/delta-audit.json`,
  `receipts/public-decisions.json` and `receipts/pr-body.md`.

| Public R515-1 epoch receipt | Checks / failures | Bytes | SHA-256 |
|---|---|---|---|
| Original source base `423ac5d9` | 114 / 4 | 3745 | `7876a3a277df5e06a9381e502249b9638b7a4e04ec676fefba207150b41d4007` |
| Published head `41bc9dac` | 127 / 4 | 3746 | `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b` |
| Merge-parent dev render closure `bd884631` | 127 / 4 | 3746 | `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b` |

The dev receipt came from R515-1's controlled build: the exact-head render
closure with the exact dev packetizer substituted. Its other HDL, harness,
recipes, configuration, generators and required gitlinks equal dev.
The archived driver and current source-closure check establish that
construction; it is not represented as a new checkout/build. The original
base's different descriptor bursts, commit-to-pin intervals and CRF margins
come from inherited dev changes. Complete stdout is compared without
deleting or normalizing those measurements.

The PR's appended qualification accurately supplies the current comparison.
Read with its named local author candidate and manager notes, the earlier
validation narrative does not claim that 114 checks or the old digest
describe `41bc9dac`. No additional wording finding or RESIDUE is raised.

**[R515] PASS Conformance - issue comments 6011846710, 6012843714 and
6016181662; REQUIREMENTS.md section 8; packetizer lines 318 and 728.**
The exception now uses the publicly designated parent. The first-sample
PHC-plus-offset contract and port/register/parameter constraints remain
unchanged. The original protocol and area conclusions stand. Resolving F1
does not claim that #657's behavior was repaired.

**[R515] PASS RTL - `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:318`, `:591`,
`:715`, `:728`, `:742`; `docs/integration/INTEGRATION_GUIDE.md:103`.**
The unchanged per-talker gate waits for owned pair zero. Reset and disable
clear admission; the first accepted sample acquires the existing timestamp
path. No new clock crossing, interface or width change accompanies this
disposition. The seven paths against dev preserve the startup change, with
its reader-table entry relocated as documented. The render harness equals dev.

**[R515] PASS Robustness - `tb/verilator/aaf/sim_start.cpp:75`, `:151`,
`:207`; `tb/verilator/aaf/start_mutants.py:24`; same-head R515-1 evidence.**
The clarification changes no reset, disable/re-enable, phase, wrap, stall,
bounded-arrival or stream-isolation behavior. The standing sweep cases and
defect controls were inspected. Its 486 starts / 4,860 PDUs and R515-1's
independent mixed-width eight-talker probe remain applicable. Accepting the
baseline introduces no new robustness exception.

**[R515] PASS Tests - `tb/verilator/aaf/Makefile:22`,
`tb/verilator/aaf/sim_start.cpp:113`, `tb/verilator/aaf/start_mutants.py:51`;
`receipts/delta-audit.json`.**
The sample-based oracle and requirement for a named assertion failure are
unchanged. R515-1's 34,020-check startup pass and eight killed controls stand.
This round checked actual epoch bytes and return-code receipts, rather than
inferring equality from summaries or the four failure lines alone.
All 19 source-publication manifest entries and 14 selected R515-1 evidence
entries match their published hashes. The historical full comparison still
names `423ac5d9` and `5d6164a2`, with 32 matching records; it was not relabeled
as a fresh full campaign at the published head.

**[R515] PASS Docs - `docs/design/TIME_SYNC.md:501`,
`tb/verilator/aaf/README.md:13`; `receipts/pr-body.md` and
`receipts/public-decisions.json`.**
The startup contract and simulation limits remain accurate. The PR states
the accepted merge-parent comparison and distinguishes the earlier source
result. The four #657 failures and surviving uncounted-repeat mutant remain
disclosed under the public exception. No test or conformance claim was
changed to make an unsuccessful measurement appear successful.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue rulings 6012843714/6016181662; REQUIREMENTS.md section 8; packetizer:318, :728; delta-audit.json | R515-2 resolves F1; other R515-1 results retained | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| RTL | CLEAN | KL_aaf_packetizer.sv:318, :591, :715, :728, :742; integration clock contract; source-closure/parent audit | R515-1 retained; R515-2 continuity checked | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Robustness | CLEAN | sim_start.cpp:75, :151, :207; start_mutants.py:24; same-head R515-1 startup and multistream evidence | R515-1 retained; R515-2 continuity checked | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Tests | CLEAN | AAF Makefile:22; sim_start.cpp:113; start_mutants.py:51; raw epoch logs/rc; publication manifests | R515-2 resolves F1; other R515-1 results retained | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Docs | CLEAN | TIME_SYNC.md:501; AAF README:13; snapshotted PR body and public clarification | R515-2 resolves F1; other R515-1 results retained | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |

**Limits and pending manager duties**

- This delta round revalidated immutable public receipts; it ran no new
  simulation, campaign, full bank or synthesis. Other same-head verdicts
  stand. No new 32-run current-parent campaign is claimed. The public ruling
  supplies F1's acceptance disposition.
- The manager reports passing source static/builder and native banks at
  this head. That validation is separate from the final current-dev candidate.
  At the merge turn, build and validate the candidate against then-current
  dev, record its base/head/tree, finish hosted and local workflow acceptance,
  and satisfy the independent review bar. This report does not authorize a
  merge or claim those duties are complete.
- No hosted context was re-polled in this round. A skipped context is not
  executed evidence. Optional physical calibration remains NOT RUN; field
  skips and physical-rate simulation provide no hardware proof.
- Retain the authorized #657 failures and surviving control as open work.
  After merge and flashing, repeat B13's 100 binds, inspect initial PDUs and
  listener EARLY/LATE counters, complete post-merge containment, and then
  complete the issue's final workflow state.

`receipts/tree-integrity.json` verifies the exact head/tree, actual tracked
blob bytes and modes, index entries, and the three required registered
submodules at their gitlinks. No source edits, commits, pushes, GitHub writes,
other-checkout edits, delegation, hardware operations or local workflow
orchestration occurred. All commands completed in the foreground.

Portable scripts are in `scripts/`. Prior drivers under
`receipts/prior/scripts/` are archived source evidence, not new executions.
Run the fetch script, public snapshot script and delta verifier with packet
and checkout paths as shown in their usage. Raw results and return codes
accompany them. Only this report and files listed in `MANIFEST.sha256` are
publication inputs; `scratch/` is excluded.

From the packet directory, the receipt checks are reproducible with:

```sh
python3 scripts/fetch_public.py .
python3 scripts/snapshot_public.py .
python3 scripts/verify_delta.py <exact-head-checkout> .
sha256sum --check MANIFEST.sha256
```

The snapshot command records the public state when it runs; rerunning it
later changes the retrieval timestamp and can observe later PR edits.
Verify the publication manifest before refreshing those snapshots.

R515-2 FINISHED
