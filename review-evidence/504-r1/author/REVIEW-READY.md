[A160] REVIEW READY - local implementation handoff; real-SDK validation BLOCKED

Commit: 3d90958f3a82ca2a9617112c107a22f332117e17
Tree: b595c57b41d253660fcc84794352f174b90008a6
Base: 52711029f374650dc93830d5ea28e81cb5c8f410
Branch: 504-hosted-rv32-compiler
State: clean, two local commits, source unpublished.

Changed: selected checksum-pinned SDK installer and cache verification;
provisioning in docs-check and elaborate; mandatory adoption through the
existing absolute selector; compiler-absent and audited disposable-prefix
reproduction helpers; workflow pins/mutations and authoritative documentation.
The scope gate permits exact SDK metadata only in installer/fixture files,
with new wrong-file, second-term and protected-product-document controls.
No firmware text refusal, resolver residual, firmware, RTL, product option,
processor pin, scheduling, scope guard, AEM injection or act boundary changed.

FINAL-HEAD EVIDENCE

All commands below exited 0 with clean before/after state at 3d90958f3a82ca2a9617112c107a22f332117e17:

- python3 scripts/ci_rv32_sdk_selftest.py: 16 tests pass. Fresh extraction and
  cache-hit controls use a small synthetic archive; wrong digest/provenance,
  malformed/truncated/symlink receipts, incomplete/corrupt trees, wrong modes,
  failed relocation, wrong tool version/target/sysroot, moved prefix and
  unsupported host refuse for their named causes. See final-installer.*.
- python3 scripts/check_baremetal_only.py --selftest: 365 arms pass, including
  23 new SDK metadata allowance/refusal controls. See final-scope-selftest.*.
- python3 scripts/check_baremetal_only.py --check: zero findings across 828
  tracked first-party files. See final-scope-check.*.
- python3 scripts/check_em_dash.py --base 52711029f374650dc93830d5ea28e81cb5c8f410:
  zero findings over 80 added lines in two pages; 57/57 controls pass.
  See final-em-dash.*.

UNCHANGED BEHAVIOR MEASURED AT THE PRECEDING IMPLEMENTATION COMMIT

These commands exited 0 at ab2671c0f12cdd68df8a9260f98960b92f533efc, tree
85b9bb5a71a82c0cdf953fdb09384d0e60b3f606, with clean before/after state.
unchanged-artifacts.json proves that both workflow files, ci_events.py,
test_builder.py and test_firmware_compiler.py retain their exact measured blobs.
The final follow-up changed only scope masks/controls, installer docstring,
fixture spellings and CI documentation. These earlier measurements are not
relabeled as executions at the final head.

- python3 sw/builder/test_firmware_compiler.py --selftest: argv mapping and
  result propagation pass; host firmware fallback is refused; the actual
  gate refuses both absent and alternate RV32 candidates under --require-rv32.
  See head-selector.*.
- python3 -u sw/builder/test_firmware_compiler.py --absent --audit
  $WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-author/head-absent-argv.jsonl:
  182/182 hostile refusals, 17/17 legitimate firmware edits, 4/4 legitimate
  Makefile edits, 46/46 RTL mutation elaborations; GATE 1b PASS, 1 NOT RUN,
  zero actual firmware compiler invocations. The NOT RUN explicitly names all
  compiler instruments and the retained text rules. See head-absent.* and
  head-absent-argv.jsonl. This is gate 1b, not the complete builder sweep.
- python3 scripts/ci_events.py --check: 1555 contract items pass.
- python3 scripts/ci_events.py --selftest: 1198 mutation arms pass.
  See head-workflow-check.* and head-workflow-selftest.*.

Additional focused checks passed with their measured source/index receipts:
Python idiom (no budget growth), docs_check (zero findings), documentation
style, hygiene, fail-fast, shell idiom, ci_scope selftest and TOC consistency.
Python idiom and docs_check were repeated on the final source before the
follow-up commit; see sdk-python-after-scope-checked.* and sdk-docs-after-scope.*.
command-index.json lists every recorded run and status; earlier failures and
command errors remain visible. RUN-NOTES.md explains their causes.
measured-local-tools.json records executable realpaths/versions. The absent
run used GNU Make 4.4.1 and Verilator 5.052; host GCC 16.2.1 only answered
version/RV32 target probes and never compiled firmware.

BLOCKER AND LIMITS

The official archive could not be completely downloaded in this session.
Several bounded direct/range attempts timed out. The normal installer download
path, invoked with an explicit disposable destination and timeout 180s,
exited 124 before extraction. Its destination remains absent. See
sdk-fresh-online.json/.log and acquisition-status.json.
No real archive was verified or executed, no real SDK installation/cache-hit
was measured, and no Bootlin-backed gate was run by this author. The selected
GCC 14.3.0/version/digest remain the public selection, not a new observation.
A10's prior public readiness result is not attributed to this author/head.
The mapped-prefix helper is ready to reproduce that measurement after a
complete pinned archive becomes available. It preserves every argument after
argv[0] and logs the actual invocation and assembly architecture.

Acceptance status:
1. Fresh hosted installation and pristine compiler-backed gate: NOT MET here.
2. Compiler-backed hostile controls: NOT RUN here; absent controls pass.
3. Deliberately absent firmware gate: PASS at the named preceding commit;
   final builder/harness blobs are unchanged. Final-head manager validation
   remains pending.
4. Focused workflow controls: PASS at the named preceding commit with unchanged
   workflow/contract blobs. Full native banks, trusted act, hosted contexts and
   candidate validation remain pending with A10.
5. Additional C-library residual: NONE; existing residual remains unchanged.

Scope interaction and narrow resolution were published before edits:
https://github.com/kebag-logic/milan-fpga/issues/504#issuecomment-5779350864
The host-tooling non-goal of #259 permits verification SDK identity metadata;
no general retired-term, product-document or firmware-rule exception was added.

R227 and R228 remain the reserved independent reviewers. No review verdict or
lens completion claim is made by the implementation author. No push, PR
metadata change, Docker/act, hardware, privilege, delegation or merge occurred.

Public author handoff: https://github.com/kebag-logic/milan-fpga/issues/504#issuecomment-5779488988
