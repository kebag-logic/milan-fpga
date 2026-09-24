DRAFT written before reading any prior review comment on PR #549 (time-ordered evidence of independence).

Draft verdict: NEGATIVE - exact head 446e79b977640d13fa1e5dc0f9896d6c5a70391d

Draft findings:
- F1 MINOR Docs: the corrected opening-edge corner says its "whole/only effect" is status skew and names LWSRP_STATUS[8].
  In the refused sub-case the gate (ACTIVE via opt window) pulses for up to three rounds for a declaration that ends Talker Failed:
  Table 5.4 STREAM_START/STREAM_STOP each +1 and interval counters zeroed (KL_talker_diag_ctx edge logic on tkd_streaming_w),
  and a PDU whose event falls in the window can leave. [8] is source 0's gate only, so the CRF (uid 1) corner never shows on [8].
  Sites: milan_datapath.sv:6587-6593, CHANGELOG.md:41, EGRESS_QUEUE_MAP.md:78-83, REGISTER_MAP.md:1112-1117, ieee8021q.md:57-58;
  FR_NFR.md:211-213 "ACTIVE, which needs ... the grant" (opt window).
- S1 SUGGESTION Docs: milan_datapath.sv:1588 "gates stop consulting the admission verdict" (gates consult ACTIVE).
- S2 SUGGESTION Docs: KL_pp_shadow.sv:143/1238 and milan_csr.sv:790 legacy "CBS slope MUX"/"bw-gate" wording (pre-existing).

Draft ledger:
Conformance CLEAN (R284-2, 446e79b9) - acceptance items 1-3 unchanged, logic unchanged; ACTIVE always requires LR/RF.
RTL CLEAN (R284-2, 446e79b9) - hdl change comment-only (83 lines, stripped-identical, no metacomments), gate logic verified.
Robustness CLEAN (R284-2, 446e79b9) - no logic change; corner paths read in processor RTL.
Tests CLEAN (R284-2, 446e79b9) - crflic 85/0, crflic-mutants 4/4, behave 317/0 at head; anchors count 1.
Docs UNCLEAN (R284-2, 446e79b9) - F1.
