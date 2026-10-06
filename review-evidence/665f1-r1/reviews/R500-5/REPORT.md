[R500] POSITIVE - exact head fa1294279c42f181b6f43c6e6bd812039798705c

Round R500-5, composition acceptance for issue #665 / PR #669. Tree: `610669663833b6aad15ef9cb3e5b312c929c6994`. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR is introduced by the composition. One wording-only RESIDUE is recorded below.

The source remains covered by [R500-4](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-6000481093) and [R501-4](https://github.com/kebag-logic/milan-fpga/pull/669#issuecomment-6000397405), both POSITIVE at `d763fce6f3e48fa9c468aaa835653befb8382d06`. This verdict means that combining the reviewed sources introduces no additional functional defect. It does not extend their hardware claims.

Reconstruction used the operating contract, CONTRIBUTING, documentation index, [frozen F1 scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5993775541), public scope decisions, requirements and saved-state/interface authorities, then the requested diff and history. The [later testing-framework direction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385) explicitly allows F0/F1 to merge before that separate lane. `independent-pass.md` records my own verdict and ledger before any prior review report was consulted. Public findings were reconciled afterwards; `public-review-state.json` identifies all eight reports, with zero submitted reviews and zero inline comments. No private author material was consulted.

**Composition evidence**

`composition.json`, `composition-history.log`, `candidate.diff` and `index-composition.diff` establish:

- Ordered parents: F0 candidate `9e05246c5455b2a1df26038345709437e13c6f18`, then F1 source `d763fce6f3e48fa9c468aaa835653befb8382d06`.
- The first parent's tree equals supplied live dev `a1e9839e909c2e44fd47307588fbf9da8c28fd53`.
- Common ancestor: `28f9666feab2b2ba287643c63ed3a16b1e0bb863`. F0 changes 88 paths; F1 changes 30. Their intersection is exactly `{docs/README.md}`.
- All 29 F1-only paths retain the reviewed source's exact mode, kind and object ID. All 87 F0-only paths retain the predecessor's exact entries. All remaining paths equal the common ancestor.
- `docs/README.md:73` keeps the F1 entry beside the other saved-state entries. Line 76 keeps the F0 mailbox entry before Verification. Each occurs once in the Architecture and integration table, with a valid relative link. Removing either added row reproduces the other parent's entire index byte-for-byte, preserving both parents' ordering.

`dependencies.json` checks semantic interaction. F1 adds no production registration, workflow edit, mailbox hook, RTL or gitlink. Its flash/state interfaces remain separate from F0's mailbox interface. The shipping firmware, builder, configurations, shared NVM codecs/shape derivation, recorded vectors, capture receipt and workflow files are unchanged from the reviewed F1 source. F0 changes the SoC, but its reserved flash-map expression and NVM-constant-emission suffix are unchanged. The mailbox remains default-off; no production build or F0 loop links this store. Event-loop timing, timer ownership and state-owner integration remain future obligations, not a new composed runtime path.

F0's CI classification, module inventories and generated documentation share global readers with F1's added files. Those readers were checked on the candidate, including workflow contracts and record pins.

**Reviewer-owned coverage ledger**

S = `d763fce6f3e48fa9c468aaa835653befb8382d06`; C = `fa1294279c42f181b6f43c6e6bd812039798705c`. Untouched implementation scopes retain both named source reviews; shared documentation and gate scopes are covered anew.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition does not change F1's normative scope: REQUIREMENTS.md:21; frozen F1 assignment; SAVED_STATE_FASTCONNECT.md:763; nvm_flash.h, nvm_state.h; unchanged source identities/generators in composition.json and dependencies.json | R500-4 and R501-4 cover source; R500-5 checks composition boundary | S for source; C for boundary |
| RTL | CLEAN | Composition does not touch F1 implementation or introduce a shared runtime: candidate.diff; sw/litex/milan_soc.py:2475 and :3298; ctrl/mbx/mbx_hal.h; ctrl_nvm/nvm_flash.h; source lists, flash map, NVM constants and gitlinks in dependencies.json | R500-4 and R501-4 cover source; R500-5 checks composition boundary | S for source; C for boundary |
| Robustness | CLEAN | Restore/write/error behavior untouched: ctrl_nvm/nvm_store.c and plat/nvm_flash_litespi.c exact blobs; no ctrl_nvm invocation from ctrl/loop/ctrl_loop.c or production build; unchanged configurations and fault tests | R500-4 and R501-4 cover source; R500-5 checks composition boundary | S for source; C for boundary |
| Tests | CLEAN | Composition touches shared discovery/inventory readers: scripts/ci_scope.py, scripts/ci_events.py, gen_module_matrix.py; ctrl_nvm/test/nvm_bench.py dependencies; gate-results.json and record/capture/mailbox receipts | R500-5 covers shared gates; R500-4 and R501-4 cover unchanged source tests | C for shared gates; S for source tests |
| Docs | CLEAN | Composition touches docs/README.md:73 and :76; both target pages and row order; docs.log, toc.log, anchors.log, em-dash.log, doc-paths.log, submodule-docs.log; wording residue below | R500-5 covers composition; R500-4 and R501-4 cover unchanged source content | C for composition; S for source content |

**Executed checks**

All commands below completed with exit 0 on C. `run_gates.py` retains separate raw `.log` and `.rc` files and command results in `gate-results.json`. Its foreground coordinator joined at most four concurrent checks.

| Command | Result / receipt |
|---|---|
| `python3 scripts/docs_check.py` | Zero findings: 195 Markdown files, 1,081 text files; 23 scrub and 4 routing controls; docs.log |
| `python3 scripts/gen_toc.py --check` | 135 annotated contents lists; toc.log |
| `python3 scripts/gen_toc.py --verify-anchors` | 343 cross-page fragment links reproduced; anchors.log |
| `python3 scripts/check_em_dash.py --base 9e05246c5455b2a1df26038345709437e13c6f18` | Zero findings across 468 added lines/3 pages; 339 controls; em-dash.log |
| `python3 scripts/check_doc_paths.py` | 924 cited paths resolve; 10 line anchors valid; doc-paths.log |
| `python3 scripts/check_submodule_docs.py` | Four exact gitlinks; submodule-docs.log |
| `python3 scripts/ci_events.py --check` | 1,655 contract items, four workflows and policy page; ci-events.log |
| `python3 scripts/ci_events.py --selftest` | 2,215 arms pass; ci-events-selftest.log |
| `python3 scripts/ci_scope.py --selftest` | Classification and discovery controls pass; ci-scope-selftest.log |
| `python3 scripts/check_nvm_record_space.py --self-test` | Five configurations, inventories/round trips/refusal controls clean; record-space.log |
| `python3 scripts/check_nvm_capture.py` | Census, clocks, timing arms and stored receipt agree; capture-record.log |
| `python3 docs/traceability/gen_module_matrix.py --check` | 77 modules, zero untested, 5/5 controls; module-matrix.log |
| `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | No output/cross-carrier drift; mailbox-records.log |

`git diff --check` also passed. Initially, TOC, anchor and em-dash checks refused with exit 2 because the pinned Markdown dependency was missing. Their `initial-*` receipts are retained. Installing the hash-locked requirements in a disposable packet-local environment resolved this prerequisite; only affected checks were rerun. No shared installation or candidate edit was made.

The index is intentionally excluded from generated per-page TOCs (`gen_toc.py:72`). Its union, placement, uniqueness and target existence were checked directly by `review_composition.py`, as well as the repository link/path gates. The TOC result alone is not being offered as proof of those rows.

**Finding: R500-5-F1**

- Severity: RESIDUE. All attributable lenses: Docs.
- Artifacts: `sw/firmware/ctrl_nvm/README.md:117` and `:458`.
- Authority/evidence: this candidate contains F0, but both passages still say its HAL or switch is not merged. `composition.json` proves F0 is present; `dependencies.json` separately proves that the store still is not linked into an image.
- Impact: stale merge-status wording only. No measurement, figure, verdict, test, code, generated artifact, privacy rule, conformance claim or clause claim changes.
- Exact outcome: replace the parenthetical, spanning two lines, with ``(`sw/firmware/ctrl/mbx/mbx_hal.h`)``. Replace the limitations bullet's two lines with `- The #665 switch and its link: F0's switch is present, but no image links` followed by `  this store.`
- Verification: both stale status phrases disappear; the interface and unlinked-store statements remain; documentation gates pass. The manager carries this exact fix to the residue checklist. It does not leave Docs unclean.

**Prior public findings at this candidate**

The source reviews' resolutions remain valid because their affected implementation, test and contract artifacts have identical blobs here. This retains independently reviewed resolutions; it does not claim to rerun their firmware probes. Short paths below are under `sw/firmware/ctrl_nvm/` unless qualified.

| Prior IDs | Disposition at C and retained evidence |
|---|---|
| R500-1-F1; R501-1-F3 | RESOLVED: accumulated local timer replaces PHC deadlines; port/time controls unchanged |
| R500-1-F2; R501-1-F2 | RESOLVED: changed work replenishes DR2c; console honors spacing/exhaustion; abandonment retained |
| R500-1-F3 | RESOLVED: current-capture changes leave no stale debounce window; boundary control retained |
| R500-1-F4 | RESOLVED: distinct binding/D3 ownership and rollback; owner-order checks unchanged |
| R500-1-F5 | RESOLVED: verify/blank tails, refusal, tie and time controls remain in nvm_mutants.py |
| R500-1-F6 | RESOLVED: README distinguishes counted work, model time and unmeasured CPU time |
| R501-1-F1 | RESOLVED: validated generation supplies selection metadata; re-stage checks CRC/SEQ |
| R501-1-F4 | RESOLVED: bounded TX/RX/drain waits and fault returns |
| R500-2-F1 | RESOLVED: bindings restore before model proof/D3; unproven-model check retains them |
| R500-2-F2; R501-2-F2 | RESOLVED: whole-call deadline, nominal/cumulative distinctions and progressing-controller checks |
| R500-2-F3 | RESOLVED: fallback re-stage and exact capture-cursor controls |
| R500-2-F4 | RESOLVED: unchanged-projection suppression calls nvm_heal; recovery control retained |
| R501-2-F1; R501-3-F1 | RESOLVED: count/digest/verdict agreement, bounded retry and UNREAD/HELD; nvm_store.c:134-247 and disagreement controls unchanged |
| R501-2-F3 | RESOLVED: public A-on-tie decision, FASTCONNECT:763 and tie control remain aligned |
| R500-3-F1 | RESOLVED: exact fractional conversion and actual per-shape clocks; clock controls unchanged |
| R500-3-R1 | RESOLVED: README:102-109 preserves requested readiness wording |
| R500-2-S1 | RESOLVED: failed fallback reports VD_LEN/UNREAD |
| R500-3-S1, documentation portion | RESOLVED: README:206-209 states the permanent-fault hold |

Remaining suggestions keep their original lenses and optional status:

| ID / severity / lenses | Artifact and evidence | Impact, optional outcome and verification |
|---|---|---|
| R500-1-S1 / SUGGESTION / Tests | .github/workflows; test/test_ctrl_nvm.py; dependencies.json confirms no lane registration | Hosted green alone omits the suite. Retain for the manager; add a named execution and prove a lane defect fails it if adopted. |
| R500-3-S1, policy portion / SUGGESTION / Robustness, Docs | nvm_store.c HELD handling; README:206; decision 2 | Permanent unread media holds persistence across boots. A narrower policy remains an owner decision; verify fault/commit/reboot cases after any authorized change. |
| R500-3-S2 / SUGGESTION / Robustness | nvm_store.h status; nvm_store.c publication; FASTCONNECT 9.2 | Future consumers must map HELD/dirty to public durability flags. Define and test that mapping during integration. |
| R500-4-S1 / SUGGESTION / Tests | test/nvm_rv32.py undefined-symbol filter | Stack-protector symbols pass the helper allowance. Optionally enumerate actual runtime helpers and require a negative symbol check to fail. |
| R500-4-S2 / SUGGESTION / Docs | README:443-449; nvm_store.c agreement search | The fault example says every read; any two matching wrong reads suffice. Optionally broaden the example to any two boot reads, preserving the documented policy. |

**Evidence limits and manager duties**

The specified [public evidence bundle](https://github.com/kebag-logic/milan-fpga/tree/38e93660c8e2d4c190a00e8538611de01fece598/review-evidence/665f1-r1) contains round-1 receipts at `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e`. Selected store, builder and documentation receipt hashes match its manifest (`public-evidence.json`). Its builder result explicitly has one NOT RUN arm. That bundle is historical evidence, not proof of C. The [round-4 evidence comment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6000120843) and source reviews are separately scoped to S.

The assignment reports candidate builder 48/48 and native 5/5 at C. Those banks were not rerun here or substituted with the historical bundle. The manager owns their exact-head receipts and acceptance, plus hosted/local-replica acceptance. No hosted execution was counted in this verdict; no skipped context was treated as an executed job.

Physical calibration NOT RUN. Field skips are not hardware proof. This review adds no CPU service-time, real flash, physical power-cut, placement or timing measurement. No full parent, processor, gPTP, synthesis or builder bank ran. No hardware, container, privileged action, shared install, source fix, commit, push, GitHub write or author contact occurred.

The manager must publish this packet, reconcile independent composition coverage, retain the residue and optional findings, verify the final merge tree against then-current dev, and satisfy the exact-head bank/hosted bar. A changed tree requires renewed affected-lens coverage. Explicit maintainer authorization and completed reviews remain merge prerequisites. Post-merge containment and workflow updates remain manager duties. Issue #665 stays open for its remaining lanes; the shipping writer's codec-parity follow-up and #671 remain separate work.

**Integrity and reproduction**

`checkout-audit.json` proves tracked blob bytes, executable/symlink modes and stage-0 index entries without relying on status to expose hidden edits: 1,105 candidate blobs, 558 processor blobs, 104 gPTP blobs and 214 axis blobs. Required registered checkouts equal these gitlinks:

- `protocol-processor`: `ead8036035affd53ef4b29979190f2f4f67084c0`.
- `gptp-processor`: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
- `third_party/verilog-axis`: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The optional external gitlink/index entry is verified; its checkout remains uninitialized and unused. The candidate is clean. No tracked bytes needed restoration. Disposable environments/data are under packet `scratch/`, excluded from publication. Every started foreground coordinator finished.

Run the portable scripts from the exact candidate checkout, using their packet paths:

```sh
python3 <packet>/review_composition.py
python3 <packet>/audit_dependencies.py
python3 <packet>/run_gates.py
python3 <packet>/audit_checkout.py
```

Use a Python environment with the repository's hash-locked `tools/markdown/requirements.txt` and normal gate prerequisites; create it under `<packet>/scratch/` for isolation. `run_gates.py` accepts gate names for individual reruns. From the packet directory, `sha256sum -c MANIFEST.sha256` verifies publication. The manifest lists every publishable file, including this report; scratch is never listed.

R500-5 FINISHED
