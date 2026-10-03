[R443] NEGATIVE - exact head e2c7d97d158a30e44289a06a33f8ff4c5e289b87

Round R443-1, external independent review of processor PR #147 (lane C7, counters), closing issues #79, #44 and #78.
Exact head `e2c7d97d158a30e44289a06a33f8ff4c5e289b87`, tree `2334d3020826afef3d61625b3b2f08b008c848e9` (verified in the review clone, receipt `receipts/R3_clone_integrity.txt`). Source base for the diff: main `c74711d45a8bbc0d6b38cb49211b26a4a6413e88`; author lane head `751e1c0`; merge-base `88969246`.

The verdict is NEGATIVE because of one open MINOR in the Docs lens (R443-1-F1). The other four lenses are clean. The RTL change, the counters-face contract, K9 to K16, the 13 new mutants, the tick removal and the README merge all hold up under independent execution. F1 is a short documentation fix.

## Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R443-1-F1 | MINOR | Docs | `docs/architecture/05_acmp_engine.md:286` (A8 `avtp.INPUT_DISABLE`); `docs/architecture/05_acmp_engine.md:106` (flowchart edge "declare/withdraw, configure/enable" to "srp + avtp adapters"); `docs/architecture/01_overview.md:238` (flowchart node "srp/maap · gptp · avtp · mclk adapters"); also the comment `hdl/acmp/KL_pp_acmp_listener.sv:25` ("toward the srp+avtp adapters") | #78 / GAP-04: the docs describe adapter ops that the landed top does not expose. This PR rewrites 02 to the landed shape and edits 05 §2 to say "no `avtp` op exists" (`05_acmp_engine.md:23-26`). It also fixes A15 and the BIND_RX sequence, and the PR body says 05 and 01 "follow". However, the same action legend still has A8 calling `avtp.INPUT_DISABLE`, and two figures still draw avtp/gptp/mclk adapters. Receipt `receipts/S1_static_checks.log` (section 4). | 05 now contradicts itself. Its normative listener-teardown primitive (A8) names an op that no port serves, so an implementer or integrator reading the F05.3 action legend is told teardown issues a request that does not exist. On the landed top, teardown is the debounced `acmp_bound_o` falling (02 §4.4). Two figures still show the class-B adapter model that 02 §1 now says the landed top does not have. This is outside the literal text of #78 acceptance 1, which is limited to 02, so it does not by itself block closing #78. It is a defect this PR's own edits left inconsistent. | A8 should describe the landed action, for example "teardown SRP: `WITHDRAW_LISTENER`; withdraw the bound view (`acmp_bound_o` falls, debounced; the integrator disarms its RX filter, 02 §4.4); clear settled {stream_id, DA, VLAN}; talker_registered←0". The 05 flowchart edge should read for example "srp ops; bound/started levels" to "srp face + avtp levels". The 01 node should name the landed faces, for example "srp/maap faces · gptp/avtp/mclk levels · gsi/ctr read faces · side-port · nvm port". The listener comment should follow. | `grep -rnE 'avtp\.[A-Z_]+\|srp \+ avtp adapters\|gptp · avtp · mclk adapters' docs` returns nothing; `make check` rc 0. |
| R443-1-F2 | SUGGESTION | Tests, Robustness | `hdl/aecp/KL_aecp_notify.sv:499-506` (slot decode); `docs/guides/integrator.md:505-507`; 06 F06.15 push paragraph | The guide and 06 state that a change strobe with no notification slot (for example AVB_INTERFACE 1 or CLOCK_DOMAIN 1) is ignored. Probe P3 removed the AVB_INTERFACE `ev_ctr_index_i == 0` filter, and the whole default pp_top model still passed (8719 checks, 0 failures). Receipt `receipts/P3_notify_avb_any_index.log`. | The RTL is correct by inspection, but no check holds the documented rule. A regression would turn an AVB_INTERFACE 1 strobe (the redundancy case, processor #69) into an unrequested AVB_INTERFACE 0 push. | Optional: add a K12-style check that `ctr_change_i` for AVB_INTERFACE 1 and CLOCK_DOMAIN 1 pushes nothing, with a matching mutant arm. This could also be done in #69. | Re-run P3: it is killed. |
| R443-1-F3 | SUGGESTION | Tests | `tb/pp_top/ctr_mutants.py` (no `--jobs`) | After main's #146 was merged in, this is the only pp_top campaign driver without `--jobs N`. The other pp_top drivers, and those of acmp_talker, adp_engine, maap, srp_admission and srp_top, have it through `tb/common/mutant_pool.py`. The 13 arms run serially. | Wall time only. | Optional: adopt `mutant_pool` and `--jobs N`, and state it in the README campaign section. | `python3 tb/pp_top/ctr_mutants.py --jobs 8 ...` gives the same per-arm record. |
| R443-1-F4 | SUGGESTION | Conformance, Docs | `docs/guides/integrator.md:456`, `:463-471` | §7.1 allows STREAM_INPUT `0x00000FFF`. The reference platform's AAF inputs use that mask, per the published design table. The quadlet column lists only "(6, 7)", though, and the "what each counter counts" table gives TIMESTAMP_VALID and TIMESTAMP_NOT_VALID no meaning, interval rule or reset rule. | Two permitted counters are left implicit in a contract that is otherwise complete for Milan's floor set (Tables 5.13 to 5.17). | Optional: name quadlets 6 and 7 and state that they follow IEEE 1722.1-2021 Table 7-156 and reset with the input bank. | Doc review. |
| R443-1-F5 | RESIDUE | Docs | `docs/architecture/02_interfaces.md:209` (new), `:435` | The external-interface text names the engine-internal parameter `MEM_TIMEOUT_CYC_P`. The integrator sets the top-level `DESC_MEM_TMO_CYC_P` (`protocol_processor_top.sv:133`, bound at `:3694`), which is the name the integrator guide uses (`integrator.md:438`). Wording only. | None on behaviour. | Exact fix: write "`DESC_MEM_TMO_CYC_P` (the engine's `MEM_TIMEOUT_CYC_P`, 06 §8.1)" at both places. | Doc review. |
| R443-1-F6 | RESIDUE | Docs | `docs/architecture/02_interfaces.md:481` (§5 catalog, `LINK_UP/DOWN` row) | The rewritten catalog says it lists every event's consumers. `link_up_i` is also consumed by the internal MAAP engine (PortOperational!/Release!, `KL_pp_maap.sv:334`, top `:2328`) and by the PRNG seed latch (`KL_pp_prng.sv:116`, top `:976`). Wording only: the behaviour is documented in 11 and 08. | None on behaviour. | Exact fix: append "the internal MAAP engine (PortOperational!, [11](11_maap_engine.md)); the PRNG seed latch (first rise)" to that row's Consumers cell. | Doc review. |

No prior public review findings exist on this PR. It is round 1, and before this verdict the PR had no review, review comment or findings comment. A same-round report from the other reviewer was posted while this review was running. It was not read, so this review stays independent.

## Focus items

1. **ctr_* contract (integrator guide §7.1) against IEEE 1722.1-2021 §7.4.42 and Milan v1.2 §5.4.2.25.**
   - **Per-type table.** It matches the processor and the cited tables: AVB_INTERFACE `0x23` (quadlets 0, 1, 5); CLOCK_DOMAIN `0x03` (quadlets 0, 1); STREAM_INPUT `0xF3F`/`0xFFF`; STREAM_OUTPUT `0x1F` (Δ9). It also holds the mask/offset rule (bit *n* ⇔ `1<<n` ⇔ block byte 4n), the order (word 32 first, then 0 to 31), the hold-not-ready polarity, the watchdog, the wrong-object rule, and the four-type gate with locate-first.
   - **Read path in the RTL.** `KL_aecp_engine.sv:1156-1164` (gate), `:2173-2177` (`ctr_desc_type_o` = type, `ctr_desc_index_o` = index, `ctr_word_o` 32/0..31), `:2331` (hold), `gen_ucode.py` E_GCTRS (locate, mask beat, then 32 block beats). The processor reads the face exactly as documented.
   - **Push.** The `ctr_change_*` path goes to `KL_aecp_notify` ev_ctr (`protocol_processor_top.sv:3982-3984`). There is one slot per stream index, plus AVB_INTERFACE 0 and CLOCK_DOMAIN 0 (`KL_aecp_notify.sv:385, 491-506`), with a 1000 ms per-descriptor window (`:1037`), as documented.
   - **Counter semantics.** Wrap, reset-with-integrator, the not-bound to bound input-bank reset on `acmp_bound_o` (debounced, so a re-bind is not a reset), the three output resets on stream start, and invariants by construction from inactive-reset edge detectors are complete for every counter in Milan's set. On the two IEEE-only extras, see F4 (suggestion).
2. **K9 to K16.**
   - The pp_top suite at head passes: 9191 checks, 0 failures (5 builds); the K-AVB section alone has 23 checks.
   - The K expectations are written from Figure 7-67 / Tables 7-152 to 7-155, not read back. K11's distinct 3/2/5 counts are byte-exact at offsets 0, 4, 20 (#44 acceptance 3). K10 and K16 read the invariants off the wire. K11's domain-only strobe counts nothing. K13 to K16 grade one push per controller, the coalescing, the per-descriptor windows and the counts of the moment.
   - The 13-arm campaign at head: control PASS, 13 of 13 KILLED by their named checks. Each arm's failure count equals the README record.
   - K14's lower bound is 900 ms. However, probes P1 and P2 shortened the window to 900 ms and 950 ms, and both were killed by the existing storm check ST2b, which grades every descriptor, AVB_INTERFACE 0 and CLOCK_DOMAIN 0 included, at ≥ 1000 ms less one tick. P1 was also killed by U9c. The once-per-second rule is therefore graded exactly by the suite.
3. **Tick removal.**
   - At base, `gm_changed_tick_o` was read only by `adp_gm_tick_nc_w`, which had no reader, and by the adp_engine bench.
   - The 39 removed checks are P5's tick count plus the tick column of the 38 non-"C" cells of the 45-cell F04.2 walk (45 − 7). The replaced loop is the same four clocks (`idle(4)`), so nothing else lost an observation.
   - adp_engine passes 1367 at base and 1328 at head. Its campaign at head is control PASS, 30 arms KILLED, each failure count equal to the README.
   - The out-of-context cost of 0 is consistent by construction, since the flop had no load. The synthesis run was not repeated here.
   - The manager's ruling (#79 comment 5963704232) is consistent with the code: the removed tick was a one-clock-late copy of `gm_change_i`, which also fires on domain-only changes.
4. **02 §4.3 to §4.6, §5 and F02.10.**
   - These match the landed top, and no removed op or event is named in 02 (receipt S1).
   - F02.10's as_capable, prop_delay_ns, path_count, streaming[src] and mc_locked[domain] rows name their gsi/ctr words. The gsi kind 1 selector 1 bit layout matches `gen_ucode.py` E_GAVB.
   - Stale adapter names survive outside 02: see F1.
5. **Redundancy path.** Nothing narrows it. The face stays keyed by `{type, index}` (`ctr_desc_index_o` = the command's index), and the guide and 02 §4.6 state that a second interface is a second index. The single notification slot per AVB_INTERFACE and CLOCK_DOMAIN is pre-existing and documented, and the ruling records it for #69.
6. **Merge of main c74711d4.** The only files changed on both sides are the two READMEs. In the merge, each side's hunks are identical to that side's own diff, and the merge brings exactly main's 15 files.

**Acceptance per issue:**
- **#79:** 1 (00 §7 GAP-05 row) met; 3 (guide §7.1, REQ-AEM-018/019 and REQ-NET-004 point at it, F07.10 corrected) met; 4 ("tracked separately" gone) met.
- **#44:** 1 met (02 catalog and 04 §2/§6 no longer list counters as an in-processor consumer); 2 met (tick removed, as ruled); 3 met (K11).
- **#78:** 1 and 2 met within 02; 3 and 4 already met on main (`tb/srp_top` Q1 to Q4; #29 CLOSED).

## Executed evidence (all at exact head unless stated; pinned simulator 5.050, identity in `receipts/R0_tool_identity.txt`)

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/pp_top run` (5 builds) | rc 0, 9191 checks, 0 failures; K-AVB 23/0 | `receipts/A_pp_top_run.log`, `.rc` |
| `make -C tb/pp_top ctr-mutants` | rc 0, control PASS, 13/13 KILLED, per-arm counts equal to the README | `receipts/B_ctr_mutants.log`, `.rc` |
| `tb/adp_engine` suite, head / base c74711d | rc 0 / rc 0; 1328 / 1367 checks | `receipts/C1_adp_head.log`, `receipts/C2_adp_base.log` |
| `make -C tb/adp_engine mutants` | rc 0, 32/32; 30 arms' failure counts equal to the README | `receipts/C3_adp_mutants.log` |
| Focused lint of `KL_adp_engine` and `protocol_processor_top` (the flags of `scripts/lint_hdl.sh`) | both OK | `receipts/D1_focused_lint.log` |
| `make check` (copy) | rc 0: 41 mermaid + 18 wavedrom, 1087 links, 115 REQ / 17 GAP, 94 rows 0 untested, 27 parameters | `receipts/D2_make_check.log` |
| `make stale`, `gen_matrix.py --check` (clone) | rc 0, rc 0 | `receipts/D3_stale_genmatrix_in_clone.log` |
| Probe P1: notify window 1000 to 900 ms | killed: U9c and ST2b ×5 (K-AVB passes) | `receipts/P1_notify_window_900.log` |
| Probe P2: notify window 1000 to 950 ms | killed: ST2b ×5 (K-AVB passes) | `receipts/P2_notify_window_950.log` |
| Probe P3: AVB_INTERFACE strobe accepted at any index | survives the whole default model (F2) | `receipts/P3_notify_avb_any_index.log` |
| Static checks (merge, tick references, removed names, face wiring) | see focus items | `receipts/S1_static_checks.log` |
| Public evidence and state | evidence hashes match its manifest; PR body = evidence copy plus the manager's merge section | `receipts/R1_public_evidence.txt`, `receipts/R2_public_state.txt` |
| Clone integrity after the review | HEAD/tree exact; worktree, index and HEAD equal; 494 tracked blobs rehashed, 0 differ; modes equal; 0 untracked/ignored; 0 gitlinks required (none in this tree) | `receipts/R3_clone_integrity.txt` |

All probes ran in disposable copies under the packet's scratch area. No file in the review clone was edited.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | integrator guide §7.1 against IEEE 1722.1-2021 §7.4.42 (Figure 7-67, Tables 7-152 to 7-159) and Milan v1.2 §5.4.2.25 (Tables 5.1, 5.4, 5.6, 5.7, 5.13 to 5.17, 5.22); E_GCTRS/E_GCTRSNS; the type gate; the face wiring; the notify slots and window; K9 to K16 byte-exact runs; F4 recorded as a suggestion | R443-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| RTL | CLEAN | `KL_adp_engine.sv` and `protocol_processor_top.sv` diff; base reader analysis of the removed tick; focused lint; adp_engine and pp_top builds; OOC record (by construction) | R443-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| Robustness | CLEAN | the tie-off row; hold, watchdog and wrong-object rules; the slotless-strobe rule (probe P3, F2 suggestion); window-shortening probes P1 and P2 killed; redundancy keying | R443-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| Tests | CLEAN | `counters_phases.hpp`; the harness store changes in `sim_main.cpp`; the K4c/K4d updates; `ctr_mutants.py` and its 13 patches (re-run); the adp_engine removal of 39 checks (re-run at base and head; campaign re-run); F2 and F3 suggestions | R443-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| Docs | UNCLEAN | 00 §5/§7 and REQ rows; 01; 02 §1, §4 to §6, F02.1/F02.9/F02.10; 03; 04; 05; 06 §6.6/F06.15; 07 F07.10/§6; 08; 09 §8.6; the integrator guide §7 and §7.1; the tb READMEs (merge); `syn/ooc` README; F1 open (MINOR); F5 and F6 residue | R443-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |

## Real limits

- The specification texts are not distributed with the repository and were not available to this review. Clause and table numbers were judged against the repository's own quotations, the code, and the published design table, not against the standard text. That includes the IEEE table numbers 7-152 to 7-159 and Milan's observation-interval wording for the interval counters.
- The out-of-context synthesis was not re-run (heavy build). The zero delta is accepted by construction: the removed flop had no load at base.
- The parent repository was not built or run. Its consumer set (16), the donor bank (9), and the adoption patches c4c6 then c8 are manager duties. A code search of the parent's default branch for the removed tick found no hits, but that does not cover `dev`.
- The full processor sweep (`run_suites.sh`), full lint, the remaining mutation campaigns, and the hosted/act jobs were not run here, per the review's scope. The manager's banks are the source for those.
- The published evidence tree for this head (`review-evidence/ppC7-r1`) contains the author's material only. This review did not find the manager's bank receipts there.
- Physical calibration was NOT RUN, and no hardware claim is made.

## Pending manager duties

- Carry F1 to the author and re-review after the fix. Carry F5 and F6 to the residue checklist. F2 to F4 are optional.
- Run the donor bank (9) and the parent consumer set (16) at this head with parent-adoption-c4c6 then c8, and publish the bank receipts for this head.
- Build the final current-dev candidate at the merge turn (source base c74711d, live dev cdf49d1a), and own hosted/act acceptance.

R443-1 FINISHED
