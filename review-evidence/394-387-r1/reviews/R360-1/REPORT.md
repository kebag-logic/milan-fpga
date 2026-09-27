[R360] NEGATIVE - exact head fddc58e43733afd90d6222e58999e0f416a30df9

# R360-1: independent internal review of PR #600 (issue #394 acceptance 2, issue #387 acceptance 4)

- Head `fddc58e43733afd90d6222e58999e0f416a30df9`, tree `fbb9754c086d837643fe580ed7eb903b630b5aad`.
- One commit on the source base `2a2a7bb655e528edc3087c88033cd3a47546feb4`. It adds `docs/findings/394_387_E1_SWITCH_CYCLES.md` (+416) and nothing else.
- Public evidence examined: `review-evidence/394-387-r1` at `8f983d245a12e18a47ced37904d405b624c7e024` (165 files).

## How the context was rebuilt

I read, in this order:
1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The #394 body with acceptance 2 as frozen, and the owner decisions 5789765478, 5810503583 and 5857769804.
4. The assignment 5858215210, the TAKEN comment 5858224404, REVIEW READY 5858459678 and the manager's comment 5858862351.
5. The #387 body with acceptance 4, and decisions 5606198212, 5794731090, 5802264260, 5810378282 and 5816509317.
6. The #117 bound decision 5795898094, #599, #75 and #593.
7. The authorities: `docs/design/GM_LOSS_RECOVERY.md` (Recovery bound; Media re-base on a PHC step), `docs/design/TIME_SYNC.md` (Step policy), `docs/testing/TESTING.md` 6b, `docs/reference/REGISTER_MAP.md` (0x110, 0x720, 0x8F8), `sw/litex/milan_soc.py:1761-1811` and `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv`.
8. The diff, then the packet.

After my own pass I read the PR's public thread. It holds two review-start notices and no findings, so no earlier finding needs to be resolved or carried forward.

## Verdict summary

The measurements are sound. Every cell of the per-cycle table and every summary number reproduces exactly from the packet's per-cycle analyses. All 50 raw-artifact rows match the packet's raw indexes. The identity gate, the OUT4 proof and the restore proof are supported. The #75 treatment is correct.

The page as a record has four open MINOR findings:
- The central per-cycle table does not render.
- The link-counter explanation says less than the evidence supports.
- The #387 PASS is graded against a bound whose provenance and scope the page does not state, on steps that never hit locked media.
- The artifact locator points to volatile and private locations.

The #394 acceptance 2 FAIL verdict is correct.

## Findings

### F1: MINOR (Docs). The per-cycle table does not render as a table

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:209-210`.
- **Evidence:**
  - The header row has 9 cells and the delimiter row has 10 (`|---|` x10).
  - Under GitHub-flavoured Markdown a table whose header and delimiter cell counts differ is not recognised.
  - The repository-pinned renderer (`tools/markdown/requirements.txt`) renders 5 tables from the page, not 6, and never produces the per-cycle header.
  - The platform's own rendered view of the file at this head (read-only contents request) also shows 5 tables. The per-cycle block appears as a run-on paragraph of pipes.
  - With the delimiter corrected to 9 cells, the same renderer yields 6 tables (positive control).
  - Receipts: `receipts/render-tables.txt`, `receipts/rendered-page-github.html`, `receipts/recompute-table.txt` (first line).
- **Impact:** the record's main deliverable, one per-cycle table as the assignment requires, cannot be read in the rendered page. The docs gates pass, so nothing flags it.
- **Required outcome:** the per-cycle table renders as a 9-column table with unchanged cell values.
- **Verification:** the pinned renderer, or the rendered view, shows 6 tables and a per-cycle header. `scripts/recompute_table.py` still reports 0 differing rows.

### F2: MINOR (Conformance, RTL, Docs). The link-counter explanation says less than the evidence supports

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:165-169`, `:244-256`, and `:10` and `:260` together.
- **Evidence:**
  - `sw/litex/milan_soc.py:1782-1797` defines `link_status` (MAC_STATUS 0x110) as a software-published CSR that resets to link_up=1, speed=2 (gmii) and full_duplex=1. That is exactly `0x0d`.
  - No C, header, assembly or Python source outside `milan_soc.py` writes it, and no firmware source uses MDIO (`receipts/source-and-packet-checks.txt`). This is the defect the manager filed as #599.
  - The page instead says:
    - "DUT MAC_STATUS stayed `0x0d` throughout each outage. Thus no DUT link-down or link-up timestamp was observable." It does not say that `0x0d` is the unwritten reset value, and so no observation of the PHY at all.
    - "This run never wrote that status to manufacture edges." This presents the cause as a choice the run made, not as the build having no publisher.
    - "The link-counter failure reproduced in all ten cycles" and "`+0 / +0`, defect", without stating that whether the DUT PHY link dropped at all was not observed.
  - #599 (acceptance 4) records that the inline capture point sits on that link and may hold it up.
  - The page cites neither #599 nor that limit.
  - In every cycle the packet shows no frame of any kind on the tapped link from 1.49-2.22 s after OFF until the wire return at 38.25-40.57 s (`receipts/step-context.txt`). That is consistent with a PHY drop, or with the capture point not passing traffic while the switch side is down. It does not decide between them.
- **Impact:** a reader takes `MAC_STATUS = 0x0d` as the DUT reporting link-up through each outage, and "defect / failure reproduced" as proof of a PHY drop that went uncounted. Neither was observed. The #599 re-run depends on exactly this distinction.
- **Required outcome:** the page states four things:
  - MAC_STATUS is the software-published register at its reset value, and nothing in this build writes it (#599).
  - So the LINK_UP/LINK_DOWN counters cannot advance on this image, whatever the PHY did.
  - Whether the DUT PHY link dropped was not observed, and the capture point may hold it up.
  - The sentence about "this run" manufacturing edges is removed.

  The FAIL verdict stays. Acceptance 2's counter increments were not shown, whatever the cause.
- **Verification:** reread lines 10, 165-169 and 244-260 against `milan_soc.py:1761-1797` and #599. No sentence may assert or imply an observed DUT PHY link drop.

### F3: MINOR (Conformance, Docs). The #387 acceptance 4 PASS does not state its bound's provenance, and the steps never hit locked media

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:11`, `:159-163`, `:197-207`, `:224` and `:307`.
- **Evidence:**
  - Acceptance 4 asks for the time from the step to relocked media "inside the bound recorded in item 2".
  - The page grades PASS on "within one further stream restart" (lines 11 and 161). That phrase is the media row of `GM_LOSS_RECOVERY.md#recovery-bound`, which the owner fixed on #117 (5795898094) for grandmaster loss and return.
  - The #387 contract that item 2 records is `GM_LOSS_RECOVERY.md` "Media re-base on a PHC step" together with `TIME_SYNC.md#step-policy`. It is count-based, one counted event per step: `tu` with at least 0.25 s holdover, one `mr` toggle and one MEDIA_RESET. It states no time bound.
  - The page does not say which of the two it applies. It does not say that no time bound exists to be "inside". Its "Step to media" column of 7.50-12.54 s is presented beside the five-second gPTP bound.
  - The packet also shows that in all ten cycles each step landed during the outage:
    - The DUT servo had been in HOLDOVER since 1.29 s after OFF.
    - The DUT listener was already unlocked.
    - Neither CRF stream was on the wire.
    - Relock followed the return of the peer's stream (first CRF PDU into the DUT 4.4-9.9 s after the step), then 2.5-3.0 s of ACQUIRE (`receipts/step-context.txt`).
  - So the measured interval is outage recovery: stream re-establishment plus servo acquisition. It is not a locked stream's reaction to a step. The page does not say so.
- **Impact:** the PASS can be read as proof that a locked CRF stream re-bases within a bound after a PHC step, and used to close #387. The run did not exercise that condition, and the bound it applies is the #117 loss/return row.
- **Required outcome:** the #387 row and the method section do three things:
  - Name the bound applied and its source (the #117 recovery-bound media row, recorded in `GM_LOSS_RECOVERY.md`).
  - State that the #387 re-base contract is one counted event per step with no time bound.
  - State that every step landed while the servo was in HOLDOVER with both streams absent, so the interval does not isolate a locked stream's step reaction.

  Then either scope the PASS to exactly that, or record it as needing a manager decision on whether this satisfies acceptance 4.
- **Verification:** reread lines 11 and 159-163 and the #387 verdict against `GM_LOSS_RECOVERY.md:88-99` and `:142-158`, and against `receipts/step-context.txt`.

### F4: MINOR (Conformance, Docs). The artifact locator names volatile and private locations

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:341-351`.
- **Evidence:**
  - Line 345, "Large raw captures remain under `/tmp/a375/cycleNN/`": a volatile local path. The captures are now in private cold storage. This is the known correction.
  - Line 343: the packet is "identified as `2026-09-23/394-a375`". That is a private management-tree name that is not publicly resolvable, and it is misdated: the run was on 2026-09-27. The public archive is `review-evidence/394-387-r1` at `8f983d245a12e18a47ced37904d405b624c7e024`, and the page does not name it.
  - Line 347: "Each cycle's `raw-artifacts.json` lists paths". Every listed path is `/tmp/a375/...`, and the page does not say that those paths are historical.
  - Line 349, "`MANIFEST.sha256` covers retained packet files". Against the public copy, `sha256sum -c` fails for 13 of 163 entries:
    - 12 files were altered at publication (the redacted gate transcripts, two tools and the validation preflight).
    - `PR-BODY.md` changed after the author's manifest was written.

    The publisher index `MANIFEST.json` verifies 165/165 and records the original and published hashes (`receipts/source-and-packet-checks.txt`).
  - Line 351 asserts "Raw retention follows TESTING section 6b" while the only locator given is volatile.
  - #387 acceptance 4 and #394 acceptance 2 both require raw artifacts retained per TESTING 6b.
- **Impact:** a cold reader cannot locate the retained evidence from the page, and a manifest check against the public packet fails.
- **Required outcome:** the locator names:
  - the public packet archive and its publisher index;
  - that the raw captures are in private cold storage, indexed by size and SHA-256 in `RAW-ARTIFACTS.json` and the per-cycle indexes, whose `/tmp` paths are historical names.

  It also drops the private packet name, or replaces it with the public one. It either scopes the `MANIFEST.sha256` claim to the author's packet before publication redaction, or points to the publisher index. No local absolute path remains.
- **Verification:**
  - `scripts/hygiene_scan.py` over the page reports no `abs-path` or `private-mgmt` hit.
  - The named archive resolves.
  - The index the page names verifies against the public files.
  - `scripts/check_hash_table.py` still reports 0 mismatches.

### S1: SUGGESTION (Tests, Docs). The docs gates accept a table whose header and delimiter cell counts differ

- **Where:** the documentation gates (`scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py`). All passed at this head over F1 (`receipts/gates.txt`, `receipts/gates-pinned-renderer.txt`).
- **Suggestion:** a follow-up issue for a gate arm that fails when a pipe block renders as no table. This is pre-existing tooling and outside this PR's scope.
- **Effect on coverage:** none, because it is optional.

## The seven assigned questions

1. **Identity gate and OUT4 proof: supported.**
   - `identity-result.txt` shows readback CRCs ROM `9b6576a9`, QSPI payload `3c18c276` and AEM `93742dd2`, equal to `expected-crc.txt`.
   - Bitstream and AEM SHA-256 equal the assignment's values.
   - The ENTITY (312 B) and CONFIGURATION (106 B) descriptors match exactly.
   - `csr.csv` is 9033 B, SHA `92981a36...`, as the page states.
   - e1 pins K18 and L16 agree with `sw/litex/platforms/alinx_ax7101.py:46,70`.
   - `9e9954e9..2a2a7bb6` changes 4 documentation or evidence files only, and the gitlinks are identical.
   - OUT4 proof (cycle 1): no switch gPTP frames on the DUT link while off; controller carrier lost; reset epoch 1 with a largest console gap of 0.250 s; the peer's ADP available_index went 65863→65871 and its GPTP_GM_CHANGED 15→17 without a reset; the outlet census while off shows every other outlet ON.
   - The page correctly says readback proves CRC consistency, not configuration SHA-256.
2. **Per-cycle numbers: all match.**
   - All 10 rows × 9 cells recompute exactly from `cycleNN/analysis.json` with independent code (`scripts/recompute_table.py`, `receipts/recompute-table.txt`).
   - The summary claims all hold: gPTP 0.441-1.817 s; first PDU after wire return 5.07-14.00 s; longest step-to-media 12.54 s; steps −358,781 s, −162.46 s, and −95.74 to −96.47 s; the intermediate MEDIA_RESET zero seen in 5/10; largest console gap 0.251 s; half-round-trip 0.074 s and 0.151 s; anchor spread ±0.051 s.
   - There is one PHC discontinuity per cycle, no unhealthy sample after recovery, and every recovery sample comes after its step bracket.
   - Timing resolution and cross-host uncertainty are stated. Cycle 10 shows a 0.03 s cross-host inversion (a controller-read MEDIA_LOCKED before the first tapped CRF PDU), which is inside the stated bounds.
   - Mutation probes show that the checks catch a changed cell or hash (`receipts/mutation-probes.txt`).
   - Presentation defect: F1.
3. **#394 acceptance 2 FAIL: correct.** The explanation is incomplete and implies an unobserved PHY drop: F2.
4. **#387 acceptance 4 PASS: not adequately bounded.** See F3. "Within one further stream restart" is the #117 loss/return media row. The #387 item-2 contract is one counted event per step, with no time bound. Within the capture window the count claim itself holds: STREAM_START/STOP +1/+1 on both talkers, and MEDIA_LOCKED/UNLOCKED +1/+1 with no further unlock.
5. **#75: correct.**
   - The page records first-PDU times against the one-second figure using the tapped wire-return landmark (lines 177-187 and 236-240).
   - It states that #75 times from CONNECT_RX success, that no CONNECT_RX was issued, and that the hundred-reconnect experiment is not satisfied.
   - It says it does not close #75 (line 15).
   - #75's body confirms the trigger and the 100-cycle requirement.
6. **Restore: supported.**
   - All 18 stream states have conn_count 0 at start and at end.
   - The DUT and peer clock source index is 0 at start and at end.
   - Every non-state, non-counter, non-AVB-info census payload is equal (`receipts/restore-census-compare.txt`).
   - Outlets were all ON at start and end, the final grader passed 10/10, and the capture driver and controller files were cleaned up.
   - The restore tooling only disconnects (ACMP type 8). Watch mode only reads, which supports "no controller re-bind".
7. **Public hygiene: two issues, both in F4.**
   - The page carries no peer, switch, host, instrument or private-suite names and no serial-like or EUI identifiers. `041060010000bb80` is the stream format.
   - The hits are `/tmp/a375/cycleNN/` (line 345, the known correction) and the private packet name `2026-09-23/394-a375` (line 343).

## Clean-lens evidence

```text
[R360] PASS Robustness - docs/findings/394_387_E1_SWITCH_CYCLES.md:79-101,222-240,311-333 with receipts/step-context.txt, receipts/recompute-table.txt, receipts/restore-census-compare.txt - Checked the record's claims on the failure and boundary paths against cycleNN/analysis.json and the censuses. The capture preflight failed before any outlet operation, and the page discloses it. The cycle-1 carrier method differs, and the page discloses it. Reset epoch stayed 1 and the console never went silent (largest gap 0.251 s), so there was no reset during activity. The outcome repeated across ten cycles. The 180 s STOP deadline was never approached: steady state was reached by about 53 s after OFF. Every resumed PDU was valid with tu=0. There was no unhealthy sample after recovery. The cross-host inversion in cycle 10 is inside the stated uncertainty. Restore after repeated disconnects is proved. No open finding is attributable to this lens.
[R360] PASS Tests - review-evidence/394-387-r1/author/tools/analyze.py:25-88 and tools/report.py:7-31 at 8f983d24; head gates receipts/gates.txt, receipts/gates-pinned-renderer.txt - The PR adds no test. I checked the operator's analyzer: the CRF validity predicate (subtype, version, type, 48 kHz, 8-byte data with interval 96, PCP 3 / VID 2, exact stream ID), the step detector (a PHC-minus-wall jump above 10 ms between consecutive reads), the recovery predicate (sync, asCapable, tu=0 with the switch as GM), and report.py's assertions. I recomputed the page independently rather than reusing report.py; mutation probes on a cell and on a hash are each caught. All ten documentation, scope, bare-metal and feature-status gates return 0 at the head, with the pinned renderer in a disposable environment. S1 is optional.
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3, F4) | #394 acceptance 2 and owner decision 5857769804; #387 acceptance 4 and decisions; `GM_LOSS_RECOVERY.md:88-158`; `TIME_SYNC.md:76-108`; `TESTING.md` 6b; #75; #593; #599; page lines 8-15, 155-187 and 242-309 | R360-1 | `fddc58e43733afd90d6222e58999e0f416a30df9` |
| RTL | UNCLEAN (F2) | `sw/litex/milan_soc.py:1761-1811`; `REGISTER_MAP.md:405` (0x110), 0x720, 0x8F8 state encoding; `KL_talker_diag_ctx.sv:62-74` (START zeroing); firmware sources for link-status writers or MDIO (none) | R360-1 | `fddc58e43733afd90d6222e58999e0f416a30df9` |
| Robustness | CLEAN | see the PASS line above | R360-1 | `fddc58e43733afd90d6222e58999e0f416a30df9` |
| Tests | CLEAN | see the PASS line above | R360-1 | `fddc58e43733afd90d6222e58999e0f416a30df9` |
| Docs | UNCLEAN (F1, F2, F3, F4) | the whole page at the head, rendered and source; locator lines 339-363; the public packet and its indexes; the hygiene scan | R360-1 | `fddc58e43733afd90d6222e58999e0f416a30df9` |

## Other observations (not findings on this page)

- **O1.** The author's `MANIFEST.sha256` in the packet is stale for `PR-BODY.md`. The publisher index records the final hash. This is folded into F4 only because the page cites that manifest.
- **O2.** The public packet, not the page, carries entity, clock and controller EUI-64 values: `analysis.json` `states_end`, the censuses and `setup.jsonl`. The manager's archive hygiene scan should decide whether these count as device identifiers.
- **O3.** After restore, two talker stream-info responses still carry a stream ID, destination MAC or VLAN with conn_count 0. That is consistent with "no bindings left". The page claims "unbound", not byte-identical states.

## Real limits

- The per-cycle raw captures (`console.jsonl`, `tap.pcap`, `controller.jsonl`, `controller-wire.pcap`) are in private cold storage.
  - I could not re-run `analyze.py`.
  - The derivation from raw data to analysis rests on the operator's analyzer, which I read, and on hash consistency: all 50 page rows match the per-cycle indexes and `RAW-ARTIFACTS.json`.
- Clock-offset estimates and USB acquisition latency are the operator's. They were not independently calibrated.
- The DUT PHY link state was not observable in this run: there was no BMSR read.
- There was no bench access, and physical calibration was NOT RUN. Field skips are not hardware proof.
- Full parent, PP, gPTP, Yosys and builder banks were not run. They were not permitted, and a documentation-only diff does not need them.

## Hosted CI at the exact head (not my acceptance)

- At review time these executed contexts had succeeded: `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate` and `wire-accountability`.
- `docs-check` was still in progress.
- The Verilator, Yosys and physical contexts were skipped. Skipped is not executed.
- Receipt: `receipts/hosted-check-runs.txt`.

## Pending manager duties

- Publish this report.
- Run a correction round for F1-F4, then a re-review at the new head covering Conformance, RTL and Docs. Robustness and Tests must be re-covered too if the change touches their scope.
- Get the external review (R361) verdict.
- Wait for the hosted `docs-check` to complete.
- Validate the candidate merge on live dev `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- Record any decision on #387 acceptance 4 under F3.
- Make the O2 archive hygiene decision.
- Re-run #394 acceptance 2 after #599.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`.
- **Scripts** (portable; each takes the page, the packet or the checkout as arguments):
  - `scripts/recompute_table.py`
  - `scripts/check_hash_table.py`
  - `scripts/step_context.py`
  - `scripts/restore_compare.py`
  - `scripts/hygiene_scan.py`
  - `scripts/render_tables.py`
  - `scripts/mutation_probes.sh`
  - `scripts/source_and_packet_checks.sh`
- **Clone integrity:** after all probes, HEAD and tree are exact, the index and worktree are clean, there are 0 untracked files, all 929 tracked blobs rehash equal, there are no odd modes, and the gitlinks `external efeb541a`, `gptp-processor 5dce647a` and `protocol-processor 870ff88a` equal HEAD (`receipts/clone-integrity.txt`).

R360-1 FINISHED
