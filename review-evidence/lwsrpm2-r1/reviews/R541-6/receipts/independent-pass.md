Independent source pass recorded before reading prior public review findings.
Head: 14c8b364863be49bc222f4913830b79d23dcf173.
Order: contributor rules and all guide roles; issue 10 acceptance and manager scope; issues 1, 6, 7, 11 and interface contracts; source-base diff/history and round-7 delta.
Conformance: saved-value obligation is represented by owned per-attribute storage; first failed Flush captures; timer/receive/explicit Flush completion consumes it. Ordinary LV recovery remains unchanged.
RTL: no RTL or submodule change in this C-library tree; inspected build selection, interfaces, queue ownership, timer lifecycle and native-test boundaries. Parent implementation acceptance remains separate.
Robustness: only one pending snapshot write, gated by !flush_pending. Source receive pre-completes withdrawal; local and replay joins write attr_val only. Reservations copy the selected saved value before indication. Reclamation requires MT; destroy frees pending attributes and queued work.
Tests: new cross-port and local matrices check old Leave value, visible Applicant updates, repeats, fresh snapshots and clearing; timer-completion regression adds three unchanged refreshes. Execution and mutation discrimination still pending.
Docs: interface and four guides describe saved-value ownership and limits. Counts and anchors require executable/checker verification.
Independent focused probes planned: deferred destination replay; all source event kinds; opposite-type replacement; repeated Flush/Re-declare; completion followed by reclaim; pending destruction; snapshot reserve-copy and length mutations.
No independent actionable defect identified in static delta pass. This is not a final verdict.
