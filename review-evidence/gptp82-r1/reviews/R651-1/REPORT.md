[R651] NEGATIVE - exact head 85373de08a5c35487f260087ac8ceaf7a3789cdc

The required behavior is incomplete. Cold boot still publishes zero for about 1.2003 seconds; capability loss can prevent return from a departed peer; and a warm reset can resurrect an absent old winner. Required parent consumer mutation evidence also remains incomplete. These are behavioral and acceptance defects, not wording residue.

Reviewed tree: `322597c55a18b4f9a80f93e00dbe1256539f0cbe`. Source base: `b9ade3a63d1b2292d75eb9b1809647e6439542a0`. Parent reference: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. No source fixes, commits, pushes, external writes, parent builds, or hardware actions were performed.

**Authority and independence.** The supplied repository instruction was read first; the checkout has no tracked `AGENTS.md` or `CONTRIBUTING.md`. Reconstruction covered `docs/README.md`, README and current role guides; the [issue body](https://github.com/Mister-M-alt/FPGA-gPTP/issues/82) and [exact assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/82#issuecomment-6249575055); parent requirements and publication interfaces; the full base-to-head diff and three commits; then the [published evidence](https://github.com/kebag-logic/milan-fpga/tree/40ed29fcc1ed0b6f785b4d28b646b86796f6460b/review-evidence/gptp82-r1), PR text and public handoff. No public scope decision waives cold-start publication, incapable-peer departure, or post-reset election correctness.

The frozen acceptance requires thisClock/{thisClock} from reset, selection of a winning peer, and return to thisClock after departure. It cites IEEE 802.1AS-2020 10.3.13.2.4 b), i); the requested path authority also includes 10.3.9.23. Milan v1.2 5.4.2.23 and 5.4.2.24 identify GET_AVB_INFO and GET_AS_PATH. Parent [REQ-PTP-07 and REQ-CSR-02](https://github.com/kebag-logic/milan-fpga/blob/e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f/REQUIREMENTS.md) require atomic publication and coherent multiword consumption. Final-edition standards texts were not independently obtained: clause obligations here are grounded in the frozen acceptance and supplied review scope. An accessible draft was not used as final-edition conformance proof.

The independent diff pass preceded public author evidence. `independent-verdict.txt`, including verdict and five-lens ledger, was written before checking other review findings. No other reviewer's report was read. Final enumeration found three issue comments, two PR review-start comments, zero submitted reviews and zero inline comments. There were no prior public FINDINGS to resolve or retain in that snapshot. See `issue-comments-final.json`, `pr-comments-final.json`, `pr-reviews.json`, and `pr-inline-comments.json`.

**R651-F1 — MAJOR — Conformance, RTL, Robustness, Tests. Cold boot still publishes zero.**

Artifacts: `hdl/top/KL_gptp_engine.sv:156`, `:823`, `:851`, `:983`, `:990`; `tb/verilator/engine/sim_main.cpp:1155`; `docs/INTEGRATION.md:486`. The identity mirror initializes invalid, only the first timer handler installs it, and the new output selection explicitly chooses zero until then. The timer is armed for 1200 ms. The new cold test accepts the first timer beat as its deadline, missing the preceding interval.

Evidence: `control-cold.log`, rc 1. With no peer traffic, both identity and count fail immediately after release. At one second: GM 0, count 0, commits 0. The first commit arrives 2,400,604 cycles after release at 2 MHz, or 1.200302 seconds; it then correctly publishes `02a1b2fffec3d4e5`, count 1. The integration guide and public handoff acknowledge the delay; acknowledgement does not amend assignment item 1 or the issue's first done condition.

Impact: the parent shadow and its public consumers retain the original fault after power-up. Required outcome: provide the self tuple at the required reset boundary and coherently commit it. Any necessary interface/parameter change must follow the assignment's STOP rule. Add a cold-start test and planted mutant that grade reset release and the pre-timer interval.

Verification: the `cold` scenario in `run_probes.py` must pass immediate identity/count and early publication checks, followed by existing peer transitions and mutation controls. Waiting 1.2 seconds before grading is insufficient.

**R651-F2 — MAJOR — Conformance, RTL, Robustness, Tests. Capability loss prevents return from a departed peer.**

Artifacts: `hdl/ucode/gen_gptp_ucode.py:1639`, capability gate `:1642`, repeated rearm `:1646`; new test `tb/verilator/engine/sim_main.cpp:4742`, `:4768`. The new departure case keeps `PD_NORMAL` active. It tests Announce silence while Pdelay remains responsive.

Evidence: `control-gone.log`, rc 1. A valid three-entry peer is elected. Pdelay responses are withheld while Announces continue; the probe verifies capability low. All peer traffic then stops for seven seconds. GM remains `0082a0fffe000001`, count 3, flags 1, with seven further commits. Both self-GM and self-path checks fail; setup checks pass.

Impact: an expired peer and its old path keep feeding public consumers. The new fallback cannot help because raw GM remains nonzero. This gate predates the delta, but assignment item 1 expressly requires departure behavior, and the added test excludes the failure. The public handoff discloses the limit without a public waiver.

Required outcome: expire the unavailable vector and coherently publish thisClock/{thisClock} even when capability has fallen, preserving any separate prohibition on transmission through an incapable port. Add capability-loss-then-departure coverage and a planted defect.

Verification: `gone` must return to self within the receipt-expiry bound with capability low and no further peer traffic. Check every committed tuple and retain the Announce-only departure control.

**R651-F3 — MAJOR — Conformance, RTL, Robustness, Tests, Docs. Warm reset can resurrect an unelected old peer.**

Artifacts: `hdl/top/KL_gptp_engine.sv:681`, `:983`; `hdl/ucode/gen_gptp_ucode.py:1555`, `:1589`, `:1606`, `:1614`; new source explanation `tb/verilator/engine/sim_main.cpp:4731`. Reset clears the outward scalar bank but retains the best vector and selected raw path. The fallback masks this state temporarily; a later Announce can select and republish it.

Evidence: `control-warm.log`, rc 1. Peer A, priority1 1, is elected with a three-entry path. The probe resets and verifies initial self publication. After capability returns, the only new Announce comes from B, priority1 2: better than local priority1 248, worse than A. Publication returns to A (`0082a0fffe000001`, count 3), not B (`0082b0fffe000001`). All setup checks pass. The submitted new test uses priority1 0, better than every retained record, and therefore misses this case.

Impact: consumers see self followed by an absent old winner. Retention predates this change but defeats its post-reset claim and the assigned winning-peer transition. The new comment stating that warm reset clears every port vector is false for this execution. This is a conformance claim, not RESIDUE.

Required outcome: invalidate pre-reset election eligibility while retaining only intended configuration. A valid post-reset peer better than thisClock must compete without an absent old peer. Correct the explanation and add a regression with a retained-vector mutant.

Verification: `warm` must elect B with B's one-entry path; additionally verify a worse-than-local newcomer leaves self selected. Retain immediate warm-reset publication and the existing peer-win control.

**R651-F4 — MAJOR — Conformance, Tests. Required source-head parent mutation gates did not pass.**

Artifacts: published `author-receipts/pgates/head/gptp_shadow-mutants.log` and `gptp_tables.log`, copied under `public-evidence/`. Both terminate with `REFUSED: required dependency gitlinks differ from HEAD` and make error 2. Their clean simulations pass; their mutation arms do not complete. The public handoff confirms the source gitlink was staged only in the parent index. Base-head mutation success is not source-head success.

Authority: assignment item 3 and the parent-consumer-gates done condition. No manager evidence comment waives these arms. Impact: source acceptance remains incomplete; pending current-dev candidate work cannot be credited as successful source validation.

Required outcome: publish successful required consumer mutation receipts from a legitimate parent snapshot containing the intended source gitlink, preserving the dependency guard; or obtain an explicit public acceptance decision defining an alternative. Do not bypass the refusal or call it a pass. Parent documentation-pin and ROM-ledger preparation also remains necessary.

Verification: both arms must execute their controls successfully with parent/source identities recorded. The manager's eventual final-candidate gates remain a separate obligation.

**Positive evidence and limits.**

Parameter and port declarations match after comment/whitespace normalization at source base and head (`interface-check.json`). The parent consumes the same widths at `hdl/milan/milan_datapath.sv:1515`; `KL_gptp_shadow.sv:733` captures the whole bank on commit. The engine preserves the existing microcode commit and adds a registered boot commit. No interface STOP condition was observed.

The focused positive control reuses only issue-related portions of the published harness against unchanged production RTL/program and passes 28 checks. All six planted defects fail every #82 check they name (`probe-results.json`, `mutant1-named.log` through `mutant6-named.log`). This confirms sensitivity of the submitted ten checks to those six defects, not sufficiency of their scenario boundaries.

A reviewer-added monitor samples before the receiving sequential edge. Across the four unmutated scenarios it observes 38 commits, checks complete expected GM/count/tail tuples and pulse width, and finds no inconsistency or extended pulse. The failures are coherent publication of wrong state or missing publication, not an observed torn read. This bounded engine monitor is not a complete parent response-interleaving campaign.

Local `make -j16 contract`, `make -j16 lint`, and `make -j16 docs` pass, including diagram and documentation self-checks. Current guides, changed source anchors and comments were examined. No new lane names, bench labels, review identifiers or issue-comment identifiers were found in added source comments. Existing historical labels were not counted as new residue.

The public `author-receipts/` directory exists at evidence commit `40ed29fcc1ed0b6f785b4d28b646b86796f6460b`. Downloaded files match its published manifest digests (`public-evidence-index.json`). `public-gates-summary.txt` records examined results. Author repository receipts report engine 1623 checks in each of three images and 39 caught controls; microCPU 768; parser 337 plus 9 controls; gaskets 81 plus 5; field-input suite 288 plus 4; bench tag, lint, contract and docs pass. These are author executions, not a manager source bank or reviewer full-bank rerun.

Parent author receipts report passing clean simulations: shadow 309, tables 36, timestamp return 85 plus 6 controls, plane 29, phase-step 62 plus 8, field campaign 677, datapath consumer legs 182/182/190. Elaboration and interface/lint checks pass. The two refusals are F4. Parent docs initially fail 35 pin-reference findings and pass after scratch pin updates; the ROM ledger likewise needs a new-pin entry. Those scratch-adjusted passes are not a committed final candidate. Other full consumer campaigns and parent mutants listed as unrun in the handoff remain unrun.

Exact-head hosted queries found zero workflow runs and zero check runs (`hosted-runs.json`, `check-runs.json`). No executed hosted job or skipped context is credited. No manager source bank exists at this head. Physical calibration is NOT RUN. Field skips and simulated field campaigns are not hardware proof.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1–F4 | Issue/assignment; parent REQ-PTP-07/REQ-CSR-02; reset, election and timeout behavior; consumer receipts | R651-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| RTL | UNCLEAN — F1–F3 | Engine reset/output/commit logic; initialization, BTCA and receipt gate; shadow/datapath; declaration comparison | R651-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| Robustness | UNCLEAN — F1–F3 | Cold initialization, retained warm state, capability loss/silence; independent probes and consumer-edge monitor | R651-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| Tests | UNCLEAN — F1–F4 | New cases and six mutants; 28-check focused control; three failing probes; author repository/parent receipts | R651-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |
| Docs | UNCLEAN — F3 | Current guides and ledger; new phase-35 reset claim; public PR/handoff; passing docs gate | R651-1 | 85373de08a5c35487f260087ac8ceaf7a3789cdc |

**Reproduction, integrity and pending duties.** `run_probes.py SOURCE PACKET --jobs 16` creates copies under `PACKET/scratch`, runs at most four campaigns with four build jobs each, and records output/return codes. It verifies the supplied pinned simulator identity first. `check_review.py SOURCE PACKET` runs lightweight gates and verifies every tracked blob, executable/symlink mode and index entry against the head. Probes drive public inputs and sample outputs; production source is not patched. The three expected rc 1 results are acceptance failures, not infrastructure failures.

All launched work was joined through foreground commands. Final `source-integrity.json` verifies head/tree and tracked bytes/modes/index. This source repository has no submodule gitlinks. `parent-gitlinks.json` records the pinned parent's public map; no parent checkout was created or modified. Disposable trees remain under `scratch/`, excluded from publication. Only `MANIFEST.sha256` entries and this report are publication artifacts.

The manager owns source-evidence acceptance and hosted/local acceptance. After findings are resolved and independent review is positive, the manager must build the current-dev merge candidate, apply required dependency/documentation/ROM-pin updates, run builder and native banks, and link candidate receipts on the PR. Source base and live parent dev are distinct; no result here claims final-candidate success. No full parent bank, full source-bank rerun, placement/routing, hardware or calibration was performed by this reviewer.

R651-1 FINISHED
