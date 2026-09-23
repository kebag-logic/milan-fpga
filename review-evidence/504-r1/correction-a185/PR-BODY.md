[A185] Hosted builder jobs previously skipped the compiler-backed firmware instruments when no supported RV32 compiler was present. Both direct consumers now install and verify the pinned Bootlin SDK, then require the existing absolute selector to adopt it. The deliberately compiler-absent path remains executable and visibly weaker. The correction round answers R228-1: the resolver now classifies every store class the adopted ISA emits, and the installer self-test fails on download and receipt faults.

Closes #504

Roles: implementation author A160, correction-round author A185; independent reviewers R227 (internal) and R228 (external); manager A10.

## Status and validation

Head `5081a25a451b4ac1c00f286ec59ab041c22fdde9` (tree `68a0628be2b55c1180a0e5751d2355cb8f987268`) descends from live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` through merge `f6a55e4c85b6bdcdaeab6caa6b6e575c51cf97df` (clean; its tree equals `git merge-tree` of the reviewed head `3d90958f` and dev). Author focused gates pass at the head; the correction-round receipts, scripts and handoff are in the author packet. Full native banks, trusted act, hosted required contexts including a hosted cache-hit run, both re-reviews, current-dev candidate validation and containment remain with the manager.

## Description

The SDK installer authenticates the fixed archive digest before extraction and relocation, verifies cache provenance and installed-file inventory before executing cached tools, and records compiler identity. Cache keys bind the archive, host and installer contract. Workflow pins and controls track both installation steps and required-compiler calls. Exact file-pinned host SDK metadata allowances preserve the bare-metal scope gate elsewhere.

Correction round (R228-1):

- F1: the adopted SDK compiles the census at `rv32imafd`/ILP32D, which emits `fsw` and `fsd`; the resolver knew only `sw`, `sh` and `sb`. Stores are now classified by instruction class (integer, floating-point, atomic AMO/SC), judged at every 32-bit word they write, and any other memory-addressing mnemonic that is not a recognised load is refused as unclassified. Every store also invalidates the modelled words it overlaps. Literal-assembly controls run on every machine; five compiled mutants (float, double, atomic exchange, fetch-or, compare-exchange) are refused on the resolved address, the atomic three only where the census ISA carries `a`. Docs state the census ISA and the classifier boundary.
- F2: the self-test drives the hosted download path (no `--archive`) with unpinned, truncated, empty and near-pin payloads, each refused before tar or relocation; a positive download-path control proves the branch is taken.
- F3: the self-test pins the provenance field set and installer digest independently, and adds retargeted-symlink and escaping-compiler controls; R228-S1's three unguarded checks gained controls too.

No firmware text refusal, resolver residual, product option, RTL, firmware, processor pin, workflow, installer byte, scheduling rule or trusted act boundary changes. #408/#409 retain text-rule retirement.

## Reproduction

Check out the head and initialize `third_party/verilog-axis`, `protocol-processor` and `gptp-processor`. Follow the disposable-prefix installation and compiler-mode commands in docs/testing/CI_WORKFLOWS.md. Run `python3 scripts/ci_rv32_sdk_selftest.py`, `python3 sw/builder/test_firmware_compiler.py --selftest`, and gate 1b with `--sdk-destination <fresh prefix>` and with `--absent`. Do not replace a workstation compiler for local reproduction.

## Definition of Done

- [x] Author focused gates and integrity at the corrected head
- [ ] Complete local source validation at the corrected head
- [ ] Fresh hosted compiler adoption, a hosted cache hit and final-head trusted replica
- [ ] Two independent positive re-reviews and a reviewer-owned all-five clean ledger
- [ ] Current candidate, authorized merge and clean containment
- [ ] Post-merge hosted results and Closed/Done
