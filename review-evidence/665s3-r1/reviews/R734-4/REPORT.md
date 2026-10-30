[R734] POSITIVE - exact head ac105b158bb740a65e0154305377fd4a7d0f6f87

External independent review R734-4 of PR #811, issue #665, platform slice S3.
Tree: `10a286051e8aa59003bfac98cf4f7d5973d241f9`.
Reviewed delta: `99de3a023abfda5604a70832e23baf7ff73481a3..ac105b158bb740a65e0154305377fd4a7d0f6f87`, with the whole PR against `f4c9ad4f` where needed to establish dependencies.

This verdict and the ledger below were written before opening either permitted prior-review comment. No other review body or review-directory file was consulted. PR metadata was fetched only through the expressly permitted JSON command. Public scope decisions, source, author gate receipts and independently executed probes supplied this pass.

No new BLOCKER, MAJOR or MINOR was found. This approves the reviewed source within the frozen platform scope; it does not discharge the manager's merge-candidate or release duties.

Authority and scope

- `AGENTS.md` section 6; `CONTRIBUTING.md` sections 2, 3 and 6; `docs/README.md` authority ordering.
- Issue #665 body and public decisions [6409738976](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976), [6493622258](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258), and [6505997821](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6505997821).
- `REQUIREMENTS.md` section 1 and REQ-CSR-02; `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 2, Milan v1.2 5.6.1 readiness ordering; `sw/firmware/ctrl_nvm/README.md` Boot and Write-back; `docs/reference/FR_NFR.md` section 3.4.1 and the project service bound; issue #397's tick rule as cited by the platform contract.
- The public ruling permits the named 8x8 two-interface platform image at 59.0 planned RAMB36, defers live SRP reconfiguration and the split grader modes, and leaves the boot as a standalone recipe. These are recorded scope decisions, not silently relaxed tests.

Independent results

[R734] PASS Conformance - `sw/firmware/ctrl/plat/ctrl_plat.c:226`, `sw/firmware/ctrl/app/ctrl_app.c:87`, `sw/firmware/ctrl/test/test_plat_boot.cpp:208` - The retained boot composition restores before opening, releases AECP at its accepted terminal and starts ADP last. The new B1 media stamps observe flash reads before any mailbox access. B10 sends a controller bind through the mailbox and observes both a successful commit and flash programming through ordinary loop service. These support the saved-state and readiness contracts; the matching two plants fail their own assertions. The delta does not change protocol ownership or wire behavior. The console bound preserves exact command recognition.

[R734] PASS RTL - `tb/verilator/ctrl_split_boot/boot_soc.py:65`, `tb/verilator/ctrl_split_boot/sim_main.cpp:206`, `sw/litex/ctrl_memory.py:211`, `sw/firmware/ctrl/plat/ctrl_plat_console.c:132` - No HDL or gitlink changes occur in the PR. The delta changes no SoC wiring, clock/reset generation, mailbox crossing or memory exception predicate. The sole executable firmware change adds a literal-terminator guard; its short-circuit order prevents an out-of-range command read. The simulation still uses the product split CPU at 50 MHz and bus at 100 MHz, acknowledged test faces and a stand-in CSR window. Published image receipts account for the added eight ROM bytes at every point with unchanged planned tile totals.

[R734] PASS Robustness - `sw/firmware/ctrl/plat/ctrl_plat_console.c:132`, `sw/firmware/ctrl/test/test_plat.cpp:151`, `tb/verilator/ctrl_split_boot/run.py:248` - Embedded NUL, prefix, suffix, overflow, FIFO-full and sliced console behavior remain checked. The native gate rejects nonzero exit, failed tally, absent tally and missing saved status; regrade reads the same persisted status. Native failure cannot be masked by earlier valid observations. Existing refused-boot tests run at one and two interfaces. Independent baseline tests pass and the unsafe compare, delayed restore and omitted store-service plants are all killed.

[R734] PASS Tests - `sw/firmware/ctrl/test/plat_arms.py:39`, `sw/firmware/ctrl/test/plat_mutants.py:94`, `sw/firmware/ctrl/test/test_plat_boot.cpp:378`, `tb/verilator/ctrl_split_boot/run.py:350` - The console compiles and links with the sanitizer and abort-on-error setting, and its revert fails K3 with the actual out-of-bounds diagnostic. B1 and B10 each kill their causal boot defect. Normal-path and regrade controls exercise the driver through a stand-in executable, not just an isolated predicate. The self-test additionally requires native completion, preventing a timeout from masquerading as a successful mutation kill. Author exact-head receipts show both simulation plants killed in completed runs. Independent execution: 10 console/CSR + 2 MMIO + 10 single-interface boot + 10 two-interface boot tests pass, 3/3 named plants caught, 6/6 native controls meet run and regrade expectations.

[R734] PASS Docs - `sw/firmware/ctrl/plat/README.md:97`, `tb/verilator/ctrl_split_boot/README.md:56`, `docs/design/SPLIT_CONTROL_MEMORY.md:214`, public author receipts at `06c6f5d97328e8c4c684314df156d02637224341:review-evidence/665s3-r1/author-r3/receipts/` - Native verdict and regrade behavior, sanitizer coverage, ordered restore observation and write-back tests match the code. The memory table matches the published image receipts, including the restricted 59.0-tile exception. Timing tables explicitly state CPU 50 MHz and bus 100 MHz. Stand-in observations, blank flash, missing datapath, deferred work and simulated UART limitations are disclosed. Source-comment cleanup in the reviewed delta introduces no new bench-lane or reviewer label.

Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat.c:226`; `ctrl_app.c:87`; `test_plat_boot.cpp:208,378`; public scope rulings | R734-4 | ac105b158bb740a65e0154305377fd4a7d0f6f87 |
| RTL | CLEAN | Whole-PR changed-path inventory; `boot_soc.py:65`; `sim_main.cpp:206`; `ctrl_memory.py:211`; image receipts | R734-4 | ac105b158bb740a65e0154305377fd4a7d0f6f87 |
| Robustness | CLEAN | `ctrl_plat_console.c:132`; `test_plat.cpp:151`; `run.py:248,335`; independent baselines and plants | R734-4 | ac105b158bb740a65e0154305377fd4a7d0f6f87 |
| Tests | CLEAN | `plat_arms.py:39`; `plat_mutants.py:94,163`; B1/B10; `run.py:350,397,414`; focused raw receipts | R734-4 | ac105b158bb740a65e0154305377fd4a7d0f6f87 |
| Docs | CLEAN | Platform and boot READMEs; memory section 5; published manifest and exact-head author gate receipts | R734-4 | ac105b158bb740a65e0154305377fd4a7d0f6f87 |

Reproduction and evidence

Run from the isolated clone, with all disposable files under the packet's `scratch/`:

```sh
python3 -B "$PACKET/verify_evidence.py" . "$PACKET"
python3 -B "$PACKET/focused_probes.py" . "$PACKET"
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$PACKET/scratch/native-controls" --native-controls
python3 -B "$PACKET/verify_checkout.py" .
```

The focused script runs independent host arms concurrently, at most three builds of four compiler jobs each. It never edits source in the checkout. All four commands succeeded. `focused-probes.log`, per-arm logs and return codes (path-prefix substitutions declared in RECEIPTS.txt), `native-controls.log`, `evidence-verification.log` and `checkout-integrity.log` are the reproducible receipts.

All 194 public author-r3 receipt hashes match `MANIFEST.json` at the pinned evidence commit. Only author receipts were retrieved; no `reviews/` directory was opened. The archive commit has no embedded signature. This verifies content hashes against the published manifest, not cryptographic signer authentication. Public author receipts are source-head evidence, not manager source-bank results.

Published exact-head spot checks: both boot grades and regrades pass with native status zero and a nonzero completed tally; both simulation plants complete and fail the intended oracle; four firmware shards pass; memory figures and refusals match the named exception; coverage remains complete for the changed console. The builder receipt explicitly retains gate 11 NOT RUN. Large archived logs were inspected by relevant sections, not treated as independent executions.

At CPU 50 MHz and bus 100 MHz, the published simulated boots are 84.383 ms (1x1) and 184.647 ms (8x8, one interface). The documented planned platform tiles are 39.0 / 42.0 / 52.0 / 59.0. These are neither mapped hardware utilization nor physical timing proof.

Limits and pending manager duties

- No full source banks, hardware work, hosted acceptance, local workflow replica, route or merge-candidate run was performed by this review. No manager source bank exists at this source head, and none is inferred.
- Physical calibration: NOT RUN. Field skips, stand-in CSR values and simulated UART traffic provide no hardware proof.
- The product faces remain a later integration step. The simulated flash is blank; valid/torn/wrong-version target restore remains separate work. The reviewed scope also retains the public SRP, grader and memory-budget exceptions.
- The CPU-budget measurement still reports misses at CPU 50 MHz and bus 100 MHz: 13/81 paths at 1x1 and 30/129 at 8x8. This review makes no service-budget closure claim; those existing misses belong to the separately assigned remediation.
- The manager must validate the merge candidate against then-current development, publish builder/native receipts, establish hosted/act acceptance distinguishing execution from skips, confirm independent review completion, and perform authorized merge and containment. Source base `f4c9ad4f` differs from the supplied live development tip `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- Integrity was checked against raw tracked blob bytes, executable modes, stage-zero index records and initialized submodule pins. `external` is uninitialized and unused by these focused probes; its index gitlink remains exact. The required processor, lwSRP and stack pins and their tracked contents match.

Prior findings reconciliation

The following two review bodies were fetched only after the independent verdict and all five ledger rows were written and hashed: [R734-1](https://github.com/kebag-logic/milan-fpga/pull/811#issuecomment-6508854695) and [R733-1](https://github.com/kebag-logic/milan-fpga/pull/811#issuecomment-6508864388). No other reviewer report was opened. The manager's [round-3 instruction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508869822) confirms the same three required fixes and comment cleanup. This reconciliation does not change the independently written positive verdict or ledger.

| Prior ID | Severity and attributable lenses | Disposition at this head | Evidence |
|---|---|---|---|
| R734-1-F1 | MAJOR; Conformance, Robustness, Tests | RESOLVED | `run.py:248,335,350` combines persisted native return status with a nonempty successful tally. Six native controls pass their expected normal/regrade outcomes in this review. Public exact-head receipts show both positive boot points, matching regrades, and both completed simulation plants. |
| R733-1-F1 | MINOR; RTL, Robustness, Tests | RESOLVED | `ctrl_plat_console.c:135` stops at the command terminator. K3 and the sanitized baseline pass. Reverting that condition produces the actual global-buffer-overflow and the named K3 failure; `plat-command-read-past-its-end.log`. |
| R733-1-F2 | MINOR; Tests | RESOLVED | `test_plat_boot.cpp:208,378` observes media-before-mailbox order and bind-to-flash write-back through the loop. The two named plants fail B1/B10 in independent execution; both baseline interface counts pass. |
| R734-1-R1 / R733-1-R1 comment subset | RESIDUE; Docs | RESOLVED within the owner comment rule | `18fa9a45` removes the listed new S3/S2/S14 and comment/ruling identifiers from source comments/docstrings. Runtime ledger explanation strings at `ctrl_memory.py:214,218` remain unchanged: they are diagnostics, not comments, and R734-1 expressly excluded executable strings. Older comments remain under #746. |
| R734-1-R2 / R733-1-R2 | RESIDUE; Docs | RESOLVED | `ctrl_split_boot/README.md:101` drops the inaccurate comparative phrase, retaining the wire-serialization figure and simulation limits. |
| R733-1-R3 | RESIDUE; Docs | RESOLVED for measured timing claims | Current PR Status, Simulation and CPU-budget-limit descriptions identify product CPU 50 MHz and bus 100 MHz. Timing tables carry the same clocks. |
| R733-1-R5 | RESIDUE; Docs | RESOLVED | The current PR row for `c787a3ce` identifies all six unchanged files whose counts were re-recorded and states that coverage remains 100% before and after. |
| R733-1-R4 | RESIDUE; Docs | RETAINED below | The unchanged allocation comment still omits its interface-0 qualification. |
| R733-1-S1 / S2 / S3 | SUGGESTION; lenses below | RETAINED, optional | Existing suggestions remain useful; the reviewed delta does not change their causes. |

R733-1-R4 - RESIDUE - Docs

Artifact: `sw/firmware/ctrl/plat/ctrl_plat.c:64`.
Authority/evidence: the comment says no source reports an address the window does not hold; `window_write()` and the documented port contract provide a window only for interface 0. B8 explicitly covers the other interface.
Impact: overly broad explanatory wording only. It changes no measurement, verdict, test, implementation, generated artifact or compliance claim.
Exact required wording: replace the comment with "the window first, then the allocation ACMP's source port reports, so no interface-0 source reports an address the window does not hold; interface 1 has no window (ctrl_plat.h)".
Verification: compare the comment with `window_write()`, `allocation()` and B8. No code change is requested. Docs remains CLEAN.

R733-1-S1 - SUGGESTION - Robustness, Tests

Artifacts: `sw/firmware/ctrl/test/test_plat.cpp` console formatting tests and `sw/firmware/ctrl/plat/ctrl_plat_console.h` response capacity.
Authority/evidence: the prior independent width probe measured the widest response at 309 bytes against the correct 320-byte reservation; reducing the reservation to 200 escaped its tests. Formatting and capacity are unchanged in the reviewed delta.
Impact: an optional additional guard against a future reservation regression; no current overflow was demonstrated.
Suggested outcome: assert the widest formatted response fits `CTRL_PLAT_RESPONSE_MAX`.
Verification: the positive maximum-width response passes and a reservation below that response fails.

R733-1-S2 - SUGGESTION - RTL, Tests

Artifact: `sw/firmware/ctrl/plat/ctrl_plat_csr.h:77`, snapshot wait.
Authority/evidence: REQ-CSR-02 and the documented snapshot contract require coherent publication. The existing host/simulation snapshot is immediate, so the prior zero-spin plant was unobservable. This wait is unchanged.
Impact: model evidence does not calibrate a physical snapshot wait.
Suggested outcome: retain this hardware-validation obligation with the integration/bench work.
Verification: a physical or latency-faithful observation establishes the required snapshot settling behavior. No physical test was run here.

R733-1-S3 - SUGGESTION - Conformance, RTL, Docs

Artifacts: `sw/firmware/ctrl/plat/ctrl_plat_csr.c:47`, `ctrl_plat.c:174`, `sw/firmware/ctrl/plat/README.md` boot step 3.
Authority/evidence: frozen acceptance requires the fifteen writes to equal `configure_fabric()`. That policy can enable the fabric allocator before the subsequent one-owner report clears it. The prior review identified the immediate PROBE-on-enable behavior in `hdl/ieee1722/maap/KL_maap.sv:24`; the relevant policy and allocator dependencies are untouched here.
Impact: an integration consideration explicitly classified as optional under the frozen acceptance, not a new defect established by this delta.
Suggested outcome: document the transient enable and obtain the placement/bench decision on clearing it in a future split-specific policy.
Verification: the eventual real-datapath integration observes startup traffic and checks the approved ownership policy.

The manager should carry retained R4 and S1-S3 together. No blocking finding was moved to another issue, and no MINOR/MAJOR/BLOCKER remains open in this ledger.


Publication: MANIFEST.sha256 enumerates every publishable receipt and portable script. Only those entries and this report are intended for publication; scratch/ and unlisted input snapshots are excluded. Selected source receipts are copied byte-for-byte under published-author-receipts/. The independent pre-reconciliation verdict hash is in isolation-receipt.txt.

R734-4 FINISHED
