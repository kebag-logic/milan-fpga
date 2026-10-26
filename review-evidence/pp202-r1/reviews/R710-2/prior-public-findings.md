https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/204#issuecomment-6414853154

## Findings

### F-1 MINOR: a declared Stream ID comes back with another DA after a disable/re-enable, with no move and no two-LeaveAllTime gap

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/acmp/KL_acmp_talker.sv:830-849`: `EVC_OFF` books no move and nothing records the DA declared under the current ID;
  - `:805-828`: any later grant is installed and declared under the unchanged ID.
- **Claims it contradicts:**
  - the banner, `:44-48`: "the new DA must never be declared under an ID that has been on the wire with another one";
  - `:1340-1342`;
  - `docs/architecture/05_acmp_engine.md:478` ("The new DA is then never declared under an ID that has been on the wire with the old one") and `:504` ("a declared ID is not declared again with another address");
  - the PR body ("a declared ID never comes back with another address").
- **Authority:**
  - IEEE 802.1Q-2018 §35.2.2.8: the same StreamID with a different FirstValue needs two LeaveAllTime periods after the withdrawal;
  - issue #202 Required: "If the same Stream ID is ever reused, the IEEE 802.1Q-2018 35.2.2.8 two-LeaveAllTime gap still holds";
  - the owner decision, item 4: "So does any path that re-declares the old ID".
- **Evidence:** `receipts/reviewer-probes-head.txt`, RP1[fresh].
  - Source 3 declares `0xAB00000000000003` with DA `91:e0:f0:00:01:03`. It is disabled, then re-enabled, and the allocator grants a fresh address. This is legal on the 02 §4.2 face after a RELEASE_DA, and it is the talker bench's own default allocator model. A probe 500 ms after the withdrawal then declares `0xAB00000000000003` with DA `91:e0:f0:00:01:08`.
  - With a block allocator (RP1[block]), the DA is unchanged and nothing is wrong.
- **Impact:**
  - This is not reachable with the in-scope `KL_pp_maap` (one block, source s = base + s, RELEASE_DA a no-op), nor with the parent shim (`eff_aaf_dmac + j`). On both, a block move raises a conflict for every source, which books the move.
  - It is reachable with any allocator that hands a source a different address after a release, which the face contract permits.
  - The behaviour pre-exists at `ed211803`. But this round's scope item and its new universal claims cover it, and the bench does not exercise it: S1's "the move survives a disable" (`tb/acmp_talker/sid_cases.hpp:146`) only reads `src_stream_id_o`.
- **Required outcome**, one of:
  - **(a) RTL:** a source whose current ID has been declared and which is granted a DA other than the one last declared under that ID must move (or keep the 35.2.2.8 gap). For example, book the move at `EVC_OFF` while `sid_used_r` is set, or keep the last declared DA per source and compare it at the grant. Add a bench case of the RP1 shape and a named STREAM_ID mutant.
  - **(b) An owner ruling** that the `maap` face requires an allocator to return the same DA for a source until it raises `MAAP_CONFLICT` for it. State that in 02 §4.2, narrow the banner, 05 and PR claims to that condition, and state what the bench's fresh-address default model represents.
- **Verification:** RP1[fresh] passes (or the narrowed contract is stated and graded), and every suite stays green.

### F-2 MINOR: no check binds a slot's published upper 48 bits to its own slot

- **Lenses:** Tests.
- **Where:**
  - `tb/acmp_talker/sid_cases.hpp:183-192` (S4 provisions slot 7 as `0xCD00000000000008` but never reads `sid_pub(7)`);
  - `tb/pp_top/sim_main.cpp` MP8 (every slot is `{OWN_MAC, s}`);
  - `tb/pp_top/acmp_mutants.py` STREAM_ID group.
- **Authority:** owner decision, item 1 ("After reset it equals the `cfg_stream_id_i` slice"); the 02 F02.10 `src_stream_id[src]` row.
- **Evidence:** `receipts/reviewer-mutant-suites.txt` and `reviewer-mutants-talker-bench.txt`.
  - In `own_pub_upper_slot0`, `g_sid_pub` takes `cfg_stream_id_i[16 +: 48]` for every slot. It SURVIVES `tb/acmp_talker`, `tb/pp_top --acmp-only` and `tb/pp_top --maap-internal-only`. Only the reviewer fuzz RP3 kills it (4,211 publish mismatches).
- **Impact:** a publish defect for a slot under other upper 48 bits would make the framer stamp and GET_STREAM_INFO name an ID that PROBE_TX and DECLARE_TALKER never carry, so a listener bound through PROBE_TX receives nothing. No committed check would catch it.
- **Required outcome:**
  - A check that every slot's `src_stream_id_o` equals its full 64-bit `cfg_stream_id_i` slice after reset, with at least one slot under other upper 48 bits. For example, in S4: `sid_pub(7) == 0xCD00000000000008` before and after src0's move.
  - A check that a moved slot under other upper 48 bits keeps them.
  - The mutant added to the STREAM_ID group and killed by name.
- **Verification:** `scripts/own_mutants_campaign.py` reports KILLED.

### F-3 MINOR: 10 says the new ID is declared "from its first New"; the RTL issues Join!

- **Lenses:** Docs, Conformance.
- **Where:** `docs/architecture/10_srp_engine.md:429` ("the Talker Advertise names the new ID from its first New").
- **Evidence:** `hdl/srp/KL_srp_talker_fsm.sv:473` (`gate_open_i ? (rec_valid_r[s] ? AE_JOIN_C : AE_NEW_C)`). `rec_valid_r` is cleared only at reset (`:542`) and set at the first open (`:589`). So the re-open after a move is a Join!, and the new ID's first message is the applicant's Join, not New. New! occurs only at a source's first declaration since reset.
- **Impact:** a statement about the MRP event on the wire that the RTL does not produce. It is a protocol-behaviour claim, so it is not RESIDUE.
- **Required outcome:** either correct the sentence to the RTL's behaviour, or, if New! is intended for a new Stream ID, change the RTL and grade the event in MP8.
- **Verification:** the text and the RTL agree. Optionally, MP8 reads the attribute event.

### RESIDUE-1: vague provenance wording

- **Where:** `tb/pp_top/README.md:2092`, "Measured 2026-10-26 on the lane tree".
- **Fix:** replace with "Measured 2026-10-26 at a8aa626e1cba (RTL as at bba84945)". This is wording only.

### SUGGESTIONs (do not affect the verdict)

- **S-1 (Robustness).** If a grant ever arrived inside the applicant's LA window after the withdrawal (before its next transmit opportunity), LA + Join! would go to AA (`KL_srp_talker_fsm.sv:236`). The open overwrites `sid_r` (`:588-592`), so the withdrawn ID's Leave would never go out and its registration would age out only by LeaveAll. This is unreachable with any IEEE 1722-2016 Annex B allocator: a fresh claim takes at least three probe intervals, which 05's lap argument already assumes. Suggest stating that assumption in 02 §4.2 / 05, or holding the re-open until the old declaration has left.
- **S-2 (Docs).** The distinctness proof holds for `cfg_stream_id_i` stable since reset, which is the quasi-static rule of 02 §2 rule 4 and integrator §6. Moved IDs persist until reset, so a re-provision without reset could meet a stale moved ID. Suggest naming the assumption in 05 `sec-05-sidmove`.
- **S-3 (parent patch).** In `KL_aaf_packetizer`, a non-zero TCTX unique ID for t > 0 still outranks `stream_id_i`. No board software drives that window, and it already diverges from `cfg_stream_id_i` at the base. Even so, the pin-adoption PR should either let `src_stream_id_o` win or state the exception.
- **S-4 (Docs).** In 00 GAP-04, the parenthesis "(withdraw → new DA → new Stream ID; Table 5.3, 802.1Q-2018 §35.2.2.8)" sits under "Mandatory behavior". Marking the new Stream ID as this design's choice (Table 5.3 is informative) would match REQ-ACMP-010.
- **S-5 (Tests, parent).** The pin-adoption PR could add one parent scenario that drives a MAAP conflict on a declaring source and compares the AAF stamp, GET_STREAM_INFO selector 2 and PROBE_TX.


https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/204#issuecomment-6414931259

**R710-F01 — MAJOR — same-ID PCP change after withdrawal bypasses two LeaveAllTime.**

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Locations:** hdl/acmp/KL_acmp_talker.sv:869 (PCP handling), :915 (listener-driven declaration), :921 (withdrawal to DA_OK), :755 (probe-driven declaration); hdl/srp/KL_srp_talker_fsm.sv:500 (new declaration latches live priority), :530 (PriorityAndRank in FirstValue). Documentation/evidence: docs/00_MILAN_COMPLIANCE_REVIEW.md:406, docs/architecture/09_verification.md:807, tb/acmp_talker/retry_cases.hpp:199 and the PR's unconditional PCP-gap claim.
- **Authority:** option A item 4 and the explicit review requirement covering every same-ID path; IEEE 802.1Q-2018 35.2.2.8 and 35.2.2.8.5; REQ-ACMP-010.
- **Evidence:** own-head.log, own-results.json, own-cases.inc. With no fresh probe, a registered listener declares source 0 at 1000 ms. Listener withdrawal at 1010 ms takes it to DA_OK. A PCP-change event at 1011 ms does nothing because EVC_PCP handles only DECLARING. Returning listener demand at 1012 ms immediately opens the same ID, with zero backoff arms. Reproduced both for configured ID `ab00000000000000` and conflict-moved ID `ab00000000000008`. The completed run reports 1483 checks, 1481 PASS, 2 FAIL; both failures are the independent gap check. No configuration input was changed at runtime in this probe.
- **Impact:** the next declaration takes the changed PCP into FirstValue under the previous Stream ID only 2 ms after withdrawal. Ordinary listener churn plus Domain adoption defeats the normative gap. The inherited DECLARING-only branch is not newly introduced, but it is explicitly within frozen acceptance's requirement that every retained same-ID path preserve the gap. The new moved-ID lifecycle also reaches it.
- **Required outcome:** preserve the gap for a previously declared ID when its PCP changes after withdrawal, including IDs moved by conflict. Retain enough withdrawal/history state, or conservatively wait, so returning listener or probe demand cannot re-declare changed FirstValue too early. Keep the stipulated same-ID PCP policy. Add regression coverage for these interleavings and align compliance/evidence claims with demonstrated coverage.
- **Verification:** rerun both independent cases; require no early same-ID open and a legal later declaration after the gap. Cover listener and PROBE_TX reopening, original and moved IDs, and the existing normal PCP/conflict cases. The assigned `pcp_skips_the_gap` mutant is killed but exercises only the DECLARING branch.

**R710-F02 — MAJOR — parent AAF context UID overrides the published moved ID.**

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Artifact:** public author/parent-src-stream-id-wiring.patch:24–26, producing hdl/ieee1722/aaf/KL_aaf_packetizer.sv:495–497; associated parent hdl/milan/milan_datapath.sv:1546, :6166, :7477, :9626. Patch digest: `770210604495083d1661f7157111c4f4c2250f80dd610f1a0975d9f5b8585f89`.
- **Authority:** option A item 7 requires the frame stamp and output GET_STREAM_INFO selector 2 to read src_stream_id_o, agreeing with PROBE_TX after conflict; processor docs/guides/integrator.md:563, docs/architecture/06_aecp_engine.md:387, IEEE 1722-2016 4.4.4.8 and IEEE 1722.1-2021 7.4.16.2.
- **Evidence:** parent-source-verification.json, parent-probe.cpp, parent-probe.log, parent-probe-result.json. The exact public patch applies cleanly to parent base `e76a755afc0536453161e3cd33f6f4d2dcd7641f`; all three source blob identities match the patch's old indices. The patched packetizer was built and driven through normal context writes, sample input and frame output. Source 1's TCTX UID was explicitly set to 1, initially agreeing with the published ID. Captured frame bytes 22–29 were `0a0b0c0d0e0f0001`. Changing the published slot to `0a0b0c0d0e0f0008` still produced `0a0b0c0d0e0f0001` on the wire. Setting the context UID to its default 0 produced the correct moved `...0008`, establishing a passing control. Build rc 0; probe rc 1, `setup=PASS post-move-agreement=FAIL`.
- **Cause and impact:** `sid_named_w = (et_r != 0) && |euid_r` overrides the processor ID for any nonzero explicit UID on a nonzero source. Even explicitly configuring the ordinary source-number UID causes disagreement after the ID moves. GSI reads the published vector directly, and processor PROBE_TX uses that identity, while AAF frames retain the withdrawn identity. A listener following the new reservation will not match those frames. The CRF connection and GSI selector wiring themselves are direct and correct. The PR's parent-agreement claim is too broad.
- **Required outcome:** in processor-owned integration, the published current ID must outrank an explicit TCTX UID. If standalone compatibility needs a fallback, select it explicitly without overriding a connected processor's identity. Add an executable parent agreement test with an explicit nonzero context UID and update the handover/evidence claims.
- **Verification:** the provided frame-byte probe must pass initial and moved IDs with UID 1 retained, as well as its default-UID control. At pin adoption, exercise an actual declaring-source MAAP conflict and compare AAF/CRF frames, GET_STREAM_INFO selector 2 and PROBE_TX. This focused parent probe supplies the changed published value directly; it is not a full parent conflict simulation.

**R710-R01 — RESIDUE — new bench labels in source comments.**

- **Lenses:** Docs; this wording-only finding does not make a lens unclean.
- **Authority:** the supplied owner comment rule dated 2026-10-15. New source comments describe behavior/reason with issue/requirement identifiers rather than bench labels. Existing instances belong to #746.
- **Locations and exact fix:** remove `S1:`, `S2:`, `S3:`, `S4:`, `S6:`, `S5:` from comment headings in tb/acmp_talker/sid_cases.hpp:81, :154, :168, :183, :194, :232, retaining the behavioral sentences. In tb/acmp_talker/sim_main.cpp:13, replace `issue #202, sections E and S` with `issue #202, REQ-ACMP-010`; at :213 replace `section S, issue #202` with `issue #202, REQ-ACMP-010`. At tb/pp_top/acmp_mutants.py:419–420, replace the section-label references with `The talker suite grades the rule; the processor-top suite grades the whole path`. At tb/pp_top/pp_top_wrap.sv:268 replace `which section MP8` with `which the conflict-recovery test`. At tb/pp_top/sim_main.cpp:9381 remove `MP8:` from the heading; at :9394 replace `MP8a, inside MP4's walk:` with `During the replacement-address claim:`; at :9410 replace `inside MP8's second` with `within the observation second`.
- **Impact:** comment style only; no measurement, assertion name, test, generated artifact, clause claim or behavior changes. Leave executable named-check strings intact. Existing labels merely carried through rewritten old comments are not separately charged here.
- **Verification:** inspect added comments and apply the specified prose-only replacements; carry to the manager's residue checklist. Findings text and test documentation may retain names needed to locate evidence.


