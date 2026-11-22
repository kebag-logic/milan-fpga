# HANDOFF r2: [A814] gPTP in software on the #872 optimisation line, round 2 (#884, #665 F6)

Status: round 2b **REVIEW READY** at `f15b3a7d` (2026-11-22; section "Round 2b" at the end). Round 2 was REVIEW READY at
`17d9d54a`. Rulings: #884 issuecomment-7067495546 (round 2) and issuecomment-7072401468 (round 2b), manager [A10].

Lane: `/data-2/milan/lanes/opt-gptp-sw`, branch `opt-gptp-sw-1`. Rebased onto `origin/dev-soft-core-optimisation`
`59b09884` (it moved by one merge, PR #945, which adds only `.github/ci-templates/docs.yml`; no overlap). Round 1's
nine commits are now `634a7d2c..424c8cf1`. Local commits only; nothing pushed; no PR; no comment posted this round.
Scratch: `/data-2/milan/tmp/gptpsw-a814`.

## Clauses confirmed (receipts/std/clauses.md)

- IEEE 802.1AS-2011 B.2.3: Pdelay turnaround <= 10 ms. Confirmed.
- Milan v1.2 4.2.6.2.6 relaxes it by 50 %, to 15 ms. Confirmed.
- Milan v1.2 8.3.4: a redundant entity implements two gPTP time-aware end stations, one per AVB interface, with no
  bridge between them. Confirmed; the ruling's "one PHC and one timestamp unit per MAC" follows from it.

## Plan (rulings applied)

| Item | Ruling | State |
|---|---|---|
| Turnaround measured at 8x8/2if (and 8x8/1if) | 1, 4 | done: 0.266 ms and 0.186 ms; THE SHARE held with the gptp burst in every composed row |
| Flood with a planted overrun; no legitimate stamp lost | 2 | done: the trailer from a stamp FIFO in step with the frame FIFO; TSU bench T2, closed-loop flood |
| Memory refusal lifted for gPTP images as recorded debt | 4 | done: three ledger entries; both 8x8 points measured with gPTP |
| One PHC + one TSU per MAC; 2if closed loop, two peers | 5 | done in the closed loop; the product SoC has one MAC (for a decision) |
| Plane stays buildable | 6 | kept; routed at this head for the A/B |
| Status block narrowed, REGISTER_MAP, answers = GEN snapshot, saving from synthesis | 7 | done: S3 −3,049 FF |
| Closed-loop plants; gptp groups at 8x8/2if | R2-4 | done (14 plants; the groups run at 8x8 and 8x8-1if) |
| Census `GPTP_SW_EN_P` shape and plant | R2-4 | not done: needs census rulings for the rows the sw build ties off (REPORT section 5) |
| Adapter gated on its event bits | R2-5 | done: no poll, each callback publishes the port it ran |
| 64x64/2if on [A813]'s split | R2-5 | not done: no gPTP image is placed there yet |
| Nothing in 2.5 assumes hart 0 | contract | TIMESTAMP names no hart |
| gPTP in the platform image (the `--sw-gptp` route's) | 4, 6 | done: `CTRL_PLAT_GPTP`, 62.0 RAMB36 at 8x8/1if |
| Routed 8x8/1if `--sw-gptp` x3 directives against the plane | | done: all meet #818's floor, best +0.237 ns |
| Final gates | | see the gate table |

## Measured (receipts/harness, receipts/syn, receipts/route)

- Harness, split CPU at 100 MHz, images `--with-gptp` at their ledgered points, built at `0e476c94` (the commits
  after it touch none of the harness's inputs):

  | Point | Turnaround (10 ms) | Composed maximum (THE SHARE 2.0 ms) | Passes over the share | gptp records under the composed load, last | gPTP CPU after link-up | Steady, slave / master |
  |---|---:|---:|---:|---:|---:|---:|
  | 8x8/2if | 0.266 ms | 1.633 ms | 0 of 5,214 | 7.945 ms | 0.308 % | 0.343 % / 0.315 % |
  | 8x8/1if | 0.186 ms | 1.638 ms | 0 of 5,441 | 7.491 ms | 0.264 % | 0.291 % / 0.256 % |

- The seven `backlog-owed` instances over 20 ms at each point are the held-egress rows. At 8x8/1if, graded by
  `egress_ledger.py`: six within their figures; `backlog-owed.service.acmp.last.if0` 62.640 ms against 62.62
  (+0.020 ms). Its service past the 60 ms hold is 2.640 ms with gPTP against 2.490 ms without (the ledger's
  measurement): the 16 Pdelay_Req records add 0.150 ms (6.0 %), past the ledger's 5 %. For a decision.
- S3 synthesis (`--sw-gptp`, 8x8/1if, same recipe as round 1's S2): −3,049 FF whole design; the narrowing's own
  hierarchy −609 FF / −653 LUT in KL_mbx, −1,232 FF / −756 LUT in KL_mbx_cdc's publication crossing, −1,198 FF /
  −716 LUT in the datapath's decode; the trailer +85 FF / +146 LUT / +86 LUTRAM in the split tap; the unit's
  egress-only FIFO −87 FF / −111 LUT. Whole-design LUT −33: modules this round did not touch move ±1.3k between
  the two syntheses.
- Routes at 8x8/1if (clones at `40bd7738`): `--sw-gptp` ExtraPostPlacementOpt WNS +0.098 / WHS +0.028 ns,
  ExtraTimingOpt +0.152 / +0.023 ns, AltSpreadLogic_high +0.237 / +0.023 ns, every corner, all meeting #818's floor;
  38.2k-38.4k LUT, 45,814 FF, 95.5 BRAM tiles. The plane, ExtraPostPlacementOpt: 43,166 LUT, 51,284 FF, 11 DSP,
  95.5 tiles, +0.139 / +0.036 ns. Worst paths in the mailbox (map edit crossing, DMA, register read), not gPTP.

## Findings

- Contract 2.5 grows the 8x8/1if platform image without gPTP: `ctrl_plat` 18,944 -> 19,008 B, rom 139,208 ->
  139,408 B (base `59b09884` measured in a clean clone), past the 139,264 B its 58.0 entry holds: 58.5. The two-
  interface image still matches its entry (21,568 B, 63.0).
- The loop's poll table is full on the platform (8 of 8), so the adapter publishes from its callbacks instead.
- The split ISA has no divide: the PHC rate is derived from PTP_INCR by shifts and subtractions.
- Round 1's `gptp_sw` and `gptp_tsu` suites had no `SUITE_SECONDS` entry, so the sharded sweep refused; registered
  (`ee0d920c`, pinned in the test-evidence contract `34dbab53`).
- Three plants no longer applied after rounds 1 and 2's edits: the platform campaign's saved-state plant (`99a329de`),
  the census's unraised-notification plant (`fb53183f`), and the driver campaign's face-count plant, whose `else`
  no longer compiled once round 1's TIMESTAMP branch followed it (`c3c03fd9`); each plants the same defect at the
  moved text.
- `milan_dp`'s `split-sw` is not a default case, so the sweep does not run it; run by hand (151 checks PASS).
- Host OOM at 21:11 (app.slice) killed a campaign; campaigns then ran at 3 jobs. Firmware shards run together in
  one clone race on its `dispatch-build` (a spurious link failure); each shard then ran in its own clone.

## Changes, each with its place and reason

Round 2's commits on round 1's `424c8cf1`: `32bfb2ca`, `29b8d697`, `cbe2a808`, `6c38cf10`, `ccdd150d`, `40bd7738`,
`9f97ee71`, `0e476c94`, `175f114e`, `5010b5dc`, `c9f6b873`, `14a54bbc`, `99a329de`, `6adf9dd5`, `ee0d920c`,
`fb53183f`, `34dbab53`, `c3c03fd9`, `9dacf75b`, `17d9d54a`.

RTL and contract (ruling items 2 and 7):

- `hdl/milan/KL_ctrl_split.sv:74, :324-345, :362`: `GPTP_P` passes gPTP frames to the mailbox with an eight-octet
  ingress trailer from a 64-entry stamp FIFO in step with the frame FIFO; a gPTP frame with no stamp entry left is
  refused at beat 1 and counted in `rx_drops_o`. Reason: no stamp of a delivered frame can be lost (item 2).
- `hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv:59, :183, :294`: the FIFO holds egress records only, 32 of them; the
  ingress stamp leaves on `rx_stamp_o`/`rx_event_o`. Reason: the ingress stamp rides with its frame.
- `hdl/milan/milan_datapath.sv:9391, :9402, :10332-10333`: the trailer wiring; the narrowed words decoded (parent,
  delay, path, count, gen tied 0); the AVB_INFO/AS_PATH change outputs off under `GPTP_SW_EN_P`. Reason: item 7.
- `sw/mailbox/mailbox.yaml:91, :1135, :1318`: the trailer, TIMESTAMP egress only and naming no hart, the
  publication narrowed to `GPTP_GM_LO/HI`, `GPTP_STATE`; regenerated `KL_mbx_pkg.sv`, `KL_mbx.sv`,
  `mbx_contract.h`, `MAILBOX_CONTRACT.md`. Reason: item 7 and contract 2.5 routable to either hart.
- `scripts/register_descriptions.json`, `docs/reference/REGISTER_MAP.md`: the zero-under-`--sw-gptp` reads
  (PDELAY, AS2_LO/HI, ASP_CMD) and the drop counters' meaning. Reason: item 7, REGISTER_MAP in the same change.

Firmware (items 5, 7, R2-5, and the platform image the route needs):

- `sw/firmware/ctrl/gptp/gptp_mbx.c:102, :125, :156, :176, :205`: the trailer read before `gptp_port_rx`; the
  snapshot kept and published from each callback, no poll; the AECP changes raised. Reason: R2-5, item 7, and the
  platform's full poll table.
- `sw/firmware/ctrl/aecp/aecp_face.c:208, :346, :374`: GET_AVB_INFO's gPTP fields and GET_AS_PATH from the gPTP
  owner's snapshot. Reason: item 7.
- `sw/firmware/ctrl/plat/ctrl_plat.c:394, :457`, `ctrl_plat_csr.c:123-160`, `ctrl_plat.h`: `CTRL_PLAT_GPTP`
  composes the ports in the platform image on the CSR's PTP block, the PHC rate from PTP_INCR without a divide.
  Reason: a `--sw-gptp` build needs an image with gPTP (items 4 and 6).
- `sw/firmware/ctrl/test/ctrl_plat_image.py`: `--with-gptp`, its required symbols, the adapter measured as a member.
- `sw/firmware/ctrl/host/mbx_model.c:236, :611, :884`: TIMESTAMP depth 32, the published GPTP words kept as the
  datapath holds them.

Memory ledger (item 4): `sw/litex/ctrl_memory.py:269, :281, :354` (three gPTP entries; the platform's 8x8
one-interface entry re-measured at 58.5 under contract 2.5), `ctrl_memory_ledger.py` (the restated sizes, cases,
plants), `test_ctrl_memory.py`, `tb/verilator/ctrl_split_boot/plat_ledger.py` (a fifth point, built
`--with-gptp`).

Harness (items 1 and 4): `tb/verilator/ctrl_service_budget/build.py:321, :325` (gPTP images planned at their
ledgered points), `sim_main.cpp:302` (the trailer on each gptp record), `gptp_group.py:42` and `scenario.py:744`
(a peer's Pdelay_Req burst in every composed window of a gPTP image), `grade.py:64` (the record's size), the
self-test's checks in `selftest_opened.py`, `README.md`.

Benches: `tb/verilator/gptp_sw/*` (two interfaces, two peers, the trailer, the cut request, the silent
grandmaster, the pass invariant, `gptp_sw_mutants.py`); `tb/verilator/gptp_tsu/*` (the split tap after the unit,
I1-I5, the 80-frame flood, `tsu_mutants.py` 24 plants); `tb/verilator/milan_dp/*` (`split-sw`).

Docs: `docs/design/GPTP_SOFTWARE.md`, `SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md` (NFR-SCOUT-02, -03 by
the rulings), the module matrix.

## New checks (planted defect -> failing words)

| Planted defect | Campaign | The [FAIL] words that kill it |
|---|---|---|
| ingress stamp not handed to the port | `gptp_sw_mutants.py` | SLAVE if0 the PHC is within 100 ns of its grandmaster |
| trailer read least significant octet first | `gptp_sw_mutants.py` | SLAVE if0 the PHC is within 100 ns of its grandmaster |
| trailer left on the frame | `gptp_sw_mutants.py` | SLAVE if1 a Pdelay_Req cut short by its last eight octets |
| egress stamp dropped | `gptp_sw_mutants.py` | SLAVE if0 the measured link delay is its link's |
| second port steers the first PHC | `gptp_sw_mutants.py` | SLAVE if1 the PHC is within 100 ns of its grandmaster |
| snapshot not kept | `gptp_sw_mutants.py` | the snapshot holds the grandmaster it published |
| AECP notice not raised | `gptp_sw_mutants.py` | the AVB_INFO and AS_PATH changes were raised |
| GET_AS_PATH shifted | `gptp_sw_mutants.py` | GET_AS_PATH is the snapshot's path |
| publication skips the grandmaster | `gptp_sw_mutants.py` | the words the datapath takes are the snapshot's |
| a record's, an event's, a tick's change left unpublished (three) | `gptp_sw_mutants.py` | SLAVE the publication follows every port change |
| servo sign | `gptp_sw_mutants.py` | SLAVE if0 the PHC is within 100 ns of its grandmaster |
| responder's t2 from another frame | `gptp_sw_mutants.py` | SLAVE if0 the peer measures the link through the firmware's answers |
| 24 timestamp-unit and trailer defects | `tsu_mutants.py` | each its own (the campaign's table) |
| a gPTP image planned at the point of an image without it | harness self-test | a gPTP image's ledgered point is named at 8x8 only |
| a gPTP image's composed windows carry no gptp records | harness self-test | every composed window's stimulus is its defined load |
| six planted gPTP ledgers (no image_gptp, past the tiles, the product ctrl_plat) | `test_ctrl_memory.py` | the ledger's facts and REFUSED rows |

## Gate table

Final head `17d9d54a`. Each gate names the head it ran at; the commits after that head touch nothing in its scope
(listed under the table).

| Gate | Head | Result | Receipt |
|---|---|---|---|
| Full Verilator sweep, 4 parallel shards (`native-shards.py`, the CI-pinned Verilator 5.050) | `ee0d920c` | 67 of 67 suites PASS, 0 in-suite failures; `tsn_fuzz`'s tsn-gen campaigns, skipped there without `TSN_GEN_ROOT`, run at `9dacf75b`: 164 and 675 PASS | `receipts/sweep/` |
| Yosys portability, 4 shards (64 tops; tied-input and tap-purity gates) | `14a54bbc` | PASS | `receipts/yosys/` |
| Firmware gate, four shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`), a clone each | `99a329de`; shard 1 (the control campaign) `c3c03fd9` | 4 of 4 PASS; the control campaign 826 of 826 caught | `receipts/fwgate/` |
| Publication census, `--check --selftest --jobs 4` | `fb53183f` | 246 checks PASS; 57 of 57 rules proved | `receipts/census/` |
| Docs, idiom and light rtl-fast gates (73: docs_check, em-dash, doc style, gPTP docs, TOC, docs inventory, register reference, idiom x4 with self-tests, naming, port contracts, RTL and SoC source lists, test evidence, lint, xvlog, gen_mailbox, module matrix, ...) | `17d9d54a` | 73 of 73 PASS | `receipts/gates/` |
| `gptp_sw` suite (`make`: slave, master, flood; 48 checks) | `14a54bbc` | PASS | `receipts/closedloop/` |
| Closed-loop campaign, `gptp_sw_mutants.py` | `14a54bbc` | 14 of 14 killed | `receipts/closedloop/` |
| `gptp_tsu` suite and `tsu_mutants.py` | `14a54bbc` | PASS; 24 of 24 killed | `receipts/tsu/` |
| `milan_dp` `split-sw` and `split-cdc` | `14a54bbc` | 151 and 13 checks PASS | `receipts/milan_dp/` |
| `test_ctrl_memory.py` | `14a54bbc` | PASS | `receipts/memory/` |
| `plat_ledger.py --self-test` | `14a54bbc` | 5 points PASS, 9 of 9 controls | `receipts/memory/` |
| Harness self-test, `run.py --self-test` | `c9f6b873` | 1,017 checks PASS; 297 of 297 mutants caught | `receipts/harness/selftest/` |
| Harness legs, 8x8 and 8x8-1if `--with-gptp` | `0e476c94` | rc 0, 0 refusals; measurements in section 2 | `receipts/harness/` |
| `egress_ledger.py --point 8x8-1if` on the gPTP run | `0e476c94` | FAIL by 0.020 ms on one row (decision 1) | `receipts/harness/` |
| Routes, 8x8/1if `--sw-gptp` x3 directives and the plane | `40bd7738` | all four meet #818's floor | `receipts/route/` |
| S3 synthesis | `0e476c94` | section 2 | `receipts/syn/` |

What moved after each gate's head: `9f97ee71`, `0e476c94`, `5010b5dc`, `14a54bbc`, `6adf9dd5` docs and comments;
`175f114e` the gates' own fixes (the split-sw build flags, the campaign helper, two test modules' length, a linked
doc); `c9f6b873` and `34dbab53` the test-evidence scripts; `99a329de` the platform campaign's plant; `ee0d920c` the
sweep's duration table and timeouts; `fb53183f` the census's plant; `c3c03fd9` and `9dacf75b` the driver campaign's
face-count plant and its module's docstring; `17d9d54a` four comments (two in the adapter, one in the closed
loop, one doc line) citing #884 for a plan item. After `40bd7738` no commit changes RTL, the SoC, or firmware
source beyond those two comments; after `0e476c94` none changes the harness's run inputs (its self-test modules moved in
`175f114e`, and the self-test ran after it, at `c9f6b873`).

## Round 2b: the derived gptp admission burst (#884 issuecomment-7072401468)

Status: **REVIEW READY** at `f15b3a7d`; option (b)'s three conditions hold (no STOP). Rulings applied: item 1 option (b), item 2 (#962), item 3 (census shape owed), item 4 (PR order).

### The derivation (`sw/mailbox/mailbox.yaml`, the gptp channel's `rate`)

Seven an interface, times the interfaces: 7 at one interface, 14 at two (the ruling expected about 8 and 16).
- A full-duplex port receives seven message kinds from its one peer: IEEE 802.1AS-2020 Table 11-5 (Sync,
  Pdelay_Req, Pdelay_Resp, Follow_Up, Pdelay_Resp_Follow_Up) and Table 10-8 (Announce, Signaling); "other values
  for the messageType field ... are not used in this standard".
- Each at most once in one 10 ms refill window: Sync and Follow_Up every 125 ms; Announce, the peer's Pdelay_Req and
  the Pdelay_Resp pair answering the port's own request every second (Milan v1.2 4.2.6.2.2 Table 4.1); a
  gPTP-capable Signaling at its default second (10.7.2.5). 10.7.2.2 and 10.7.2.3 hold 90 % of the intervals within
  30 % of nominal, so the closest in-tolerance Sync pair is 87.5 ms apart.
- Not fitted to the row: the figure comes from the message kinds alone and was fixed before any re-measurement.

### Changes (commits `0bb83b9d`, `f828861c`, `62fcd154`, `f15b3a7d`)

- Contract: `rate: {burst_per_interface: 7, refill_ms: 10}`; `mailbox_model.py` scales a burst stated an interface
  by the contract's (or a variant's) interfaces (`_scaled`, `with_interfaces`) and range-checks the result;
  `mailbox_emit.py` states it in MAILBOX_CONTRACT.md. Generated: `KL_mbx_pkg.sv` and `mbx_contract.h` carry 7; a
  two-interface variant carries 14. Readers: the RTL's token buckets (`KL_mbx_rx.sv:747`, `:764`) and the host
  model (`mbx_model.c:55`); no firmware source, so the routed build's firmware image is byte-identical to round 2's.
- Harness: `scenario.admission` and `composed_load` at the point's interfaces; `grade.defined_load`, `check_load`
  and `composed` at the build's (`grade()`'s `at`, kept as `stated_at`); `channel_gate.loaded` through
  `with_interfaces`; `rows_grade.contract` reads a per-interface rate. The self-test restates the gPTP loads at one
  and two interfaces and plants the burst held at one interface's (caught).
- Found and fixed: six self-test stand-ins of `check_load` and `defined_load` had the base's signatures. Round 1
  added the opened-channel argument, so since then three mutants raised `TypeError` instead of planting their
  defect, and the selftest counted the raise as a catch. Each is now caught by its named check (the earlier-rule
  "load is the stimulus's own declaration" by its own refusal, as at the base).
- Found and fixed (`f15b3a7d`): the closed loop's two-interface contract and driver copy were a file target with no
  prerequisites, so a kept `obj_dir` kept its old contract. The lane's own one still read burst 16. The rule now
  depends on `mailbox.yaml`, the generator and the driver. `make -n -W <file>` regenerates for each of the three,
  where at `62fcd154` a `mailbox.yaml` change regenerated nothing. The round 2b flood receipt was built fresh
  (`gen/mbx_contract.h`: `MBX_CH_GPTP_RATE_BURST 14u`), and the sweep's clones are cleaned, so no receipt ran the old
  burst.
- `62fcd154` is the design page (GPTP_SOFTWARE.md: the burst, the bounds, the held row, #962, the census owed).

### Re-measured at `f828861c` (the harness's run inputs unchanged since)

| Point | Held row `acmp.last.if0` (ledger 62.62 ms) | egress_ledger.py | Turnaround (10 ms) | Last gptp record, composed load | Composed maximum | Passes over the share |
|---|---:|---|---:|---:|---:|---:|
| 8x8/1if (burst 7) | 62.535 ms | PASS, all seven rows within | 0.186 ms | 6.040 ms | 1.638 ms | 0 of 5,441 |
| 8x8/2if (burst 14) | 62.496 ms | no ledger at this point (see below) | 0.266 ms | 7.790 ms | 1.633 ms | 0 of 5,213 |

- The egress ledger is derived at 8x8/1if only (#894's ledger ruling; `--point` offers `8x8-1if` alone). Graded
  against those figures, the 8x8/2if run's six same-named rows are all within, and its held row is 62.496 ms. The
  tool still reports FAIL, for a structural reason: the composed load alternates its 16 AECP records over the
  interfaces (`n % p.interfaces`), so at 2if the AECP row's last instance is `aecp.last.if1` (62.088 ms, under the
  62.16 ms of its `if0` name). It is the same at round 2's burst of 16, and the same head without gPTP fails the same
  way (`receipts/round2b/harness/8x8-nogptp/`, at `62fcd154`: `aecp.last.if1` 61.771 ms, `acmp.last.if0`
  62.093 ms). So no option could make the tool green at 8x8/2if. Not a condition of option (b), which holds at both
  points; the 2if ledger is the ledger owner's.
- For the ledger owner: at 2if the burst of 14 adds 0.403 ms (19 %) to the held row's 2.093 ms of service past the
  60 ms hold, against 0.045 ms (1.8 %) at 1if. A 2if ledger derived by the 1if rule from the run without gPTP alone
  would be 62.20 ms, under the gPTP run's 62.496 ms.
- Re-routed at `62fcd154` (the burst reaches `KL_mbx_rx`; the firmware image is round 2's, byte for byte):
  AltSpreadLogic_high WNS +0.230 ns, WHS +0.015 ns; ExtraPostPlacementOpt +0.205 / +0.013 ns. Both meet #818's floor.
- Flood (closed loop at the derived burst, 14 at two interfaces): 977 handed out, 462 committed at once, 526
  refused or held, 490 received stamped, 0 unstamped, 0 egress records lost; the flooded port locked by 2.9 s,
  worst 95 ns after. 48 checks PASS.
- gPTP CPU after link-up unchanged: 0.308 % at 8x8/2if, 0.264 % at 8x8/1if.

All three conditions hold, so no STOP.

### Gates at the round 2b head (final head `f15b3a7d`)

| Gate | Head | Result |
|---|---|---|
| Full Verilator sweep, 4 shards | `f15b3a7d` | 67 of 67 suites PASS, 0 in-suite failures |
| Docs, idiom and light rtl-fast gates (73) | `f15b3a7d` | 73 of 73 PASS |
| Closed-loop campaign | `f15b3a7d`, `f828861c` | 14 of 14 killed at each |
| `milan_dp` `split-sw`, `split-cdc` | `f15b3a7d` | 151, 13 checks PASS |
| `plat_ledger.py --self-test`, `test_ctrl_memory.py` | `f15b3a7d` | PASS (five points as round 2's; 9 of 9 controls) |
| Harness self-test | `62fcd154` | 1,017 checks; 298 of 298 mutants caught |
| Firmware gate, four shards | `62fcd154` | 4 of 4 PASS; control campaign 826 of 826 |
| Yosys portability | `62fcd154` | 64 tops PASS |
| Publication census with self-test | `62fcd154` | 246 checks; 164 arms; 57 of 57 rules |
| Routes ASL and EPPO | `62fcd154` | both meet the floor |
| Harness legs; `egress_ledger.py` at 8x8-1if | `f828861c` | rc 0; PASS |

After `62fcd154` only `f15b3a7d` (the closed loop's Makefile), whose readers re-ran at it. Receipts:
`receipts/round2b/`, indexed in `receipts/INDEX.md`. Not posted: nothing on #884 this round (the resume asks for no
second comment); nothing pushed.
