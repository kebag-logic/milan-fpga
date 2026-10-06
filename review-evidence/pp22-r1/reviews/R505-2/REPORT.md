[R505] POSITIVE - exact head d52bd7f277c6339b13fe7c8ebe849b25f3e14638

Independent external review of issue #22 / PR #162, round R505-2. Tree: `7b74e9bc8bee72a089f20b38578ac6d64b474b96`. All five lenses are CLEAN. There are no open BLOCKER, MAJOR, MINOR or RESIDUE findings. Two earlier SUGGESTIONs are retained below. This verdict covers the source merge and the unchanged declaration fix; final integration acceptance remains with the manager.

The review followed the required reconstruction order: repository instructions and contribution rules; `docs/README.md`; public acceptance and scope decisions; linked interface/requirements authorities; the full `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8..d52bd7f277c6339b13fe7c8ebe849b25f3e14638` diff and history; then public executable evidence. No on-disk `AGENTS.md` or `CONTRIBUTING.md` was present in the checkout or searched ancestors, and neither was tracked. No private author material or other review report was read during the independent pass. The independent verdict and ledger were written to `receipts/independent-verdict.txt` before consulting earlier reviews; `receipts/prior-findings.json` records the subsequent reconciliation.

The [issue acceptance](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/22), [frozen assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/22#issuecomment-6008772151) and [round-2 start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162#issuecomment-6010668951) define declaration reordering, mutation compatibility, unchanged behavior and complete source analysis. The manager's [PR-body ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162) reserves the `Synth 8-6901` count and issue closure for the next parent pin adoption. `Relates to #22` remains accurate. The imported registrar behavior is documented by [issue #134](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134) and `docs/architecture/10_srp_engine.md:548`.

The merge has the expected two parents: first `2139f3dc10161b456dfbd51d2f73a63f9164e041`, second processor main `7e5415e0` (the full identifier is in `receipts/final-integrity.json`). The two #22 paths and the 24 paths imported from main are disjoint. Every imported path has exactly main's blob and mode. Both #22 paths have exactly the first parent's blob and mode. Every remaining tree entry agrees as well: the result contains no extra merge resolution or hidden source change. `git diff --check` is clean. These are direct tree comparisons, not a replayed merge; see `scripts/identity.py`, `receipts/base-head.diff` and `receipts/history.txt`.

The declaration moves remain byte-identical. `hdl/packet_engine/KL_pp_originator.sv:188` declares the cancel signals before their uses at lines 197–198. `hdl/packet_engine/KL_pp_rx_validator.sv:232` declares the intact FIFO/verdict groups before the use at line 385. All four declarations retain module scope, types and widths, without initializers. Removing only those declaration lines and blank lines from base and head yields identical ordered text, in addition to identical line multisets. No #22 port, parameter, register, driver or executable statement changed.

The #134 delta was independently examined in both registrar event chains (`hdl/srp/KL_srp_talker_fsm.sv:720`, `hdl/srp/KL_srp_listener_fsm.sv:747`), its tests, six new patch definitions and documentation. Expiry is no longer masked by a same-clock non-registering leave. A same-clock New/Join still ends IN, cancels the obsolete timer and preserves continuous publication; Lv/LA/In/Mt end MT. The pending-ARM guard remains. This agrees with architecture 10 section 6.5's composed Table 10-4 transitions and preserves the documented Milan immediate withdrawal from IN. The two diagnostic argument fixes in `tb/pp_top/d3_phases.hpp` also match main exactly.

The reviewer-owned ledger is:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #22 acceptance and manager ruling; `docs/README.md`; architecture 02 interfaces, 03 packet engine and 10 section 6.5; unchanged declaration semantics; exact main import | R505-2, with R505-1 coverage retained for unchanged #22 bytes | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| RTL | CLEAN | both moved declaration groups and their uses; both registrar expiry chains; full merge diff and tree identity; 46 per-file analysis receipts | R505-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| Robustness | CLEAN | originator cancellation/ownership model; validator malformed/frame/FIFO checks; SC1 simultaneous-event matrix; 6,416 integrated expiry offsets; six new fault definitions | R505-2; earlier unchanged donor controls retained | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| Tests | CLEAN | four focused default suites and walk/storage configurations; all 283 patches and 199 required exact-text arms; broader planting census; seven new fault rows and three controls; revision-bound public full-bank records | R505-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| Docs | CLEAN | architecture 10 section 6.5; stream-FSM and SRP-top READMEs against actual tallies; architecture 09 evidence rules; PR validation revision and deferred-synthesis wording; exact-head hosted docs execution | R505-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |

The local execution results are:

| Check at the exact merge head | Result | Receipt |
|---|---|---|
| Consumer-derived source list, packages first; separate `xvlog -sv --work work` per file | 46/46 rc 0; zero `VRFC 10-3380`, zero `VRFC 10-8530` | `receipts/analysis/table.json`, `receipts/analysis/*.log`, `sources.txt` |
| Originator default suite | 107 PASS, 0 FAIL | `receipts/originator.log`, `.rc` |
| RX validator default suite | 555 PASS, 0 FAIL | `receipts/rx_validator.log`, `.rc` |
| Stream-FSM default suite | 1,347 PASS; walk configurations 1×1, 2×2, 3×5, 9×9: 35/46/67/123 PASS; all zero failures | `receipts/srp_stream_fsms.log`, `.rc` |
| SRP-top default suite | 8,656 PASS; four storage configurations: 15 PASS each; all zero failures; 210,547,557 executed clocks | `receipts/srp_top.log`, `.rc` |
| Integrated expiry cases | 6,416/6,416 CLOSED; each has one STREAM_STOP and one TK_UNREGISTERED; eight LV-withdrawal cases complete | `receipts/srp_top.log`, `review-summary.json` |
| Every tracked `tb/**/*.patch` | 283/283 check, apply and reverse successfully, including all six new #134 definitions | `receipts/planting.json` |
| Required notification/ACMP/D3 exact-text tables | 56 + 33 + 110 = 199/199 plant through their own planting functions | `receipts/planting.json` |
| Additional exact-text and line-anchor coverage | 20 GSI, 3 admission, 70 retry, 1 name-write, 1 descriptor-guard, 135 NVM figure/model, 12 NVM line arms, 3 historical anchors pass; total planting census 727/727 | `receipts/planting.json`, `.log`, `.rc` |
| Adoption patches at frozen parent `28f9666f` | 148 then 22 both check/apply; resulting budget has zero entries and section count zero | `receipts/adoption-plant.json` |

The source list comes from the pinned public parent's `scripts/pp_srcs.py`, with only its source-root input pointed at this clone. It contains every tracked design source without exclusions. The frontend ran analysis only; no synthesis or implementation was invoked. Compiler identity was checked before use: 5.050, revision v5.050, with wrapper and binary hashes in `receipts/compiler-identity.json`.

The focused fault campaign completed 10/10 required outcomes: three clean controls and seven fault rows representing six new definitions. Every kill required a completed simulation tally and its named failing assertion, not merely a failed build.

| Fault | Graded suite/group | Observed failing checks | Required witness |
|---|---|---:|---|
| `lv-second-lv-ends` | SRP top / lvleave | 16 | S1, S2 |
| `lv-never-ends` | SRP top / lvleave | 16 | S2, S3 |
| `lv-expiry-masked` | SRP top / lvcoll | 16 | SC2 |
| `lv-expiry-masked` | stream FSMs / suite | 16 | SC1 |
| `lv-expiry-last` | stream FSMs / suite | 48 | SC1 |
| `lv-expiry-dropped` | stream FSMs / suite | 86, including 80 SC1 | SC1 |
| `lv-sweep-misses-collision` | SRP top / lvcoll | 16 | SC3 |

See `receipts/new-mutations.log` and the uniquely named suite/group logs and return-code files under `receipts/new-mutations/`. Both masked-expiry receipts are preserved. Planting the full 727-case census is a separate claim from executing these seven fault rows. Earlier #22 fault coverage stands because its source files and relevant tests remain identical; this round did not rerun every historical fault campaign.

All 16 files in the [pinned public evidence bundle](https://github.com/kebag-logic/milan-fpga/tree/2e889399824b70f9ed9a20c53d925e61a617a976/review-evidence/pp22-r1) match its published SHA-256 manifest. The complete base/head statistics pairs for both #22 modules and `protocol_processor_top` are byte-identical in that bundle. Its 33-suite, 1,021,651-check record and 17 successful consumer records belong to `2139f3dc`, with the specified parent and ordered patches. They are not relabeled as merge-head executions. The unchanged #22 bytes preserve their applicability to the declaration fix; the new registrar functionality is separately covered above. `receipts/public-evidence-verified.json` records the checksum comparison.

The review assignment reports that the manager's full source static/builder and native banks passed at `d52bd7f2`. That is manager-supplied exact-head evidence, not this reviewer's full-bank execution. The retrieved public issue/PR timelines contain scope and review-start comments, but no additional manager exact-head bank transcripts. The linked bundle remains revision-bound to round 1. No full parent, processor, timing-processor, Yosys or builder bank was rerun here.

Exact-head hosted push run [37423558584](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37423558584) has successful completed docs and portability jobs; their logs explicitly record checkout of `d52bd7f277c6339b13fe7c8ebe849b25f3e14638`. The PR run [37423565146](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37423565146) also reports those jobs successful. Both suite jobs remained in progress at the saved snapshot. Their cached compiler-build step was skipped; that step is not counted as executed validation. No workflow-wide success is inferred. See `receipts/hosted-snapshot.json`, `hosted-docs-gates.log` and `hosted-portability.log`.

After the independent verdict and ledger were frozen, both earlier public reports were read. [R505-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162#issuecomment-6009669777) contains no findings. [R504-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162#issuecomment-6009861919) contains two SUGGESTIONs and no BLOCKER, MAJOR, MINOR or RESIDUE. Submitted-review and inline-comment endpoints are empty. The unchanged affected artifacts retain both suggestions at this head:

- **ID R504-1/S1 — SUGGESTION; attributable lens: RTL.** Path: `hdl/packet_engine/KL_pp_rx_validator.sv:232–233`, with the explanatory V9 block at line 607. Authority/evidence: the earlier public finding and unchanged file identity. The moved wires retain their original spacing and are distant from the FIFO explanation. Impact: readability only; no functional effect. Required outcome: no change required for this PR; optionally add a V9 pointer comment and align spacing in a separate cosmetic change. Verification: repeat all patch/exact-text planting checks and confirm declaration semantics remain unchanged. **Retained.**
- **ID R504-1/S2 — SUGGESTION; attributable lenses: Tests, Docs.** Artifact: `hdl/README.md:48–49`, rule 2, and the parent-owned declaration-order gate. Authority/evidence: the earlier public finding, issue #22's optional gate proposal and the unchanged rule. Impact: future instances of this portability defect may first be rejected at parent adoption. Required outcome: no change required for this PR; optionally document declaration-before-use or add a processor-side analysis gate in a follow-up. Verification: the follow-up's own acceptance should demonstrate a passing clean source and rejection of a planted declaration-order defect. **Retained.**

Neither suggestion changes the positive verdict or leaves a lens unclean. There is no wording-only RESIDUE to transfer.

Real limits and pending manager duties:

- Source validation is distinct from the final current-dev candidate. The source base is `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`; live parent dev is `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`. The manager constructs and validates the final candidate at the merge turn, including its actual staged processor gitlink and consumer bank. This review did not create that candidate.
- The manager owns hosted/local-workflow acceptance, completion of required contexts, two independent positive reviews, integration and publication. In-progress and skipped contexts retain their recorded meanings.
- At parent pin adoption, apply the prescribed adoption patches, measure `Synth 8-6901`, and close #22 only on the required result. Analysis success is not that synthesis measurement.
- Physical calibration is **NOT RUN**. Field skips, simulation and shape guards are not hardware proof. No hardware was accessed.
- Historical statistics equality is not formal equivalence. The exact declaration-move proof establishes the source invariance for #22; imported #134 behavior is intentionally functional mainline content.

All generated source copies, builds, patches and temporary snapshots stayed under this packet's `scratch/`. The clone was never edited. Independent suites and fault work ran concurrently under foreground supervisors, with campaign job limits, `make -j16` and at most 16 compiler workers; per-file analysis began after compiler builds finished. Peak unit memory was 5,736,386,560 bytes under the 12,884,901,888-byte cap, with zero limit/OOM events. No prohibited bank, external write, merge, commit, push, shared installation, privilege change or other-checkout edit was performed.

The final direct integrity check disables object replacement, hashes all 562 tracked disk entries using Git blob framing, verifies modes and the complete stage-zero index, and confirms an empty status including ignored files. HEAD and tree match the required identifiers. There are no submodule gitlinks in this processor checkout. The public parent trees at both `28f9666f` and `423ac5d9` were separately checked: unchanged timing-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, external leaf `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`, and pre-adoption processor `ead8036035affd53ef4b29979190f2f4f67084c0`. These read-only public gitlink checks do not claim a staged merge-turn candidate. See `receipts/final-integrity.json` and `public-parent-gitlinks.json`.

Portable scripts and replay instructions are in `scripts/` and `REPRODUCE.txt`. `MANIFEST.sha256` lists every publishable receipt and script with packet-relative paths. Only those files and this report are for publication; `scratch/` is excluded.

R505-2 FINISHED
