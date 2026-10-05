[A542] REVIEW READY (round 4)
Commit: `e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d` on local branch `665-f0-mailbox` (not pushed), tree `ce7e90dd`. It is round-3 head `3ebd6ca3` plus 4 one-line commits (`c11735c6`, `98205382`, `a440f737`, `e6420c0f`). Dev is still `28f9666f`, fetched at the start and again before this comment, so there is no merge this round.

**Changed**, per the round-4 assignment (5999248955), R496-3 (5999143101) and R497-3 (5999243199):

1. **Owed DEPARTINGs are bounded by construction (R497-3 F1).** I took the assignment's first option: coalescing under a stated rule.
   - **The rule** (`adp.h`, `ADP_DEPARTING_OWED_MAX` 2):
     - at most two ENTITY_DEPARTINGs are owed: the oldest, with its SHUTDOWN's index, and one queued behind it, which carries 0;
     - a SHUTDOWN that finds both owed adds no third. It is coalesced into the queued one and counted in `departing_coalesced`, so the condition is not silent;
     - why this keeps the wire semantics: the coalesced DEPARTING would also carry 0, and nothing the interface sends can leave between the two (an AVAILABLE never passes an owed DEPARTING), so it could only repeat the queued frame back to back. The wire keeps every distinct frame, in order;
     - no receiver acts on the repeat: a Milan listener that took the earlier DEPARTING is in TK_NOT_DISCOVERED, where RCV_ADP_DEPARTING is ignored (Milan v1.2 Table 5.54), and IEEE 1722.1-2021's `removeEntity` (6.2.6.3.5) has no record left to remove.
   - **Unchanged:** `adp_set_enable` gains no precondition, and a poll still sends one frame.
   - **A21 in `test_adp.c`:**
     - the second SHUTDOWN takes the last place: two owed, the oldest with index 1, none coalesced;
     - the next SHUTDOWN is coalesced and counted, the oldest keeps index 1, and its run's owed AVAILABLE is dropped;
     - after 100,000 more pairs, two are still owed and 100,001 are counted;
     - with room, the wire carries DEPARTING 1, one DEPARTING 0, then the restart's AVAILABLE 0 at its TMR_DELAY expiry.
   - **Defects:** `coalesced-departing-uncounted`, `coalesce-drops-queued-departing` and `coalesce-overwrites-oldest-index` are caught by A21. `departing-queue-unbounded` (round 3's counter restored) is caught by E5.
   - **R497-3's public-API probe at its 2^32 scale** (a copy with one print added): 2 owed plus 4,294,967,294 coalesced and counted, 4,294,967,296 in all. It still exits 1 by its own each-stays-owed criterion, which is the criterion this rule replaces.
2. **The latency statement matches the behaviour (R496-3 F1).**
   - **`ctrl_loop.h` A3** is restated: a response with k frames owed ahead of it is committed in pass k + 1, counted from the first pass that starts after the room returns, and not before the pass that takes its input. A module bounds k.
   - **`adp_mbx.h`** gains an "owed frames" paragraph, `ADP_MBX_OWED_PASSES` (3: the later of k + 1 with k at most 2, and an event's pass 2) and `ADP_MBX_OWED_ACCESSES` (4 x 407 = 1,628, with a pass already running).
   - Where the headers said a response is committed in the pass that takes its input, they now say it holds "under A3". The design page's A3 bullet and service-latency section say the same.
   - **E5** runs 1, 2 and 64 SHUTDOWNs behind a full ring through the driver, the model's timer and the loop, with the expiry taken before and after the room returns:
     - the AVAILABLE is committed in pass k + 1 exactly (2, 3 and 3);
     - measured cost: 63, 69, 93, 99, 93 and 99 accesses, against 1,628;
     - the wire carries DEPARTING 1, (DEPARTING 0,) AVAILABLE 0;
     - the machine then sits in WAITING with TMR_ADVERTISE armed and nothing owed.
   - **Defect:** `departing-queue-unbounded` fails E5.
   - **R496-3's `probe_owed_bound.c` against the head:** k = 0, 1 and 2 give passes 1, 2 and 3 as before. k = 3, 16 and 64 now give pass 3 at 93 to 99 accesses (round 3: passes 4, 17 and 65, up to 1,959 accesses).
3. **The three unguarded legs are checked (R496-3 F2).** The core is unchanged: it was correct on all three.
   - **A18:** a link loss during the restart, before and after its TMR_DELAY expiry, keeps the owed DEPARTING (index 1) and drops only the run's owed AVAILABLE. The link's return starts a new run, and the wire then carries DEPARTING 1, AVAILABLE 0.
   - **A19:** a GM change, an ENTITY_DISCOVER and a stray expiry in DELAY each leave the owed AVAILABLE owed, with no timer started. The next poll with room sends it and enters WAITING.
   - **A20:** a link loss drops an owed AVAILABLE at once, before any poll. After the link returns, a poll sends nothing until the new TMR_DELAY expires.
   - **Defects:**
     - R496-3's three copies, by name: `link-loss-drops-owed-departing` (A18), `gm-change-drops-owed-available` (A19) and `link-loss-keeps-owed-available` (A20);
     - two siblings: `discover-drops-owed-available` and `stray-expiry-drops-owed-available` (A19).
   - **R496-3's `adp_reviewer_mutants.py` against the head:**
     - all 7 applicable copies are caught;
     - `second-shutdown-overwrites-index` reports "PATCH SITE NOT UNIQUE (0)", because its line is the one item 1 replaced. It is re-planted at its new site in `ctrl_mutants.py`, where A16 catches it.
   - **`probe_owed_rules.c`:** the head is correct on L1 to L3, and each planted copy is wrong exactly as in R496-3's run.
4. **Merge dev:** not needed; dev has not moved.

Files changed since `3ebd6ca3`:
- `sw/firmware/ctrl/adp/{adp.c,adp.h,adp_mbx.h}` and `sw/firmware/ctrl/loop/ctrl_loop.h`;
- `sw/firmware/ctrl/test/{test_adp.c,ctrl_mutants.py}` and `sw/firmware/ctrl/README.md`;
- `docs/design/MAILBOX_SPLIT.md`.

Nothing under `hdl`, `sw/litex`, `sw/builder`, `configs`, `avdecc`, `milan_baremetal`, `syn` or `tb` changed, and no gitlink.

**Validation** (all at `e6420c0f`, each with its own log and rc file, 58 rc files, all 0; the tree is clean with nothing ignored left):
- **Firmware:** `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>` gives 757 checks:
  - model 134, port 81, adp 163, walk 320, entity 45, rv32 1, lwsrp 13;
  - **51 of 51** firmware defects caught, and both lwSRP pin refusals ok;
  - RV32I text 11,520 B, bss 170 B, no heap symbol.
- **Mailbox suite:** `make -C tb/verilator/mbx -j16` (Verilator 5.050, from clean) gives 134 Wishbone + 179 AXI4-Lite + 13 co-simulation checks (the co-simulation runs the round-4 firmware), 0 failures, quick mutants 4 of 4. `mutants.py --jobs 4`: both controls ok, **46 of 46** caught. `suite_tally.py --verdict`: rc 0.
- **Builder bank:** `test_builder.py --require-rv32` (LiteX interpreter given) gives ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the Arty route report is not on this host, as in every round). Gates 23f and 23g elaborate all five recipes.
- **Scope and contract:** `ci_scope.py --selftest` PASS; `ci_events.py --check` and `--selftest`; `gen_mailbox.py --check --crosscheck` and `--selftest`.
- **Other gates:**
  - `test_nvm_firmware.py --self-test`;
  - `lint_rtl.py --check` and `--self-test`, and Yosys on the three mailbox tops (full and elaborate);
  - SoC and RTL source lists (with self-tests), bare-metal-only (with self-test), sweep/deploy/entity shapes, wire accountability, `pp_srcs`;
  - the SV/C++/Python/shell idiom gates with their self-tests, hygiene, TODO ownership, test evidence, naming, port contracts, fail-fast (the same notes as round 3);
  - `gen_module_matrix.py --check`.
- **Docs gates:**
  - `docs_check`; em-dash against `fa450d30` (0 findings over 2,304 added lines) and its self-test; `gen_toc` (3 modes);
  - doc paths, style, map, gPTP, solution, submodule, PNG, feature status, archive;
  - `git diff --check` against `origin/dev` and against `fa450d30`.
- **Default build unchanged, by file identity.** Round 4 changes no file the gateware export reads, so round 3's export comparison against dev `28f9666f` stands: 22 of 22 files equal for all five configs.

**Acceptance criteria:**
- Round-4 items 1 to 4 are met, with the evidence above.
- Lane items and round-2 and round-3 items remain met.

**Open risks/questions:**
- **The coalescing rule** rests on the assignment's option 1. A third or later SHUTDOWN behind a stalled ring sends no frame of its own. The wire loses only a back-to-back repeat of DEPARTING 0, which would also have been one more chance against frame loss; ADP handles loss with valid_time, not repetition.
- **Not run:**
  - `act` and the hosted contexts (the head is not pushed);
  - `xvlog_gate.py`, a new switch-on OOC area, the default-build exports, the sw/litex tests and `gen_hdl_reference`. Each reads only RTL, SoC or LiteX files, which round 4 does not touch, so the round-3 results stand by file identity.
- **Re-review scope:** round 4 changes ADP firmware source and its stated bound, so Conformance, RTL (architecture), Robustness, Tests and Docs all need re-review at this head.
- **R497-3 R1 = R496-2 R1** (RESIDUE, `CI_WORKFLOWS.md` wording) is left for the residue checklist.
- **Unchanged limits:** the SEQ count belongs to one firmware run, and time per access (A4) is not measured.
