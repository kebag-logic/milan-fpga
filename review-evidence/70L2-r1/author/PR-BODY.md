[A448]

Relates to #70

#70 lane 2: the parent adopts processor `b2db3a97` (processor `main`: PR #132,
D3 lane 1, merged as `d352bbaa`, plus PR #133, lane C1), under the
[lane-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5888775832),
the [scope record](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5880276193)
and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475)
on this lane's STOP. The processor's D3 writer now writes and restores the
scalar records (configuration, sampling rates, clock sources, both stream
formats, presentation offsets); the firmware loads the AEM image before the
restore and starts the walk on every boot path; and the parent glue, status,
harnesses, gates and documents follow PR #132's "Parent-visible for pin
adoption: rounds 1-6, consolidated" list and PR #133's declared parent edits.

## Items

1. **Pin** (`43ff2435`, then `504396aa` for `b2db3a97`): the gitlink;
   `syn/yosys/rom_digests.tsv` rows for both pins (content equal to
   `c951a9ff`'s: neither PR changes a ROM generator); the RTL source lists are
   derived and unchanged; the submodule boundary diagram, PNG and manifest;
   `docs/reference/SUBMODULES.md`.
2. **PR #132's consolidated list** (D3 sections 5.2 and 8.7):
   - `0a2ace1c`: `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`,
     `restore_cause_o[1:0]` and `d3_unflushed_o` connected in `KL_pp_shadow.sv`
     and carried to `PP_STAT[16]`, `[17]`, `[20:18]`, `[22:21]` (no new CSR);
     `pend_i` takes the D3 writer's unflushed records (`aecp_dyn_dirty_o` stays
     a diagnostic); the processor's combined done, busy, fail and blank.
   - `862dd4da`, `1b972392`: the restore deadlines and write backoff stay
     derived inside the processor from `CLK_HZ_P`, the parent's clock; nothing
     is restated at the instance.
   - `a8668505`: the `d3_mutants.py` disposition row.
   - The counter, snapshot word 37: graded in every `sim_nxn` leg and
     documented in the register map.
   - Harnesses: `d5eff227` (`gmstep`, `gptp`/`gptp-lat`, `ax1x1gptp`),
     `f43ff09d` (the image-less legs name CLOSED), `9cb94bdb` (`sim_nxn`: the
     AECP hold and word-37 drop replace the retired degrade arm; the
     wedged-memory arm runs after the image and reads word 36 around its heal),
     `f827d8ed` (render T8), `1c89332d` (`pp_shadow`), `ac26999e` (`nvm_cosim`).
3. **Firmware** (`4333a5a0`, #70 5880276193 item 2): every boot path starts the
   restore walk; the persistence-disabled path runs it blind; the wait ends on
   done or CLOSED. `sw/firmware/nvm_hosttest/test_boot_walk.py` boots five paths
   per shape: 9 findings on the dev firmware, both planted controls caught.
4. **The ruling's option 1**:
   - `20919727`: builder gate 1b keeps `aem_loaded`'s symbol slot across a call
     only while three pins hold on the source it compiled (one write, the
     verifier's; no address taken; a file-scope static of the one translation
     unit, declared once, emitted with internal linkage and named by no other
     unit), with the soundness argument in one comment at the rule. Five planted
     breaks are each refused on the verdict with the broken pin named:
     `aem_loaded = 0;` inside `nvm_boot()`, `aem_loaded = 1;` in the UART status
     handler, `&aem_loaded` taken and written through inside `nvm_boot()`, the
     verdict without `static`, and a second translation unit declaring it. An
     AEM-first base is accepted only with the slot kept and refused under the
     old forget-on-call rule.
   - `a6dc7f49`: `milan_init()` is `configure_fabric`, `load_aem_image`,
     `nvm_boot`, `entity_advertise` (D3 section 5.3 change 1), with the ledger
     fact and the order block; every statement that called it open is current.
5. **PR #133's declared parent edits**: `376391bb` re-bases the crflic `[C]`
   LeaveAll counts to `>= 3` and adds a check of the restart itself (every DUT
   LeaveAll at least 10 s after the switch's preceding one): 416/0 at
   `b2db3a97`, and exactly that check fails at the previous pin `d352bbaa`
   (5 and 5 LeaveAlls, the soonest DUT LeaveAll 2,210 ms after the switch's);
   the `milan_dp` README `[C]` row, "What it cannot show" and the failing-arm
   row. `73e50787`, `b61f1d3c`: `ieee8021q.md` MRP-4..MRP-7, the compliance
   matrix 4.2.7.1 and 4.2.7.3/4.4.1, CHANGELOG.
6. **Docs** (`3852b27c` and the commits above): the compliance matrix, the
   saved-state pages, the register map, the firmware and integration pages and
   `CHANGELOG.md` describe D3 lane 1 and the AEM-first order as in the product.
7. **The native service and capture evidence** (`18199bac`, `597dba85`): see
   the decision below; the capture receipt is re-recorded and
   `check_nvm_capture` passes.

## A decision for the reviewers: the service grader under the AEM-first order

The native service bank's first run at `b61f1d3c` refused every plan on two
findings, "over-budget tick stretch: aem_copy_crc" and "over-budget PHY service
stretch: aem_copy_crc". The harness measures the AEM duty from the first AEM
read to the entity enable. In the old order that span followed the writer's
arming (the first heartbeat opportunity) and held the copy alone (137 ms at
8x8). Under the ruled order it starts inside the pre-heartbeat prefix and holds
the copy, the CRC and `nvm_boot()` up to the walk: 1,015 ms with no heartbeat
opportunity, because none exists before the writer does. The harness README
already says that prefix "precedes writer liveness arming" and "must not be
interpreted as an armed-writer gap".

`18199bac` makes the enforce-service verdict charge every duty's tick and PHY
stretch from the first heartbeat opportunity; a duty that starts armed keeps
its whole span, so every old-order row and the three recorded oracle traces
grade exactly as before. The receipt records the arming cycle and the armed
bound. Three self-test controls pin the rule (the unarmed prefix is not
charged; an armed stretch one cycle past the allowance is refused on both
stretches; an armed duty keeps its whole span), and three planted wrong rules
are each refused by name. The retained failing log regrades to exactly the two
findings under the old rule and to none under the new one. The ruling did not
spell this out, so it is flagged here rather than assumed.

## Validation

At `597dba85`, clean tree, the physical path, every gate rc 0:

- Full builder bank with the RV32 compiler required (`--require-elaboration
  --require-rv32`), gate 1b reading "refused 5/5 planted pin breaks on the
  verdict, each naming its pin"; and with every cross-compiler candidate
  hidden. Both close "ALL GATES PASS EXCEPT n NOT RUN" on recorded reasons
  unrelated to this lane (the gate-11 calibration tree), as at the base.
- `milan_dp`, every leg: `gmstep` 104/0, `gptp` 182/0, `gptp-lat` 182/0,
  `obj_dir` 235/0, `notify` 382/0, `crflic` 416/0 (the restart check: the
  soonest DUT LeaveAll 10,210 ms after the switch's), `nxn` 1,845/0, `nxndv`
  1,847/0, `nxn8` 3,525/0, `nxn4c` 1,845/0, `nolpf` 235/0, `prune` 33/0,
  `ax1x1` 232/0, `aclk` 191/0; `ax1x1gptp` 139/0 with its negative control. Every leg that serves the
  image reads the walk done 1, CLOSED 0 before its first AECP command.
- `nvm_cosim` 465/465 and 39 of 39 mutants killed; its lint with no
  `PINMISSING`; `pp_shadow` 606, 606, 646 and 311 checks, 0 failures.
- `milan_dp_render` (65/0 and 152/0).
- `check_nvm_capture`, the firmware host tests (five boot paths on all five
  shapes, both planted controls caught), the `fw_service_budget` self-test
  (50 grading checks).
- Yosys portability, lint, `xvlog`, the source-list, port-contract, naming,
  evidence-classifier, idiom, feature-status, submodule, boundary-diagram,
  bare-metal-only and CI-scope gates, `git diff --check`, and the Markdown gates
  in the pinned environment.

The five native groups (PR #609's recipe), at `18199bac` (the only later
commit, `597dba85`, changes the receipt and three documents): 25 arms, 65
commands, all rc 0. Service 8x8 and 1x1: all twelve plans pass with no service
finding and zero unbacked cycles, the boot reading `walk done=1 fail=0 ...
closed=0` with the AEM copied first. Mutations: `remove-dispatch` 1,051 and 350
per-line findings, `late-sample` and `no-publish` caught by name. Capture: both
contract maxima unchanged (1x1 3.88779 ms, 12.6036x; 8x8 13.23352 ms,
3.7027x); the 100 MHz comparison moves to 9.95772 ms; `byte-only` 1.8358x,
`skip-copy` and `no-traffic` caught. `docs/findings/397_SERVICE_BUDGET.md` and
the snapshot page's section 18 carry the new figures; the page's tables are
regenerated by a script first validated by reproducing all 84 rows of the
previous page from PR #609's receipts.

Timing and area:

- Out-of-context `KL_pp_shadow` at the 1x1 arrays: 25,668 LUT, 25,937 FF, 16
  RAMB36 + 2 RAMB18, 8 DSP; the D3 writer is 912 LUT / 488 FF. PR #132's
  same-session delta for lane 1 is +1,031 LUT / +559 FF / 0 BRAM / 0 DSP; C1
  adds +93 LUT / +57 FF in `KL_srp_top` (same instrument against `d352bbaa`).
- Firmware: `milan_baremetal.o` text +287 B against the base firmware, same
  toolchain; the BIOS image text +232 B (about 41% of the 128 KiB ROM).

AX7101 1x1 TDM8 place sweep at `597dba85`, PR #615's recipe at 32 threads, the
three seeds run one at a time under the Vivado lock. Worst over the four
declared corners (Slow and Fast at 0 and 85 C):

| Seed | Directive | Worst WNS ns | Worst WHS ns | Refusal gate |
|---|---|---|---|---|
| asl | AltSpreadLogic_high | +0.064 | +0.034 | accepted |
| eto | ExtraTimingOpt | +0.034 | +0.034 | accepted |
| eppo | ExtraPostPlacementOpt | +0.135 | +0.014 | accepted |

- Every seed meets WNS >= +0.030 ns and WHS >= 0 at every corner; TNS and THS
  are zero. `eto` holds the least margin.
- `eto`'s router ended at WNS -0.248 ns (`Route 35-39`, a critical warning);
  the flow's post-route physical optimization closed it to +0.034 ns before
  the signoff reports and the bitstream. `asl` and `eppo` met at the router and
  carry no critical warning.
- Each log has none of the three refused diagnostics and 112 quasi-static
  cells; the build gate accepted all three bitstreams. All four Ethernet pairs
  read `Max Delay Datapath Only` at 8 ns.
- Post-place: at most 50,265 of 63,400 LUTs (79.3%), 58,796 registers, 92.5
  BRAM tiles, 14 DSPs.

## What remains for lanes 3-5

- Lane 3: the user names (both ENTITY names and every writable ordinal), their
  trigger, replay and cold cycle.
- Lane 4: both channel-map directions and the format/map transaction; the
  parent map plane's roll-back reset.
- Lane 5: the full saved-set fault campaign and the release bench.
- Still with #70 beyond lane 2's list: the targeted 1x1 cold cycle of every
  scalar group on silicon with restored PTOF on the wire; DR2c's firmware
  transaction limit; a matched post-place area comparison (no base sweep with
  this base's build inputs exists) and the 8x8 post-place obligation (open,
  blocked, not waived).
- From PR #133 for the bench: the DUT LeaveAll cadence against the reference
  switch and first-bind latency (#76, #606).
