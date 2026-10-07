# HANDOFF: [A559] lane F3 for #665 (ACMP on the bare-metal core), round 3 (area)

Status: STOP at `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` (issue #665 comment 6033939473).
The ruling's area target cannot be met with the behaviour unchanged: the term costs 357 LUT
(target 300) and 86 FF (target 120). Every gate below exits 0. Not pushed.

- Branch `665-f3-acmp`, round 3 on `8c2b58bf` (round 2's REVIEW READY head), three one-line
  commits, no rebase, no amend.
- Assignment: issue #665 comment 6032450078 ("F3 round 3 (area)").
- Scope: `git diff --name-only 8c2b58bf HEAD -- hdl sw/litex configs` lists
  `hdl/milan/mailbox/KL_mbx.sv` (generated) and `hdl/milan/mailbox/KL_mbx_rx.sv` only;
  `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md` and `mailbox.yaml` are byte-identical,
  so the register map is unchanged; no submodule moves; the mailbox is elaborated only under the
  default-off `--ctrl-mailbox`, so the default build and the shipping image read nothing changed.

## Round 3

### Commits

| Commit | Subject |
|---|---|
| `a00c2681` | KL_mbx_rx: the bound-talker table in distributed RAM, compared byte by byte as the identity arrives |
| `04dc6de5` | Mailbox suite: the table's byte compare, its reset and its timing, and their planted defects |
| `4f6216ab` | Describe the bound-talker table in distributed RAM and its measured area against the target |

### Measured area (the STOP)

Recipe unchanged from round 2 (`docs/design/MAILBOX_SPLIT.md` "Measured area": `KL_mbx` behind
`KL_mbx_wb` as `tb_mbx_top` with `HOST_P=0`, `xc7a100tfgg484-2`, 10 ns, Vivado 2026.1 defaults,
synthesized, placed and routed, under the shared lock, nothing else of this lane running). The
measured RTL equals the head's by sha256 (`KL_mbx_rx.sv` 289ac7d2..., `KL_mbx.sv` abeb8c58...).

| Block | LUT FC r2 | LUT r2 | LUT r3 | FF FC r2 | FF r2 | FF r3 |
|---|---:|---:|---:|---:|---:|---:|
| `KL_mbx_rx` | 1,151 | 1,951 | 1,481 | 1,069 | 1,076 | 1,155 |
| `KL_mbx` | 295 | 752 | 294 | 532 | 1,572 | 532 |
| `KL_mbx_evt` | 682 | 727 | 702 | 978 | 978 | 978 |
| `KL_mbx_tx` | 529 | 481 | 488 | 280 | 280 | 280 |
| `KL_mbx_wb` | 67 | 93 | 122 | 1 | 1 | 1 |
| **Total** | **2,745** | **4,025** | **3,102** | **2,860** | **3,907** | **2,946** |

WNS +0.402 ns, all 6,041 routable nets routed, no DSP, block RAM unchanged (1 RAMB36, 10
RAMB18); 128 SRL16E, 34 RAMD32 and 10 RAMS32 (`util_hier.rpt` sha256 05d3b666..., 2.3 KB, kept in
scratch). The term: **+357 LUT, +86 FF**. Breakdown: 64 LUT the shift registers (two SRL16E to a
LUT), 22 the read-back memory (six RAM32M), 271 logic (the byte compare and match flag, about 108
by synthesis; `BOUND_EN`, the owed copy and the two written-since-reset flags with their write
decode; the copier; the skeleton's decode and read-back select; +55 and +20 attributed to the
unchanged `KL_mbx_wb` and `KL_mbx_evt` by cross-hierarchy combining). FF: five flags per entry
(80) and the copier (8), two merged.

Variants measured with the same recipe, kept out of the tree:

| Variant | LUT | FF | WNS | Contract change |
|---|---:|---:|---:|---|
| head | +357 | +86 | +0.402 | none |
| `BOUND_EID` not cleared by a reset | +337 | +56 | +0.096 | `BOUND_EID` keeps its value through a reset (0 after configuration) |
| that, and `BOUND_EID` write-only | +300 | +56 | +0.208 | and it reads 0 |
| (earlier version) read-back registered into the answer mux | -15 vs its base | +34 | | none; not kept |

Tried and dropped, each measured: one compare memory per entry in single-port LUTRAM (one bit per
LUT, RAM16X1S: 3,240 LUT); a copy at every `BOUND_EID` write (a burst of sixteen rewrites left
Q13's frame behind the copies); a one-hot copier pointer (-4 LUT for +18 FF, synthesis).

### Changes (file:line at the head)

| What | Where |
|---|---|
| Ports: the host's decoded access in, the stored word, its validity and `BOUND_EN` out | `KL_mbx_rx.sv:86` to `:94` |
| `NE_C`, `KW_C`, `RD_C`; `BO_C` from the contract's tables; elaboration `$error` if `eq_bound` terms read two fields or more than 32 entries | `KL_mbx_rx.sv:124`, `:131`, `:155` |
| Per-entry state (`en_r`, `vlo_r`, `vhi_r`, `owed_r`, `match_r`), copier (`cp_busy_r`, `cp_k_r`, `cp_b_r`) | `KL_mbx_rx.sv:217` |
| A write owes a copy (`howe_w`); the copier's step gives way to the host | `KL_mbx_rx.sv:238`, `:247` |
| Read-back memory, its written-since-reset flag at the read index | `KL_mbx_rx.sv:250`, `:261`, `:271` |
| Copy byte (lane, 0 when unwritten), per-entry shift registers (`g_cmp`) | `KL_mbx_rx.sv:281`, `:287` |
| Arrival interface's table (`fok_w`, `fif_w`), liveness, byte compare, `bound_hit_w` | `KL_mbx_rx.sv:306`, `:307`, `:315` |
| Copier, host writes, match flags | `KL_mbx_rx.sv:317`, `:331`, `:349`, `:356` |
| Verdict reads one hit for every `eq_bound` term | `KL_mbx_rx.sv:430` |
| Skeleton: `BOUND_CODE`, `_bound_decode` (bit fields), the two reads, the instance | `mailbox_skeleton.py:46`, `:224`, `:349`, `:492`; generated `KL_mbx.sv:119`, `:246`, `:512` |
| Generator refusals: strides not powers of two, `eq_bound` on two fields | `mailbox_skeleton.py:454`, `:458`; self-test arms `gen_mailbox.py:297`, `:299` |
| Bench: part of a frame (`send_bytes`) | `bench.hpp:128` |
| Suite: Q14 to Q17 (shared), Q18 to Q21 (RTL only), `offer_stalled`, `run_bound_timing` | `suite.hpp:98`, `:222`, `:1427`, `:1457`, `:1495`; `sim_main.cpp:43` |
| Planted defects (30 rules, 60 arms) | `mutants.py:297` |
| Docs | `MAILBOX_SPLIT.md:584` (design), `:722` (verification), `:849` (area), `:925` (open item); `tb/verilator/mbx/README.md` |

### Tests and the planted defects each catches (RTL campaign, both adapters)

| Check | Arms that must fail it |
|---|---|
| Q12 a bound talker's AVAILABLE delivered | `pkg-adp-bound-term-dropped`, `rx-bound-copy-halves-swapped`, `rx-bound-byte-index-off-by-one`, `rx-bound-copy-lanes-reversed`, `rx-bound-copy-not-owed-on-enable` |
| Q12 no other message_type | `pkg-adp-bound-term-any-type` |
| Q12 an identity differing in [63:32] only | `rx-bound-low-word-only` |
| Q12 an entry with BOUND_EN clear | `rx-bound-enable-ignored` |
| Q12 a frame that ends inside entity_id | `rx-bound-field-length-unchecked` |
| Q12 the last entry | `rx-bound-first-entry-only`, `rx-bound-scan-skips-the-last-entry` |
| R1 each entry at its own address, BOUND_EN one bit | `rx-bound-entry-write-lands-in-entry-0`, `top-bound-entry-decoded-as-0`, `top-bound-en-read-from-eid` |
| Q13 an index with no interface (one interface) | `rx-bound-table-of-interface-0` |
| Q13 a talker bound on interface i (two interfaces) | `rx-bound-enable-of-interface-0`, `top-bound-write-ignores-interface`, `rx-bound-taps-of-interface-0`, `rx-bound-copy-into-interface-0` |
| Q14 the bound talker right after another talker | `rx-bound-flag-never-rearmed` (stale flag across frames) |
| Q14 one differing in its first identity byte right after a match | `rx-bound-flag-carried-into-the-next-frame` (stale flag across frames) |
| Q15 one identity byte differing, each of eight | `rx-bound-last-byte-uncompared` |
| Q16 the new talker after a rewrite with BOUND_EN set | `rx-bound-copy-not-owed-on-rewrite` |
| Q17 every entry reads 0 after a reset | `top-bound-unwritten-word-read-raw`, `rx-bound-valid-kept-through-reset` |
| Q17 an entry enabled with no identity holds talker 0 | `rx-bound-unwritten-word-copied-raw` |
| Q18 BOUND_EN cleared and set inside a stalled identity | `rx-bound-liveness-at-the-verdict-only` |
| Q19 BOUND_EN set again inside a stalled identity | `rx-bound-live-while-owed` |
| Q20 the entry copied while another is read | `rx-bound-copy-ignores-the-host` |
| Q21 a rewrite at each of 32 clocks of a copy | `rx-bound-copy-not-restarted` |

Every arm is caught by the check named in its row (`mutants.py` requires the named `[FAIL]`):
141 of 141 with the four positive controls (380/425 checks at one and at two interfaces). No new
model twin: the model's reset clears its whole state in one `memset`, and the other round-3
rules are the RTL's own mechanisms; the 27 ctrl-campaign defects that run the model arm (and so
the grown suite) are all still caught.

### Coverage

`python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4`, rc 0: unchanged from round 2 (the
firmware did not change); every ratcheted file 100 % after exclusions, `acmp.c` 729/729 and
342/342, `mbx.c` 185/185 and 68/68.

### Gate table (round 3, at `4f6216ab`)

Each command run on its own, rc recorded, output never piped. Verilator is the pinned 5.050.

| Gate | Command | rc | Result |
|---|---|---:|---|
| mbx suite | `make -C tb/verilator/mbx clean`, then `make -C tb/verilator/mbx run-wb run-axil run-cosim run-if2` | 0 | Wishbone 380, AXI4-Lite 425, co-simulation 32, two interfaces 380 / 425, model 369 |
| mbx RTL campaign | `python3 -B tb/verilator/mbx/mutants.py --jobs 2` | 0 | 141 of 141, four positive controls, 491 s |
| mbx quick arm | `python3 -B tb/verilator/mbx/mutants.py --quick --jobs 2` | 0 | 5 of 5 |
| contract | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | 0 findings |
| contract | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | 0 arms failed (46, two new) |
| lint | `python3 scripts/lint_rtl.py --check --self-test` | 0 | 90 <= ratchet 90 |
| Vivado front-end | `python3 scripts/xvlog_gate.py --check` (xvlog on PATH, under the lock) | 0 | 0 findings in `hdl/`; the processor's 2 at the ratchet |
| Yosys | `syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil` | 0 | 3 of 3 pass |
| firmware-unit | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32` | 0 | every arm PASS, `model` 23 tests |
| ctrl campaign, model arm | the 27 defects whose arm is `model`, planted with the campaign's own `campaign()` in two slices | 0 | 27 of 27 |
| coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | 17 files at the ratchet |
| docs workflow and idiom | round 2's 71 commands (`check_em_dash.py --base 910f338d...`), with the contract and lint rows above | 0 | 74 of 74 |
| OOC area | the recipe above | 0 | +357 LUT, +86 FF: **target not met** |

Not rerun, as nothing they read changed since round 2's runs: the full ctrl campaign's other 321
defects (firmware sources unchanged), the store and saved-state gates, the builder bank (reads
no mailbox file), `fw_coverage.py --selftest` and `tally_selftest.py`.

### Open questions and risks

1. **The decision the STOP asks for:** accept +357 LUT and +86 FF, or take one of the measured
   contract changes (the second meets +300 exactly), or another direction.
2. **Copy latency** is derived from the RTL (176 clocks for sixteen entries owed at once, plus a
   clock per host access to the tables), not measured on its own; the suite waits 256 clocks.
3. A host that held the bound-talker registers every cycle would hold the copier off; the
   adapters leave every other cycle free.
4. Round 2's open questions stand (A4 timing, processor issue #168, hosted CI and `act`).

# Round 2


Status: REVIEW READY at `8c2b58bfa7bc0b9509cdfadb21f3ce89e72bcd28` (issue #665 comment 6032434205;
every gate below rc 0; the builder bank and the out-of-context area as stated in their rows). Not
pushed.

- Branch `665-f3-acmp`, round 2 from `351ae81f` (round 1's REVIEW READY head, PR #688).
- Round-2 assignment: issue #665 comment 6030067436. The `adp` term decision: comment 6029368753.
  Reviews answered: R531-1 (comment 6029581606) and R530-1 (comment 6030054402), their reports
  on the `665f3-review-evidence` branch (`review-evidence/665f3-r1/reviews/`). Processor issue
  Mister-M-alt/protocol-processor-control-plane-avb-milan#168 carries LD1 to LD3 and TD1.
- Merges, each `--no-ff`: FC round 2 `db9aa8c9` (`08130eca`), then dev `910f338d` with #679
  (`b03929fc`). Conflicts and how both sides were kept: below.
- Scope: the only RTL changed is inside the mailbox block (`hdl/milan/mailbox/KL_mbx.sv`,
  `KL_mbx_pkg.sv`, both generated, and `KL_mbx_rx.sv`); `git diff --name-only b03929fc HEAD --
  hdl sw/litex configs` lists those three only, and no submodule moves. The mailbox sources are
  in `sw/litex/milan_soc.py`'s list only under `--ctrl-mailbox` (default off) and `KL_mbx`'s
  port list is unchanged, so the default all-fabric build and the shipping image read nothing
  this round changed. The register-map change is the mailbox window's own (contract 2.1).

## Commits (round 2)

| Commit | Subject |
|---|---|
| `08130eca` | Merge lane FC round 2 (db9aa8c9) into lane F3 |
| `b03929fc` | Merge dev (910f338d, #679) into lane F3 |
| `5a8cc3d7` | Mailbox contract 2.1: the bound-talker term and table (generator, KL_mbx_rx, the host model) |
| `a76aec98` | Mailbox suite: the bound talkers through both adapters and at two interfaces, RTL defects, run-cosim relink |
| `c28743c1` | ACMP: AVTP version 0 only, TMR_NO_RESP from the accepted send, the slot range compared, the admit port |
| `63ab3d68` | ACMP tests and planted defects for the round-2 findings, `acmpif2`, the co-simulation |
| `ccb39a72` | Docs: the bound-talker term, the round-2 fixes and figures, the TD1 ruling |
| `a45a9563` | Lane F3's planted defects name B3's per-interface words |
| `1bde5d96` | Mailbox RTL defects: FC's own-MAC arm names its line beside the bound-talker table's |
| `b6877341` | KL_mbx_rx: comparators for the eq_bound term only (the area fix, below) |
| `8c2b58bf` | Record the out-of-context area of the bound-talker term |

Merge conflicts: FC round 2 into F3, `docs/design/MAILBOX_SPLIT.md` (FC's 316 checks and
DEFEND row kept with F3's co-simulation, ctrl and ACMP rows) and `sw/firmware/gtest/README.md`
(FC's eight model groups kept with F3's arms). Dev into F3: `sw/firmware/ctrl/test/ctrl_arms.py`
(the import list: F3's `HOST` and `NVM_DIR` kept, dev's `fw_rv32` taken and `RV32_CANDIDATES`
dropped as dev removed it) and `sw/firmware/ctrl/README.md` (dev's RV32 text kept with F3's
PyYAML reason). `ctrl_build.py` and `test_ctrl_firmware.py` merged cleanly; no check dropped.

## Findings and their resolution

| Finding | Change (file:line) | Test | Planted defects |
|---|---|---|---|
| The `adp` term (decision 6029368753) | `sw/mailbox/mailbox.yaml:55` (minor 1), `:60` (`bound_talkers: 16`), `:268` (`interface_bound_registers`), `:495` (`eq_bound`), `:517` (the adp channel's third term, message types 0 and 1); `mailbox_model.py:369` (`_check_blocks`), `mailbox_skeleton.py:41` and `:414`, `mailbox_emit.py`, `gen_mailbox.py:246`, `:288`; `KL_mbx_rx.sv:67`, `:161`, `:235`, `:245`; generated `KL_mbx.sv`, `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md`; model `mbx_model.c:349`, `:604`; firmware `acmp.h:304` (the `admit` port), `acmp.c:176`, `:441` (`admit`), `:479` (`sink_reset` keeps it), `:1199` (`acmp_open`), `acmp_mbx.c:14`, `:59`, `:137`, `mbx.c:118`, `ctrl_app.c:43` | suite Q12, Q13, R0, R1 (`suite.hpp:1276`, `:1336`, `:327`, `:404`) on both adapters, at two interfaces and on the model; A29 (two tests), B5, B8, C0, C3, C10, C11, F5, U5, D13; co-simulation | 24 RTL arms (12 rules, both adapters, two at two interfaces); 7 model twins; 6 driver; 10 core and adapter |
| R531-1-F1 AVTP version | `acmp.h:19`, `:146`; `acmp.c:53`, `:986`, `:1034` (both receive paths, before any decode) | A26 (BIND_RX, a talker command, PROBE_TX_RESPONSE, AVAILABLE, DEPARTING, a restored binding in PRB_W_AVAIL; versions 1 to 7 with version-0 controls); B9 through the real filter and adapter | `acmp-version-unchecked`, `acmp-adp-version-unchecked`, `acmp-version-bits-misread`, `acmp-header-version-1` |
| R531-1-F2 TMR_NO_RESP from the accepted send | `acmp.h:351` (`timer_held`), `:366` (`probe_of`); `acmp.c:254` (`transmit` returns SENT, OWED or LOST), `:316` (`sm_running`), `:660` (`send_probe` holds an owed probe's timer), `:687` (`probe_left`: starts it when that probe, by sequence_id, leaves), `:1093`, `:1154` | A27 (three tests: a stalled initial probe, the reviewer's 5 ms duplicate stall with its 402 ms response, the 404/405 ms boundary, command order, the single duplicate and its sequence_id, an expiry while owed, unbind, re-bind and success while owed), A23 updated | `acmp-owed-probe-timer-runs`, `-never-starts`, `-no-resp-2s`, `-sequence-unchecked`, `-unnamed`, `-names-the-next-sink`, `acmp-held-timer-expires`, `acmp-held-timer-armed`, `acmp-lost-probe-held`, `acmp-stop-keeps-the-hold` |
| R531-1-F3 slot range | `acmp_mbx.c:13`, `:71` (compared, never summed or narrowed); `acmp_mbx.h` init contract | B7: the last legal range taken (last interface on the last slot), the first illegal, 16, 256, 256 + 15, `UINT_MAX - N_IF + 1`, `UINT_MAX` refused | `acmp-slot-sum-wraps`, `acmp-slot-narrowed-first`, `acmp-slots-one-short`, `acmp-slots-past-the-bank` |
| R531-1-F4 owed-frame timing text | `docs/design/MAILBOX_SPLIT.md` "ACMP service latency": the reviewer's correction, with round 2's figures (the owed-frame bound is now 8,964 accesses, 8.96 ms at 1 us: it fits) | (docs) | (none: text) |
| R531-1-F5 poll contract | `acmp.h:424`: the reviewer's exact words | A19, E2 (unchanged) | (existing `acmp-poll-drains-everything`) |
| R530-1-F1 adapter at two interfaces | `ctrl_arms.py:57` (`acmpif2`: a copy of the tree with the generator's two-interface header; `mbx.h` includes the contract by quotes, so `-I` order cannot select it), `acmp_if2.cpp`; B3, B4, B6, B8 and the C paths loop over the interfaces (`test_acmp_mbx.cpp:289` to `:616`) | `acmpif2` arm, 19 tests | `acmp-one-slot-for-all-interfaces` (R530's X3), `acmp-expiry-to-interface-0`, `acmp-gptp-of-interface-0`, `acmp-admit-on-interface-0` |
| R530-1-F2 BINDING record | (code unchanged) | A24TheRecordIsTheProcessorsPayloadOneFlagAtATime (`test_acmp.cpp:1385`: 0x03, 0x01, 0x05 byte for byte from `KL_acmp_nvm_shadow.sv:484`, each restored to its one flag); A24UnboundRecordsRefusalsAndRollback (0, 21, 276, `UINT_MAX` bytes refused) | `acmp-record-flag-defines-swapped` (S3), `acmp-record-valid-bit-moved`, `acmp-longer-record-applied` (S8) |
| R530-1-F3 D3 roll-back | (code unchanged) | N7 (`test_acmp_nvm.cpp:250`): at the port, and at a boot whose D3 walk faults at settle and is rolled back (terminal DEFAULTS, binding kept) | `acmp-nvm-d3-rollback-drops-bindings` (S4) |
| R530-1-F4 32-bit wrap | (code unchanged) | A28 (two tests, `test_acmp.cpp:1630`, `:1694`): TMR_NO_RESP, TMR_RETRY, TMR_NO_TK, TMR_DELAY and TMR_NO_ADP armed across the wrap, none at the last millisecond before it or 1 ms early, each at its deadline; the earliest-deadline choice across the wrap | `acmp-due-unsigned` (W1), `acmp-earliest-unsigned` (W2), `acmp-no-adp-due-unsigned`, one saturating deadline per timer (5) |
| R530-1-F5 TD1 | `MAILBOX_SPLIT.md` "Differences from the processor"; `sw/firmware/ctrl/README.md`; `acmp.h:60`; `acmp_walk.cpp:42` | (the record) | (none: text) |
| R530-1-R1 | every "open decision" phrase replaced by the decided term (`MAILBOX_SPLIT.md`, `sw/firmware/ctrl/README.md`, `acmp_mbx.h`, `test_acmp_mbx.cpp` header) | | |
| Harness: `run-cosim` relink | `tb/verilator/mbx/Makefile:48` (the library depends on every firmware header too), `:74` (the binary goes when the library is newer) | shown by hand: a firmware-only planted defect (`ctrl_app.c`, `return true ||`) in a built tree rebuilt the library, relinked `Vmbx_cosim` and failed `the firmware answered ACMP on the model`; restored (sha256 checked), 32 of 32 | |

Expectations that moved, each because the rule it encoded changed: A23's outer bind with no
transmit room now has its TMR_NO_RESP held for the owed probe, not running (R531-1-F2); B5's
first check now requires the bound talker's AVAILABLE to pass the filter (the term); the
co-simulation's ACMP list is now `7, 0, 0, 5, 1, 0, 0, 11, 9` (the bound talker's AVAILABLE
passes both filters at 2000 ms, so TMR_RETRY delays and probes again at 5565 ms with
sequence_id 1). Repaired defect fixtures (each keeps its check): FC's
`model-mismatch-counts-identity-refusals` (the model's `rule_passes` takes the interface) and
`rx-own-mac-of-interface-0` (its line now also opens the bound-table block); six of F3's
round-1 defects whose lines changed; the needles of B3, B5, B6, C10 and C11 defects whose
words changed.

## Reviewers' probes replayed at the head

- R530-1's six escaped probes (its `r530_probes.py`, unmodified but for the selection, the
  `acmpif2` arm added to X3's arms, and N7 added to S4's expected tests; the diff is in the
  receipt): `[CAUGHT]` X3 (`acmp=0 acmpif2=1`: only two interfaces show it, which is R530-1-F1's
  point), S3, S4, S8, W1, W2: 6 of 6.
- R531-1's `independent_probes.cpp` with its `run_probes.py`, unmodified: 9 of 9 pass at one
  and at two interfaces (rc 0 both; at `351ae81f` both were rc 1 with six failing).

## Measured figures (round 2)

- Per path (bound / measured, mailbox accesses, the model): BIND_RX 76/76, UNBIND_RX 49/49,
  GET_RX_STATE 47/47, PROBE_TX_RESPONSE 28/28, talker commands 47/47, TMR_DELAY or the first
  TMR_NO_RESP 34/34, the second TMR_NO_RESP, TMR_RETRY, TMR_NO_TK 13/12 to 13, ENTITY_AVAILABLE
  from its RX_HEAD 35/35, ENTITY_DEPARTING from its RX_HEAD 30/29, TMR_NO_ADP 12/12; the same at
  each interface of the two-interface build.
- Backlogs: pass bound 996 (worst measured 193); an event by pass 2 (2,988); an ACMP command
  behind a full acmp ring by pass 10 (10,956); H-DISC, an ENTITY_AVAILABLE behind a full adp ring
  filled through the filter, from its RX_HEAD commit: pass 13 of 26 records, 333 accesses
  (bound 21,912); an owed response in pass k + 1 (8,964; measured 25, 100, 200 for k = 0, 3, 7).
  At two interfaces the pass bound is 1,027 and the same paths measure the same.
- RV32I (`riscv32-linux-gcc -march=rv32i -mabi=ilp32`, dev's freestanding headers): text 25,888
  bytes (24,848 at round 1), data 0, bss 170; undefined `__lshrdi3, __mulsi3, __udivsi3,
  __umodsi3, memcpy, memset, vsnprintf` (no heap); largest static frame 256 bytes.
- Co-simulation: 14 frames (5 ADP, 9 ACMP), identical bytes and NOW_MS on the RTL and the model,
  32 checks.
- Out-of-context area (`docs/design/MAILBOX_SPLIT.md` "Measured area": `KL_mbx` behind
  `KL_mbx_wb`, `xc7a100tfgg484-2`, 10 ns, Vivado 2026.1 defaults, placed and routed, under the
  shared lock, nothing else of this lane running): FC round 2 `db9aa8c9` 2,745 LUT, 2,860 FF,
  1 RAMB36, 10 RAMB18, WNS +0.186 ns, 5,630 nets (FC's recorded figures, repeated exactly); this
  head 4,025 LUT, 3,907 FF, the same block RAM, no DSP, WNS +0.283 ns, all 7,907 nets routed.
  The term costs 1,280 LUT and 1,047 FF (`KL_mbx_rx` 1,151 to 1,951 LUT; `KL_mbx` 295 to 752 LUT
  and 532 to 1,572 FF, the table's 1,040). A first version measured 4,887 LUT (comparators for
  every term position, the term being read by the frame's channel); `b6877341` builds them only
  for the `eq_bound` term and saved 862 LUT. The measured RTL equals the head's, by sha256.

## Coverage table

`python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4`, rc 0; the ratchet re-recorded by
`--write` (never a drop):

| File | Lines | Branches | After exclusions |
|---|---:|---:|---|
| sw/firmware/ctrl/acmp/acmp.c | 729/729 | 342/342 | 100 % / 100 % |
| sw/firmware/ctrl/acmp/acmp_mbx.c | 73/73 | 26/26 | 100 % / 100 % |
| sw/firmware/ctrl/acmp/acmp_nvm.c | 38/38 | 10/10 | 100 % / 100 % |
| sw/firmware/ctrl/app/ctrl_app.c | 22/23 | 19/22 | 100 % / 100 % |
| sw/firmware/ctrl/mbx/mbx.c | 185/185 | 68/68 | 100 % / 100 % |
| (the other 12 ratcheted files) | unchanged | unchanged | 100 % / 100 % |

No new exclusion: `ctrl_app.c`'s one line and three arcs are round 1's and F0's rows. The ACMP
files and `mbx.c` are 100 % raw.

## Tests and the planted defects each catches

Arms: `acmp` 78 tests, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 19, `model` 23, `unit` 24 + 2.
The campaign plants each defect in a copy and requires the named test to print `[FAIL]` with
the named words; `unnamed_tests` fails the campaign when a test of F3's sources is named by no
defect. Full campaign at `a45a9563` (sw/firmware unchanged since): 348 of 348 caught in 16
slices, 0 escapes, 0 unnamed tests. RTL campaign (`tb/verilator/mbx/mutants.py`) at the head:
105 of 105, with positive controls at one and two interfaces through both adapters. Generated
from the tables:

| Test | Source | Planted defects that must fail it (arm) |
|---|---|---|
| `AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold` | test_acmp.cpp | 5: `acmp-init-no-interface`, `acmp-init-sink-interface`, `acmp-init-source-interface`, `acmp-init-too-many-sinks`, `acmp-init-too-many-sources` |
| `AcmpCore.A0EverySinkStartsUnboundAndNothingIsCalled` | test_acmp.cpp | 1: `acmp-init-reads-the-seed` |
| `AcmpCore.A1BindFromUnboundRespondsThenProbes` | test_acmp.cpp | 11: `acmp-bind-change-before-response`, `acmp-bind-count-0`, `acmp-bind-starts-no-discovery`, `acmp-header-cdl-84`, `acmp-header-no-resp-2s`, `acmp-header-version-1`, `acmp-no-resp-2s`, `acmp-nothing-persisted`, `acmp-probe-before-response`, `acmp-probe-without-fast-connect`, `acmp-streaming-wait-ignored` |
| `AcmpCore.A1BindWithoutStreamingWaitBindsStarted` | test_acmp.cpp | 2: `acmp-bind-response-always-streaming-wait`, `acmp-new-bind-never-started` |
| `AcmpCore.A2GetRxStateInEveryState` | test_acmp.cpp | 2: `acmp-getrx-count-unbound`, `acmp-getrx-no-fast-connect` |
| `AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed` | test_acmp.cpp | 5: `acmp-getrx-no-registering-failed`, `acmp-header-registering-failed-bit`, `acmp-registered-kind-dropped`, `acmp-sw-read-from-fast-connect`, `acmp-view-without-registering-failed` |
| `AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId` | test_acmp.cpp | 2: `acmp-header-listener-unknown-is-2`, `acmp-unknown-sink-silent` |
| `AcmpCore.A3UnbindInEveryState` | test_acmp.cpp | 5: `acmp-unbind-change-before-response`, `acmp-unbind-echoes-the-talker`, `acmp-unbind-keeps-discovery`, `acmp-unbind-keeps-srp`, `acmp-unbind-srp-after-response` |
| `AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind` | test_acmp.cpp | 2: `acmp-lock-ignored`, `acmp-not-authorized-is-13` |
| `AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked` | test_acmp.cpp | 2: `acmp-get-rx-state-locked`, `acmp-lock-refuses-the-holder` |
| `AcmpCore.A5RebindTheSameSourceUpdatesAndExits` | test_acmp.cpp | 2: `acmp-rebind-same-keeps-the-controller`, `acmp-rebind-same-reprobes` |
| `AcmpCore.A6BindAnotherSourceRestartsTheSink` | test_acmp.cpp | 2: `acmp-bind-new-keeps-srp`, `acmp-rebind-not-persisted` |
| `AcmpCore.A6TheSameTalkerAnotherSourceIsANewBinding` | test_acmp.cpp | 1: `acmp-bind-same-talker-is-the-same-source` |
| `AcmpCore.A7ResponsesKeyOnTheListenerUniqueId` | test_acmp.cpp | 1: `acmp-response-keyed-on-the-source` |
| `AcmpCore.A7EachGuardTermIsChecked` | test_acmp.cpp | 4: `acmp-guard-controller-dropped`, `acmp-guard-sequence-id-dropped`, `acmp-guard-talker-dropped`, `acmp-guard-unique-id-dropped` |
| `AcmpCore.A7TheGuardReadsTheSentProbeNotTheBinding` | test_acmp.cpp | 1: `acmp-guard-reads-the-binding` |
| `AcmpCore.A7ResponsesOutsideProbingAreIgnored` | test_acmp.cpp | 1: `acmp-responses-taken-outside-probing` |
| `AcmpCore.A8SuccessSettles` | test_acmp.cpp | 5: `acmp-header-no-tk-5s`, `acmp-no-tk-1s`, `acmp-settle-starts-no-srp`, `acmp-settle-swaps-stream-fields`, `acmp-vlan-masked` |
| `AcmpCore.A9FailureWaitsForTheRetry` | test_acmp.cpp | 3: `acmp-failure-retries-at-200ms`, `acmp-failure-status-dropped`, `acmp-header-retry-2s` |
| `AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp` | test_acmp.cpp | 3: `acmp-duplicate-takes-a-new-sequence-id`, `acmp-no-duplicate`, `acmp-second-timeout-keeps-status-0` |
| `AcmpCore.A11RetryWaitsForTheTalkerOrDelays` | test_acmp.cpp | 2: `acmp-retry-ignores-discovery`, `acmp-retry-zeroes-the-status` |
| `AcmpCore.A12DelaySendsANewProbe` | test_acmp.cpp | 2: `acmp-delay-resends-the-old-probe`, `acmp-sequence-id-never-advances` |
| `AcmpCore.A13NoTalkerAttributeReprobes` | test_acmp.cpp | 2: `acmp-no-tk-keeps-srp`, `acmp-reprobe-ignores-discovery` |
| `AcmpCore.A14RegisteredSettlesTheReservation` | test_acmp.cpp | 2: `acmp-registered-anywhere`, `acmp-registered-keeps-no-tk` |
| `AcmpCore.A15UnregisteredReprobes` | test_acmp.cpp | 3: `acmp-reprobe-ignores-discovery`, `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp` |
| `AcmpCore.A16OneCounterForEveryNewProbe` | test_acmp.cpp | 2: `acmp-sequence-id-never-advances`, `acmp-sequence-id-per-sink` |
| `AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline` | test_acmp.cpp | 5: `acmp-expiry-not-consumed`, `acmp-expiry-takes-every-interface`, `acmp-timer-at-the-latest-deadline`, `acmp-timer-never-stopped`, `acmp-timer-port-called-every-time` |
| `AcmpCore.A18AZeroDelayProbesInTheSameExpiry` | test_acmp.cpp | 2: `acmp-delay-up-to-4s`, `acmp-zero-delay-waits` |
| `AcmpCore.A18TheSeedIsTakenAtTheFirstDraw` | test_acmp.cpp | 2: `acmp-rng-left-at-0`, `acmp-seed-at-every-draw` |
| `AcmpCore.A20ProbeTxIsAnsweredFromTheSource` | test_acmp.cpp | 4: `acmp-probe-tx-any-interface`, `acmp-probe-tx-no-destination-mac-check`, `acmp-probe-tx-reports-asking-failed`, `acmp-unknown-source-answered` |
| `AcmpCore.A20DisconnectGetTxStateAndGetTxConnection` | test_acmp.cpp | 5: `acmp-disconnect-always-succeeds`, `acmp-get-tx-connection-supported`, `acmp-get-tx-state-echoes-the-listener`, `acmp-get-tx-state-registering-failed-0`, `acmp-get-tx-state-unheld-mac` |
| `AcmpCore.A21MessagesNotForThisEntityAreIgnored` | test_acmp.cpp | 2: `acmp-every-listener-is-this-one`, `acmp-every-talker-is-this-one` |
| `AcmpCore.A21MalformedFramesAreCounted` | test_acmp.cpp | 2: `acmp-longer-pdu-refused`, `acmp-short-pdu-read` |
| `AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits` | test_acmp.cpp | 2: `acmp-change-not-held-for-its-response`, `acmp-poll-drains-everything` |
| `AcmpCore.A19NothingPassesAnOwedFrame` | test_acmp.cpp | 2: `acmp-poll-newest-first`, `acmp-response-passes-an-owed-frame` |
| `AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs` | test_acmp.cpp | 1: `acmp-full-queue-acts` |
| `AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered` | test_acmp.cpp | 2: `acmp-lost-probe-held`, `acmp-lost-probe-uncounted` |
| `AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether` | test_acmp.cpp | 1: `acmp-first-owed-releases-every-change` |
| `AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches` | test_acmp.cpp | 4: `acmp-discovery-reads-no-domain`, `acmp-discovery-reads-no-grandmaster`, `acmp-header-valid-time-in-seconds`, `acmp-valid-time-in-seconds` |
| `AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail` | test_acmp.cpp | 2: `acmp-discovered-probing-stays-passive`, `acmp-grandmaster-read-twice` |
| `AcmpCore.A22DiscoveredStateCells` | test_acmp.cpp | 6: `acmp-discovered-interface-unchecked`, `acmp-grandmaster-sampled-for-the-refresh`, `acmp-refresh-notes-no-index`, `acmp-restart-mismatch-keeps-aging`, `acmp-restart-on-a-smaller-index-only`, `acmp-restart-raises-no-discovered` |
| `AcmpCore.A22DepartingAndAging` | test_acmp.cpp | 4: `acmp-departing-interface-unchecked`, `acmp-departing-keeps-aging`, `acmp-departing-taken-undiscovered`, `acmp-no-aging` |
| `AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface` | test_acmp.cpp | 3: `acmp-discovery-on-every-interface`, `acmp-discovery-on-unbound-sinks`, `acmp-grandmaster-sampled-per-sink` |
| `AcmpCore.A22OtherAdpFramesAreIgnored` | test_acmp.cpp | 4: `acmp-adp-discover-taken`, `acmp-adp-ethertype-unchecked`, `acmp-adp-short-frame-taken`, `acmp-adp-subtype-unchecked` |
| `AcmpCore.A23EveryEntryRefusesACallFromInsideAPort` | test_acmp.cpp | 5: `acmp-open-unguarded`, `acmp-owed-probe-timer-runs`, `acmp-reentry-unguarded`, `acmp-reentry-untrapped`, `acmp-send-port-unflagged` |
| `AcmpCore.A23EveryPortIsGuarded` | test_acmp.cpp | 11: `acmp-admit-port-unflagged`, `acmp-changed-port-unflagged`, `acmp-clock-port-unflagged`, `acmp-gptp-port-unflagged`, `acmp-lock-port-unflagged`, `acmp-persist-port-unflagged`, `acmp-reentry-unguarded`, `acmp-seed-port-unflagged`, `acmp-source-port-unflagged`, `acmp-srp-port-unflagged`, `acmp-timer-port-unflagged` |
| `AcmpCore.A24ARestoredBindingFastConnects` | test_acmp.cpp | 4: `acmp-record-unique-id-little-endian`, `acmp-restore-lands-in-prb-w-resp`, `acmp-restore-starts-no-discovery`, `acmp-restore-unique-id-little-endian` |
| `AcmpCore.A24UnboundRecordsRefusalsAndRollback` | test_acmp.cpp | 3: `acmp-longer-record-applied`, `acmp-roll-back-keeps-the-bindings`, `acmp-unbound-record-not-zero` |
| `AcmpCore.A24StartedIsSavedAndReported` | test_acmp.cpp | 1: `acmp-started-not-saved` |
| `AcmpCore.A24TheRecordIsTheProcessorsPayloadOneFlagAtATime` | test_acmp.cpp | 2: `acmp-record-flag-defines-swapped`, `acmp-record-valid-bit-moved` |
| `AcmpCore.A25OnlyTable522ItemsAreReported` | test_acmp.cpp | 3: `acmp-discovery-notifies`, `acmp-second-timeout-keeps-status-0`, `acmp-status-not-notified` |
| `AcmpCore.A26AnotherAvtpVersionIsDiscardedBeforeItIsRead` | test_acmp.cpp | 3: `acmp-adp-version-unchecked`, `acmp-version-bits-misread`, `acmp-version-unchecked` |
| `AcmpCore.A27AnOwedProbeStartsItsTimerWhenItLeaves` | test_acmp.cpp | 7: `acmp-held-timer-armed`, `acmp-held-timer-expires`, `acmp-owed-probe-names-the-next-sink`, `acmp-owed-probe-never-starts`, `acmp-owed-probe-no-resp-2s`, `acmp-owed-probe-timer-runs`, `acmp-owed-probe-unnamed` |
| `AcmpCore.A27AStalledDuplicateGetsItsWholeInterval` | test_acmp.cpp | 2: `acmp-owed-probe-never-starts`, `acmp-owed-probe-timer-runs` |
| `AcmpCore.A27AProbeOwedPastAnUnbindARebindOrASuccessStartsNothing` | test_acmp.cpp | 2: `acmp-owed-probe-sequence-unchecked`, `acmp-stop-keeps-the-hold` |
| `AcmpCore.A28EveryTimerExpiresAtItsDeadlineAcrossTheWrap` | test_acmp.cpp | 7: `acmp-delay-deadline-saturates`, `acmp-due-unsigned`, `acmp-no-adp-deadline-saturates`, `acmp-no-adp-due-unsigned`, `acmp-no-resp-deadline-saturates`, `acmp-no-tk-deadline-saturates`, `acmp-retry-deadline-saturates` |
| `AcmpCore.A28TheEarliestDeadlineIsChosenAcrossTheWrap` | test_acmp.cpp | 2: `acmp-due-unsigned`, `acmp-earliest-unsigned` |
| `AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker` | test_acmp.cpp | 4: `acmp-admit-ignores-another-talker`, `acmp-admit-never-called`, `acmp-admit-on-every-entry`, `acmp-admit-on-interface-0` |
| `AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens` | test_acmp.cpp | 2: `acmp-open-does-nothing`, `acmp-reset-forgets-the-admitted` |
| `AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder` | test_acmp_mbx.cpp | 2: `acmp-frames-on-the-adp-channel`, `acmp-frames-to-the-own-mac` |
| `AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused` | test_acmp_mbx.cpp | 4: `acmp-frames-to-the-own-mac`, `app-own-mac-not-the-entity-mac`, `model-mismatch-never-counted`, `model-own-any-unicast` |
| `AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot` | test_acmp_mbx.cpp | 5: `acmp-expiry-to-interface-0` (acmpif2), `acmp-no-resp-2s` (acmp), `acmp-one-slot-for-all-interfaces` (acmpif2), `acmp-timer-deadline-taken-as-a-delay` (acmp), `acmp-timer-on-the-next-slot` (acmp) |
| `AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded` | test_acmp_mbx.cpp | 3: `acmp-stale-tag-taken`, `acmp-stop-keeps-the-arm`, `acmp-tag-reused` |
| `AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp` | test_acmp_mbx.cpp | 4: `acmp-no-tap`, `acmp-tap-drops-the-rest`, `acmp-tap-takes-discover`, `app-acmp-never-opened` |
| `AcmpMailbox.B6TheGrandmasterIsTheInterfaces` | test_acmp_mbx.cpp | 2: `acmp-domain-not-sampled` (acmp), `acmp-gptp-of-interface-0` (acmpif2) |
| `AcmpAdapterUnit.B7RefusalsOfTheAdapter` | test_acmp_mbx.cpp | 8: `acmp-attach-before-adp`, `acmp-attach-ignores-poll-room`, `acmp-attach-ignores-sink-room`, `acmp-interfaces-past-the-mailbox`, `acmp-slot-narrowed-first`, `acmp-slot-sum-wraps`, `acmp-slots-one-short`, `acmp-slots-past-the-bank` |
| `AcmpMailbox.B8TheBoundTalkerTableFollowsEachBinding` | test_acmp_mbx.cpp | 6: `acmp-admit-ignores-another-talker` (acmp), `acmp-admit-never-called` (acmp), `acmp-admit-on-interface-0` (acmpif2), `acmp-mbx-admit-always-bound` (acmp), `mbx-bound-halves-swapped` (acmp), `mbx-bound-withdraw-writes-nothing` (acmp) |
| `AcmpMailbox.B9AnotherAvtpVersionPassesTheFilterAndChangesNothing` | test_acmp_mbx.cpp | 2: `acmp-adp-version-unchecked`, `acmp-version-unchecked` |
| `AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem` | test_acmp_mbx.cpp | 8: `acmp-admit-never-called`, `acmp-admit-on-every-entry`, `acmp-bind-reads-the-clock-twice`, `acmp-get-rx-state-reads-the-clock`, `acmp-mbx-admit-always-bound`, `acmp-probe-response-reads-the-clock-twice`, `acmp-talker-reads-the-clock`, `acmp-unbind-reads-the-clock` |
| `AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry` | test_acmp_mbx.cpp | 5: `acmp-delay-reads-the-clock-again`, `acmp-expiry-reads-the-clock-twice`, `acmp-no-tk-samples-the-grandmaster`, `acmp-retry-samples-the-grandmaster`, `acmp-second-no-resp-samples-the-grandmaster` |
| `AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord` | test_acmp_mbx.cpp | 4: `acmp-available-reads-the-clock-twice`, `acmp-departing-samples-the-grandmaster`, `acmp-grandmaster-read-twice`, `acmp-timer-never-stopped` |
| `AcmpMailbox.C12AgingIsServedInThePassThatTakesTheExpiry` | test_acmp_mbx.cpp | 1: `acmp-aging-samples-the-grandmaster` |
| `AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt` | test_acmp_mbx.cpp | 2: `acmp-change-not-held-for-its-response`, `acmp-poll-owes-nothing` |
| `AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1` | test_acmp_mbx.cpp | 2: `acmp-poll-drains-everything`, `acmp-poll-newest-first` |
| `AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound` | test_acmp_mbx.cpp | 5: `acmp-backlog-understated`, `acmp-pass-bound-understated`, `events-halved`, `model-event-ring-a-record-short`, `rx-one-record-per-pass` |
| `AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing` | test_acmp_mbx.cpp | 2: `acmp-backlog-understated`, `acmp-smallest-record-overstated` |
| `AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound` | test_acmp_mbx.cpp | 3: `acmp-adp-ring-bound-understated`, `acmp-discovery-takes-the-first-sink`, `rx-one-record-per-pass` |
| `AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract` | test_acmp_mbx.cpp | 8: `acmp-init-reads-the-seed`, `acmp-mbx-admit-on-entry-0`, `acmp-no-tap`, `acmp-open-does-nothing`, `app-acmp-before-adp`, `app-acmp-never-composed`, `app-acmp-never-opened`, `mbx-bound-entry-stride-ignored` |
| `ListenerWalk.Graded` | acmp_walk.cpp | 35: `acmp-bind-count-0`, `acmp-bind-new-keeps-srp`, `acmp-bind-starts-no-discovery`, `acmp-delay-resends-the-old-probe`, `acmp-discovery-notifies`, `acmp-duplicate-takes-a-new-sequence-id`, `acmp-failure-retries-at-200ms`, `acmp-failure-status-dropped`, `acmp-getrx-count-unbound`, `acmp-getrx-no-fast-connect`, `acmp-header-no-resp-2s`, `acmp-header-retry-2s`, `acmp-no-duplicate`, `acmp-no-tk-1s`, `acmp-no-tk-keeps-srp`, `acmp-probe-without-fast-connect`, `acmp-probing-status-not-notified`, `acmp-rebind-same-reprobes`, `acmp-registered-anywhere`, `acmp-registered-keeps-no-tk`, `acmp-registered-kind-dropped`, `acmp-reprobe-ignores-discovery`, `acmp-responses-taken-outside-probing`, `acmp-retry-ignores-discovery`, `acmp-retry-zeroes-the-status`, `acmp-second-timeout-keeps-status-0`, `acmp-sequence-id-per-sink`, `acmp-settle-starts-no-srp`, `acmp-settle-swaps-stream-fields`, `acmp-unbind-echoes-the-talker`, `acmp-unbind-keeps-discovery`, `acmp-unbind-keeps-srp`, `acmp-unbind-not-persisted`, `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp` |
| `ListenerScenario.LD3TheLockRefusalStatus` | acmp_walk.cpp | 1: `acmp-not-authorized-is-13` |
| `ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages` | acmp_walk.cpp | 4: `acmp-guard-controller-dropped`, `acmp-guard-sequence-id-dropped`, `acmp-guard-talker-dropped`, `acmp-guard-unique-id-dropped` |
| `DiscoveryWalk.Graded` | acmp_walk.cpp | 10: `acmp-departing-interface-unchecked`, `acmp-departing-keeps-aging`, `acmp-discovered-interface-unchecked`, `acmp-discovery-reads-no-domain`, `acmp-discovery-reads-no-grandmaster`, `acmp-no-aging`, `acmp-refresh-notes-no-index`, `acmp-restart-mismatch-keeps-aging`, `acmp-restart-raises-no-discovered`, `acmp-valid-time-in-seconds` |
| `TalkerWalk.TW1ProbeTheFlagLawAndTheSource` | acmp_walk.cpp | 2: `acmp-probe-tx-echoes-every-flag`, `acmp-probe-tx-no-destination-mac-check` |
| `TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive` | acmp_walk.cpp | 3: `acmp-get-tx-state-echoes-the-listener`, `acmp-get-tx-state-registering-failed-0`, `acmp-unknown-source-answered` |
| `TalkerWalk.TW3DisconnectAndGetTxConnection` | acmp_walk.cpp | 2: `acmp-disconnect-always-succeeds`, `acmp-get-tx-connection-supported` |
| `TalkerWalk.TW4TheInterfaceAndTheStatelessProperty` | acmp_walk.cpp | 1: `acmp-probe-tx-any-interface` |
| `AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects` | test_acmp_nvm.cpp | 6: `acmp-nothing-persisted`, `acmp-nvm-bindings-latched-by-the-others`, `acmp-nvm-bindings-to-the-others`, `acmp-restore-announced`, `acmp-restore-lands-in-prb-w-resp`, `acmp-restore-starts-no-discovery` |
| `AcmpStore.N2AnUnbindIsSavedAsAnUnboundRecord` | test_acmp_nvm.cpp | 1: `acmp-unbind-not-persisted` |
| `AcmpStore.N3EachSinksStartedStateIsSaved` | test_acmp_nvm.cpp | 2: `acmp-record-flags-swapped`, `acmp-started-not-saved` |
| `AcmpStore.N4AnUnreadSlotRefusesPersistence` | test_acmp_nvm.cpp | 1: `acmp-rebind-not-persisted` |
| `AcmpStore.N5ARecordTheCoreRefusesKeepsItsDefault` | test_acmp_nvm.cpp | 1: `acmp-nvm-refusal-applied` |
| `AcmpStore.N6TheRollBackAndEveryOtherGroup` | test_acmp_nvm.cpp | 7: `acmp-nvm-d3-roll-back-kept`, `acmp-nvm-latch-length-unchecked`, `acmp-nvm-model-always-ready`, `acmp-nvm-refusal-applied`, `acmp-nvm-release-dropped`, `acmp-nvm-settle-dropped`, `acmp-roll-back-keeps-the-bindings` |
| `AcmpStore.N7AD3RollBackKeepsTheBindings` | test_acmp_nvm.cpp | 1: `acmp-nvm-d3-rollback-drops-bindings` |
| `DriverUnit.D13BoundTalkerEntries` | test_unit_driver.cpp | 6: `mbx-bound-enabled-before-the-identity`, `mbx-bound-entry-stride-ignored`, `mbx-bound-entry-unguarded`, `mbx-bound-halves-swapped`, `mbx-bound-unguarded`, `mbx-bound-withdraw-writes-nothing` |
| `Suite/MbxModelGroup.PassesOnTheModel/AdpBoundTalkers` (round-2 defects only) | model_suite.cpp | 5: `model-bound-enable-ignored`, `model-bound-low-word-only`, `model-bound-table-of-interface-0`, `model-bound-term-any-type`, `model-bound-term-misses` |
| `Suite/MbxModelGroup.PassesOnTheModel/ResetIdentityAndRegisterMasks` (round-2 defects only) | model_suite.cpp | 2: `model-bound-en-reads-the-eid`, `model-bound-entry-decoded-as-0` |

## Gate table (round 2)

Each command run on its own, at the head unless stated, rc recorded, output never piped.
Verilator is the pinned 5.050 for every build and lint.

| Gate | Command | rc | Result |
|---|---|---:|---|
| firmware-unit: tally | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | 18 of 18 planted cases |
| firmware-unit: ctrl suites | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32` | 0 | every arm PASS (`acmp` 78, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 19, `model` 23); rv32 text 25,888 |
| ctrl campaign | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice K/16`, K = 1 to 16, four at a time | 0 (x16) | 348 of 348, at `a45a9563` (`sw/firmware` unchanged since: `git diff --stat a45a9563 HEAD -- sw/firmware` is empty); peak unit memory 4.7 GiB |
| firmware-unit: coverage | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 28 of 28 |
| firmware-unit: coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | 17 files at the ratchet |
| firmware-unit: store | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 5 shapes, 434 tests (at `1bde5d96`; `sw/firmware` unchanged since) |
| saved-state writer | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 5 shapes, every planted defect reddened (at `1bde5d96`) |
| mbx suite | `make -C tb/verilator/mbx clean`, then `make -C tb/verilator/mbx run-wb run-axil run-cosim run-if2` | 0 | 348 (Wishbone), 393 (AXI4-Lite), co-simulation 32, two interfaces 348/393/348 (at `b6877341`; the RTL and the suite unchanged since) |
| mbx suite | `python3 -B tb/verilator/mbx/mutants.py --quick --jobs 2` (the default `make`'s arm, at two jobs) | 0 | 5 of 5 |
| mbx suite | `python3 -B tb/verilator/mbx/mutants.py --jobs 2` (`make mutants`, at two jobs) | 0 | 105 of 105, four positive controls (at `b6877341`) |
| reviewers' probes | R530-1's `r530_probes.py` (six escaped probes; selection, X3's `acmpif2` arm and S4's N7 added) and R531-1's `run_probes.py` with `independent_probes.cpp` (unmodified) | 0 | 6 of 6 caught; 9 of 9 pass at one and two interfaces (at `1bde5d96`; firmware unchanged since) |
| contract | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | 0 findings |
| contract | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | 0 arms failed (44 arms, incl. 10 new) |
| builder bank | `python3 sw/builder/test_builder.py --require-rv32` | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a placed utilization report from a Vivado build tree this host does not hold, as in round 1 (1,222 s, at the head; also 1,247 s at `1bde5d96`) |
| idiom | `python3 scripts/check_py_idiom.py`, `check_cpp_idiom.py`, `check_sv_idiom.py` | 0 | at their ratchets |
| docs workflow | `python3 scripts/docs_check.py` | 0 | |
| docs workflow | `python3 scripts/check_em_dash.py --base 910f338dbd050f4efd2d96991ddcf928a583d55f` | 0 | |
| docs workflow | `python3 scripts/check_em_dash.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_doc_style.py` | 0 | |
| docs workflow | `python3 scripts/check_doc_style.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py --selftest` | 0 | |
| docs workflow | `python3 docs/DOC_MAP.gen.py --check` | 0 | |
| docs workflow | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | |
| docs workflow | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | |
| docs workflow | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_solution_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_solution_docs.py --selftest` | 0 | |
| docs workflow | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | |
| docs workflow | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_submodule_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_submodule_docs.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_diagram_pngs.py` | 0 | |
| docs workflow | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_feature_status.py --self-test` | 0 | |
| docs workflow | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | |
| docs workflow | `python3 scripts/measure_control_flow.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_cohesion.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_baremetal_only.py --check` | 0 | |
| docs workflow | `python3 scripts/check_baremetal_only.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_nvm_record_space.py` | 0 | |
| docs workflow | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_nvm_capture.py` | 0 | |
| docs workflow | `python3 scripts/check_soc_sources.py` | 0 | |
| docs workflow | `python3 scripts/check_soc_sources.py --selftest` | 0 | |
| docs workflow | `python3 sw/litex/iob_pack_selftest.py` | 0 | |
| docs workflow | `python3 scripts/check_rtl_source_lists.py` | 0 | |
| docs workflow | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_naming.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_naming.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_port_contracts.py` | 0 | |
| docs workflow | `python3 scripts/check_port_contracts.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_fail_fast.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_fail_fast.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_todo_ownership.py` | 0 | |
| docs workflow | `python3 scripts/check_todo_ownership.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_test_evidence.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_test_evidence.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_hygiene.py --check` | 0 | |
| docs workflow | `python3 scripts/check_hygiene.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sv_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_sv_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_cpp_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_py_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_py_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sh_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_sh_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/ci_events.py --check` | 0 | |
| docs workflow | `python3 scripts/ci_events.py --selftest` | 0 | |
| docs workflow | `python3 scripts/act_ci.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_doc_paths.py` | 0 | |
| docs workflow | `python3 scripts/check_archive.py` | 0 | |
| docs workflow | `python3 scripts/check_archive.py --selftest` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --selftest` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --verify-anchors` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --check` | 0 | |
| docs workflow | `python3 avdecc/gen_aem_store.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_sweep_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_deploy_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_entity_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_wire_accountability.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_feature_status.py` | 0 | |
| docs workflow | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | |
| docs workflow | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | |

The docs-workflow commands are `docs.yml`'s steps that need no hosted install, run with the
pinned Markdown renderer from a scratch environment; not run here: the HDL reference build (its
pinned pip set), the wavedrom checks (`wavedrom` not installed) and the `--absent` compiler
audit, none of which reads a file this lane changed. The em-dash base is `git merge-base
origin/dev HEAD` (`910f338d`).

## Open questions and risks

1. **T_svc at full backlog (A4).** The full-ring bounds fit T_svc = 10 ms only at 0.91 us per
   access or less (acmp ring) and 0.46 us or less (H-DISC behind a full adp ring; 0.91 us for
   the 20 ms ceiling). The access time is an acceptance item of the F2 to F5 bench pass
   (decision 6029368753).
2. **The bound-talker table's area.** 16 entries of 65 bits per interface in flip-flops (see the
   area figures). A distributed-RAM table scanned after entity_id arrives would save most of
   them; not done here.
3. The processor's four differences are processor issue #168; the submodule is unchanged.
4. Hosted CI and `act` acceptance are the manager's; nothing pushed.

# Round 1

Round 1's handoff, as it was at its REVIEW READY head `351ae81f` (issue #665 comment
6029338230); its figures are that head's.

Status: REVIEW READY at `351ae81f` (every gate below rc 0), with the open decision on the
adp filter term ("Open questions and risks" 1).

- Branch `665-f3-acmp`, head `351ae81f33efc1ca818c1fea21d360260ecc2587`, not pushed.
- Base: the FC head `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` (PR #685). FC is not in
  `dev` yet (checked 2026-10-07: `git merge-base --is-ancestor 021b9c1f origin/dev` exits 1,
  `origin/dev` at `79b086d44`), so `dev` is not merged here; the `--no-ff` merge of `dev`
  is owed once FC lands.
- Assignment: issue #665 comment 6026721148. TAKEN: comment 6026823815.
  REVIEW READY: comment 6029338230 (head `351ae81f`).
- Scope held: no file under `hdl/`, `sw/litex/`, `configs/` or `sw/mailbox/` changes
  (`git diff --stat 021b9c1f HEAD -- hdl sw/litex configs sw/mailbox` is empty), so the
  default all-fabric build, the shipping image and the register map are unchanged.

### Summary

| Item of the assignment | Where | State |
|---|---|---|
| 1. Talker and listener, Milan v1.2 5.5 bind model, 200 ms TMR_NO_RESP, retry, sequence IDs, responses keyed on the consumer's unique ID | `sw/firmware/ctrl/acmp/acmp.c` | done; every Table 5.30 transition, talker 5.5.4.1 to .4 |
| 2. Listener discovery (5.6.4, Table 5.54) through F0's ADP public API | `acmp.c:547-600`, `acmp_mbx.c:109` (the tap) | done in firmware; the tree's adp filter passes no ENTITY_AVAILABLE/DEPARTING (decision open, see "Open questions") |
| 3. Fast connect from the F1 store; no persistence on a read fault | `sw/firmware/ctrl/acmp/acmp_nvm.c`, `acmp.c:1096` | done; N1 to N6 on the real store |
| 4. Response before notification (#653) | `acmp.c:240` (owed FIFO, release mask), `acmp.c:415` (`finish`) | done; A19, E1 |
| 5. Differential against the processor's ACMP suites | `sw/firmware/ctrl/test/acmp_walk.cpp`, `ctrl_reuse.py` | done; 88 + 33 cells, talker F05.11; 4 differences asserted |
| 6. H-ACMP and H-DISC (#664 3.4.2) on the host model | `test_acmp_mbx.cpp` C0 to C12, E1, E2, F0 to F5 | done in mailbox accesses; time not measured (A4) |
| GoogleTest at the ratchet, 100 % branches, no unjustified exclusion | `sw/firmware/gtest/coverage.ratchet`, `README.md:319` | done; one new exclusion row, same form as F0's |
| A planted defect per check | `sw/firmware/ctrl/test/acmp_mutants.py` | 195 defects; every test of the three arms named, proven by `unnamed_tests` |
| Co-simulate with the host mailbox model | `test_acmp_mbx.cpp` (model), `tb/verilator/mbx/cosim_main.cpp` (RTL vs model) | done; 12 frames identical |
| No RTL change; default build unchanged | see above | held |

### Progress log

- Confirmed origin and base head.
- Posted TAKEN: issue #665 comment 6026823815. Blocker published there: the
  tree's `adp` channel filter passes only ENTITY_DISCOVER and both of its
  accept terms are used, so a bound talker's ENTITY_AVAILABLE/DEPARTING
  cannot reach the core without an RTL change (forbidden here). Decision
  requested; the rest of the lane proceeds.
- Differential finding (processor, not fixed here): `pp_acmp_pkg.sv:123`
  answers CONTROLLER_NOT_AUTHORIZED with 13; IEEE 1722.1-2021 Table 8-3 says
  16 (13 is TALKER_MISBEHAVING).
- Core `sw/firmware/ctrl/acmp/acmp.[ch]`, adapter `acmp_mbx.[ch]`, store
  glue `acmp_nvm.[ch]`, app compose/open split written; the existing arms all
  pass with them compiled in (rv32 text 11,756 -> 24,800 bytes).
- Commits 574911a2 (firmware) and 4a9fa9db (tests): arms acmp (66 tests),
  acmpwalk (127), acmpnvm (6) green; coverage ratchet written, every ctrl
  file 100 % lines and branches after exclusions; one new exclusion row
  (ctrl_app.c ACMP attach refusal, unreachable in the app, same form as F0's
  ADP row, whose function name moved to ctrl_app_compose).
- Commit 331455c9: 175 ACMP planted defects (ctrl_mutants.py, after F0/FC's
  93; table now 268), each caught by the check it names in a scratch run with
  4 workers; tests now spell the standards' numbers in `spec` (acmp_fake.hpp)
  so a wrong constant in acmp.h fails them; `--slice K/N` added to the gate.
- Added the H-DISC bound behind a full adp ring in the ADP+ACMP composition
  (`ACMP_MBX_ADP_RX_ACCESSES`, test F5; measured 333 accesses in pass 13
  against 21,670) with three planted defects.
- Added ACMP to the RTL co-simulation (`tb/verilator/mbx/cosim_main.cpp`):
  twelve frames identical on the RTL and the model. The first run exposed a
  harness limit (a second frame committed in the same pass was collected one
  millisecond late); the collector now waits while frames finish
  (`bench.hpp` `tx_open()`). A planted firmware defect (ACMP never composed)
  fails the new check; recorded below.
- Audit of the planted defects against the tests: five tests of the ACMP
  arms and several labelled checks (C6 to C9, F0 to F2, A2's view, B2) had
  no defect naming them, contrary to the earlier progress entry. Added 17
  defects and extra kills on six existing ones; every test of the ACMP
  arms is now named, and `unnamed_tests` proves it in the campaign before
  planting. B2's "to the multicast address" check now reads the address.
- Docs: ctrl README, gtest README, ctrl_nvm README, mbx README,
  MAILBOX_SPLIT.md (the ACMP module section, latency tables, differences,
  open items).
- Commits 048cd2b3 (H-DISC full-ring bound, co-simulation, defect audit), 6afca717 (docs),
  351ae81f (lane F3's defects in `acmp_mutants.py`, lines within 120 columns, the discovery
  walk's rig out of its test body, for the Python and C++ idiom gates).
- Gates run at 351ae81f (table below). The first builder run used the host's Verilator by
  mistake and was stopped; it was rerun with the pinned 5.050.
- Posted REVIEW READY on #665 (comment 6029338230). FC still open (#685) at posting; `dev` unmerged.

### Changes (file:line)

Firmware (all new unless noted):

- `sw/firmware/ctrl/acmp/acmp.h:1-108`: the module's contract and every clause it implements;
  `acmp.h:120-136` static sizes and wire constants; `acmp.h:286-301` `struct acmp_env`;
  `acmp.h:378-406` the entries.
- `sw/firmware/ctrl/acmp/acmp.c`:
  - `:83` `enter()`, the #678 guard; `:94-165` every port wrapped with the in-port flag.
  - `:174-220` decode, build (to the ACMP multicast address, `:197`), echo.
  - `:240-279` `transmit`/`respond`/`room`: owed FIFO of 8, release mask per frame (#653), busy drops.
  - `:286-353` the sink timers, the lazy seed and draw (`:299`), one timer per interface at its earliest deadline (`:330`).
  - `:355-435` the Table 5.22 view, the 20-byte saved record, `finish()` (persist on a record change, notify after the response).
  - `:456-600` discovery (5.6.4): start/stop, EVT_TK_DISCOVERED (`:501`), EVT_TK_DEPARTED (`:515`), TMR_NO_ADP from valid_time (`:525`), the one gPTP sample per frame (`:547`), AVAILABLE (`:557`), DEPARTING (`:589`).
  - `:602-672` SRP stop, probe with a fresh sequence_id (`:612`, `:635`), every timer expiry (`:648`).
  - `:676-833` the listener: lock (`:676`), BIND_RX (`:695`), UNBIND_RX (`:730`), GET_RX_STATE (`:751`), dispatch (`:772`), PROBE_TX_RESPONSE keyed on listener_unique_id and the sent probe (`:798`).
  - `:834-884` the talker: PROBE_TX, GET_TX_STATE, DISCONNECT_TX, GET_TX_CONNECTION.
  - `:886-1155` the public entries.
- `sw/firmware/ctrl/acmp/acmp_mbx.h:1-90` the adapter's contract, the tap and the latency
  derivation; `:110-143` the per-path and backlog bounds, incl. `ACMP_MBX_ADP_RX_ACCESSES` (`:142`).
- `sw/firmware/ctrl/acmp/acmp_mbx.c:10-48` ports on the mailbox; `:50` init; `:69-107` frame, event (tag rule), poll; `:109` the ADP tap; `:119` attach.
- `sw/firmware/ctrl/acmp/acmp_nvm.h:43-50`, `acmp_nvm.c:9-68`: the binding owner on F1's `nvm_state` port.
- `sw/firmware/ctrl/app/ctrl_app.h:18-23, 44, 50, 65-79` (changed): compose/open split, `CTRL_APP_ACMP_FIRST_SLOT`, the ACMP config; `ctrl_app.c:10, 29, 44` (changed).

Tests and harness:

- `sw/firmware/ctrl/test/acmp_fake.hpp`: the standards' numbers (`spec`), fakes, frame builders.
- `test_acmp.cpp` (A0 to A25, core), `test_acmp_mbx.cpp` (B1 to B7, C0 to C12, E1, E2, F0 to F5, U5, model), `acmp_walk.cpp` (Table 5.30, Table 5.54, LD3, LW2, TW1 to TW4), `test_acmp_nvm.cpp` (N1 to N6).
- `ctrl_arms.py:43, 51, 69` the arms `acmp`, `acmpwalk`, `acmpnvm`; `ctrl_build.py:36-41` sources and includes; `ctrl_reuse.py:37-43` the three processor slices; `test_ctrl_firmware.py:131` `--slice K/N`.
- `acmp_mutants.py` (lane F3's 195 defects), `ctrl_mutant.py` (the `Mutant` type), `ctrl_mutants.py:419-430` `NAMED_SOURCES` and `unnamed_tests`, `:491` `sliced`.
- `tb/verilator/mbx/cosim_main.cpp:88-95` the frame collector waits while frames finish; `:197-245` the ACMP stimulus and config; `tb/verilator/mbx/bench.hpp:149` `tx_open()`; `Makefile:39-47` firmware sources.
- Existing tests given the two new config fields: `adp_walk.cpp`, `test_adp.cpp`, `test_unit_seams.cpp`.

Docs: `docs/design/MAILBOX_SPLIT.md:484-620` (The ACMP module, discovery and the adp filter,
ACMP service latency, differences from the processor), open items and verification rows;
`sw/firmware/ctrl/README.md:44` (The ACMP module), arms, reuse, planted defects;
`sw/firmware/gtest/README.md` (F3 arms, exclusion row `:319`); `sw/firmware/ctrl_nvm/README.md`
(the binding owner); `tb/verilator/mbx/README.md` (the co-simulation).

### Tests and the planted defect each catches

Arms: `acmp` 67 tests, `acmpwalk` 127 (88 Table 5.30 cells, 33 Table 5.54 cells, 6
scenarios), `acmpnvm` 6. The campaign plants each defect in a copy and requires the named
test to print `[FAIL]` with the named words; `unnamed_tests` fails the campaign when any
test of the three sources is named by no defect. Full campaign at the head: 288 of 288
caught (12 slices of 24), 0 escapes, 0 unnamed tests. Generated from the table:

| Test | Arm | Planted defects that must fail it |
|---|---|---|
| `AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold` (test_acmp.cpp) | `acmp` | 5: `acmp-init-no-interface`, `acmp-init-sink-interface`, `acmp-init-source-interface`, `acmp-init-too-many-sinks`, `acmp-init-too-many-sources` |
| `AcmpCore.A0EverySinkStartsUnboundAndNothingIsCalled` (test_acmp.cpp) | `acmp` | 1: `acmp-init-reads-the-seed` |
| `AcmpCore.A1BindFromUnboundRespondsThenProbes` (test_acmp.cpp) | `acmp` | 10: `acmp-bind-change-before-response`, `acmp-bind-count-0`, `acmp-bind-starts-no-discovery`, `acmp-header-cdl-84`, `acmp-header-no-resp-2s`, `acmp-no-resp-2s`, `acmp-nothing-persisted`, `acmp-probe-before-response`, `acmp-probe-without-fast-connect`, `acmp-streaming-wait-ignored` |
| `AcmpCore.A1BindWithoutStreamingWaitBindsStarted` (test_acmp.cpp) | `acmp` | 2: `acmp-bind-response-always-streaming-wait`, `acmp-new-bind-never-started` |
| `AcmpCore.A2GetRxStateInEveryState` (test_acmp.cpp) | `acmp` | 2: `acmp-getrx-count-unbound`, `acmp-getrx-no-fast-connect` |
| `AcmpCore.A2GetRxStateReportsStreamingWaitAndRegisteringFailed` (test_acmp.cpp) | `acmp` | 5: `acmp-getrx-no-registering-failed`, `acmp-header-registering-failed-bit`, `acmp-registered-kind-dropped`, `acmp-sw-read-from-fast-connect`, `acmp-view-without-registering-failed` |
| `AcmpCore.A2UnknownSinkIsAnsweredListenerUnknownId` (test_acmp.cpp) | `acmp` | 2: `acmp-header-listener-unknown-is-2`, `acmp-unknown-sink-silent` |
| `AcmpCore.A3UnbindInEveryState` (test_acmp.cpp) | `acmp` | 5: `acmp-unbind-change-before-response`, `acmp-unbind-echoes-the-talker`, `acmp-unbind-keeps-discovery`, `acmp-unbind-keeps-srp`, `acmp-unbind-srp-after-response` |
| `AcmpCore.A4LockedByAnotherControllerRefusesBindAndUnbind` (test_acmp.cpp) | `acmp` | 2: `acmp-lock-ignored`, `acmp-not-authorized-is-13` |
| `AcmpCore.A4TheLockingControllerPassesAndGetRxStateIsNotLocked` (test_acmp.cpp) | `acmp` | 2: `acmp-get-rx-state-locked`, `acmp-lock-refuses-the-holder` |
| `AcmpCore.A5RebindTheSameSourceUpdatesAndExits` (test_acmp.cpp) | `acmp` | 2: `acmp-rebind-same-keeps-the-controller`, `acmp-rebind-same-reprobes` |
| `AcmpCore.A6BindAnotherSourceRestartsTheSink` (test_acmp.cpp) | `acmp` | 2: `acmp-bind-new-keeps-srp`, `acmp-rebind-not-persisted` |
| `AcmpCore.A6TheSameTalkerAnotherSourceIsANewBinding` (test_acmp.cpp) | `acmp` | 1: `acmp-bind-same-talker-is-the-same-source` |
| `AcmpCore.A7ResponsesKeyOnTheListenerUniqueId` (test_acmp.cpp) | `acmp` | 1: `acmp-response-keyed-on-the-source` |
| `AcmpCore.A7EachGuardTermIsChecked` (test_acmp.cpp) | `acmp` | 4: `acmp-guard-controller-dropped`, `acmp-guard-sequence-id-dropped`, `acmp-guard-talker-dropped`, `acmp-guard-unique-id-dropped` |
| `AcmpCore.A7TheGuardReadsTheSentProbeNotTheBinding` (test_acmp.cpp) | `acmp` | 1: `acmp-guard-reads-the-binding` |
| `AcmpCore.A7ResponsesOutsideProbingAreIgnored` (test_acmp.cpp) | `acmp` | 1: `acmp-responses-taken-outside-probing` |
| `AcmpCore.A8SuccessSettles` (test_acmp.cpp) | `acmp` | 5: `acmp-header-no-tk-5s`, `acmp-no-tk-1s`, `acmp-settle-starts-no-srp`, `acmp-settle-swaps-stream-fields`, `acmp-vlan-masked` |
| `AcmpCore.A9FailureWaitsForTheRetry` (test_acmp.cpp) | `acmp` | 3: `acmp-failure-retries-at-200ms`, `acmp-failure-status-dropped`, `acmp-header-retry-2s` |
| `AcmpCore.A10NoResponseSendsTheDuplicateThenGivesUp` (test_acmp.cpp) | `acmp` | 3: `acmp-duplicate-takes-a-new-sequence-id`, `acmp-no-duplicate`, `acmp-second-timeout-keeps-status-0` |
| `AcmpCore.A11RetryWaitsForTheTalkerOrDelays` (test_acmp.cpp) | `acmp` | 2: `acmp-retry-ignores-discovery`, `acmp-retry-zeroes-the-status` |
| `AcmpCore.A12DelaySendsANewProbe` (test_acmp.cpp) | `acmp` | 2: `acmp-delay-resends-the-old-probe`, `acmp-sequence-id-never-advances` |
| `AcmpCore.A13NoTalkerAttributeReprobes` (test_acmp.cpp) | `acmp` | 2: `acmp-no-tk-keeps-srp`, `acmp-reprobe-ignores-discovery` |
| `AcmpCore.A14RegisteredSettlesTheReservation` (test_acmp.cpp) | `acmp` | 2: `acmp-registered-anywhere`, `acmp-registered-keeps-no-tk` |
| `AcmpCore.A15UnregisteredReprobes` (test_acmp.cpp) | `acmp` | 3: `acmp-reprobe-ignores-discovery`, `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp` |
| `AcmpCore.A16OneCounterForEveryNewProbe` (test_acmp.cpp) | `acmp` | 2: `acmp-sequence-id-never-advances`, `acmp-sequence-id-per-sink` |
| `AcmpCore.A17EachInterfaceTimerHoldsItsEarliestDeadline` (test_acmp.cpp) | `acmp` | 5: `acmp-expiry-not-consumed`, `acmp-expiry-takes-every-interface`, `acmp-timer-at-the-latest-deadline`, `acmp-timer-never-stopped`, `acmp-timer-port-called-every-time` |
| `AcmpCore.A18AZeroDelayProbesInTheSameExpiry` (test_acmp.cpp) | `acmp` | 2: `acmp-delay-up-to-4s`, `acmp-zero-delay-waits` |
| `AcmpCore.A18TheSeedIsTakenAtTheFirstDraw` (test_acmp.cpp) | `acmp` | 2: `acmp-rng-left-at-0`, `acmp-seed-at-every-draw` |
| `AcmpCore.A20ProbeTxIsAnsweredFromTheSource` (test_acmp.cpp) | `acmp` | 4: `acmp-probe-tx-any-interface`, `acmp-probe-tx-no-destination-mac-check`, `acmp-probe-tx-reports-asking-failed`, `acmp-unknown-source-answered` |
| `AcmpCore.A20DisconnectGetTxStateAndGetTxConnection` (test_acmp.cpp) | `acmp` | 5: `acmp-disconnect-always-succeeds`, `acmp-get-tx-connection-supported`, `acmp-get-tx-state-echoes-the-listener`, `acmp-get-tx-state-registering-failed-0`, `acmp-get-tx-state-unheld-mac` |
| `AcmpCore.A21MessagesNotForThisEntityAreIgnored` (test_acmp.cpp) | `acmp` | 2: `acmp-every-listener-is-this-one`, `acmp-every-talker-is-this-one` |
| `AcmpCore.A21MalformedFramesAreCounted` (test_acmp.cpp) | `acmp` | 2: `acmp-longer-pdu-refused`, `acmp-short-pdu-read` |
| `AcmpCore.A19AResponseWithoutRoomIsOwedAndItsChangeWaits` (test_acmp.cpp) | `acmp` | 2: `acmp-change-not-held-for-its-response`, `acmp-poll-drains-everything` |
| `AcmpCore.A19NothingPassesAnOwedFrame` (test_acmp.cpp) | `acmp` | 2: `acmp-poll-newest-first`, `acmp-response-passes-an-owed-frame` |
| `AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs` (test_acmp.cpp) | `acmp` | 1: `acmp-full-queue-acts` |
| `AcmpCore.A19AProbeWithoutRoomIsLostAndRecovered` (test_acmp.cpp) | `acmp` | 1: `acmp-lost-probe-uncounted` |
| `AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether` (test_acmp.cpp) | `acmp` | 1: `acmp-first-owed-releases-every-change` |
| `AcmpCore.A22AvailableDiscoversWhenTheGrandmasterMatches` (test_acmp.cpp) | `acmp` | 4: `acmp-discovery-reads-no-domain`, `acmp-discovery-reads-no-grandmaster`, `acmp-header-valid-time-in-seconds`, `acmp-valid-time-in-seconds` |
| `AcmpCore.A22DiscoveredStartsTheProbeFromPrbWAvail` (test_acmp.cpp) | `acmp` | 2: `acmp-discovered-probing-stays-passive`, `acmp-grandmaster-read-twice` |
| `AcmpCore.A22DiscoveredStateCells` (test_acmp.cpp) | `acmp` | 6: `acmp-discovered-interface-unchecked`, `acmp-grandmaster-sampled-for-the-refresh`, `acmp-refresh-notes-no-index`, `acmp-restart-mismatch-keeps-aging`, `acmp-restart-on-a-smaller-index-only`, `acmp-restart-raises-no-discovered` |
| `AcmpCore.A22DepartingAndAging` (test_acmp.cpp) | `acmp` | 4: `acmp-departing-interface-unchecked`, `acmp-departing-keeps-aging`, `acmp-departing-taken-undiscovered`, `acmp-no-aging` |
| `AcmpCore.A22OnlyBoundSinksOfThatTalkerOnThatInterface` (test_acmp.cpp) | `acmp` | 3: `acmp-discovery-on-every-interface`, `acmp-discovery-on-unbound-sinks`, `acmp-grandmaster-sampled-per-sink` |
| `AcmpCore.A22OtherAdpFramesAreIgnored` (test_acmp.cpp) | `acmp` | 4: `acmp-adp-discover-taken`, `acmp-adp-ethertype-unchecked`, `acmp-adp-short-frame-taken`, `acmp-adp-subtype-unchecked` |
| `AcmpCore.A23EveryEntryRefusesACallFromInsideAPort` (test_acmp.cpp) | `acmp` | 3: `acmp-reentry-unguarded`, `acmp-reentry-untrapped`, `acmp-send-port-unflagged` |
| `AcmpCore.A23EveryPortIsGuarded` (test_acmp.cpp) | `acmp` | 10: `acmp-changed-port-unflagged`, `acmp-clock-port-unflagged`, `acmp-gptp-port-unflagged`, `acmp-lock-port-unflagged`, `acmp-persist-port-unflagged`, `acmp-reentry-unguarded`, `acmp-seed-port-unflagged`, `acmp-source-port-unflagged`, `acmp-srp-port-unflagged`, `acmp-timer-port-unflagged` |
| `AcmpCore.A24ARestoredBindingFastConnects` (test_acmp.cpp) | `acmp` | 4: `acmp-record-unique-id-little-endian`, `acmp-restore-lands-in-prb-w-resp`, `acmp-restore-starts-no-discovery`, `acmp-restore-unique-id-little-endian` |
| `AcmpCore.A24UnboundRecordsRefusalsAndRollback` (test_acmp.cpp) | `acmp` | 2: `acmp-roll-back-keeps-the-bindings`, `acmp-unbound-record-not-zero` |
| `AcmpCore.A24StartedIsSavedAndReported` (test_acmp.cpp) | `acmp` | 1: `acmp-started-not-saved` |
| `AcmpCore.A25OnlyTable522ItemsAreReported` (test_acmp.cpp) | `acmp` | 3: `acmp-discovery-notifies`, `acmp-second-timeout-keeps-status-0`, `acmp-status-not-notified` |
| `AcmpMailbox.B1TheChannelCarriesCommandsAndResponsesInOrder` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-frames-on-the-adp-channel`, `acmp-frames-to-the-own-mac` |
| `AcmpMailbox.B2OwnUnicastIsAToleranceAndForeignUnicastIsRefused` (test_acmp_mbx.cpp) | `acmp` | 4: `acmp-frames-to-the-own-mac`, `app-own-mac-not-the-entity-mac`, `model-mismatch-never-counted`, `model-own-any-unicast` |
| `AcmpMailbox.B3TheTimersRunOnTheInterfaceSlot` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-no-resp-2s`, `acmp-timer-deadline-taken-as-a-delay`, `acmp-timer-on-the-next-slot` |
| `AcmpMailbox.B4AnExpiryThatRacedAStopOrAReArmIsDiscarded` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-stale-tag-taken`, `acmp-stop-keeps-the-arm`, `acmp-tag-reused` |
| `AcmpMailbox.B5TheTapHandsAvailableToDiscoveryAndTheRestToAdp` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-no-tap`, `acmp-tap-drops-the-rest`, `acmp-tap-takes-discover` |
| `AcmpMailbox.B6TheGrandmasterIsTheInterfaces` (test_acmp_mbx.cpp) | `acmp` | 1: `acmp-domain-not-sampled` |
| `AcmpAdapterUnit.B7RefusalsOfTheAdapter` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-attach-before-adp`, `acmp-attach-ignores-poll-room`, `acmp-attach-ignores-sink-room`, `acmp-interfaces-past-the-mailbox`, `acmp-slots-past-the-bank` |
| `AcmpMailbox.C0ToC4CommandsAreAnsweredInThePassThatTakesThem` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-bind-reads-the-clock-twice`, `acmp-get-rx-state-reads-the-clock`, `acmp-probe-response-reads-the-clock-twice`, `acmp-talker-reads-the-clock`, `acmp-unbind-reads-the-clock` |
| `AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-delay-reads-the-clock-again`, `acmp-expiry-reads-the-clock-twice`, `acmp-no-tk-samples-the-grandmaster`, `acmp-retry-samples-the-grandmaster`, `acmp-second-no-resp-samples-the-grandmaster` |
| `AcmpMailbox.C10C11DiscoveryPathsAreServedInThePassThatTakesTheRecord` (test_acmp_mbx.cpp) | `acmp` | 4: `acmp-available-reads-the-clock-twice`, `acmp-departing-samples-the-grandmaster`, `acmp-grandmaster-read-twice`, `acmp-timer-never-stopped` |
| `AcmpMailbox.C12AgingIsServedInThePassThatTakesTheExpiry` (test_acmp_mbx.cpp) | `acmp` | 1: `acmp-aging-samples-the-grandmaster` |
| `AcmpMailbox.E1AnOwedResponseLeavesFirstAndItsChangeAfterIt` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-change-not-held-for-its-response`, `acmp-poll-owes-nothing` |
| `AcmpMailbox.E2AnOwedResponseIsCommittedInPassKPlus1` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-poll-drains-everything`, `acmp-poll-newest-first` |
| `AcmpMailbox.F0ToF3FullRingsAreTakenWithinTheBound` (test_acmp_mbx.cpp) | `acmp` | 5: `acmp-backlog-understated`, `acmp-pass-bound-understated`, `events-halved`, `model-event-ring-a-record-short`, `rx-one-record-per-pass` |
| `AcmpMailbox.F4TheSmallestRecordsTheFilterPassesFillTheRing` (test_acmp_mbx.cpp) | `acmp` | 2: `acmp-backlog-understated`, `acmp-smallest-record-overstated` |
| `AcmpMailbox.F5AnAvailableBehindAFullAdpRingIsServedWithinTheBound` (test_acmp_mbx.cpp) | `acmp` | 3: `acmp-adp-ring-bound-understated`, `acmp-discovery-takes-the-first-sink`, `rx-one-record-per-pass` |
| `AcmpMailbox.U5AcmpComesAfterAdpAndReadsNothingBeforeTheContract` (test_acmp_mbx.cpp) | `acmp` | 4: `acmp-init-reads-the-seed`, `acmp-no-tap`, `app-acmp-before-adp`, `app-acmp-never-composed` |
| `ListenerWalk.Graded` (acmp_walk.cpp) | `acmpwalk` | 35: `acmp-bind-count-0`, `acmp-bind-new-keeps-srp`, `acmp-bind-starts-no-discovery`, `acmp-delay-resends-the-old-probe`, `acmp-discovery-notifies`, `acmp-duplicate-takes-a-new-sequence-id`, `acmp-failure-retries-at-200ms`, `acmp-failure-status-dropped`, `acmp-getrx-count-unbound`, `acmp-getrx-no-fast-connect`, `acmp-header-no-resp-2s`, `acmp-header-retry-2s`, `acmp-no-duplicate`, `acmp-no-tk-1s`, `acmp-no-tk-keeps-srp`, `acmp-probe-without-fast-connect`, `acmp-probing-status-not-notified`, `acmp-rebind-same-reprobes`, `acmp-registered-anywhere`, `acmp-registered-keeps-no-tk`, `acmp-registered-kind-dropped`, `acmp-reprobe-ignores-discovery`, `acmp-responses-taken-outside-probing`, `acmp-retry-ignores-discovery`, `acmp-retry-zeroes-the-status`, `acmp-second-timeout-keeps-status-0`, `acmp-sequence-id-per-sink`, `acmp-settle-starts-no-srp`, `acmp-settle-swaps-stream-fields`, `acmp-unbind-echoes-the-talker`, `acmp-unbind-keeps-discovery`, `acmp-unbind-keeps-srp`, `acmp-unbind-not-persisted`, `acmp-unregistered-anywhere`, `acmp-unregistered-keeps-srp` |
| `ListenerScenario.LD3TheLockRefusalStatus` (acmp_walk.cpp) | `acmpwalk` | 1: `acmp-not-authorized-is-13` |
| `ListenerScenario.LW2GuardsUnknownSinksAndForeignMessages` (acmp_walk.cpp) | `acmpwalk` | 4: `acmp-guard-controller-dropped`, `acmp-guard-sequence-id-dropped`, `acmp-guard-talker-dropped`, `acmp-guard-unique-id-dropped` |
| `DiscoveryWalk.Graded` (acmp_walk.cpp) | `acmpwalk` | 10: `acmp-departing-interface-unchecked`, `acmp-departing-keeps-aging`, `acmp-discovered-interface-unchecked`, `acmp-discovery-reads-no-domain`, `acmp-discovery-reads-no-grandmaster`, `acmp-no-aging`, `acmp-refresh-notes-no-index`, `acmp-restart-mismatch-keeps-aging`, `acmp-restart-raises-no-discovered`, `acmp-valid-time-in-seconds` |
| `TalkerWalk.TW1ProbeTheFlagLawAndTheSource` (acmp_walk.cpp) | `acmpwalk` | 2: `acmp-probe-tx-echoes-every-flag`, `acmp-probe-tx-no-destination-mac-check` |
| `TalkerWalk.TW2GetTxStateReadsRegisteringFailedLive` (acmp_walk.cpp) | `acmpwalk` | 3: `acmp-get-tx-state-echoes-the-listener`, `acmp-get-tx-state-registering-failed-0`, `acmp-unknown-source-answered` |
| `TalkerWalk.TW3DisconnectAndGetTxConnection` (acmp_walk.cpp) | `acmpwalk` | 2: `acmp-disconnect-always-succeeds`, `acmp-get-tx-connection-supported` |
| `TalkerWalk.TW4TheInterfaceAndTheStatelessProperty` (acmp_walk.cpp) | `acmpwalk` | 1: `acmp-probe-tx-any-interface` |
| `AcmpStore.N1ABindSurvivesAPowerCycleAndFastConnects` (test_acmp_nvm.cpp) | `acmpnvm` | 6: `acmp-nothing-persisted`, `acmp-nvm-bindings-latched-by-the-others`, `acmp-nvm-bindings-to-the-others`, `acmp-restore-announced`, `acmp-restore-lands-in-prb-w-resp`, `acmp-restore-starts-no-discovery` |
| `AcmpStore.N2AnUnbindIsSavedAsAnUnboundRecord` (test_acmp_nvm.cpp) | `acmpnvm` | 1: `acmp-unbind-not-persisted` |
| `AcmpStore.N3EachSinksStartedStateIsSaved` (test_acmp_nvm.cpp) | `acmpnvm` | 2: `acmp-record-flags-swapped`, `acmp-started-not-saved` |
| `AcmpStore.N4AnUnreadSlotRefusesPersistence` (test_acmp_nvm.cpp) | `acmpnvm` | 1: `acmp-rebind-not-persisted` |
| `AcmpStore.N5ARecordTheCoreRefusesKeepsItsDefault` (test_acmp_nvm.cpp) | `acmpnvm` | 1: `acmp-nvm-refusal-applied` |
| `AcmpStore.N6TheRollBackAndEveryOtherGroup` (test_acmp_nvm.cpp) | `acmpnvm` | 7: `acmp-nvm-d3-roll-back-kept`, `acmp-nvm-latch-length-unchecked`, `acmp-nvm-model-always-ready`, `acmp-nvm-refusal-applied`, `acmp-nvm-release-dropped`, `acmp-nvm-settle-dropped`, `acmp-roll-back-keeps-the-bindings` |

Labelled assertions inside a test are not each proven. Of the 323 labelled `EXPECT`/`ASSERT`
statements in the four sources, 152 are named by no defect's words at the head (168 before
this round). The rule enforced mechanically is F1's (every test is named), plus the checks
the test names themselves carry (C6 to C9, F0 to F2), which now have defects of their own.
Some of the 152 are preconditions (for example "B1 the filter passes a BIND_RX"); the rest
are a gap a reviewer may weigh under `Tests`.

Co-simulation (`make run-cosim`): the planted firmware defect "ACMP never composed"
(`ctrl_app.c`, `return true ||`) fails `the firmware answered ACMP on the model, each frame
of the scenario in order` (run by hand, tree restored; the RTL campaign `mutants.py` builds
only the suite).

### Coverage table

`python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4`, rc 0, at the head:

| File | Lines | Branches | After exclusions |
|---|---:|---:|---|
| sw/firmware/ctrl/acmp/acmp.c | 690/690 | 316/316 | 100 % / 100 % |
| sw/firmware/ctrl/acmp/acmp_mbx.c | 66/66 | 26/26 | 100 % / 100 % |
| sw/firmware/ctrl/acmp/acmp_nvm.c | 38/38 | 10/10 | 100 % / 100 % |
| sw/firmware/ctrl/adp/adp.c | 168/170 | 73/80 | 100 % / 100 % |
| sw/firmware/ctrl/adp/adp_mbx.c | 83/83 | 38/40 | 100 % / 100 % |
| sw/firmware/ctrl/app/ctrl_app.c | 20/21 | 17/20 | 100 % / 100 % |
| sw/firmware/ctrl/loop/ctrl_loop.c | 95/95 | 56/56 | 100 % / 100 % |
| sw/firmware/ctrl/mbx/mbx.c | 173/173 | 62/62 | 100 % / 100 % |
| sw/firmware/ctrl/mbx/mbx_wire.h | 15/15 | 12/12 | 100 % / 100 % |
| sw/firmware/ctrl/plat/mbx_plat_mmio.c | 10/10 | 0/0 | 100 % / 100 % |
| sw/firmware/ctrl/port/ctrl_debug.c | 19/19 | 6/6 | 100 % / 100 % |
| sw/firmware/ctrl/port/ctrl_pool.c | 99/99 | 60/60 | 100 % / 100 % |
| sw/firmware/ctrl/port/shlan_port.c | 22/22 | 6/6 | 100 % / 100 % |
| sw/firmware/ctrl/wire/wire.h | 10/10 | 2/2 | 100 % / 100 % |
| sw/firmware/ctrl_nvm/nvm_klj2.c | 195/196 | 104/108 | 100 % / 100 % |
| sw/firmware/ctrl_nvm/nvm_store.c | 434/434 | 259/266 | 100 % / 100 % |
| sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c | 100/100 | 63/64 | 100 % / 100 % |

The ACMP files are 100 % raw. The one new exclusion (`ctrl_app.c`, the ACMP attach refusal,
unreachable in the composition) is `sw/firmware/gtest/README.md:319`, with its reason; F0's
row moved with the function to `ctrl_app_compose`.

### Measured figures

- Per path, in mailbox accesses on the host model (bound / measured): BIND_RX 72/72, UNBIND_RX
  48/48, GET_RX_STATE 47/47, PROBE_TX_RESPONSE 28/28, talker commands 47/47, TMR_DELAY or the
  first TMR_NO_RESP 34/34, the second TMR_NO_RESP, TMR_RETRY, TMR_NO_TK 13/12 to 13,
  ENTITY_AVAILABLE 35/35, ENTITY_DEPARTING 30/29, TMR_NO_ADP 12/12.
- Backlogs: pass bound 985 (worst measured 185); an event by pass 2 (2,955); an ACMP command
  behind a full acmp ring by pass 10 (10,835; measured 19 smallest records cleared in pass 10);
  an ENTITY_AVAILABLE behind a full adp ring by pass 21 (21,670; measured pass 13 of 26
  records, 333 accesses); an owed response in pass k + 1 (8,865; measured 25, 100, 200 for
  k = 0, 3, 7).
- RV32I freestanding (`riscv32-linux-gcc -march=rv32i -mabi=ilp32`): text 11,756 bytes at the
  base, 24,848 at the head; data 0; bss 170 (unchanged); externals `__lshrdi3, __mulsi3,
  __udivsi3, __umodsi3, memcpy, memset, vsnprintf` (no heap). Static state on RV32:
  `struct acmp` 4,416 bytes (a sink 224), `struct acmp_mbx` 4,464, `struct ctrl_app` 6,544.
- Co-simulation: 12 frames (5 ADP, 7 ACMP), identical bytes and NOW_MS on the RTL and the
  model; 28 checks, 0 failures.

### Gate table

Each command run on its own, at head `351ae81f`, rc recorded, output never piped.

| Gate | Command | rc | Result |
|---|---|---:|---|
| firmware-unit: tally | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | the tally reads a failing and a crashing test as failures |
| firmware-unit: ctrl suites | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32` | 0 | every arm PASS: `acmp` 67, `acmpwalk` 127, `acmpnvm` 6 tests; rv32 text 24,848 bytes, no heap symbol |
| ctrl campaign | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice K/12`, K = 1 to 12, each its own process | 0 (x12) | `mutants: 24 of 24 caught` in every slice: 288 of 288, 0 escapes, 0 unnamed tests |
| firmware-unit: coverage | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | |
| firmware-unit: coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | 17 files at the ratchet, 100 % lines and branches after exclusions (146 s) |
| firmware-unit: store | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 5 shapes, 434 tests (98 s) |
| mbx suite | `make -C tb/verilator/mbx clean`, then `make -C tb/verilator/mbx -j2 run-wb run-axil` | 0 | 285 checks (Wishbone), 330 (AXI4-Lite) |
| mbx suite | `make -C tb/verilator/mbx` | 0 | both adapters; co-simulation 28 checks, 12 identical frames; two interfaces 285/330/285; `mutants.py --quick` 5 of 5 |
| mbx suite | `make -C tb/verilator/mbx mutants` | 0 | `mbx mutants: 67 of 67 caught` (107 s) |
| contract | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | 0 findings |
| contract | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | 0 arms failed |
| builder bank | `python3 sw/builder/test_builder.py --require-rv32` | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a placed utilization report from a Vivado build tree, which this host does not hold (1,255 s, RTL mutation variants linted) |
| saved-state writer | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 5 shapes, every planted defect reddened |
| scope | `git diff --stat 021b9c1f HEAD -- hdl sw/litex configs sw/mailbox` | | empty |
| docs workflow | `python3 scripts/docs_check.py` | 0 | |
| docs workflow | `python3 scripts/check_em_dash.py --base 6714181d0c8a16e2983f85b724f4d688f5111835` | 0 | |
| docs workflow | `python3 scripts/check_em_dash.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_doc_style.py` | 0 | |
| docs workflow | `python3 scripts/check_doc_style.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py --selftest` | 0 | |
| docs workflow | `python3 docs/DOC_MAP.gen.py --check` | 0 | |
| docs workflow | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | |
| docs workflow | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | |
| docs workflow | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_solution_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_solution_docs.py --selftest` | 0 | |
| docs workflow | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | |
| docs workflow | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_submodule_docs.py` | 0 | |
| docs workflow | `python3 scripts/check_submodule_docs.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_diagram_pngs.py` | 0 | |
| docs workflow | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_feature_status.py --self-test` | 0 | |
| docs workflow | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | |
| docs workflow | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | |
| docs workflow | `python3 scripts/measure_control_flow.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_cohesion.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_naming.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_naming.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_port_contracts.py` | 0 | |
| docs workflow | `python3 scripts/check_port_contracts.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_fail_fast.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_fail_fast.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_todo_ownership.py` | 0 | |
| docs workflow | `python3 scripts/check_todo_ownership.py --selftest` | 0 | |
| docs workflow | `python3 scripts/measure_test_evidence.py --check` | 0 | |
| docs workflow | `python3 scripts/measure_test_evidence.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_hygiene.py --check` | 0 | |
| docs workflow | `python3 scripts/check_hygiene.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sv_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_sv_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_cpp_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_py_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_py_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sh_idiom.py` | 0 | |
| docs workflow | `python3 scripts/check_sh_idiom.py --selftest` | 0 | |
| docs workflow | `python3 scripts/ci_events.py --check` | 0 | |
| docs workflow | `python3 scripts/ci_events.py --selftest` | 0 | |
| docs workflow | `python3 scripts/act_ci.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_doc_paths.py` | 0 | |
| docs workflow | `python3 scripts/check_archive.py` | 0 | |
| docs workflow | `python3 scripts/check_archive.py --selftest` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --selftest` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --verify-anchors` | 0 | |
| docs workflow | `python3 scripts/gen_toc.py --check` | 0 | |
| docs workflow | `python3 avdecc/gen_aem_store.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_deploy_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_baremetal_only.py --check` | 0 | |
| docs workflow | `python3 scripts/check_baremetal_only.py --selftest` | 0 | |
| docs workflow | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_nvm_record_space.py` | 0 | |
| docs workflow | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_nvm_capture.py` | 0 | |
| docs workflow | `python3 scripts/check_soc_sources.py` | 0 | |
| docs workflow | `python3 scripts/check_soc_sources.py --selftest` | 0 | |
| docs workflow | `python3 sw/litex/iob_pack_selftest.py` | 0 | |
| docs workflow | `python3 scripts/check_rtl_source_lists.py` | 0 | |
| docs workflow | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | |
| docs workflow | `python3 scripts/check_sweep_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_entity_shape.py --self-test` | 0 | |
| docs workflow | `python3 scripts/check_wire_accountability.py --self-test` | 0 | |

Verilator for every build and lint above: the pinned 5.050 (`verilator --version` printed
in each log). Temporary trees on the scratch disk, except the ctrl suite run and campaign
slice 1, which used the default temporary directory before that was set. The docs-workflow commands
are the `docs.yml` steps that need no hosted install; not run here: the HDL reference build
(its pinned pip set), the wavedrom no-drift checks (`wavedrom` not installed) and the
`--absent` compiler audit, none of which reads a file this lane changed. The em-dash base is
`git merge-base origin/dev HEAD` (`6714181d`), which includes F0's and FC's lines.
Peak memory of the service unit during the campaign: 4.4 GiB.

### Open questions and risks

1. **The adp channel's AVAILABLE/DEPARTING term (decision open, TAKEN comment 6026823815).**
   The contract passes only ENTITY_DISCOVER into the adp channel and both terms are used; any
   added term changes the elaborated filter (RTL), which this lane may not touch. Until it
   lands, discovery receives nothing from the fabric: a restored binding waits in
   PRB_W_AVAIL, and a bound sink whose probe fails or times out reaches PRB_W_AVAIL after
   TMR_RETRY (5.5.3.5.30 step 1) and stays there. H-DISC is shown on the host model with
   records written into the adp ring in the contract's layout, and the co-simulation shows
   the RTL's filter refusing the AVAILABLE as the model does.
2. **T_svc at full backlog.** The full-ring bounds fit T_svc = 10 ms only at 0.92 us per
   access or less (acmp ring) and 0.46 us or less (H-DISC behind a full adp ring; 0.92 us for
   the 20 ms ceiling). The access time is unmeasured (A4). The bounds charge every term at
   its maximum at once; the measured backlogs are far below them.
3. **Processor differences (submodule, not changed here; for the maintainers to file):**
   lock refusal status 13 instead of 16 (`pp_acmp_pkg.sv:123`); UNBIND_RX_RESPONSE echoes the
   talker fields (Table 5.36: 0); TMR_RETRY with the talker discovered zeroes the ACMP status
   (5.5.3.5.30 step 2 sets none); DISCONNECT_TX of an unknown source answers SUCCESS (5.5.4.2
   step 1: TALKER_UNKNOWN_ID). Not exercised by the reused stimulus: the processor masks
   stream_vlan_id to 12 bits (5.3.8.9 keeps the value); its probe guard reads the current
   binding's controller rather than the sent probe's.
4. **Harness finding (F0's, not changed here):** `tb/verilator/mbx/Makefile`'s `run-cosim`
   relinks `Vmbx_cosim` only when Verilator rebuilds, so a firmware-only change runs a stale
   binary in a dirty tree; CI builds from clean. All evidence here is from `make clean`.
5. The `--no-ff` merge of `dev` is owed once FC is in `dev`; the gates must then run again.
