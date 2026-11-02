[R754] NEGATIVE - exact head 96bfa8513978ebc8c2f2e73bd98914b56e84bf12

Round R754-2, external cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1), tree `816e6324dd4f2f38240faca3e85f547a85a32168`, round-2 delta against `a8bcfba9`, with live dev `1f29f189` merged.

## Verdict

The generator and its gate now do what round 1 asked of them. A separate simulation of `milan_csr` at shipping parameters agrees with every Reset and Type cell: 203 registers, 257 words and 8,224 bit checks, with no unexplained row. All 38 plants fail as required and the comment-only control stays fresh. A word the parser cannot read refuses, and the page is left untouched.

The verdict is NEGATIVE because seven MINOR defects remain in what the page and the design notes say:

- Two statements do not describe the merged tree, and a third is incomplete against it (F1, F6, F7).
- Two generated or new rows are false against the RTL (F2, F3).
- A design-notes sentence written this round is false against the RTL (F5).
- 23 read-condition rows are false as printed (F4).

No RTL changed in this PR, so none of this is a hardware defect. All seven are fixes to `scripts/register_descriptions.json`, the design notes, or the generator's row and condition wording in `scripts/register_page.py`.

## Findings

### F1 - MINOR - Conformance, Docs - `MAC_STATUS` says firmware writes it only while the saved-state writer runs

- **Where:** `docs/reference/REGISTER_MAP.md:516`, from `scripts/register_descriptions.json:1268`; `docs/design/CSR_REGISTER_NOTES.md:164` and `:198`.
- **Authority:** #797 acceptance, "no document marked current contains a statement contradicted by the code"; this round's check 3, the page describes the merged tree.
- **Evidence:** PR #816 for #70 merged in this delta. `sw/firmware/milan_baremetal/milan_baremetal.c:1099-1102` polls the PHY when `nvm_started` is 0 if `phy_live` is set. `:1671` sets `phy_live` in `nvm_boot()`. `:950-954` states the rule: "published on every boot path from there, persistence disabled included". This was true at `1e80128f`, which is why round 1 kept it. Commit `96bfa851` restated it on the page after the merge.
- **Impact:** on a persistence-disabled boot a reader concludes the word keeps `0x0000000D`. Firmware publishes the real link there.
- **Required outcome:** page and both notes lines say firmware publishes from MDIO on every boot path that reached `nvm_boot()`, and that nothing writes it after a CSR identity mismatch.
- **Verification:** re-read against the cited lines; `--check` fresh.

### F2 - MINOR - Conformance, RTL, Docs - `PP_NVM_STAT[1:0]` says "stored and read back, drives nothing"; those bits are the heartbeat and the commit acknowledge

- **Where:** `docs/reference/REGISTER_MAP.md:4495` and the `[6:2]` rows above it; `docs/diagrams/regmap/pp/PP_NVM_STAT.svg`. Cause: `scripts/register_page.py:249-250` prints the sentence for any `R/W` field named `RESERVED`, and `scripts/register_descriptions.json:3940` `split` makes `[1:0]` such a field. At `a8bcfba9` the word was one `[31:0]` row, so this is new in the delta.
- **Authority:** #797 issuecomment-6522974767, "side effects ... doorbells ... stated in the field's row"; the page legend, "A reserved `R/W` field stores bits that drive nothing".
- **Evidence:**
  - `hdl/common/csr/milan_csr.sv:2200-2204` forwards the whole written word to the backend's strobe index, and `:2282` serves reads from the input, so nothing is stored here.
  - `hdl/milan/KL_nvm_backend.sv:455-461` decodes `[0]` as heartbeat, `[1]` as commit acknowledged, and `[2]` to `[6]` as commit started, ARM, ATTEST, RELEASE and RELOAD.
  - `hdl/milan/KL_nvm_backend.sv:593-599` reads `[1:0]` as `2'd0`.
  - `milan_baremetal.c:1112` writes `NVM_STROBE_HB` (`0x1`) here on every heartbeat, which re-arms `T-NVM-WRITER-ALIVE`.
  - `receipts/compare_page.txt` rows `RW-NOT-STORED | PP_NVM_STAT@93C` measure no stored bit.
  - All seven strobes are listed once, in the `[31:24]` `TAG` row. The `[6:2]` rows name status bits only.
- **Impact:** a reader of the row concludes that writing bit 0 is harmless. It is the writer's liveness heartbeat. Round 1's F6 asked for exactly this: a row must not read as plain storage where the hardware fires an action.
- **Required outcome:** `[1:0]` no longer claims storage or "drives nothing", and each strobe is stated in the row of its own bit. A control holds the sentence off a word whose write leaves the block.
- **Verification:** re-read against the cited lines; a planted `split` `RESERVED` on this word refuses, or its row names the strobes.

### F3 - MINOR - Conformance, RTL, Docs - `ADP_CMD` rows say the strobes store and read back; they read 0

- **Where:** `docs/reference/REGISTER_MAP.md:1410-1411`, from `scripts/register_descriptions.json:1868-1869`. New in this delta: at `a8bcfba9` these rows were empty.
- **Evidence:** `hdl/common/csr/milan_csr.sv:1799-1802` are self-clearing strobes. `receipts/sim_word.txt`, `word 0x640`: `w1=0x00000000 w0=0x00000000`. The row's own `W1S` type, and page line 88's "`W1S` command strobes read back 0", disagree with it. "Reaches no logic" is correct: `hdl/milan/milan_datapath.sv:2780-2781` leaves both outputs open.
- **Impact:** a false readback claim, contradicted by the same row's type.
- **Required outcome:** exact text: "Inert strobe: self-clears and reads 0, and reaches no logic. Was advertise-now." and the same with "Was depart."
- **Verification:** re-read against `receipts/sim_word.txt`; `--check` fresh.

### F4 - MINOR - Conformance, RTL, Tests, Docs - Read conditions lose their grouping, so they are false as printed

- **Where:** "When / A read returns" tables, 23 of 71 rows: `docs/reference/REGISTER_MAP.md:3437-3441`, `:3507-3511`, `:3531-3535`, `:3555-3557`, `:3577-3579`, `:3653-3654`. Cause: `scripts/register_page.py:137-138` and `:150` join nested `&&` and `||` with no grouping. No selftest control covers grouping.
- **Authority:** round-1 F6, "generated conditions read as sentences"; #797 acceptance.
- **Evidence:** line 3439 reads "the selected stream does not exist or a snapshot is running or ... and the selected stream exists ..." and returns `{31'd0, aaf_ctrl[0]}`. Line 3441 gives the same first clauses and returns 0. Read normally, an absent stream returns `AAF_CTRL[0]`. `receipts/sim_directed.txt`, section "read-table grouping", with `AAF_CTRL[0]` at 1: an out-of-range talker row reads 0, and the in-range talker row reads 1. `hdl/common/csr/milan_csr.sv:2538` gates the arm on `win_in_range_w`. The rows are true only with brackets the page does not print.
- **Impact:** a programmer predicts the wrong source for a window read. Pseudo-code became words, but the logic did not survive the change.
- **Required outcome:** each row is unambiguous, by grouping or by one conjunction per row, and rows repeating a term are simplified. A selftest control fails when grouping is removed.
- **Verification:** each row read as printed agrees with a directed simulation of that row, and the new control fails on a generator mutant.

### F5 - MINOR - Conformance, Docs - The design notes say `STRM_SEL[9]` "acts only while `[8]` is 0"; it also acts with `[8]` at 1

- **Where:** `docs/design/CSR_REGISTER_NOTES.md:974`, a sentence written this round to answer round-1 F4; the page row at `docs/reference/REGISTER_MAP.md:3394`, from `scripts/register_descriptions.json:3292`, leaves the `[8]` = 1 case unstated.
- **Authority:** this round's check 2, the moved rationale states nothing the RTL contradicts.
- **Evidence:** `hdl/common/csr/milan_csr.sv:2528` `srp_idx0_ls_w` has no direction term. `:2574-2576` and `:3086-3087` use it for the read mux and the poll engine. `:1811` stores `[9]` whatever `[8]` holds. `receipts/sim_directed.txt`, with `i_lwsrp_status` high: `SEL` `0x100` reads `0xFFFFFFFF` at 0x85C, and `SEL` `0x300` reads `0x00000000`.
- **Impact:** a talker-side read with `[9]` left set silently loses the `LWSRP_STATUS` alias, and the notes say it cannot.
- **Required outcome:** exact text for the notes: "With `[8]` at 0 it selects sink 0's dedicated row. With `[8]` at 1 and `[3:0]` at 0 it still moves `STRMW_SRP` off the `LWSRP_STATUS` alias to the talker row." The page row states the same in its own words.
- **Verification:** re-read against the two `sim_directed` rows.
- **Note:** the RTL comment at `milan_csr.sv:2524-2525` says talker direction stays excluded. RTL comments are outside this PR. If the intent is that `[9]` should not act here, that is a new RTL Issue, and the page still states the code.

### F6 - MINOR - Conformance, RTL, Docs - The page says either bit enables the entity; the fabric holds the enable until the restore releases it

Retained from R753-2 F2, after re-reading its evidence.

- **Where:** `docs/reference/REGISTER_MAP.md:96`, `:1166`, `:1189`, `:4361`, from `scripts/register_descriptions.json:296`, `:1689`, `:3864`; `docs/design/CSR_REGISTER_NOTES.md:86`, `:348`, `:1229`.
- **Evidence:** `protocol-processor/hdl/top/protocol_processor_top.sv:2027`: `adp_enable_w = entity_enable_i && restore_done_o && !rbt_adp_off_w`. `hdl/milan/milan_datapath.sv:9586` also gates on `!amr_rs_hold_r`. `milan_baremetal.c:1846-1849`, new with #70: "The two writes REQUEST the enable; the fabric holds it until the restore walk releases it at COMPLETE or DEFAULTS, and a CLOSED restore holds it until reset."
- **Impact:** software that reads `PP_CTRL[0]` as 1 is told the entity is enabled while ADP may be held, or held until reset after CLOSED.
- **Required outcome:** exact wording for line 96: "`PP_CTRL[0]` or `ADP_CTRL[0]` requests the entity enable. The fabric holds it until the restore releases it." The rows and notes follow, and name the CLOSED case.
- **Verification:** re-read against the cited lines; `check_doc_style.py` rc 0.

### F7 - MINOR - Conformance, Docs - The page omits #787's hardware set of `milan_mac_phy_crg_reset`

Retained from R753-2 F3, after re-reading its evidence.

- **Where:** `docs/reference/REGISTER_MAP.md:4519`, and the `PHY_RESET_N` row at `:559`, which names this CSR as the PHY reset that reaches the pin.
- **Authority:** #797 issuecomment-6522974767, side effects in the field's row; this round's check 3 names #787's registers.
- **Evidence:** `sw/litex/milan_soc.py:2132`: `self.sync += If(reboot_phy_hold_sys, self.phy.crg._reset.storage.eq(1))`. `:2115-2123` and `docs/design/REBOOT_RESET.md:163-164` describe a level that only rises, where a CPU write in the same cycle clears it for that one cycle only. `REBOOT_RESET.md:173` confirms #787 adds no CSR, so this is its only register-visible effect.
- **Impact:** the row describes a plain software RW bit. A reader debugging a link drop after a REBOOT is not told the hardware owns it.
- **Required outcome:** the row states that an AECP REBOOT sets the storage and holds it, and links `docs/design/REBOOT_RESET.md`.
- **Verification:** re-read against `milan_soc.py:2115-2132`; `--check` fresh.

### SUGGESTIONS

- **S1:** the link-guard diagram omits `SETTLE --> HOLD` on a re-death (`hdl/common/KL_link_guard.sv:291-294`), and the servo diagram omits the returns to `IDLE` (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:972`). Labels are checked against the RTL, but edges are not. R753-2 S1, verified.
- **S2:** the `CHMAP_LOOP` sequence diagram reads the word with no busy poll, while the `STRM_SNAP` and `PP_STAT` diagrams show one. R753-2 S2.
- **S3:** rows name internal flops such as `pp_busy_r`, `lctx_wr_p_r` and `tctx_wr_addr_r`. The outward effect would read better where one exists. R753-2 S3, also seen here.
- **S4:** `SW_LINK` at line 2359 could say that `LINK_CTRL[0]` also gates gPTP `portEnabled` since the merge (`.port_enabled_i(eff_link_w)`, PR #813 for #806). No row states otherwise.
- **S5:** `RST_EPOCH` says "the count survives reset". A REBOOT's configuration reload returns it to its initial 0 (`milan_csr.sv:2300`, `docs/design/REBOOT_RESET.md:31`). Adding "a datapath reset" would be exact.

### RESIDUE

Purely wording, or a new contrived gate escape by the brief's rule. The manager carries these to the residue checklist.

- **R1:** lines 623, 992, 993, 2358 and 4420 run a carried fragment into the generated sentence with no stop. Exact fix: end each fragment with a full stop in the descriptions file. R753-2 R1.
- **R2:** `MAC_STATUS` rows read "full_duplex." and "link_up." and "speed (0=10,1=100,2=1000)". Exact fix: "Full duplex.", "Link up.", "Speed: 0 = 10, 1 = 100, 2 = 1000 Mb/s." R753-2 R2.
- **R3:** `CHMAP_LOOP[31:28]` says "Reserved." at reset `Dh`, against line 78's rule, and `[26]` at line 4277 says "This word is a measurement." at reset `1h`. Exact fixes: "Reserved: 0 on a measurement, `Dh` in the poison." and "1 on a word from the fabric. The poison also has this bit set, so compare the whole word with `0xDEADDEAD` first." R753-2 R3, widened.
- **R4:** line 68 says "RW words still store", while window and `PP_*` words write a different store. Exact fix: "No register was removed. Every word still decodes."
- **R5 (contrived escape):** a description note holding a literal Markdown one-column table of 40 words gives `--write` rc 0, `--check` rc 0 and `check_doc_style.py` rc 0 (`receipts/one_column_note_probe.txt`). The refusal at `scripts/register_page.py:508` covers only tables the generator builds. Nothing on the page uses this form: 0 one-column rows. Exact fix: refuse a note whose text holds a table delimiter row.

## Round-1 findings at this head

| Finding | State | Evidence at this head |
|---|---|---|
| F1 `--check` fresh on real changes | Closed | `receipts/mutants.tsv`: rc 2 on 24 rows, rc 1 on 14, rc 0 only on the comment-only control. Rows 20-37 all fail. Return codes identical to the author's published rerun |
| F1 gaps: blank purpose, unread form | Closed | `receipts/probes.tsv`: both rc 2 on `--write`, page byte-identical |
| F2 Gate skips 55% of the page | Closed for the page | `receipts/page_audit.txt`: 808 prose blocks, 5,149 words, 0 over 20, 0 one-column rows. A 340-word note and a 340-word cell each refuse. R5 records the contrived escape |
| F3 Reset and Type cells | Closed | `receipts/compare_page.txt`: 0 `X-NOT-INPUT`, no `PPS_ENABLE` row. The 200 numeric headings and 200 summary rows agree with simulated reset, by `receipts/page_audit.txt`. `CHMAP_LOOP` reads `0xDEADDEAD`. `RST_EPOCH` keeps `X`, and its row says why |
| F4 Carried prose | Closed, with one replacement false | All six rows re-read against the cited lines. The `STRM_SEL` rewrite introduced F5 |
| F5 Memory-map overprint | Closed | `receipts/renders/memory_map.png`: every label inside its block, no markup. A long label exits 2 in the selftest |
| F6 Side effects, conditions | Partly retained | 0 empty rows of 528 table rows by this round's parse. The W1S, W1C and doorbell rows read true, and a planted doorbell fails `--check` rc 1. Retained: `PP_NVM_STAT` strobes (F2) and condition grouping (F4) |
| F7 Mechanism diagrams | Closed | 10 generated Mermaid blocks, 10 parse with the published parser (`receipts/mermaid_parse.txt`), catalog rows present. Transition detail is S1 and S2. Not rendered visually |
| F8 Device labels | Closed | Both labels and the capture tool's name count 0 in the page, the notes and the descriptions. Remaining MAC strings are protocol multicast constants |
| S1, S2, S3 | Closed | `receipts/renders/MAC_CTRL.png`, `PP_NVM_STAT.png` split per lane; `CAP` fields named; no `if False` left |
| S4 | Out of this PR by ruling | RTL comments; not assessed |
| R1 to R6 | Closed | `TCAM_KEY_LO` row clean; 0 `Group summary`; legend corrected; 0 `lane-K`, 0 `#617 round 3`; `docs/DOC_GENERATION.md:175-179` names both generators |

### Rows in `compare_page.txt` that are not defects

These are the classes round 1 read and explained, plus one new word.

- `RW-NOT-STORED`: the guard on `PHY_RESET`, `LINK_CTRL[1]` and `ETH_GUARD`; window words and `PP_*` writing another store; `CHMAP_WORD` refused while disarmed; `REST_CMD` latching at commit. `PP_NVM_STAT` is new here, and F2 covers its reserved row.
- `W-NO-EFFECT`: `TCAM_CMD` and `REST_FLAGS`, which latch with the commit bit.
- `R-BUT-OUTPUT`: `LTAP_CTRL` and the `PP_SPADDR` doorbell.
- `R-BUT-WRITABLE`: `CHMAP_SNAP[2]`, a timeout flag moving after an earlier arm.
- `RESET-INPUT-DEP`: sticky inputs held high through reset release.
- Unlisted addresses with activity: 0.

## Round-2 checks

1. **Closure.** The table above.
2. **Design notes.** `receipts/survival.txt`: this round's own splitter finds 2,061 of 2,146 sentences of the previous page verbatim across the page, notes and descriptions. The 85 others are `Group summary` rows, the old pseudo-code conditions, the corrected rows, and bench or tool text removed by F8. Each sampled one was removed by a ruling or restated. Sampled facts survive: the arming history is at notes line 934, and the old `STRMW_SRP` status format stays in the port comment at `milan_csr.sv:633`. No fact loss found. Statements contradicted: F1 (notes `:164`, `:198`), F5 (`:974`), F6 (`:86`, `:348`, `:1229`). The notes hold about 31,000 words, so this is a sample. Their banner states that the reference and the RTL win.
3. **Merged tree.** `hdl/common/csr/milan_csr.sv` is unchanged by the merge. The published export's `csr.csv` differs from round 1 only in its timestamp and the ISA string's order. Its comment-stripped hash equals `csr_csv_sha256` in `scripts/register_map_soc.json`, and all 79 CSR addresses match. PR #813 for #806, #814 and #818 add no register. #787 adds no CSR, only the hold on `milan_mac_phy_crg_reset` (F7) and the two `REBOOT_MAC_*` parameters in the extract. #70 changes what `MAC_STATUS` and the enable bits mean in practice (F1, F6). The dev side did not edit the old page, so no dev text was lost in the merge.
4. **Docs workflow.** The step is `gate_50` in `.github/workflows/docs.yml:430-435`, and `ci_events.py --check` and `ci_gate_workflows.py --check` are rc 0. Local gates are all rc 0 (`receipts/gates/rc.txt`). The selftest prints 58/58 (`receipts/gates/selftest.txt`).
5. **ETH_GUARD.** The page states the code: `sw/litex/milan_soc.py:1622` and `:2162` bind the level and nothing else reads it. The row, the key behaviour and the guarded levers agree with `receipts/sim_directed.txt`. The issue's other link-control items are on the page. Implementing the gating is out of this PR by ruling.
6. **Comment rule.** No bench lane labels, review rounds, reviewer IDs or issue-comment IDs in the added lines of the generator sources or `memory_map.gen.py`. The two `issuecomment` links in the notes (`:1102`, `:1112`) are carried prose, not source comments. No RESIDUE arises.
7. **Author's packet.** `receipts/evidence_manifest_check.txt`: five sampled files, including the handoff and `csr.csv`, match `published_sha256` in the evidence `MANIFEST.json`. The evidence tree holds no detached signature file, so hash agreement is what was verified. `HEAD.txt` names this head and tree.

## Prior public findings

Read only after this round's verdict was on disk (`receipts/verdict_preread.md`). R753-1 and R754-1 are closed or retained in the table above, with the same results as R753-2's round-1 table. R753-2 at this head:

| R753-2 finding | This round |
|---|---|
| F1 `MAC_STATUS` | Same defect, found independently: F1 |
| F2 entity enable | Retained: F6 |
| F3 REBOOT hold | Retained: F7 |
| F4 read conditions | Same defect, found independently: F4 |
| F5 `ADP_CMD` | Same defect, found independently: F3 |
| S1, S2, S3 | Retained: S1, S2, S3 |
| R1, R2, R3 | Retained: R1, R2, R3 |

F2, F5 and R4 here are not in R753-2.

## Hosted evidence at this head

Observed, not accepted; the manager owns acceptance. `receipts/hosted_snapshot.txt` is taken at the time of writing.

- The `docs` jobs concluded success in run 41359351300, including `docs-gates-0`, `docs-gates-1`, `docs-gates-2`, `docs-check`, `docs-check-no-git` and `wire-accountability`. In `docs-gates-0`, the steps "Register reference freshness gate" and "Concise audience documentation gate" concluded success. One late-cancel job was still queued, so the run had no overall conclusion.
- `rtl-fast`, `elaborate` and `rtl-full` were still running, with no failure visible. `Physical gPTP (nightly and manual)` is skipped, so it is not execution evidence.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 to F7) | #797 body and comments 6489587365, 6522974767, 6523093123; `docs/reference/REGISTER_MAP.md`; `receipts/compare_page.txt`; `receipts/sim_directed.txt`; `milan_baremetal.c:950-954,1099-1102,1671,1846-1849`; `milan_soc.py:2115-2132`; `receipts/mermaid_parse.txt` | R754-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| RTL | UNCLEAN (F2, F3, F4, F6) | `hdl/common/csr/milan_csr.sv` under simulation at shipping parameters; `receipts/sim_word.txt`, `sim_reset.txt`, `attribution.txt`; `hdl/milan/KL_nvm_backend.sv:455-461,593-599`; `milan_datapath.sv:2780-2781,9586`; `protocol_processor_top.sv:2027`. No RTL file changed in this PR | R754-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| Robustness | CLEAN | `scripts/register_sv.py`, `register_decode.py`, `register_fields.py`, `gen_register_reference.py`: rows 20-37 of `receipts/mutants.tsv`, `receipts/probes.tsv`. Refusals leave the page untouched, an unreadable form exits 2, a description key the RTL lacks exits 2. R5 is a contrived escape, residue by the brief's rule | R754-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| Tests | UNCLEAN (F4) | `scripts/register_selftest.py`, 58/58; 39 plants; 7 refusal probes; `scripts/check_doc_style.py`. All listed classes fail as claimed; no control covers condition grouping | R754-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |
| Docs | UNCLEAN (F1 to F7) | Page; `docs/design/CSR_REGISTER_NOTES.md`; `docs/diagrams/README.md`; `docs/DOC_GENERATION.md`; `docs/README.md:69`; `receipts/renders/`; `receipts/page_audit.txt`; `receipts/survival.txt` | R754-2 | 96bfa8513978ebc8c2f2e73bd98914b56e84bf12 |

## Real limits

- **Simulation scope:** `milan_csr` alone at the shipping parameters, handshake inputs tied, no engines. Window words were exercised at the reset selection and in the directed cases, not against an engine. Datapath and backend wiring were read, not simulated.
- **Export:** no export was rerun. The check used the author's published `csr.csv`, and `--check --soc-from` rests on the author's receipt.
- **Prose:** the design notes and the 18,500 table words were sampled, not all checked. Statements about silicon history were not verified.
- **Diagrams:** Mermaid blocks were parsed, not rendered visually.
- **Standards:** no IEEE or Milan text was read in this round.
- **Gates:** the full behave suite, the builder bank and the Verilator and Yosys banks were not rerun. `counters_contract_milan.feature` and builder leg 1 rest on the author's receipts. No manager source bank runs at this head. No hardware was used. Physical calibration was not run, and field skips are not hardware proof.
- **Isolation:** `receipts/verdict_preread.md` was on disk before R753-2 was read. After reading it, this round made three changes. F6 and F7 became MINOR findings: both gaps had been noted earlier as wording-level, and F6 moved once the processor gate was read. F3 and F4 gained the RTL attribution, since their rows contradict the RTL. F4 gained the Tests lens, which moved Tests to UNCLEAN against the pre-read file's CLEAN.
- **Harness changes from round 1:** `scripts/mutants.py` adds the three paths the generator now reads, and `scripts/sim_main.cpp` adds the read-table grouping section. `receipts/survival.txt` is this round's own splitter, not the author's tool.
- **Restore:** `receipts/restore_check.txt` shows the exact head, tree, clean index, clean tracked bytes and modes, and the five required submodule gitlinks.

## Pending manager duties

- Hosted and act acceptance at the final head, including the `rtl-fast`, `elaborate` and `rtl-full` runs still in progress here.
- The current-dev merge candidate (builder and native banks) against live dev at the merge turn.
- Carry R1 to R5 to the residue checklist.
- Lane conflict with PR #815: both add a docs-check step, and D0's inventory must list `docs/design/CSR_REGISTER_NOTES.md`.
- The ETH_GUARD gating and RTL comment decision stays open and out of this PR.

R754-2 FINISHED
