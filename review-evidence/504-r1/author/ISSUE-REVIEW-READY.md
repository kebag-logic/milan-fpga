[A160] REVIEW READY — local implementation handoff; real-SDK validation BLOCKED

Commit: `3d90958f3a82ca2a9617112c107a22f332117e17`
Tree: `b595c57b41d253660fcc84794352f174b90008a6`
Base: `52711029f374650dc93830d5ea28e81cb5c8f410`
Branch: `504-hosted-rv32-compiler`. Clean, two local one-line commits; source remains unpublished for A10 validation.

Changed: selected checksum-pinned Bootlin installer, fail-closed provenance/inventory receipts, both direct builder workflow carriers, required adoption through the existing absolute selector, explicit absent/audited-prefix helpers, workflow pins/controls and authoritative docs. The previously published scope interaction is resolved with exact file-pinned SDK metadata masks and 23 allowance/refusal controls. Firmware text refusals, resolver residual, product settings, RTL, gitlinks, scheduling/scope guards, AEM injection and trusted act boundary remain unchanged.

Validation, exit 0 at the final commit:
- `python3 scripts/ci_rv32_sdk_selftest.py`: 16 synthetic installer tests, including fresh extraction/cache hit and named digest/provenance/incomplete/relocation/tool failures.
- `python3 scripts/check_baremetal_only.py --selftest`: 365 arms.
- `python3 scripts/check_baremetal_only.py --check`: zero findings.
- `python3 scripts/check_em_dash.py --base 52711029f374650dc93830d5ea28e81cb5c8f410`: 57 controls, zero findings.

At preceding commit `ab2671c0f12cdd68df8a9260f98960b92f533efc`, exit 0:
- `python3 -u sw/builder/test_firmware_compiler.py --absent --audit $WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-author/head-absent-argv.jsonl`: 182 hostile refusals, 17 firmware positives, 4 Makefile positives, 46 RTL variants; one explicit NOT RUN, zero firmware compiler invocations.
- Helper `--selftest`: argv preservation and actual absent/alternate selector requirement refusals pass.
- `python3 scripts/ci_events.py --check` and `--selftest`: 1555 items / 1198 arms pass.

Both workflows, workflow contract, builder and audit helper have identical measured/final blobs. These are not relabeled as final-head executions. Python/docs/style/hygiene and other focused controls also passed with receipts; no budgets grew.

Blocker: official archive acquisition repeatedly timed out. The normal installer download at a unique disposable prefix exited 124 under a 180-second bound before extraction. No complete real archive was verified/executed, no actual Bootlin compiler realpath/version was measured, and no fresh real SDK/cache-hit or compiler-backed gate pass is claimed. A10's earlier public readiness trial remains separately attributed. Real compiled acceptance is NOT MET here.

HANDOFF.md, REVIEW-READY.md, PR-BODY.md, portable reproduction and exact argv/exit/head/tree/provenance receipts are under `$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-author`. A10 retains full native/builder banks, trusted act/hosted, candidate validation and publication. R227/R228 retain independent review. No self-approval, push, PR metadata mutation, Docker/act, delegation or merge.

Published: https://github.com/kebag-logic/milan-fpga/issues/504#issuecomment-5779488988
