[R709] NEGATIVE - exact head a8aa626e1cba30625ac764c70e1fb8fb02c69c40

# R709-1: independent review of PR #204 (issue #202) at exact head

- **Head:** `a8aa626e1cba30625ac764c70e1fb8fb02c69c40`, tree `7eb73a9f7b4b00799fd9e0206bda786cf0c3c0f1`, four commits on `ed211803`, 20 files. The [A676b] round follows the owner's option-A decision (issue #202, comment 6408987895).
- **Verdict:** NEGATIVE. Three MINOR findings are open: F-1, F-2 and F-3. There is one RESIDUE item and five SUGGESTIONs.
- **Prior public findings:** none. PR #204 has no reviews and no review comments. Its only comment is the manager's review-start notice. There is nothing to resolve or retain.

## How the review was done

I worked in a cleared context, using only public material:

- the repository README and docs/README conventions (the repository has no AGENTS.md or CONTRIBUTING.md);
- the issue body and its six comments: the [A676] STOP, the owner decision and the [A676b] REVIEW READY;
- the PR body;
- the authorities the diff names;
- `git diff ed211803..a8aa626e` and its history (bba8494 to a8aa626 changes docs only);
- the public evidence at kebag-logic/milan-fpga `51842a7a` `review-evidence/pp202-r1`, specifically the parent patch, PARENT-STATE and the consumer SUMMARY files.

I read no private material and no other reviewer's report.

**Execution:**
- Every build ran in a disposable copy under `scratch/`, using pinned Verilator 5.050. Its identity is recorded in `receipts/env.txt`. The PATH default is 5.052 and was not used.
- Afterwards, the review clone was verified byte-exact at head:
  - status, including ignored files, is empty;
  - `write-tree` gives `7eb73a9f`;
  - the index and tree mode/blob digests are equal;
  - the tree has no gitlinks, so there are none to check.

## Focus items, verified

**(1) Top-level change.**
- The only port change in `hdl/top/protocol_processor_top.sv` is the new output `src_stream_id_o[N_STREAM_OUT_P*64-1:0]` (lines 680-686), plus its connection (line 2356). There is no parameter or register-map change.
- After reset, `sid_ovr_v_r` = 0, so `g_sid_pub` (`KL_acmp_talker.sv:1359-1363`) equals the `cfg_stream_id_i` slice.
- The output is named in 02 F02.10 and §4.3, the integrator guide §6 and §8, and diagram 21.
- For the same-upper-bits case, this is checked by S1, MP8a and MP8. For slots under other upper 48 bits it is **not** checked (F-2).

**(2) Conflict path, move rule, distinctness.**
- `EVC_CONFLICT` on DECLARING closes the gate, invalidates the DA and goes to NO_DA, with `ev_initset_w` set and no draw (`:851-867`). This is independent of the processor's T-SRP-LEAVEALL2.
- The grant (`:805-828`) installs the booked move. It runs a search in `S_EV_SID`, one candidate per clock (`:1086-1092`, `:1314-1355`), and the declaration in the same walk uses `mv_sid_w`.
- The rule keeps the upper 48 bits. A candidate is refused if it equals any slot's configured ID or any slot's moved ID as a whole 64-bit value, the mover's own included. Every current ID is a configured or moved ID, so the result differs from every current ID, the withdrawn one included. The search ends within 2·N+1 clocks.
- I tried colliding provisioned values myself:
  - **RP2:** the mover's own slot was provisioned with the first candidate `{UP, 8}`. The move skips it and takes `{UP, 9}`.
  - **RP3:** 40 random provisionings with two upper-48 values. Unique IDs were drawn from the first candidates (8-31), the default block (0-7) and the wrap edge (0xFFF8-0xFFFF), with every source declaring. Across 12,000 random conflicts, there were 0 violations of: new ID ≠ withdrawn ID, ≠ every other current ID, upper 48 bits kept, `src_stream_id_o` = declared ID, no other ID moving, and PROBE_TX and GET_TX_STATE answering the new ID and DA.
- The move is not deferred by the processor's own gap. Conflict to new declaration took 1,700 ms in S1 and 1,737 ms in MP8 through the in-scope MAAP engine.
- PROBE_TX (`:1447`), GET_TX_STATE (`:1470`) and both DECLARE_TALKER strobes (`:1500`, `:1507`) carry the current ID.
- The clause statement, Milan v1.2 Table 5.3 (5.3.7.5, informative), sits with the rule in the banner and in 05 `sec-05-sidmove`.

**(3) PROBE_TX failure status.**
- `da_ok_w = rec_w.da_valid && !pe_conflict_r` (`:736`). TALKER_DEST_MAC_FAILED is answered exactly while the source holds no valid DA, or while a conflict is pending.
- This is checked by E2, S1 and MP8a.
- My mutant `own_probe_ignores_da_valid` is killed by the authors' checks (E2, I4, J5 and others).

**(4) Same-Stream-ID paths.**
- The PCP path (`:869-878`) is unchanged and keeps BACKOFF with the draw. F2, F5 and R6 check it, and the mutant `pcp_skips_the_gap` is killed.
- A conflict inside the PCP backoff does not shorten it.
- **Not held:** the disable/re-enable path re-declares the same ID with another DA and no gap (F-1).

**(5) Tests and mutants.**
- Suite results at head:
  - `tb/acmp_talker`: 1,463/1,463 at head, 1,376/1,376 at base;
  - `tb/pp_top` full `make run`: 10,749/10,749, MP8 1,737 ms;
  - the STREAM_ID group of `acmp_mutants.py` (`--jobs 8`): **20 of 20 KILLED** by their named checks, goldens PASS;
  - the talker retry campaign: 62 killed, 7 equivalence controls, 1 performance control, rc 0.
- On the old behaviour, the head bench run on the base talker RTL (with `src_stream_id_o` stubbed to the configured IDs) fails 115 checks. These include every S1 timing and new-ID check (`receipts/talker-head-bench-on-old-rtl.txt`).
- I planted five mutants of my own:
  - **Killed by the authors' checks:**
    - `own_search_unchecked_step` (a colliding ID taken after one hit): killed by S5;
    - `own_search_skips_self` (the withdrawn ID taken back): killed by S5 and by my RP2;
    - `own_output_lags_declaration` (the output follows only once declared): killed by S6;
    - `own_probe_ignores_da_valid`.
  - **Survived the authors' checks:** `own_pub_upper_slot0`, in which every slot publishes slot 0's upper 48 bits. It survived `tb/acmp_talker`, `tb/pp_top --acmp-only` and `tb/pp_top --maap-internal-only` under the repository's own judge, and only my RP3 kills it (F-2).

**(6) Documents.**
- REQ-ACMP-010 (00:406) now cites IEEE 802.1Q-2018 §35.2.2.8 and marks Table 5.3 informative. The 08 T-SRP-LEAVEALL2 row (08:36) is limited to the same Stream ID.
- F05.12, 02, 06, 09 §8.13 and the integrator guide match the RTL, except for the claims in F-1, and the 10 claim in F-3.
- `make -j16 check` and `scripts/lint_hdl.sh` pass at head.

**Parent wiring patch.** `pp202-a676b/parent-src-stream-id-wiring.patch`, sha256 `77021060…`, applies cleanly (`patch --dry-run`) to milan-fpga `e76a755afc`. I judged it by reading:
- At `e76a755afc`, the per-source ID has three consumers: the AAF stamp, the CRF stamp and output GET_STREAM_INFO selector 2. The patch repoints all three:
  - **AAF stamp:** `KL_aaf_packetizer` gains a `stream_id_i` input, fed from `pp_cd_src_stream_id_w`.
  - **CRF stamp:** it reads the CRF source's slice through `crft_tx_sid_w` when that source exists, and keeps the CSR value otherwise.
  - **GET_STREAM_INFO selector 2:** `gsi_osid_w` reads `pp_cd_src_stream_id_w`.
- `KL_pp_shadow` passes the port out.
- Selector 2 answers only while declaring (`gsi_decl_w`). So the wire, GET_STREAM_INFO and PROBE_TX agree after a conflict, with one exception: a software-named TCTX unique ID still outranks the processor's ID (S-3).
- The parent SRP control plane is the processor, and the lwSRP applicant is deleted. So no parent-side declaration bypasses `src_stream_id_o`.
- No parent suite drives a conflict on a declaring source (this is stated in the PR), so parent-side agreement after a conflict is established by reading and by MP8, not by a parent run.

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

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1, F-3) | 802.1Q-2018 §35.2.2.8 / Table 10-7 and Milan v1.2 5.3.7.5 Table 5.3, 5.5.4.1 step 3, Table 5.42 against `KL_acmp_talker.sv` (conflict, PCP, OFF, grant, response, gate paths) and `KL_srp_talker_fsm.sv` applicant events; REQ-ACMP-010; 08 row | R709-1 | a8aa626e1cba30625ac764c70e1fb8fb02c69c40 |
| RTL | UNCLEAN (F-1) | full `KL_acmp_talker.sv` read; top port delta; move search and publish; walker serialisation; RP1 to RP3; 5 own mutants; base-RTL replay | R709-1 | a8aa626e1cba30625ac764c70e1fb8fb02c69c40 |
| Robustness | UNCLEAN (F-1) | disable/re-enable with a fresh allocator; conflict inside the PCP backoff, while disabled and during an in-flight allocation; cursor lap (S5); fuzzed provisioning (RP3); fast-grant applicant window (S-1) | R709-1 | a8aa626e1cba30625ac764c70e1fb8fb02c69c40 |
| Tests | UNCLEAN (F-1, F-2) | `sid_cases.hpp`, `retry_cases.hpp`, the `sim_main.cpp` diffs, MP8/MP8a; suites rerun (1,463, 10,749); STREAM_ID 20/20; retry 62/7/1; head bench on old RTL (115 FAIL); 5 own mutants (1 survivor) | R709-1 | a8aa626e1cba30625ac764c70e1fb8fb02c69c40 |
| Docs | UNCLEAN (F-1, F-3) | 00, 02, 05, 06, 08, 09, 10, integrator guide, diagram 21, the three tb READMEs; `make -j16 check` rc 0; lint rc 0; comment-rule scan of every added hdl/tb line (no source-comment residue; RESIDUE-1 is in a README) | R709-1 | a8aa626e1cba30625ac764c70e1fb8fb02c69c40 |

## Real limits

- I did not run the full suite bank, the other campaigns (MAAP, AECP, notifications, D3, elaboration guards), Yosys portability or the parent suites. The parent figures quoted come from the author's published receipts, and the parent patch was judged by reading and a dry-run apply only.
- The `tb/maap` campaign and the parent consumer gate were not re-executed.
- Hosted checks at this head (read 11:22Z, inspection only): docs-gates success ×2, portability success ×2, suites in progress ×2. Nothing was inferred from the in-progress contexts.
- No manager source bank exists at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Rule on F-1, option (a) or (b), and carry RESIDUE-1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `ed211803`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`) with the builder and native banks, and link the receipts.
- Own hosted/act acceptance, including the `suites` contexts still running at 11:22Z.
- Land the parent wiring in the milan-fpga pin-adoption PR, with S-3 and S-5 considered there.

## Packet

- **Scripts** (`scripts/`):
  - `r709_cases.hpp`: reviewer probes RP1 to RP3;
  - `run_talker_probe.sh`: copies a tree, adds the probes, optionally plants one edit, builds and runs;
  - `mutants/*.py`: the five reviewer mutants;
  - `own_mutants_campaign.py`: grades F-2's mutant through the repository's own judge;
  - `collect_receipts.sh`: builds the receipts from the raw logs.
- **Receipts** (`receipts/`): excerpts (tallies, every FAIL line, verdicts), with local install paths replaced by placeholders. The full mutant `results.json` files are included.
- Every published file is listed in `MANIFEST.sha256`.

R709-1 FINISHED
