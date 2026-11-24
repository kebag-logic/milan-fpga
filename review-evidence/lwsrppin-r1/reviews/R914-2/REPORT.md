[R914] POSITIVE - exact head ed7df79c6f87a4172c885f268ad67629bd56c4eb

Independent delta assessment, R914-2, issue #991 / PR #992.
Tree: `9065222f25fa3e23aa73783effe26694949ceaea`.
Reviewed delta: `dbba60e68a6e4a46f80e381c30ff823ee4ff7484..ed7df79c6f87a4172c885f268ad67629bd56c4eb`.
Two commits change three files, +34/-10. The full source-base range from
`aa30d77f75cd97b3a29878ca0ed68010a7629266` was inspected for scope/history;
unchanged round-1 implementation was not reopened.

This independent assessment and ledger were written before consulting prior
public review findings. Those findings were then read in the PR discussion and
reconciled below. No private author material or other checkout was consulted.

Authority and evidence provenance: [issue #991](https://github.com/kebag-logic/milan-fpga/issues/991),
[PR #992](https://github.com/kebag-logic/milan-fpga/pull/992), and the
[immutable public packet](https://github.com/kebag-logic/milan-fpga/tree/a2a3c4d0cc3dc2b27aa74f1dddcaa3fe428742c4/review-evidence/lwsrppin-r1).
Paths beginning `author-r2/` and `author-route/` below refer to that packet.
Local `receipts/` and `scripts/` paths refer to this review packet.
Reconstruction followed AGENTS/CONTRIBUTING, docs/README, the frozen issue and
public scope decisions, REQUIREMENTS and the SRP/submodule interface contracts,
then history/diff and executable evidence. Issue #991 has no comments at the
inspected snapshot. Manager review-start notices identify the review roles;
the live PR body records the accepted mapping and completed route condition.

[R914] PASS Conformance - `tb/verilator/milan_dp/twin_mrp.py:398-442` - The added traces test the Registrar's received LeaveAll at txLAF! against IEEE 802.1Q-2022 10.7.5.9, 10.7.6.6 and Tables 10-3/10-4. The starting registration is explicitly IN. After omission from a full frame, JoinMt is accepted with AA/LV or AA/MT; JoinIn is rejected. No normative behavior changes in this delta. Issue #991's original scope and Milan 4.2.7 remain unchanged.

[R914] PASS RTL - `dbba60e6..ed7df79c` changed-path inventory; `sw/firmware/ctrl/test/test_ctrl_firmware.py:80-85`; `author-r2/receipts/images/elf-hashes.txt`; `author-route/receipts/{base,head}/baseline_utilization.rpt` - No RTL, pin, firmware executable or image-input change. The firmware driver's executable AST is identical after removing its module docstring. Only selftest changes among the twin's functions/classes. Published rebuild receipts report 28 unique ELF/bin/hex paths identical to dbba60e6, both ledger builds PASS. The prior route remains applicable to these source inputs.

[R914] PASS Robustness - `tb/verilator/milan_dp/twin_mrp.py:416-468`; `receipts/mutants.log`; `receipts/adapted-probe.log` - The previously untested registered/full-frame combination now has positive and negative checks. All nine unmodified mutations are caught, including suppression of the Registrar's rLA!, and the control passes. The count is recorded at each executed check and appears on success and failure paths. Empty execution exits nonzero. The original five additional probe mutations remain caught.

[R914] PASS Tests - `tb/verilator/milan_dp/twin_mrp.py:398-468`; `receipts/runtime-census.log`; `receipts/legacy-census.log`; `receipts/mutants.log`; published `author-r2/receipts/twin/{twin.log,plants-full.log,times.txt}` - Independent profiling counts 11 distinct checks, matching the CLI's 11. The original census probe reaches its obsolete == 9 assertion as expected; changing only that pin to 11 allows its 72 table combinations, two decoder boundaries and five mutations to pass. Published exact-head execution records 0 twin findings and all 16 plants refused twice, 32 refusals. Those complete simulations were inspected, not rerun here.

[R914] PASS Docs - `tb/verilator/milan_dp/README.md:1404-1410`; `sw/firmware/ctrl/test/test_ctrl_firmware.py:80-85`; PR #992 body; `receipts/route-check.log` - New prose describes the Registrar case, runtime census and both firmware reproduction shapes. It introduces no private identity, review identity or source-comment lane label. PR counts agree with the packet, and its completed route table agrees with raw utilization and all eight timing-summary sections. The live body differs from author-r2/PR-BODY.md only in the completed route section. Published documentation receipts contain 44 successful steps.

Reviewer-owned ledger (delta coverage plus preserved unaffected scope):

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | twin_mrp.py:398-442; issue #991; IEEE clauses and existing SRP contract | R914-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| RTL | CLEAN | three-file delta; executable AST comparison; image hashes; raw route reports | R914-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| Robustness | CLEAN | registered/full-frame positive and negative traces; nine mutations; CLI failure/count path | R914-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| Tests | CLEAN | runtime census; original and adjusted probes; twin and plants receipts | R914-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| Docs | CLEAN | README and firmware docstring delta; live PR body; documentation and route receipts | R914-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |

No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION. No open reviewed finding
remains at this head. Unchanged round-1 scope retains its prior clean verdict;
this ledger records the independent delta pass and resolution of affected Tests
and Docs coverage, not a fresh execution of the entire source gate bank.

Prior public finding reconciliation:

- **R913-1-F1, MINOR, Tests: RESOLVED.** Public finding:
  [7120874663](https://github.com/kebag-logic/milan-fpga/pull/992#issuecomment-7120874663).
  Cause: the only full-frame self-test previously started with Registrar MT,
  allowing suppression of the Registrar's rLA! to escape. At
  `twin_mrp.py:434-442`, the new trace establishes IN, verifies the legal
  JoinMt outcome and rejects JoinIn. The unmodified `twin_mutants.py` now
  reports control PASS and all nine CAUGHT; `txlaf-registrar-kept` fails
  both new named checks, rc 1, rather than crashing. The exact-head published
  twin and plant receipts retain 0 findings and 16/16 plants refused.
- **R914-1-F1, MINOR, Tests and Docs: RESOLVED.** Public finding:
  [7120402143](https://github.com/kebag-logic/milan-fpga/pull/992#issuecomment-7120402143).
  Cause: a fixed printed total overstated executed checks. `check()` now
  appends each executed name, and the CLI derives its total from that list
  (`twin_mrp.py:416-423,462-468`). Profiling independently counts 11 distinct
  calls; the CLI prints 11. Both new cases account for the rise from nine.
  The original `probe_twin.py` is unchanged and stops at its old == 9 pin;
  this expected rc 1 is not a product regression or a passed test. With
  exactly that constant changed to 11, all remaining probes pass. Current
  README/PR claims match; historical receipts remain historical.
- **R913-1-S1, SUGGESTION, Docs: ADDRESSED.** The gate's `srp` docstring now
  names `srp_own_leaveall.cpp`, both shapes, every 8x8 input, the 5-200 ms
  withdrawal window, 240 ms Lv bound and no-withdrawal control. This is a
  docstring-only change, as confirmed by executable AST equality.

The prior internal report also carried two ungraded process observations:
issue-contract/takeover completeness, and older receipt-index wording about
published scratch paths. These are retained for manager triage; this delta
introduces neither and does not claim to resolve them. No prior graded
finding is deferred to another issue.

Evidence and execution limits:

- `receipts/evidence-verification.log` verifies all 346 author, author-r2 and
  author-route manifest entries against their **published** SHA-256 values.
  Packet commit `a2a3c4d0cc3dc2b27aa74f1dddcaa3fe428742c4` has tree
  `7523043ad6107e533d69a1601991e6d4014e863f`. It contains no commit signature;
  the packet supplies a hash manifest, not a separately authenticated signer
  receipt. Thus this review proves commit-pinned content integrity and does
  not claim cryptographic signature verification.
- Independent execution here consists of the focused mutations, census,
  adjusted table/decoder probes, receipt recounts, AST/delta checks and
  checkout verification. The four probe subprocesses ran concurrently under
  one foreground runner and all completed. No full bank, synthesis, route,
  hardware or container execution occurred. The published simulation/build
  version was inspected in receipts; no simulator was invoked here.
- The 28 identical image files are verified from the published hash/build
  receipts, not rebuilt or rehashed from unpublished binaries. Empty
  image-input delta and firmware AST equality independently support reuse.
  Full timing reports/checkpoints were not available as binaries: the
  published timing stubs include summary sections and full-file hashes.
- The route at `dbba60e6` meets the supplied condition and carries forward:
  8x8/1if, first directive `ExtraPostPlacementOpt`, versus `aa30d77f`.
  Raw post-route totals are 43,068 LUT / 51,015 FF versus 43,145 / 51,005
  (-77/+10); RAMB36/RAMB18/DSP remain 78/33/11. All four head corners
  pass the +0.030 ns WNS / nonnegative WHS floor; worst head WNS/WHS is
  +0.194/+0.032 ns, base +0.193/+0.036 ns. The live PR table agrees.
  This is routed source-image evidence, not a new route of the final merge
  candidate. The published route has no bitstream.
- Complete licensed standards were not reopened in this delta review. The
  frozen issue reading, repository contracts and unchanged state tables
  govern the test expectations; no new clause interpretation is claimed.
- The original reproduction, firmware shards, load/flip, harness, ledger and
  mapping evidence remains source evidence from the author's earlier
  published receipts. Exact-head twin/docs receipts are identified above.
  **No manager source bank at this head is claimed or inferred.**
- Physical calibration is **NOT RUN**. Field skips and simulations are not
  hardware proof. #990 remains outside this issue's frozen scope.

Pending manager duties:

- Complete independent review accounting and exact-head hosted/act acceptance.
  No hosted acceptance is asserted here, and skipped contexts are not counted
  as executed jobs.
- Build and validate the final current-dev merge candidate, including builder
  and native banks, and link its receipts. Source base remains
  `aa30d77f75cd97b3a29878ca0ed68010a7629266`; supplied live dev is
  `e275d7950ef3385753e6a15d2e191ba855b171ed`. Source-head evidence does not
  substitute for that candidate's evidence. Other shapes await their next
  composed route as recorded in the PR.
- Obtain merge authorization, finish post-merge containment and public issue/
  project completion under CONTRIBUTING. This review authorizes no merge.

Checkout preservation: `receipts/checkout.log` verifies 1,943 root entries,
exact blob bytes, executable/symlink modes and index equality, plus every
tracked entry in the five initialized required submodules. All six gitlinks
match HEAD; only the unused `external` import is uninitialized. No source
restoration was necessary. No source fix, commit, push, GitHub write, author
contact, shared installation or hardware access was performed.

Reproduce from this packet directory:

```sh
python3 -I -B scripts/run_probes.py <candidate-root>
python3 -I -B scripts/verify_evidence.py <candidate-root> <extracted-public-packet>
python3 -I -B scripts/check_route.py <extracted-public-packet> receipts/pr-body.md
python3 -I -B scripts/verify_checkout.py <candidate-root>
```

`<extracted-public-packet>` is the immutable commit's
`review-evidence/lwsrppin-r1` directory. `receipts/probe-provenance.log` proves
the original two reviewer probes and author census script were copied without
changes; the adjusted probe changes only == 9 to == 11. Only files listed in
MANIFEST.sha256 and REPORT.md are publishable. `scratch/` is excluded.

R914-2 FINISHED
