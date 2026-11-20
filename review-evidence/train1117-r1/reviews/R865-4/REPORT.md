[R865] NEGATIVE - exact head 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd

Round R865-4, internal cleared-context review of PR #945 (the flip train), composition delta `0839453f..8dc85884`
(tree `22335ec4d79d67a5b9a2e0e7ab480fd868be9bba`). All five lenses were applied independently. Four lenses are CLEAN.
Docs is UNCLEAN on two MINOR findings: the PR body's figure and evidence claims about the final head, and an unpublished
receipt for the gating images' firmware identity. Neither touches code, tests, statements or measured figures. The
firmware logic of the delta (F-G5 and the SRP cut), the item-4 restatements, the rules' application and the figures all
hold. Wording residue and suggestions are listed for one-pass absorption.

## Verdict basis in one paragraph

- Steps 13 and 14 equal their frozen heads and are carried line for line: `a16899b1` = #953 head and `f09d82e0` =
  #952 head, both ancestors of the head. 20+2 and 7+3 files match, and both merges touch only the PR's files.
- F-G5 (`01765bb0`) is correct against the RTL's boot clip and the restore's own settle step.
- The SRP cut (`92de01f7`): each of the four claimed equivalences holds for every lwSRP Applicant/Registrar path the
  firmware can reach. Its differential against the pre-cut adapter and its 10 plants catch what they claim to catch.
  Two extra reviewer probes that were not planted are covered or provably unreachable.
- Item 4 (`8c5e2b4f`) restates exactly the owner-allowed statements by the rule. (950 us, 130 ms) is the unique
  fixed point of the slice rule and the queued rule. The re-anchored controls still refuse their plants and still catch
  a blinded detector.
- At head, my own runs of the checks reproduce the rows (127.31/130, 29.06/30, 47.88/49), the loads (0.511, 0.744) and
  the base's eleven 8x8/2if findings.
- The image-identity and gate receipts support the carried 8x8/1if figures.
- Open MINORs: the PR body still presents pre-cut figures, and a pending full measurement, as the final head's (F1).
  The gating ELFs' loaded-section identity and the release-export identity at `8c5e2b4f` are asserted with no published
  receipt (F2).

## Findings

### R865-4-F1 — MINOR — Docs — PR #945 body: figures and evidence state attributed to the final head are not the final head's

- **Artifact:** the PR #945 body as published at review time (the body equals `author-r6/PR-BODY.md` but for the
  packet link line):
  - line 182, "Composed figures at the final head";
  - line 186 (1x1/1if row): "ACMP 29.93 of 30 ms, txL 48.89 of 49, the last queued notice 137.97 of 140; the load 0.522
    of 0.70; the paced record 310 of 310 us";
  - line 187 (8x8/1if row): "the SRP record 35,547 cycles", the `unit375` image's figure;
  - line 190, "Restated at the final head", and line 192, "1x1/1if: the paced record 310 us";
  - lines 440-446, Known limitations: "The CPU budget at `01765bb0` is confirmed on a sample, not re-measured … Pending:
    the full measurement";
  - line 447: "The gating bench run is on `7650a02d`'s bitstreams. The final head `0839453f` …".
- **Authority/evidence:**
  - AGENTS.md section 6, Docs lens: the PR must carry enough evidence for another cold reviewer.
  - The owner's RESIDUE rule excludes defects that change a figure or a verdict claim.
  - At `8dc85884` my own `flip_grade.py --check --point 1x1/1if` gives last 127.31 of 130, ACMP 29.06 of 30 and txL
    47.88 of 49 (`receipts/sel_flip_grade.py_--check_--point_1x1_1if.txt`), and `load_grade.py --check` gives 0.511
    (`receipts/sel_load_grade.py_--check.txt`).
  - `edit_rows.PACED['1x1/1if']['a one-row edit']` is 315, and the full measurement was made at `92de01f7` (8x8/1if)
    and `8c5e2b4f` (1x1/1if) (`CPU-TABLE-92de01f7.md`, `CPU-TABLE-8c5e2b4f.md`).
  - The gating bitstreams are of `8c5e2b4f` (`receipts/step16/gating/`).
  - The body's own Status section (lines 16-37) and its "Expected result" (lines 423-429) state the right figures, so
    the body contradicts itself.
  - The figures at lines 186-192 are `c1e95dc1`'s (the STOP measurement) and `unit375`'s, not `0839453f`'s, so line
    43's caveat ("the step-12 figures below are `0839453f`'s") does not rescue them.
- **Impact:** a cold reader of the sections titled "at the final head" takes the pre-cut rows, load, paced statement and
  SRP record as the merge candidate's. The reader also takes the full measurement as still pending and the gating run
  as on old bitstreams. No code or test is affected. These are figure and evidence claims, so this is not RESIDUE.
- **Required outcome:**
  - Either restate lines 182-200 at `8dc85884`, or retitle them to the head they describe.
    - 1x1/1if at the head: last 127.31 of 130 (owner 140), ACMP 29.06 of 30, txL 47.88 of 49, load 0.5114 of 0.70, the
      paced record 315 of 315.
    - 8x8/1if at the head: `record.srp` 34,803 cycles within 375, load 0.7436 of 0.75.
    - "Restated at the final head" then lists item 4's six statements (notice item 150, long notice 315, map edit 315,
      SET_STREAM_INFO 250, ADP record 105, centisecond 170) and `CTRL_LOOP_SLICE_US` 950 and `CTRL_LOOP_QUEUED_MS` 130.
  - Replace the two Known-limitations bullets (lines 440-449) with the current state: the full re-measure is done; the
    gating bitstreams are `8c5e2b4f`'s; the bench re-check is pending.
- **Verification:** the body's every "final head" figure equals `flip_grade.py --check --point`, `load_grade.py
  --check` and `CPU-TABLE-8c5e2b4f.md`/`CPU-TABLE-92de01f7.md` at `8dc85884`. No Known-limitations bullet names a
  superseded head as the final one.

### R865-4-F2 — MINOR — Docs — the gating images' firmware identity and the release-export identity at `8c5e2b4f` are asserted with no published receipt

- **Artifact:**
  - `author-r6/RESOLUTIONS.md` line 781: "Their loaded firmware sections equal the ledger's link of the head's
    product images".
  - `author-r6/RESOLUTIONS.md` "Release export: byte-identical where loaded" under `8c5e2b4f`.
  - `author-r6/HANDOFF-r5.md` lines 96-98 and 111 (1x1/1if `1fd5bc47…`, 8x8/1if `ac014c6a…`, `bios.bin`
    `603b9ca3…`).
- **Authority/evidence:**
  - AGENTS.md section 6, Docs: the evidence must let a cold reviewer disagree.
  - The packet's `receipts/step16/gating/{1x1,8x8}/artifacts.sha256` give only whole-file hashes of the gating ELFs
    (`c873a0aa…`, `d67fd049…`). These differ from the head's product images in `receipts/step16/images/product-images.txt`
    (`fe12a3f1…`, `c6355962…`), as expected for a link against the build's own CSR map.
  - No published file compares their loaded sections. The 1x1/1if loaded hash `1fd5bc47…` appears in no receipt;
    `ac014c6a…` is receipted only for the product image (`receipts/step15/images/images-17.txt`).
  - `receipts/step16/gates/rel.log` holds only "export done: 3876 files", with no comparison.
  - The bitstreams' #818 floors and identity gate are receipted (`signoff.txt`, `identity.log`). The gating builds'
    source head is printed only in logs kept in scratch.
- **Impact:** the claim that the bench bitstreams run the head's firmware cannot be checked from public state. That claim
  lets bench results stand for this head. So does the release image's byte identity at this head.
- **Required outcome:** publish the loaded-section (`.text`, `.rodata`, `.data`) comparison of each gating ELF against
  the head's product-image link, with both hashes. Publish the gating builds' clone head and porcelain line, and the
  release-export comparison at `8c5e2b4f` (or `8dc85884`). Alternatively, the manager's candidate validation supplies
  equivalent receipts and the PR links them.
- **Verification:** a published receipt names the gating ELF's loaded hash equal to the product image's at both points,
  and the release export's `bios.bin`/AEM/ROM/SRAM init hashes equal the prior head's.

### R865-4-R1 — RESIDUE — Docs — issue-comment IDs added in source comments by the delta

- **Artifact** (12 lines in 9 files, all added by `8c5e2b4f`):
  - `sw/firmware/ctrl/aecp/aecp_mbx.h:77`;
  - `sw/firmware/ctrl/loop/ctrl_loop.h:218,283,344`;
  - `tb/verilator/ctrl_service_budget/load_grade.py:219,273`;
  - `notice_window.py:69`;
  - `shape_costs.py:408,513`;
  - `selftest_notice.py:115` (a check's text);
  - `edit_rows.py:51`;
  - `poll_grade.py:108`.
- **Authority:** the owner's source-comment rule (2026-10-15).
- **Impact:** wording only.
- **Exact fix:** replace "#665 issuecomment-7044585511" with "#665's owner decision of 2026-11-20 (item 4)"
  everywhere. Where "(the owner's decision of 2026-11-20, #665 issuecomment-7044585511)" appears, write "(#665's owner
  decision of 2026-11-20)". Keep the dates and item numbers.
- **Verification:** `git grep -n issuecomment-7044585511 -- '*.c' '*.h' '*.py'` prints nothing; the self-tests'
  check names change only in that text.

### R865-4-R2 — RESIDUE — Docs — a reviewer finding ID in step 13's harness

- **Artifact:** `tb/verilator/ctrl_service_budget/declaring_outputs.py:296` (docstring, "R872-1-F2") and `:323` (a check
  string, "R872-1-F2's").
- **Status:** step 13's own content (#953 at `a16899b1`), carried unchanged. It is recorded for the residue checklist,
  not re-reviewed.
- **Exact fix:** drop "R872-1-F2" and "(R872-1-F2's)", keeping "a brief observation that leaves it cleared is
  completed".
- **Verification:** `git grep -n "R872-" tb/` prints nothing.

### Suggestions (optional; no lens effect)

- **R865-4-S1:** the declaring-outputs arm's reported-not-held records at the final head.
  - At 1x1/1if, a paced REMOVE_AUDIO_MAPPINGS that ran no completion measures 30,839 cycles: 325 us by the rule, against
    the held 315 (`CPU-TABLE-8c5e2b4f.md`, "REPORTED").
  - At 8x8/1if the declaring arm's long records are 1765 and 1725 us by the rule, against 1720 (`CPU-TABLE-92de01f7.md`).
  - Each is under its statement measured and outside the held set by #943's approved design (`record_classes.held`).
    RESOLUTIONS states at `c1e95dc1` that holding the reported edit would put the 1x1/1if last row at 141.47 ms.
  - Suggest stating the same "if held" row at the final head in the PR body, so the owner sees the margin the class
    rule carries.
- **R865-4-S2:** `SRP_FREED_APPL`'s AO and QO bits (`srp_mbx.c:513`).
  - In lwSRP's tables (`mrp_mad.c:149-290`, `reg_table`) a Registrar at MT with an Applicant at AO or QO is reachable
    only through Flush. The firmware never calls `mrp_port_role_change`.
  - So my planted removal of either bit survives every SRP suite at both shapes (`receipts/probe_ao-dropped.txt`,
    `probe_qo-dropped.txt`, `probe_ao-qo-dropped.txt`). The bits are correct and match `mrp_reclaim` exactly.
  - Suggest a comment saying they are kept for exactness with `mrp_reclaim` and unreachable without a Flush.
- **R865-4-S3:** `srp_rx_retry.cpp` at 8x8/1if.
  - The suite is run at 1x1/1if only. There it catches my "medium class only" probe of `attribute_room`
    (`receipts/probe3_room-medium-only_srp_rx_retry.cpp.txt`), which no other suite catches.
  - At 8x8/1if its `DomainFloodCannotDelayLaterRapidLeave` fails on the clean tree (`rx_discarded` 0), because the
    larger pool never exhausts (`receipts/probe3_control_srp_rx_retry.cpp.txt`). This is pre-existing: the suite is
    unchanged by the delta and is not gated at 8x8.
  - Suggest a shape-sized flood, so the large-class term is also held at 8x8/1if.
- **R865-4-S4:** `docs/design/SPLIT_CONTROL_MEMORY.md:3228`, "What is left". It still says 1x1/1if "0.519 at the pin"
  and 8x8/2if "0.798" "at this head". Both were stale before the delta (the same line at `0839453f`); the head gives
  0.511 and 0.799. Suggest a refresh when `8dc85884`'s edit of that section is next touched.

## Lens results (clean lenses in findings format)

```text
[R865] PASS Conformance — sw/firmware/ctrl/aecp/aecp_face.c:211-230, aecp_maps.c:570-606,668-682, app/ctrl_app_aecp.c:290-300, hdl/milan/milan_datapath.sv:4930-4960,5070-5082,5300-5320,6550-6577 — F-G5: before the face opens the verdict's bit 1 reads the store's pre-clip reset set, so a restored narrowed input is judged supported alone. The core's restore and settle then clip orphaned rows. From the open on the low byte must be exactly 3 (Milan v1.2 5.4.2.7 SET_STREAM_FORMAT's orphan refusal, the RTL's sfv verdict). The format port is reached before the open only by the restore (aecp_commands.c:292, aecp_nvm.c:90). Item 4: the six restated statements are exactly the owner decision's (#665 owner decision 2026-11-20) and each equals measured +5 %, rounded up to 5 us (14,084→150, 29,652→315, 29,993→315, 23,726→250, 9,585→105, 15,976→170). (950 us, 130 ms) is the unique fixed point of rows_tiers.ruled and queued_bound.ruled: from (900,140) the rules iterate 140→900→135→950→130 (receipts/probe_fixed_point*.txt). Owner bounds unchanged: rows_grade/rows_tiers bounds, loads 0.70/0.75, last 140 (MOST_MS), ACMP 30, txL 49 (receipts/sel_flip_grade*.txt).
[R865] PASS RTL — sw/firmware/ctrl/srp/srp_mbx.c:96-106,205-220,430-467,487-531,843-903,988-1066 against third_party/lwSRP/src/core/mrp_mad.c:467-501,506-523,618-760,876-880,946-1076,1103-1122 and port/ctrl_pool.c:135-197 — every claimed equivalence holds. sources_of's byte-7 prefilter precedes the same full compare, its ≤16-source mask fits (mbx_contract.h:33), and no loop body moves a source's StreamID. The filter's sink pass is a no-op while not stale, because listener_kind's inputs change only in talker_changed and srp_mbx_bind, which both set stale, and the entry snapshot leaves desired == listener_kind. moved() owes the reclaim on every observed change into mrp_reclaim's exact condition; observe() always reports full to-states, and the only unobserved creation is get_or_create_attr's (VO, MT). apply_receive's room count is exact: attributes are 176 B on RV32 (medium), map works are freed in-event (n_ports 1, MVRP has no map hooks), mrp_rx frees nothing else, and fresh's uint8 wrap only over-reclaims (receipts: sizes from scripts/sizes.c). No HDL is in the delta (git diff --stat 0839453f..HEAD).
[R865] PASS Robustness — srp_mbx.c:853-903 (refused receive, partial NO_MEMORY), :1249-1258 (owed frame), aecp_face.c:228 (before/after open), test_plat_sinks.cpp S12 power cut — pool exhaustion: the large-class term is exercised and its removal caught by srp_rx_retry.cpp at 1x1/1if (receipts/probe3_room-medium-only_srp_rx_retry.cpp.txt). A refused receive's created attributes are still counted. The reclaim stays owed while a frame is owed (unchanged). The F-G5 open boundary is tested both sides with out-of-range verdicts 2, 5 and 0x103 (test_aecp.cpp:5346-5363). The restore across a power cut is tested at both shapes, with the far store reseeded.
[R865] PASS Tests — sw/firmware/ctrl/test/srp_listeners.cpp (reference-reclaim differential, 4 named tests), srp_reclaim_mutants.py (10 plants), srp_compare_mutants.py/srp_kind_mutants.py (fb083864's 2 re-targets), aecp_face_mutants.py/sink_mutants.py (F-G5's 3 plants), flip_grade/rows_tiers/shape_costs/selftest_notice re-anchors — my probes: a prefilter on the wrong byte is caught (receipts/probe_prefilter-byte6.txt), and a medium-only room count is caught at 1x1/1if (probe3). The re-anchored THE TRANSMIT control escapes a detector blinded by one ms and stays clean on the tree's (receipts/probe_blind_tx.txt). Self-tests run at head: flip 616/616, rows_tiers 1033/1033, shape_costs 25/25, load 28/28, record_classes 26/26 (receipts/sel_*). The author's shard receipts: 826/826 caught, the four shards rc 0 (receipts/step16/gates/fw*.rc, fw1 "mutants: 826 of 826 caught"); twin, avtp_rxmon, both boot simulations, ctrl_boundary ×2 and ledger 9/9 pass. The exception sets equal 01765bb0's exactly (flip_check without --point, ci_tool_inventory, the docs workflow's environment rows). The flip check at all points reproduces the base's eleven 8x8/2if OVER lines (receipts/sel_flip_grade_all_points.txt).
```

```text
[R865] MINOR Docs — PR #945 body lines 182-192, 440-449 — R865-4-F1 (above)
[R865] MINOR Docs — author-r6 RESOLUTIONS.md:781, HANDOFF-r5.md:96-98,111; receipts/step16/gating, gates/rel.log — R865-4-F2 (above)
```

Docs was also applied clean where it holds. FR_NFR.md 3.4.1 states the 140 ms owner bound and the 130 ms statement.
SPLIT_CONTROL_MEMORY.md's notice-path section and `8dc85884`'s "What is left" state 950 us and 130 ms. The
srp/aecp/plat READMEs and MAILBOX_SPLIT.md describe the cut and F-G5 as built. `docs_check`, `check_py_idiom`,
`check_hygiene`, `docs_inventory --check` and `fw_coverage --check` pass at head (receipts/doc_*). `gen_toc` could not
run here (no html5lib); the author's receipt passes (`receipts/step16/gates/q.log`).

## The delta's composition checks

- **Frozen heads.** The PRs' metadata gives #953's head `a16899b1` and #952's head `f09d82e0`. Both are ancestors of the head
  and both are merged by `c05d5acb` and `4b9f66c5` (second parents).
- **Carried line for line** (`scripts/carried.sh`):
  - #953: 20 files equal and 2 shared files with every added line of both sides present.
  - #952: 7 equal and 3 shared, likewise.
  - Neither merge touches a file outside its PR's (`receipts/carried_step13.txt`, `carried_step14.txt`,
    `merge_scope.txt`).
  - Neither merge had a conflict, as RESOLUTIONS states, and every auto-merged shared file keeps both sides.
- **`c1e95dc1`.** `sink_mutants.py` and `talker_notice.py` compile nothing, and their `OUTSIDE` entries are accurate.
- **`fb083864`.** Both re-targeted plants are caught in the author's campaign, 826/826.
  - The Failed-first copy plant is caught by the differential, because the reference run recomputes at every filter
    call and the cut only once stale.
  - `same`'s skipped last byte is caught under a Talker's near miss, now that `sources_of` masks it for Listeners.
- **Image identity.**
  - At `fb083864` vs `8c5e2b4f`, the 8 CPU-budget images at 8x8/1if and 8x8/2if are hash-equal. The 4 at 1x1/1if differ
    only in five immediates: 900→950 and values derived from it, with sections, symbols and data equal.
  - Product images `1x1-if2`, `8x8-if1` and `8x8-if2` are equal, and `1x1-if1` differs in the same immediates
    (`receipts/step16/images/*`).
  - `fb083864` changes tests only, so its images are `92de01f7`'s. `8dc85884` changes one doc, so `8c5e2b4f`'s images
    are the head's.
  - So 8x8/1if's `92de01f7` measurement carries: 0 of 68 exceeded, `record.srp` 34,803 cycles (370 by the rule, ≤ 375),
    `item.reclaim` 995 (≤ 40), load 0.7436, which my `load_grade --check` gives as 0.744.
  - My `flip_grade --check` recomputes the 1x1/1if figures from the tree's statements, which the CPU-TABLE's
    measurements bound: 0 of 68 exceeded, and every measured cost's rule ≤ its statement.
- **Gating bitstreams of `8c5e2b4f`.** They meet #818's floor at every corner: 1x1/1if WNS ≥ +0.131 and WHS ≥ +0.036
  ns; 8x8/1if WNS ≥ +0.176 and WHS ≥ +0.036 ns. The identity gate passes (`signoff.txt`, `identity.log`). Their
  firmware's identity to the head's product images is F2.

## Prior public findings at this head

- **R866-1-R1:** RESIDUE, Docs, RETAINED. `sw/firmware/ctrl/test/test_plat_boot.cpp:91,95,116,119` still carry B24/Phy
  and L5/L6 labels. The file is unchanged in the delta.
- **R866-1-R2 / R865-1-RES-2:** RESIDUE, Docs, RETAINED. `sw/firmware/ctrl/plat/ctrl_split_hot.txt:14,19` still carry
  `issuecomment-6959600243` and `issuecomment-6967930396`. Unchanged.
- **R865-1-RES-1:** RESIDUE, Docs, RETAINED. `docs/design/AREA_BUDGET.md:139,141` still name the superseded record and
  ExtraPostPlacementOpt. Unchanged.
- **R866-2-R1:** RESOLVED at `0839453f` by R866-3, and not reintroduced.
- **R866-3-R1:** RESIDUE, Docs, RETAINED/OPEN. PR body line 470, "The release export comparison … was last made at step
  9", is still present. It sits beside F1's stale Known-limitations bullets but is kept as its own residue.
- No prior BLOCKER, MAJOR or MINOR was open on this PR.
- A review of this same head by the other internal session was posted during this round. It was not read, to keep the
  two reviews independent; it is not a prior-head finding. My verdict draft predates reading any prior finding
  (`receipts/verdict_draft_before_prior_findings.txt`).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_face.c`, `aecp_maps.c`, `ctrl_app_aecp.c`, `milan_datapath.sv` boot clip/verdict; item-4 statements in `aecp_mbx.h`, `ctrl_loop.h`, `load_grade.py`, `poll_grade.py`, `edit_rows.py`; `rows_tiers.ruled`, `queued_bound.ruled` (fixed-point probe); owner bounds | R865-4 | `8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd` |
| RTL | CLEAN | `srp_mbx.c`/`.h` cut vs `lwSRP mrp_mad.c` tables, observer, reclaim, rx, map paths; `ctrl_pool.c`; struct sizes; bitmask bounds; no HDL in the delta | R865-4 | `8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd` |
| Robustness | CLEAN | exhaustion and refused-receive paths, owed-frame reclaim, F-G5 open boundary and power-cut restore, probe3 | R865-4 | `8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd` |
| Tests | CLEAN | `srp_listeners.cpp` differential and tests; `srp_reclaim_mutants.py`; `fb083864` re-targets; F-G5 plants; six reviewer probes; re-anchored controls with a blinded detector; self-tests at head; author shard/gate receipts at `8c5e2b4f` | R865-4 | `8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd` |
| Docs | UNCLEAN (F1, F2 MINOR open; R1, R2 and the retained residues are RESIDUE) | PR #945 body; RESOLUTIONS/HANDOFF/CPU-TABLEs; FR_NFR.md, SPLIT_CONTROL_MEMORY.md, READMEs; docs checks at head | R865-4 | `8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd` |

Lenses outside the delta (steps 13 and 14's own content; steps 1-12) keep their prior verdicts:

| Prior covering round | Head |
|---|---|
| R872-2 / R871-2 POSITIVE | #953 at `a16899b1` |
| R869-1 POSITIVE | #952 at `f09d82e0` |
| R866-3 POSITIVE | `0839453f` |

The delta changes nothing they depend on but the measured figures, and those are re-established above. R870-2's
NEGATIVE on #952 rests on final-image CPU timing evidence. This round finds that evidence in the 8x8/1if (`92de01f7`)
and 1x1/1if (`8c5e2b4f`) full re-measures, but leaves its acceptance to R870's own re-check.

## Real limits

- I did not re-run the firmware shards, the twin, `avtp_rxmon`, the boot simulations, `ctrl_boundary`, the ledger or the
  CPU-budget measurement. For these I rely on the author's published receipts at `8c5e2b4f`; `8dc85884` is docs only.
- `run.py --self-test` exceeded my 590 s foreground limit (`receipts/sel_run.py_--self-test.txt`, rc 124 by timeout, no
  failure printed). The author's receipt reports 0 failures.
- `gen_toc --check`/`--verify-anchors` could not run here (no html5lib).
- No image or bitstream was rebuilt. Image identity rests on the author's receipts, and F2 names what is missing.
- Physical calibration was NOT RUN, and bench and field skips are not hardware proof.
- No manager source bank exists at this head. The current-dev merge candidate (source base `cb96336d`, live dev
  `e275d795…`) is not validated by this round.
- Hosted and act contexts were not inspected for acceptance.

## Pending manager duties

- Absorb F1 and F2 (PR body restatement; the gating-firmware and release-export receipts, or the candidate's
  equivalents), then re-review the Docs lens.
- Carry R865-4-R1 and R2 and the retained residues (R866-1-R1, R866-1-R2/R865-1-RES-2, R865-1-RES-1, R866-3-R1) to the
  residue checklist.
- At the merge turn, build and validate the current-dev candidate (builder and native banks) and link the receipts.
- Hosted/act acceptance.
- The bench re-check of F-G5 on the `8c5e2b4f` gating images.
- R870's separate re-check of #952's timing evidence.
- Maintainer merge authorization.

R865-4 FINISHED
