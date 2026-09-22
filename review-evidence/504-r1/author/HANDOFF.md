[A160] Author handoff for issue #504

Local implementation is prepared. Real SDK validation is BLOCKED by download timeouts.
The direct installer download attempt exited 124 under a 180-second limit,
before extraction; its destination does not exist. No real SDK archive was
verified, extracted or executed in this author session. No fresh local Bootlin
installation or compiler-backed compatibility result is claimed.

Final local commit: 3d90958f3a82ca2a9617112c107a22f332117e17
Tree: b595c57b41d253660fcc84794352f174b90008a6
The lane is clean and unpublished, with two one-line commits and no trailers. Command receipts and unfiltered logs
are in this directory. Each JSON identifies argv, exit, head and tree.

Base: 52711029f374650dc93830d5ea28e81cb5c8f410
Lane: $CANDIDATE
Branch: 504-hosted-rv32-compiler
Executor: A160. Independent reviewers: R227 internal Codex, R228 external Opus.

The two builder jobs cache the selected SDK and always verify it at
$HOME/br-milan-rv32/host before invoking the builder with --require-rv32.
The installer verifies the pinned archive before extraction and relocation.
The scope gate permits only exact SDK metadata in the installer and fixture;
23 new controls preserve wrong-file, appended-term and product-document refusals.
Cache receipts bind provenance, installer bytes/revision, host identity,
installation prefix, installed file hashes/modes/link targets, and actual
compiler identification. Existing unreceipted installations are refused.
The scripts do not change the workstation selector or HOME.

The explicit absent control hides only cross compiler candidates. Real host
compiler version/target probes remain visible; firmware compilation through
host or alternate candidates is refused. The real gate 1b, including retained
text refusals and legitimate controls, runs unchanged except for the required
compiler assertion and identification print. The mapped SDK mode changes only
the existing absolute selector argv[0], logging requested and executed argv,
return codes and assembly architecture. This proves local compatibility only.

The workflow scope guard, scheduling, AEM selftest injection, trusted act
orchestrator, firmware, RTL, product build options, residual and gitlinks remain
unchanged. No text refusal was retired. No budgets grew. No push, PR metadata,
Docker/act, privilege, hardware, merge or delegated work was performed.

Manager A10 retains full builder/native parent/PP/gPTP/Yosys banks, candidate
validation, trusted act, exact-head hosted evidence, independent review,
publishing and merge/post-merge containment. This author reports evidence,
not approval or completed issue acceptance.

Reproduction uses the committed commands in docs/testing/CI_WORKFLOWS.md,
under Elaboration. The installation prefix must be unique and disposable for
local trials. Keep HOME and existing host selector paths untouched. A cold
runner uses the settled home-relative location through both workflow steps.

Focused evidence and acceptance-by-criterion status are in REVIEW-READY.md.
PR-BODY.md is an unpublished draft using the repository template.
RUN-NOTES.md explains controls, earlier command errors and evidence limits.
The complete pinned archive is the remaining author-side input needed for
real-SDK validation; independently verify its full SHA256 before --archive.

The final-head installer fixture, scope check/selftest and em-dash check pass.
The real absent gate and workflow integrity runs are recorded at the preceding
commit ab2671c0f12cdd68df8a9260f98960b92f533efc; their workflow/builder/harness
blobs are unchanged, as unchanged-artifacts.json records. They are not claimed
as executions at the final head. See REVIEW-READY.md for exact attribution.

Public author handoff: https://github.com/kebag-logic/milan-fpga/issues/504#issuecomment-5779488988
