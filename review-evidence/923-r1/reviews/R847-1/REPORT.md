[R847] NEGATIVE - exact head 70c100da36330bb3862d76fa6eb003091775f310

# R847-1: internal cleared-context review of PR #931 (issues #923 and #924)

- Head `70c100da36330bb3862d76fa6eb003091775f310`, tree `9be8e9f218622a0e65053d6b99cf0b54dce2eae0`, delta `16ba667d..70c100da` (ten commits).
- All five lenses applied. Conformance, RTL and Robustness are clean. Tests and Docs each carry one open MINOR, so the verdict is NEGATIVE.
- The change itself is sound:
  - the EDIT transaction matches the release processor's;
  - all or none holds on every refusal and silence path I traced;
  - #924 is right;
  - every gate and measurement I re-ran reproduced the author's receipts exactly.
- The two MINORs are a test that cannot fail for one face defect, and one wrong figure in a README. Each is a one-line fix.

## Reconstruction (public state only)

- **Sources read:** AGENTS.md, CONTRIBUTING.md sections 3, 5 and 6, and docs/README. Issue #923 and #924 bodies. On #923: TAKEN 6904937191, STOP 6906644789, ruling 6906679024, STOP 6922227027, ruling 6923091710, and REVIEW READY 6928332881. The PR #931 body, `docs/reference/MAILBOX_CONTRACT.md` (EDIT window and field tables), `docs/design/MAILBOX_SPLIT.md`, the datapath's transaction server (`hdl/milan/milan_datapath.sv`, `amap_edit_validate`, beat detection, boot sweep) and `hdl/milan/mailbox/KL_mbx_cdc_window.sv`.
- **Release reference:** the transaction face and microcode (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:465-485, 2324-2424`; `hdl/aecp/ucode/gen_ucode.py:2195-2240`).
- **Then:** the full diff and history, and the author's receipts at archive `62ad61af` (the round-2 receipts, the sweep shards, the workflow table, routes and release, the budget files listed in `receipts/evidence-read/author-receipts-read.sha256`).
- **Prior public review findings on this PR:** none exist at this head. The PR carries only the two review-start comments (R847-1 and R848-1), so there is nothing to resolve or retain.

## Findings

### F1 - MINOR - Tests - the face's record selection (`pick`) has no test that can fail

- **Location:** `sw/firmware/ctrl/aecp/aecp_face.c:273`, `sw/firmware/ctrl/test/test_aecp.cpp:4285-4400` (the Face tests), `tb/verilator/milan_dp/twin_split.cpp:673`.
- **Authority and evidence:**
  - The core hands the face the mappings that change the map through `pick` (`aecp_maps.c:493-503`). Examples: an ADD's new mappings when some are already held, or a REMOVE's distinct mappings.
  - The face reads record k at `records + 8 * pick[k]`. Every Face test sends commands whose `pick` is the identity: all-new ADDs, or distinct REMOVEs.
  - The Core tests decode `pick` in the test's own mock (`test_aecp.cpp` `store()`), not through the face.
  - twin-maps sends no mixed edit either: a REMOVE of all eight, then an ADD of three new mappings.
  - **Probe:** I replaced the selection with `records + 8u * (pick != NULL ? k : k)`, so the face ignores `pick`. All 102 Core, Face and AppStore tests still pass, and the unplanted control passes too (`receipts/probes/unit-probe-pick.json`, `receipts/probes/face-pick-ignored.log`).
  - Branch coverage is 100 % for both arms of that line, so the ratchet cannot see this gap.
  - AGENTS.md section 6, `Tests`: "Each new test can fail for the defect it claims to detect".
- **Impact:** a later defect in how the face honours `pick` would ship green. Example: an ADD of {held A, new B} commits A in place of B. The store then misses B while GET_AUDIO_MAP shows it. That is #923's own failure: the render store and the firmware's map disagree.
- **Required outcome:** a test through the face (and so through the EDIT window) where `pick` is not the identity. Examples: an ADD of a held and a new mapping, and a REMOVE with a repeat. Assert the committed records, and that the store and GET_AUDIO_MAP agree. Optionally add a plant in `aecp_map_mutants.py` caught by name.
- **Verification:** the same probe (`scripts/r847_probe_mutants.py --only face-pick-ignored`) must turn that test red.

### F2 - MINOR - Docs - `plat/README.md` states the 8x8/1if image's overflow as 888 B; it is 1,280 B

- **Location:** `sw/firmware/ctrl/plat/README.md:111`. The text reads: "it plans 56.5 since #923, 888 B of `rom` past what 56.0 held".
- **Authority and evidence:**
  - 888 B was the image's spare at 56.0 before the change: base 130,184 B of the 131,072 B that 56.0 holds. The change adds 2,168 B.
  - The overflow past 56.0 is therefore 1,280 B, the figure the ruling uses (#923 issuecomment-6906679024), and the figure in `sw/litex/ctrl_memory.py:280-284` ("888 B of rom spare ... 1,280 B of rom") and `docs/design/SPLIT_CONTROL_MEMORY.md:148, 567`.
  - `plat_ledger.py` at this head links the image at 132,368 B (`receipts/memory/plat_ledger.log`), which is 1,296 B past 56.0 with that gate's own link.
- **Impact:** the README states a wrong debt figure for a product image's ledger entry.
- **Required outcome:** the sentence states the measured overflow, for example "1,280 B of `rom` past the 131,072 B that 56.0 holds (888 B were spare before #923's 2,168 B)".
- **Verification:** read `plat/README.md:111` against `ctrl_memory.py:280-284` and section 5 of the fit page.

### R1 - RESIDUE - Docs - a new source comment names a lane

- **Location:** `sw/litex/ctrl_memory.py:243`.
- **Authority:** the owner's comment rule of 2026-10-15. Source comments never show lane labels or names; a new instance in the delta is residue.
- **Evidence:** the new `#:` block reads "may overflow as debt owed to S14, which supersedes the 60.5 cap of 2026-11-12 until S14". The base block named only "hybrid XIP work (#665 decision D3)".
  - The new `owed` data string at line 280 ("lane S14, ...") is the ledger field whose documented content is the recovering lane (`owed: str  # the lane that recovers the tiles`). It is not a comment, so it is not counted.
- **Exact fix:** "may overflow as debt owed to the hybrid XIP work (#665 decision D3), which supersedes the 60.5 cap of 2026-11-12 until that work lands".
- Wording only: no figure, test or code changes. It does not leave Docs unclean.

### Suggestions (optional; no lens effect)

- **S1 (Tests):** `twin-maps-plants` plants only the edit-port cut. Under it, MAPS-SAVED passes (`receipts/twin/no-edit.log`), because the second boot composes a fresh edit port.
  - My probe cut the boot restore commit (`ctrl_app_aecp.c:262`). MAPS-SAVED then failed by name: "the saved map, restored at boot, reached the render store" (`receipts/probes/twin-maps-restore-commit-cut.log`). So the check is sound.
  - A standing `--plant no-restore` would make that permanent. At unit level, `restore-not-committed-at-open` already covers it.
- **S2 (Tests):** `kept()`'s `d->length >= 82u` (`aecp_maps.c:589`) is not pinned at its boundary. The `> 82u` probe survives (`receipts/probes/kept-length-boundary.log`); the test pins only length 81. A length-82 case would close it. Shipped descriptors are longer, so there is no product effect.
- **S3 (Tests):** twin-maps runs at 1x1 on STREAM_PORT_INPUT 0 only. The output port's edit path (DESC_STREAM_PORT_OUT, the output claim and reservation) is exercised on RTL by nothing in this delta; it is covered against the Face model only.
- **S4 (Robustness):** after an accepted commit-begin, an unanswered APPLY or FINISH beat is counted (`aecp_face.c:261`) and the edit still returns SUCCESS (`aecp_face.c:309-312`).
  - This mirrors the release processor's point of no return (`KL_aecp_engine.sv:469-471`). The datapath's only edit wait is the boot sweep (`milan_datapath.sv:4816`), so the path is unreachable after boot.
  - If a datapath stall is ever added there, the map and the store would disagree silently. The count could be surfaced (it already is in the twin's summary line) or asserted.

## The focus items, checked

1. **Transaction and all-or-none.**
   - The face runs begin, validate each record, commit-begin, commit each record, then finish. Any refusal or silence before commit-begin aborts. Phase, REC, COUNT, REMOVE and the record halves match `MAILBOX_CONTRACT.md:369-378, 534-553`, and the beat order and status mapping match the release microcode (`gen_ucode.py:2205-2235`: refused begin NOT_SUPPORTED, refused record or commit-begin BAD_ARGUMENTS, abort in both).
   - The store is asked before the map moves (`aecp_maps.c:501-508`). A refusal returns its status with no map change and no notice.
   - Late answers: `KL_mbx_cdc_window.sv` ("a newer request wins") plus the abort after every failure means a timed-out begin, record or commit-begin reaches the store only as begin, possibly a validate, then abort. Nothing is applied.
   - Boot restore (`aecp_maps.c:643-657`): every moved port's clipped reset set is removed first, then each restored set is added. Each fallback leaves the firmware's map equal to what the store holds: the reset set on a refused removal; the reset set, or none, on a refused add. This is consistent with the datapath's boot clip (`milan_datapath.sv:4855-4895`) and with the split having no datapath map restore (`g_sp_amr`, `amr_own_r = 0`).
   - A LiteX soft reset resets the datapath domain with the CPU (shared CRG reset, `milan_soc.py:282-293`), so the restore's assumption that the store holds its power-on image holds.
   - Clean apart from S4.
2. **No RTL or contract change.**
   - The delta touches nothing under `hdl/`, the processors or the mailbox contract, and no `.sv`, `.v`, `.xdc` or `.yaml` file. The gitlinks are identical (`receipts/clone-state.txt`).
   - `twin_probes.vlt` is read-only `public_flat_rd`.
   - `mbx_win_ask` writes only request words `from .. to-1`, clamped to the window (`mbx.c:397-410`).
   - The EDIT beats write REQ and BEAT on begin, BEAT and the record halves on record beats, BEAT alone otherwise, and never the value lane; this is asserted by `Face.AnEditIsTheReleasesTransactionOnTheEditWindow`.
3. **#924.**
   - `aecp_commands.c:192-194`: an index at or past configurations_count answers NO_SUCH_DESCRIPTOR (IEEE 1722.1-2021 7.4.7.1).
   - `aecp_commands.c:363-366`: a SET accepts exactly 48 or at least 84 octets, refuses 49 to 83 and anything under 48, and answers in the 84-octet body. The SET reads only offsets 4 and 24, both inside the 48-octet 2013 body.
   - Bodies past 84 are still taken: #926, known.
4. **Tests.**
   - 14 new GoogleTest cases. The plant rows add up to 27 in `aecp_map_mutants.py`, 2 in `aecp_mutants.py` and 1 in `aecp_configuration_mutants.py`: 30, matching the PR.
   - My AECP campaign: 329 of 329 caught. Control: 716 of 716. SRP: 421 of 421. Suites shard PASS, the AECP app arm 161 tests at one and two interfaces (`receipts/firmware/`).
   - Coverage `--check` PASS, 39 files. The six changed files are at 100 % lines and branches after the one pre-existing documented exclusion in `mark` (`receipts/firmware/fw_coverage.log`).
   - twin-maps: 20 checks PASS. twin-maps-plants: the no-edit plant caught on its three phrases (`receipts/twin/`).
   - My probes: 4 of 6 caught (`receipts/probes/unit-probes.json`). The kept-length boundary survived (S2) and the `pick` probe survived (F1).
5. **Ledger.**
   - `ctrl_memory.LEDGERED` holds 8x8/1if `platform-8x8-one-interface` at 56.5 by `nvm_stage` 13,594 B and `ctrl_plat` 18,240 B, and the two 8x8/2if entries at 59.5 and 61.0 (`ctrl_plat` 20,416 B).
   - `own_point` matches every symbol at its listed size.
   - `test_ctrl_memory.py`: 0 failures. Its arms include the product build planning each ledgered image at its own entry, refusing each half a tile past its entry, and refusing an unledgered 8x8 image at 56.5, both with another `ctrl_plat` and with none. Three new mutants are caught.
   - `plat_ledger.py --self-test`: PASS at four points, 7 of 7 controls (`receipts/memory/`).
6. **CPU budget.** I re-measured the edit legs on my own builds (`receipts/budget/`). Each figure matches the author's receipt to the cycle:

   | Point | Record | Cycles | Cost by the rule | Stated |
   |---|---|---:|---:|---:|
   | 1x1/1if | one-row edit | 27,866 | 295 us | 300 us |
   | 1x1/1if | largest legal command | 92,714 | 975 us | 975 us |
   | 1x1/1if | accepted SET_CONFIGURATION | 28,076 | 295 us | - |
   | 8x8/2if | one-row edit | 33,481 | 355 us | - |
   | 8x8/2if | largest legal command | 132,751 | 1,395 us | 1,650 us |

   - 0 budget misses and 0 refusals at both points.
   - At 8x8/2if, 2 of 140 largest-notice passes are over THE SHARE, the same as the base (section 13). At two interfaces every edit answered SUCCESS, which confirms the harness fix.
   - `edit_rows.PACED` moves its members only: `EDIT_RECORD_US` stays 300 and 595, and `rows_tiers.py` and `LONG_RECORD_US` are unchanged across the delta. So the tier model's inputs are unchanged.
   - Firmware sources are byte-identical between `def26a61` (where arm A was measured) and the head.
   - I did not re-run full arm A, `record_classes.py` over every leg, or the seven `backlog-owed` rows; those are the author's receipts.
7. **Timing and release.** Inspected, not re-run.
   - Route receipts: 8x8/1if meets WNS and WHS of at least +0.030 ns on all three directives. 1x1/1if holds at +0.014 to +0.015 ns at the fast corners, as its base does at +0.014 on the TDM render FIFO crossing. That is owed to #927 by ruling 6923091710, and is not a finding.
   - Release: `bios.bin` byte-identical at `679b4a44`. `git diff --stat 679b4a44..HEAD` touches only docs, firmware tests, the coverage ratchet and the CPU budget harness, none of which the all-fabric recipe reads.
8. **Gates.** Inspected, not re-run.
   - Workflow receipt `verify-70c100da.md`: 118 ran, 130 not run with reasons, 0 bad.
   - Sweep shards: 15, 17, 17 and 16 suites, 65 PASS, 2,713,040 checks, each exit 0.
   - I re-ran locally: the four firmware shards, coverage, the memory and ledger gates, twin-maps and its plants, `docs_check.py` (0 findings) and `gen_toc.py --check` (OK). Results are above.

## Per-lens results

[R847] PASS Conformance - `sw/firmware/ctrl/aecp/aecp_maps.c:490-520`, `aecp_face.c:243-314`, `aecp_commands.c:188-195, 359-366` - the EDIT transaction and its statuses against the release microcode (`gen_ucode.py:2195-2240`) and `MAILBOX_CONTRACT.md:369-378, 527-590`; all or none (Milan v1.2 5.4.2.27, 5.4.2.28) on refusal, silence and boot-restore paths; 5.4.2.7 on RTL (twin-maps MAPS-REFUSED and MAPS-FORMAT); #924 against IEEE 1722.1-2021 7.4.7.1 and the 2013 7.4.15 48-octet layout. No finding.

[R847] PASS RTL - `hdl/milan/milan_datapath.sv:4760-4900, 5011-5050, 5115-5175, 5646, 6140-6160`, `hdl/milan/mailbox/KL_mbx_cdc_window.sv`, `KL_mbx.sv:690-720`, `tb/verilator/milan_dp/twin_probes.vlt` - no RTL, contract or gitlink change in the delta; the firmware's use of the edit face (phase encoding, per-beat request edges, `rec < count[7:0]` with AECP_MAP_PAGE 176, the boot-sweep wait and the retried begin, a newer request winning at the crossing) is consistent with the RTL; the probe is read-only. No finding.

[R847] PASS Robustness - `aecp_maps.c:585-657`, `aecp_face.c:249-314`, `mbx.c:392-415`, `sw/litex/ctrl_memory.py:288-292`, `milan_soc.py:3344-3345` - core refusals never reach the store; store refusals change nothing; silence before commit-begin aborts; late answers cannot apply; restore fallbacks match the store; a CPU and datapath reset is shared; `own_point` cannot match two entries, and unledgered images stay at 56. SUGGESTION S4 only.

Tests: UNCLEAN. F1 (MINOR) is open. The artifacts examined are in focus item 4 and `receipts/probes/`.

Docs: UNCLEAN. F2 (MINOR) is open, and R1 is residue. Examined: `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 13, `MAILBOX_SPLIT.md:1467-1478, 1518-1522, 2131-2136`, `FR_NFR.md:383`, `sw/firmware/ctrl/aecp/README.md:174-203`, `plat/README.md:107-113, 132-135`, `ctrl_service_budget/README.md:46-64`, `milan_dp/README.md:1744-1770`, `ctrl_split_boot/README.md:140-150`, and `docs_check.py` and `gen_toc.py --check`.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_maps.c`, `aecp_face.c`, `aecp_commands.c` against `MAILBOX_CONTRACT.md` EDIT, release `gen_ucode.py` and `KL_aecp_engine.sv`, Milan v1.2 5.4.2.7, .27, .28, IEEE 1722.1-2021 7.4.7.1, 2013 7.4.15; twin-maps on the split RTL | R847-1 | `70c100da36330bb3862d76fa6eb003091775f310` |
| RTL | CLEAN | `milan_datapath.sv` edit server, boot clip and sweep, split amr stub; `KL_mbx_cdc_window.sv`; `KL_mbx.sv` EDIT window; `twin_probes.vlt`; delta path and gitlink check | R847-1 | `70c100da36330bb3862d76fa6eb003091775f310` |
| Robustness | CLEAN | refusal, silence, late-answer, partial-commit and boot-restore paths in `aecp_maps.c`, `aecp_face.c`, `mbx.c`; `own_point` and `add_ctrl_memory`; reset domains in `milan_soc.py` | R847-1 | `70c100da36330bb3862d76fa6eb003091775f310` |
| Tests | UNCLEAN (F1) | `test_aecp.cpp` 14 cases; 30 plant rows; campaigns 329, 716, 421 re-run; coverage re-run; twin-maps and plants re-run; 6 reviewer probes plus 1 twin probe; `test_ctrl_memory.py`, `plat_ledger.py` re-run | R847-1 | `70c100da36330bb3862d76fa6eb003091775f310` |
| Docs | UNCLEAN (F2; R1 residue) | the pages listed under Per-lens results; `docs_check.py`, `gen_toc.py --check` re-run | R847-1 | `70c100da36330bb3862d76fa6eb003091775f310` |

## Real limits

- Not run by me: Vivado routes, the release image rebuild, the 118-step clean-clone workflow pass, the 4-shard native sweep, the full arm A and 8x8/1if budget runs, `record_classes.py` over every leg, and the `load_grade` and `flip_grade` checks. For each of these I inspected the author's receipts only.
- twin-maps covers 1x1 and the input port only (S3).
- No hardware, bench or physical calibration was run; field skips are not hardware proof.
- I did not run a manager source bank at this head and do not infer one.
- Hosted exact-head checks when I read them: 4 complete (success), 6 in progress, 14 queued (`receipts/evidence-read/hosted-checks-70c100da.txt`).
- The host was shared and loaded (load average 45 to 75) during my runs; no run of mine was cut.

## Pending manager duties

- The hosted exact-head contexts and the local replica acceptance.
- The current-dev merge candidate (source base `16ba667d`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`), with builder and native banks and post-merge containment.
- The bench acceptance of #923 (a narrowing SET_STREAM_FORMAT with the mappings in place, and 1, 2, 4 and 6 channels once they are removed; persistence; render) and of #924.
- Carry R1 to the residue checklist.
- Re-review of the fixes for F1 and F2 at the head that carries them.

R847-1 FINISHED
