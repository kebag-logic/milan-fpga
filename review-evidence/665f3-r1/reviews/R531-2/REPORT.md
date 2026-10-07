[R531] NEGATIVE - exact head 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8

R531-2, external independent source review of issue #665 / PR #688. One MAJOR and one MINOR remain open. All five lenses were applied. The accepted area result stands. The queued-send fix works, but the accepted-send timing requirement remains incomplete on the immediate-send path.

Tree: `ff7dc21ef660db87721e80f59c498f925708c04e`. Reconstructed AGENTS/CONTRIBUTING, docs/README, public acceptance and decisions, requirements/interfaces, the `021b9c1f..HEAD` diff and history, and public evidence. Reviewed `351ae81f..HEAD` particularly closely. The independent verdict and ledger were written before consulting the earlier public findings. Those findings were then reconciled individually below. No private lane material or other checkout was inspected.

**R531-2-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | `sw/firmware/ctrl/acmp/acmp.c:663`, `:676`, `:107`, `:1083`; `docs/design/MAILBOX_SPLIT.md:546` | Immediate sends still lose time from TMR_NO_RESP.**

Authority/evidence: Milan v1.2 5.5.3.5.3 steps 5-7 sends the initial probe before starting its 200 ms timer; 5.5.3.5.16 steps 1-2 does the same for its duplicate. The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030067436) expressly requires the interval from the accepted send of each attempt. `send_probe()` computes the deadline before calling `transmit()`. A `SENT` result never replaces it. The clock helper caches its first read for the entire entry; timer dispatch has already sampled it before sending a duplicate.

The independent port in `scripts/independent_timers.cpp` accepts a send after five milliseconds of elapsed work, without calling back into the core. Initial acceptance at 1005 produces deadline 1200, instead of 1205. Duplicate acceptance at 1205 produces deadline 1400, instead of 1405. At 1404, just 199 ms after acceptance, the sink has already entered PRB_W_RETRY and ignores a matching successful response. Both immediate-send tests fail. A queued-send control gets the correct post-acceptance deadline, and a zero-duration control passes. See `receipts/independent-timers.log` and `.rc`.

Impact: a bounded send that crosses the millisecond counter, including work within the stated service allowance, shortens the response window and can incorrectly report LISTENER_TALKER_TIMEOUT. The existing A27 tests advance time between refused attempts but keep time fixed inside successful sends. The design and API claim accepted-send timing for both paths, which the current behavior does not provide. This also affects firmware architecture under the RTL lens, irrespective of the mailbox RTL's successful checks.

Required outcome: anchor the response interval to acceptance of each initial or duplicate probe, including immediate success and dispatch with an already-cached clock. Preserve FIFO order, sequence ID, one duplicate, cancellation/rebind handling and the explicit lost-probe recovery policy. Recheck any affected access-cost figures.

Verification: the four supplied tests must pass, with a response accepted at 199 ms and timeout only at the full interval; retain the existing queued, cancelled, rebound and wrap cases. This retains R531-1-F2's required outcome, with its original queued-send reproducer now fixed.

**R531-2-F2 | MINOR | Conformance, Tests, Docs | issue #665 comment `6030870481`; `sw/firmware/ctrl/test/ctrl_arms.py:254`; published `author-r3/HANDOFF.md` and PR #688 body | Required linked firmware footprint is absent.**

Authority/evidence: the [public acceptance addition](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), made before this head, requires each F-lane's linked composed `ctrl_app` image: text, rodata, data, bss and entity-sized static pools, for the shipping and largest supported shapes, with a delta from its base. The published packet reports RV32 object totals, including 25,888 bytes of text. Its executable arm compiles individual objects and totals their sizes at `ctrl_arms.py:267` and `:283`; it does not link that image. The current PR body explicitly says no image links this firmware yet. The public issue/PR evidence inspected contains no replacement linked-size report. `receipts/public-evidence-audit.json` records the audited archive and PR-body identities.

Impact: the required block-RAM budget comparison remains unproved. Object totals omit the composed static allocation and final link effects; the public acceptance checkbox is premature.

Required outcome: publish reproducible linked-image/map and section/pool measurements for both required shapes at this head or its corrected successor, plus the base comparison. Any change to this acceptance item needs an explicit public disposition.

Verification: independently reproduce the link and reconcile every reported section and pool against its map and shape. This is an acceptance/evidence gap and does not qualify as wording-only residue.

**Prior public findings, resolved or retained at this head**

Consulted PR comments [6029581606](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6029581606) and [6030054402](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6030054402) after the independent pass. Original severity and lens assignments are preserved. Nine targeted regression faults were also replayed; each failed its named assertion (`receipts/native-regression-mutations.json`).

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R531-1-F1, MAJOR, Conformance/RTL/Robustness/Tests: unsupported AVTP versions | Resolved | `acmp.c:985` and `:1033` reject bits 6:4 before decode. A26 covers commands/responses and AVAILABLE/DEPARTING; B9 exercises the adapter. Removing the command check fails its named assertion. IEEE 1722-2016 4.4.3.4 and 1722.1-2021 6.2.2.3/8.2.1.3 checked. |
| R531-1-F2, MAJOR, Conformance/RTL/Robustness/Tests: send-origin timeout | Partially fixed; retained through R531-2-F1 | `timer_held`, `probe_of`, `probe_left()` and A27 fix owed initial/duplicate attempts, rebind, cancel and success while owed. Removing the hold is detected. Immediate success still uses the earlier timestamp, demonstrated independently. |
| R531-1-F3, MINOR, Conformance/RTL/Robustness/Tests: slot overflow | Resolved | `acmp_mbx.c:71` compares against `MBX_N_TIMERS - MBX_N_IF` before narrowing. B7 covers last legal, first illegal, UINT_MAX and narrowing values. Reintroducing addition is caught. |
| R531-1-F4, MINOR, Docs: owed-frame arithmetic | Resolved | `MAILBOX_SPLIT.md:666` correctly puts 8,964 accesses at 8.964 ms for 1 us/access, excluding waiting for room. The full acmp/adp ring figures still exceed 10 ms under that assumption. |
| R531-1-F5, MINOR, Docs: poll interface | Resolved | `acmp.h:424` specifies at most one owed frame per call, consistent with `acmp_poll()`, A19, E2 and the per-pass bound. |
| R530-1-F1, MINOR, Tests/Robustness: two-interface adapter | Resolved | `ctrl_arms.py:62` builds `acmpif2` against the generated two-interface contract. All 19 tests pass, including B3/B4/B6 and the C paths. The shared-slot fault fails B3 on interface 1. |
| R530-1-F2, MINOR, Tests: BINDING layout/length | Resolved | A24 pins flags 0x01, 0x03 and 0x05 and complete payload bytes against the processor layout; overlength records are refused. Symmetric flag exchange and the long-record acceptance fault are both caught. |
| R530-1-F3, MINOR, Tests: D3 rollback | Resolved | `test_acmp_nvm.cpp:250` N7 preserves a live applied binding through the port and a real store boot with a D3 settle fault. The binding-dropping fault fails N7. |
| R530-1-F4, MINOR, Tests/Robustness: millisecond wrap | Resolved | A28 crosses 2^32 for NO_RESP, RETRY, NO_TK, DELAY and NO_ADP and checks earliest deadline ordering. Unsigned due/earliest faults both fail named A28 tests. |
| R530-1-F5, MINOR, Conformance/Docs: TD1 authority/evidence | Resolved | `MAILBOX_SPLIT.md:681`, `acmp.h:59`, `acmp_walk.cpp`, current PR body and processor #168 distinguish LD1-LD3's executed comparison from TD1's source reading. The 5.5.2.7 overview defers to the detailed 5.5.4.2 procedure; Table 5.44 assigns TALKER_UNKNOWN_ID. Verified the processor's unconditional SUCCESS at `KL_acmp_talker.sv:1301`. |
| R530-1-R1, RESIDUE, Docs: undecided adp term | Resolved | The current discovery/filter description, ctrl README and PR body name decision 6029368753 and the implemented bound-talker term. Historical round-1 text in the archive remains historical evidence. |

**Applied lenses and executable evidence**

Conformance: examined the listener/talker/discovery implementations in `acmp.c`, public port contracts and `acmp_walk.cpp` against Milan 5.5.3, 5.5.4 and 5.6.4/Table 5.54, IEEE 1722.1 wire fields and the frozen lane decisions. Checked response routing by listener unique ID and saved probe tuple, duplicate sequence preservation, lock/error answers, repeated commands, valid_time aging, available_index restart, GM/domain and interface guards, and response-before-notification ordering. The 127-case processor walk passes; it reuses the pinned test models/constants, with TD1 explicitly source-read. F1 and F2 above prevent clean coverage.

RTL/architecture: traced `mailbox.yaml` contract 2.1 through `mailbox_model.py`, `mailbox_emit.py`, `mailbox_skeleton.py`, generated `KL_mbx_pkg.sv`/`KL_mbx.sv`, `KL_mbx_rx.sv`, the host model, `mbx_filter_set_bound_talker()`, `acmp_mbx.c` and `ctrl_app_open()`. The third adp term admits only message types 0/1 against enabled entries of the receiving interface. The copier reads the low/high words in byte order, masks words unwritten since reset, restarts on rewrites, and suppresses a match while an entry is disabled or copying. Match flags are reseeded at byte 18 and accumulate through byte 25. The completed-field guard rejects truncation. Bus strobes, reset/readback and invalid entries are covered on both adapters. No new clock crossing is introduced. Firmware's timer architecture retains F1.

Robustness: reviewed malformed versions/lengths, slot boundaries, last table entry, per-interface isolation, stale match flags, reset, byte-stream stalls, enabled-entry rewrites, concurrent reads/copies, stale timer tags, owed frames, cancellation/rebind, clock wrap, BINDING restore and D3 rollback. Q12-Q21 exercise the table and copier. Four independently selected faults (wrong half of the byte index, previous-frame first-byte match retained, last entry excluded, opposite-interface lookup) all fail on both adapters: eight detected runs. F1 remains open.

Tests: independently executed the following at the exact source head, using disposable builds under `scratch/`. Drivers waited for every child; no work was detached. At most two simulator builds ran together, each limited to four compile jobs; native compilation also used explicit four-job bounds. No whole-repository bank was run.

| Run | Result | Receipt |
|---|---|---|
| Native model, ACMP, two-interface adapter, processor walk, real-store binding integration | 23 + 78 + 19 + 127 + 7 = 254 tests, zero failures | `receipts/native.log` |
| Mailbox through Wishbone / AXI4-Lite | 380 / 425 checks, zero failures | `receipts/run-wb.log`, `run-axil.log` |
| Two-interface mailbox through both adapters and host model | 380 / 425 / 369 checks, zero failures | `receipts/run-if2.log` |
| Firmware/RTL co-simulation | 32 checks, 14 identical frames | `receipts/run-cosim.log` |
| Contract consistency and generator self-test | Both exit 0; 46 self-test arms | `receipts/generator-check.log`, `generator-selftest.log` |
| Four independent table faults, each adapter | 8/8 detected | `receipts/rtl-mutations.json`, corresponding `mutation-*.log` |
| Nine targeted round-1 regression faults | 9/9 detected by named assertions | `receipts/native-regression-mutations.json`, corresponding `regression-*.log` |
| Firmware-only relink fault, then restored source | Changed binary fails; restored binary changes again and passes 32 checks | `receipts/relink.json`, `relink-mutated.log`, `relink-restored.log` |
| Independent accepted-send timing | Two immediate-send failures; deferred and zero-duration controls pass | `receipts/independent-timers.log` |

The relink probe changes only the disposable firmware copy after the co-simulation is already built. It proves `run-cosim` picks up firmware changes without cleaning. H-DISC C10/C11/F5 now enters through the model filter's `RX_HEAD`, including both interfaces and the full adp-ring backlog. The RTL co-simulation also receives the bound talker's announcement and rejects a foreign talker. Those measurements remain mailbox-access counts, conditional on physical calibration. The new timing tests show why passing stock tests and the published coverage ratchet do not complete F1. Coverage and full mutation campaigns were not rerun in this review.

Docs: checked `MAILBOX_SPLIT.md`, generated `MAILBOX_CONTRACT.md`, the ctrl/ctrl_nvm/gtest/mailbox READMEs, API headers, published handoff and PR body against source and executed results. The TD1 ruling and decided term are recorded. The accepted-send claim is still broader than behavior (F1), and linked-size acceptance lacks its required evidence (F2). No new RESIDUE finding is recorded.

**Area and scope**

Checked the [published round-3 record](https://github.com/kebag-logic/milan-fpga/blob/203843a3a4e68d53040970f6d3c71cd7ab677cc5/review-evidence/665f3-r1/author-r3/HANDOFF.md) against [the manager's acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6033962557). Its recipe is `tb_mbx_top`, HOST_P=0, `xc7a100tfgg484-2`, 10 ns, placed and routed under the shared lock. FC round 2's 2,745 LUT / 2,860 FF versus this head's 3,102 / 2,946 gives exactly +357 / +86; recorded WNS is +0.402 ns, with all 6,041 nets routed, unchanged block RAM and no DSP. The record identifies 128 SRL16E plus the read-back memory, consistent with the inspected distributed-memory implementation. The measured source digest prefixes match the exact-head files. The 57-LUT target excess is explicitly accepted. See `receipts/public-evidence-audit.json`. The raw utilization report is described as retained in scratch and is absent from the published archive; this review verifies the published measurement record, without independently rerunning physical implementation.

`08130eca45b39d8d791ed8447b41f573dd70886d` has ordered parents `351ae81f` and `db9aa8c9`; `b03929fc123fc2d5e261e69fb2f0f39b87eee95b` then merges `910f338d`. Both requested two-parent merges are present. No source under `sw/litex`, `configs`, `sw/builder` or `sw/firmware/milan_baremetal` differs from the initial FC base. `milan_soc.py:2590` still defaults `ctrl_mailbox=False`, and `:3295` adds its sources only when enabled. F3's RTL changes are confined to three mailbox files. The full FC-to-head diff also contains the AAF change inherited from dev; outside-mailbox RTL is byte-identical to integrated dev `910f338d`. Thus the unchanged-default/shipping claim applies to F3, with that inherited change accounted for. No image was generated in this review. Scope/parent receipts are in `receipts/scope-history.json`.

**Reviewer-owned completion ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | Milan/IEEE clauses; `acmp.c:663`; `mailbox.yaml`; issue acceptance 6030870481; public evidence audit | R531-2 applied; no clean covering round | 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8 |
| RTL | UNCLEAN: F1 | `acmp.c:107,663,1083`; generated mailbox/core RTL and adapters; generator; co-simulation and eight RTL fault runs | R531-2 applied; no clean covering round | 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8 |
| Robustness | UNCLEAN: F1 | A24/A26-A29, B3/B7/B9, N7, Q12-Q21; independent accepted-send probes; table and regression faults | R531-2 applied; no clean covering round | 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8 |
| Tests | UNCLEAN: F1, F2 | `ctrl_arms.py:254`; stock native/simulation receipts; independent timing and sensitivity probes; missing linked-image evidence | R531-2 applied; no clean covering round | 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8 |
| Docs | UNCLEAN: F1, F2 | `MAILBOX_SPLIT.md:546`; API headers; generated contract; READMEs; exact-head public handoff and PR body | R531-2 applied; no clean covering round | 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8 |

**Reproduction, limits and remaining manager duties**

With the checkout, packet, pinned simulator and native test dependencies available, run the portable scripts below. Set `REVIEW_VERILATOR` to the scoped 5.050 executable; its identity was checked before use. Fault scripts require `run_checks.py`'s disposable builds. A detected mutation has a nonzero child receipt and a successful campaign result; the independent timing driver itself exits nonzero for the open defect.

```sh
python3 "$PACKET/scripts/run_checks.py" "$CHECKOUT" "$PACKET"
python3 "$PACKET/scripts/rtl_mutations.py" "$PACKET"
python3 "$PACKET/scripts/native_regression_mutations.py" "$CHECKOUT" "$PACKET"
python3 "$PACKET/scripts/relink_probe.py" "$PACKET"
python3 "$PACKET/scripts/run_timer_probes.py" "$CHECKOUT" "$PACKET"
python3 "$PACKET/scripts/verify_tree.py" "$CHECKOUT"
```

The original clone remained unchanged. Final verification reads every tracked blob and mode directly, compares every index record, and proves all three required submodule gitlinks and checkout bytes. It checked 1,163 parent files and 876 submodule files, with no failures and an empty status (`receipts/tree-integrity.json`). Disposable source probes were restored; mutation copies remain confined to unpublished scratch. Receipt logs preserve command output, with only local home/install prefixes redacted; `receipts/path-redactions.json` records original and published hashes, and originals remain in scratch. `MANIFEST.sha256` defines the publication set.

The manager's stated full source static/builder/native evidence is distinct from this focused review and from the later current-dev candidate. Full parent/processor/gPTP/synthesis/builder banks, full firmware coverage/campaigns, hosted execution, local container replication and hardware were not run here. A read-only exact-head hosted query returned zero check runs and zero workflow runs; no executed or skipped hosted context is claimed. Hosted/local acceptance remains manager-owned.

Physical calibration: NOT RUN. Field skips are not hardware proof. The access-time assumption, service budget under full backlog, H-ACMP wire round trip and physical bench acceptance remain pending. The physical area record supplies no firmware timing calibration.

The manager must carry F1 and F2 to correction/evidence and independent re-review, preserve the resolved round-1 checks, and obtain the complete review and gate bar. Integrating live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` is a later round, as assigned; its absence here is not a finding. The manager owns final candidate construction and gates, executed hosted/local evidence, authorized merge and post-merge containment. Processor #168 remains separately tracked; the reviewed lane changes no processor gitlink. This verdict supplies no merge authorization.

R531-2 FINISHED
