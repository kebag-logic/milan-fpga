[R334] NEGATIVE - exact head a9b7874d415d935949becd7ccfd58799927efb08

Internal independent review, round R334-1, of processor PR #121 for issue #120
(`Mister-M-alt/protocol-processor-control-plane-avb-milan`). Exact head
`a9b7874d415d935949becd7ccfd58799927efb08`, tree `14040d6f4646d648748540d73c1c2e38de4f2b2e`,
source base `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.

## Verdict in one paragraph

The RTL change is right. `aecp_name_wr_o` is the descriptor store's own live name-RAM
write enable (`take_wr_w && st_name_i`). The store's RAM mux now consumes the exported
net itself, so the pulse and the RAM write cannot diverge. With comments and whitespace
stripped, the complete functional delta is 8 lines: three new 1-bit outputs and their two
connections. No other port, parameter, register or timing changed. The pre-existing 7666
pp_top checks pass unchanged, and every measured latency line is byte-identical to the
base. The shipped tests kill every mutant I built that is observable in reachable operation:
decode-driven, level, stretched, late, missing-lane, first-lane-only, boot-inclusive and
tied-low. The mutants that survive are equivalent under the dispatched microcode, and a
counting probe over the full suite confirms it. Documentation of the new port is correct.
**One MINOR finding stops a positive verdict.** The PR inserted the two new harness ports
inside an existing `//!` bundle in `tb/pp_top/pp_top_wrap.sv`. That detaches the contract
of three pre-existing ports, by the parent's own accepted port parser. This is the same
defect round 2 fixed in the engine, and it contradicts the round-2 claim that the added
port creates no documentation debt. The fix is to move a few lines, with no behaviour change.

## 1. Reconstructed scope and authorities

- `AGENTS.md` / `CONTRIBUTING.md`: **not present** in this repository at head (checked;
  the conventions live in `README.md`, `docs/README.md`, `hdl/README.md` and the guides).
  Read: `README.md`, `docs/README.md` (single-source rules, editing workflow, `make check`).
- Issue #120 body (frozen): add one output `aecp_name_wr_o`, a single-cycle `clk_i` pulse
  per accepted live name write into the descriptor store. It is driven from the store's
  acceptance, not from command decode. Refused, aborted and out-of-range writes stay
  silent. No other behaviour change, no new state, and the NVM mark is unchanged.
  Acceptance 1 is the port, its `//!` contract, the integrator guide and the top contract
  table. Acceptance 2 is exactly-once per accepted write including multi-beat names, never
  on refused/aborted writes, plus a command-decode mutant that must fail. Acceptance 3 is
  the area delta, the donor gates and the parent consumer gates.
- Manager correction 5845334300: the parent consumer bar runs with the parent carrying an
  explicit open `.aecp_name_wr_o()`, because parent strict lint makes an unconnected
  output fatal (PINMISSING at `KL_pp_shadow.sv:1072`). Nothing changes in this PR for it.
- Manager round-2 assignment 5845451831 lists four processor-side parent-gate findings at
  `691f1d2b`: C++ long function, undocumented Python functions, port contracts ("every
  port this PR added or changed, in the top, the engine, the store and the harness"), and
  wall-clock dependence. Their disposition is in section 4.
- Parent prerequisite report (milan-fpga#502, issuecomment-5844910603): the parent needs a
  live name-write event to feed a sticky "saved state pending" bit. The map path already has
  `amap_edit_req_o` with phase 5.
- Interface authorities: `docs/architecture/02_interfaces.md` §8.1 (the saved-state
  pending outputs table), `docs/guides/integrator.md` §8 (class-D status wires table), the
  `//!` port contracts in `hdl/top/protocol_processor_top.sv`, `hdl/aecp/KL_aecp_engine.sv`
  and `hdl/aecp/KL_aecp_desc_store.sv`, and `07_memory_maps.md` §3.4 (name overlay).
- History: `691f1d2` (first author round) and `a9b7874` (second author round).
- Public evidence: `kebag-logic/milan-fpga@27f87160…/review-evidence/pp120-r1`, 123
  manifest entries with 0 hash mismatches (`receipts/14-public-evidence.log`). Its
  producers are the two author rounds only (`author/`, `author-r2/`). I found no
  manager-produced bank receipts in that tree and no manager evidence comment on the
  issue or PR beyond the review-start notice.
- Prior public review findings on PR #121: **none exist** (the PR has no reviews; its only
  comment is the review-start notice). The only prior findings are the manager's four
  round-2 parent-gate findings, resolved below.

## 2. Answers to the five verification questions

**(1) Driven from the store's actual acceptance, exactly once per accepted lane.**
- The comment-stripped RTL delta is 8 lines (`receipts/02-rtl-tokens.log`). In
  `KL_aecp_desc_store.sv:457`, `assign name_wr_o = take_wr_w && st_name_i;`, and `:545`
  now reads `name_we_w = name_wr_o;` in place of the identical base expression. So the
  export is the live name-RAM write enable. The boot-load branch (`S_NAM_RSP`) is
  exclusive with `st_ready_o` (`S_READY`/`S_BAD`), so boot loading cannot pulse.
  `691f1d2..a9b7874` changed 0 RTL tokens.
- The µCPU drives one request per `NAME_WR` µop and advances on `st_ready_i`
  (`KL_aecp_ucpu.sv:299,344`). `rb_hold_w` cannot extend a `NAME_WR`, because only
  response-building ops drive `rb_we_o`. So one accepted lane gives exactly one
  acceptance cycle. `SET_NAME` issues `NAME_WR` only for lanes whose bytes differ
  (`gen_ucode.py:2079-2086`). Lock refusal (`CHECK_LOCK`) and range checks (`RGN_NADDR`)
  both precede any write.
- Focused suite at head: `NW: 85 checks, 0 failures` (`receipts/03-*`). The PR's own
  mutation campaign reproduces: the decode mutant builds and fails the required
  `NW EIGHT/LOCKED/ABORT` count checks, and golden and restored pass
  (`receipts/04-shipped-mutation/`).
- Reviewer mutants (`scripts/05-reviewer-mutants.py`, `receipts/05-summary.txt`). Every
  store-level mutant changes only the export and keeps the RAM enable on its original
  expression, so the wrapper's RAM-enable tap stays an independent observer. Verdicts come
  from the completed simulation only; a build failure never counts as a kill.

  | Mutant | What it models | Verdict |
  |---|---|---|
  | M01 | command decode: pulse on the group-7 completion mark | KILLED (count 1≠8, ordering, alignment) |
  | M05 | level: sticky after the first write | KILLED |
  | M06 | two-cycle stretch | KILLED (width + count) |
  | M07 | one cycle late (registered) | KILLED (alignment tap only) |
  | M08 / M09 | multi-beat lane 0 / lane 7 missing | KILLED |
  | M10 | only the first lane per command | KILLED |
  | M11 | includes boot name loading | KILLED (`NW BOOT`) |
  | M14 | top output tied low | KILLED |
  | M02 / M03 / M04 | µop-level request (with/without first-cycle, not ready-qualified) | SURVIVED NW and full suite: **equivalent** |
  | M12 | any accepted store write (drops `st_name_i`) | SURVIVED NW and full suite: **equivalent** |

  Equivalence proof. After the `NAME_RD` answer that precedes every `NAME_WR`, the store
  sits in `S_READY` and has no autonomous exit (`KL_aecp_desc_store.sv:809-841`, `:1028-1040`).
  The µCPU is its only master and issues no store request in between, so every `NAME_WR`
  is accepted on its first cycle. Region-0 `WRITE_ST` exists only in µcode exemplars at 288
  and 512, which none of the engine's 56 `UPC_*_C` constants dispatch. The counting probe
  over the complete default pp_top run (`receipts/06-*`) found 31 name-write request cycles,
  31 pulses, 0 held cycles and 0 accepted non-name writes.
**(2) No other port, timing or behaviour change.**
- The elaborated port lists of `protocol_processor_top`, `KL_aecp_engine` and
  `KL_aecp_desc_store` (name, direction, width) differ only by the three new 1-bit outputs
  (`receipts/01-portdiff.log`).
- Donor suites at head with the pinned simulator: pp_top 7751/0, desc_store 584/0,
  desc_mem_guard 78/0, ucpu 386/0, acmp_nvm 349/0, timer_map 1360/0, all matching the
  author tallies (`receipts/07-donor-summary.log`). HDL lint gives 40/40 modules clean
  (`receipts/08-*`).
- Base pp_top gives 7666/0, and head gives exactly 7666 + 85. The two simulation
  transcripts differ only in the added NW lines and build noise, so every latency
  measurement (for example `[B4] … 2363 clocks`) is identical. The Verilator warning set is
  identical between base and head builds.
**(3) Contracts and docs.** The top, engine and store `//!` contracts, 02 §8.1 and
integrator §8 all describe one `clk_i` cycle per accepted 64-bit lane at the accepting
edge. They cover multi-lane pulses, silence for unchanged, boot, refused and out-of-range
writes and pre-acceptance aborts, no ready/ack, and the explicit open connection when
unused. The relation to the mark is correct: the live writes precede the unchanged group-7
completion mark, and the test checks both that ordering and the unchanged mark count.
The clock domain (`clk_i`, consumer owns the crossing) is correct. The integrator guide §8
already states that these outputs are combinational reads of `clk_i` registers. The docs
gates pass (`receipts/09-docs-gates.log`), and the `07 §3.4` cross-reference resolves.
**(4) Area.** The author's whole-top xc7 mapping (at `691f1d2`, RTL-token-identical to
head): LUT 66,461 → 66,439, and FF 32,462, RAMB 17 and DSP 4 unchanged, with OBUF +1.
My own out-of-context store synthesis, base vs head (`receipts/10-*`): FF 773/773, RAMB
2/2, LUTRAM 22/22, DSP 1/1 and CARRY4 117/117 are all unchanged, with OBUF +1. LUTs go
1345 → 1277, which is mapping variation, not added logic. No new state, and the area delta
is trivial.
**(5) Parent consumer gates, with the whole project judged.** The public author-r2
receipts show all 12 prescribed consumer commands at rc 0. That run used parent `7eb3b0d4`,
the supplied patch (`KL_pp_shadow.sv` +2 open-port lines and `measure_test_evidence.py` +3
reader-disposition lines, SHA-256 `1de2a73a…`) and the processor gitlink at `a9b7874`.
pp_shadow gives 402/0 in each of three builds. The processor port-contract count is
111 ≤ 111. DUT-source readers are 0 ≤ 0 and wall-clock files 3 ≤ 3. Builder gate 11
(utilization calibration) is SKIP because the real report is absent. I read the parent at
`7eb3b0d4` read-only. It binds the processor by explicit named ports (`u_pp`), and
`measure_test_evidence.py` already dispositions the sibling `gsi_mutants.py`. So the
open-port line and one reader disposition are exactly what the new pin needs. Parent
`990f965` is an ancestor of this PR's base, so that consumer run also covers the five
intervening processor commits. Hosted CI at the exact head: `hdl` push and pull_request
runs, 6 jobs, all executed and successful. The only skipped step is the cached Verilator
build (`receipts/14-public-evidence.log`).

## 3. Findings

### R334-F1 — MINOR — Docs, Tests
- **Where:** `tb/pp_top/pp_top_wrap.sv:312-332` at head.
- **What:** the existing `//!` bundle ("These three observe the effects themselves: the
  dynamic store's accepted-write counter, the OP_NVM_MARK strobe and the OP_NOTIFY_ENQ
  strobe") documented `dbg_dyn_writes_o`, `aecp_nvm_stb_o`, `aecp_nvm_mark_o` and
  `dbg_notify_enq_o` as one contiguous group. This PR inserted `aecp_name_wr_o` and
  `dbg_name_live_we_o`, each with its own `//!` block and followed by a blank line, between
  `dbg_dyn_writes_o` (`:320`) and `aecp_nvm_stb_o` (`:330`). That detaches the bundle
  from three pre-existing ports.
- **Authority / evidence:** the parent's accepted port parser (`check_port_contracts.scan_ports`,
  fetched read-only at parent `7eb3b0d4`) reports this file at 162 undocumented ports at
  base and 165 at head. The newly undocumented ports are exactly `aecp_nvm_stb_o`,
  `aecp_nvm_mark_o` and `dbg_notify_enq_o` (`receipts/12-parent-rules-focused.log`).
  Moving only the two new ports, with their contracts, after `dbg_notify_enq_o` restores
  162 with no effect or name port undocumented (`receipts/13-harness-bundle-probe.log`).
  Round-2 finding 3 names the harness explicitly. The round-2 PR text says it "restores the
  effect-strobe documentation bundle so the added port creates no documentation debt",
  and it did that for the engine, where the same insertion pattern cost ten ports. The
  parent gate scans only `hdl/`, which is why it stayed green (111 ≤ 111) while this
  harness debt went unmeasured.
- **Impact:** new documentation debt introduced by this PR in the harness that states the
  test contract. Three existing observation ports lose their contract under the project's
  accepted form, and the "these three" prose now sits above ports it does not describe.
  There is no functional impact.
- **Required outcome:** place the two new harness ports so that the existing bundle again
  covers its four declarations contiguously, for example after `dbg_notify_enq_o` or before
  the bundle comment. Keep both new `//!` contracts. No RTL or behaviour change.
- **Verification:** `scripts/13-harness-bundle-probe.py` (or `scan_ports`) on the fixed
  file reports 162 undocumented and none among the effect/name ports. `make -C tb/pp_top
  name-writes` still reports `NW: 85 checks, 0 failures`, and the full pp_top stays 7751/0.

### R334-S1 — SUGGESTION — Tests, RTL
The store contract says "Held requests pulse only when accepted"
(`KL_aecp_desc_store.sv:187`), and the export excludes non-name writes. Neither
qualification is observable through the top with the dispatched microcode (M02–M04 and
M12 are equivalent). A small `tb/desc_store` check would pin both at the one level where
they are reachable. It would hold a name write while the store is walking or patching,
issue a non-name write, and assert `name_wr_o` only on the accepting edge. That would
protect the contract if the microcode or store sequencing ever changes.

### R334-S2 — SUGGESTION — Docs, Tests
`tb/pp_top/README.md:29` says the wrapper tap checks alignment "independently of the
exported wire". In the shipped store, the tapped live `name_we_w` is the same net as
`name_wr_o` (`:545`). So the tap is independent of the engine and top wiring, not of the
store expression; faults there are caught by byte-exact readback instead. Wording such as
"independently of the engine/top export path" would be exact.

### R334-S3 — SUGGESTION — Docs
02 §8.1 (`02_interfaces.md:556`) replaced "combinational reads of `clk_i`-domain
registers" with "in the `clk_i` domain". `aecp_name_wr_o` is an unregistered
combinational function of µCPU E-stage and store state. Saying so in §8.1 (register in
`clk_i` before any pulse capture or crossing) would keep that page self-contained. The
integrator guide §8 already says it.

## 4. Prior findings at this head

| Prior finding (manager round 2, at `691f1d2b`) | Status at `a9b7874` | Reviewer evidence |
|---|---|---|
| 1. C++ long function in `sim_main.cpp` (parent Rule 11) | RESOLVED | parent `check_cpp_idiom.scan` on head: every rule 0, no function > 100 lines (`receipts/12-*`) |
| 2. Undocumented public Python functions (Rule 12) | RESOLVED | parent `check_py_idiom.scan` on `name_wr_mutant.py`: every rule 0 |
| 3. Port contracts for added/changed ports (top, engine, store, harness) | RESOLVED for the gated `hdl/` surface (store, engine and top newly undocumented = none; the two added harness ports documented); **harness bundle regression retained as R334-F1** | `receipts/12-*`, `receipts/13-*` |
| 4. Wall-clock dependence in `name_wr_mutant.py` | RESOLVED | parent `uses_wall_clock` = False; the script has no deadline; verdicts come from completed simulation |

No prior public review findings exist on PR #121.

## 5. Lens detail

- **Conformance.** `SET_NAME`/`GET_NAME` wire behaviour (IEEE 1722.1-2021 §7.4.17/18,
  Milan v1.2 §5.4.2.11) is unchanged. The NW phase checks byte-exact SET responses, GET
  readback, ENTITY_LOCKED refusal carrying the current name, and complete error bodies for
  BAD_ARGUMENTS and NO_SUCH_DESCRIPTOR. The pre-existing conformance checks pass
  unchanged. The new port is an integration export with no protocol surface.
- **RTL.** The token diff, port diff, acceptance path analysis (store, µCPU and engine
  gating: `st_name_w` excludes `dyn_sel_w`/`strq_sel_w`), boot mux exclusivity, and all
  instantiations (the `tb/desc_mem_guard/wrap.sv` explicit sink, OOC and timer_map
  elaboration by name) were checked. Lint is 40/40 clean, with no new simulator warnings
  and no new state (FF counts identical).
- **Robustness.** Refused, out-of-range, truncated, stalled (delayed fetch) and watchdog-
  aborted SETs are all silent. Recovery keeps the last accepted name. Reset and boot
  loading are silent. Mid-command response voids (gather watchdog) cannot desynchronise
  the pulse from storage, because the pulse is the RAM write itself. That matches the
  documented "earlier accepted writes remain visible".
- **Tests.** 85 focused checks, the shipped mutant reproduced, and 14 reviewer mutants:
  every reachable-observable one killed, and the survivors proven equivalent. UNCLEAN
  only through R334-F1 (harness contract).
- **Docs.** The top, engine and store contracts, 02 §8.1, integrator §8 and the pp_top
  README are accurate. The docs gates pass. UNCLEAN through R334-F1.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_main.cpp` NW phase and name suite, `gen_ucode.py` SET/GET_NAME, pp_top 7751/0, base 7666/0 comparison | R334-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| RTL | CLEAN | `KL_aecp_desc_store.sv`, `KL_aecp_engine.sv`, `protocol_processor_top.sv`, `KL_aecp_ucpu.sv` handshake, token diff, port diff, lint 40/40, store OOC area | R334-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| Robustness | CLEAN | NW refusal/stall/abort/recovery scenarios, store state machine exits, reachability probe, boot-mux exclusivity | R334-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| Tests | UNCLEAN (R334-F1) | `sim_main.cpp`, `pp_top_wrap.sv`, `name_wr_mutant.py`, `Makefile`, shipped campaign, 14 reviewer mutants, donor suites | R334-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| Docs | UNCLEAN (R334-F1) | `02_interfaces.md` §8.1, `integrator.md` §8, the three `//!` contracts, `tb/pp_top/README.md`, `pp_top_wrap.sv` contracts, docs gates | R334-1 | a9b7874d415d935949becd7ccfd58799927efb08 |

## 7. Real limits

- The prescribed simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`
  **does not exist**. I used the same pinned installation that the same-head wrapper
  targets, verified as Verilator 5.050 rev v5.050 (`verilator_bin` SHA-256 `44898b22…`,
  `receipts/00-identity.txt`), through a packet-local wrapper. Scratch copies capped
  Verilator build parallelism at `-j 8`; nothing else was changed.
- The parent consumer gates were **not** executed by me: full parent banks were out of
  scope. My consumer evidence is the public author-r2 receipts, plus a read-only reading of
  the parent at `7eb3b0d4` and the parent's per-file scanners applied to processor files.
  I found no manager-produced consumer or bank receipts in the public evidence tree.
- Consumer builder gate 11 (utilization calibration) is SKIP, because the real
  implementation report is absent. That is not coverage. Physical calibration is NOT RUN,
  and hardware and field behaviour are not proven.
- Whole-top area is the author's measurement at `691f1d2` (RTL-token-identical to head).
  My own synthesis covers only the store, out of context. Full synthesis, portability and
  the full processor suite bank were not rerun by me; hosted CI at the exact head ran them
  successfully.
- My store area probe briefly left an empty untracked `abc.history` in the review clone
  (the synthesis tool's working-directory file). I removed it, fixed the script, and
  re-verified the clone: HEAD, tree, index == tree, all 248 blobs and modes re-hash, no
  residue, and 0 gitlinks (none required in this repository) (`receipts/11-*`).
- Receipts have the host home directory replaced by `$HOME`.

## 8. Pending manager duties

- Resolve R334-F1, then re-review at the new head.
- Build and validate the final current-dev candidate at the merge turn (source base
  `0922e434`, live parent dev `7eb3b0d4`). Own hosted/act acceptance.
- Publish or link the manager's own consumer-bank receipts at the final head. The parent
  pin bump must carry the open `.aecp_name_wr_o()` line (or the real #502 connection) and
  the `name_wr_mutant.py` reader disposition, or parent strict lint and the evidence
  ratchet fail.
- Obtain the second independent review. Physical calibration and hardware remain open.

## 9. Receipts

All listed in `MANIFEST.sha256`. Scripts `scripts/00`–`14` are portable (packet-relative,
clone path overridable with `CLONE=`). Key receipts: `00-identity.txt`, `01-portdiff.log`,
`02-rtl-tokens.log`, `03-*`, `04-shipped-mutation/`, `05-reviewer-mutants/` +
`05-summary.txt`, `06-*`, `07-*`, `08-*`, `09-docs-gates.log`, `10-*`, `11-restore-verify.log`,
`12-parent-rules-focused.log`, `13-harness-bundle-probe.log`, `14-public-evidence.log`.

R334-1 FINISHED
