[R867] NEGATIVE - exact head 66c6edf3f0d05915ee8ddb7346302013833cf66a

Round R867-1, internal cleared-context review of kebag-logic/milan-fpga PR #947 (issue #946, relates #665), a member of the flip train PR #945 (step 12).
Head `66c6edf3f0d05915ee8ddb7346302013833cf66a`, tree `a37bcaecd8c7761f5da29b47b805dbe84bc39ae9`, on dev-soft-core `cb96336d`, six commits. The head commit changes only `sw/firmware/ctrl/plat/README.md` (+2 lines). Every other file is code-identical at `0749e0d8`, the commit the author's receipts name.

Verdict: NEGATIVE. The fix is correct, race-free for what it covers, and well tested. Three MINOR findings remain open: the ROM ledger the owner's 2026-11-15 rule requires was not raised, so an existing check turns red; the poll's owed-flag clearing is untested; and the follow-up tickets for F-G2 and the release image's F-G1 are not filed. One RESIDUE. No BLOCKER and no MAJOR.

## What was reconstructed, in order

1. AGENTS.md, CONTRIBUTING.md (by AGENTS reference), docs/README map.
2. Issue #946 body and both public comments (TAKEN, REVIEW READY). PR #947 body and its two public comments (review starts). Owner decision of 2026-11-15 on #665 (`issuecomment-6892332745`).
3. Authorities: Milan v1.2 Table 5.6 / 4.4.2.2 (as cited); IEEE 1722.1-2021 7.4.9, 7.4.16, 8.2 (as cited); `docs/reference/REGISTER_MAP.md` 0x800 window; the LCTX contract in `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` header; `aecp/aecp_face.h`/`.c` (publish, owed, commits, applied); `docs/design/SPLIT_CONTROL_MEMORY.md` section 5; MAILBOX_SPLIT (no contract file is in the diff).
4. `git diff cb96336d..66c6edf3`, 15 files, and the six commits.
5. Executable evidence: my own runs (below) first. Then the author packet `review-evidence/946-r1` (archive `7bb94e82`, fetched into a scratch bare repository).

Prior public review findings on PR #947: none. The PR has no review and no review comment, only the two review-start notices. Nothing to resolve or retain.

## Executions (all at exact head unless stated; receipts in `receipts/`)

| Run | Result | Receipt |
|---|---|---|
| Firmware gate, suites phase (`test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4`) | PASS, 81 arms `[ok]`, 0 failed/skipped; `platsinks` 8x8/1if 5/5 and 1x1/1if 5/5 | `fw_suites_head.log` / `.rc` = 0 |
| The 19 sink planted defects through `ctrl_mutants.campaign` (driver `run_sink_campaign.py`; full-table "named by no defect" check kept) | 19 of 19 caught on their named tests, 0 tests unnamed | `sink_campaign_head.log` / `.rc` = 0 |
| Same on the composition (train `b1f1161b` + head, merge-tree `74c60aaa`) | 19 of 19 caught | `sink_campaign_composition.log` / `.rc` = 0 |
| `plat` + `platsinks` arms at head | 3/3 arms PASS | `platsinks_head.log` |
| Shipped behaviour: head tree with `ctrl_plat.c` restored to `cb96336d` | `Sinks.S1` fails for each of inputs 1 to 7 by name ("input n holds none"); S2, S4, S5 fail; 1x1 passes (no context) | `platsinks_oldcode.log` / `.rc` = 1 |
| `plat` + `platsinks` on the composition | 3/3 PASS | `platsinks_composition.log` |
| `make -C tb/verilator/avtp_rxmon`, pinned Verilator 5.050 (identity printed in log) | every suite PASS; `CTXFMT N=8: 96 checks, 0 failures`; `ctxfmt_mutants.py` `5 checks: 5 PASS` | `avtp_rxmon_make_head.log` / `.rc` = 0 |
| `fw_coverage.py --check --jobs 4` | PASS (39 files); `ctrl_plat.c` and `ctrl_plat_csr.c` 100 % lines/branches after exclusions | `fw_coverage_head.log` / `.rc` = 0 |
| Reviewer probes (`run_extra_probes.py`) | R1 caught by S2; **R2 escaped every check (0 failed)**; R3 caught (by S2) | `extra_probes_head.log` |
| `plat_ledger.py` at base `cb96336d` | PASS: 8x8-if1 rom 130,504 B, 56 RAMB36 | `plat_ledger_base.log` / `.rc` = 0 |
| `plat_ledger.py` at head | FAIL: 8x8-if1 rom 131,464 B, **56.5 RAMB36, link REFUSED** by `ctrl_plat_image.py` | `plat_ledger_head.log` / `.rc` = 1 |
| `plat_ledger.py` on the composition | FAIL: 8x8-if2 rom 140,008 B, **63 RAMB36 past its 62.5 entry, link REFUSED**; 8x8-if1 58 PASS | `plat_ledger_composition.log` / `.rc` = 1 |
| Size-fixture split images (the CPU-budget images) sha256 | base = head at 1x1 and 8x8; composition = the train's recorded `55484254e638ed7f…` / `175418f4b5b1a9d4…` exactly | `budget_fixture_image_hashes.txt` |
| Release and budget image inputs, git object ids base vs head (28 paths incl. hdl, syn, constraints, configs, avdecc, sw/litex, milan_baremetal, sw/builder, aecp/mbx/loop/app/srp/maap, ctrl_nvm, fixture sources, link script, all submodule gitlinks) | 28 EQUAL, 0 differ | `release_and_budget_inputs.txt` |
| `git merge-tree --write-tree b1f1161b 66c6edf3` | rc 0, tree `74c60aaa…`; the train's own changes to milan_csr.sv are a one-line comment, and its datapath diff has no LCTX, monitor or fmt line | `composition_945.txt` |
| Review clone integrity after all probes | HEAD/tree exact, worktree = index = HEAD, no untracked file, gitlinks unchanged | `clone_integrity.txt` |

The RV32 compiler is the gate's first candidate, `riscv32-linux-gcc` (Buildroot 2026.05, 14.3.0). It has no `ci_rv32_sdk.py` receipt. My ledger and fixture-image byte counts and hashes equal the author's to the byte, so the two builds agree. Probes ran only in disposable copies under `scratch/`. The copy named `oldcode` held head plus the base `ctrl_plat.c` for the shipped-behaviour run. It was then reset and checked out as the composition. Home-directory path prefixes in the logs are shown as `~`.

## The eight focus checks

1. **Race freedom: met for every path the lane names.**
   - Bind and re-bind: a format moves only while its input is unbound (`aecp_commands.c:129` for SET_STREAM_FORMAT, `:188` `any_running` for SET_CONFIGURATION). A stream reaches a context only once ACMP publishes a settled stream_id, after the probe response (`tsn-c-stack/src/acmp.c:222-236`, `settled ? stream_id : 0`).
   - Boot: the boot writes every context after `ctrl_app_open_aecp` and before `ctrl_app_release_adp`, with no loop step in between (`ctrl_plat.c:357-361`). A restored binding cannot settle before READY.
   - Immediate write: the SET_STREAM_FORMAT write happens in the face's change port only when `!f->owed[0]` after the call, which means interface 0's commit was acknowledged (`aecp_face.c:77-103`). Otherwise the change is owed to the poll, written once the commit count moves (`ctrl_plat.c:178-201`). IN_PROGRESS re-does call the port again.
   - Arbitration: the RAM has one write port, the engine has priority, and a window write is accepted only in a free slot (`KL_avtp_rx_monitor_ctx.sv:719-723`). The engine writes FMT words only for stream 0 (`:1177`). The CSR holds the window request until the engine accepts it and holds off the next AXI write meanwhile (`milan_csr.sv:1117`, `:1665`, `:1888-1897`), so the closing SEL write lands after FMT_HI.
   - Clocks: the CSR and the monitor are both on `axis_clk` (`milan_datapath.sv:2824`, `:7820`), so the window adds no clock crossing.
   - Unbind: an unbind keeps the words (CF5, and the context RAM has no reset).
   - Owed path on live contexts: it rewrites a bound input's words with identical values, so the engine's two-cycle FMT read cannot tear.
2. **Stream 0 and CRF unchanged.** Stream 0 still uses `aecp_in0_fmt` (`milan_datapath.sv:3767`). `ctrl_plat_csr_sink_context` excludes index 0 and non-AAF subtypes (`ctrl_plat_csr.c:102`). C6 and S1 plants cover both.
3. **Release image byte-identical: proved by inputs, not by a built image.** All 28 release and budget input object ids are equal, the release placement compiles none of `sw/firmware/ctrl/plat`, and RTL is untouched (no `hdl/` path in the diff). A release image build is a builder bank and was not run.
4. **New tests fail on the old code by name, and nothing was weakened.** S1 fails for each of inputs 1 to 7 with the shipped `ctrl_plat.c`. 19/19 plants are caught at head and on the composition. The 4 engine plants plus the clean control give 5/5. CF1 reproduces the bench state at N=8. No existing test, check or acceptance text is removed or relaxed: the diff's eight deleted lines are each replaced by an extended form: the console's poll registration and its comment, the README's arm count, the campaign's `SOURCES` tuple (now also naming the sink suite), the Makefile's `.PHONY` and clean lines, and the wrapper's fixed `[1:0]` match index.
5. **CPU budget rows carry.** The size-fixture images are byte-identical base vs head, and on the composition they equal the train's recorded hashes. Boot delta 0.107 ms at 8x8 against the 20 s ADP-valid bound is the author's split-boot receipt (`boot/delta.txt`); I did not rerun the split boot simulation. The new per-pass poll in the product image is measured by no row (see F-2).
6. **ROM figures reproduced exactly**: 56 → 56.5 at 8x8/1if on dev-soft-core, and 62.5 entry vs 63.0 plan at the train's 8x8/2if. The entries were not raised as the owner's rule requires (F-1).
7. **F-G2 and F-G3 claims hold.** The parser keeps the highest enabled matching entry (`avtp_stream_parser.sv:189-199`), one context per PDU, so fan-out to two inputs is an RTL cause. #943 is open for the GSI `stream_dest_mac` defect. Neither F-G2 nor the release F-G1 has a ticket (F-3).
8. **Composes cleanly onto #945 `b1f1161b`.** merge-tree rc 0. The train's face changes (EDIT window, REBOOT gate, PHY) leave `publish`, `owed`, `commits` and the bound-input refusal unchanged. The sink arms and the 19-plant campaign pass on the composition.

## Findings

### F-1 MINOR — Docs, Tests — `sw/litex/ctrl_memory.py` LEDGERED / `docs/design/SPLIT_CONTROL_MEMORY.md` §5 / `sw/firmware/ctrl/plat/README.md:123` — ROM entries not raised as the owner's 2026-11-15 rule requires; the ledger check turns red
- **Authority / evidence:** The owner's decision of 2026-11-15 (#665 `issuecomment-6892332745`): "An image past its entry raises the entry to its measured size, at the next half tile, as named debt owed to S14". `plat_ledger.py` passes at base and fails at head: 8x8-if1 56.5 RAMB36, and `ctrl_plat_image.py` exits 2 "allocation over budget". On the composition it fails at 8x8-if2: 63 past the 62.5 entry, link refused. Receipts: `plat_ledger_{base,head,composition}.log`. The lane deliberately leaves the ledger untouched (PR body, "ROM"). `plat/README.md:123`, in the file this PR edits, still says "Every other point is within 56", which is false at this head.
- **Impact:** On dev-soft-core the 8x8/1if product image, the shape this fix targets, is refused at link. On the train composition the 8x8/2if product image is refused. An existing green check becomes red, and the authoritative memory document and README carry stale figures.
- **Required outcome:** Each image past its entry has the entry raised to its measured half tile as named S14 debt, with the ledger record (`ctrl_memory.LEDGERED`/`ctrl_memory_ledger.py`), SPLIT_CONTROL_MEMORY §5 rows and README statement current. Two ways satisfy this: on the lane for dev-soft-core's 8x8/1if (56.5), or as a publicly recorded step of the train composition that raises `platform-8x8-two-interfaces` to 63.0, with the lane only ever landing through the train.
- **Verification:** `plat_ledger.py --self-test` PASS on the lane head and on the composition. README/§5 figures match its POINT lines.

### F-2 MINOR — Tests, Robustness — `sw/firmware/ctrl/plat/ctrl_plat.c:196-198`, `sw/firmware/ctrl/test/test_plat_sinks.cpp:480-508` — the poll's owed-flag clearing has no test; a poll that rewrites every context on every pass escapes
- **Authority / evidence:** AGENTS §6 Tests and Robustness (repeated commands and idempotence; each test can fail for the defect it claims to cover). The README's new claim at `README.md:84` reads "The poll's own share is one comparison a pass". Reviewer plant R2 removes `sinks.owed = false;` from `plat_poll`. Every `plat`/`platsinks` check still passes (0 failed): `extra_probes_head.log`. S5 checks only that the words written since `from` hold the format in force, never that the rewrite happens once.
- **Impact:** After the first deferred change (SET_NAME, a lock, IDENTIFY, a STREAM_OUTPUT format), the product loop would rewrite all seven contexts on every pass. That is 35 window accesses plus a descriptor scan per pass, about 0.1 ms at 8x8 by the boot receipt. No CPU-budget row measures the product image (PR body says so), so neither the suites nor the budget harness would see the regression.
- **Required outcome:** A check that a deferred change is written once: for example, after S5's rewrite, further loop passes make no window write. That defect is then added to `sink_mutants.py`.
- **Verification:** The R2 plant (or its equivalent) is caught by its named test on its own words.

### F-3 MINOR — Docs, Conformance — PR #947 body "Known limitations" and issue #946 — follow-up tickets for F-G2 and the release image's F-G1 not filed while the PR says `Closes #946`
- **Authority / evidence:** AGENTS §4: newly discovered work becomes another public Issue. The PR names two items "for its own ticket": F-G2, one stream bound to two inputs, an RTL cause at `avtp_stream_parser.sv:189-199`; and the all-fabric image sharing the Table 5.6 defect, whose fix is RTL. An issue search on 2026-11-18 finds neither. #946 is their only public record. #943 exists for F-G3.
- **Impact:** Closing #946 leaves a known Milan v1.2 Table 5.6 non-conformance in the release image, and the F-G2 fan-out defect, with no open work item.
- **Required outcome:** Both issues are filed and linked from #946/#947, or #946 stays open naming them, before #946 closes.
- **Verification:** Both issue links are present on #946 and #947.

### R-1 RESIDUE — Docs — `tb/verilator/avtp_rxmon/sim_ctxfmt.cpp:5` — a work-lane name in a new source comment
- "the lane-A stack of avtp_rxmon_nx_wrap": "lane A" is a work-lane name (`docs/history/v1/NXN_ARCHITECTURE.md:929`). The owner's comment rule (2026-10-15) applies; the existing instances in the wrapper and `sim_main_nx.cpp` are tracked by #746. Exact fix: "the multi-stream RX stack of avtp_rxmon_nx_wrap".

No other wording defect was found in the delta's source comments: no bench label, reviewer ID, round or comment ID.

## Per-lens results (same format; lenses with an open finding are UNCLEAN)

- `[R867] PASS RTL — KL_avtp_rx_monitor_ctx.sv:719-723,1177; milan_csr.sv:1117,1665,1888-1897; milan_datapath.sv:2824,3767,7820; avtp_stream_parser.sv:189-199; avtp_rxmon_nx_wrap.sv:94-97,137 at 66c6edf3 — the window/engine write arbitration, the CSR request hold-off, one clock domain (no new CDC), stream-0 alias, engine FMT writes limited to stream 0, the parser's one-context match, and the wrapper's match-index width at N=4 (unchanged 2 bits) and N=8 (3 bits), against the LCTX contract and REGISTER_MAP 0x800; the RTL suite PASS with the pinned 5.050; the train composition leaves this path unchanged.`
- Conformance: UNCLEAN (F-3). Clean parts, examined at `66c6edf3`:
  - the AAF-above-0 formats now judged as Table 5.6 / 4.4.2.2 require (CF2, S1);
  - 1722.1 7.4.9 refusal of a bound input (`aecp_commands.c:129,328`, S2 and the `set-format-bound-accepted` plant) and SET_CONFIGURATION's `any_running` (`:188`);
  - SEL `{dir 0, idx}` and FMT_LO/HI at 0x824/0x828 → LCTX w2/w3 against REGISTER_MAP and `milan_csr.sv:1888-1897`;
  - no mailbox-contract file in the diff.
- Robustness: UNCLEAN (F-2). Clean parts:
  - unacknowledged commit (S3) and IN_PROGRESS re-do (S4);
  - unbind and silence unlock (CF5);
  - a write the cycle before a bind (CF4);
  - another writer's selection restored (C5, S1);
  - short descriptor, wrong interface/configuration/type (C6);
  - datapath reset leaves the words (context RAM has no reset);
  - 1x1 shape with no contexts.
- Tests: UNCLEAN (F-1 existing ledger check red; F-2 untested idempotence). Clean parts:
  - old-code failure by name;
  - 19/19 plants at head and on the composition, plus 4 engine plants and the clean control (5/5);
  - fw_coverage 100 % on both changed files;
  - 81 firmware arms PASS, the RTL suite PASS;
  - nothing weakened.
- Docs: UNCLEAN (F-1 README:123 and §5 stale, F-3 missing tickets; R-1 residue only). Clean parts: `plat/README.md:79-88` describes the writer, the timing and the race argument as the code does, and the `KL_avtp_rx_monitor_ctx` header already states that streams above 0 read FMT from the window.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-3) | aecp_commands.c:129,188,328; ctrl_plat_csr.c:70-104; REGISTER_MAP 0x800; milan_csr.sv:1888-1897; issue #946 AC; PR body | R867-1 | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| RTL | CLEAN | KL_avtp_rx_monitor_ctx.sv:719-723,1177; milan_csr.sv:1117,1665,1888-1897; milan_datapath.sv:2824,3767,7820; avtp_stream_parser.sv:189-199; avtp_rxmon_nx_wrap.sv; avtp_rxmon suite log | R867-1 | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| Robustness | UNCLEAN (F-2) | ctrl_plat.c:148-201,300-303,357-359; aecp_face.c:77-139; test_plat_sinks.cpp S1-S5; sim_ctxfmt.cpp CF1-CF5; extra_probes_head.log | R867-1 | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| Tests | UNCLEAN (F-1, F-2) | test_plat.cpp C5/C6; test_plat_sinks.cpp; sink_mutants.py; ctxfmt_mutants.py; fw_suites, sink campaign (head and composition), platsinks_oldcode, fw_coverage, plat_ledger base/head/composition receipts | R867-1 | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| Docs | UNCLEAN (F-1, F-3) | plat/README.md:79-88,123,127-135; SPLIT_CONTROL_MEMORY.md §5; REGISTER_MAP 0x800; PR body; issue #946; sim_ctxfmt.cpp header (R-1) | R867-1 | 66c6edf3f0d05915ee8ddb7346302013833cf66a |

## Real limits

- No hardware: issue acceptance item 3 (the bench's stream, power-cycle and soak items at 8x8/1if) is not met here. Acceptance item 1 is met in simulation only: CF2 binds all eight contexts at once, and S1 shows the product firmware writing the words. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No end-to-end simulation joins the real firmware's writes to a PDU's acceptance. The chain is shown in two halves with identical words: the firmware writes `02006000`/`02050220` (C5, S1, author boot receipt), and the RTL accepts on those words (CF2).
- The release image was not built; byte identity is shown by identical inputs. The split boot simulation, the twin and its plants, the docs workflow steps and the full sweep were not rerun; those figures are the author's receipts. No hosted or act result was inspected or claimed.
- The RV32 compiler is not the receipted `ci_rv32_sdk.py` install; its outputs match the author's byte for byte.
- Two-interface placement of AAF inputs on interface 1 was not examined beyond the interface-0 filter; the issue is scoped to 8x8/1if.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Disposition of F-1: who raises the 8x8/1if (dev-soft-core) and `platform-8x8-two-interfaces` (train) entries as named S14 debt, and in which commit.
- F-3 tickets, before #946 closes.
- R-1 to the residue checklist.
- The current-dev merge candidate (builder and native banks; source base `cb96336d`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), hosted/act acceptance, the gating bench run after composition, and the external review (R868).

## Packet

Portable drivers: `run_sink_campaign.py`, `run_platsinks.py` and `run_extra_probes.py`. Each takes `<checkout> <output> [jobs]`. Receipts are in `receipts/`; every published file is listed in `MANIFEST.sha256`.

R867-1 FINISHED
