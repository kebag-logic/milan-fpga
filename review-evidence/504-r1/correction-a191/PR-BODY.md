[A191] Hosted builder jobs used to skip the compiler-backed firmware instruments when no supported RV32 compiler was present. Both direct consumers now install and verify the pinned Bootlin SDK, then require the existing absolute selector to adopt it. The deliberately compiler-absent path remains executable and visibly weaker.

Two correction rounds followed the first review. The first answered R228-1: the resolver classifies every store class the adopted ISA emits, and the installer self-test fails on download and receipt faults. The second answers R227-2 and R228-2. A rewritten frame slot is no longer read back stale, each resolver correction has a control that fails when it is removed, and the firmware page claims only what the census observes.

Closes #504

Roles: implementation author A160; correction-round authors A185 and A191; independent reviewers R227 (internal) and R228 (external); manager A10.

## Status and validation

Head `97aa1ec943ac740a27b942210a248f6512ae3ff6`, tree `4a12a545bdb478083d711a8f319d3c6d70c1b1d9`. It descends from live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2` through merge `4914eea5faac2e4816c38455584f259263ad8c20`. The merge is clean: its tree equals `git merge-tree` of the reviewed head `5081a25a` and dev. The author's focused gates pass at the head. The receipts, scripts and handoff are in the author packet. The manager holds these remaining items: the full native banks, trusted act, the hosted required contexts, both re-reviews, current-dev candidate validation and containment.

## Description

The SDK installer authenticates the fixed archive digest before extraction and relocation. It verifies cache provenance and the installed-file inventory before executing cached tools, and it records the compiler's identity. Cache keys bind the archive, the host and the installer contract. Workflow pins and controls track both installation steps and the required-compiler calls. Exact, file-pinned host SDK metadata allowances keep the bare-metal scope gate in force everywhere else.

First correction round (R228-1):

- Stores are classified by instruction class: integer, FP, and RV32A AMO and SC.
- Each store is judged at every 32-bit word it writes, and an unknown memory-writing mnemonic fails closed.
- The installer self-test drives the hosted download path and pins the receipt bindings.

Second correction round (R227-2, R228-2):

- **R227-2-F1.** A frame slot now keeps a value only after `sw` or `amoswap.w`, which is the rule the static branch already applied; both models now take it from one function. A store through a stack address makes every frame slot unknown. Four compiled mutants passed the whole gate before this and are now refused as the unplaced store in `configure_fabric()`: a union byte overwrite and a union half-word overwrite of a parked `ADP_CTRL` address, and an integer and a `float` rewrite of a local through a pointer to it.
- **R227-2-F2 and R228-F4.** Literal-assembly controls, which run on every machine, now cover the ranged-store footprint width, the slot-mirror stop at every store class, the value that non-swap AMOs and SC leave behind, and the symbol-overlap width. Each correction is shown to fail its own control when it is removed.
- **R228-F5.** The firmware page states what the census does not observe: stores inside a called function (`memset` and libatomic calls, and a callee's write into its caller's frame), numeric stores that happen to hit the stack, and sub-word frame-slot loads.

No firmware text refusal, resolver residual, product option, RTL, firmware, processor pin, workflow, installer byte, scheduling rule, ratchet or trusted act boundary changes. #408 and #409 retain text-rule retirement.

## Reproduction

1. Check out the head and initialize `third_party/verilog-axis`, `protocol-processor` and `gptp-processor`.
2. Follow the disposable-prefix installation and compiler-mode commands in `docs/testing/CI_WORKFLOWS.md`.
3. Run `python3 scripts/ci_rv32_sdk_selftest.py` and `python3 sw/builder/test_firmware_compiler.py --selftest`.
4. Run gate 1b twice: once with `--sdk-destination <fresh prefix>` and once with `--absent`.

Do not replace a workstation compiler for local reproduction.

## Definition of Done

- [x] Author focused gates and integrity at the corrected head
- [ ] Complete local source validation at the corrected head
- [ ] Fresh hosted compiler adoption, a hosted cache hit and final-head trusted replica
- [ ] Two independent positive re-reviews and a reviewer-owned all-five clean ledger
- [ ] Current candidate, authorized merge and clean containment
- [ ] Post-merge hosted results and Closed/Done
